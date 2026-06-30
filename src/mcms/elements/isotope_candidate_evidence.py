"""Purpose: define source-specific isotope candidate evidence receipts.

Project scope: models isotope evidence candidates collected under atom behavior
v2 isotope source policies before admission into canonical isotope evidence.
Dependencies: isotope source policy, isotope source search, and isotope instances.
Invariants: candidate receipts do not close gaps, generate atom behavior profiles,
or mutate seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.instances import build_isotope_instance
from mcms.elements.isotope_source_policy import get_isotope_source_policy
from mcms.elements.isotope_source_search import (
    get_isotope_source_search_receipt,
)

VALID_ISOTOPE_CANDIDATE_EVIDENCE_STATUSES = {
    "isotope_evidence_candidate",
    "isotope_evidence_rejected",
}
VALID_ISOTOPE_CANDIDATE_DECISIONS = {
    "awaiting_isotope_admission_review",
    "reject_after_review",
}
VALID_ISOTOPE_CANDIDATE_STABILITY_CLASSES = {"stable", "radioactive"}


@dataclass(frozen=True)
class IsotopeCandidateValue:
    isotope_id: str
    mass_number: int
    neutron_count: int
    relative_atomic_mass: str
    isotopic_composition: str | None
    stability_classification: str
    half_life_value: str | None
    half_life_unit: str | None
    decay_mode: str | None
    source_value_note: str

    def validate(self, symbol: str) -> list[str]:
        errors: list[str] = []
        isotope = build_isotope_instance(symbol, self.mass_number)
        if self.isotope_id != isotope.instance_id:
            errors.append("isotope candidate id must match canonical isotope instance id.")
        if self.neutron_count != isotope.neutron_count:
            errors.append("isotope candidate neutron count must match isotope instance.")
        if not self.relative_atomic_mass:
            errors.append("isotope candidate requires relative atomic mass.")
        if self.stability_classification not in VALID_ISOTOPE_CANDIDATE_STABILITY_CLASSES:
            errors.append("isotope candidate stability classification is unknown.")
        if self.stability_classification == "stable":
            if self.isotopic_composition is None:
                errors.append("stable isotope candidate requires isotopic composition.")
            if (
                self.half_life_value is not None
                or self.half_life_unit is not None
                or self.decay_mode is not None
            ):
                errors.append("stable isotope candidate must not carry decay fields.")
        if self.stability_classification == "radioactive":
            if not self.half_life_value or not self.half_life_unit or not self.decay_mode:
                errors.append("radioactive isotope candidate requires decay fields.")
        if not self.source_value_note:
            errors.append("isotope candidate requires a source value note.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IsotopeCandidateEvidenceReceipt:
    receipt_id: str
    policy_id: str
    source_search_id: str
    target_atom_behavior_gap_receipt_id: str
    target_unresolved_isotope_receipt_id: str
    symbol: str
    atomic_number: int
    source_key: str
    source_authority: str
    source_title: str
    source_citation: str
    retrieval_date: str
    field_name_mapping: str
    source_license_boundary: str
    standard_atomic_weight_interval: str
    candidate_values: tuple[IsotopeCandidateValue, ...]
    admission_status: str
    admission_decision: str
    conflict_status: str
    closes_gap: bool = False
    atom_behavior_generation_allowed: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "isotope_candidate_evidence_receipt"
    notes: tuple[str, ...] = (
        "Candidate isotope evidence is source-specific and not admitted evidence.",
        "Atom behavior profile generation requires a later admission decision.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        policy = get_isotope_source_policy(self.policy_id)
        search = get_isotope_source_search_receipt(self.source_search_id)
        candidate_by_key = {
            candidate.source_key: candidate for candidate in policy.candidate_sources
        }
        candidate = candidate_by_key.get(self.source_key)
        if self.target_atom_behavior_gap_receipt_id != (
            policy.target_atom_behavior_gap_receipt_id
        ):
            errors.append("isotope candidate gap receipt must match policy.")
        if self.target_unresolved_isotope_receipt_id != (
            policy.target_unresolved_isotope_receipt_id
        ):
            errors.append("isotope candidate unresolved receipt must match policy.")
        if self.symbol != policy.symbol:
            errors.append("isotope candidate symbol must match policy.")
        if self.atomic_number != policy.atomic_number:
            errors.append("isotope candidate atomic number must match policy.")
        if self.policy_id != search.policy_id:
            errors.append("isotope candidate search must target the same policy.")
        if search.candidate_receipt_id != self.receipt_id:
            errors.append("isotope candidate receipt id must match source-search pointer.")
        if candidate is None:
            errors.append("isotope candidate source key must be allowed by policy.")
        elif not {
            "stable_isotope_list",
            "relative_atomic_mass",
            "isotopic_composition",
        }.issubset(set(candidate.allowed_evidence)):
            errors.append("isotope candidate source lacks required isotope evidence classes.")
        if self.admission_status not in VALID_ISOTOPE_CANDIDATE_EVIDENCE_STATUSES:
            errors.append("isotope candidate evidence status is unknown.")
        if self.admission_decision not in VALID_ISOTOPE_CANDIDATE_DECISIONS:
            errors.append("isotope candidate admission decision is unknown.")
        if not self.standard_atomic_weight_interval:
            errors.append("isotope candidate requires standard atomic weight interval.")
        if not self.candidate_values:
            errors.append("isotope candidate requires isotope value rows.")
        for value in self.candidate_values:
            errors.extend(value.validate(self.symbol))
        required_text_fields = (
            self.source_authority,
            self.source_title,
            self.source_citation,
            self.retrieval_date,
            self.field_name_mapping,
            self.source_license_boundary,
            self.conflict_status,
        )
        if any(not field for field in required_text_fields):
            errors.append("isotope candidate requires complete provenance fields.")
        if self.closes_gap:
            errors.append("isotope candidate receipt must not close a gap.")
        if self.atom_behavior_generation_allowed:
            errors.append("isotope candidate receipt must not generate atom behavior profiles.")
        if self.seed_mutation_allowed:
            errors.append("isotope candidate receipt must not allow seed mutation.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidate_values"] = [value.to_dict() for value in self.candidate_values]
        payload["notes"] = list(self.notes)
        return payload


def list_isotope_candidate_evidence_receipts() -> tuple[
    IsotopeCandidateEvidenceReceipt, ...
]:
    return ()


def get_isotope_candidate_evidence_receipt(
    identifier: str | int,
) -> IsotopeCandidateEvidenceReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_isotope_candidate_evidence_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.policy_id
            or identifier_text == receipt.source_search_id
            or identifier_text == receipt.target_atom_behavior_gap_receipt_id
            or identifier_text == receipt.target_unresolved_isotope_receipt_id
        ):
            return receipt
    raise KeyError(f"unknown isotope candidate evidence receipt: {identifier_text}")


def validate_isotope_candidate_evidence_receipts(
    receipts: tuple[IsotopeCandidateEvidenceReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_isotope_candidate_evidence_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    candidate_values = tuple(
        value for receipt in checked_receipts for value in receipt.candidate_values
    )
    return {
        "validation_status": (
            "isotope_candidate_evidence_receipts_validated"
            if not invalid_receipts
            else "isotope_candidate_evidence_receipts_rejected"
        ),
        "receipt_count": len(checked_receipts),
        "candidate_isotope_count": len(candidate_values),
        "stable_candidate_count": sum(
            1 for value in candidate_values if value.stability_classification == "stable"
        ),
        "radioisotope_candidate_count": sum(
            1
            for value in candidate_values
            if value.stability_classification == "radioactive"
        ),
        "admitted_count": sum(
            1
            for receipt in checked_receipts
            if receipt.admission_status == "isotope_evidence_admitted"
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "atom_behavior_generation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.atom_behavior_generation_allowed
        ),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }


def build_isotope_candidate_evidence_template(
    identifier: str | int,
    *,
    source_key: str = "nist_atomic_weights_isotopic_compositions",
) -> dict[str, Any]:
    policy = get_isotope_source_policy(identifier)
    search = get_isotope_source_search_receipt(identifier)
    if source_key not in {candidate.source_key for candidate in policy.candidate_sources}:
        raise KeyError(f"unknown isotope source candidate for policy: {source_key}")
    return {
        "receipt_id": (
            f"MSPEE-ISOTOPE-CANDIDATE-EVIDENCE-"
            f"Z{policy.atomic_number:03d}-{policy.symbol}-{source_key}"
        ),
        "policy_id": policy.policy_id,
        "source_search_id": search.search_id,
        "target_atom_behavior_gap_receipt_id": policy.target_atom_behavior_gap_receipt_id,
        "target_unresolved_isotope_receipt_id": (
            policy.target_unresolved_isotope_receipt_id
        ),
        "symbol": policy.symbol,
        "atomic_number": policy.atomic_number,
        "source_key": source_key,
        "required_receipt_fields": (
            "source_authority",
            "source_title",
            "source_citation",
            "retrieval_date",
            "field_name_mapping",
            "source_license_boundary",
            "standard_atomic_weight_interval",
            "candidate_values",
            "conflict_status",
        ),
        "required_candidate_value_fields": (
            "isotope_id",
            "mass_number",
            "neutron_count",
            "relative_atomic_mass",
            "isotopic_composition",
            "stability_classification",
            "half_life_value",
            "half_life_unit",
            "decay_mode",
            "source_value_note",
        ),
        "default_admission_status": "isotope_evidence_candidate",
        "default_admission_decision": "awaiting_isotope_admission_review",
        "closes_gap": False,
        "atom_behavior_generation_allowed": False,
        "seed_mutation_allowed": False,
    }
