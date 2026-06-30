"""Purpose: audit unresolved physical-property evidence gaps.

Project scope: turns incomplete PubChem physical-property rows into explicit
gap receipts without guessing missing measured values.
Dependencies: unresolved physical-property evidence records.
Invariants: source-backed measured values are not invented; promotion-impact
flags are derived from declared unresolved evidence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.evidence import (
    PHYSICAL_PROPERTY_EVIDENCE_SOURCE_REFERENCES,
    list_unresolved_physical_property_evidence_records,
)

PUBCHEM_PERIODIC_TABLE_CSV_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV"
PHYSICAL_PROPERTY_GAP_SOURCE_CHECK_DATE = "2026-06-29"
VALID_PHYSICAL_PROPERTY_GAP_STATUSES = {"awaiting_authoritative_source_value"}
VALID_PHYSICAL_PROPERTY_SOURCE_ROW_STATUSES = {"source_row_incomplete"}


@dataclass(frozen=True)
class PhysicalPropertyGapAuditReceipt:
    receipt_id: str
    element_id: str
    symbol: str
    atomic_number: int
    missing_fields: tuple[str, ...]
    present_fields: tuple[str, ...]
    source_keys: tuple[str, ...]
    source_url: str
    source_checked_date: str
    source_row_status: str
    gap_status: str
    blocks_promotion_spans: tuple[str, ...]
    required_next_action: str
    no_guess_policy: bool = True
    evidence_status: str = "physical_property_gap_audit_receipt"
    notes: tuple[str, ...] = (
        "The source row is incomplete; missing physical-property values are not guessed.",
        "This receipt records source-gap status and promotion impact only.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.receipt_id:
            errors.append("physical-property gap receipt id is required.")
        if not self.missing_fields:
            errors.append("physical-property gap receipt requires missing fields.")
        if self.source_row_status not in VALID_PHYSICAL_PROPERTY_SOURCE_ROW_STATUSES:
            errors.append("physical-property source row status is unknown.")
        if self.gap_status not in VALID_PHYSICAL_PROPERTY_GAP_STATUSES:
            errors.append("physical-property gap status is unknown.")
        if not self.no_guess_policy:
            errors.append("physical-property gap receipts must enforce no-guess policy.")
        if self.symbol == "At" and "Cs-Rn" not in self.blocks_promotion_spans:
            errors.append("At physical-property gap must block the Cs-Rn promotion span.")
        if self.symbol != "At" and "Cs-Rn" in self.blocks_promotion_spans:
            errors.append("only At currently blocks the Cs-Rn promotion span.")
        if "boiling_point_k" not in self.missing_fields:
            errors.append("current unresolved physical-property gaps must include boiling point.")
        if not self.required_next_action:
            errors.append("physical-property gap receipt requires a next action.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["missing_fields"] = list(self.missing_fields)
        payload["present_fields"] = list(self.present_fields)
        payload["source_keys"] = list(self.source_keys)
        payload["blocks_promotion_spans"] = list(self.blocks_promotion_spans)
        payload["notes"] = list(self.notes)
        return payload


def _present_fields_for_unresolved_record(record: Any) -> tuple[str, ...]:
    present_fields: list[str] = []
    for field_name in ("standard_state", "melting_point_k", "boiling_point_k", "density_value"):
        if getattr(record, field_name) is not None:
            present_fields.append(field_name)
    return tuple(present_fields)


def _build_gap_receipt(record: Any) -> PhysicalPropertyGapAuditReceipt:
    return PhysicalPropertyGapAuditReceipt(
        receipt_id=f"MSPEE-PHYSICAL-PROPERTY-GAP-Z{record.atomic_number:03d}-{record.symbol}",
        element_id=record.element_id,
        symbol=record.symbol,
        atomic_number=record.atomic_number,
        missing_fields=record.missing_fields,
        present_fields=_present_fields_for_unresolved_record(record),
        source_keys=tuple(source.key for source in PHYSICAL_PROPERTY_EVIDENCE_SOURCE_REFERENCES),
        source_url=PUBCHEM_PERIODIC_TABLE_CSV_URL,
        source_checked_date=PHYSICAL_PROPERTY_GAP_SOURCE_CHECK_DATE,
        source_row_status="source_row_incomplete",
        gap_status="awaiting_authoritative_source_value",
        blocks_promotion_spans=("Cs-Rn",) if record.symbol == "At" else (),
        required_next_action=(
            "wait for PubChem to publish a complete row or add a governed secondary "
            "source with explicit provenance"
        ),
    )


def list_physical_property_gap_audit_receipts() -> tuple[PhysicalPropertyGapAuditReceipt, ...]:
    return tuple(
        _build_gap_receipt(record)
        for record in list_unresolved_physical_property_evidence_records()
    )


def get_physical_property_gap_audit_receipt(
    identifier: str | int,
) -> PhysicalPropertyGapAuditReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_gap_audit_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.element_id
            or identifier_text == receipt.receipt_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property gap audit receipt: {identifier_text}")


def validate_physical_property_gap_audit_receipts(
    receipts: tuple[PhysicalPropertyGapAuditReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_physical_property_gap_audit_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_gap_audit_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_gap_audit_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "cs_rn_blocking_gap_count": sum(
            1 for receipt in checked_receipts if "Cs-Rn" in receipt.blocks_promotion_spans
        ),
        "boiling_point_gap_count": sum(
            1 for receipt in checked_receipts if "boiling_point_k" in receipt.missing_fields
        ),
        "no_guess_policy_count": sum(1 for receipt in checked_receipts if receipt.no_guess_policy),
        "invalid_receipts": invalid_receipts,
    }
