import json

import pytest

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import (
    build_isotope_candidate_evidence_template,
    get_isotope_candidate_evidence_receipt,
    get_isotope_source_policy,
    get_isotope_source_search_receipt,
    list_isotope_candidate_evidence_receipts,
    list_isotope_source_policies,
    list_isotope_source_search_receipts,
    validate_isotope_candidate_evidence_receipts,
    validate_isotope_source_policies,
    validate_isotope_source_search_receipts,
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


def test_isotope_source_search_receipts_track_policy_work_without_values():
    receipts = list_isotope_source_search_receipts()
    validation = validate_isotope_source_search_receipts(receipts)
    oxygen = get_isotope_source_search_receipt("O")

    assert validation["validation_status"] == "isotope_source_search_receipts_validated"
    assert validation["search_receipt_count"] == 52
    assert validation["open_search_count"] == 51
    assert validation["candidate_receipt_created_count"] == 1
    assert validation["candidate_source_count"] == 3
    assert validation["gap_closure_count"] == 0
    assert validation["atom_behavior_generation_allowed_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert oxygen.search_id == "MSPEE-ISOTOPE-SOURCE-SEARCH-Z008-O"
    assert oxygen.policy_id == "MSPEE-ISOTOPE-SOURCE-POLICY-Z008-O"
    assert oxygen.search_status == "isotope_source_search_complete_candidate_receipt_created"
    assert oxygen.candidate_receipt_id == "MSPEE-ISOTOPE-CANDIDATE-EVIDENCE-Z008-O-NIST"
    assert "mass_number" in oxygen.required_evidence
    assert "relative_atomic_mass" in oxygen.required_evidence
    assert "stable_or_radioactive_classification" in oxygen.required_evidence
    assert oxygen.closes_gap is False
    assert oxygen.atom_behavior_generation_allowed is False
    assert oxygen.seed_mutation_allowed is False
    assert oxygen.validate() == []


def test_oxygen_isotope_candidate_evidence_stays_non_admitted():
    receipts = list_isotope_candidate_evidence_receipts()
    validation = validate_isotope_candidate_evidence_receipts(receipts)
    oxygen = get_isotope_candidate_evidence_receipt("O")
    template = build_isotope_candidate_evidence_template("O")

    assert validation["validation_status"] == "isotope_candidate_evidence_receipts_validated"
    assert validation["receipt_count"] == 1
    assert validation["candidate_isotope_count"] == 3
    assert validation["stable_candidate_count"] == 3
    assert validation["radioisotope_candidate_count"] == 0
    assert validation["admitted_count"] == 0
    assert validation["gap_closure_count"] == 0
    assert validation["atom_behavior_generation_allowed_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert oxygen.receipt_id == "MSPEE-ISOTOPE-CANDIDATE-EVIDENCE-Z008-O-NIST"
    assert oxygen.source_key == "nist_atomic_weights_isotopic_compositions"
    assert oxygen.admission_status == "isotope_evidence_candidate"
    assert oxygen.admission_decision == "awaiting_isotope_admission_review"
    assert tuple(value.mass_number for value in oxygen.candidate_values) == (16, 17, 18)
    assert oxygen.candidate_values[0].relative_atomic_mass == "15.99491461957(17)"
    assert oxygen.candidate_values[0].isotopic_composition == "0.99757(16)"
    assert oxygen.candidate_values[1].neutron_count == 9
    assert oxygen.candidate_values[2].stability_classification == "stable"
    assert oxygen.closes_gap is False
    assert oxygen.atom_behavior_generation_allowed is False
    assert oxygen.seed_mutation_allowed is False
    assert template["symbol"] == "O"
    assert template["default_admission_status"] == "isotope_evidence_candidate"
    assert oxygen.validate() == []


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


def test_local_api_exposes_isotope_source_search_routes():
    receipts = handle_api_request("GET", "/atom/behavior/isotope-source-search")
    oxygen = handle_api_request("GET", "/atom/behavior/isotope-source-search/O")
    radon = handle_api_request("GET", "/atom/behavior/isotope-source-search/Rn")

    assert receipts.status_code == 200
    assert receipts.payload["validation"]["search_receipt_count"] == 52
    assert receipts.payload["validation"]["open_search_count"] == 51
    assert receipts.payload["validation"]["candidate_receipt_created_count"] == 1
    assert oxygen.status_code == 200
    assert oxygen.payload["validation"]["search_receipt_count"] == 1
    assert oxygen.payload["receipt"]["symbol"] == "O"
    assert oxygen.payload["receipt"]["search_status"] == (
        "isotope_source_search_complete_candidate_receipt_created"
    )
    assert oxygen.payload["receipt"]["candidate_receipt_id"] == (
        "MSPEE-ISOTOPE-CANDIDATE-EVIDENCE-Z008-O-NIST"
    )
    assert oxygen.payload["receipt"]["atom_behavior_generation_allowed"] is False
    assert radon.status_code == 404


def test_local_api_exposes_isotope_candidate_evidence_routes():
    receipts = handle_api_request("GET", "/atom/behavior/isotope-candidate-evidence")
    oxygen = handle_api_request("GET", "/atom/behavior/isotope-candidate-evidence/O")
    template = handle_api_request(
        "GET",
        "/atom/behavior/isotope-candidate-evidence/template/O",
    )
    radon = handle_api_request("GET", "/atom/behavior/isotope-candidate-evidence/Rn")

    assert receipts.status_code == 200
    assert receipts.payload["validation"]["receipt_count"] == 1
    assert receipts.payload["validation"]["candidate_isotope_count"] == 3
    assert oxygen.status_code == 200
    assert oxygen.payload["receipt"]["symbol"] == "O"
    assert oxygen.payload["receipt"]["admission_status"] == "isotope_evidence_candidate"
    assert oxygen.payload["receipt"]["closes_gap"] is False
    assert template.status_code == 200
    assert template.payload["template"]["symbol"] == "O"
    assert template.payload["template"]["seed_mutation_allowed"] is False
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


def test_element_cli_prints_isotope_source_search(capsys):
    cmd_elements(
        symbol="O",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        isotope_source_search=True,
    )
    output = json.loads(capsys.readouterr().out)

    assert output["validation"]["search_receipt_count"] == 1
    assert output["receipts"][0]["symbol"] == "O"
    assert output["receipts"][0]["search_status"] == (
        "isotope_source_search_complete_candidate_receipt_created"
    )
    assert output["receipts"][0]["candidate_receipt_id"] == (
        "MSPEE-ISOTOPE-CANDIDATE-EVIDENCE-Z008-O-NIST"
    )
    assert output["receipts"][0]["seed_mutation_allowed"] is False


def test_element_cli_prints_isotope_candidate_evidence_and_template(capsys):
    cmd_elements(
        symbol="O",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        isotope_candidate_evidence=True,
    )
    evidence_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="O",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        isotope_candidate_evidence_template=True,
    )
    template_output = json.loads(capsys.readouterr().out)

    assert evidence_output["validation"]["receipt_count"] == 1
    assert evidence_output["receipts"][0]["symbol"] == "O"
    assert evidence_output["receipts"][0]["admission_status"] == (
        "isotope_evidence_candidate"
    )
    assert evidence_output["receipts"][0]["candidate_values"][0]["mass_number"] == 16
    assert template_output["template"]["symbol"] == "O"
    assert template_output["template"]["atom_behavior_generation_allowed"] is False
