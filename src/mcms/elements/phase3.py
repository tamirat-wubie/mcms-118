"""Purpose: Phase 3 f-block expansion profiles for lanthanides and actinides.

Project scope: adds bounded f-orbital, nuclear-state, uncertainty, and relativistic
flags over the existing 118-element snapshot.
Dependencies: local snapshot records and dataclass serialization.
Invariants: profiles do not invent isotope half-lives or exact f-orbital occupancies.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.snapshot import ElementSourceSnapshotRecord, get_snapshot_record

VALID_F_BLOCK_SERIES = {"lanthanide", "actinide"}
VALID_F_SHELL_FAMILIES = {"4f", "5f"}

LANTHANIDE_SYMBOLS = (
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
)
ACTINIDE_SYMBOLS = (
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
)
RADIOACTIVE_F_BLOCK_SYMBOLS = frozenset(("Pm",) + ACTINIDE_SYMBOLS)


@dataclass(frozen=True)
class FBlockExpansionProfile:
    atomic_number: int
    symbol: str
    name: str
    series: str
    f_shell_family: str
    period: int
    group: int | None
    block: str
    standard_atomic_weight_status: str
    lanthanide_contraction_relevance: bool
    radioactive_decay_relevance: bool
    actinide_instability_relevance: bool
    nuclear_state_extension_required: bool
    heavy_element_uncertainty: bool
    relativistic_effect_relevance: bool
    notes: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.series not in VALID_F_BLOCK_SERIES:
            errors.append("f-block series is unknown.")
        if self.f_shell_family not in VALID_F_SHELL_FAMILIES:
            errors.append("f-shell family is unknown.")
        if self.block != "f":
            errors.append("Phase 3 profile must reference an f-block snapshot row.")
        if self.group is not None:
            errors.append("f-block profile keeps group unset to avoid forced group assignment.")
        if self.series == "lanthanide" and self.f_shell_family != "4f":
            errors.append("lanthanide profile must use 4f shell family.")
        if self.series == "actinide" and self.f_shell_family != "5f":
            errors.append("actinide profile must use 5f shell family.")
        if self.actinide_instability_relevance and self.series != "actinide":
            errors.append("actinide instability flag is only valid for actinide profiles.")
        if self.radioactive_decay_relevance and not self.nuclear_state_extension_required:
            errors.append("radioactive profiles require nuclear-state extension.")
        if self.heavy_element_uncertainty and not self.relativistic_effect_relevance:
            errors.append("heavy-element uncertainty requires relativistic-effect relevance flag.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FBlockExpansionValidationResult:
    profile_count: int
    lanthanide_count: int
    actinide_count: int
    radioactive_relevance_count: int
    invalid_profiles: tuple[str, ...]
    validation_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _series_for_symbol(symbol: str) -> str:
    if symbol in LANTHANIDE_SYMBOLS:
        return "lanthanide"
    if symbol in ACTINIDE_SYMBOLS:
        return "actinide"
    raise KeyError(f"element is not in the Phase 3 f-block expansion set: {symbol}")


def _profile_from_snapshot(record: ElementSourceSnapshotRecord) -> FBlockExpansionProfile:
    series = _series_for_symbol(record.symbol)
    radioactive_decay_relevance = record.symbol in RADIOACTIVE_F_BLOCK_SYMBOLS
    atomic_weight_unavailable = record.atomic_weight_model.model_type == "unavailable"
    actinide = series == "actinide"
    notes = (
        "f-orbital behavior is represented as a series-level frontier flag.",
        "exact isotope half-lives and f-orbital occupancies require later source-backed data.",
    )
    if series == "lanthanide":
        notes += ("lanthanide contraction is relevant across the 4f series.",)
    else:
        notes += ("actinide profiles require nuclear-state uncertainty handling.",)
    if radioactive_decay_relevance:
        notes += ("radioactive decay is flagged without assigning isotope-specific half-life.",)
    return FBlockExpansionProfile(
        atomic_number=record.atomic_number,
        symbol=record.symbol,
        name=record.name,
        series=series,
        f_shell_family="4f" if series == "lanthanide" else "5f",
        period=record.period,
        group=record.group,
        block=record.block,
        standard_atomic_weight_status=record.atomic_weight_model.model_type,
        lanthanide_contraction_relevance=series == "lanthanide",
        radioactive_decay_relevance=radioactive_decay_relevance,
        actinide_instability_relevance=actinide,
        nuclear_state_extension_required=radioactive_decay_relevance or actinide,
        heavy_element_uncertainty=actinide or atomic_weight_unavailable,
        relativistic_effect_relevance=True,
        notes=notes,
    )


def list_f_block_expansion_profiles() -> tuple[FBlockExpansionProfile, ...]:
    return tuple(
        _profile_from_snapshot(get_snapshot_record(symbol))
        for symbol in LANTHANIDE_SYMBOLS + ACTINIDE_SYMBOLS
    )


def get_f_block_expansion_profile(identifier: str | int) -> FBlockExpansionProfile:
    record = get_snapshot_record(identifier)
    if record.symbol not in set(LANTHANIDE_SYMBOLS + ACTINIDE_SYMBOLS):
        raise KeyError(f"element is not in the Phase 3 f-block expansion set: {record.symbol}")
    return _profile_from_snapshot(record)


def validate_f_block_expansion_profiles(
    profiles: tuple[FBlockExpansionProfile, ...] | None = None,
) -> FBlockExpansionValidationResult:
    checked_profiles = profiles if profiles is not None else list_f_block_expansion_profiles()
    invalid_profiles = tuple(
        profile.symbol for profile in checked_profiles if profile.validate()
    )
    observed_symbols = tuple(profile.symbol for profile in checked_profiles)
    expected_symbols = LANTHANIDE_SYMBOLS + ACTINIDE_SYMBOLS
    validation_status = "f_block_expansion_profiles_validated"
    if invalid_profiles or observed_symbols != expected_symbols:
        validation_status = "f_block_expansion_profiles_rejected"
    return FBlockExpansionValidationResult(
        profile_count=len(checked_profiles),
        lanthanide_count=sum(1 for profile in checked_profiles if profile.series == "lanthanide"),
        actinide_count=sum(1 for profile in checked_profiles if profile.series == "actinide"),
        radioactive_relevance_count=sum(
            1 for profile in checked_profiles if profile.radioactive_decay_relevance
        ),
        invalid_profiles=invalid_profiles,
        validation_status=validation_status,
    )
