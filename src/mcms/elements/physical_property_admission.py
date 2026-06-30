"""Purpose: decide admission status for secondary physical-property evidence.

Project scope: records whether reviewed secondary evidence can close an
unresolved measured-property gap.
Dependencies: secondary evidence receipts.
Invariants: conflicting secondary sources do not silently close gaps; admission
decisions do not mutate seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_secondary_evidence import (
    get_physical_property_secondary_evidence_receipt,
)

VALID_ADMISSION_DECISION_STATUSES = {
    "secondary_evidence_not_admitted_conflict",
    "secondary_evidence_not_admitted_needs_corroboration",
    "secondary_evidence_not_admitted_pending_review",
    "secondary_evidence_admitted_for_gap_closure",
    "secondary_evidence_rejected",
}


@dataclass(frozen=True)
class PhysicalPropertySecondaryEvidenceAdmissionDecision:
    decision_id: str
    target_receipt_id: str
    symbol: str
    atomic_number: int
    field_name: str
    source_key: str
    candidate_value: float
    candidate_unit: str
    decision_status: str
    decision_reason: str
    conflict_sources: tuple[str, ...]
    required_next_action: str
    closes_gap: bool
    seed_mutation_allowed: bool
    evidence_status: str = "physical_property_secondary_evidence_admission_decision"
    notes: tuple[str, ...] = (
        "Admission decisions do not mutate seed records.",
        "Conflicting secondary values require explicit conflict resolution.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        receipt = get_physical_property_secondary_evidence_receipt(self.target_receipt_id)
        if self.symbol != receipt.symbol:
            errors.append("admission decision symbol must match target receipt.")
        if self.atomic_number != receipt.atomic_number:
            errors.append("admission decision atomic number must match target receipt.")
        if self.field_name != receipt.field_name:
            errors.append("admission decision field must match target receipt.")
        if self.source_key != receipt.source_key:
            errors.append("admission decision source key must match target receipt.")
        if self.candidate_value != receipt.normalized_value:
            errors.append("admission decision value must match target receipt.")
        if self.candidate_unit != receipt.normalized_unit:
            errors.append("admission decision unit must match target receipt.")
        if self.decision_status not in VALID_ADMISSION_DECISION_STATUSES:
            errors.append("admission decision status is unknown.")
        if not self.decision_reason:
            errors.append("admission decision reason is required.")
        if self.closes_gap and self.decision_status != "secondary_evidence_admitted_for_gap_closure":
            errors.append("only admitted evidence may close a gap.")
        if self.seed_mutation_allowed:
            errors.append("admission decision alone must not allow seed mutation.")
        if self.decision_status == "secondary_evidence_not_admitted_conflict":
            if not self.conflict_sources:
                errors.append("conflict decision requires conflict sources.")
            if self.closes_gap:
                errors.append("conflict decision must not close gap.")
        if self.decision_status == "secondary_evidence_not_admitted_needs_corroboration":
            if not self.conflict_sources:
                errors.append("corroboration decision requires source notes.")
            if self.closes_gap:
                errors.append("corroboration decision must not close gap.")
        if self.decision_status == "secondary_evidence_not_admitted_pending_review":
            if not self.conflict_sources:
                errors.append("pending-review decision requires source notes.")
            if self.closes_gap:
                errors.append("pending-review decision must not close gap.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["conflict_sources"] = list(self.conflict_sources)
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_secondary_evidence_admission_decisions() -> tuple[
    PhysicalPropertySecondaryEvidenceAdmissionDecision, ...
]:
    astatine_receipt = get_physical_property_secondary_evidence_receipt("At")
    francium_receipt = get_physical_property_secondary_evidence_receipt("Fr")
    francium_density_receipt = get_physical_property_secondary_evidence_receipt(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-Z087-Fr-density_value-WebElements"
    )
    protactinium_receipt = get_physical_property_secondary_evidence_receipt("Pa")
    berkelium_receipt = get_physical_property_secondary_evidence_receipt("Bk")
    californium_boiling_receipt = get_physical_property_secondary_evidence_receipt(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-Z098-Cf-boiling_point_k-LANL"
    )
    californium_density_receipt = get_physical_property_secondary_evidence_receipt(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-Z098-Cf-density_value-RSC"
    )
    einsteinium_receipt = get_physical_property_secondary_evidence_receipt(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-Z099-Es-boiling_point_k-LANL"
    )
    return (
        PhysicalPropertySecondaryEvidenceAdmissionDecision(
            decision_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-"
                "Z085-At-boiling_point_k-LANL"
            ),
            target_receipt_id=astatine_receipt.receipt_id,
            symbol=astatine_receipt.symbol,
            atomic_number=astatine_receipt.atomic_number,
            field_name=astatine_receipt.field_name,
            source_key=astatine_receipt.source_key,
            candidate_value=astatine_receipt.normalized_value,
            candidate_unit=astatine_receipt.normalized_unit,
            decision_status="secondary_evidence_not_admitted_conflict",
            decision_reason=(
                "LANL/Chemicool/Lenntech align near 337 degC, but RSC lists "
                "350 degC; conflict must be resolved before gap closure."
            ),
            conflict_sources=(
                "RSC periodic table lists At boiling point as 350 degC / 623 K",
            ),
            required_next_action=(
                "create a conflict-resolution receipt or select a higher-precedence "
                "field-specific source before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertySecondaryEvidenceAdmissionDecision(
            decision_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-"
                "Z087-Fr-boiling_point_k-LANL"
            ),
            target_receipt_id=francium_receipt.receipt_id,
            symbol=francium_receipt.symbol,
            atomic_number=francium_receipt.atomic_number,
            field_name=francium_receipt.field_name,
            source_key=francium_receipt.source_key,
            candidate_value=francium_receipt.normalized_value,
            candidate_unit=francium_receipt.normalized_unit,
            decision_status="secondary_evidence_not_admitted_conflict",
            decision_reason=(
                "LANL lists 680 degC for Fr boiling point, while RSC and "
                "WebElements list different values; conflict review is required."
            ),
            conflict_sources=(
                "RSC/WebElements values differ from the LANL Fr boiling-point candidate.",
            ),
            required_next_action=(
                "create a conflict-resolution receipt or select a higher-precedence "
                "field-specific source before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertySecondaryEvidenceAdmissionDecision(
            decision_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-"
                "Z087-Fr-density_value-WebElements"
            ),
            target_receipt_id=francium_density_receipt.receipt_id,
            symbol=francium_density_receipt.symbol,
            atomic_number=francium_density_receipt.atomic_number,
            field_name=francium_density_receipt.field_name,
            source_key=francium_density_receipt.source_key,
            candidate_value=francium_density_receipt.normalized_value,
            candidate_unit=francium_density_receipt.normalized_unit,
            decision_status="secondary_evidence_not_admitted_needs_corroboration",
            decision_reason=(
                "WebElements lists a Fr density candidate, but RSC lists density "
                "as unknown; corroboration is required."
            ),
            conflict_sources=(
                "RSC periodic table lists Fr density as unknown.",
            ),
            required_next_action=(
                "find corroborating field-specific evidence or record an explicit "
                "rejection before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertySecondaryEvidenceAdmissionDecision(
            decision_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-"
                "Z091-Pa-boiling_point_k-LANL"
            ),
            target_receipt_id=protactinium_receipt.receipt_id,
            symbol=protactinium_receipt.symbol,
            atomic_number=protactinium_receipt.atomic_number,
            field_name=protactinium_receipt.field_name,
            source_key=protactinium_receipt.source_key,
            candidate_value=protactinium_receipt.normalized_value,
            candidate_unit=protactinium_receipt.normalized_unit,
            decision_status="secondary_evidence_not_admitted_conflict",
            decision_reason=(
                "LANL lists 4027 degC for Pa boiling point, while RSC/WebElements "
                "list nearby but not identical values; conflict review is required."
            ),
            conflict_sources=(
                "RSC/WebElements values are near the LANL candidate but not identical.",
            ),
            required_next_action=(
                "create a conflict-resolution receipt or select a higher-precedence "
                "field-specific source before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertySecondaryEvidenceAdmissionDecision(
            decision_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-"
                "Z098-Cf-boiling_point_k-LANL"
            ),
            target_receipt_id=californium_boiling_receipt.receipt_id,
            symbol=californium_boiling_receipt.symbol,
            atomic_number=californium_boiling_receipt.atomic_number,
            field_name=californium_boiling_receipt.field_name,
            source_key=californium_boiling_receipt.source_key,
            candidate_value=californium_boiling_receipt.normalized_value,
            candidate_unit=californium_boiling_receipt.normalized_unit,
            decision_status="secondary_evidence_not_admitted_needs_corroboration",
            decision_reason=(
                "LANL lists a Cf boiling-point candidate, but RSC lists the "
                "boiling point as unknown; corroboration is required."
            ),
            conflict_sources=(
                "RSC periodic table lists Cf boiling point as unknown.",
            ),
            required_next_action=(
                "find corroborating field-specific evidence or record an explicit "
                "rejection before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertySecondaryEvidenceAdmissionDecision(
            decision_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-"
                "Z098-Cf-density_value-RSC"
            ),
            target_receipt_id=californium_density_receipt.receipt_id,
            symbol=californium_density_receipt.symbol,
            atomic_number=californium_density_receipt.atomic_number,
            field_name=californium_density_receipt.field_name,
            source_key=californium_density_receipt.source_key,
            candidate_value=californium_density_receipt.normalized_value,
            candidate_unit=californium_density_receipt.normalized_unit,
            decision_status="secondary_evidence_not_admitted_pending_review",
            decision_reason=(
                "RSC lists a Cf density candidate, but admission requires a review "
                "receipt before the density gap can close."
            ),
            conflict_sources=(
                "RSC density candidate requires source review before admission.",
            ),
            required_next_action=(
                "create a density review receipt or select a higher-precedence "
                "field-specific source before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertySecondaryEvidenceAdmissionDecision(
            decision_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-"
                "Z099-Es-boiling_point_k-LANL"
            ),
            target_receipt_id=einsteinium_receipt.receipt_id,
            symbol=einsteinium_receipt.symbol,
            atomic_number=einsteinium_receipt.atomic_number,
            field_name=einsteinium_receipt.field_name,
            source_key=einsteinium_receipt.source_key,
            candidate_value=einsteinium_receipt.normalized_value,
            candidate_unit=einsteinium_receipt.normalized_unit,
            decision_status="secondary_evidence_not_admitted_needs_corroboration",
            decision_reason=(
                "LANL lists an Es boiling-point candidate, but RSC lists the "
                "boiling point as unknown; corroboration is required."
            ),
            conflict_sources=(
                "RSC periodic table lists Es boiling point as unknown.",
            ),
            required_next_action=(
                "find corroborating field-specific evidence or record an explicit "
                "rejection before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
        PhysicalPropertySecondaryEvidenceAdmissionDecision(
            decision_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-"
                "Z097-Bk-boiling_point_k-LANL"
            ),
            target_receipt_id=berkelium_receipt.receipt_id,
            symbol=berkelium_receipt.symbol,
            atomic_number=berkelium_receipt.atomic_number,
            field_name=berkelium_receipt.field_name,
            source_key=berkelium_receipt.source_key,
            candidate_value=berkelium_receipt.normalized_value,
            candidate_unit=berkelium_receipt.normalized_unit,
            decision_status="secondary_evidence_not_admitted_needs_corroboration",
            decision_reason=(
                "LANL lists a Bk boiling-point candidate, but RSC lists the "
                "boiling point as unknown; corroboration is required."
            ),
            conflict_sources=(
                "RSC periodic table lists Bk boiling point as unknown.",
            ),
            required_next_action=(
                "find corroborating field-specific evidence or record an explicit "
                "rejection before admission"
            ),
            closes_gap=False,
            seed_mutation_allowed=False,
        ),
    )


def get_physical_property_secondary_evidence_admission_decision(
    identifier: str | int,
) -> PhysicalPropertySecondaryEvidenceAdmissionDecision:
    identifier_text = str(identifier).strip()
    for decision in list_physical_property_secondary_evidence_admission_decisions():
        if (
            identifier_text == str(decision.atomic_number)
            or identifier_text.upper() == decision.symbol.upper()
            or identifier_text == decision.target_receipt_id
            or identifier_text == decision.decision_id
        ):
            return decision
    raise KeyError(f"unknown secondary evidence admission decision: {identifier_text}")


def validate_physical_property_secondary_evidence_admission_decisions(
    decisions: tuple[PhysicalPropertySecondaryEvidenceAdmissionDecision, ...] | None = None,
) -> dict[str, Any]:
    checked_decisions = (
        decisions
        if decisions is not None
        else list_physical_property_secondary_evidence_admission_decisions()
    )
    invalid_decisions = tuple(
        decision.decision_id for decision in checked_decisions if decision.validate()
    )
    validation_status = "physical_property_secondary_evidence_admission_decisions_validated"
    if invalid_decisions:
        validation_status = "physical_property_secondary_evidence_admission_decisions_rejected"
    return {
        "validation_status": validation_status,
        "decision_count": len(checked_decisions),
        "admitted_gap_closure_count": sum(1 for decision in checked_decisions if decision.closes_gap),
        "conflict_blocked_count": sum(
            1
            for decision in checked_decisions
            if decision.decision_status == "secondary_evidence_not_admitted_conflict"
        ),
        "corroboration_blocked_count": sum(
            1
            for decision in checked_decisions
            if decision.decision_status
            == "secondary_evidence_not_admitted_needs_corroboration"
        ),
        "pending_review_count": sum(
            1
            for decision in checked_decisions
            if decision.decision_status == "secondary_evidence_not_admitted_pending_review"
        ),
        "seed_mutation_allowed_count": sum(
            1 for decision in checked_decisions if decision.seed_mutation_allowed
        ),
        "invalid_decisions": invalid_decisions,
    }
