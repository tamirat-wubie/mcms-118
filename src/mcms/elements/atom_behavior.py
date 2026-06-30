"""Purpose: additive atom behavior v2 contracts for MSPEE element records.

Project scope: derives atom-level behavior profiles from source-backed isotope
evidence, Level 1 element state, and measured matter profiles without mutating
seed records.
Dependencies: isotope evidence records, element instances, seed records, and
bounded matter-behavior profiles.
Invariants: proton count defines element identity; neutron count defines isotope
state; electron count and charge define ion state; quantum and force layers are
declared as bounded explanatory context, not simulation claims.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any

from mcms.elements.evidence import (
    IsotopeEvidenceRecord,
    find_isotope_evidence_records,
    list_isotope_evidence_records,
)
from mcms.elements.instances import build_isotope_instance
from mcms.elements.matter import build_matter_behavior_profile
from mcms.elements.seed import get_seed_element

VALID_ATOM_BEHAVIOR_STATUSES = {"atom_behavior_v2"}
ATOM_BEHAVIOR_NON_CLAIMS = (
    "profile does not solve electron wavefunctions",
    "profile does not predict reactions",
    "profile does not replace isotope-specific laboratory data",
    "profile does not claim complete quantum simulation",
)


def _charge_label(charge: int) -> str:
    if charge > 0:
        return f"plus-{charge}"
    if charge < 0:
        return f"minus-{abs(charge)}"
    return "neutral-0"


def _profile_id(atomic_number: int, symbol: str, mass_number: int, charge: int) -> str:
    return (
        f"MSPEE-Z{atomic_number:03d}-{symbol}-isotope-{mass_number}-"
        f"charge-{_charge_label(charge)}-atom-behavior-v2"
    )


def _single_isotope_evidence(
    identifier: str | int,
    mass_number: int,
) -> IsotopeEvidenceRecord:
    records = find_isotope_evidence_records(identifier, mass_number=mass_number)
    if len(records) != 1:
        raise KeyError(
            f"expected one isotope evidence record for {identifier} mass {mass_number}; "
            f"found {len(records)}"
        )
    return records[0]


def _nuclear_behavior_basis(record: IsotopeEvidenceRecord) -> tuple[str, ...]:
    basis = [
        "element_identity := proton_count",
        "isotope_identity := proton_count + neutron_count",
        f"mass_number={record.mass_number}",
        f"neutron_count={record.neutron_count}",
        f"isotope_evidence_status={record.evidence_status}",
    ]
    if record.evidence_status == "radioisotope_evidence":
        basis.extend(
            (
                f"half_life={record.half_life_value} {record.half_life_unit}",
                f"decay_mode={record.decay_mode}",
            )
        )
    if record.evidence_status == "stable_isotope_evidence":
        basis.append(f"isotopic_composition={record.isotopic_composition}")
    return tuple(basis)


def _electron_behavior_basis(
    neutral_configuration: str,
    atomic_number: int,
    charge: int,
    electron_count: int,
) -> tuple[str, ...]:
    return (
        "electron_count = atomic_number - charge",
        "electron changes define ion state, not element identity",
        f"neutral_electron_configuration={neutral_configuration}",
        f"neutral_electron_count={atomic_number}",
        f"charge={charge}",
        f"electron_count={electron_count}",
    )


def _force_layer_basis(record: IsotopeEvidenceRecord) -> tuple[str, ...]:
    weak_context = (
        f"weak_decay_context={record.decay_mode}"
        if record.evidence_status == "radioisotope_evidence"
        else "weak_decay_context=not_active_in_record"
    )
    return (
        "strong_nuclear_force_context=nucleus_binding",
        "electromagnetic_force_context=nucleus_electron_binding",
        weak_context,
        "gravity_context=negligible_at_atom_scale",
    )


@dataclass(frozen=True)
class AtomBehaviorProfile:
    profile_id: str
    isotope_id: str
    element_id: str
    symbol: str
    atomic_number: int
    proton_count: int
    neutron_count: int
    mass_number: int
    charge: int
    electron_count: int
    isotope_evidence_status: str
    neutral_electron_configuration: str
    quantum_state_basis: tuple[str, ...]
    nuclear_behavior_basis: tuple[str, ...]
    electron_behavior_basis: tuple[str, ...]
    force_layer_basis: tuple[str, ...]
    matter_behavior_tags: tuple[str, ...]
    source_keys: tuple[str, ...]
    profile_status: str = "atom_behavior_v2"
    derivation_trace: tuple[str, ...] = (
        "protons define element identity",
        "neutrons define isotope state",
        "electrons define charge and frontier behavior",
        "forces define bounded existence context",
    )
    non_claims: tuple[str, ...] = ATOM_BEHAVIOR_NON_CLAIMS

    def validate(self) -> list[str]:
        errors: list[str] = []
        element = get_seed_element(self.symbol)
        isotope_instance = build_isotope_instance(self.symbol, self.mass_number)
        matter_profile = build_matter_behavior_profile(self.symbol)
        expected_profile_id = _profile_id(
            self.atomic_number,
            self.symbol,
            self.mass_number,
            self.charge,
        )
        if self.profile_id != expected_profile_id:
            errors.append("atom behavior profile id does not match canonical id.")
        if self.isotope_id != isotope_instance.instance_id:
            errors.append("atom behavior isotope id must match isotope instance id.")
        if self.element_id != element.id:
            errors.append("atom behavior element id must match seed element id.")
        if self.atomic_number != element.identity.atomic_number:
            errors.append("atom behavior atomic number must match seed element.")
        if self.proton_count != self.atomic_number:
            errors.append("atom behavior must preserve proton-count identity.")
        if self.neutron_count != self.mass_number - self.atomic_number:
            errors.append("atom behavior neutron count must equal mass_number - atomic_number.")
        if self.mass_number != self.proton_count + self.neutron_count:
            errors.append("atom behavior mass number must equal protons plus neutrons.")
        if self.electron_count != self.atomic_number - self.charge:
            errors.append("atom behavior electron count must equal atomic_number - charge.")
        if self.electron_count < 0:
            errors.append("atom behavior electron count cannot be negative.")
        if self.neutral_electron_configuration != element.state.neutral_electron_configuration:
            errors.append("atom behavior neutral configuration must match seed element.")
        if self.isotope_evidence_status not in {
            "stable_isotope_evidence",
            "radioisotope_evidence",
        }:
            errors.append("atom behavior isotope evidence status is unknown.")
        if not self.quantum_state_basis:
            errors.append("atom behavior requires quantum-state basis.")
        if not self.nuclear_behavior_basis:
            errors.append("atom behavior requires nuclear behavior basis.")
        if not self.electron_behavior_basis:
            errors.append("atom behavior requires electron behavior basis.")
        if not self.force_layer_basis:
            errors.append("atom behavior requires force-layer basis.")
        if tuple(matter_profile.inferred_behavior_tags) != self.matter_behavior_tags:
            errors.append("atom behavior matter tags must match matter profile.")
        if not set(matter_profile.source_keys) <= set(self.source_keys):
            errors.append("atom behavior must preserve matter-profile source keys.")
        if self.profile_status not in VALID_ATOM_BEHAVIOR_STATUSES:
            errors.append("atom behavior profile status is unknown.")
        if self.non_claims != ATOM_BEHAVIOR_NON_CLAIMS:
            errors.append("atom behavior non-claims must match v2 boundary.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_atom_behavior_profile(
    identifier: str | int,
    mass_number: int,
    *,
    charge: int = 0,
) -> AtomBehaviorProfile:
    isotope_evidence = _single_isotope_evidence(identifier, mass_number)
    element = get_seed_element(isotope_evidence.symbol)
    isotope_instance = build_isotope_instance(isotope_evidence.symbol, mass_number)
    matter_profile = build_matter_behavior_profile(isotope_evidence.symbol)
    electron_count = element.identity.atomic_number - charge
    profile = AtomBehaviorProfile(
        profile_id=_profile_id(
            element.identity.atomic_number,
            element.identity.symbol,
            mass_number,
            charge,
        ),
        isotope_id=isotope_instance.instance_id,
        element_id=element.id,
        symbol=element.identity.symbol,
        atomic_number=element.identity.atomic_number,
        proton_count=element.identity.proton_count,
        neutron_count=isotope_instance.neutron_count,
        mass_number=mass_number,
        charge=charge,
        electron_count=electron_count,
        isotope_evidence_status=isotope_evidence.evidence_status,
        neutral_electron_configuration=element.state.neutral_electron_configuration,
        quantum_state_basis=(
            "electron_cloud represented by source-backed configuration",
            "energy_state=neutral_ground_configuration_context",
            "exact wavefunction is outside current claim boundary",
        ),
        nuclear_behavior_basis=_nuclear_behavior_basis(isotope_evidence),
        electron_behavior_basis=_electron_behavior_basis(
            element.state.neutral_electron_configuration,
            element.identity.atomic_number,
            charge,
            electron_count,
        ),
        force_layer_basis=_force_layer_basis(isotope_evidence),
        matter_behavior_tags=matter_profile.inferred_behavior_tags,
        source_keys=tuple(
            sorted(set(isotope_evidence.source_keys + matter_profile.source_keys))
        ),
    )
    validation_errors = profile.validate()
    if validation_errors:
        raise ValueError("; ".join(validation_errors))
    return profile


@lru_cache(maxsize=1)
def list_atom_behavior_profiles() -> tuple[AtomBehaviorProfile, ...]:
    return tuple(
        build_atom_behavior_profile(record.symbol, record.mass_number)
        for record in list_isotope_evidence_records()
    )


def find_atom_behavior_profile(
    identifier: str | int,
    mass_number: int | None = None,
    *,
    charge: int = 0,
) -> AtomBehaviorProfile:
    if mass_number is not None:
        return build_atom_behavior_profile(identifier, mass_number, charge=charge)
    identifier_text = str(identifier).strip()
    matches = tuple(
        profile
        for profile in list_atom_behavior_profiles()
        if identifier_text.upper()
        in {
            profile.profile_id.upper(),
            profile.isotope_id.upper(),
            profile.symbol.upper(),
            str(profile.atomic_number),
        }
    )
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise KeyError(
            f"atom behavior lookup is ambiguous for {identifier_text}; provide mass_number"
        )
    raise KeyError(f"unknown atom behavior profile: {identifier_text}")


def validate_atom_behavior_profiles(
    profiles: tuple[AtomBehaviorProfile, ...] | None = None,
) -> dict[str, Any]:
    checked_profiles = profiles if profiles is not None else list_atom_behavior_profiles()
    invalid_profiles = tuple(
        profile.profile_id for profile in checked_profiles if profile.validate()
    )
    return {
        "validation_status": (
            "atom_behavior_profiles_validated"
            if not invalid_profiles
            else "atom_behavior_profiles_rejected"
        ),
        "profile_count": len(checked_profiles),
        "neutral_profile_count": sum(
            1 for profile in checked_profiles if profile.charge == 0
        ),
        "stable_isotope_profile_count": sum(
            1
            for profile in checked_profiles
            if profile.isotope_evidence_status == "stable_isotope_evidence"
        ),
        "radioisotope_profile_count": sum(
            1
            for profile in checked_profiles
            if profile.isotope_evidence_status == "radioisotope_evidence"
        ),
        "invalid_profiles": invalid_profiles,
        "source_keys": tuple(
            sorted({source_key for profile in checked_profiles for source_key in profile.source_keys})
        ),
    }
