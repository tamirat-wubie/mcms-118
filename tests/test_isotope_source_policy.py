import json

import pytest

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import (
    get_isotope_source_policy,
    list_isotope_source_policies,
    validate_isotope_source_policies,
)


def test_isotope_source_policies_cover_isotope_only_atom_behavior_gaps():
    policies = list_isotope_source_policies()
    validation = validate_isotope_source_policies(policies)
    oxygen = get_isotope_source_policy("O")

    assert validation["validation_status"] == "isotope_source_policies_validated"
    assert validation["policy_count"] == 52
    assert validation["candidate_source_count"] == 3
    assert validation["primary_source_candidate_count"] == 2
    assert validation["bounded_secondary_candidate_count"] == 1
    assert validation["gap_closure_count"] == 0
    assert validation["atom_behavior_generation_allowed_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert oxygen.policy_id == "MSPEE-ISOTOPE-SOURCE-POLICY-Z008-O"
    assert oxygen.target_atom_behavior_gap_receipt_id == "MSPEE-ATOM-BEHAVIOR-GAP-Z008-O"
    assert oxygen.target_unresolved_isotope_receipt_id == (
        "MSPEE-Z008-O-isotope_evidence-unresolved"
    )
    assert oxygen.gap_closure_status == "gap_not_closed_by_policy"
    assert oxygen.atom_behavior_generation_allowed is False
    assert oxygen.seed_mutation_allowed is False
    assert oxygen.validate() == []


def test_isotope_source_policy_candidates_have_bounded_precedence():
    oxygen = get_isotope_source_policy("O")
    candidate_keys = {candidate.source_key for candidate in oxygen.candidate_sources}
    candidate_statuses = {candidate.candidate_status for candidate in oxygen.candidate_sources}

    assert candidate_keys == {
        "ciaaw_isotopic_compositions_2024",
        "nist_atomic_weights_isotopic_compositions",
        "pubchem_isotope_record_candidate",
    }
    assert candidate_statuses == {
        "primary_source_required",
        "bounded_secondary_source",
    }
    assert oxygen.source_precedence_order[0] == "primary_source_precedence"
    assert "conflict_receipt_if_sources_disagree" in oxygen.admission_requirements
    assert "operator_approval_before_profile_generation" in oxygen.admission_requirements


def test_isotope_source_policy_rejects_seed_and_matter_blocked_gaps():
    with pytest.raises(KeyError):
        get_isotope_source_policy("Rn")


def test_local_api_exposes_isotope_source_policy_routes():
    policies = handle_api_request("GET", "/atom/behavior/isotope-source-policy")
    oxygen = handle_api_request("GET", "/atom/behavior/isotope-source-policy/O")
    radon = handle_api_request("GET", "/atom/behavior/isotope-source-policy/Rn")

    assert policies.status_code == 200
    assert policies.payload["validation"]["policy_count"] == 52
    assert oxygen.status_code == 200
    assert oxygen.payload["validation"]["policy_count"] == 1
    assert oxygen.payload["policy"]["symbol"] == "O"
    assert oxygen.payload["policy"]["atom_behavior_generation_allowed"] is False
    assert radon.status_code == 404


def test_element_cli_prints_isotope_source_policy(capsys):
    cmd_elements(
        symbol="O",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        isotope_source_policy=True,
    )
    output = json.loads(capsys.readouterr().out)

    assert output["validation"]["policy_count"] == 1
    assert output["policies"][0]["symbol"] == "O"
    assert output["policies"][0]["gap_closure_status"] == "gap_not_closed_by_policy"
    assert output["policies"][0]["seed_mutation_allowed"] is False
