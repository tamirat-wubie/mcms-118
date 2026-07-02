"""Purpose: prioritize unresolved physical-property evidence work.

Project scope: turns unresolved physical-property records into a deterministic
operator work queue without closing gaps or mutating seed records.
Dependencies: unresolved physical-property evidence, gap receipts, and conflict
receipts.
Invariants: workplan records are planning metadata only; they do not admit
secondary evidence, close gaps, or update element state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.evidence import (
    find_physical_property_evidence_record,
    find_unresolved_physical_property_evidence_record,
    list_unresolved_physical_property_evidence_records,
)
from mcms.elements.physical_property_conflict import (
    get_physical_property_conflict_resolution_receipt,
)
from mcms.elements.physical_property_gap import get_physical_property_gap_audit_receipt

VALID_PHYSICAL_PROPERTY_GAP_WORK_STATUSES = {
    "conflict_blocked_promotion",
    "conflict_resolved_for_promotion",
    "single_field_source_search",
    "partial_property_source_search",
    "synthetic_superheavy_uncertainty",
}


@dataclass(frozen=True)
class PhysicalPropertyGapWorkItem:
    work_item_id: str
    target_gap_receipt_id: str
    symbol: str
    atomic_number: int
    missing_fields: tuple[str, ...]
    present_field_count: int
    missing_field_count: int
    priority_rank: int
    work_status: str
    promotion_impact: str
    required_next_action: str
    closes_gap: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "physical_property_gap_work_item"
    notes: tuple[str, ...] = (
        "Gap work items are planning metadata, not evidence admission.",
        "Physical-property gaps remain open until governed evidence is admitted.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        gap_receipt = get_physical_property_gap_audit_receipt(self.target_gap_receipt_id)
        if self.symbol != gap_receipt.symbol:
            errors.append("gap work item symbol must match gap receipt.")
        if self.atomic_number != gap_receipt.atomic_number:
            errors.append("gap work item atomic number must match gap receipt.")
        if self.missing_fields != gap_receipt.missing_fields:
            errors.append("gap work item missing fields must match gap receipt.")
        if self.missing_field_count != len(self.missing_fields):
            errors.append("gap work item missing-field count is inconsistent.")
        if self.present_field_count < 0:
            errors.append("gap work item present-field count must be non-negative.")
        if self.priority_rank < 0:
            errors.append("gap work item priority rank must be non-negative.")
        if self.work_status not in VALID_PHYSICAL_PROPERTY_GAP_WORK_STATUSES:
            errors.append("gap work item status is unknown.")
        if self.closes_gap:
            errors.append("gap work item must not close a gap.")
        if self.seed_mutation_allowed:
            errors.append("gap work item must not allow seed mutation.")
        if not self.required_next_action:
            errors.append("gap work item requires a next action.")
        if self.symbol == "At":
            conflict = get_physical_property_conflict_resolution_receipt("At")
            if conflict.resolution_decision not in {
                "blocked_pending_higher_precedence_source",
                "resolved_admit_candidate",
            }:
                errors.append("At work item must align with conflict receipt.")
            if (
                "Cs-Rn" in gap_receipt.blocks_promotion_spans
                and self.work_status != "conflict_blocked_promotion"
            ):
                errors.append("At promotion-blocking work item must remain conflict-blocked.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["missing_fields"] = list(self.missing_fields)
        payload["notes"] = list(self.notes)
        return payload


def _present_field_count(record: Any) -> int:
    return sum(
        1
        for value in (
            record.standard_state,
            record.melting_point_k,
            record.boiling_point_k,
            record.density_value,
        )
        if value is not None
    )


def _classify_work_item(record: Any) -> tuple[int, str, str, str]:
    if record.symbol == "At":
        try:
            find_physical_property_evidence_record("At")
        except KeyError:
            has_admitted_astatine_evidence = False
        else:
            has_admitted_astatine_evidence = True
        if has_admitted_astatine_evidence:
            return (
                0,
                "conflict_resolved_for_promotion",
                "PubChem source gap remains, but Cs-Rn promotion blocker is closed",
                "monitor PubChem for a complete At row while retaining admitted secondary evidence",
            )
        return (
            0,
            "conflict_blocked_promotion",
            "blocks Cs-Rn seed promotion",
            "resolve At boiling-point conflict receipt with higher-precedence evidence",
        )
    if len(record.missing_fields) == 1:
        return (
            1,
            "single_field_source_search",
            "does not currently block Cs-Rn promotion",
            "collect one field-specific authoritative or governed secondary value",
        )
    if len(record.missing_fields) == 2:
        return (
            2,
            "partial_property_source_search",
            "future heavy-element property completion",
            "collect boiling-point and density evidence before admission review",
        )
    return (
        3,
        "synthetic_superheavy_uncertainty",
        "future synthetic-element uncertainty governance",
        "record measured, estimated, or predicted values with explicit uncertainty class",
    )


def _build_gap_work_item(record: Any) -> PhysicalPropertyGapWorkItem:
    priority_rank, work_status, promotion_impact, required_next_action = _classify_work_item(
        record
    )
    gap_receipt = get_physical_property_gap_audit_receipt(record.symbol)
    return PhysicalPropertyGapWorkItem(
        work_item_id=(
            f"MSPEE-PHYSICAL-PROPERTY-GAP-WORK-Z{record.atomic_number:03d}-{record.symbol}"
        ),
        target_gap_receipt_id=gap_receipt.receipt_id,
        symbol=record.symbol,
        atomic_number=record.atomic_number,
        missing_fields=record.missing_fields,
        present_field_count=_present_field_count(record),
        missing_field_count=len(record.missing_fields),
        priority_rank=priority_rank,
        work_status=work_status,
        promotion_impact=promotion_impact,
        required_next_action=required_next_action,
    )


def list_physical_property_gap_work_items() -> tuple[PhysicalPropertyGapWorkItem, ...]:
    return tuple(
        sorted(
            (
                _build_gap_work_item(record)
                for record in list_unresolved_physical_property_evidence_records()
            ),
            key=lambda item: (item.priority_rank, item.atomic_number),
        )
    )


def get_physical_property_gap_work_item(
    identifier: str | int,
) -> PhysicalPropertyGapWorkItem:
    identifier_text = str(identifier).strip()
    try:
        return _build_gap_work_item(
            find_unresolved_physical_property_evidence_record(identifier_text)
        )
    except KeyError:
        pass
    for item in list_physical_property_gap_work_items():
        if (
            identifier_text == str(item.atomic_number)
            or identifier_text.upper() == item.symbol.upper()
            or identifier_text == item.target_gap_receipt_id
            or identifier_text == item.work_item_id
        ):
            return item
    raise KeyError(f"unknown physical-property gap work item: {identifier_text}")


def validate_physical_property_gap_work_items(
    items: tuple[PhysicalPropertyGapWorkItem, ...] | None = None,
) -> dict[str, Any]:
    checked_items = items if items is not None else list_physical_property_gap_work_items()
    invalid_items = tuple(item.work_item_id for item in checked_items if item.validate())
    validation_status = "physical_property_gap_work_items_validated"
    if invalid_items:
        validation_status = "physical_property_gap_work_items_rejected"
    return {
        "validation_status": validation_status,
        "work_item_count": len(checked_items),
        "conflict_blocked_count": sum(
            1 for item in checked_items if item.work_status == "conflict_blocked_promotion"
        ),
        "conflict_resolved_for_promotion_count": sum(
            1
            for item in checked_items
            if item.work_status == "conflict_resolved_for_promotion"
        ),
        "single_field_source_search_count": sum(
            1 for item in checked_items if item.work_status == "single_field_source_search"
        ),
        "partial_property_source_search_count": sum(
            1 for item in checked_items if item.work_status == "partial_property_source_search"
        ),
        "synthetic_superheavy_uncertainty_count": sum(
            1
            for item in checked_items
            if item.work_status == "synthetic_superheavy_uncertainty"
        ),
        "gap_closure_count": sum(1 for item in checked_items if item.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for item in checked_items if item.seed_mutation_allowed
        ),
        "invalid_items": invalid_items,
    }
