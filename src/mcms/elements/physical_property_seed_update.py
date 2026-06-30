"""Purpose: record physical-property seed-update status after closure approval.

Project scope: models whether a reviewed physical-property value is allowed to
modify seed evidence.
Dependencies: physical-property closure approval receipts.
Invariants: deferred approval blocks seed update; blocked updates do not close
gaps or mutate records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_closure_approval import (
    get_physical_property_closure_approval_receipt,
)

VALID_PHYSICAL_PROPERTY_SEED_UPDATE_STATUSES = {
    "seed_update_blocked_by_deferred_approval",
    "seed_update_ready_to_apply",
    "seed_update_rejected",
}


@dataclass(frozen=True)
class PhysicalPropertySeedUpdateReceipt:
    receipt_id: str
    target_closure_approval_receipt_id: str
    symbol: str
    atomic_number: int
    field_name: str
    candidate_value: float
    candidate_unit: str
    update_status: str
    update_reason: str
    required_next_action: str
    closes_gap: bool
    seed_mutation_allowed: bool
    seed_update_applied: bool
    evidence_status: str = "physical_property_seed_update_receipt"
    notes: tuple[str, ...] = (
        "Seed-update receipts are the only receipt type allowed to report seed mutation.",
        "Blocked seed updates preserve the current seed record unchanged.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        approval = get_physical_property_closure_approval_receipt(
            self.target_closure_approval_receipt_id
        )
        if self.symbol != approval.symbol:
            errors.append("seed update symbol must match closure approval.")
        if self.atomic_number != approval.atomic_number:
            errors.append("seed update atomic number must match closure approval.")
        if self.field_name != approval.field_name:
            errors.append("seed update field must match closure approval.")
        if self.candidate_value != approval.candidate_value:
            errors.append("seed update value must match closure approval.")
        if self.candidate_unit != approval.candidate_unit:
            errors.append("seed update unit must match closure approval.")
        if self.update_status not in VALID_PHYSICAL_PROPERTY_SEED_UPDATE_STATUSES:
            errors.append("seed update status is unknown.")
        if not self.update_reason:
            errors.append("seed update reason is required.")
        if not self.required_next_action:
            errors.append("seed update next action is required.")
        if approval.approval_status == "closure_approval_deferred":
            if self.update_status != "seed_update_blocked_by_deferred_approval":
                errors.append("deferred approval must block seed update.")
            if self.closes_gap:
                errors.append("deferred approval seed update must not close gap.")
            if self.seed_mutation_allowed:
                errors.append("deferred approval seed update must not allow mutation.")
            if self.seed_update_applied:
                errors.append("deferred approval seed update must not be applied.")
        if self.seed_update_applied and not self.seed_mutation_allowed:
            errors.append("applied seed update requires mutation allowance.")
        if self.seed_mutation_allowed and not self.closes_gap:
            errors.append("seed mutation requires gap closure.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_seed_update_receipts() -> tuple[
    PhysicalPropertySeedUpdateReceipt, ...
]:
    approval = get_physical_property_closure_approval_receipt("Cf")
    return (
        PhysicalPropertySeedUpdateReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-SEED-UPDATE-Z098-Cf-density_value",
            target_closure_approval_receipt_id=approval.receipt_id,
            symbol=approval.symbol,
            atomic_number=approval.atomic_number,
            field_name=approval.field_name,
            candidate_value=approval.candidate_value,
            candidate_unit=approval.candidate_unit,
            update_status="seed_update_blocked_by_deferred_approval",
            update_reason=(
                "Cf density seed update is blocked because closure approval is deferred."
            ),
            required_next_action=(
                "issue an approved closure-approval receipt before allowing seed update"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
            seed_update_applied=False,
        ),
    )


def get_physical_property_seed_update_receipt(
    identifier: str | int,
) -> PhysicalPropertySeedUpdateReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_seed_update_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_closure_approval_receipt_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property seed-update receipt: {identifier_text}")


def validate_physical_property_seed_update_receipts(
    receipts: tuple[PhysicalPropertySeedUpdateReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_physical_property_seed_update_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_seed_update_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_seed_update_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "blocked_by_deferred_approval_count": sum(
            1
            for receipt in checked_receipts
            if receipt.update_status == "seed_update_blocked_by_deferred_approval"
        ),
        "ready_to_apply_count": sum(
            1
            for receipt in checked_receipts
            if receipt.update_status == "seed_update_ready_to_apply"
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "seed_update_applied_count": sum(
            1 for receipt in checked_receipts if receipt.seed_update_applied
        ),
        "invalid_receipts": invalid_receipts,
    }
