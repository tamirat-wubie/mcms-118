from __future__ import annotations

import argparse
import json

from mcms.api import serve_api
from mcms.core.boundaries import compile_claim_boundary
from mcms.core.phases import latest_phase, load_phase_registry
from mcms.elements import (
    VALID_RELATION_TYPES,
    build_element_dashboard_view_model,
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
from mcms.release.robust_evidence_network import analyze_robust_evidence_network


def cmd_demo() -> None:
    claim = compile_claim_boundary("NaCl is a compound made of sodium and chlorine", "source_backed_claim", 0.8)
    evidence = analyze_robust_evidence_network("release/demo", evidence_strength=0.9)
    print(json.dumps({"claim": claim.to_dict(), "robust_evidence": evidence.to_dict()}, indent=2))


def cmd_phases() -> None:
    phases = load_phase_registry()
    print(json.dumps({"count": len(phases), "latest": latest_phase()}, indent=2))


def cmd_elements(
    symbol: str | None,
    list_only: bool,
    full_snapshot: bool,
    schema_name: str | None,
    graph_export: bool,
    dashboard_export: bool,
    relation_type: str | None,
) -> None:
    if schema_name:
        schema_builders = {
            "seed": element_seed_json_schema,
            "snapshot": element_snapshot_json_schema,
            "bundle": element_schema_bundle,
        }
        print(json.dumps(schema_builders[schema_name](), indent=2, sort_keys=True))
        return
    if dashboard_export:
        dashboard = build_element_dashboard_view_model(
            identifier=symbol,
            relation_type=relation_type,
        )
        print(json.dumps(dashboard.to_dict(), indent=2, sort_keys=True))
        return
    if graph_export:
        graph = build_element_relation_graph(identifier=symbol, relation_type=relation_type)
        print(json.dumps(graph.to_dict(), indent=2, sort_keys=True))
        return
    if full_snapshot:
        if list_only:
            records = list_full_snapshot_records()
            print(
                json.dumps(
                    {
                        "count": len(records),
                        "symbols": [record.symbol for record in records],
                        "validation": validate_full_snapshot(records).to_dict(),
                    },
                    indent=2,
                )
            )
            return
        if symbol:
            record = get_snapshot_record(symbol)
            print(
                json.dumps(
                    {
                        "snapshot": record.to_dict(),
                        "receipt": build_snapshot_receipt(record),
                    },
                    indent=2,
                )
            )
            return
        print(json.dumps(validate_full_snapshot().to_dict(), indent=2))
        return
    if list_only:
        elements = list_seed_elements()
        print(
            json.dumps(
                {
                    "count": len(elements),
                    "symbols": [element.identity.symbol for element in elements],
                    "validation": validate_seed_pack().to_dict(),
                },
                indent=2,
            )
        )
        return
    if symbol:
        element = get_seed_element(symbol)
        print(
            json.dumps(
                {
                    "element": element.to_dict(),
                    "receipt": build_element_receipt(element),
                },
                indent=2,
            )
        )
        return
    print(json.dumps(validate_seed_pack().to_dict(), indent=2))


def cmd_api(host: str, port: int) -> None:
    serve_api(host=host, port=port)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="mcms")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    sub.add_parser("phases")
    api_parser = sub.add_parser("api")
    api_parser.add_argument("--host", default="127.0.0.1")
    api_parser.add_argument("--port", type=int, default=8765)
    elements_parser = sub.add_parser("elements")
    elements_parser.add_argument("--symbol", help="Element symbol, name, or atomic number")
    elements_parser.add_argument("--list", action="store_true", help="List MSPEE seed elements")
    elements_parser.add_argument(
        "--full",
        action="store_true",
        help="Use the full 118-element identity snapshot instead of the Level 1 seed pack",
    )
    elements_parser.add_argument(
        "--schema",
        choices=("seed", "snapshot", "bundle"),
        help="Print the JSON Schema contract for seed records, snapshot records, or both",
    )
    elements_parser.add_argument(
        "--graph",
        action="store_true",
        help="Print the Level 1 element relation graph, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Print a dashboard-facing element read model, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--relation",
        choices=tuple(sorted(VALID_RELATION_TYPES)),
        help="Filter graph export by relation type",
    )
    args = parser.parse_args(argv)
    if args.cmd == "demo":
        cmd_demo()
    elif args.cmd == "phases":
        cmd_phases()
    elif args.cmd == "api":
        cmd_api(args.host, args.port)
    elif args.cmd == "elements":
        cmd_elements(
            args.symbol,
            args.list,
            args.full,
            args.schema,
            args.graph,
            args.dashboard,
            args.relation,
        )


if __name__ == "__main__":
    main()
