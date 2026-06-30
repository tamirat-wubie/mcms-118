"""Purpose: record physical-property secondary-source conflicts.

Project scope: captures reviewed conflicts between secondary physical-property
values without closing gaps or mutating seed records.
Dependencies: secondary evidence admission decisions.
Invariants: a conflict-resolution receipt may block admission, but it cannot
promote candidate evidence or alter source-backed element state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_admission import (
    get_physical_property_secondary_evidence_admission_decision,
)

VALID_PHYSICAL_PROPERTY_CONFLICT_DECISIONS = {
    "blocked_pending_higher_precedence_source",
    "resolved_admit_candidate",
    "resolved_reject_candidate",
}


@dataclass(frozen=True)
class PhysicalPropertyConflictSourceValue:
    source_key: str
    source_authority: str
    source_citation: str
    raw_value: str
    raw_unit: str
    normalized_value: float
    normalized_unit: str
    value_type: str
    alignment_group: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        required_text_fields = (
            self.source_key,
            self.source_authority,
            self.source_citation,
            self.raw_value,
            self.raw_unit,
            self.normalized_unit,
            self.value_type,
            self.alignment_group,
        )
        if any(not field for field in required_text_fields):
            errors.append("conflict source value requires complete provenance fields.")
        if self.normalized_value <= 0:
            errors.append("conflict source normalized value must be positive.")
        if self.normalized_unit != "K":
            errors.append("temperature conflict source values must normalize to kelvin.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PhysicalPropertyConflictResolutionReceipt:
    receipt_id: str
    target_admission_decision_id: str
    symbol: str
    atomic_number: int
    field_name: str
    compared_values: tuple[PhysicalPropertyConflictSourceValue, ...]
    conflict_summary: str
    resolution_decision: str
    resolution_reason: str
    required_next_action: str
    closes_gap: bool
    seed_mutation_allowed: bool
    evidence_status: str = "physical_property_conflict_resolution_receipt"
    notes: tuple[str, ...] = (
        "Conflict receipts are read-only evidence governance records.",
        "Conflicts cannot close physical-property gaps without explicit resolution.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        admission = get_physical_property_secondary_evidence_admission_decision(
            self.target_admission_decision_id
        )
        if self.symbol != admission.symbol:
            errors.append("conflict receipt symbol must match admission decision.")
        if self.atomic_number != admission.atomic_number:
            errors.append("conflict receipt atomic number must match admission decision.")
        if self.field_name != admission.field_name:
            errors.append("conflict receipt field must match admission decision.")
        if len(self.compared_values) < 2:
            errors.append("conflict receipt requires at least two compared source values.")
        if self.resolution_decision not in VALID_PHYSICAL_PROPERTY_CONFLICT_DECISIONS:
            errors.append("conflict receipt resolution decision is unknown.")
        if not self.conflict_summary:
            errors.append("conflict receipt requires a conflict summary.")
        if not self.resolution_reason:
            errors.append("conflict receipt requires a resolution reason.")
        if not self.required_next_action:
            errors.append("conflict receipt requires a next action.")
        if self.seed_mutation_allowed:
            errors.append("conflict receipt must not allow seed mutation.")
        if self.closes_gap and self.resolution_decision != "resolved_admit_candidate":
            errors.append("only resolved admitted candidates may close a gap.")
        source_errors = tuple(
            error
            for source_value in self.compared_values
            for error in source_value.validate()
        )
        errors.extend(source_errors)
        alignment_groups = {source_value.alignment_group for source_value in self.compared_values}
        if len(alignment_groups) < 2:
            errors.append("conflict receipt requires at least two distinct alignment groups.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["compared_values"] = [
            source_value.to_dict() for source_value in self.compared_values
        ]
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_conflict_resolution_receipts() -> tuple[
    PhysicalPropertyConflictResolutionReceipt, ...
]:
    astatine_admission = get_physical_property_secondary_evidence_admission_decision("At")
    francium_admission = get_physical_property_secondary_evidence_admission_decision("Fr")
    protactinium_admission = get_physical_property_secondary_evidence_admission_decision("Pa")
    return (
        PhysicalPropertyConflictResolutionReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-CONFLICT-RESOLUTION-Z085-At-boiling_point_k",
            target_admission_decision_id=astatine_admission.decision_id,
            symbol=astatine_admission.symbol,
            atomic_number=astatine_admission.atomic_number,
            field_name=astatine_admission.field_name,
            compared_values=(
                PhysicalPropertyConflictSourceValue(
                    source_key="lanl_periodic_table_candidate",
                    source_authority="Los Alamos National Laboratory",
                    source_citation="https://periodic.lanl.gov/85.shtml",
                    raw_value="337",
                    raw_unit="degC",
                    normalized_value=610.15,
                    normalized_unit="K",
                    value_type="estimated",
                    alignment_group="337_degC_cluster",
                ),
                PhysicalPropertyConflictSourceValue(
                    source_key="rsc_periodic_table_conflict_value",
                    source_authority="Royal Society of Chemistry",
                    source_citation="https://www.rsc.org/periodic-table/element/85/astatine",
                    raw_value="350",
                    raw_unit="degC",
                    normalized_value=623.15,
                    normalized_unit="K",
                    value_type="listed_reference_value",
                    alignment_group="350_degC_cluster",
                ),
            ),
            conflict_summary=(
                "LANL candidate lists At boiling point as 337 degC, while RSC lists "
                "350 degC; the disagreement prevents secondary-source admission."
            ),
            resolution_decision="blocked_pending_higher_precedence_source",
            resolution_reason=(
                "No higher-precedence field-specific source is recorded for the At "
                "boiling-point gap, so neither secondary value is promoted."
            ),
            required_next_action=(
                "record a higher-precedence field-specific source or create an "
                "operator-approved resolution receipt before closing the At gap"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertyConflictResolutionReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-CONFLICT-RESOLUTION-Z087-Fr-boiling_point_k",
            target_admission_decision_id=francium_admission.decision_id,
            symbol=francium_admission.symbol,
            atomic_number=francium_admission.atomic_number,
            field_name=francium_admission.field_name,
            compared_values=(
                PhysicalPropertyConflictSourceValue(
                    source_key="lanl_periodic_table_candidate",
                    source_authority="Los Alamos National Laboratory",
                    source_citation="https://periodic.lanl.gov/87.shtml",
                    raw_value="680",
                    raw_unit="degC",
                    normalized_value=953.15,
                    normalized_unit="K",
                    value_type="estimated",
                    alignment_group="953_K_cluster",
                ),
                PhysicalPropertyConflictSourceValue(
                    source_key="rsc_periodic_table_conflict_value",
                    source_authority="Royal Society of Chemistry",
                    source_citation="https://periodic-table.rsc.org/element/87/francium",
                    raw_value="650",
                    raw_unit="degC",
                    normalized_value=923.15,
                    normalized_unit="K",
                    value_type="listed_reference_value",
                    alignment_group="923_K_cluster",
                ),
            ),
            conflict_summary=(
                "LANL lists Fr boiling point as 680 degC / 953.15 K, while RSC "
                "lists 650 degC / 923 K."
            ),
            resolution_decision="blocked_pending_higher_precedence_source",
            resolution_reason=(
                "The Fr candidate has non-identical secondary values; the "
                "boiling-point field remains unresolved pending higher-precedence evidence."
            ),
            required_next_action=(
                "record a higher-precedence field-specific source or operator-approved "
                "resolution before closing the Fr boiling-point gap"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertyConflictResolutionReceipt(
            receipt_id="MSPEE-PHYSICAL-PROPERTY-CONFLICT-RESOLUTION-Z091-Pa-boiling_point_k",
            target_admission_decision_id=protactinium_admission.decision_id,
            symbol=protactinium_admission.symbol,
            atomic_number=protactinium_admission.atomic_number,
            field_name=protactinium_admission.field_name,
            compared_values=(
                PhysicalPropertyConflictSourceValue(
                    source_key="lanl_periodic_table_candidate",
                    source_authority="Los Alamos National Laboratory",
                    source_citation="https://periodic.lanl.gov/91.shtml",
                    raw_value="4027",
                    raw_unit="degC",
                    normalized_value=4300.15,
                    normalized_unit="K",
                    value_type="estimated",
                    alignment_group="4300_K_cluster",
                ),
                PhysicalPropertyConflictSourceValue(
                    source_key="rsc_periodic_table_conflict_value",
                    source_authority="Royal Society of Chemistry",
                    source_citation="https://periodic-table.rsc.org/element/91/protactinium",
                    raw_value="4000",
                    raw_unit="degC",
                    normalized_value=4273.15,
                    normalized_unit="K",
                    value_type="listed_reference_value",
                    alignment_group="4273_K_cluster",
                ),
                PhysicalPropertyConflictSourceValue(
                    source_key="webelements_periodic_table_conflict_value",
                    source_authority="WebElements",
                    source_citation="https://www.webelements.com/protactinium/",
                    raw_value="4300",
                    raw_unit="K",
                    normalized_value=4300.0,
                    normalized_unit="K",
                    value_type="listed_reference_value",
                    alignment_group="4300_K_cluster",
                ),
            ),
            conflict_summary=(
                "LANL lists Pa boiling point as 4027 degC / 4300.15 K, RSC "
                "lists 4000 degC / 4273 K, and WebElements lists 4300 K."
            ),
            resolution_decision="blocked_pending_higher_precedence_source",
            resolution_reason=(
                "The Pa candidate has nearby but non-identical secondary values; "
                "the gap remains unresolved pending higher-precedence evidence."
            ),
            required_next_action=(
                "record a higher-precedence field-specific source or operator-approved "
                "resolution before closing the Pa boiling-point gap"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
    )


def get_physical_property_conflict_resolution_receipt(
    identifier: str | int,
) -> PhysicalPropertyConflictResolutionReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_conflict_resolution_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_admission_decision_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property conflict receipt: {identifier_text}")


def validate_physical_property_conflict_resolution_receipts(
    receipts: tuple[PhysicalPropertyConflictResolutionReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts
        if receipts is not None
        else list_physical_property_conflict_resolution_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_conflict_resolution_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_conflict_resolution_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "blocked_pending_higher_precedence_source_count": sum(
            1
            for receipt in checked_receipts
            if receipt.resolution_decision == "blocked_pending_higher_precedence_source"
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
