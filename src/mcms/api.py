"""Purpose: local read-only HTTP API for MCMS/MSPEE element surfaces.

Governance scope: exposes existing validated element, snapshot, schema, and graph contracts.
Dependencies: Python standard-library HTTP server and local MSPEE APIs.
Invariants: API routes do not mutate state; every error response carries causal context.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from mcms.elements import (
    VALID_RELATION_TYPES,
    build_element_receipt,
    build_element_relation_graph,
    build_snapshot_receipt,
    element_schema_bundle,
    element_seed_json_schema,
    element_snapshot_json_schema,
    get_seed_element,
    get_snapshot_record,
    list_full_snapshot_records,
    list_seed_elements,
    validate_full_snapshot,
    validate_seed_pack,
)

API_STATUS = "mcms_local_api_ready"
API_VERSION = "0.1.0"


@dataclass(frozen=True)
class ApiResponse:
    status_code: int
    payload: dict[str, Any]

    def to_json_bytes(self) -> bytes:
        return json.dumps(self.payload, indent=2, sort_keys=True).encode("utf-8")


def _error_response(status_code: int, error: str, detail: str) -> ApiResponse:
    return ApiResponse(
        status_code=status_code,
        payload={
            "api_status": "mcms_local_api_error",
            "error": error,
            "detail": detail,
        },
    )


def _first_query_value(query: dict[str, list[str]], key: str) -> str | None:
    values = query.get(key, [])
    if not values:
        return None
    value = values[0].strip()
    return value or None


def _index_payload() -> dict[str, Any]:
    return {
        "api_status": API_STATUS,
        "api_version": API_VERSION,
        "routes": [
            "GET /health",
            "GET /elements",
            "GET /elements/{symbol|name|atomic_number}",
            "GET /snapshot",
            "GET /snapshot/{symbol|name|atomic_number}",
            "GET /schemas/{seed|snapshot|bundle}",
            "GET /graph",
            "GET /graph?symbol=Zn&relation=same_block",
        ],
        "relation_types": sorted(VALID_RELATION_TYPES),
    }


def _seed_list_payload() -> dict[str, Any]:
    elements = list_seed_elements()
    return {
        "api_status": API_STATUS,
        "count": len(elements),
        "symbols": [element.identity.symbol for element in elements],
        "validation": validate_seed_pack(elements).to_dict(),
    }


def _snapshot_list_payload() -> dict[str, Any]:
    records = list_full_snapshot_records()
    return {
        "api_status": API_STATUS,
        "count": len(records),
        "symbols": [record.symbol for record in records],
        "validation": validate_full_snapshot(records).to_dict(),
    }


def _schema_payload(schema_name: str) -> dict[str, Any]:
    schema_builders = {
        "seed": element_seed_json_schema,
        "snapshot": element_snapshot_json_schema,
        "bundle": element_schema_bundle,
    }
    if schema_name not in schema_builders:
        raise KeyError(f"unknown schema: {schema_name}")
    return {"api_status": API_STATUS, "schema": schema_builders[schema_name]()}


def _graph_payload(identifier: str | None, relation_type: str | None) -> dict[str, Any]:
    graph = build_element_relation_graph(identifier=identifier, relation_type=relation_type)
    return {"api_status": API_STATUS, "graph": graph.to_dict()}


def handle_api_request(method: str, raw_target: str) -> ApiResponse:
    if method.upper() != "GET":
        return _error_response(
            HTTPStatus.METHOD_NOT_ALLOWED,
            "method_not_allowed",
            "Only GET is supported by the local read-only API.",
        )

    parsed_target = urlparse(raw_target)
    path_parts = [
        unquote(part)
        for part in parsed_target.path.strip("/").split("/")
        if part
    ]
    query = parse_qs(parsed_target.query)

    try:
        if not path_parts:
            return ApiResponse(HTTPStatus.OK, _index_payload())
        if path_parts == ["health"]:
            return ApiResponse(
                HTTPStatus.OK,
                {
                    "api_status": API_STATUS,
                    "seed_count": len(list_seed_elements()),
                    "snapshot_count": len(list_full_snapshot_records()),
                },
            )
        if path_parts == ["elements"]:
            return ApiResponse(HTTPStatus.OK, _seed_list_payload())
        if len(path_parts) == 2 and path_parts[0] == "elements":
            element = get_seed_element(path_parts[1])
            return ApiResponse(
                HTTPStatus.OK,
                {
                    "api_status": API_STATUS,
                    "element": element.to_dict(),
                    "receipt": build_element_receipt(element),
                },
            )
        if path_parts == ["snapshot"]:
            return ApiResponse(HTTPStatus.OK, _snapshot_list_payload())
        if len(path_parts) == 2 and path_parts[0] == "snapshot":
            snapshot = get_snapshot_record(path_parts[1])
            return ApiResponse(
                HTTPStatus.OK,
                {
                    "api_status": API_STATUS,
                    "snapshot": snapshot.to_dict(),
                    "receipt": build_snapshot_receipt(snapshot),
                },
            )
        if len(path_parts) == 2 and path_parts[0] == "schemas":
            return ApiResponse(HTTPStatus.OK, _schema_payload(path_parts[1]))
        if path_parts == ["graph"]:
            return ApiResponse(
                HTTPStatus.OK,
                _graph_payload(
                    identifier=_first_query_value(query, "symbol"),
                    relation_type=_first_query_value(query, "relation"),
                ),
            )
        if len(path_parts) == 2 and path_parts[0] == "graph":
            return ApiResponse(
                HTTPStatus.OK,
                _graph_payload(
                    identifier=path_parts[1],
                    relation_type=_first_query_value(query, "relation"),
                ),
            )
    except KeyError as error:
        return _error_response(HTTPStatus.NOT_FOUND, "not_found", str(error))
    except ValueError as error:
        return _error_response(HTTPStatus.BAD_REQUEST, "bad_request", str(error))

    return _error_response(
        HTTPStatus.NOT_FOUND,
        "route_not_found",
        f"Unknown API route: {parsed_target.path}",
    )


class MCMSApiHandler(BaseHTTPRequestHandler):
    server_version = "MCMSLocalAPI/0.1"

    def do_GET(self) -> None:
        response = handle_api_request("GET", self.path)
        self._send_json_response(response, include_body=True)

    def do_HEAD(self) -> None:
        response = handle_api_request("GET", self.path)
        self._send_json_response(response, include_body=False)

    def do_POST(self) -> None:
        response = handle_api_request("POST", self.path)
        self._send_json_response(response, include_body=True)

    def _send_json_response(self, response: ApiResponse, *, include_body: bool) -> None:
        body = response.to_json_bytes()
        self.send_response(response.status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body) if include_body else 0))
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def build_api_server(host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), MCMSApiHandler)


def serve_api(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = build_api_server(host=host, port=port)
    print(f"MCMS local API listening on http://{host}:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m mcms.api")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    serve_api(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
