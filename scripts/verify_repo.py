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
    get_f_block_expansion_profile,
    get_seed_element,
    get_snapshot_record,
    list_f_block_expansion_profiles,
    list_full_snapshot_records,
    list_seed_elements,
    validate_f_block_expansion_profiles,
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
    f_block_profiles = list_f_block_expansion_profiles()
    f_block_result = validate_f_block_expansion_profiles(f_block_profiles)
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
    assert f_block_result.validation_status == "f_block_expansion_profiles_validated", f_block_result
    assert f_block_result.profile_count == 30, f_block_result
    assert f_block_result.lanthanide_count == 15, f_block_result
    assert f_block_result.actinide_count == 15, f_block_result
    Draft202012Validator.check_schema(element_schema)
    Draft202012Validator.check_schema(snapshot_schema)
    element_schema_validator.validate(json.loads(json.dumps(get_seed_element("Zn").to_dict())))
    oxygen = get_seed_element("O")
    calcium = get_seed_element("Ca")
    chromium = get_seed_element("Cr")
    copper = get_seed_element("Cu")
    zinc = get_seed_element("Zn")
    gallium = get_seed_element("Ga")
    krypton = get_seed_element("Kr")
    assert oxygen.state.data_level == 2, oxygen.state
    assert oxygen.state.oxidation_states == (-2,), oxygen.state
    assert oxygen.state.electronegativity_value == 3.44, oxygen.state
    assert "pubchem_periodic_table_properties" in oxygen.source_keys(), oxygen.source_keys()
    assert calcium.state.oxidation_states == (2,), calcium.state
    assert chromium.state.configuration_audit.is_exception is True, chromium.state
    assert chromium.state.configuration_audit.simple_aufbau_candidate == "[Ar] 3d^4 4s^2"
    assert chromium.state.frontier_signature.d_shell_stability == "half_filled_d_shell"
    assert copper.state.configuration_audit.is_exception is True, copper.state
    assert copper.state.configuration_audit.simple_aufbau_candidate == "[Ar] 3d^9 4s^2"
    assert copper.state.frontier_signature.d_shell_stability == "filled_d_shell"
    assert zinc.state.oxidation_states == (2,), zinc.state
    assert zinc.state.electronegativity_value == 1.65, zinc.state
    assert zinc.state.first_ionization_energy_ev == 9.394, zinc.state
    assert zinc.state.first_ionization_energy_source_key == "pubchem_periodic_table_properties"
    assert zinc.state.bond_tendency_tags == ("metallic_bonding", "coordination_complex")
    assert zinc.state.bond_tendency_source_key == "pubchem_periodic_table_properties"
    assert gallium.state.frontier_signature.d_shell == "3d^10", gallium.state
    assert gallium.state.frontier_signature.valence_model == "period_4_p_block_d_core"
    assert krypton.state.oxidation_states == (0,), krypton.state
    assert krypton.state.electronegativity_value == 3.00, krypton.state
    assert krypton.state.first_ionization_energy_ev == 14.000, krypton.state
    assert krypton.state.bond_tendency_tags == ("noble_gas_low_reactivity",)
    level_2_zinc_payload = json.loads(json.dumps(get_seed_element("Zn").to_dict()))
    level_2_zinc_payload["state"]["oxidation_states"] = [-2, 0, 2]
    level_2_zinc_payload["state"]["electronegativity_scale"] = "pauling"
    level_2_zinc_payload["state"]["electronegativity_value"] = 1.65
    level_2_zinc_payload["state"]["electronegativity_source_key"] = "level_2_reference_seed"
    level_2_zinc_payload["state"]["data_level"] = 2
    element_schema_validator.validate(level_2_zinc_payload)
    snapshot_schema_validator.validate(json.loads(json.dumps(get_snapshot_record("La").to_dict())))
    promethium_profile = get_f_block_expansion_profile("Pm")
    uranium_profile = get_f_block_expansion_profile("U")
    assert promethium_profile.series == "lanthanide", promethium_profile
    assert promethium_profile.f_shell_family == "4f", promethium_profile
    assert promethium_profile.radioactive_decay_relevance is True, promethium_profile
    assert promethium_profile.nuclear_state_extension_required is True, promethium_profile
    assert uranium_profile.series == "actinide", uranium_profile
    assert uranium_profile.f_shell_family == "5f", uranium_profile
    assert uranium_profile.actinide_instability_relevance is True, uranium_profile
    assert uranium_profile.heavy_element_uncertainty is True, uranium_profile
    zinc_block_graph = build_element_relation_graph("Zn", relation_type="same_block")
    assert zinc_block_graph.graph_status == "element_relation_graph_exported", zinc_block_graph
    assert zinc_block_graph.query["node_count"] == 10, zinc_block_graph.query
    assert zinc_block_graph.query["edge_count"] == 9, zinc_block_graph.query
    api_health = handle_api_request("GET", "/health")
    api_graph = handle_api_request("GET", "/graph?symbol=Zn&relation=same_block")
    api_dashboard = handle_api_request("GET", "/dashboard/Zn?relation=same_block")
    api_chromium_reasoning = handle_api_request("GET", "/reasoning/configuration/Cr")
    api_copper_potassium_reasoning = handle_api_request(
        "GET",
        "/reasoning/similarity?left=Cu&right=K",
    )
    api_f_block_profiles = handle_api_request("GET", "/phase3/f-block")
    api_uranium_profile = handle_api_request("GET", "/phase3/f-block/U")
    dashboard = build_element_dashboard_view_model("Zn", relation_type="same_block")
    assert api_health.status_code == 200, api_health
    assert api_health.payload["seed_count"] == 36, api_health.payload
    assert api_graph.status_code == 200, api_graph
    assert api_graph.payload["graph"]["query"]["edge_count"] == 9, api_graph.payload
    assert api_dashboard.status_code == 200, api_dashboard
    assert api_dashboard.payload["dashboard"]["selected_element"]["symbol"] == "Zn", api_dashboard.payload
    assert api_chromium_reasoning.status_code == 200, api_chromium_reasoning
    assert (
        api_chromium_reasoning.payload["reasoning"]["evidence"]["configuration_audit"][
            "is_exception"
        ]
        is True
    )
    assert api_copper_potassium_reasoning.status_code == 200, api_copper_potassium_reasoning
    assert (
        api_copper_potassium_reasoning.payload["reasoning"]["evidence"]["surface_similarity"]
        is True
    )
    assert (
        api_copper_potassium_reasoning.payload["reasoning"]["evidence"]["deep_similarity"]
        is False
    )
    assert api_f_block_profiles.status_code == 200, api_f_block_profiles
    assert api_f_block_profiles.payload["validation"]["profile_count"] == 30, (
        api_f_block_profiles.payload
    )
    assert api_uranium_profile.status_code == 200, api_uranium_profile
    assert api_uranium_profile.payload["profile"]["series"] == "actinide", api_uranium_profile.payload
    assert (
        api_uranium_profile.payload["profile"]["nuclear_state_extension_required"]
        is True
    )
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
        f"element_snapshot_records={len(snapshot_records)} "
        f"f_block_profiles={len(f_block_profiles)}"
    )


def verify_standard_files() -> None:
    for standard_file in STANDARD_FILES:
        if not Path(standard_file).exists():
            raise SystemExit(f"missing standard file: {standard_file}")
    print("standard_files=ok")


if __name__ == "__main__":
    main()
    verify_standard_files()
