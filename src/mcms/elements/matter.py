"""Purpose: bounded MSPEE matter-behavior profiles.

Project scope: derives first-pass matter profiles from element identity, symbolic
state, and measured physical-property evidence without claiming reaction prediction.
Dependencies: element seed records and physical-property evidence records.
Invariants: measured evidence, symbolic inference, and non-claims remain separate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from mcms.elements.evidence import (
    PhysicalPropertyEvidenceRecord,
    find_physical_property_evidence_record,
    list_physical_property_evidence_records,
)
from mcms.elements.seed import get_seed_element

MATTER_BEHAVIOR_CONTEXT = "standard_conditions_symbolic_baseline"
VALID_MATTER_PROFILE_STATUS = {"matter_behavior_profile_v1"}


@dataclass(frozen=True)
class MatterBehaviorProfile:
    element_id: str
    symbol: str
    atomic_number: int
    environment_context: str
    standard_state: str
    measured_evidence_inputs: tuple[str, ...]
    symbolic_state_inputs: tuple[str, ...]
    inferred_behavior_tags: tuple[str, ...]
    source_keys: tuple[str, ...]
    profile_status: str = "matter_behavior_profile_v1"
    non_claims: tuple[str, ...] = (
        "profile does not predict reactions",
        "profile does not model compounds",
        "profile does not replace measured condition-specific data",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        element = get_seed_element(self.symbol)
        physical_evidence = find_physical_property_evidence_record(self.symbol)
        if self.element_id != element.id:
            errors.append("matter profile element id must match seed element id.")
        if self.atomic_number != element.identity.atomic_number:
            errors.append("matter profile atomic number must match seed element.")
        if self.environment_context != MATTER_BEHAVIOR_CONTEXT:
            errors.append("matter profile environment context is unknown.")
        if self.standard_state != physical_evidence.standard_state:
            errors.append("matter profile standard state must match measured evidence.")
        if not self.measured_evidence_inputs:
            errors.append("matter profile requires measured evidence inputs.")
        if not self.symbolic_state_inputs:
            errors.append("matter profile requires symbolic state inputs.")
        if not self.inferred_behavior_tags:
            errors.append("matter profile requires inferred behavior tags.")
        if not set(physical_evidence.source_keys) <= set(self.source_keys):
            errors.append("matter profile must preserve physical evidence source keys.")
        if self.profile_status not in VALID_MATTER_PROFILE_STATUS:
            errors.append("matter profile status is unknown.")
        if not self.non_claims:
            errors.append("matter profile must declare non-claims.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


def _state_tag(physical_evidence: PhysicalPropertyEvidenceRecord) -> str:
    return f"standard_state_{physical_evidence.standard_state.lower()}"


def _thermal_tags(physical_evidence: PhysicalPropertyEvidenceRecord) -> tuple[str, ...]:
    tags: list[str] = []
    if physical_evidence.boiling_point_k < 400:
        tags.append("low_boiling_boundary")
    if physical_evidence.melting_point_k > 1000:
        tags.append("high_melting_boundary")
    if physical_evidence.boiling_point_k > 2500:
        tags.append("high_boiling_boundary")
    return tuple(tags)


def _density_tags(physical_evidence: PhysicalPropertyEvidenceRecord) -> tuple[str, ...]:
    if physical_evidence.density_value < 0.01:
        return ("low_density_boundary",)
    if physical_evidence.density_value >= 7.0:
        return ("high_density_boundary",)
    return ("moderate_density_boundary",)


def build_matter_behavior_profile(identifier: str | int) -> MatterBehaviorProfile:
    physical_evidence = find_physical_property_evidence_record(identifier)
    element = get_seed_element(physical_evidence.symbol)
    measured_evidence_inputs = (
        f"standard_state={physical_evidence.standard_state}",
        f"melting_point_k={physical_evidence.melting_point_k}",
        f"boiling_point_k={physical_evidence.boiling_point_k}",
        f"density={physical_evidence.density_value} {physical_evidence.density_unit}",
    )
    symbolic_state_inputs = (
        f"block={element.state.block}",
        f"group={element.state.group}",
        f"period={element.state.period}",
        f"valence_shell={element.state.valence_shell}",
    ) + element.state.behavior_tags
    inferred_behavior_tags = (
        _state_tag(physical_evidence),
    ) + _thermal_tags(physical_evidence) + _density_tags(physical_evidence)
    return MatterBehaviorProfile(
        element_id=element.id,
        symbol=element.identity.symbol,
        atomic_number=element.identity.atomic_number,
        environment_context=MATTER_BEHAVIOR_CONTEXT,
        standard_state=physical_evidence.standard_state,
        measured_evidence_inputs=measured_evidence_inputs,
        symbolic_state_inputs=symbolic_state_inputs,
        inferred_behavior_tags=inferred_behavior_tags,
        source_keys=physical_evidence.source_keys,
    )


def list_matter_behavior_profiles() -> tuple[MatterBehaviorProfile, ...]:
    profiles: list[MatterBehaviorProfile] = []
    for record in list_physical_property_evidence_records():
        try:
            get_seed_element(record.symbol)
        except KeyError:
            continue
        profiles.append(build_matter_behavior_profile(record.symbol))
    return tuple(profiles)


def validate_matter_behavior_profiles(
    profiles: tuple[MatterBehaviorProfile, ...] | None = None,
) -> dict:
    checked_profiles = profiles if profiles is not None else list_matter_behavior_profiles()
    invalid_profiles = tuple(
        profile.element_id for profile in checked_profiles if profile.validate()
    )
    return {
        "validation_status": (
            "matter_behavior_profiles_validated"
            if not invalid_profiles
            else "matter_behavior_profiles_rejected"
        ),
        "profile_count": len(checked_profiles),
        "standard_states": tuple(
            sorted({profile.standard_state for profile in checked_profiles})
        ),
        "invalid_profiles": invalid_profiles,
        "source_keys": tuple(
            sorted({source_key for profile in checked_profiles for source_key in profile.source_keys})
        ),
    }
