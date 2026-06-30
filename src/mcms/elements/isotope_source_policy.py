"""Purpose: source policy for isotope evidence required by atom behavior v2.

Project scope: defines admissible isotope evidence sources for Level 1 elements
whose atom behavior profile is blocked only by unresolved isotope evidence.
Dependencies: atom behavior gap receipts.
Invariants: policy records do not import isotope values, close gaps, generate atom
behavior profiles, or mutate element seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.atom_behavior_gap import (
    AtomBehaviorGapReceipt,
    get_atom_behavior_gap_receipt,
    list_atom_behavior_gap_receipts,
)

VALID_ISOTOPE_SOURCE_CANDIDATE_STATUSES = {
    "primary_source_required",
    "bounded_secondary_source",
}
VALID_ISOTOPE_SOURCE_POLICY_STATUSES = {"isotope_source_policy_defined"}
VALID_ISOTOPE_GAP_CLOSURE_STATUSES = {"gap_not_closed_by_policy"}


@dataclass(frozen=True)
class IsotopeEvidenceSourceCandidate:
    source_key: str
    authority: str
    title: str
    url: str
    precedence_rank: int
    candidate_status: str
    allowed_evidence: tuple[str, ...]
    required_evidence: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.source_key:
            errors.append("isotope source candidate key is required.")
        if not self.authority:
            errors.append("isotope source candidate authority is required.")
        if not self.title:
            errors.append("isotope source candidate title is required.")
        if not self.url.startswith("https://"):
            errors.append("isotope source candidate url must be https.")
        if self.precedence_rank < 0:
            errors.append("isotope source candidate precedence rank must be non-negative.")
        if self.candidate_status not in VALID_ISOTOPE_SOURCE_CANDIDATE_STATUSES:
            errors.append("isotope source candidate status is unknown.")
        if not self.allowed_evidence:
            errors.append("isotope source candidate requires allowed evidence labels.")
        if "source_url_or_citation" not in self.required_evidence:
            errors.append("isotope source candidate requires source citation evidence.")
        if "source_authority_and_version" not in self.required_evidence:
            errors.append("isotope source candidate requires authority/version evidence.")
        if "retrieval_date" not in self.required_evidence:
            errors.append("isotope source candidate requires retrieval date evidence.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_evidence"] = list(self.allowed_evidence)
        payload["required_evidence"] = list(self.required_evidence)
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class IsotopeSourcePolicy:
    policy_id: str
    policy_status: str
    target_atom_behavior_gap_receipt_id: str
    target_unresolved_isotope_receipt_id: str
    symbol: str
    atomic_number: int
    missing_evidence: tuple[str, ...]
    candidate_sources: tuple[IsotopeEvidenceSourceCandidate, ...]
    admission_requirements: tuple[str, ...]
    source_precedence_order: tuple[str, ...]
    gap_closure_status: str
    atom_behavior_generation_allowed: bool
    seed_mutation_allowed: bool
    required_next_action: str
    notes: tuple[str, ...] = (
        "This policy authorizes source review criteria; it does not import isotope values.",
        "Atom behavior profiles remain blocked until source-specific isotope evidence is added.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        gap_receipt = get_atom_behavior_gap_receipt(self.target_atom_behavior_gap_receipt_id)
        if self.policy_id != (
            f"MSPEE-ISOTOPE-SOURCE-POLICY-Z{self.atomic_number:03d}-{self.symbol}"
        ):
            errors.append("isotope source policy id is not canonical.")
        if self.policy_status not in VALID_ISOTOPE_SOURCE_POLICY_STATUSES:
            errors.append("isotope source policy status is unknown.")
        if gap_receipt.profile_blockers != ("isotope_evidence",):
            errors.append("isotope source policy only applies to isotope-only atom behavior gaps.")
        if self.target_unresolved_isotope_receipt_id != (
            gap_receipt.target_unresolved_isotope_receipt_id
        ):
            errors.append("isotope source policy unresolved receipt target is inconsistent.")
        if self.symbol != gap_receipt.symbol:
            errors.append("isotope source policy symbol must match atom behavior gap.")
        if self.atomic_number != gap_receipt.atomic_number:
            errors.append("isotope source policy atomic number must match atom behavior gap.")
        if self.missing_evidence != gap_receipt.missing_evidence:
            errors.append("isotope source policy missing evidence must match gap receipt.")
        if len(self.candidate_sources) != 3:
            errors.append("isotope source policy requires three candidate sources.")
        if "isotope_specific_source_receipt" not in self.admission_requirements:
            errors.append("isotope source policy requires an isotope-specific source receipt.")
        if "mass_number" not in self.admission_requirements:
            errors.append("isotope source policy requires mass-number evidence.")
        if "relative_atomic_mass" not in self.admission_requirements:
            errors.append("isotope source policy requires relative atomic mass evidence.")
        if "primary_source_precedence" not in self.source_precedence_order:
            errors.append("isotope source policy requires primary-source precedence.")
        if self.gap_closure_status not in VALID_ISOTOPE_GAP_CLOSURE_STATUSES:
            errors.append("isotope source policy gap closure status is unknown.")
        if self.atom_behavior_generation_allowed:
            errors.append("isotope source policy alone must not generate atom behavior profiles.")
        if self.seed_mutation_allowed:
            errors.append("isotope source policy must not allow seed mutation.")
        if not self.required_next_action:
            errors.append("isotope source policy requires a next action.")
        for candidate in self.candidate_sources:
            errors.extend(candidate.validate())
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["missing_evidence"] = list(self.missing_evidence)
        payload["candidate_sources"] = [
            candidate.to_dict() for candidate in self.candidate_sources
        ]
        payload["admission_requirements"] = list(self.admission_requirements)
        payload["source_precedence_order"] = list(self.source_precedence_order)
        payload["notes"] = list(self.notes)
        return payload


_COMMON_REQUIRED_EVIDENCE = (
    "source_url_or_citation",
    "source_authority_and_version",
    "field_name_mapping",
    "retrieval_date",
    "license_or_usage_boundary",
)

_CANDIDATE_SOURCES = (
    IsotopeEvidenceSourceCandidate(
        source_key="ciaaw_isotopic_compositions_2024",
        authority="CIAAW/IUPAC",
        title="Isotopic Compositions of the Elements 2024",
        url="https://www.ciaaw.org/isotopic-abundances.htm",
        precedence_rank=0,
        candidate_status="primary_source_required",
        allowed_evidence=(
            "stable_isotope_list",
            "natural_abundance",
            "isotopic_composition",
        ),
        required_evidence=_COMMON_REQUIRED_EVIDENCE,
        notes=("Primary authority for stable isotope composition and abundance.",),
    ),
    IsotopeEvidenceSourceCandidate(
        source_key="nist_atomic_weights_isotopic_compositions",
        authority="NIST",
        title="Atomic Weights and Isotopic Compositions",
        url="https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl",
        precedence_rank=1,
        candidate_status="primary_source_required",
        allowed_evidence=(
            "stable_isotope_list",
            "relative_atomic_mass",
            "isotopic_composition",
        ),
        required_evidence=_COMMON_REQUIRED_EVIDENCE,
        notes=("Primary cross-check for isotope mass and composition fields.",),
    ),
    IsotopeEvidenceSourceCandidate(
        source_key="pubchem_isotope_record_candidate",
        authority="PubChem/NCBI",
        title="PubChem isotope compound summaries",
        url="https://pubchem.ncbi.nlm.nih.gov/",
        precedence_rank=2,
        candidate_status="bounded_secondary_source",
        allowed_evidence=(
            "radioisotope_list",
            "half_life_or_stability_status",
            "decay_mode_when_radioactive",
        ),
        required_evidence=_COMMON_REQUIRED_EVIDENCE,
        notes=(
            "Bounded secondary context for radioisotope records when primary tables "
            "do not provide the needed decay fields.",
        ),
    ),
)


def _policy_id(receipt: AtomBehaviorGapReceipt) -> str:
    return f"MSPEE-ISOTOPE-SOURCE-POLICY-Z{receipt.atomic_number:03d}-{receipt.symbol}"


def _build_isotope_source_policy(receipt: AtomBehaviorGapReceipt) -> IsotopeSourcePolicy:
    if receipt.profile_blockers != ("isotope_evidence",):
        raise KeyError(
            f"isotope source policy is only available for isotope-only gaps: {receipt.symbol}"
        )
    return IsotopeSourcePolicy(
        policy_id=_policy_id(receipt),
        policy_status="isotope_source_policy_defined",
        target_atom_behavior_gap_receipt_id=receipt.receipt_id,
        target_unresolved_isotope_receipt_id=receipt.target_unresolved_isotope_receipt_id,
        symbol=receipt.symbol,
        atomic_number=receipt.atomic_number,
        missing_evidence=receipt.missing_evidence,
        candidate_sources=_CANDIDATE_SOURCES,
        admission_requirements=(
            "isotope_specific_source_receipt",
            "source_authority_and_version",
            "source_url_or_citation",
            "retrieval_date",
            "mass_number",
            "relative_atomic_mass",
            "stable_or_radioactive_classification",
            "natural_abundance_when_stable",
            "half_life_when_radioactive",
            "decay_mode_when_radioactive",
            "conflict_receipt_if_sources_disagree",
            "operator_approval_before_profile_generation",
        ),
        source_precedence_order=(
            "primary_source_precedence",
            "ciaaw_stable_isotope_composition",
            "nist_isotope_mass_cross_check",
            "pubchem_radioisotope_secondary_context",
            "unresolved_status_if_no_admissible_source",
        ),
        gap_closure_status="gap_not_closed_by_policy",
        atom_behavior_generation_allowed=False,
        seed_mutation_allowed=False,
        required_next_action=(
            "collect an isotope-specific source receipt for this element and validate it "
            "against the source policy before adding isotope evidence"
        ),
    )


def list_isotope_source_policies() -> tuple[IsotopeSourcePolicy, ...]:
    return tuple(
        _build_isotope_source_policy(receipt)
        for receipt in list_atom_behavior_gap_receipts()
        if receipt.profile_blockers == ("isotope_evidence",)
    )


def get_isotope_source_policy(identifier: str | int) -> IsotopeSourcePolicy:
    identifier_text = str(identifier).strip()
    for policy in list_isotope_source_policies():
        if (
            identifier_text == str(policy.atomic_number)
            or identifier_text.upper() == policy.symbol.upper()
            or identifier_text == policy.target_atom_behavior_gap_receipt_id
            or identifier_text == policy.target_unresolved_isotope_receipt_id
            or identifier_text == policy.policy_id
        ):
            return policy
    raise KeyError(f"unknown isotope source policy: {identifier_text}")


def validate_isotope_source_policies(
    policies: tuple[IsotopeSourcePolicy, ...] | None = None,
) -> dict[str, Any]:
    checked_policies = policies if policies is not None else list_isotope_source_policies()
    invalid_policies = tuple(policy.policy_id for policy in checked_policies if policy.validate())
    return {
        "validation_status": (
            "isotope_source_policies_validated"
            if not invalid_policies
            else "isotope_source_policies_rejected"
        ),
        "policy_count": len(checked_policies),
        "candidate_source_count": len(_CANDIDATE_SOURCES),
        "primary_source_candidate_count": sum(
            1
            for candidate in _CANDIDATE_SOURCES
            if candidate.candidate_status == "primary_source_required"
        ),
        "bounded_secondary_candidate_count": sum(
            1
            for candidate in _CANDIDATE_SOURCES
            if candidate.candidate_status == "bounded_secondary_source"
        ),
        "gap_closure_count": sum(
            1
            for policy in checked_policies
            if policy.gap_closure_status != "gap_not_closed_by_policy"
        ),
        "atom_behavior_generation_allowed_count": sum(
            1 for policy in checked_policies if policy.atom_behavior_generation_allowed
        ),
        "seed_mutation_allowed_count": sum(
            1 for policy in checked_policies if policy.seed_mutation_allowed
        ),
        "invalid_policies": invalid_policies,
    }
