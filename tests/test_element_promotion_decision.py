import pytest

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import (
    get_full_span_promotion_approval_review_receipt,
    get_partial_promotion_eligibility_receipt,
    get_promotion_batch_policy_receipt,
    get_promotion_decision_receipt,
    list_promotion_decision_receipts,
    validate_full_span_promotion_approval_review_receipt,
    validate_partial_promotion_eligibility_receipt,
    validate_promotion_batch_policy_receipt,
    validate_promotion_decision_receipts,
)


def test_promotion_decision_receipts_cover_cs_through_rn():
    receipts = list_promotion_decision_receipts()
    result = validate_promotion_decision_receipts(receipts)
    assert len(receipts) == 32
    assert result["validation_status"] == "promotion_decision_receipts_validated"
    assert result["receipt_count"] == 32
    assert result["ready_pending_approval_count"] == 32
    assert result["blocked_unresolved_physical_property_count"] == 0
    assert result["approved_for_seed_count"] == 0
    assert receipts[0].symbol == "Cs"
    assert receipts[-1].symbol == "Rn"


def test_promotion_decision_separates_ready_from_approved():
    gold = get_promotion_decision_receipt("Au")
    astatine = get_promotion_decision_receipt("At")
    assert gold.decision_status == "promotion_ready_pending_approval"
    assert gold.readiness_status == "promotion_ready"
    assert gold.unresolved_blockers == ()
    assert gold.approval_required is True
    assert astatine.decision_status == "promotion_ready_pending_approval"
    assert astatine.readiness_status == "promotion_ready"
    assert astatine.unresolved_blockers == ()
    assert astatine.validate() == []


def test_promotion_batch_policy_allows_full_span_approval_review():
    receipt = get_promotion_batch_policy_receipt()
    result = validate_promotion_batch_policy_receipt(receipt)
    assert result["validation_status"] == "promotion_batch_policy_receipt_validated"
    assert result["policy_status"] == "span_ready_for_approval"
    assert result["policy_decision"] == "allow_full_span_approval_review"
    assert result["ready_count"] == 32
    assert result["blocked_count"] == 0
    assert result["seed_mutation_allowed"] is False
    assert receipt.blocked_symbols == ()
    assert "contiguous_level_1_seed_span" in receipt.invariants_preserved


def test_partial_promotion_eligibility_exposes_review_queue_without_seed_mutation():
    receipt = get_partial_promotion_eligibility_receipt()
    result = validate_partial_promotion_eligibility_receipt(receipt)

    assert result["validation_status"] == "partial_promotion_eligibility_receipt_validated"
    assert result["eligible_count"] == 32
    assert result["blocked_count"] == 0
    assert result["partial_review_allowed"] is True
    assert result["seed_mutation_allowed"] is False
    assert receipt.eligibility_status == "partial_review_available_seed_mutation_blocked"
    assert receipt.eligible_symbols[0] == "Cs"
    assert receipt.eligible_symbols[-1] == "Rn"
    assert receipt.blocked_symbols == ()
    assert receipt.batch_policy_decision == "allow_full_span_approval_review"
    assert "no_partial_seed_hole" in receipt.invariants_preserved
    assert receipt.validate() == []


def test_full_span_promotion_approval_review_is_open_without_seed_mutation():
    receipt = get_full_span_promotion_approval_review_receipt()
    result = validate_full_span_promotion_approval_review_receipt(receipt)

    assert result["validation_status"] == (
        "full_span_promotion_approval_review_receipt_validated"
    )
    assert result["review_status"] == "full_span_approval_review_open"
    assert result["ready_count"] == 32
    assert result["blocked_count"] == 0
    assert result["approval_review_allowed"] is True
    assert result["seed_mutation_allowed"] is False
    assert receipt.ready_symbols[0] == "Cs"
    assert receipt.ready_symbols[-1] == "Rn"
    assert receipt.blocked_symbols == ()
    assert receipt.batch_policy_decision == "allow_full_span_approval_review"
    assert "approval_review_is_not_seed_mutation" in receipt.invariants_preserved
    assert receipt.validate() == []


def test_partial_promotion_eligibility_api_and_cli_are_read_only(capsys):
    response = handle_api_request("GET", "/promotion/partial-eligibility")
    review_response = handle_api_request("GET", "/promotion/full-span-approval-review")

    cmd_elements(
        symbol=None,
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        partial_promotion_eligibility=True,
    )
    partial_output = capsys.readouterr().out

    cmd_elements(
        symbol=None,
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        full_span_promotion_approval_review=True,
    )
    review_output = capsys.readouterr().out

    assert response.status_code == 200
    assert response.payload["validation"]["eligible_count"] == 32
    assert response.payload["receipt"]["blocked_symbols"] == []
    assert response.payload["receipt"]["seed_mutation_allowed"] is False
    assert review_response.status_code == 200
    assert review_response.payload["validation"]["review_status"] == (
        "full_span_approval_review_open"
    )
    assert review_response.payload["receipt"]["approval_review_allowed"] is True
    assert review_response.payload["receipt"]["seed_mutation_allowed"] is False
    assert '"partial_review_allowed": true' in partial_output
    assert '"seed_mutation_allowed": false' in partial_output
    assert '"approval_review_allowed": true' in review_output
    assert '"seed_mutation_allowed": false' in review_output


def test_local_api_index_exposes_full_span_approval_review():
    response = handle_api_request("GET", "/")
    assert response.status_code == 200
    assert "GET /promotion/full-span-approval-review" in response.payload["routes"]


def test_promotion_decision_rejects_out_of_span_lookup():
    with pytest.raises(KeyError):
        get_promotion_decision_receipt("Xe")
    with pytest.raises(KeyError):
        get_promotion_decision_receipt(54)
    with pytest.raises(KeyError):
        get_promotion_decision_receipt("Xx")
