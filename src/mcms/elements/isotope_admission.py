"""Purpose: record isotope candidate admission receipts for atom behavior v2.

Project scope: preserves the causal link between closed isotope candidate work
and canonical isotope evidence rows.
Dependencies: isotope evidence records and atom behavior profiles.
Invariants: admission receipts are read-only; they do not retain active
candidate receipts, create evidence rows, close current gaps, or mutate seeds.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.evidence import find_isotope_evidence_records

VALID_ISOTOPE_CANDIDATE_ADMISSION_STATUSES = {
    "isotope_candidate_admitted_to_canonical_evidence",
    "isotope_candidate_not_admitted_pending_review",
    "isotope_candidate_rejected",
}
VALID_ISOTOPE_CANDIDATE_RETENTION_STATUSES = {
    "candidate_receipt_closed_after_canonical_admission",
    "candidate_receipt_retained_for_review",
    "candidate_receipt_rejected",
}


@dataclass(frozen=True)
class IsotopeCandidateAdmissionReceipt:
    receipt_id: str
    source_candidate_receipt_id: str
    symbol: str
    atomic_number: int
    admitted_isotope_ids: tuple[str, ...]
    admitted_mass_numbers: tuple[int, ...]
    required_source_keys: tuple[str, ...]
    source_citations: tuple[str, ...]
    admission_status: str
    admission_reason: str
    candidate_retention_status: str
    active_candidate_receipt_retained: bool
    canonical_evidence_update_applied: bool
    atom_behavior_profiles_available: bool
    seed_mutation_allowed: bool
    evidence_status: str = "isotope_candidate_admission_receipt"
    notes: tuple[str, ...] = (
        "Admission receipts are historical audit records, not active candidates.",
        "Canonical isotope evidence remains the source for atom behavior generation.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        records = find_isotope_evidence_records(self.symbol)
        record_ids = tuple(record.isotope_id for record in records)
        record_mass_numbers = tuple(record.mass_number for record in records)
        if self.atomic_number not in {record.atomic_number for record in records}:
            errors.append("admission atomic number must match isotope evidence records.")
        if self.admitted_isotope_ids != record_ids:
            errors.append("admitted isotope ids must match canonical isotope evidence rows.")
        if self.admitted_mass_numbers != record_mass_numbers:
            errors.append("admitted mass numbers must match canonical isotope evidence rows.")
        for record in records:
            missing_keys = set(self.required_source_keys).difference(record.source_keys)
            if missing_keys:
                errors.append(
                    f"admitted isotope record {record.isotope_id} lacks required source keys."
                )
        if self.admission_status not in VALID_ISOTOPE_CANDIDATE_ADMISSION_STATUSES:
            errors.append("isotope candidate admission status is unknown.")
        if self.candidate_retention_status not in VALID_ISOTOPE_CANDIDATE_RETENTION_STATUSES:
            errors.append("isotope candidate retention status is unknown.")
        if not self.source_candidate_receipt_id:
            errors.append("source candidate receipt id is required.")
        if not self.source_citations:
            errors.append("source citations are required.")
        if not self.admission_reason:
            errors.append("admission reason is required.")
        if self.seed_mutation_allowed:
            errors.append("isotope admission receipts must not allow seed mutation.")
        if self.admission_status == "isotope_candidate_admitted_to_canonical_evidence":
            if self.active_candidate_receipt_retained:
                errors.append("admitted isotope candidate must not remain active.")
            if not self.canonical_evidence_update_applied:
                errors.append("admitted isotope candidate requires canonical evidence update.")
            if self.candidate_retention_status != (
                "candidate_receipt_closed_after_canonical_admission"
            ):
                errors.append("admitted isotope candidate requires closed candidate status.")
        if self.atom_behavior_profiles_available:
            from mcms.elements.atom_behavior import find_atom_behavior_profile

            for mass_number in self.admitted_mass_numbers:
                try:
                    find_atom_behavior_profile(self.symbol, mass_number=mass_number)
                except KeyError:
                    errors.append(
                        f"atom behavior profile is missing for {self.symbol}-{mass_number}."
                    )
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["admitted_isotope_ids"] = list(self.admitted_isotope_ids)
        payload["admitted_mass_numbers"] = list(self.admitted_mass_numbers)
        payload["required_source_keys"] = list(self.required_source_keys)
        payload["source_citations"] = list(self.source_citations)
        payload["notes"] = list(self.notes)
        return payload


def list_isotope_candidate_admission_receipts() -> tuple[
    IsotopeCandidateAdmissionReceipt, ...
]:
    oxygen_records = find_isotope_evidence_records("O")
    technetium_records = find_isotope_evidence_records("Tc")
    return (
        IsotopeCandidateAdmissionReceipt(
            receipt_id="MSPEE-ISOTOPE-CANDIDATE-ADMISSION-Z008-O",
            source_candidate_receipt_id=(
                "MSPEE-ISOTOPE-CANDIDATE-EVIDENCE-Z008-O-NIST"
            ),
            symbol="O",
            atomic_number=8,
            admitted_isotope_ids=tuple(record.isotope_id for record in oxygen_records),
            admitted_mass_numbers=tuple(record.mass_number for record in oxygen_records),
            required_source_keys=(
                "ciaaw_isotopic_compositions_2024",
                "nist_atomic_weights_isotopic_compositions",
            ),
            source_citations=(
                "CIAAW isotopic compositions 2024",
                "NIST Atomic Weights and Isotopic Compositions for Oxygen",
            ),
            admission_status="isotope_candidate_admitted_to_canonical_evidence",
            admission_reason=(
                "O-16/O-17/O-18 have source-backed canonical isotope evidence "
                "from CIAAW and NIST; the candidate receipt is closed after admission."
            ),
            candidate_retention_status="candidate_receipt_closed_after_canonical_admission",
            active_candidate_receipt_retained=False,
            canonical_evidence_update_applied=True,
            atom_behavior_profiles_available=True,
            seed_mutation_allowed=False,
        ),
        IsotopeCandidateAdmissionReceipt(
            receipt_id="MSPEE-ISOTOPE-CANDIDATE-ADMISSION-Z043-Tc",
            source_candidate_receipt_id=(
                "MSPEE-ISOTOPE-CANDIDATE-EVIDENCE-Z043-Tc-NIST-EPA"
            ),
            symbol="Tc",
            atomic_number=43,
            admitted_isotope_ids=tuple(
                record.isotope_id for record in technetium_records
            ),
            admitted_mass_numbers=tuple(
                record.mass_number for record in technetium_records
            ),
            required_source_keys=(
                "nist_atomic_weights_isotopic_compositions",
                "epa_radionuclide_basics_tc99",
            ),
            source_citations=(
                "NIST Atomic Weights and Isotopic Compositions for Technetium",
                "US EPA Radionuclide Basics: Technetium-99",
            ),
            admission_status="isotope_candidate_admitted_to_canonical_evidence",
            admission_reason=(
                "Tc-99 has source-backed canonical isotope mass evidence from NIST "
                "and radioisotope half-life/decay context from EPA; the candidate "
                "receipt is closed after admission."
            ),
            candidate_retention_status="candidate_receipt_closed_after_canonical_admission",
            active_candidate_receipt_retained=False,
            canonical_evidence_update_applied=True,
            atom_behavior_profiles_available=True,
            seed_mutation_allowed=False,
        ),
    )


def get_isotope_candidate_admission_receipt(
    identifier: str | int,
) -> IsotopeCandidateAdmissionReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_isotope_candidate_admission_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.source_candidate_receipt_id
            or identifier_text in receipt.admitted_isotope_ids
        ):
            return receipt
    raise KeyError(f"unknown isotope candidate admission receipt: {identifier_text}")


def validate_isotope_candidate_admission_receipts(
    receipts: tuple[IsotopeCandidateAdmissionReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_isotope_candidate_admission_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    return {
        "validation_status": (
            "isotope_candidate_admission_receipts_validated"
            if not invalid_receipts
            else "isotope_candidate_admission_receipts_rejected"
        ),
        "receipt_count": len(checked_receipts),
        "admitted_to_canonical_count": sum(
            1
            for receipt in checked_receipts
            if receipt.admission_status == "isotope_candidate_admitted_to_canonical_evidence"
        ),
        "admitted_isotope_count": sum(
            len(receipt.admitted_isotope_ids) for receipt in checked_receipts
        ),
        "active_candidate_retained_count": sum(
            1 for receipt in checked_receipts if receipt.active_candidate_receipt_retained
        ),
        "canonical_evidence_update_count": sum(
            1 for receipt in checked_receipts if receipt.canonical_evidence_update_applied
        ),
        "atom_behavior_profiles_available_count": sum(
            1 for receipt in checked_receipts if receipt.atom_behavior_profiles_available
        ),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
