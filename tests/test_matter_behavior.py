import json

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import (
    build_matter_behavior_profile,
    list_matter_behavior_profiles,
    validate_matter_behavior_profiles,
)


def test_matter_behavior_profiles_combine_identity_evidence_and_inference():
    profiles = list_matter_behavior_profiles()
    validation = validate_matter_behavior_profiles(profiles)
    bromine = build_matter_behavior_profile("Br")
    iron = build_matter_behavior_profile("Fe")

    assert validation["validation_status"] == "matter_behavior_profiles_validated"
    assert validation["profile_count"] == 54
    assert validation["standard_states"] == ("Gas", "Liquid", "Solid")
    assert bromine.standard_state == "Liquid"
    assert "standard_state=Liquid" in bromine.measured_evidence_inputs
    assert "standard_state_liquid" in bromine.inferred_behavior_tags
    assert "low_boiling_boundary" in bromine.inferred_behavior_tags
    assert "high_density_boundary" in iron.inferred_behavior_tags
    assert bromine.validate() == []


def test_matter_behavior_profiles_keep_non_claims_explicit():
    copper = build_matter_behavior_profile("Cu")

    assert copper.profile_status == "matter_behavior_profile_v1"
    assert "profile does not predict reactions" in copper.non_claims
    assert "profile does not model compounds" in copper.non_claims
    assert "pubchem_periodic_table_properties" in copper.source_keys


def test_local_api_exposes_matter_behavior_profiles():
    profiles = handle_api_request("GET", "/matter/profiles")
    bromine = handle_api_request("GET", "/matter/profiles/Br")

    assert profiles.status_code == 200
    assert profiles.payload["validation"]["profile_count"] == 54
    assert bromine.status_code == 200
    assert bromine.payload["profile"]["standard_state"] == "Liquid"
    assert "low_boiling_boundary" in bromine.payload["profile"]["inferred_behavior_tags"]


def test_element_cli_prints_matter_behavior_profile(capsys):
    cmd_elements(
        symbol="Br",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        matter_profile=True,
    )
    output = json.loads(capsys.readouterr().out)

    assert output["profiles"][0]["symbol"] == "Br"
    assert output["profiles"][0]["standard_state"] == "Liquid"
    assert "density=3.11 g/cm^3" in output["profiles"][0]["measured_evidence_inputs"]
