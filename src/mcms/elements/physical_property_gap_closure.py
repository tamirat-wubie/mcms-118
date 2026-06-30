"""Purpose: decide whether reviewed secondary physical-property evidence may close a gap.

Project scope: records governed closure readiness for corroborated candidate
values without mutating seed records.
Dependencies: physical-property review receipts and gap audit receipts.
Invariants: closure decisions do not mutate seed records; pending approvals do
not close gaps.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_gap import get_physical_property_gap_audit_receipt
from mcms.elements.physical_property_review import get_physical_property_review_receipt

VALID_PHYSICAL_PROPERTY_GAP_CLOSURE_STATUSES = {
    "gap_closure_ready_pending_operator_approval",
    "gap_closure_approved_for_seed_update",
    "gap_closure_rejected",
}


@dataclass(frozen=True)
class PhysicalPropertyGapClosureDecision:
    decision_id: str
    target_review_receipt_id: str
    target_gap_receipt_id: str
    symbol: str
    atomic_number: int
    field_name: str
    candidate_value: float
    candidate_unit: str
    closure_status: str
    closure_reason: str
    required_next_action: str
    closes_gap: bool
    seed_mutation_allowed: bool
    evidence_status: str = "physical_property_gap_closure_decision"
    notes: tuple[str, ...] = (
        "Gap-closure decisions are separate from evidence review receipts.",
        "Pending closure approval does not mutate seed records.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        review = get_physical_property_review_receipt(self.target_review_receipt_id)
        gap = get_physical_property_gap_audit_receipt(self.target_gap_receipt_id)
        if review.review_decision != "resolved_admit_candidate":
            errors.append("gap closure decision requires a resolved admit-candidate review.")
        if self.symbol != review.symbol or self.symbol != gap.symbol:
            errors.append("gap closure symbol must match review and gap receipts.")
        if self.atomic_number != review.atomic_number or self.atomic_number != gap.atomic_number:
            errors.append("gap closure atomic number must match review and gap receipts.")
        if self.field_name != review.field_name:
            errors.append("gap closure field must match review receipt.")
        if self.field_name not in gap.missing_fields:
            errors.append("gap closure field must be missing in the target gap.")
        if self.candidate_value != review.candidate_value:
            errors.append("gap closure candidate value must match review receipt.")
        if self.candidate_unit != review.candidate_unit:
            errors.append("gap closure candidate unit must match review receipt.")
        if self.closure_status not in VALID_PHYSICAL_PROPERTY_GAP_CLOSURE_STATUSES:
            errors.append("gap closure status is unknown.")
        if not self.closure_reason:
            errors.append("gap closure decision requires reason.")
        if not self.required_next_action:
            errors.append("gap closure decision requires next action.")
        if self.closes_gap and self.closure_status != "gap_closure_approved_for_seed_update":
            errors.append("only approved closure decisions may close a gap.")
        if self.seed_mutation_allowed and not self.closes_gap:
            errors.append("seed mutation requires an approved gap closure.")
        if self.closure_status == "gap_closure_ready_pending_operator_approval":
            if self.closes_gap:
                errors.append("pending approval must not close a gap.")
            if self.seed_mutation_allowed:
                errors.append("pending approval must not allow seed mutation.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_gap_closure_decisions() -> tuple[
    PhysicalPropertyGapClosureDecision, ...
]:
    review = get_physical_property_review_receipt("Cf")
    gap = get_physical_property_gap_audit_receipt("Cf")
    return (
        PhysicalPropertyGapClosureDecision(
            decision_id="MSPEE-PHYSICAL-PROPERTY-GAP-CLOSURE-Z098-Cf-density_value",
            target_review_receipt_id=review.receipt_id,
            target_gap_receipt_id=gap.receipt_id,
            symbol=review.symbol,
            atomic_number=review.atomic_number,
            field_name=review.field_name,
            candidate_value=review.candidate_value,
            candidate_unit=review.candidate_unit,
            closure_status="gap_closure_ready_pending_operator_approval",
            closure_reason=(
                "Cf density has corroborated secondary evidence, but seed mutation "
                "requires explicit governed approval."
            ),
            required_next_action=(
                "approve or reject the Cf density gap closure through a governed "
                "seed-update receipt"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
    )


def get_physical_property_gap_closure_decision(
    identifier: str | int,
) -> PhysicalPropertyGapClosureDecision:
    identifier_text = str(identifier).strip()
    for decision in list_physical_property_gap_closure_decisions():
        if (
            identifier_text == str(decision.atomic_number)
            or identifier_text.upper() == decision.symbol.upper()
            or identifier_text == decision.decision_id
            or identifier_text == decision.target_review_receipt_id
            or identifier_text == decision.target_gap_receipt_id
        ):
            return decision
    raise KeyError(f"unknown physical-property gap-closure decision: {identifier_text}")


def validate_physical_property_gap_closure_decisions(
    decisions: tuple[PhysicalPropertyGapClosureDecision, ...] | None = None,
) -> dict[str, Any]:
    checked_decisions = (
        decisions if decisions is not None else list_physical_property_gap_closure_decisions()
    )
    invalid_decisions = tuple(
        decision.decision_id for decision in checked_decisions if decision.validate()
    )
    validation_status = "physical_property_gap_closure_decisions_validated"
    if invalid_decisions:
        validation_status = "physical_property_gap_closure_decisions_rejected"
    return {
        "validation_status": validation_status,
        "decision_count": len(checked_decisions),
        "ready_pending_operator_approval_count": sum(
            1
            for decision in checked_decisions
            if decision.closure_status == "gap_closure_ready_pending_operator_approval"
        ),
        "approved_for_seed_update_count": sum(
            1
            for decision in checked_decisions
            if decision.closure_status == "gap_closure_approved_for_seed_update"
        ),
        "gap_closure_count": sum(1 for decision in checked_decisions if decision.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for decision in checked_decisions if decision.seed_mutation_allowed
        ),
        "invalid_decisions": invalid_decisions,
    }
