"""Purpose: Cs-Rn Level 1 promotion-readiness audit profiles.

Project scope: evaluates whether snapshot-only elements 55-86 have enough
source-backed evidence to become full Level 1 seed elements.
Dependencies: snapshot records, Level 1 seed lookup, physical-property evidence,
and f-block expansion profiles.
Invariants: readiness profiles never promote an element; they only state available
evidence, missing evidence, and blockers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.evidence import (
    find_physical_property_evidence_record,
    find_unresolved_physical_property_evidence_record,
)
from mcms.elements.phase3 import get_f_block_expansion_profile
from mcms.elements.seed import get_seed_element
from mcms.elements.snapshot import ElementSourceSnapshotRecord, get_snapshot_record

CS_RN_PROMOTION_SYMBOLS = (
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
)

LEVEL_1_PROMOTION_REQUIRED_EVIDENCE = (
    "nist_neutral_electron_configuration",
    "nist_first_cation_configuration",
    "configuration_audit",
    "frontier_signature",
    "valence_shell_signature",
    "oxidation_state_evidence",
    "relation_edges",
    "level_1_behavior_tags",
)

VALID_PROMOTION_READINESS_STATUSES = {
    "promotion_ready",
    "promotion_blocked_missing_source_evidence",
    "promotion_rejected_invalid_profile",
}


@dataclass(frozen=True)
class ElementPromotionReadinessProfile:
    element_id: str
    symbol: str
    atomic_number: int
    name: str
    target_level: str
    snapshot_available: bool
    level_1_seed_available: bool
    physical_property_evidence_available: bool
    unresolved_physical_property_evidence_available: bool
    f_block_profile_available: bool
    available_evidence: tuple[str, ...]
    required_missing_evidence: tuple[str, ...]
    promotion_blockers: tuple[str, ...]
    readiness_status: str
    notes: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not 55 <= self.atomic_number <= 86:
            errors.append("Cs-Rn promotion profile atomic number must be between 55 and 86.")
        if self.symbol not in CS_RN_PROMOTION_SYMBOLS:
            errors.append("profile symbol must be in the Cs-Rn promotion span.")
        if not self.snapshot_available:
            errors.append("promotion profile requires a full-snapshot source record.")
        if (
            self.physical_property_evidence_available
            and self.unresolved_physical_property_evidence_available
        ):
            errors.append(
                "physical-property evidence cannot be both complete and unresolved."
            )
        if self.readiness_status not in VALID_PROMOTION_READINESS_STATUSES:
            errors.append("promotion readiness status is unknown.")
        if self.readiness_status == "promotion_ready" and self.promotion_blockers:
            errors.append("promotion-ready profile must not contain blockers.")
        if (
            self.readiness_status == "promotion_blocked_missing_source_evidence"
            and not self.required_missing_evidence
        ):
            errors.append("blocked promotion profile must list missing evidence.")
        if self.required_missing_evidence and not self.promotion_blockers:
            errors.append("missing evidence must be represented as promotion blockers.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PromotionReadinessValidationResult:
    profile_count: int
    atomic_number_span: tuple[int, int]
    blocked_count: int
    ready_count: int
    physical_property_evidence_count: int
    unresolved_physical_property_evidence_count: int
    f_block_profile_count: int
    invalid_profiles: tuple[str, ...]
    validation_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _lookup_exists(lookup, identifier: str) -> bool:
    try:
        lookup(identifier)
    except KeyError:
        return False
    return True


def _configuration_evidence_exists(identifier: str) -> bool:
    from mcms.elements.configuration_evidence import find_configuration_evidence_record

    return _lookup_exists(find_configuration_evidence_record, identifier)


def _frontier_valence_signature_exists(identifier: str) -> bool:
    from mcms.elements.frontier_valence import find_frontier_valence_signature_record

    return _lookup_exists(find_frontier_valence_signature_record, identifier)


def _oxidation_state_evidence_exists(identifier: str) -> bool:
    from mcms.elements.oxidation_evidence import find_oxidation_state_evidence_record

    return _lookup_exists(find_oxidation_state_evidence_record, identifier)


def _behavior_tag_overlay_exists(identifier: str) -> bool:
    from mcms.elements.behavior_tags import find_behavior_tag_overlay_record

    return _lookup_exists(find_behavior_tag_overlay_record, identifier)


def _relation_overlay_exists(identifier: str) -> bool:
    from mcms.elements.relation_overlay import find_relation_overlay_record

    return _lookup_exists(find_relation_overlay_record, identifier)


def _profile_from_snapshot(
    record: ElementSourceSnapshotRecord,
) -> ElementPromotionReadinessProfile:
    element_id = f"MSPEE-Z{record.atomic_number:03d}-{record.symbol}"
    level_1_seed_available = _lookup_exists(get_seed_element, record.symbol)
    physical_property_evidence_available = _lookup_exists(
        find_physical_property_evidence_record,
        record.symbol,
    )
    unresolved_physical_property_evidence_available = _lookup_exists(
        find_unresolved_physical_property_evidence_record,
        record.symbol,
    )
    f_block_profile_available = _lookup_exists(get_f_block_expansion_profile, record.symbol)
    configuration_evidence_available = _configuration_evidence_exists(record.symbol)
    frontier_valence_signature_available = _frontier_valence_signature_exists(record.symbol)
    oxidation_state_evidence_available = _oxidation_state_evidence_exists(record.symbol)
    behavior_tag_overlay_available = _behavior_tag_overlay_exists(record.symbol)
    relation_overlay_available = _relation_overlay_exists(record.symbol)
    available_evidence = ["full_118_identity_snapshot"]
    if configuration_evidence_available:
        available_evidence.append("nist_configuration_evidence")
    if frontier_valence_signature_available:
        available_evidence.append("frontier_valence_signature")
    if oxidation_state_evidence_available:
        available_evidence.append("oxidation_state_evidence")
    if behavior_tag_overlay_available:
        available_evidence.append("level_1_behavior_tags")
    if relation_overlay_available:
        available_evidence.append("relation_edges")
    if physical_property_evidence_available:
        available_evidence.append("physical_property_evidence")
    if unresolved_physical_property_evidence_available:
        available_evidence.append("unresolved_physical_property_evidence")
    if f_block_profile_available:
        available_evidence.append("f_block_expansion_profile")
    required_missing_evidence = list(LEVEL_1_PROMOTION_REQUIRED_EVIDENCE)
    if configuration_evidence_available:
        required_missing_evidence = [
            evidence_name
            for evidence_name in required_missing_evidence
            if evidence_name
            not in {
                "nist_neutral_electron_configuration",
                "nist_first_cation_configuration",
                "configuration_audit",
            }
        ]
    if frontier_valence_signature_available:
        required_missing_evidence = [
            evidence_name
            for evidence_name in required_missing_evidence
            if evidence_name not in {"frontier_signature", "valence_shell_signature"}
        ]
    if oxidation_state_evidence_available:
        required_missing_evidence = [
            evidence_name
            for evidence_name in required_missing_evidence
            if evidence_name != "oxidation_state_evidence"
        ]
    if behavior_tag_overlay_available:
        required_missing_evidence = [
            evidence_name
            for evidence_name in required_missing_evidence
            if evidence_name != "level_1_behavior_tags"
        ]
    if relation_overlay_available:
        required_missing_evidence = [
            evidence_name
            for evidence_name in required_missing_evidence
            if evidence_name != "relation_edges"
        ]
    if unresolved_physical_property_evidence_available:
        required_missing_evidence.append("complete_physical_property_evidence")
    if level_1_seed_available:
        required_missing_evidence = []
    promotion_blockers = tuple(
        f"missing:{evidence_name}" for evidence_name in required_missing_evidence
    )
    return ElementPromotionReadinessProfile(
        element_id=element_id,
        symbol=record.symbol,
        atomic_number=record.atomic_number,
        name=record.name,
        target_level="level_1_seed_promotion",
        snapshot_available=True,
        level_1_seed_available=level_1_seed_available,
        physical_property_evidence_available=physical_property_evidence_available,
        unresolved_physical_property_evidence_available=(
            unresolved_physical_property_evidence_available
        ),
        f_block_profile_available=f_block_profile_available,
        available_evidence=tuple(available_evidence),
        required_missing_evidence=tuple(required_missing_evidence),
        promotion_blockers=promotion_blockers,
        readiness_status=(
            "promotion_ready"
            if not promotion_blockers
            else "promotion_blocked_missing_source_evidence"
        ),
        notes=(
            "Profile is a promotion audit, not a promoted element seed.",
            "Source-backed configuration and behavior evidence must be added before promotion.",
        ),
    )


def list_cs_rn_promotion_readiness_profiles() -> tuple[ElementPromotionReadinessProfile, ...]:
    return tuple(
        _profile_from_snapshot(get_snapshot_record(symbol))
        for symbol in CS_RN_PROMOTION_SYMBOLS
    )


def get_cs_rn_promotion_readiness_profile(
    identifier: str | int,
) -> ElementPromotionReadinessProfile:
    record = get_snapshot_record(identifier)
    if record.symbol not in CS_RN_PROMOTION_SYMBOLS:
        raise KeyError(f"element is not in the Cs-Rn promotion-readiness span: {record.symbol}")
    return _profile_from_snapshot(record)


def validate_cs_rn_promotion_readiness_profiles(
    profiles: tuple[ElementPromotionReadinessProfile, ...] | None = None,
) -> PromotionReadinessValidationResult:
    checked_profiles = (
        profiles if profiles is not None else list_cs_rn_promotion_readiness_profiles()
    )
    invalid_profiles = tuple(
        profile.symbol for profile in checked_profiles if profile.validate()
    )
    observed_symbols = tuple(profile.symbol for profile in checked_profiles)
    observed_atomic_numbers = tuple(profile.atomic_number for profile in checked_profiles)
    validation_status = "cs_rn_promotion_readiness_profiles_validated"
    full_span_expected = profiles is None or len(checked_profiles) == len(CS_RN_PROMOTION_SYMBOLS)
    if invalid_profiles or (
        full_span_expected
        and (
            observed_symbols != CS_RN_PROMOTION_SYMBOLS
            or observed_atomic_numbers != tuple(range(55, 87))
        )
    ):
        validation_status = "cs_rn_promotion_readiness_profiles_rejected"
    return PromotionReadinessValidationResult(
        profile_count=len(checked_profiles),
        atomic_number_span=(
            min(observed_atomic_numbers) if observed_atomic_numbers else 0,
            max(observed_atomic_numbers) if observed_atomic_numbers else 0,
        ),
        blocked_count=sum(
            1
            for profile in checked_profiles
            if profile.readiness_status == "promotion_blocked_missing_source_evidence"
        ),
        ready_count=sum(
            1 for profile in checked_profiles if profile.readiness_status == "promotion_ready"
        ),
        physical_property_evidence_count=sum(
            1 for profile in checked_profiles if profile.physical_property_evidence_available
        ),
        unresolved_physical_property_evidence_count=sum(
            1
            for profile in checked_profiles
            if profile.unresolved_physical_property_evidence_available
        ),
        f_block_profile_count=sum(
            1 for profile in checked_profiles if profile.f_block_profile_available
        ),
        invalid_profiles=invalid_profiles,
        validation_status=validation_status,
    )
