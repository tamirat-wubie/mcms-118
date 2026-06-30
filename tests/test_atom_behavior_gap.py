import json

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import (
    get_atom_behavior_gap_receipt,
    get_atom_behavior_gap_work_item,
    list_atom_behavior_gap_receipts,
    list_atom_behavior_gap_work_items,
    validate_atom_behavior_gap_receipts,
    validate_atom_behavior_gap_work_items,
)


def test_atom_behavior_gap_receipts_make_missing_profile_coverage_explicit():
    receipts = list_atom_behavior_gap_receipts()
    validation = validate_atom_behavior_gap_receipts(receipts)
    gallium = get_atom_behavior_gap_receipt("Ga")
    radon = get_atom_behavior_gap_receipt("Rn")

    assert validation["validation_status"] == "atom_behavior_gap_receipts_validated"
    assert validation["receipt_count"] == 88
    assert validation["isotope_only_gap_count"] == 24
    assert validation["seed_and_matter_gap_count"] == 64
    assert validation["no_guess_policy_count"] == 88
    assert gallium.receipt_id == "MSPEE-ATOM-BEHAVIOR-GAP-Z031-Ga"
    assert gallium.target_unresolved_isotope_receipt_id == (
        "MSPEE-Z031-Ga-isotope_evidence-unresolved"
    )
    assert gallium.profile_blockers == ("isotope_evidence",)
    assert "stable_isotope_list" in gallium.missing_evidence
    assert gallium.no_guess_policy is True
    assert radon.profile_blockers == (
        "isotope_evidence",
        "level_1_seed_record",
        "matter_behavior_profile",
    )
    assert gallium.validate() == []
    assert radon.validate() == []


def test_atom_behavior_gap_work_items_prioritize_buildable_seed_span_first():
    items = list_atom_behavior_gap_work_items()
    validation = validate_atom_behavior_gap_work_items(items)
    gallium = get_atom_behavior_gap_work_item("Ga")
    radon = get_atom_behavior_gap_work_item("Rn")

    assert validation["validation_status"] == "atom_behavior_gap_work_items_validated"
    assert validation["work_item_count"] == 88
    assert validation["isotope_evidence_required_count"] == 24
    assert validation["seed_and_matter_profile_required_count"] == 64
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert items[0].symbol == "Ga"
    assert gallium.priority_rank == 0
    assert gallium.work_status == "isotope_evidence_required"
    assert radon.priority_rank == 1
    assert radon.work_status == "seed_and_matter_profile_required"
    assert radon.seed_mutation_allowed is False
    assert gallium.validate() == []
    assert radon.validate() == []


def test_local_api_exposes_atom_behavior_gap_routes():
    gaps = handle_api_request("GET", "/atom/behavior/gaps")
    gallium_gap = handle_api_request("GET", "/atom/behavior/gaps/Ga")
    workplan = handle_api_request("GET", "/atom/behavior/workplan")
    radon_work = handle_api_request("GET", "/atom/behavior/workplan/Rn")

    assert gaps.status_code == 200
    assert gaps.payload["validation"]["receipt_count"] == 88
    assert gallium_gap.status_code == 200
    assert gallium_gap.payload["receipt"]["profile_blockers"] == ["isotope_evidence"]
    assert workplan.status_code == 200
    assert workplan.payload["validation"]["work_item_count"] == 88
    assert radon_work.status_code == 200
    assert radon_work.payload["item"]["work_status"] == "seed_and_matter_profile_required"
    assert radon_work.payload["item"]["seed_mutation_allowed"] is False


def test_element_cli_prints_atom_behavior_gap_and_workplan(capsys):
    cmd_elements(
        symbol="Ga",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        atom_behavior_gap=True,
    )
    gap_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Rn",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        atom_behavior_workplan=True,
    )
    workplan_output = json.loads(capsys.readouterr().out)

    assert gap_output["validation"]["receipt_count"] == 1
    assert gap_output["receipts"][0]["symbol"] == "Ga"
    assert gap_output["receipts"][0]["profile_blockers"] == ["isotope_evidence"]
    assert workplan_output["validation"]["work_item_count"] == 1
    assert workplan_output["items"][0]["symbol"] == "Rn"
    assert workplan_output["items"][0]["work_status"] == "seed_and_matter_profile_required"
