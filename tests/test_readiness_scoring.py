import json

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import (
    get_element_readiness_score,
    list_element_readiness_scores,
    validate_element_readiness_scores,
)


def test_element_readiness_scores_partition_ready_and_blocked_elements():
    scores = list_element_readiness_scores()
    validation = validate_element_readiness_scores(scores)
    oxygen = get_element_readiness_score("O")
    rubidium = get_element_readiness_score("Rb")
    radon = get_element_readiness_score("Rn")

    assert validation["validation_status"] == "element_readiness_scores_validated"
    assert validation["score_count"] == 118
    assert validation["ready_count"] == 36
    assert validation["blocked_by_isotope_evidence_count"] == 18
    assert validation["blocked_by_seed_and_matter_count"] == 64
    assert validation["high_priority_gap_count"] == 18
    assert validation["seed_mutation_allowed_count"] == 0
    assert oxygen.readiness_status == "atom_behavior_ready_from_evidence"
    assert oxygen.isotope_record_count == 3
    assert oxygen.atom_behavior_profile_count == 3
    assert oxygen.behavior_readiness_score == 1.0
    assert oxygen.constraint_tension_score == 0.0
    assert rubidium.readiness_status == "atom_behavior_blocked_by_isotope_evidence"
    assert rubidium.source_policy_id == "MSPEE-ISOTOPE-SOURCE-POLICY-Z037-Rb"
    assert rubidium.gap_priority_score == 1.0
    assert rubidium.constraint_tension_score == 0.9
    assert radon.readiness_status == "atom_behavior_blocked_by_seed_and_matter"
    assert radon.gap_priority_score == 0.5
    assert radon.constraint_tension_score == 1.0
    assert oxygen.validate() == []
    assert rubidium.validate() == []
    assert radon.validate() == []


def test_local_api_exposes_readiness_score_routes():
    scores = handle_api_request("GET", "/scoring/readiness")
    oxygen = handle_api_request("GET", "/scoring/readiness/O")
    rubidium = handle_api_request("GET", "/scoring/readiness/Rb")
    unknown = handle_api_request("GET", "/scoring/readiness/Xx")

    assert scores.status_code == 200
    assert scores.payload["validation"]["score_count"] == 118
    assert scores.payload["validation"]["ready_count"] == 36
    assert oxygen.status_code == 200
    assert oxygen.payload["score"]["readiness_status"] == "atom_behavior_ready_from_evidence"
    assert oxygen.payload["score"]["seed_mutation_allowed"] is False
    assert rubidium.status_code == 200
    assert rubidium.payload["score"]["readiness_status"] == (
        "atom_behavior_blocked_by_isotope_evidence"
    )
    assert rubidium.payload["score"]["source_policy_id"] == (
        "MSPEE-ISOTOPE-SOURCE-POLICY-Z037-Rb"
    )
    assert unknown.status_code == 404


def test_element_cli_prints_readiness_scores(capsys):
    cmd_elements(
        symbol="Rb",
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
    assert output["validation"]["blocked_by_isotope_evidence_count"] == 1
    assert output["scores"][0]["symbol"] == "Rb"
    assert output["scores"][0]["gap_priority_score"] == 1.0
    assert output["scores"][0]["seed_mutation_allowed"] is False
