"""Purpose: record active source searches for partial physical-property gaps.

Project scope: tracks unresolved records with two missing physical-property
fields so evidence work can proceed without importing values.
Dependencies: physical-property gap workplan and secondary-source policy.
Invariants: partial-source search receipts do not contain measured values, close
gaps, or allow seed mutation.
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

PARTIAL_PHYSICAL_PROPERTY_SEARCH_SYMBOLS = ("Fr", "Cf", "Es", "Fm", "Md", "No", "Lr")
VALID_PARTIAL_SOURCE_SEARCH_STATUSES = {
    "partial_source_search_open",
    "partial_source_search_blocked",
    "partial_source_search_complete_pending_receipts",
}


@dataclass(frozen=True)
class PartialPhysicalPropertyFieldSearch:
    field_name: str
    candidate_source_keys: tuple[str, ...]
    required_evidence: tuple[str, ...]

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.field_name:
            errors.append("partial field search requires field name.")
        if not self.candidate_source_keys:
            errors.append("partial field search requires candidate source keys.")
        if "source_url_or_citation" not in self.required_evidence:
            errors.append("partial field search requires citation evidence.")
        if "unit_normalization_to_kelvin_or_g_per_cm3" not in self.required_evidence:
            errors.append("partial field search requires unit-normalization evidence.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidate_source_keys"] = list(self.candidate_source_keys)
        payload["required_evidence"] = list(self.required_evidence)
        return payload


@dataclass(frozen=True)
class PartialPhysicalPropertySourceSearchReceipt:
    search_id: str
    target_work_item_id: str
    target_gap_receipt_id: str
    symbol: str
    atomic_number: int
    missing_fields: tuple[str, ...]
    field_searches: tuple[PartialPhysicalPropertyFieldSearch, ...]
    search_status: str
    search_reason: str
    required_next_action: str
    closes_gap: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "partial_physical_property_source_search_receipt"
    notes: tuple[str, ...] = (
        "Partial source-search receipts track evidence work only.",
        "Each missing field still requires a field-specific evidence receipt.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        work_item = get_physical_property_gap_work_item(self.target_work_item_id)
        policy = get_physical_property_secondary_source_policy(self.target_gap_receipt_id)
        candidate_by_key = {
            candidate.source_key: candidate for candidate in policy.candidate_sources
        }
        if self.symbol != work_item.symbol:
            errors.append("partial source-search symbol must match work item.")
        if self.atomic_number != work_item.atomic_number:
            errors.append("partial source-search atomic number must match work item.")
        if self.target_gap_receipt_id != work_item.target_gap_receipt_id:
            errors.append("partial source-search gap receipt must match work item.")
        if self.missing_fields != work_item.missing_fields:
            errors.append("partial source-search missing fields must match work item.")
        if work_item.work_status != "partial_property_source_search":
            errors.append("partial source-search requires partial-property work item.")
        if self.search_status not in VALID_PARTIAL_SOURCE_SEARCH_STATUSES:
            errors.append("partial source-search status is unknown.")
        if len(self.field_searches) != len(self.missing_fields):
            errors.append("partial source-search requires one field search per missing field.")
        for field_search in self.field_searches:
            errors.extend(field_search.validate())
            if field_search.field_name not in self.missing_fields:
                errors.append("partial field search field must be missing in work item.")
            for source_key in field_search.candidate_source_keys:
                candidate = candidate_by_key.get(source_key)
                if candidate is None:
                    errors.append("partial field search source must be policy candidate.")
                elif field_search.field_name not in candidate.allowed_fields:
                    errors.append("partial field search source must allow the target field.")
        if not self.search_reason:
            errors.append("partial source-search requires a search reason.")
        if not self.required_next_action:
            errors.append("partial source-search requires next action.")
        if self.closes_gap:
            errors.append("partial source-search receipt must not close a gap.")
        if self.seed_mutation_allowed:
            errors.append("partial source-search receipt must not allow seed mutation.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["missing_fields"] = list(self.missing_fields)
        payload["field_searches"] = [field_search.to_dict() for field_search in self.field_searches]
        payload["notes"] = list(self.notes)
        return payload


def _candidate_source_keys_for_field(field_name: str) -> tuple[str, ...]:
    if field_name == "density_value":
        return ("crc_handbook_candidate", "web_elements_candidate")
    return (
        "lanl_periodic_table_candidate",
        "nist_chemistry_webbook_candidate",
        "crc_handbook_candidate",
        "web_elements_candidate",
    )


def _build_partial_source_search_receipt(
    symbol: str,
) -> PartialPhysicalPropertySourceSearchReceipt:
    work_item = get_physical_property_gap_work_item(symbol)
    required_evidence = (
        "source_url_or_citation",
        "source_authority_and_version",
        "field_name_mapping",
        "unit_normalization_to_kelvin_or_g_per_cm3",
        "value_type_measured_estimated_or_predicted",
        "retrieval_date",
        "license_or_usage_boundary",
        "conflict_status",
    )
    return PartialPhysicalPropertySourceSearchReceipt(
        search_id=(
            f"MSPEE-PHYSICAL-PROPERTY-PARTIAL-SOURCE-SEARCH-"
            f"Z{work_item.atomic_number:03d}-{work_item.symbol}"
        ),
        target_work_item_id=work_item.work_item_id,
        target_gap_receipt_id=work_item.target_gap_receipt_id,
        symbol=work_item.symbol,
        atomic_number=work_item.atomic_number,
        missing_fields=work_item.missing_fields,
        field_searches=tuple(
            PartialPhysicalPropertyFieldSearch(
                field_name=field_name,
                candidate_source_keys=_candidate_source_keys_for_field(field_name),
                required_evidence=required_evidence,
            )
            for field_name in work_item.missing_fields
        ),
        search_status="partial_source_search_open",
        search_reason=(
            f"{work_item.symbol} has two unresolved physical-property fields and "
            "requires field-specific source evidence for each."
        ),
        required_next_action=(
            "collect separate field-specific source values for each missing field "
            "before creating candidate evidence receipts"
        ),
    )


def list_partial_physical_property_source_search_receipts() -> tuple[
    PartialPhysicalPropertySourceSearchReceipt, ...
]:
    return tuple(
        _build_partial_source_search_receipt(symbol)
        for symbol in PARTIAL_PHYSICAL_PROPERTY_SEARCH_SYMBOLS
    )


def get_partial_physical_property_source_search_receipt(
    identifier: str | int,
) -> PartialPhysicalPropertySourceSearchReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_partial_physical_property_source_search_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.target_gap_receipt_id
            or identifier_text == receipt.target_work_item_id
            or identifier_text == receipt.search_id
        ):
            return receipt
    raise KeyError(f"unknown partial physical-property source-search receipt: {identifier_text}")


def validate_partial_physical_property_source_search_receipts(
    receipts: tuple[PartialPhysicalPropertySourceSearchReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_partial_physical_property_source_search_receipts()
    )
    invalid_receipts = tuple(
        receipt.search_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "partial_physical_property_source_search_receipts_validated"
    if invalid_receipts:
        validation_status = "partial_physical_property_source_search_receipts_rejected"
    return {
        "validation_status": validation_status,
        "search_receipt_count": len(checked_receipts),
        "open_search_count": sum(
            1 for receipt in checked_receipts if receipt.search_status == "partial_source_search_open"
        ),
        "field_search_count": sum(len(receipt.field_searches) for receipt in checked_receipts),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
