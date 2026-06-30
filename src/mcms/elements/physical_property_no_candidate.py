"""Purpose: record reviewed searches with no admissible physical-property candidate.

Project scope: captures partial-property targets where checked secondary sources
do not provide field-specific values.
Dependencies: partial physical-property source-search receipts.
Invariants: no-candidate receipts contain no substitute values, close no gaps,
and allow no seed mutation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_partial_search import (
    get_partial_physical_property_source_search_receipt,
)

VALID_NO_CANDIDATE_REVIEW_DECISIONS = {
    "blocked_no_admissible_candidate_found",
    "superseded_by_candidate_receipt",
}


@dataclass(frozen=True)
class PhysicalPropertyNoCandidateFieldReview:
    field_name: str
    checked_sources: tuple[str, ...]
    review_summary: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.field_name:
            errors.append("no-candidate field review requires field name.")
        if not self.checked_sources:
            errors.append("no-candidate field review requires checked sources.")
        if not self.review_summary:
            errors.append("no-candidate field review requires summary.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["checked_sources"] = list(self.checked_sources)
        return payload


@dataclass(frozen=True)
class PhysicalPropertyNoCandidateReviewReceipt:
    receipt_id: str
    target_search_id: str
    target_gap_receipt_id: str
    symbol: str
    atomic_number: int
    field_reviews: tuple[PhysicalPropertyNoCandidateFieldReview, ...]
    review_decision: str
    review_reason: str
    required_next_action: str
    closes_gap: bool
    seed_mutation_allowed: bool
    evidence_status: str = "physical_property_no_candidate_review_receipt"
    notes: tuple[str, ...] = (
        "No-candidate receipts are evidence governance records, not values.",
        "The physical-property gap remains open until admissible field evidence exists.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        search = get_partial_physical_property_source_search_receipt(self.target_search_id)
        reviewed_fields = tuple(review.field_name for review in self.field_reviews)
        if self.symbol != search.symbol:
            errors.append("no-candidate receipt symbol must match source-search receipt.")
        if self.atomic_number != search.atomic_number:
            errors.append("no-candidate receipt atomic number must match source-search receipt.")
        if self.target_gap_receipt_id != search.target_gap_receipt_id:
            errors.append("no-candidate receipt gap must match source-search receipt.")
        if reviewed_fields != search.missing_fields:
            errors.append("no-candidate receipt must review every missing field.")
        if self.review_decision not in VALID_NO_CANDIDATE_REVIEW_DECISIONS:
            errors.append("no-candidate review decision is unknown.")
        if not self.review_reason:
            errors.append("no-candidate receipt requires reason.")
        if not self.required_next_action:
            errors.append("no-candidate receipt requires next action.")
        for field_review in self.field_reviews:
            errors.extend(field_review.validate())
        if self.closes_gap:
            errors.append("no-candidate receipt must not close a gap.")
        if self.seed_mutation_allowed:
            errors.append("no-candidate receipt must not allow seed mutation.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["field_reviews"] = [review.to_dict() for review in self.field_reviews]
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_no_candidate_review_receipts() -> tuple[
    PhysicalPropertyNoCandidateReviewReceipt, ...
]:
    fermium_search = get_partial_physical_property_source_search_receipt("Fm")
    mendelevium_search = get_partial_physical_property_source_search_receipt("Md")
    nobelium_search = get_partial_physical_property_source_search_receipt("No")
    lawrencium_search = get_partial_physical_property_source_search_receipt("Lr")
    return (
        PhysicalPropertyNoCandidateReviewReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-NO-CANDIDATE-REVIEW-Z100-Fm",
            target_search_id=fermium_search.search_id,
            target_gap_receipt_id=fermium_search.target_gap_receipt_id,
            symbol=fermium_search.symbol,
            atomic_number=fermium_search.atomic_number,
            field_reviews=(
                PhysicalPropertyNoCandidateFieldReview(
                    field_name="boiling_point_k",
                    checked_sources=(
                        "LANL Periodic Table lists Fm boiling point as blank.",
                        "RSC Periodic Table lists Fm boiling point as unknown.",
                        "WebElements lists Fm boiling point as no data.",
                    ),
                    review_summary=(
                        "No checked candidate source provides an admissible Fm "
                        "boiling-point value."
                    ),
                ),
                PhysicalPropertyNoCandidateFieldReview(
                    field_name="density_value",
                    checked_sources=(
                        "RSC Periodic Table lists Fm density as unknown.",
                        "WebElements lists Fm density as no data.",
                    ),
                    review_summary=(
                        "No checked candidate source provides an admissible Fm "
                        "density value."
                    ),
                ),
            ),
            review_decision="blocked_no_admissible_candidate_found",
            review_reason=(
                "Fm remains unresolved because the checked secondary sources provide "
                "no admissible value for either missing field."
            ),
            required_next_action=(
                "keep the Fm physical-property gap open until a field-specific "
                "higher-precedence or admissible secondary source is found"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertyNoCandidateReviewReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-NO-CANDIDATE-REVIEW-Z101-Md",
            target_search_id=mendelevium_search.search_id,
            target_gap_receipt_id=mendelevium_search.target_gap_receipt_id,
            symbol=mendelevium_search.symbol,
            atomic_number=mendelevium_search.atomic_number,
            field_reviews=(
                PhysicalPropertyNoCandidateFieldReview(
                    field_name="boiling_point_k",
                    checked_sources=(
                        "LANL Periodic Table lists Md boiling point as blank.",
                        "RSC Periodic Table lists Md boiling point as unknown.",
                        "WebElements lists Md boiling point as no data.",
                    ),
                    review_summary=(
                        "No checked candidate source provides an admissible Md "
                        "boiling-point value."
                    ),
                ),
                PhysicalPropertyNoCandidateFieldReview(
                    field_name="density_value",
                    checked_sources=(
                        "RSC Periodic Table lists Md density as unknown.",
                        "WebElements lists Md density as no data.",
                    ),
                    review_summary=(
                        "No checked candidate source provides an admissible Md "
                        "density value."
                    ),
                ),
            ),
            review_decision="blocked_no_admissible_candidate_found",
            review_reason=(
                "Md remains unresolved because the checked secondary sources provide "
                "no admissible value for either missing field."
            ),
            required_next_action=(
                "keep the Md physical-property gap open until a field-specific "
                "higher-precedence or admissible secondary source is found"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertyNoCandidateReviewReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-NO-CANDIDATE-REVIEW-Z102-No",
            target_search_id=nobelium_search.search_id,
            target_gap_receipt_id=nobelium_search.target_gap_receipt_id,
            symbol=nobelium_search.symbol,
            atomic_number=nobelium_search.atomic_number,
            field_reviews=(
                PhysicalPropertyNoCandidateFieldReview(
                    field_name="boiling_point_k",
                    checked_sources=(
                        "LANL Periodic Table lists No boiling point as blank.",
                        "RSC Periodic Table lists No boiling point as unknown.",
                        "WebElements lists No boiling point as no data.",
                    ),
                    review_summary=(
                        "No checked candidate source provides an admissible No "
                        "boiling-point value."
                    ),
                ),
                PhysicalPropertyNoCandidateFieldReview(
                    field_name="density_value",
                    checked_sources=(
                        "RSC Periodic Table lists No density as unknown.",
                        "WebElements lists No density as no data.",
                    ),
                    review_summary=(
                        "No checked candidate source provides an admissible No "
                        "density value."
                    ),
                ),
            ),
            review_decision="blocked_no_admissible_candidate_found",
            review_reason=(
                "No remains unresolved because the checked secondary sources provide "
                "no admissible value for either missing field."
            ),
            required_next_action=(
                "keep the No physical-property gap open until a field-specific "
                "higher-precedence or admissible secondary source is found"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertyNoCandidateReviewReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-NO-CANDIDATE-REVIEW-Z103-Lr",
            target_search_id=lawrencium_search.search_id,
            target_gap_receipt_id=lawrencium_search.target_gap_receipt_id,
            symbol=lawrencium_search.symbol,
            atomic_number=lawrencium_search.atomic_number,
            field_reviews=(
                PhysicalPropertyNoCandidateFieldReview(
                    field_name="boiling_point_k",
                    checked_sources=(
                        "LANL Periodic Table lists Lr boiling point as blank.",
                        "RSC Periodic Table lists Lr boiling point as unknown.",
                        "WebElements lists Lr boiling point as no data.",
                    ),
                    review_summary=(
                        "No checked candidate source provides an admissible Lr "
                        "boiling-point value."
                    ),
                ),
                PhysicalPropertyNoCandidateFieldReview(
                    field_name="density_value",
                    checked_sources=(
                        "RSC Periodic Table lists Lr density as unknown.",
                        "WebElements lists Lr density as no data.",
                    ),
                    review_summary=(
                        "No checked candidate source provides an admissible Lr "
                        "density value."
                    ),
                ),
            ),
            review_decision="blocked_no_admissible_candidate_found",
            review_reason=(
                "Lr remains unresolved because the checked secondary sources provide "
                "no admissible value for either missing field."
            ),
            required_next_action=(
                "keep the Lr physical-property gap open until a field-specific "
                "higher-precedence or admissible secondary source is found"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
    )


def get_physical_property_no_candidate_review_receipt(
    identifier: str | int,
) -> PhysicalPropertyNoCandidateReviewReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_no_candidate_review_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_search_id
            or identifier_text == receipt.target_gap_receipt_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property no-candidate receipt: {identifier_text}")


def validate_physical_property_no_candidate_review_receipts(
    receipts: tuple[PhysicalPropertyNoCandidateReviewReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts
        if receipts is not None
        else list_physical_property_no_candidate_review_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_no_candidate_review_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_no_candidate_review_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "blocked_no_admissible_candidate_found_count": sum(
            1
            for receipt in checked_receipts
            if receipt.review_decision == "blocked_no_admissible_candidate_found"
        ),
        "field_review_count": sum(len(receipt.field_reviews) for receipt in checked_receipts),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
