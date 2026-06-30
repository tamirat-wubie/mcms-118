"""Purpose: compact period-5 Level 2 chemistry profiles for Rb through Xe.

Project scope: exposes PubChem chemistry fields as a small projection over promoted
Level 1 seed records and existing snapshot identities.
Dependencies: local snapshot records, shared element validation constants, and dataclasses.
Invariants: profiles are source-backed chemistry projections; full electron-state
seed records remain the authority for Level 1 identity/state payloads.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.model import (
    ELECTRONEGATIVITY_MAX,
    ELECTRONEGATIVITY_MIN,
    FIRST_IONIZATION_ENERGY_MAX_EV,
    FIRST_IONIZATION_ENERGY_MIN_EV,
    OXIDATION_STATE_MAX,
    OXIDATION_STATE_MIN,
    VALID_BOND_TENDENCY_TAGS,
    SourceReference,
)
from mcms.elements.snapshot import ElementSourceSnapshotRecord, get_snapshot_record

LEVEL_2_SNAPSHOT_SOURCE_REFERENCE = SourceReference(
    key="pubchem_periodic_table_properties",
    authority="PubChem/NCBI",
    title="PubChem Periodic Table of Elements CSV",
    url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV",
    version="source page observed 2026-06-28",
)

PERIOD_5_LEVEL_2_SYMBOLS = (
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
)

_BOND_TENDENCY_TAGS_BY_PUBCHEM_GROUP_BLOCK: dict[str, tuple[str, ...]] = {
    "Alkali metal": ("metallic_bonding", "ionic_bonding"),
    "Alkaline earth metal": ("metallic_bonding", "ionic_bonding"),
    "Halogen": ("covalent_bonding", "ionic_bonding", "molecular_covalent"),
    "Metalloid": ("covalent_bonding", "network_covalent"),
    "Noble gas": ("noble_gas_low_reactivity",),
    "Post-transition metal": ("metallic_bonding", "covalent_bonding"),
    "Transition metal": ("metallic_bonding", "coordination_complex"),
}

_PERIOD_5_PUBCHEM_CHEMISTRY_BY_SYMBOL: dict[str, dict[str, Any]] = {
    "Rb": {
        "oxidation_states": (1,),
        "electronegativity_value": 0.82,
        "first_ionization_energy_ev": 4.177,
        "group_block": "Alkali metal",
    },
    "Sr": {
        "oxidation_states": (2,),
        "electronegativity_value": 0.95,
        "first_ionization_energy_ev": 5.695,
        "group_block": "Alkaline earth metal",
    },
    "Y": {
        "oxidation_states": (3,),
        "electronegativity_value": 1.22,
        "first_ionization_energy_ev": 6.217,
        "group_block": "Transition metal",
    },
    "Zr": {
        "oxidation_states": (4,),
        "electronegativity_value": 1.33,
        "first_ionization_energy_ev": 6.634,
        "group_block": "Transition metal",
    },
    "Nb": {
        "oxidation_states": (5, 3),
        "electronegativity_value": 1.6,
        "first_ionization_energy_ev": 6.759,
        "group_block": "Transition metal",
    },
    "Mo": {
        "oxidation_states": (6,),
        "electronegativity_value": 2.16,
        "first_ionization_energy_ev": 7.092,
        "group_block": "Transition metal",
    },
    "Tc": {
        "oxidation_states": (7, 6, 4),
        "electronegativity_value": 1.9,
        "first_ionization_energy_ev": 7.28,
        "group_block": "Transition metal",
    },
    "Ru": {
        "oxidation_states": (3,),
        "electronegativity_value": 2.2,
        "first_ionization_energy_ev": 7.361,
        "group_block": "Transition metal",
    },
    "Rh": {
        "oxidation_states": (3,),
        "electronegativity_value": 2.28,
        "first_ionization_energy_ev": 7.459,
        "group_block": "Transition metal",
    },
    "Pd": {
        "oxidation_states": (3, 2),
        "electronegativity_value": 2.2,
        "first_ionization_energy_ev": 8.337,
        "group_block": "Transition metal",
    },
    "Ag": {
        "oxidation_states": (1,),
        "electronegativity_value": 1.93,
        "first_ionization_energy_ev": 7.576,
        "group_block": "Transition metal",
    },
    "Cd": {
        "oxidation_states": (2,),
        "electronegativity_value": 1.69,
        "first_ionization_energy_ev": 8.994,
        "group_block": "Transition metal",
    },
    "In": {
        "oxidation_states": (3,),
        "electronegativity_value": 1.78,
        "first_ionization_energy_ev": 5.786,
        "group_block": "Post-transition metal",
    },
    "Sn": {
        "oxidation_states": (4, 2),
        "electronegativity_value": 1.96,
        "first_ionization_energy_ev": 7.344,
        "group_block": "Post-transition metal",
    },
    "Sb": {
        "oxidation_states": (5, 3, -3),
        "electronegativity_value": 2.05,
        "first_ionization_energy_ev": 8.64,
        "group_block": "Metalloid",
    },
    "Te": {
        "oxidation_states": (6, 4, -2),
        "electronegativity_value": 2.1,
        "first_ionization_energy_ev": 9.01,
        "group_block": "Metalloid",
    },
    "I": {
        "oxidation_states": (7, 5, 1, -1),
        "electronegativity_value": 2.66,
        "first_ionization_energy_ev": 10.451,
        "group_block": "Halogen",
    },
    "Xe": {
        "oxidation_states": (0,),
        "electronegativity_value": 2.6,
        "first_ionization_energy_ev": 12.13,
        "group_block": "Noble gas",
    },
}


@dataclass(frozen=True)
class SnapshotLevel2ChemistryProfile:
    atomic_number: int
    symbol: str
    name: str
    period: int
    group: int | None
    block: str
    source_key: str
    source_scope: str
    oxidation_states: tuple[int, ...]
    electronegativity_scale: str | None
    electronegativity_value: float | None
    first_ionization_energy_ev: float
    pubchem_group_block: str
    bond_tendency_tags: tuple[str, ...]
    promotion_status: str
    notes: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.source_key != LEVEL_2_SNAPSHOT_SOURCE_REFERENCE.key:
            errors.append("snapshot Level 2 chemistry source key is unknown.")
        if self.source_scope != "snapshot_level_2_period_5":
            errors.append("snapshot Level 2 chemistry source scope is unknown.")
        if self.symbol not in PERIOD_5_LEVEL_2_SYMBOLS:
            errors.append("snapshot Level 2 profile is outside the period-5 expansion set.")
        if self.period != 5:
            errors.append("snapshot Level 2 period-5 profile must reference period 5.")
        if not self.oxidation_states:
            errors.append("snapshot Level 2 profile requires oxidation states.")
        if len(set(self.oxidation_states)) != len(self.oxidation_states):
            errors.append("oxidation states must not contain duplicates.")
        for oxidation_state in self.oxidation_states:
            if oxidation_state < OXIDATION_STATE_MIN or oxidation_state > OXIDATION_STATE_MAX:
                errors.append(
                    f"oxidation states must be in [{OXIDATION_STATE_MIN}, {OXIDATION_STATE_MAX}]."
                )
        if self.electronegativity_scale != "pauling":
            errors.append("period-5 PubChem profiles require Pauling electronegativity scale.")
        if (
            self.electronegativity_value is None
            or self.electronegativity_value < ELECTRONEGATIVITY_MIN
            or self.electronegativity_value > ELECTRONEGATIVITY_MAX
        ):
            errors.append(
                "electronegativity value must be present and in "
                f"[{ELECTRONEGATIVITY_MIN}, {ELECTRONEGATIVITY_MAX}]."
            )
        if (
            self.first_ionization_energy_ev < FIRST_IONIZATION_ENERGY_MIN_EV
            or self.first_ionization_energy_ev > FIRST_IONIZATION_ENERGY_MAX_EV
        ):
            errors.append(
                "first ionization energy value must be in "
                f"[{FIRST_IONIZATION_ENERGY_MIN_EV}, {FIRST_IONIZATION_ENERGY_MAX_EV}] eV."
            )
        if not self.bond_tendency_tags:
            errors.append("snapshot Level 2 profile requires bond tendency tags.")
        if len(set(self.bond_tendency_tags)) != len(self.bond_tendency_tags):
            errors.append("bond tendency tags must not contain duplicates.")
        for tag in self.bond_tendency_tags:
            if tag not in VALID_BOND_TENDENCY_TAGS:
                errors.append("bond tendency tag is unknown.")
        expected_tags = _BOND_TENDENCY_TAGS_BY_PUBCHEM_GROUP_BLOCK.get(
            self.pubchem_group_block,
            (),
        )
        if self.bond_tendency_tags != expected_tags:
            errors.append("bond tendency tags do not match PubChem GroupBlock classification.")
        if self.promotion_status != "snapshot_level_2_chemistry_profile":
            errors.append("snapshot Level 2 promotion status is unknown.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["oxidation_states"] = list(self.oxidation_states)
        payload["bond_tendency_tags"] = list(self.bond_tendency_tags)
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class SnapshotLevel2ChemistryValidationResult:
    profile_count: int
    expected_profile_count: int
    atomic_number_span: tuple[int, int] | None
    invalid_profiles: tuple[str, ...]
    source_key: str
    validation_status: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["atomic_number_span"] = (
            list(self.atomic_number_span) if self.atomic_number_span is not None else None
        )
        payload["invalid_profiles"] = list(self.invalid_profiles)
        return payload


def _period_5_profile_from_snapshot(
    record: ElementSourceSnapshotRecord,
) -> SnapshotLevel2ChemistryProfile:
    chemistry = _PERIOD_5_PUBCHEM_CHEMISTRY_BY_SYMBOL[record.symbol]
    group_block = chemistry["group_block"]
    return SnapshotLevel2ChemistryProfile(
        atomic_number=record.atomic_number,
        symbol=record.symbol,
        name=record.name,
        period=record.period,
        group=record.group,
        block=record.block,
        source_key=LEVEL_2_SNAPSHOT_SOURCE_REFERENCE.key,
        source_scope="snapshot_level_2_period_5",
        oxidation_states=chemistry["oxidation_states"],
        electronegativity_scale="pauling",
        electronegativity_value=chemistry["electronegativity_value"],
        first_ionization_energy_ev=chemistry["first_ionization_energy_ev"],
        pubchem_group_block=group_block,
        bond_tendency_tags=_BOND_TENDENCY_TAGS_BY_PUBCHEM_GROUP_BLOCK[group_block],
        promotion_status="snapshot_level_2_chemistry_profile",
        notes=(
            "profile is a compact chemistry projection over the promoted seed record",
            "full Level 1 seed payload remains the authority for electron-state records",
        ),
    )


def list_period_5_level_2_profiles() -> tuple[SnapshotLevel2ChemistryProfile, ...]:
    return tuple(
        _period_5_profile_from_snapshot(get_snapshot_record(symbol))
        for symbol in PERIOD_5_LEVEL_2_SYMBOLS
    )


def get_period_5_level_2_profile(
    identifier: str | int,
) -> SnapshotLevel2ChemistryProfile:
    record = get_snapshot_record(identifier)
    if record.symbol not in PERIOD_5_LEVEL_2_SYMBOLS:
        raise KeyError(f"element is not in the period-5 Level 2 snapshot set: {record.symbol}")
    return _period_5_profile_from_snapshot(record)


def validate_period_5_level_2_profiles(
    profiles: tuple[SnapshotLevel2ChemistryProfile, ...] | None = None,
) -> SnapshotLevel2ChemistryValidationResult:
    checked_profiles = profiles if profiles is not None else list_period_5_level_2_profiles()
    invalid_profiles = tuple(
        profile.symbol for profile in checked_profiles if profile.validate()
    )
    observed_symbols = tuple(profile.symbol for profile in checked_profiles)
    observed_atomic_numbers = tuple(profile.atomic_number for profile in checked_profiles)
    expected_atomic_numbers = tuple(range(37, 55))
    validation_status = "period_5_level_2_snapshot_profiles_validated"
    if (
        invalid_profiles
        or observed_symbols != PERIOD_5_LEVEL_2_SYMBOLS
        or observed_atomic_numbers != expected_atomic_numbers
    ):
        validation_status = "period_5_level_2_snapshot_profiles_rejected"
    atomic_number_span = (
        (min(observed_atomic_numbers), max(observed_atomic_numbers))
        if observed_atomic_numbers
        else None
    )
    return SnapshotLevel2ChemistryValidationResult(
        profile_count=len(checked_profiles),
        expected_profile_count=len(PERIOD_5_LEVEL_2_SYMBOLS),
        atomic_number_span=atomic_number_span,
        invalid_profiles=invalid_profiles,
        source_key=LEVEL_2_SNAPSHOT_SOURCE_REFERENCE.key,
        validation_status=validation_status,
    )
