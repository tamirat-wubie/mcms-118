import json
import threading
from urllib.request import urlopen

from mcms.api import build_api_server, handle_api_request


def _payload(response):
    return response.payload


def test_local_api_health_and_index_routes_are_read_only_contracts():
    index = _payload(handle_api_request("GET", "/"))
    health = _payload(handle_api_request("GET", "/health"))
    method_error = handle_api_request("POST", "/health")
    assert index["api_status"] == "mcms_local_api_ready"
    assert "GET /elements/{symbol|name|atomic_number}" in index["routes"]
    assert "GET /reasoning/configuration/Cr" in index["routes"]
    assert "GET /phase3/f-block/U" in index["routes"]
    assert health["seed_count"] == 36
    assert health["snapshot_count"] == 118
    assert method_error.status_code == 405


def test_local_api_exposes_element_snapshot_and_schema_payloads():
    element = _payload(handle_api_request("GET", "/elements/Zn"))
    snapshot = _payload(handle_api_request("GET", "/snapshot/La"))
    schema = _payload(handle_api_request("GET", "/schemas/bundle"))
    assert element["element"]["identity"]["symbol"] == "Zn"
    assert element["receipt"]["validation_status"] == "element_seed_validated"
    assert snapshot["snapshot"]["group"] is None
    assert snapshot["receipt"]["validation_status"] == "element_snapshot_validated"
    assert "mullu_standard_symbolic_element" in schema["schema"]["schemas"]


def test_local_api_graph_query_and_error_paths_are_explicit():
    graph = _payload(handle_api_request("GET", "/graph?symbol=Zn&relation=same_block"))
    missing = handle_api_request("GET", "/elements/Xx")
    bad_relation = handle_api_request("GET", "/graph?symbol=Zn&relation=same_shell")
    assert graph["graph"]["query"]["symbol"] == "Zn"
    assert graph["graph"]["query"]["edge_count"] == 9
    assert missing.status_code == 404
    assert missing.payload["error"] == "not_found"
    assert bad_relation.status_code == 400
    assert bad_relation.payload["error"] == "bad_request"


def test_local_api_exposes_phase_2_reasoning_examples():
    chromium = _payload(handle_api_request("GET", "/reasoning/configuration/Cr"))
    similarity = _payload(handle_api_request("GET", "/reasoning/similarity?left=Cu&right=K"))
    missing_query = handle_api_request("GET", "/reasoning/similarity?left=Cu")
    assert chromium["reasoning"]["evidence"]["configuration_audit"]["is_exception"] is True
    assert chromium["reasoning"]["evidence"]["identity"]["proton_count"] == 24
    assert similarity["reasoning"]["evidence"]["surface_similarity"] is True
    assert similarity["reasoning"]["evidence"]["deep_similarity"] is False
    assert similarity["reasoning"]["answer_lines"][0] == "Partially, but not deeply."
    assert missing_query.status_code == 400


def test_local_api_exposes_phase_3_f_block_profiles():
    profiles = _payload(handle_api_request("GET", "/phase3/f-block"))
    uranium = _payload(handle_api_request("GET", "/phase3/f-block/U"))
    krypton = handle_api_request("GET", "/phase3/f-block/Kr")
    assert profiles["validation"]["profile_count"] == 30
    assert profiles["validation"]["lanthanide_count"] == 15
    assert profiles["validation"]["actinide_count"] == 15
    assert profiles["profiles"][0]["symbol"] == "La"
    assert uranium["profile"]["series"] == "actinide"
    assert uranium["profile"]["nuclear_state_extension_required"] is True
    assert krypton.status_code == 404


def test_local_api_http_server_serves_json_on_ephemeral_port():
    server = build_api_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urlopen(f"http://127.0.0.1:{server.server_port}/graph/Zn?relation=same_block") as response:
            payload = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
        assert payload["api_status"] == "mcms_local_api_ready"
        assert payload["graph"]["query"]["symbol"] == "Zn"
        assert payload["graph"]["query"]["edge_count"] == 9
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
