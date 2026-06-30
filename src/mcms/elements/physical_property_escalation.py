"""Purpose: prioritize blocked physical-property evidence escalations.

Project scope: converts unresolved physical-property conflict, corroboration,
and approval blocks into operator-facing escalation receipts.
Dependencies: conflict, corroboration, and seed-update receipts.
Invariants: escalation receipts are planning metadata only; they do not close
gaps, admit values, or mutate seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_conflict import (
    get_physical_property_conflict_resolution_receipt,
    list_physical_property_conflict_resolution_receipts,
)
from mcms.elements.physical_property_corroboration import (
    get_physical_property_corroboration_review_receipt,
    list_physical_property_corroboration_review_receipts,
)
from mcms.elements.physical_property_seed_update import (
    get_physical_property_seed_update_receipt,
    list_physical_property_seed_update_receipts,
)

VALID_PHYSICAL_PROPERTY_ESCALATION_CLASSES = {
    "higher_precedence_source_required",
    "corroborating_source_required",
    "operator_approval_required",
}


@dataclass(frozen=True)
class PhysicalPropertyEscalationReceipt:
    receipt_id: str
    target_receipt_id: str
    symbol: str
    atomic_number: int
    field_name: str
    escalation_class: str
    escalation_reason: str
    required_next_action: str
    priority_rank: int
    closes_gap: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "physical_property_escalation_receipt"
    notes: tuple[str, ...] = (
        "Escalation receipts are planning metadata, not evidence admission.",
        "Escalation receipts preserve blocked status until a governed receipt resolves it.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.escalation_class not in VALID_PHYSICAL_PROPERTY_ESCALATION_CLASSES:
            errors.append("physical-property escalation class is unknown.")
        if not self.escalation_reason:
            errors.append("physical-property escalation reason is required.")
        if not self.required_next_action:
            errors.append("physical-property escalation next action is required.")
        if self.priority_rank < 0:
            errors.append("physical-property escalation priority must be non-negative.")
        if self.closes_gap:
            errors.append("physical-property escalation must not close a gap.")
        if self.seed_mutation_allowed:
            errors.append("physical-property escalation must not allow seed mutation.")
        if self.escalation_class == "higher_precedence_source_required":
            conflict = get_physical_property_conflict_resolution_receipt(
                self.target_receipt_id
            )
            if self.symbol != conflict.symbol or self.field_name != conflict.field_name:
                errors.append("conflict escalation target metadata mismatch.")
            if conflict.resolution_decision != "blocked_pending_higher_precedence_source":
                errors.append("conflict escalation requires a blocked conflict receipt.")
        if self.escalation_class == "corroborating_source_required":
            corroboration = get_physical_property_corroboration_review_receipt(
                self.target_receipt_id
            )
            if (
                self.symbol != corroboration.symbol
                or self.field_name != corroboration.field_name
            ):
                errors.append("corroboration escalation target metadata mismatch.")
            if corroboration.review_decision != "blocked_pending_corroborating_source":
                errors.append(
                    "corroboration escalation requires a blocked corroboration receipt."
                )
        if self.escalation_class == "operator_approval_required":
            seed_update = get_physical_property_seed_update_receipt(self.target_receipt_id)
            if self.symbol != seed_update.symbol or self.field_name != seed_update.field_name:
                errors.append("seed-update escalation target metadata mismatch.")
            if seed_update.update_status != "seed_update_blocked_by_deferred_approval":
                errors.append("approval escalation requires a blocked seed-update receipt.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["notes"] = list(self.notes)
        return payload


def _conflict_escalation_receipts() -> tuple[PhysicalPropertyEscalationReceipt, ...]:
    return tuple(
        PhysicalPropertyEscalationReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-ESCALATION-"
                f"Z{receipt.atomic_number:03d}-{receipt.symbol}-{receipt.field_name}"
            ),
            target_receipt_id=receipt.receipt_id,
            symbol=receipt.symbol,
            atomic_number=receipt.atomic_number,
            field_name=receipt.field_name,
            escalation_class="higher_precedence_source_required",
            escalation_reason=receipt.resolution_reason,
            required_next_action=receipt.required_next_action,
            priority_rank=0 if receipt.symbol == "At" else 1,
        )
        for receipt in list_physical_property_conflict_resolution_receipts()
    )


def _corroboration_escalation_receipts() -> tuple[
    PhysicalPropertyEscalationReceipt, ...
]:
    return tuple(
        PhysicalPropertyEscalationReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-ESCALATION-"
                f"Z{receipt.atomic_number:03d}-{receipt.symbol}-{receipt.field_name}"
            ),
            target_receipt_id=receipt.receipt_id,
            symbol=receipt.symbol,
            atomic_number=receipt.atomic_number,
            field_name=receipt.field_name,
            escalation_class="corroborating_source_required",
            escalation_reason=receipt.review_reason,
            required_next_action=receipt.required_next_action,
            priority_rank=2,
        )
        for receipt in list_physical_property_corroboration_review_receipts()
    )


def _approval_escalation_receipts() -> tuple[PhysicalPropertyEscalationReceipt, ...]:
    return tuple(
        PhysicalPropertyEscalationReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-ESCALATION-"
                f"Z{receipt.atomic_number:03d}-{receipt.symbol}-{receipt.field_name}"
            ),
            target_receipt_id=receipt.receipt_id,
            symbol=receipt.symbol,
            atomic_number=receipt.atomic_number,
            field_name=receipt.field_name,
            escalation_class="operator_approval_required",
            escalation_reason=receipt.update_reason,
            required_next_action=receipt.required_next_action,
            priority_rank=3,
        )
        for receipt in list_physical_property_seed_update_receipts()
    )


def list_physical_property_escalation_receipts() -> tuple[
    PhysicalPropertyEscalationReceipt, ...
]:
    return tuple(
        sorted(
            (
                *_conflict_escalation_receipts(),
                *_corroboration_escalation_receipts(),
                *_approval_escalation_receipts(),
            ),
            key=lambda receipt: (receipt.priority_rank, receipt.atomic_number),
        )
    )


def get_physical_property_escalation_receipt(
    identifier: str | int,
) -> PhysicalPropertyEscalationReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_escalation_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_receipt_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property escalation receipt: {identifier_text}")


def validate_physical_property_escalation_receipts(
    receipts: tuple[PhysicalPropertyEscalationReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_physical_property_escalation_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_escalation_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_escalation_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "higher_precedence_source_required_count": sum(
            1
            for receipt in checked_receipts
            if receipt.escalation_class == "higher_precedence_source_required"
        ),
        "corroborating_source_required_count": sum(
            1
            for receipt in checked_receipts
            if receipt.escalation_class == "corroborating_source_required"
        ),
        "operator_approval_required_count": sum(
            1
            for receipt in checked_receipts
            if receipt.escalation_class == "operator_approval_required"
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
