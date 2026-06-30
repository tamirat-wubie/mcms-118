"""Purpose: atom behavior v2 source-gap receipts and work items.

Project scope: makes missing atom behavior coverage explicit for elements whose
isotope evidence is unresolved, without inventing isotope, neutron, or behavior
values.
Dependencies: unresolved isotope evidence records and full element snapshots.
Invariants: atom behavior profiles require source-backed isotope evidence; gap
records are planning metadata only and never close evidence gaps or mutate seeds.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.evidence import (
    UnresolvedEvidenceRecord,
    list_unresolved_isotope_evidence_records,
)
from mcms.elements.snapshot import get_snapshot_record

ATOM_BEHAVIOR_GAP_SOURCE_CHECK_DATE = "2026-06-30"
VALID_ATOM_BEHAVIOR_GAP_STATUSES = {"awaiting_isotope_evidence"}
VALID_ATOM_BEHAVIOR_GAP_WORK_STATUSES = {
    "isotope_evidence_required",
    "seed_and_matter_profile_required",
}
LEVEL_1_ATOM_BEHAVIOR_BOUNDARY = 54


def _element_id(atomic_number: int, symbol: str) -> str:
    return f"MSPEE-Z{atomic_number:03d}-{symbol}"


def _gap_receipt_id(atomic_number: int, symbol: str) -> str:
    return f"MSPEE-ATOM-BEHAVIOR-GAP-Z{atomic_number:03d}-{symbol}"


def _work_item_id(atomic_number: int, symbol: str) -> str:
    return f"MSPEE-ATOM-BEHAVIOR-GAP-WORK-Z{atomic_number:03d}-{symbol}"


def _profile_blockers(record: UnresolvedEvidenceRecord) -> tuple[str, ...]:
    if record.atomic_number <= LEVEL_1_ATOM_BEHAVIOR_BOUNDARY:
        return ("isotope_evidence",)
    return ("isotope_evidence", "level_1_seed_record", "matter_behavior_profile")


@dataclass(frozen=True)
class AtomBehaviorGapReceipt:
    receipt_id: str
    target_unresolved_isotope_receipt_id: str
    element_id: str
    symbol: str
    atomic_number: int
    missing_evidence: tuple[str, ...]
    profile_blockers: tuple[str, ...]
    source_boundary: str
    source_checked_date: str
    gap_status: str
    required_next_action: str
    no_guess_policy: bool = True
    evidence_status: str = "atom_behavior_gap_receipt"
    notes: tuple[str, ...] = (
        "Atom behavior profiles are blocked until isotope evidence is source-backed.",
        "Neutron count, isotope stability, and decay behavior are not guessed.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        expected_element_id = _element_id(snapshot.atomic_number, snapshot.symbol)
        expected_receipt_id = _gap_receipt_id(snapshot.atomic_number, snapshot.symbol)
        if self.receipt_id != expected_receipt_id:
            errors.append("atom behavior gap receipt id is not canonical.")
        if self.element_id != expected_element_id:
            errors.append("atom behavior gap element id must match snapshot element id.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("atom behavior gap atomic number must match snapshot element.")
        if not self.target_unresolved_isotope_receipt_id.endswith(
            "-isotope_evidence-unresolved"
        ):
            errors.append("atom behavior gap must target an unresolved isotope receipt.")
        if not self.missing_evidence:
            errors.append("atom behavior gap requires missing evidence labels.")
        required_missing = {
            "stable_isotope_list",
            "radioisotope_list",
            "natural_abundance",
            "half_life_or_stability_status",
            "decay_mode_when_radioactive",
        }
        if not required_missing <= set(self.missing_evidence):
            errors.append("atom behavior gap must preserve isotope missing-evidence labels.")
        if self.profile_blockers != _profile_blockers(
            UnresolvedEvidenceRecord(
                receipt_id=self.target_unresolved_isotope_receipt_id,
                element_id=self.element_id,
                symbol=self.symbol,
                atomic_number=self.atomic_number,
                evidence_domain="isotope_evidence",
                missing_evidence=self.missing_evidence,
                source_boundary=self.source_boundary,
            )
        ):
            errors.append("atom behavior gap profile blockers are inconsistent.")
        if self.gap_status not in VALID_ATOM_BEHAVIOR_GAP_STATUSES:
            errors.append("atom behavior gap status is unknown.")
        if not self.no_guess_policy:
            errors.append("atom behavior gaps must enforce no-guess policy.")
        if not self.required_next_action:
            errors.append("atom behavior gap requires a next action.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["missing_evidence"] = list(self.missing_evidence)
        payload["profile_blockers"] = list(self.profile_blockers)
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class AtomBehaviorGapWorkItem:
    work_item_id: str
    target_gap_receipt_id: str
    symbol: str
    atomic_number: int
    priority_rank: int
    work_status: str
    profile_blockers: tuple[str, ...]
    required_next_action: str
    closes_gap: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "atom_behavior_gap_work_item"
    notes: tuple[str, ...] = (
        "Atom behavior work items are planning metadata, not evidence admission.",
        "A work item never creates isotope evidence or mutates element seed records.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        gap_receipt = get_atom_behavior_gap_receipt(self.target_gap_receipt_id)
        if self.work_item_id != _work_item_id(self.atomic_number, self.symbol):
            errors.append("atom behavior gap work item id is not canonical.")
        if self.symbol != gap_receipt.symbol:
            errors.append("atom behavior work item symbol must match gap receipt.")
        if self.atomic_number != gap_receipt.atomic_number:
            errors.append("atom behavior work item atomic number must match gap receipt.")
        if self.profile_blockers != gap_receipt.profile_blockers:
            errors.append("atom behavior work item blockers must match gap receipt.")
        if self.priority_rank < 0:
            errors.append("atom behavior work item priority rank must be non-negative.")
        if self.work_status not in VALID_ATOM_BEHAVIOR_GAP_WORK_STATUSES:
            errors.append("atom behavior work item status is unknown.")
        if self.closes_gap:
            errors.append("atom behavior work item must not close a gap.")
        if self.seed_mutation_allowed:
            errors.append("atom behavior work item must not allow seed mutation.")
        if not self.required_next_action:
            errors.append("atom behavior work item requires a next action.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["profile_blockers"] = list(self.profile_blockers)
        payload["notes"] = list(self.notes)
        return payload


def _build_gap_receipt(record: UnresolvedEvidenceRecord) -> AtomBehaviorGapReceipt:
    blockers = _profile_blockers(record)
    return AtomBehaviorGapReceipt(
        receipt_id=_gap_receipt_id(record.atomic_number, record.symbol),
        target_unresolved_isotope_receipt_id=record.receipt_id,
        element_id=record.element_id,
        symbol=record.symbol,
        atomic_number=record.atomic_number,
        missing_evidence=record.missing_evidence,
        profile_blockers=blockers,
        source_boundary=record.source_boundary,
        source_checked_date=ATOM_BEHAVIOR_GAP_SOURCE_CHECK_DATE,
        gap_status="awaiting_isotope_evidence",
        required_next_action=(
            "source isotope list, natural abundance, stability or half-life, and decay "
            "mode evidence before creating atom behavior profiles"
            if blockers == ("isotope_evidence",)
            else "promote element seed and matter profile after isotope evidence is sourced"
        ),
    )


def list_atom_behavior_gap_receipts() -> tuple[AtomBehaviorGapReceipt, ...]:
    return tuple(
        _build_gap_receipt(record)
        for record in list_unresolved_isotope_evidence_records()
    )


def get_atom_behavior_gap_receipt(identifier: str | int) -> AtomBehaviorGapReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_atom_behavior_gap_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.element_id
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_unresolved_isotope_receipt_id
        ):
            return receipt
    raise KeyError(f"unknown atom behavior gap receipt: {identifier_text}")


def _build_gap_work_item(receipt: AtomBehaviorGapReceipt) -> AtomBehaviorGapWorkItem:
    work_status = (
        "isotope_evidence_required"
        if receipt.profile_blockers == ("isotope_evidence",)
        else "seed_and_matter_profile_required"
    )
    return AtomBehaviorGapWorkItem(
        work_item_id=_work_item_id(receipt.atomic_number, receipt.symbol),
        target_gap_receipt_id=receipt.receipt_id,
        symbol=receipt.symbol,
        atomic_number=receipt.atomic_number,
        priority_rank=0 if work_status == "isotope_evidence_required" else 1,
        work_status=work_status,
        profile_blockers=receipt.profile_blockers,
        required_next_action=receipt.required_next_action,
    )


def list_atom_behavior_gap_work_items() -> tuple[AtomBehaviorGapWorkItem, ...]:
    return tuple(
        sorted(
            (_build_gap_work_item(receipt) for receipt in list_atom_behavior_gap_receipts()),
            key=lambda item: (item.priority_rank, item.atomic_number),
        )
    )


def get_atom_behavior_gap_work_item(identifier: str | int) -> AtomBehaviorGapWorkItem:
    identifier_text = str(identifier).strip()
    for item in list_atom_behavior_gap_work_items():
        if (
            identifier_text == str(item.atomic_number)
            or identifier_text.upper() == item.symbol.upper()
            or identifier_text == item.target_gap_receipt_id
            or identifier_text == item.work_item_id
        ):
            return item
    raise KeyError(f"unknown atom behavior gap work item: {identifier_text}")


def validate_atom_behavior_gap_receipts(
    receipts: tuple[AtomBehaviorGapReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = receipts if receipts is not None else list_atom_behavior_gap_receipts()
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    return {
        "validation_status": (
            "atom_behavior_gap_receipts_validated"
            if not invalid_receipts
            else "atom_behavior_gap_receipts_rejected"
        ),
        "receipt_count": len(checked_receipts),
        "isotope_only_gap_count": sum(
            1 for receipt in checked_receipts if receipt.profile_blockers == ("isotope_evidence",)
        ),
        "seed_and_matter_gap_count": sum(
            1
            for receipt in checked_receipts
            if "level_1_seed_record" in receipt.profile_blockers
        ),
        "no_guess_policy_count": sum(1 for receipt in checked_receipts if receipt.no_guess_policy),
        "invalid_receipts": invalid_receipts,
    }


def validate_atom_behavior_gap_work_items(
    items: tuple[AtomBehaviorGapWorkItem, ...] | None = None,
) -> dict[str, Any]:
    checked_items = items if items is not None else list_atom_behavior_gap_work_items()
    invalid_items = tuple(item.work_item_id for item in checked_items if item.validate())
    return {
        "validation_status": (
            "atom_behavior_gap_work_items_validated"
            if not invalid_items
            else "atom_behavior_gap_work_items_rejected"
        ),
        "work_item_count": len(checked_items),
        "isotope_evidence_required_count": sum(
            1 for item in checked_items if item.work_status == "isotope_evidence_required"
        ),
        "seed_and_matter_profile_required_count": sum(
            1
            for item in checked_items
            if item.work_status == "seed_and_matter_profile_required"
        ),
        "gap_closure_count": sum(1 for item in checked_items if item.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for item in checked_items if item.seed_mutation_allowed
        ),
        "invalid_items": invalid_items,
    }
