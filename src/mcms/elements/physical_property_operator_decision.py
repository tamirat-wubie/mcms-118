"""Purpose: record operator decision status for escalation recommendations.

Project scope: captures whether an operator has approved, rejected, or deferred
physical-property escalation recommendations.
Dependencies: physical-property escalation-resolution receipts.
Invariants: deferred operator decisions do not close gaps, apply final
resolutions, or mutate seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any

from mcms.elements.physical_property_escalation_resolution import (
    get_physical_property_escalation_resolution_receipt,
    list_physical_property_escalation_resolution_receipts,
)

VALID_OPERATOR_DECISION_STATUSES = {
    "operator_decision_deferred",
    "operator_resolution_approved",
    "operator_resolution_rejected",
}


@dataclass(frozen=True)
class PhysicalPropertyOperatorDecisionReceipt:
    receipt_id: str
    target_resolution_receipt_id: str
    symbol: str
    atomic_number: int
    field_name: str
    operator_decision_status: str
    decision_reason: str
    required_next_action: str
    final_resolution_applied: bool
    closes_gap: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "physical_property_operator_decision_receipt"
    notes: tuple[str, ...] = (
        "Deferred operator decisions preserve unresolved evidence boundaries.",
        "Only approved operator decisions may trigger later closure receipts.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        resolution = get_physical_property_escalation_resolution_receipt(
            self.target_resolution_receipt_id
        )
        if self.symbol != resolution.symbol:
            errors.append("operator decision symbol must match resolution receipt.")
        if self.atomic_number != resolution.atomic_number:
            errors.append("operator decision atomic number must match resolution receipt.")
        if self.field_name != resolution.field_name:
            errors.append("operator decision field must match resolution receipt.")
        if self.operator_decision_status not in VALID_OPERATOR_DECISION_STATUSES:
            errors.append("operator decision status is unknown.")
        if not self.decision_reason:
            errors.append("operator decision reason is required.")
        if not self.required_next_action:
            errors.append("operator decision next action is required.")
        if self.operator_decision_status == "operator_decision_deferred":
            if self.final_resolution_applied:
                errors.append("deferred operator decision must not apply final resolution.")
            if self.closes_gap:
                errors.append("deferred operator decision must not close gap.")
            if self.seed_mutation_allowed:
                errors.append("deferred operator decision must not allow seed mutation.")
        if self.final_resolution_applied and self.operator_decision_status != (
            "operator_resolution_approved"
        ):
            errors.append("final resolution requires operator approval.")
        if self.seed_mutation_allowed and not self.closes_gap:
            errors.append("seed mutation allowance requires gap closure.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["notes"] = list(self.notes)
        return payload


def _build_operator_decision_receipt(
    resolution_receipt_id: str,
) -> PhysicalPropertyOperatorDecisionReceipt:
    resolution = get_physical_property_escalation_resolution_receipt(resolution_receipt_id)
    return PhysicalPropertyOperatorDecisionReceipt(
        receipt_id=resolution.receipt_id.replace(
            "ESCALATION-RESOLUTION",
            "OPERATOR-DECISION",
        ),
        target_resolution_receipt_id=resolution.receipt_id,
        symbol=resolution.symbol,
        atomic_number=resolution.atomic_number,
        field_name=resolution.field_name,
        operator_decision_status="operator_decision_deferred",
        decision_reason=(
            "No explicit operator approval or rejection has been recorded for this "
            "physical-property recommendation."
        ),
        required_next_action=(
            "record operator approval, rejection, or continued-evidence decision before "
            "any final resolution is applied"
        ),
        final_resolution_applied=False,
    )


@lru_cache(maxsize=1)
def list_physical_property_operator_decision_receipts() -> tuple[
    PhysicalPropertyOperatorDecisionReceipt, ...
]:
    return tuple(
        _build_operator_decision_receipt(receipt.receipt_id)
        for receipt in list_physical_property_escalation_resolution_receipts()
    )


def _validate_operator_decision_with_resolution(
    receipt: PhysicalPropertyOperatorDecisionReceipt,
    resolution: Any | None,
) -> tuple[str, ...]:
    errors: list[str] = []
    if resolution is None:
        errors.append("operator decision target resolution is unknown.")
        return tuple(errors)
    if receipt.symbol != resolution.symbol:
        errors.append("operator decision symbol must match resolution receipt.")
    if receipt.atomic_number != resolution.atomic_number:
        errors.append("operator decision atomic number must match resolution receipt.")
    if receipt.field_name != resolution.field_name:
        errors.append("operator decision field must match resolution receipt.")
    if receipt.operator_decision_status not in VALID_OPERATOR_DECISION_STATUSES:
        errors.append("operator decision status is unknown.")
    if not receipt.decision_reason:
        errors.append("operator decision reason is required.")
    if not receipt.required_next_action:
        errors.append("operator decision next action is required.")
    if receipt.operator_decision_status == "operator_decision_deferred":
        if receipt.final_resolution_applied:
            errors.append("deferred operator decision must not apply final resolution.")
        if receipt.closes_gap:
            errors.append("deferred operator decision must not close gap.")
        if receipt.seed_mutation_allowed:
            errors.append("deferred operator decision must not allow seed mutation.")
    if (
        receipt.final_resolution_applied
        and receipt.operator_decision_status != "operator_resolution_approved"
    ):
        errors.append("final resolution requires operator approval.")
    if receipt.seed_mutation_allowed and not receipt.closes_gap:
        errors.append("seed mutation allowance requires gap closure.")
    return tuple(errors)


def get_physical_property_operator_decision_receipt(
    identifier: str | int,
) -> PhysicalPropertyOperatorDecisionReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_operator_decision_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_resolution_receipt_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property operator decision receipt: {identifier_text}")


def validate_physical_property_operator_decision_receipts(
    receipts: tuple[PhysicalPropertyOperatorDecisionReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts
        if receipts is not None
        else list_physical_property_operator_decision_receipts()
    )
    resolution_index = {
        resolution.receipt_id: resolution
        for resolution in list_physical_property_escalation_resolution_receipts()
    }
    invalid_receipts = tuple(
        receipt.receipt_id
        for receipt in checked_receipts
        if _validate_operator_decision_with_resolution(
            receipt,
            resolution_index.get(receipt.target_resolution_receipt_id),
        )
    )
    validation_status = "physical_property_operator_decision_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_operator_decision_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "deferred_decision_count": sum(
            1
            for receipt in checked_receipts
            if receipt.operator_decision_status == "operator_decision_deferred"
        ),
        "approved_resolution_count": sum(
            1
            for receipt in checked_receipts
            if receipt.operator_decision_status == "operator_resolution_approved"
        ),
        "rejected_resolution_count": sum(
            1
            for receipt in checked_receipts
            if receipt.operator_decision_status == "operator_resolution_rejected"
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
