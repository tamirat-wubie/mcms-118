"""Purpose: approve or defer physical-property gap-closure decisions.

Project scope: records final operator-approval status for reviewed closure
decisions without mutating seed records.
Dependencies: physical-property gap-closure decisions.
Invariants: deferred approval does not close gaps or allow seed mutation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_gap_closure import (
    get_physical_property_gap_closure_decision,
)

VALID_PHYSICAL_PROPERTY_CLOSURE_APPROVAL_STATUSES = {
    "closure_approval_deferred",
    "closure_approved_for_seed_update",
    "closure_rejected",
}


@dataclass(frozen=True)
class PhysicalPropertyClosureApprovalReceipt:
    receipt_id: str
    target_closure_decision_id: str
    symbol: str
    atomic_number: int
    field_name: str
    candidate_value: float
    candidate_unit: str
    approval_status: str
    approval_reason: str
    required_next_action: str
    closes_gap: bool
    seed_mutation_allowed: bool
    evidence_status: str = "physical_property_closure_approval_receipt"
    notes: tuple[str, ...] = (
        "Closure approval receipts are the final approval boundary before seed mutation.",
        "Deferred approvals preserve the unresolved source gap.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        decision = get_physical_property_gap_closure_decision(self.target_closure_decision_id)
        if decision.closure_status != "gap_closure_ready_pending_operator_approval":
            errors.append("closure approval requires a ready pending approval decision.")
        if self.symbol != decision.symbol:
            errors.append("closure approval symbol must match closure decision.")
        if self.atomic_number != decision.atomic_number:
            errors.append("closure approval atomic number must match closure decision.")
        if self.field_name != decision.field_name:
            errors.append("closure approval field must match closure decision.")
        if self.candidate_value != decision.candidate_value:
            errors.append("closure approval value must match closure decision.")
        if self.candidate_unit != decision.candidate_unit:
            errors.append("closure approval unit must match closure decision.")
        if self.approval_status not in VALID_PHYSICAL_PROPERTY_CLOSURE_APPROVAL_STATUSES:
            errors.append("closure approval status is unknown.")
        if not self.approval_reason:
            errors.append("closure approval reason is required.")
        if not self.required_next_action:
            errors.append("closure approval next action is required.")
        if self.approval_status == "closure_approval_deferred":
            if self.closes_gap:
                errors.append("deferred approval must not close a gap.")
            if self.seed_mutation_allowed:
                errors.append("deferred approval must not allow seed mutation.")
        if self.closes_gap and self.approval_status != "closure_approved_for_seed_update":
            errors.append("only approved closure may close a gap.")
        if self.seed_mutation_allowed and not self.closes_gap:
            errors.append("seed mutation requires gap closure.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_closure_approval_receipts() -> tuple[
    PhysicalPropertyClosureApprovalReceipt, ...
]:
    decision = get_physical_property_gap_closure_decision("Cf")
    return (
        PhysicalPropertyClosureApprovalReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-CLOSURE-APPROVAL-Z098-Cf-density_value",
            target_closure_decision_id=decision.decision_id,
            symbol=decision.symbol,
            atomic_number=decision.atomic_number,
            field_name=decision.field_name,
            candidate_value=decision.candidate_value,
            candidate_unit=decision.candidate_unit,
            approval_status="closure_approval_deferred",
            approval_reason=(
                "Cf density closure is ready, but seed mutation is deferred until "
                "an explicit operator approval event is issued."
            ),
            required_next_action=(
                "issue an approved or rejected closure approval receipt before "
                "changing seed physical-property evidence"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
    )


def get_physical_property_closure_approval_receipt(
    identifier: str | int,
) -> PhysicalPropertyClosureApprovalReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_closure_approval_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_closure_decision_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property closure approval receipt: {identifier_text}")


def validate_physical_property_closure_approval_receipts(
    receipts: tuple[PhysicalPropertyClosureApprovalReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_physical_property_closure_approval_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_closure_approval_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_closure_approval_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "deferred_approval_count": sum(
            1
            for receipt in checked_receipts
            if receipt.approval_status == "closure_approval_deferred"
        ),
        "approved_for_seed_update_count": sum(
            1
            for receipt in checked_receipts
            if receipt.approval_status == "closure_approved_for_seed_update"
        ),
        "rejected_count": sum(
            1 for receipt in checked_receipts if receipt.approval_status == "closure_rejected"
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
