import json

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import (
    get_element_readiness_score,
    list_element_readiness_scores,
    validate_element_readiness_scores,
)
from mcms.elements.evidence import (
    get_element_evidence_console_record,
    list_element_evidence_console_records,
    validate_element_evidence_console_records,
)


def test_element_readiness_scores_partition_ready_and_blocked_elements():
    scores = list_element_readiness_scores()
    validation = validate_element_readiness_scores(scores)
    oxygen = get_element_readiness_score("O")
    technetium = get_element_readiness_score("Tc")
    radon = get_element_readiness_score("Rn")

    assert validation["validation_status"] == "element_readiness_scores_validated"
    assert validation["score_count"] == 118
    assert validation["ready_count"] == 54
    assert validation["blocked_by_isotope_evidence_count"] == 0
    assert validation["blocked_by_seed_and_matter_count"] == 64
    assert validation["high_priority_gap_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert oxygen.readiness_status == "atom_behavior_ready_from_evidence"
    assert oxygen.isotope_record_count == 3
    assert oxygen.atom_behavior_profile_count == 3
    assert oxygen.behavior_readiness_score == 1.0
    assert oxygen.constraint_tension_score == 0.0
    assert technetium.readiness_status == "atom_behavior_ready_from_evidence"
    assert technetium.source_policy_id is None
    assert technetium.isotope_record_count == 1
    assert technetium.atom_behavior_profile_count == 1
    assert technetium.behavior_readiness_score == 1.0
    assert technetium.constraint_tension_score == 0.0
    assert radon.readiness_status == "atom_behavior_blocked_by_seed_and_matter"
    assert radon.gap_priority_score == 0.5
    assert radon.constraint_tension_score == 1.0
    assert oxygen.validate() == []
    assert technetium.validate() == []
    assert radon.validate() == []


def test_local_api_exposes_readiness_score_routes():
    scores = handle_api_request("GET", "/scoring/readiness")
    oxygen = handle_api_request("GET", "/scoring/readiness/O")
    technetium = handle_api_request("GET", "/scoring/readiness/Tc")
    unknown = handle_api_request("GET", "/scoring/readiness/Xx")

    assert scores.status_code == 200
    assert scores.payload["validation"]["score_count"] == 118
    assert scores.payload["validation"]["ready_count"] == 54
    assert oxygen.status_code == 200
    assert oxygen.payload["score"]["readiness_status"] == "atom_behavior_ready_from_evidence"
    assert oxygen.payload["score"]["seed_mutation_allowed"] is False
    assert technetium.status_code == 200
    assert technetium.payload["score"]["readiness_status"] == (
        "atom_behavior_ready_from_evidence"
    )
    assert technetium.payload["score"]["source_policy_id"] is None
    assert unknown.status_code == 404


def test_element_cli_prints_readiness_scores(capsys):
    cmd_elements(
        symbol="Tc",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        readiness_score=True,
    )
    output = json.loads(capsys.readouterr().out)

    assert output["validation"]["score_count"] == 1
    assert output["validation"]["blocked_by_isotope_evidence_count"] == 0
    assert output["scores"][0]["symbol"] == "Tc"
    assert output["scores"][0]["gap_priority_score"] == 0.0
    assert output["scores"][0]["seed_mutation_allowed"] is False


def test_evidence_console_records_partition_element_lifecycle_state():
    records = list_element_evidence_console_records()
    validation = validate_element_evidence_console_records(records)
    oxygen = get_element_evidence_console_record("O")
    technetium = get_element_evidence_console_record("Tc")
    radon = get_element_evidence_console_record("Rn")

    assert validation["validation_status"] == "element_evidence_console_records_validated"
    assert validation["record_count"] == 118
    assert validation["canonical_evidence_ref_count"] == 281
    assert validation["candidate_evidence_ref_count"] == 8
    assert validation["unresolved_gap_ref_count"] == 200
    assert validation["admission_receipt_ref_count"] == 10
    assert validation["conflict_ref_count"] == 8
    assert validation["mutation_allowed_count"] == 0
    assert oxygen.canonical_evidence_count == 4
    assert oxygen.unresolved_gap_count == 1
    assert oxygen.admission_receipt_count == 1
    assert technetium.canonical_evidence_count == 2
    assert technetium.admission_receipt_count == 1
    assert radon.readiness_status == "atom_behavior_blocked_by_seed_and_matter"
    assert radon.promotion_decision_status == "promotion_ready_pending_approval"
    assert radon.unresolved_gap_count == 2
    assert radon.mutation_allowed is False


def test_local_api_and_cli_expose_evidence_console(capsys):
    api_record = handle_api_request("GET", "/evidence/console/O")
    missing = handle_api_request("GET", "/evidence/console/Xx")
    cmd_elements(
        symbol="O",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        evidence_console=True,
    )
    output = json.loads(capsys.readouterr().out)

    assert api_record.status_code == 200
    assert api_record.payload["record"]["canonical_evidence_count"] == 4
    assert api_record.payload["record"]["mutation_allowed"] is False
    assert missing.status_code == 404
    assert output["validation"]["record_count"] == 1
    assert output["records"][0]["symbol"] == "O"
    assert output["records"][0]["admission_receipt_count"] == 1
