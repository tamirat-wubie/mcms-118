import pytest

from mcms.elements import (
    get_promotion_batch_policy_receipt,
    get_promotion_decision_receipt,
    list_promotion_decision_receipts,
    validate_promotion_batch_policy_receipt,
    validate_promotion_decision_receipts,
)


def test_promotion_decision_receipts_cover_cs_through_rn():
    receipts = list_promotion_decision_receipts()
    result = validate_promotion_decision_receipts(receipts)
    assert len(receipts) == 32
    assert result["validation_status"] == "promotion_decision_receipts_validated"
    assert result["receipt_count"] == 32
    assert result["ready_pending_approval_count"] == 31
    assert result["blocked_unresolved_physical_property_count"] == 1
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
    assert astatine.decision_status == "promotion_blocked_unresolved_physical_property"
    assert astatine.readiness_status == "promotion_blocked_missing_source_evidence"
    assert astatine.unresolved_blockers == ("missing:complete_physical_property_evidence",)
    assert astatine.validate() == []


def test_promotion_batch_policy_holds_full_span_until_astatine_is_resolved():
    receipt = get_promotion_batch_policy_receipt()
    result = validate_promotion_batch_policy_receipt(receipt)
    assert result["validation_status"] == "promotion_batch_policy_receipt_validated"
    assert result["policy_status"] == "span_hold_pending_blocker_resolution"
    assert result["policy_decision"] == "hold_full_cs_rn_span"
    assert result["ready_count"] == 31
    assert result["blocked_count"] == 1
    assert result["seed_mutation_allowed"] is False
    assert receipt.blocked_symbols == ("At",)
    assert "contiguous_level_1_seed_span" in receipt.invariants_preserved


def test_promotion_decision_rejects_out_of_span_lookup():
    with pytest.raises(KeyError):
        get_promotion_decision_receipt("Xe")
    with pytest.raises(KeyError):
        get_promotion_decision_receipt(54)
    with pytest.raises(KeyError):
        get_promotion_decision_receipt("Xx")
