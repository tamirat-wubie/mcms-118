"""Purpose: record corroboration review for secondary physical-property evidence.

Project scope: captures candidate values that need corroboration before
admission because available secondary references do not confirm a value.
Dependencies: secondary evidence admission decisions.
Invariants: corroboration receipts do not admit values, close gaps, or mutate
seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_admission import (
    get_physical_property_secondary_evidence_admission_decision,
)

VALID_CORROBORATION_REVIEW_DECISIONS = {
    "blocked_pending_corroborating_source",
    "resolved_admit_candidate",
    "resolved_reject_candidate",
}


@dataclass(frozen=True)
class PhysicalPropertyCorroborationReviewReceipt:
    receipt_id: str
    target_admission_decision_id: str
    symbol: str
    atomic_number: int
    field_name: str
    candidate_source_key: str
    candidate_value: float
    candidate_unit: str
    corroboration_sources_checked: tuple[str, ...]
    corroboration_summary: str
    review_decision: str
    review_reason: str
    required_next_action: str
    closes_gap: bool
    seed_mutation_allowed: bool
    evidence_status: str = "physical_property_corroboration_review_receipt"
    notes: tuple[str, ...] = (
        "Corroboration receipts are read-only evidence governance records.",
        "A candidate that lacks corroboration remains unadmitted.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        admission = get_physical_property_secondary_evidence_admission_decision(
            self.target_admission_decision_id
        )
        if self.symbol != admission.symbol:
            errors.append("corroboration receipt symbol must match admission decision.")
        if self.atomic_number != admission.atomic_number:
            errors.append("corroboration receipt atomic number must match admission decision.")
        if self.field_name != admission.field_name:
            errors.append("corroboration receipt field must match admission decision.")
        if self.candidate_source_key != admission.source_key:
            errors.append("corroboration receipt source key must match admission decision.")
        if self.candidate_value != admission.candidate_value:
            errors.append("corroboration receipt value must match admission decision.")
        if self.candidate_unit != admission.candidate_unit:
            errors.append("corroboration receipt unit must match admission decision.")
        if admission.decision_status != "secondary_evidence_not_admitted_needs_corroboration":
            errors.append("corroboration receipt requires corroboration-blocked admission.")
        if not self.corroboration_sources_checked:
            errors.append("corroboration receipt requires checked sources.")
        if not self.corroboration_summary:
            errors.append("corroboration receipt requires summary.")
        if self.review_decision not in VALID_CORROBORATION_REVIEW_DECISIONS:
            errors.append("corroboration review decision is unknown.")
        if not self.review_reason:
            errors.append("corroboration receipt requires review reason.")
        if not self.required_next_action:
            errors.append("corroboration receipt requires next action.")
        if self.closes_gap and self.review_decision != "resolved_admit_candidate":
            errors.append("only resolved admitted candidates may close a gap.")
        if self.seed_mutation_allowed:
            errors.append("corroboration receipt must not allow seed mutation.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["corroboration_sources_checked"] = list(self.corroboration_sources_checked)
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_corroboration_review_receipts() -> tuple[
    PhysicalPropertyCorroborationReviewReceipt, ...
]:
    berkelium_admission = get_physical_property_secondary_evidence_admission_decision("Bk")
    francium_density_admission = get_physical_property_secondary_evidence_admission_decision(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z087-Fr-density_value-WebElements"
    )
    californium_admission = get_physical_property_secondary_evidence_admission_decision(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z098-Cf-boiling_point_k-LANL"
    )
    einsteinium_admission = get_physical_property_secondary_evidence_admission_decision(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z099-Es-boiling_point_k-LANL"
    )
    return (
        PhysicalPropertyCorroborationReviewReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-CORROBORATION-REVIEW-Z087-Fr-density_value",
            target_admission_decision_id=francium_density_admission.decision_id,
            symbol=francium_density_admission.symbol,
            atomic_number=francium_density_admission.atomic_number,
            field_name=francium_density_admission.field_name,
            candidate_source_key=francium_density_admission.source_key,
            candidate_value=francium_density_admission.candidate_value,
            candidate_unit=francium_density_admission.candidate_unit,
            corroboration_sources_checked=(
                "RSC periodic table lists Fr density as unknown.",
            ),
            corroboration_summary=(
                "WebElements lists a Fr density candidate, but the checked RSC "
                "reference does not corroborate a numeric density value."
            ),
            review_decision="blocked_pending_corroborating_source",
            review_reason=(
                "The Fr density candidate has not been corroborated by a second "
                "field-specific source, so it cannot close the gap."
            ),
            required_next_action=(
                "find a corroborating field-specific source or record a rejection "
                "receipt before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertyCorroborationReviewReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-CORROBORATION-REVIEW-Z097-Bk-boiling_point_k",
            target_admission_decision_id=berkelium_admission.decision_id,
            symbol=berkelium_admission.symbol,
            atomic_number=berkelium_admission.atomic_number,
            field_name=berkelium_admission.field_name,
            candidate_source_key=berkelium_admission.source_key,
            candidate_value=berkelium_admission.candidate_value,
            candidate_unit=berkelium_admission.candidate_unit,
            corroboration_sources_checked=(
                "RSC periodic table lists Bk boiling point as unknown.",
            ),
            corroboration_summary=(
                "LANL lists a Bk boiling-point candidate, but the checked RSC "
                "reference does not corroborate a numeric boiling point."
            ),
            review_decision="blocked_pending_corroborating_source",
            review_reason=(
                "The Bk candidate has not been corroborated by a second "
                "field-specific source, so it cannot close the gap."
            ),
            required_next_action=(
                "find a corroborating field-specific source or record a rejection "
                "receipt before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertyCorroborationReviewReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-CORROBORATION-REVIEW-Z098-Cf-boiling_point_k",
            target_admission_decision_id=californium_admission.decision_id,
            symbol=californium_admission.symbol,
            atomic_number=californium_admission.atomic_number,
            field_name=californium_admission.field_name,
            candidate_source_key=californium_admission.source_key,
            candidate_value=californium_admission.candidate_value,
            candidate_unit=californium_admission.candidate_unit,
            corroboration_sources_checked=(
                "RSC periodic table lists Cf boiling point as unknown.",
            ),
            corroboration_summary=(
                "LANL lists a Cf boiling-point candidate, but the checked RSC "
                "reference does not corroborate a numeric boiling point."
            ),
            review_decision="blocked_pending_corroborating_source",
            review_reason=(
                "The Cf boiling-point candidate has not been corroborated by a "
                "second field-specific source, so it cannot close the gap."
            ),
            required_next_action=(
                "find a corroborating field-specific source or record a rejection "
                "receipt before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertyCorroborationReviewReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-CORROBORATION-REVIEW-Z099-Es-boiling_point_k",
            target_admission_decision_id=einsteinium_admission.decision_id,
            symbol=einsteinium_admission.symbol,
            atomic_number=einsteinium_admission.atomic_number,
            field_name=einsteinium_admission.field_name,
            candidate_source_key=einsteinium_admission.source_key,
            candidate_value=einsteinium_admission.candidate_value,
            candidate_unit=einsteinium_admission.candidate_unit,
            corroboration_sources_checked=(
                "RSC periodic table lists Es boiling point as unknown.",
            ),
            corroboration_summary=(
                "LANL lists an Es boiling-point candidate, but the checked RSC "
                "reference does not corroborate a numeric boiling point."
            ),
            review_decision="blocked_pending_corroborating_source",
            review_reason=(
                "The Es boiling-point candidate has not been corroborated by a "
                "second field-specific source, so it cannot close the gap."
            ),
            required_next_action=(
                "find a corroborating field-specific source or record a rejection "
                "receipt before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
    )


def get_physical_property_corroboration_review_receipt(
    identifier: str | int,
) -> PhysicalPropertyCorroborationReviewReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_corroboration_review_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_admission_decision_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property corroboration receipt: {identifier_text}")


def validate_physical_property_corroboration_review_receipts(
    receipts: tuple[PhysicalPropertyCorroborationReviewReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts
        if receipts is not None
        else list_physical_property_corroboration_review_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_corroboration_review_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_corroboration_review_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "blocked_pending_corroborating_source_count": sum(
            1
            for receipt in checked_receipts
            if receipt.review_decision == "blocked_pending_corroborating_source"
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
