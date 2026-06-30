"""Purpose: recommend outcomes for completed physical-property escalation searches.

Project scope: turns blocked source-investigation receipts into operator-facing
resolution recommendations without applying final decisions.
Dependencies: physical-property escalation-search receipts.
Invariants: recommendation receipts do not close gaps, admit/reject evidence as
final state, or mutate seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_escalation_search import (
    get_physical_property_escalation_search_receipt,
    list_physical_property_escalation_search_receipts,
)

VALID_ESCALATION_RESOLUTION_STATUSES = {
    "conflict_resolution_blocked_pending_operator_decision",
    "candidate_rejection_recommended_pending_operator_decision",
}


@dataclass(frozen=True)
class PhysicalPropertyEscalationResolutionReceipt:
    receipt_id: str
    target_search_id: str
    symbol: str
    atomic_number: int
    field_name: str
    resolution_status: str
    recommendation_reason: str
    required_next_action: str
    final_resolution_applied: bool
    closes_gap: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "physical_property_escalation_resolution_receipt"
    notes: tuple[str, ...] = (
        "Resolution recommendation receipts are not final operator decisions.",
        "A final approval or rejection requires a later explicit receipt.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        search = get_physical_property_escalation_search_receipt(self.target_search_id)
        if self.symbol != search.symbol:
            errors.append("resolution symbol must match escalation search.")
        if self.atomic_number != search.atomic_number:
            errors.append("resolution atomic number must match escalation search.")
        if self.field_name != search.field_name:
            errors.append("resolution field must match escalation search.")
        if self.resolution_status not in VALID_ESCALATION_RESOLUTION_STATUSES:
            errors.append("resolution status is unknown.")
        if not self.recommendation_reason:
            errors.append("resolution recommendation reason is required.")
        if not self.required_next_action:
            errors.append("resolution next action is required.")
        if self.final_resolution_applied:
            errors.append("recommendation receipt must not apply final resolution.")
        if self.closes_gap:
            errors.append("recommendation receipt must not close a gap.")
        if self.seed_mutation_allowed:
            errors.append("recommendation receipt must not allow seed mutation.")
        if (
            search.search_status == "higher_precedence_source_not_found"
            and self.resolution_status
            != "conflict_resolution_blocked_pending_operator_decision"
        ):
            errors.append("higher-precedence search requires blocked conflict resolution.")
        if (
            search.search_status == "corroborating_source_not_found"
            and self.resolution_status
            != "candidate_rejection_recommended_pending_operator_decision"
        ):
            errors.append(
                "failed corroboration search requires rejection recommendation."
            )
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["notes"] = list(self.notes)
        return payload


def _build_resolution_receipt(
    search_id: str,
) -> PhysicalPropertyEscalationResolutionReceipt:
    search = get_physical_property_escalation_search_receipt(search_id)
    if search.search_status == "higher_precedence_source_not_found":
        resolution_status = "conflict_resolution_blocked_pending_operator_decision"
        required_next_action = (
            "operator must either provide higher-precedence evidence or explicitly "
            "resolve the conflict before gap closure"
        )
    elif search.search_status == "corroborating_source_not_found":
        resolution_status = "candidate_rejection_recommended_pending_operator_decision"
        required_next_action = (
            "operator must approve candidate rejection or provide independent "
            "corroboration before admission"
        )
    else:
        raise ValueError(f"unsupported escalation search status: {search.search_status}")
    return PhysicalPropertyEscalationResolutionReceipt(
        receipt_id=search.search_id.replace(
            "ESCALATION-SEARCH",
            "ESCALATION-RESOLUTION",
        ),
        target_search_id=search.search_id,
        symbol=search.symbol,
        atomic_number=search.atomic_number,
        field_name=search.field_name,
        resolution_status=resolution_status,
        recommendation_reason=search.conclusion,
        required_next_action=required_next_action,
        final_resolution_applied=False,
    )


def list_physical_property_escalation_resolution_receipts() -> tuple[
    PhysicalPropertyEscalationResolutionReceipt, ...
]:
    return tuple(
        _build_resolution_receipt(search.search_id)
        for search in list_physical_property_escalation_search_receipts()
    )


def get_physical_property_escalation_resolution_receipt(
    identifier: str | int,
) -> PhysicalPropertyEscalationResolutionReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_escalation_resolution_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_search_id
        ):
            return receipt
    raise KeyError(
        f"unknown physical-property escalation resolution receipt: {identifier_text}"
    )


def validate_physical_property_escalation_resolution_receipts(
    receipts: tuple[PhysicalPropertyEscalationResolutionReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts
        if receipts is not None
        else list_physical_property_escalation_resolution_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_escalation_resolution_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_escalation_resolution_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "conflict_resolution_blocked_count": sum(
            1
            for receipt in checked_receipts
            if receipt.resolution_status
            == "conflict_resolution_blocked_pending_operator_decision"
        ),
        "candidate_rejection_recommended_count": sum(
            1
            for receipt in checked_receipts
            if receipt.resolution_status
            == "candidate_rejection_recommended_pending_operator_decision"
        ),
        "final_resolution_applied_count": sum(
            1 for receipt in checked_receipts if receipt.final_resolution_applied
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
