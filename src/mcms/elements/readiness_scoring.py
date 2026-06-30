"""Purpose: deterministic readiness scoring for MCMS atom behavior evidence.

Project scope: summarizes admitted isotope evidence, atom behavior profile
availability, unresolved gap blockers, and source-policy availability without
creating evidence or predictions.
Dependencies: isotope evidence records, atom behavior profiles, atom behavior
gap receipts, isotope source policies, and full element snapshots.
Invariants: score records are read-only; scores never close gaps, generate atom
behavior profiles, mutate seeds, or override missing evidence receipts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.atom_behavior import list_atom_behavior_profiles
from mcms.elements.atom_behavior_gap import (
    AtomBehaviorGapReceipt,
    get_atom_behavior_gap_receipt,
)
from mcms.elements.evidence import (
    find_isotope_evidence_records,
    list_isotope_evidence_records,
)
from mcms.elements.isotope_source_policy import (
    get_isotope_source_policy,
)
from mcms.elements.snapshot import get_snapshot_record, list_full_snapshot_records

VALID_READINESS_SCORE_STATUSES = {
    "atom_behavior_ready_from_evidence",
    "atom_behavior_blocked_by_isotope_evidence",
    "atom_behavior_blocked_by_seed_and_matter",
}

_REQUIRED_ISOTOPE_FIELDS = (
    "mass_number",
    "neutron_count",
    "relative_atomic_mass",
    "source_keys",
    "stable_or_radioactive_classification",
)
_STABLE_ISOTOPE_FIELDS = ("isotopic_composition",)
_RADIOISOTOPE_FIELDS = ("half_life", "decay_mode")


def _round_score(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 4)


@dataclass(frozen=True)
class ElementReadinessScore:
    score_id: str
    symbol: str
    atomic_number: int
    isotope_record_count: int
    atom_behavior_profile_count: int
    evidence_completeness_score: float
    source_confidence_score: float
    behavior_readiness_score: float
    gap_priority_score: float
    constraint_tension_score: float
    readiness_status: str
    blocking_receipt_id: str | None
    source_policy_id: str | None
    scoring_basis: tuple[str, ...]
    seed_mutation_allowed: bool = False
    evidence_status: str = "element_readiness_score"
    notes: tuple[str, ...] = (
        "Readiness scores summarize existing evidence and gap receipts only.",
        "A high score does not create isotope evidence or close an unresolved receipt.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        if self.score_id != f"MSPEE-READINESS-SCORE-Z{self.atomic_number:03d}-{self.symbol}":
            errors.append("readiness score id is not canonical.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("readiness score atomic number must match snapshot.")
        if self.symbol != snapshot.symbol:
            errors.append("readiness score symbol must match snapshot.")
        if self.readiness_status not in VALID_READINESS_SCORE_STATUSES:
            errors.append("readiness score status is unknown.")
        for field_name in (
            "evidence_completeness_score",
            "source_confidence_score",
            "behavior_readiness_score",
            "gap_priority_score",
            "constraint_tension_score",
        ):
            value = getattr(self, field_name)
            if value < 0.0 or value > 1.0:
                errors.append(f"{field_name} must be in [0, 1].")
        if self.seed_mutation_allowed:
            errors.append("readiness scoring must not allow seed mutation.")
        if self.readiness_status == "atom_behavior_ready_from_evidence":
            if self.isotope_record_count <= 0:
                errors.append("ready score requires isotope evidence records.")
            if self.atom_behavior_profile_count <= 0:
                errors.append("ready score requires atom behavior profiles.")
            if self.blocking_receipt_id is not None:
                errors.append("ready score must not carry a blocking receipt.")
            if self.behavior_readiness_score != 1.0:
                errors.append("ready score must have behavior readiness of 1.0.")
        if self.readiness_status != "atom_behavior_ready_from_evidence":
            if not self.blocking_receipt_id:
                errors.append("blocked score requires a blocking receipt.")
            if self.behavior_readiness_score != 0.0:
                errors.append("blocked score must have behavior readiness of 0.0.")
        if not self.scoring_basis:
            errors.append("readiness score requires scoring basis.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["scoring_basis"] = list(self.scoring_basis)
        payload["notes"] = list(self.notes)
        return payload


def _evidence_completeness_score(symbol: str) -> float:
    try:
        records = find_isotope_evidence_records(symbol)
    except KeyError:
        return 0.0
    record_scores = []
    for record in records:
        required_field_count = len(_REQUIRED_ISOTOPE_FIELDS)
        present_field_count = required_field_count
        if record.evidence_status == "stable_isotope_evidence":
            required_field_count += len(_STABLE_ISOTOPE_FIELDS)
            present_field_count += int(record.isotopic_composition is not None)
        if record.evidence_status == "radioisotope_evidence":
            required_field_count += len(_RADIOISOTOPE_FIELDS)
            present_field_count += int(record.half_life_value is not None)
            present_field_count += int(record.decay_mode is not None)
        record_scores.append(present_field_count / required_field_count)
    return _round_score(sum(record_scores) / len(record_scores))


def _source_confidence_score(symbol: str, gap: AtomBehaviorGapReceipt | None) -> float:
    try:
        records = find_isotope_evidence_records(symbol)
    except KeyError:
        records = ()
    if records:
        source_counts = [min(len(record.source_keys), 2) / 2 for record in records]
        return _round_score(sum(source_counts) / len(source_counts))
    if gap is None:
        return 0.0
    try:
        policy = get_isotope_source_policy(symbol)
    except KeyError:
        return 0.0
    primary_sources = sum(
        1
        for candidate in policy.candidate_sources
        if candidate.candidate_status == "primary_source_required"
    )
    return _round_score(0.25 + min(primary_sources, 2) * 0.125)


def _gap_priority_score(gap: AtomBehaviorGapReceipt | None) -> float:
    if gap is None:
        return 0.0
    if gap.profile_blockers == ("isotope_evidence",):
        return 1.0
    return 0.5


def build_element_readiness_score(identifier: str | int) -> ElementReadinessScore:
    snapshot = get_snapshot_record(identifier)
    isotope_records = tuple(
        record
        for record in list_isotope_evidence_records()
        if record.symbol == snapshot.symbol
    )
    atom_behavior_profiles = tuple(
        profile
        for profile in list_atom_behavior_profiles()
        if profile.symbol == snapshot.symbol
    )
    try:
        gap = get_atom_behavior_gap_receipt(snapshot.symbol)
    except KeyError:
        gap = None
    try:
        policy = get_isotope_source_policy(snapshot.symbol)
    except KeyError:
        policy = None
    if atom_behavior_profiles:
        readiness_status = "atom_behavior_ready_from_evidence"
    elif gap and gap.profile_blockers == ("isotope_evidence",):
        readiness_status = "atom_behavior_blocked_by_isotope_evidence"
    else:
        readiness_status = "atom_behavior_blocked_by_seed_and_matter"
    behavior_readiness_score = 1.0 if atom_behavior_profiles else 0.0
    evidence_completeness_score = _evidence_completeness_score(snapshot.symbol)
    source_confidence_score = _source_confidence_score(snapshot.symbol, gap)
    gap_priority_score = _gap_priority_score(gap)
    constraint_tension_score = _round_score(
        1.0
        - (
            evidence_completeness_score * 0.4
            + source_confidence_score * 0.2
            + behavior_readiness_score * 0.4
        )
    )
    score = ElementReadinessScore(
        score_id=f"MSPEE-READINESS-SCORE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}",
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        isotope_record_count=len(isotope_records),
        atom_behavior_profile_count=len(atom_behavior_profiles),
        evidence_completeness_score=evidence_completeness_score,
        source_confidence_score=source_confidence_score,
        behavior_readiness_score=behavior_readiness_score,
        gap_priority_score=gap_priority_score,
        constraint_tension_score=constraint_tension_score,
        readiness_status=readiness_status,
        blocking_receipt_id=gap.receipt_id if gap else None,
        source_policy_id=policy.policy_id if policy else None,
        scoring_basis=(
            "isotope_evidence_records",
            "atom_behavior_profiles",
            "atom_behavior_gap_receipts",
            "isotope_source_policies",
        ),
    )
    validation_errors = score.validate()
    if validation_errors:
        raise ValueError("; ".join(validation_errors))
    return score


def list_element_readiness_scores() -> tuple[ElementReadinessScore, ...]:
    return tuple(
        build_element_readiness_score(record.symbol)
        for record in list_full_snapshot_records()
    )


def get_element_readiness_score(identifier: str | int) -> ElementReadinessScore:
    return build_element_readiness_score(identifier)


def validate_element_readiness_scores(
    scores: tuple[ElementReadinessScore, ...] | None = None,
) -> dict[str, Any]:
    checked_scores = scores if scores is not None else list_element_readiness_scores()
    invalid_scores = tuple(score.score_id for score in checked_scores if score.validate())
    return {
        "validation_status": (
            "element_readiness_scores_validated"
            if not invalid_scores
            else "element_readiness_scores_rejected"
        ),
        "score_count": len(checked_scores),
        "ready_count": sum(
            1
            for score in checked_scores
            if score.readiness_status == "atom_behavior_ready_from_evidence"
        ),
        "blocked_by_isotope_evidence_count": sum(
            1
            for score in checked_scores
            if score.readiness_status == "atom_behavior_blocked_by_isotope_evidence"
        ),
        "blocked_by_seed_and_matter_count": sum(
            1
            for score in checked_scores
            if score.readiness_status == "atom_behavior_blocked_by_seed_and_matter"
        ),
        "high_priority_gap_count": sum(
            1 for score in checked_scores if score.gap_priority_score == 1.0
        ),
        "seed_mutation_allowed_count": sum(
            1 for score in checked_scores if score.seed_mutation_allowed
        ),
        "invalid_scores": invalid_scores,
    }
