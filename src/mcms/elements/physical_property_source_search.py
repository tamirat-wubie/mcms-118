"""Purpose: record active source searches for physical-property gaps.

Project scope: creates governed search receipts for prioritized physical-property
gap work items before any candidate value is admitted.
Dependencies: physical-property gap workplan and secondary-source policy.
Invariants: source-search receipts do not contain measured values, close gaps, or
allow seed mutation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_gap_workplan import (
    get_physical_property_gap_work_item,
)
from mcms.elements.physical_property_source_policy import (
    get_physical_property_secondary_source_policy,
)

VALID_PHYSICAL_PROPERTY_SOURCE_SEARCH_STATUSES = {
    "source_search_open",
    "source_search_blocked",
    "source_search_complete_pending_receipt",
    "source_search_complete_candidate_receipt_created",
}


@dataclass(frozen=True)
class PhysicalPropertySourceSearchReceipt:
    search_id: str
    target_work_item_id: str
    target_gap_receipt_id: str
    symbol: str
    atomic_number: int
    field_name: str
    search_status: str
    candidate_source_keys: tuple[str, ...]
    required_evidence: tuple[str, ...]
    candidate_receipt_id: str | None
    search_reason: str
    required_next_action: str
    closes_gap: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "physical_property_source_search_receipt"
    notes: tuple[str, ...] = (
        "Source-search receipts track evidence work only.",
        "A source-search receipt does not contain or admit a physical-property value.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        work_item = get_physical_property_gap_work_item(self.target_work_item_id)
        policy = get_physical_property_secondary_source_policy(self.target_gap_receipt_id)
        policy_source_keys = {candidate.source_key for candidate in policy.candidate_sources}
        if self.symbol != work_item.symbol:
            errors.append("source-search symbol must match work item.")
        if self.atomic_number != work_item.atomic_number:
            errors.append("source-search atomic number must match work item.")
        if self.target_gap_receipt_id != work_item.target_gap_receipt_id:
            errors.append("source-search gap receipt must match work item.")
        if self.field_name not in work_item.missing_fields:
            errors.append("source-search field must be missing in the work item.")
        if work_item.work_status != "single_field_source_search":
            errors.append("source-search receipt requires single-field source-search work item.")
        if self.search_status not in VALID_PHYSICAL_PROPERTY_SOURCE_SEARCH_STATUSES:
            errors.append("source-search status is unknown.")
        if (
            self.search_status == "source_search_complete_candidate_receipt_created"
            and not self.candidate_receipt_id
        ):
            errors.append("completed source-search receipt requires candidate receipt id.")
        if not self.candidate_source_keys:
            errors.append("source-search receipt requires candidate source keys.")
        if not set(self.candidate_source_keys).issubset(policy_source_keys):
            errors.append("source-search candidate sources must be allowed by policy.")
        if "source_url_or_citation" not in self.required_evidence:
            errors.append("source-search receipt requires citation evidence.")
        if "unit_normalization_to_kelvin_or_g_per_cm3" not in self.required_evidence:
            errors.append("source-search receipt requires unit-normalization evidence.")
        if not self.search_reason:
            errors.append("source-search receipt requires a search reason.")
        if not self.required_next_action:
            errors.append("source-search receipt requires a next action.")
        if self.closes_gap:
            errors.append("source-search receipt must not close a gap.")
        if self.seed_mutation_allowed:
            errors.append("source-search receipt must not allow seed mutation.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidate_source_keys"] = list(self.candidate_source_keys)
        payload["required_evidence"] = list(self.required_evidence)
        payload["notes"] = list(self.notes)
        return payload


def _build_source_search_receipt(symbol: str) -> PhysicalPropertySourceSearchReceipt:
    work_item = get_physical_property_gap_work_item(symbol)
    policy = get_physical_property_secondary_source_policy(symbol)
    return PhysicalPropertySourceSearchReceipt(
        search_id=(
            f"MSPEE-PHYSICAL-PROPERTY-SOURCE-SEARCH-"
            f"Z{work_item.atomic_number:03d}-{work_item.symbol}-{work_item.missing_fields[0]}"
        ),
        target_work_item_id=work_item.work_item_id,
        target_gap_receipt_id=work_item.target_gap_receipt_id,
        symbol=work_item.symbol,
        atomic_number=work_item.atomic_number,
        field_name=work_item.missing_fields[0],
        search_status="source_search_open",
        candidate_source_keys=tuple(candidate.source_key for candidate in policy.candidate_sources),
        required_evidence=(
            "source_url_or_citation",
            "source_authority_and_version",
            "field_name_mapping",
            "unit_normalization_to_kelvin_or_g_per_cm3",
            "value_type_measured_estimated_or_predicted",
            "retrieval_date",
            "license_or_usage_boundary",
            "conflict_status",
        ),
        candidate_receipt_id=None,
        search_reason=(
            f"{work_item.symbol} has one unresolved physical-property field "
            f"({work_item.missing_fields[0]}) and no active conflict receipt."
        ),
        required_next_action=(
            "collect a field-specific source value and convert it into a secondary "
            "evidence receipt before admission review"
        ),
    )


def _build_completed_candidate_source_search_receipt(
    symbol: str,
) -> PhysicalPropertySourceSearchReceipt:
    receipt = _build_source_search_receipt(symbol)
    return PhysicalPropertySourceSearchReceipt(
        search_id=receipt.search_id,
        target_work_item_id=receipt.target_work_item_id,
        target_gap_receipt_id=receipt.target_gap_receipt_id,
        symbol=receipt.symbol,
        atomic_number=receipt.atomic_number,
        field_name=receipt.field_name,
        search_status="source_search_complete_candidate_receipt_created",
        candidate_source_keys=receipt.candidate_source_keys,
        required_evidence=receipt.required_evidence,
        candidate_receipt_id=(
            f"MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
            f"Z{receipt.atomic_number:03d}-{receipt.symbol}-{receipt.field_name}-LANL"
        ),
        search_reason=receipt.search_reason,
        required_next_action=(
            "review the candidate secondary evidence receipt for admission, conflict, "
            "or rejection"
        ),
    )


def list_physical_property_source_search_receipts() -> tuple[
    PhysicalPropertySourceSearchReceipt, ...
]:
    return (
        _build_completed_candidate_source_search_receipt("Pa"),
        _build_completed_candidate_source_search_receipt("Bk"),
    )


def get_physical_property_source_search_receipt(
    identifier: str | int,
) -> PhysicalPropertySourceSearchReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_source_search_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.target_gap_receipt_id
            or identifier_text == receipt.target_work_item_id
            or identifier_text == receipt.search_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property source-search receipt: {identifier_text}")


def validate_physical_property_source_search_receipts(
    receipts: tuple[PhysicalPropertySourceSearchReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_physical_property_source_search_receipts()
    )
    invalid_receipts = tuple(
        receipt.search_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_source_search_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_source_search_receipts_rejected"
    return {
        "validation_status": validation_status,
        "search_receipt_count": len(checked_receipts),
        "open_search_count": sum(
            1 for receipt in checked_receipts if receipt.search_status == "source_search_open"
        ),
        "candidate_receipt_created_count": sum(
            1
            for receipt in checked_receipts
            if receipt.search_status == "source_search_complete_candidate_receipt_created"
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
