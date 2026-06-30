"""Purpose: record active isotope source searches for atom behavior v2 gaps.

Project scope: creates governed search receipts for isotope-only atom behavior
blockers before any isotope evidence value is imported.
Dependencies: isotope source policy records.
Invariants: source-search receipts do not contain isotope values, close gaps,
generate atom behavior profiles, or mutate element seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.isotope_source_policy import (
    get_isotope_source_policy,
    list_isotope_source_policies,
)

VALID_ISOTOPE_SOURCE_SEARCH_STATUSES = {
    "isotope_source_search_open",
    "isotope_source_search_blocked",
    "isotope_source_search_complete_pending_receipt",
    "isotope_source_search_complete_candidate_receipt_created",
}
OXYGEN_NIST_CANDIDATE_RECEIPT_ID = "MSPEE-ISOTOPE-CANDIDATE-EVIDENCE-Z008-O-NIST"


@dataclass(frozen=True)
class IsotopeSourceSearchReceipt:
    search_id: str
    policy_id: str
    target_atom_behavior_gap_receipt_id: str
    target_unresolved_isotope_receipt_id: str
    symbol: str
    atomic_number: int
    search_status: str
    candidate_source_keys: tuple[str, ...]
    required_evidence: tuple[str, ...]
    candidate_receipt_id: str | None
    search_reason: str
    required_next_action: str
    closes_gap: bool = False
    atom_behavior_generation_allowed: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "isotope_source_search_receipt"
    notes: tuple[str, ...] = (
        "Isotope source-search receipts track evidence collection only.",
        "A source-search receipt does not contain or admit isotope values.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        policy = get_isotope_source_policy(self.policy_id)
        policy_source_keys = {candidate.source_key for candidate in policy.candidate_sources}
        if self.target_atom_behavior_gap_receipt_id != (
            policy.target_atom_behavior_gap_receipt_id
        ):
            errors.append("isotope source-search gap receipt must match policy.")
        if self.target_unresolved_isotope_receipt_id != (
            policy.target_unresolved_isotope_receipt_id
        ):
            errors.append("isotope source-search unresolved receipt must match policy.")
        if self.symbol != policy.symbol:
            errors.append("isotope source-search symbol must match policy.")
        if self.atomic_number != policy.atomic_number:
            errors.append("isotope source-search atomic number must match policy.")
        if self.search_status not in VALID_ISOTOPE_SOURCE_SEARCH_STATUSES:
            errors.append("isotope source-search status is unknown.")
        if (
            self.search_status == "isotope_source_search_complete_candidate_receipt_created"
            and not self.candidate_receipt_id
        ):
            errors.append("completed isotope source-search requires candidate receipt id.")
        if not self.candidate_source_keys:
            errors.append("isotope source-search requires candidate source keys.")
        if not set(self.candidate_source_keys).issubset(policy_source_keys):
            errors.append("isotope source-search candidates must be allowed by policy.")
        if "source_url_or_citation" not in self.required_evidence:
            errors.append("isotope source-search requires source citation evidence.")
        if "source_authority_and_version" not in self.required_evidence:
            errors.append("isotope source-search requires authority/version evidence.")
        if "mass_number" not in self.required_evidence:
            errors.append("isotope source-search requires mass-number evidence.")
        if "relative_atomic_mass" not in self.required_evidence:
            errors.append("isotope source-search requires relative atomic mass evidence.")
        if "stable_or_radioactive_classification" not in self.required_evidence:
            errors.append("isotope source-search requires stability classification evidence.")
        if "retrieval_date" not in self.required_evidence:
            errors.append("isotope source-search requires retrieval date evidence.")
        if not self.search_reason:
            errors.append("isotope source-search requires a search reason.")
        if not self.required_next_action:
            errors.append("isotope source-search requires a next action.")
        if self.closes_gap:
            errors.append("isotope source-search must not close a gap.")
        if self.atom_behavior_generation_allowed:
            errors.append("isotope source-search must not generate atom behavior profiles.")
        if self.seed_mutation_allowed:
            errors.append("isotope source-search must not allow seed mutation.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidate_source_keys"] = list(self.candidate_source_keys)
        payload["required_evidence"] = list(self.required_evidence)
        payload["notes"] = list(self.notes)
        return payload


def _build_isotope_source_search_receipt(
    identifier: str | int,
) -> IsotopeSourceSearchReceipt:
    policy = get_isotope_source_policy(identifier)
    search_status = "isotope_source_search_open"
    candidate_receipt_id = None
    required_next_action = (
        "collect a source-specific isotope evidence receipt and validate it "
        "against the isotope source policy before profile generation"
    )
    if policy.symbol == "O":
        search_status = "isotope_source_search_complete_candidate_receipt_created"
        candidate_receipt_id = OXYGEN_NIST_CANDIDATE_RECEIPT_ID
        required_next_action = (
            "review the Oxygen NIST isotope candidate receipt before any isotope "
            "evidence admission or atom behavior profile generation"
        )
    return IsotopeSourceSearchReceipt(
        search_id=(
            f"MSPEE-ISOTOPE-SOURCE-SEARCH-"
            f"Z{policy.atomic_number:03d}-{policy.symbol}"
        ),
        policy_id=policy.policy_id,
        target_atom_behavior_gap_receipt_id=policy.target_atom_behavior_gap_receipt_id,
        target_unresolved_isotope_receipt_id=policy.target_unresolved_isotope_receipt_id,
        symbol=policy.symbol,
        atomic_number=policy.atomic_number,
        search_status=search_status,
        candidate_source_keys=tuple(
            candidate.source_key for candidate in policy.candidate_sources
        ),
        required_evidence=(
            "source_url_or_citation",
            "source_authority_and_version",
            "field_name_mapping",
            "retrieval_date",
            "license_or_usage_boundary",
            "mass_number",
            "relative_atomic_mass",
            "stable_or_radioactive_classification",
            "natural_abundance_when_stable",
            "half_life_when_radioactive",
            "decay_mode_when_radioactive",
            "conflict_status",
        ),
        candidate_receipt_id=candidate_receipt_id,
        search_reason=(
            f"{policy.symbol} has an isotope-only atom behavior blocker and requires "
            "source-specific isotope evidence before profile generation."
        ),
        required_next_action=required_next_action,
    )


def list_isotope_source_search_receipts() -> tuple[IsotopeSourceSearchReceipt, ...]:
    return tuple(
        _build_isotope_source_search_receipt(policy.policy_id)
        for policy in list_isotope_source_policies()
    )


def get_isotope_source_search_receipt(
    identifier: str | int,
) -> IsotopeSourceSearchReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_isotope_source_search_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.search_id
            or identifier_text == receipt.policy_id
            or identifier_text == receipt.target_atom_behavior_gap_receipt_id
            or identifier_text == receipt.target_unresolved_isotope_receipt_id
        ):
            return receipt
    raise KeyError(f"unknown isotope source-search receipt: {identifier_text}")


def validate_isotope_source_search_receipts(
    receipts: tuple[IsotopeSourceSearchReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_isotope_source_search_receipts()
    )
    invalid_receipts = tuple(
        receipt.search_id for receipt in checked_receipts if receipt.validate()
    )
    return {
        "validation_status": (
            "isotope_source_search_receipts_validated"
            if not invalid_receipts
            else "isotope_source_search_receipts_rejected"
        ),
        "search_receipt_count": len(checked_receipts),
        "open_search_count": sum(
            1
            for receipt in checked_receipts
            if receipt.search_status == "isotope_source_search_open"
        ),
        "candidate_receipt_created_count": sum(
            1
            for receipt in checked_receipts
            if receipt.search_status
            == "isotope_source_search_complete_candidate_receipt_created"
        ),
        "candidate_source_count": len(
            {
                source_key
                for receipt in checked_receipts
                for source_key in receipt.candidate_source_keys
            }
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
