from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mcms.api import handle_api_request  # noqa: E402
from mcms.elements import (  # noqa: E402
    build_element_dashboard_view_model,
    build_element_relation_graph,
    element_seed_json_schema,
    element_snapshot_json_schema,
    get_seed_element,
    get_snapshot_record,
    list_full_snapshot_records,
    list_seed_elements,
    validate_full_snapshot,
    validate_seed_pack,
)
from mcms.module_registry import all_modules  # noqa: E402
from mcms.phase_registry import list_phases  # noqa: E402

REQUIRED_KEYS = {
    "phase", "phase_id", "slug", "title", "status", "maturity", "domain", "layer",
    "objective", "capability_chain", "relationships", "boundary", "blocked_claims", "invariants",
    "claim_types", "evidence_policy", "risk_profile", "artifacts", "modules", "module_count",
    "status_vocabulary", "inputs", "outputs", "implementation_truth", "upgrade_path", "audit_metadata",
}

STANDARD_FILES = (
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/NAMING_STANDARD.md",
    "docs/STANDARDS_PROFILE.md",
)


def main() -> None:
    phases = list_phases()
    modules = all_modules()
    elements = list_seed_elements()
    snapshot_records = list_full_snapshot_records()
    element_seed_result = validate_seed_pack(elements)
    snapshot_result = validate_full_snapshot(snapshot_records)
    element_schema = element_seed_json_schema()
    snapshot_schema = element_snapshot_json_schema()
    element_schema_validator = Draft202012Validator(element_schema)
    snapshot_schema_validator = Draft202012Validator(snapshot_schema)
    assert len(phases) == 135, len(phases)
    assert len(modules) >= 180, len(modules)
    assert len(elements) == 36, len(elements)
    assert len(snapshot_records) == 118, len(snapshot_records)
    assert element_seed_result.validation_status == "element_seed_pack_validated", element_seed_result
    assert not element_seed_result.invalid_elements, element_seed_result.invalid_elements
    assert snapshot_result.validation_status == "full_element_snapshot_validated", snapshot_result
    assert not snapshot_result.invalid_elements, snapshot_result.invalid_elements
    Draft202012Validator.check_schema(element_schema)
    Draft202012Validator.check_schema(snapshot_schema)
    element_schema_validator.validate(json.loads(json.dumps(get_seed_element("Zn").to_dict())))
    oxygen = get_seed_element("O")
    calcium = get_seed_element("Ca")
    zinc = get_seed_element("Zn")
    krypton = get_seed_element("Kr")
    assert oxygen.state.data_level == 2, oxygen.state
    assert oxygen.state.oxidation_states == (-2,), oxygen.state
    assert oxygen.state.electronegativity_value == 3.44, oxygen.state
    assert "pubchem_periodic_table_properties" in oxygen.source_keys(), oxygen.source_keys()
    assert calcium.state.oxidation_states == (2,), calcium.state
    assert zinc.state.oxidation_states == (2,), zinc.state
    assert zinc.state.electronegativity_value == 1.65, zinc.state
    assert zinc.state.first_ionization_energy_ev is None, zinc.state
    assert zinc.state.bond_tendency_tags == (), zinc.state
    assert krypton.state.oxidation_states == (0,), krypton.state
    assert krypton.state.electronegativity_value == 3.00, krypton.state
    level_2_zinc_payload = json.loads(json.dumps(get_seed_element("Zn").to_dict()))
    level_2_zinc_payload["state"]["oxidation_states"] = [-2, 0, 2]
    level_2_zinc_payload["state"]["electronegativity_scale"] = "pauling"
    level_2_zinc_payload["state"]["electronegativity_value"] = 1.65
    level_2_zinc_payload["state"]["electronegativity_source_key"] = "level_2_reference_seed"
    level_2_zinc_payload["state"]["data_level"] = 2
    element_schema_validator.validate(level_2_zinc_payload)
    snapshot_schema_validator.validate(json.loads(json.dumps(get_snapshot_record("La").to_dict())))
    zinc_block_graph = build_element_relation_graph("Zn", relation_type="same_block")
    assert zinc_block_graph.graph_status == "element_relation_graph_exported", zinc_block_graph
    assert zinc_block_graph.query["node_count"] == 10, zinc_block_graph.query
    assert zinc_block_graph.query["edge_count"] == 9, zinc_block_graph.query
    api_health = handle_api_request("GET", "/health")
    api_graph = handle_api_request("GET", "/graph?symbol=Zn&relation=same_block")
    api_dashboard = handle_api_request("GET", "/dashboard/Zn?relation=same_block")
    dashboard = build_element_dashboard_view_model("Zn", relation_type="same_block")
    assert api_health.status_code == 200, api_health
    assert api_health.payload["seed_count"] == 36, api_health.payload
    assert api_graph.status_code == 200, api_graph
    assert api_graph.payload["graph"]["query"]["edge_count"] == 9, api_graph.payload
    assert api_dashboard.status_code == 200, api_dashboard
    assert api_dashboard.payload["dashboard"]["selected_element"]["symbol"] == "Zn", api_dashboard.payload
    assert dashboard.dashboard_status == "element_dashboard_view_model_ready", dashboard
    assert dashboard.selected_element is not None, dashboard
    assert dashboard.graph["query"]["edge_count"] == 9, dashboard.graph
    for phase in phases:
        missing = REQUIRED_KEYS - set(phase)
        assert not missing, (phase["phase"], sorted(missing))
        assert phase["phase_id"].startswith("MCMS-118-P")
        assert phase["artifacts"]["phase_metadata_json"]
        path = Path(phase["artifacts"]["phase_metadata_json"])
        assert path.exists(), path
        disk = json.loads(path.read_text())
        assert disk["phase"] == phase["phase"]
    print(
        f"phases={len(phases)} modules={len(modules)} "
        f"metadata_files={len(phases)} element_seeds={len(elements)} "
        f"element_snapshot_records={len(snapshot_records)}"
    )


def verify_standard_files() -> None:
    for standard_file in STANDARD_FILES:
        if not Path(standard_file).exists():
            raise SystemExit(f"missing standard file: {standard_file}")
    print("standard_files=ok")


if __name__ == "__main__":
    main()
    verify_standard_files()
