import json

import pytest

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import (
    build_isotope_candidate_evidence_template,
    get_isotope_candidate_admission_receipt,
    get_isotope_candidate_evidence_receipt,
    get_isotope_source_policy,
    get_isotope_source_search_receipt,
    list_isotope_candidate_admission_receipts,
    list_isotope_candidate_evidence_receipts,
    list_isotope_source_policies,
    list_isotope_source_search_receipts,
    validate_isotope_candidate_admission_receipts,
    validate_isotope_candidate_evidence_receipts,
    validate_isotope_source_policies,
    validate_isotope_source_search_receipts,
)


def test_isotope_source_policies_cover_isotope_only_atom_behavior_gaps():
    policies = list_isotope_source_policies()
    validation = validate_isotope_source_policies(policies)
    rubidium = get_isotope_source_policy("Rb")

    assert validation["validation_status"] == "isotope_source_policies_validated"
    assert validation["policy_count"] == 18
    assert validation["candidate_source_count"] == 3
    assert validation["primary_source_candidate_count"] == 2
    assert validation["bounded_secondary_candidate_count"] == 1
    assert validation["gap_closure_count"] == 0
    assert validation["atom_behavior_generation_allowed_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert rubidium.policy_id == "MSPEE-ISOTOPE-SOURCE-POLICY-Z037-Rb"
    assert rubidium.target_atom_behavior_gap_receipt_id == "MSPEE-ATOM-BEHAVIOR-GAP-Z037-Rb"
    assert rubidium.target_unresolved_isotope_receipt_id == (
        "MSPEE-Z037-Rb-isotope_evidence-unresolved"
    )
    assert rubidium.gap_closure_status == "gap_not_closed_by_policy"
    assert rubidium.atom_behavior_generation_allowed is False
    assert rubidium.seed_mutation_allowed is False
    assert rubidium.validate() == []


def test_isotope_source_policy_candidates_have_bounded_precedence():
    rubidium = get_isotope_source_policy("Rb")
    candidate_keys = {candidate.source_key for candidate in rubidium.candidate_sources}
    candidate_statuses = {candidate.candidate_status for candidate in rubidium.candidate_sources}

    assert candidate_keys == {
        "ciaaw_isotopic_compositions_2024",
        "nist_atomic_weights_isotopic_compositions",
        "pubchem_isotope_record_candidate",
    }
    assert candidate_statuses == {
        "primary_source_required",
        "bounded_secondary_source",
    }
    assert rubidium.source_precedence_order[0] == "primary_source_precedence"
    assert "conflict_receipt_if_sources_disagree" in rubidium.admission_requirements
    assert "operator_approval_before_profile_generation" in rubidium.admission_requirements


def test_isotope_source_policy_rejects_seed_and_matter_blocked_gaps():
    with pytest.raises(KeyError):
        get_isotope_source_policy("Rn")

    with pytest.raises(KeyError):
        get_isotope_source_policy("O")

    with pytest.raises(KeyError):
        get_isotope_source_policy("Li")

    with pytest.raises(KeyError):
        get_isotope_source_policy("Na")


def test_isotope_source_search_receipts_track_policy_work_without_values():
    receipts = list_isotope_source_search_receipts()
    validation = validate_isotope_source_search_receipts(receipts)
    rubidium = get_isotope_source_search_receipt("Rb")

    assert validation["validation_status"] == "isotope_source_search_receipts_validated"
    assert validation["search_receipt_count"] == 18
    assert validation["open_search_count"] == 18
    assert validation["candidate_receipt_created_count"] == 0
    assert validation["candidate_source_count"] == 3
    assert validation["gap_closure_count"] == 0
    assert validation["atom_behavior_generation_allowed_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert rubidium.search_id == "MSPEE-ISOTOPE-SOURCE-SEARCH-Z037-Rb"
    assert rubidium.policy_id == "MSPEE-ISOTOPE-SOURCE-POLICY-Z037-Rb"
    assert rubidium.search_status == "isotope_source_search_open"
    assert rubidium.candidate_receipt_id is None
    assert "mass_number" in rubidium.required_evidence
    assert "relative_atomic_mass" in rubidium.required_evidence
    assert "stable_or_radioactive_classification" in rubidium.required_evidence
    assert rubidium.closes_gap is False
    assert rubidium.atom_behavior_generation_allowed is False
    assert rubidium.seed_mutation_allowed is False
    assert rubidium.validate() == []


def test_isotope_candidate_evidence_is_empty_after_oxygen_admission():
    receipts = list_isotope_candidate_evidence_receipts()
    validation = validate_isotope_candidate_evidence_receipts(receipts)

    assert validation["validation_status"] == "isotope_candidate_evidence_receipts_validated"
    assert validation["receipt_count"] == 0
    assert validation["candidate_isotope_count"] == 0
    assert validation["stable_candidate_count"] == 0
    assert validation["radioisotope_candidate_count"] == 0
    assert validation["admitted_count"] == 0
    assert validation["gap_closure_count"] == 0
    assert validation["atom_behavior_generation_allowed_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    template = build_isotope_candidate_evidence_template("Rb")
    assert template["symbol"] == "Rb"
    assert template["default_admission_status"] == "isotope_evidence_candidate"
    with pytest.raises(KeyError):
        get_isotope_candidate_evidence_receipt("O")


def test_isotope_candidate_admission_records_oxygen_canonical_closure():
    receipts = list_isotope_candidate_admission_receipts()
    validation = validate_isotope_candidate_admission_receipts(receipts)
    oxygen = get_isotope_candidate_admission_receipt("O")

    assert validation["validation_status"] == "isotope_candidate_admission_receipts_validated"
    assert validation["receipt_count"] == 1
    assert validation["admitted_to_canonical_count"] == 1
    assert validation["admitted_isotope_count"] == 3
    assert validation["active_candidate_retained_count"] == 0
    assert validation["canonical_evidence_update_count"] == 1
    assert validation["atom_behavior_profiles_available_count"] == 1
    assert validation["seed_mutation_allowed_count"] == 0
    assert oxygen.receipt_id == "MSPEE-ISOTOPE-CANDIDATE-ADMISSION-Z008-O"
    assert oxygen.admitted_mass_numbers == (16, 17, 18)
    assert oxygen.active_candidate_receipt_retained is False
    assert oxygen.seed_mutation_allowed is False
    assert oxygen.validate() == []


def test_local_api_exposes_isotope_source_policy_routes():
    policies = handle_api_request("GET", "/atom/behavior/isotope-source-policy")
    rubidium = handle_api_request("GET", "/atom/behavior/isotope-source-policy/Rb")
    oxygen = handle_api_request("GET", "/atom/behavior/isotope-source-policy/O")
    radon = handle_api_request("GET", "/atom/behavior/isotope-source-policy/Rn")

    assert policies.status_code == 200
    assert policies.payload["validation"]["policy_count"] == 18
    assert rubidium.status_code == 200
    assert rubidium.payload["validation"]["policy_count"] == 1
    assert rubidium.payload["policy"]["symbol"] == "Rb"
    assert rubidium.payload["policy"]["atom_behavior_generation_allowed"] is False
    assert oxygen.status_code == 404
    assert radon.status_code == 404


def test_local_api_exposes_isotope_source_search_routes():
    receipts = handle_api_request("GET", "/atom/behavior/isotope-source-search")
    rubidium = handle_api_request("GET", "/atom/behavior/isotope-source-search/Rb")
    oxygen = handle_api_request("GET", "/atom/behavior/isotope-source-search/O")
    radon = handle_api_request("GET", "/atom/behavior/isotope-source-search/Rn")

    assert receipts.status_code == 200
    assert receipts.payload["validation"]["search_receipt_count"] == 18
    assert receipts.payload["validation"]["open_search_count"] == 18
    assert receipts.payload["validation"]["candidate_receipt_created_count"] == 0
    assert rubidium.status_code == 200
    assert rubidium.payload["validation"]["search_receipt_count"] == 1
    assert rubidium.payload["receipt"]["symbol"] == "Rb"
    assert rubidium.payload["receipt"]["search_status"] == "isotope_source_search_open"
    assert rubidium.payload["receipt"]["candidate_receipt_id"] is None
    assert rubidium.payload["receipt"]["atom_behavior_generation_allowed"] is False
    assert oxygen.status_code == 404
    assert radon.status_code == 404


def test_local_api_exposes_isotope_candidate_evidence_routes():
    receipts = handle_api_request("GET", "/atom/behavior/isotope-candidate-evidence")
    oxygen = handle_api_request("GET", "/atom/behavior/isotope-candidate-evidence/O")
    template = handle_api_request(
        "GET",
        "/atom/behavior/isotope-candidate-evidence/template/Rb",
    )
    radon = handle_api_request("GET", "/atom/behavior/isotope-candidate-evidence/Rn")

    assert receipts.status_code == 200
    assert receipts.payload["validation"]["receipt_count"] == 0
    assert receipts.payload["validation"]["candidate_isotope_count"] == 0
    assert oxygen.status_code == 404
    assert template.status_code == 200
    assert template.payload["template"]["symbol"] == "Rb"
    assert template.payload["template"]["seed_mutation_allowed"] is False
    assert radon.status_code == 404


def test_local_api_exposes_isotope_candidate_admission_routes():
    receipts = handle_api_request("GET", "/atom/behavior/isotope-candidate-admission")
    oxygen = handle_api_request("GET", "/atom/behavior/isotope-candidate-admission/O")
    rubidium = handle_api_request("GET", "/atom/behavior/isotope-candidate-admission/Rb")

    assert receipts.status_code == 200
    assert receipts.payload["validation"]["receipt_count"] == 1
    assert receipts.payload["validation"]["admitted_isotope_count"] == 3
    assert oxygen.status_code == 200
    assert oxygen.payload["receipt"]["symbol"] == "O"
    assert oxygen.payload["receipt"]["admission_status"] == (
        "isotope_candidate_admitted_to_canonical_evidence"
    )
    assert oxygen.payload["receipt"]["active_candidate_receipt_retained"] is False
    assert rubidium.status_code == 404


def test_element_cli_prints_isotope_source_policy(capsys):
    cmd_elements(
        symbol="Rb",
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
    assert output["policies"][0]["symbol"] == "Rb"
    assert output["policies"][0]["gap_closure_status"] == "gap_not_closed_by_policy"
    assert output["policies"][0]["seed_mutation_allowed"] is False


def test_element_cli_prints_isotope_source_search(capsys):
    cmd_elements(
        symbol="Rb",
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
    assert output["receipts"][0]["symbol"] == "Rb"
    assert output["receipts"][0]["search_status"] == "isotope_source_search_open"
    assert output["receipts"][0]["candidate_receipt_id"] is None
    assert output["receipts"][0]["seed_mutation_allowed"] is False


def test_element_cli_prints_isotope_candidate_evidence_and_template(capsys):
    cmd_elements(
        symbol=None,
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
        symbol="Rb",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        isotope_candidate_evidence_template=True,
    )
    template_output = json.loads(capsys.readouterr().out)

    assert evidence_output["validation"]["receipt_count"] == 0
    assert evidence_output["receipts"] == []
    assert template_output["template"]["symbol"] == "Rb"
    assert template_output["template"]["atom_behavior_generation_allowed"] is False


def test_element_cli_prints_isotope_candidate_admission(capsys):
    cmd_elements(
        symbol="O",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        isotope_candidate_admission=True,
    )
    output = json.loads(capsys.readouterr().out)

    assert output["validation"]["receipt_count"] == 1
    assert output["validation"]["admitted_isotope_count"] == 3
    assert output["receipts"][0]["symbol"] == "O"
    assert output["receipts"][0]["seed_mutation_allowed"] is False
