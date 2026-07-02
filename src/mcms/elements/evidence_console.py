"""Purpose: read-only per-element evidence console records.

Project scope: aggregates canonical, candidate, unresolved, admission,
conflict, readiness, and promotion state without admitting evidence or mutating
seed records.
Dependencies: evidence records, atom behavior gaps, readiness scoring, physical
property review receipts, promotion decision receipts, and full snapshots.
Invariants: console records are read-only; mutation authority is always false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.atom_behavior_gap import list_atom_behavior_gap_receipts
from mcms.elements.evidence import (
    list_common_ion_evidence_records,
    list_isotope_evidence_records,
    list_physical_property_evidence_records,
    list_unresolved_common_ion_evidence_records,
    list_unresolved_isotope_evidence_records,
    list_unresolved_physical_property_evidence_records,
)
from mcms.elements.isotope_admission import list_isotope_candidate_admission_receipts
from mcms.elements.isotope_candidate_evidence import list_isotope_candidate_evidence_receipts
from mcms.elements.physical_property_admission import (
    list_physical_property_secondary_evidence_admission_decisions,
)
from mcms.elements.physical_property_conflict import (
    list_physical_property_conflict_resolution_receipts,
)
from mcms.elements.physical_property_corroboration import (
    list_physical_property_corroboration_review_receipts,
)
from mcms.elements.physical_property_review import list_physical_property_review_receipts
from mcms.elements.physical_property_secondary_evidence import (
    list_physical_property_secondary_evidence_receipts,
)
from mcms.elements.promotion_decision import get_promotion_decision_receipt
from mcms.elements.readiness_scoring import build_element_readiness_score
from mcms.elements.snapshot import get_snapshot_record, list_full_snapshot_records

VALID_EVIDENCE_CONSOLE_STATUSES = {"element_evidence_console_read_model"}


@dataclass(frozen=True)
class ElementEvidenceConsoleRecord:
    record_id: str
    symbol: str
    atomic_number: int
    readiness_status: str
    promotion_decision_status: str | None
    canonical_evidence_refs: tuple[str, ...]
    candidate_evidence_refs: tuple[str, ...]
    unresolved_gap_refs: tuple[str, ...]
    admission_receipt_refs: tuple[str, ...]
    conflict_review_refs: tuple[str, ...]
    next_governed_action: str
    mutation_allowed: bool = False
    evidence_status: str = "element_evidence_console_read_model"

    @property
    def canonical_evidence_count(self) -> int:
        return len(self.canonical_evidence_refs)

    @property
    def candidate_evidence_count(self) -> int:
        return len(self.candidate_evidence_refs)

    @property
    def unresolved_gap_count(self) -> int:
        return len(self.unresolved_gap_refs)

    @property
    def admission_receipt_count(self) -> int:
        return len(self.admission_receipt_refs)

    @property
    def conflict_review_count(self) -> int:
        return len(self.conflict_review_refs)

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        if self.record_id != f"MSPEE-EVIDENCE-CONSOLE-Z{self.atomic_number:03d}-{self.symbol}":
            errors.append("evidence console record id is not canonical.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("evidence console atomic number must match snapshot.")
        if self.symbol != snapshot.symbol:
            errors.append("evidence console symbol must match snapshot.")
        if self.evidence_status not in VALID_EVIDENCE_CONSOLE_STATUSES:
            errors.append("evidence console status is unknown.")
        if self.mutation_allowed:
            errors.append("evidence console records must not allow mutation.")
        if 55 <= self.atomic_number <= 86 and self.promotion_decision_status is None:
            errors.append("Cs-Rn console records require promotion decision status.")
        if not self.next_governed_action:
            errors.append("evidence console requires next governed action.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for field_name in (
            "canonical_evidence_refs",
            "candidate_evidence_refs",
            "unresolved_gap_refs",
            "admission_receipt_refs",
            "conflict_review_refs",
        ):
            payload[field_name] = list(payload[field_name])
        payload["canonical_evidence_count"] = self.canonical_evidence_count
        payload["candidate_evidence_count"] = self.candidate_evidence_count
        payload["unresolved_gap_count"] = self.unresolved_gap_count
        payload["admission_receipt_count"] = self.admission_receipt_count
        payload["conflict_review_count"] = self.conflict_review_count
        return payload


def _record_ref(record: Any) -> str:
    for field_name in ("record_id", "receipt_id", "decision_id", "item_id"):
        value = getattr(record, field_name, None)
        if value:
            return str(value)
    return repr(record)


def _refs_for_symbol(records: tuple[Any, ...], symbol: str) -> tuple[str, ...]:
    return tuple(
        _record_ref(record)
        for record in records
        if getattr(record, "symbol", None) == symbol
    )


def build_element_evidence_console_record(
    identifier: str | int,
) -> ElementEvidenceConsoleRecord:
    snapshot = get_snapshot_record(identifier)
    score = build_element_readiness_score(snapshot.symbol)
    try:
        promotion_decision_status = get_promotion_decision_receipt(
            snapshot.symbol
        ).decision_status
        next_governed_action = "await or inspect full-span approval execution packet"
    except KeyError:
        promotion_decision_status = None
        next_governed_action = (
            "resolve readiness blockers"
            if score.readiness_status != "atom_behavior_ready_from_evidence"
            else "maintain read-only evidence state"
        )
    record = ElementEvidenceConsoleRecord(
        record_id=f"MSPEE-EVIDENCE-CONSOLE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}",
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        readiness_status=score.readiness_status,
        promotion_decision_status=promotion_decision_status,
        canonical_evidence_refs=(
            _refs_for_symbol(list_isotope_evidence_records(), snapshot.symbol)
            + _refs_for_symbol(list_common_ion_evidence_records(), snapshot.symbol)
            + _refs_for_symbol(list_physical_property_evidence_records(), snapshot.symbol)
        ),
        candidate_evidence_refs=(
            _refs_for_symbol(list_isotope_candidate_evidence_receipts(), snapshot.symbol)
            + _refs_for_symbol(
                list_physical_property_secondary_evidence_receipts(),
                snapshot.symbol,
            )
        ),
        unresolved_gap_refs=(
            _refs_for_symbol(list_unresolved_isotope_evidence_records(), snapshot.symbol)
            + _refs_for_symbol(
                list_unresolved_common_ion_evidence_records(),
                snapshot.symbol,
            )
            + _refs_for_symbol(
                list_unresolved_physical_property_evidence_records(),
                snapshot.symbol,
            )
            + _refs_for_symbol(list_atom_behavior_gap_receipts(), snapshot.symbol)
        ),
        admission_receipt_refs=(
            _refs_for_symbol(list_isotope_candidate_admission_receipts(), snapshot.symbol)
            + _refs_for_symbol(
                list_physical_property_secondary_evidence_admission_decisions(),
                snapshot.symbol,
            )
        ),
        conflict_review_refs=(
            _refs_for_symbol(
                list_physical_property_conflict_resolution_receipts(),
                snapshot.symbol,
            )
            + _refs_for_symbol(
                list_physical_property_corroboration_review_receipts(),
                snapshot.symbol,
            )
            + _refs_for_symbol(list_physical_property_review_receipts(), snapshot.symbol)
        ),
        next_governed_action=next_governed_action,
    )
    validation_errors = record.validate()
    if validation_errors:
        raise ValueError("; ".join(validation_errors))
    return record


def list_element_evidence_console_records() -> tuple[ElementEvidenceConsoleRecord, ...]:
    return tuple(
        build_element_evidence_console_record(snapshot.symbol)
        for snapshot in list_full_snapshot_records()
    )


def get_element_evidence_console_record(
    identifier: str | int,
) -> ElementEvidenceConsoleRecord:
    return build_element_evidence_console_record(identifier)


def validate_element_evidence_console_records(
    records: tuple[ElementEvidenceConsoleRecord, ...] | None = None,
) -> dict[str, Any]:
    checked_records = records if records is not None else list_element_evidence_console_records()
    invalid_records = tuple(record.record_id for record in checked_records if record.validate())
    return {
        "validation_status": (
            "element_evidence_console_records_validated"
            if not invalid_records
            else "element_evidence_console_records_rejected"
        ),
        "record_count": len(checked_records),
        "ready_record_count": sum(
            1
            for record in checked_records
            if record.readiness_status == "atom_behavior_ready_from_evidence"
        ),
        "promotion_pending_approval_count": sum(
            1
            for record in checked_records
            if record.promotion_decision_status == "promotion_ready_pending_approval"
        ),
        "mutation_allowed_count": sum(1 for record in checked_records if record.mutation_allowed),
        "canonical_evidence_ref_count": sum(
            record.canonical_evidence_count for record in checked_records
        ),
        "candidate_evidence_ref_count": sum(
            record.candidate_evidence_count for record in checked_records
        ),
        "unresolved_gap_ref_count": sum(
            record.unresolved_gap_count for record in checked_records
        ),
        "admission_receipt_ref_count": sum(
            record.admission_receipt_count for record in checked_records
        ),
        "conflict_ref_count": sum(
            record.conflict_review_count for record in checked_records
        ),
        "invalid_records": invalid_records,
    }
