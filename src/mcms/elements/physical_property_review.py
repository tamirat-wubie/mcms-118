"""Purpose: record pending review for secondary physical-property evidence.

Project scope: captures candidate values that are source-backed but still require
review before admission.
Dependencies: secondary evidence admission decisions.
Invariants: review receipts do not admit values, close gaps, or mutate seed
records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_admission import (
    get_physical_property_secondary_evidence_admission_decision,
)

VALID_PHYSICAL_PROPERTY_REVIEW_DECISIONS = {
    "blocked_pending_source_review",
    "resolved_admit_candidate",
    "resolved_reject_candidate",
}


@dataclass(frozen=True)
class PhysicalPropertyReviewReceipt:
    receipt_id: str
    target_admission_decision_id: str
    symbol: str
    atomic_number: int
    field_name: str
    candidate_source_key: str
    candidate_value: float
    candidate_unit: str
    corroborating_sources_checked: tuple[str, ...]
    review_summary: str
    review_decision: str
    review_reason: str
    required_next_action: str
    closes_gap: bool
    seed_mutation_allowed: bool
    evidence_status: str = "physical_property_review_receipt"
    notes: tuple[str, ...] = (
        "Review receipts are read-only evidence governance records.",
        "A candidate pending review remains unadmitted.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        admission = get_physical_property_secondary_evidence_admission_decision(
            self.target_admission_decision_id
        )
        if self.symbol != admission.symbol:
            errors.append("review receipt symbol must match admission decision.")
        if self.atomic_number != admission.atomic_number:
            errors.append("review receipt atomic number must match admission decision.")
        if self.field_name != admission.field_name:
            errors.append("review receipt field must match admission decision.")
        if self.candidate_source_key != admission.source_key:
            errors.append("review receipt source key must match admission decision.")
        if self.candidate_value != admission.candidate_value:
            errors.append("review receipt value must match admission decision.")
        if self.candidate_unit != admission.candidate_unit:
            errors.append("review receipt unit must match admission decision.")
        if admission.decision_status != "secondary_evidence_not_admitted_pending_review":
            errors.append("review receipt requires pending-review admission.")
        if not self.corroborating_sources_checked:
            errors.append("review receipt requires checked corroborating sources.")
        if not self.review_summary:
            errors.append("review receipt requires summary.")
        if self.review_decision not in VALID_PHYSICAL_PROPERTY_REVIEW_DECISIONS:
            errors.append("review decision is unknown.")
        if not self.review_reason:
            errors.append("review receipt requires reason.")
        if not self.required_next_action:
            errors.append("review receipt requires next action.")
        if self.closes_gap and self.review_decision != "resolved_admit_candidate":
            errors.append("only resolved admitted candidates may close a gap.")
        if self.seed_mutation_allowed:
            errors.append("review receipt must not allow seed mutation.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["corroborating_sources_checked"] = list(self.corroborating_sources_checked)
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_review_receipts() -> tuple[PhysicalPropertyReviewReceipt, ...]:
    admission = get_physical_property_secondary_evidence_admission_decision(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z098-Cf-density_value-RSC"
    )
    return (
        PhysicalPropertyReviewReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-REVIEW-Z098-Cf-density_value",
            target_admission_decision_id=admission.decision_id,
            symbol=admission.symbol,
            atomic_number=admission.atomic_number,
            field_name=admission.field_name,
            candidate_source_key=admission.source_key,
            candidate_value=admission.candidate_value,
            candidate_unit=admission.candidate_unit,
            corroborating_sources_checked=(
                "WebElements lists Cf density of solid as 15100 kg/m^3, normalized to 15.1 g/cm^3.",
            ),
            review_summary=(
                "RSC lists a Cf density candidate of 15.1 g/cm3, and WebElements "
                "corroborates the same normalized density value."
            ),
            review_decision="resolved_admit_candidate",
            review_reason=(
                "The Cf density candidate is corroborated at the secondary-source "
                "level but still requires governed gap-closure approval before "
                "seed mutation."
            ),
            required_next_action=(
                "prepare a governed gap-closure decision for Cf density or select "
                "a higher-precedence field-specific source before seed mutation"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
    )


def get_physical_property_review_receipt(
    identifier: str | int,
) -> PhysicalPropertyReviewReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_review_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_admission_decision_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property review receipt: {identifier_text}")


def validate_physical_property_review_receipts(
    receipts: tuple[PhysicalPropertyReviewReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = receipts if receipts is not None else list_physical_property_review_receipts()
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_review_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_review_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "blocked_pending_source_review_count": sum(
            1
            for receipt in checked_receipts
            if receipt.review_decision == "blocked_pending_source_review"
        ),
        "resolved_admit_candidate_count": sum(
            1 for receipt in checked_receipts if receipt.review_decision == "resolved_admit_candidate"
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
