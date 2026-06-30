"""Purpose: Cs-Rn frontier and valence-signature overlay.

Project scope: derives bounded frontier signatures from Cs-Rn NIST configuration
evidence without promoting snapshot records to Level 1 seeds.
Dependencies: configuration evidence records and snapshot identity records.
Invariants: derived signatures close only frontier/valence readiness blockers;
oxidation states, behavior tags, and relation edges remain separate evidence.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any

from mcms.elements.configuration_evidence import find_configuration_evidence_record
from mcms.elements.promotion import CS_RN_PROMOTION_SYMBOLS
from mcms.elements.snapshot import get_snapshot_record

VALID_CS_RN_FRONTIER_MODELS = {
    "period_6_s_block",
    "lanthanide_4f_frontier",
    "period_6_transition_frontier",
    "period_6_p_block_f_d_core",
}
VALID_SHELL_STABILITY_STATES = {"open_shell", "half_filled_shell", "filled_shell"}
VALID_FRONTIER_VALENCE_STATUSES = {"frontier_valence_signature"}

_SUBSHELL_PATTERN = re.compile(r"(?P<n>[1-9])(?P<orbital>[spdf])\^(?P<count>[0-9]+)")


@dataclass(frozen=True)
class SubshellOccupancy:
    shell: int
    orbital: str
    occupancy: int

    @property
    def label(self) -> str:
        return f"{self.shell}{self.orbital}^{self.occupancy}"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FrontierValenceSignatureRecord:
    element_id: str
    symbol: str
    atomic_number: int
    neutral_configuration: str
    frontier_model: str
    frontier_signature: str
    outer_shell: str
    valence_shell_signature: str
    frontier_occupancy_count: int
    d_shell: str | None
    d_shell_stability: str | None
    f_shell: str | None
    f_shell_stability: str | None
    p_shell: str | None
    source_keys: tuple[str, ...]
    derivation_rule: str = "frontier signature derived from source-backed neutral configuration"
    evidence_status: str = "frontier_valence_signature"
    notes: tuple[str, ...] = (
        "Frontier and valence signatures are derived from configuration evidence.",
        "This overlay does not claim oxidation states, behavior tags, or relation edges.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        evidence = find_configuration_evidence_record(self.symbol)
        expected_element_id = f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}"
        if self.element_id != expected_element_id:
            errors.append("frontier element id must match snapshot element id.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("frontier atomic number must match snapshot element.")
        if self.symbol not in CS_RN_PROMOTION_SYMBOLS:
            errors.append("frontier symbol must be in the Cs-Rn span.")
        if self.neutral_configuration != evidence.neutral_configuration:
            errors.append("frontier source configuration must match configuration evidence.")
        if self.frontier_model not in VALID_CS_RN_FRONTIER_MODELS:
            errors.append("frontier model is unknown.")
        if not self.frontier_signature:
            errors.append("frontier signature is required.")
        if not self.outer_shell:
            errors.append("outer shell is required.")
        if not self.valence_shell_signature:
            errors.append("valence shell signature is required.")
        if self.frontier_occupancy_count <= 0:
            errors.append("frontier occupancy count must be positive.")
        if self.evidence_status not in VALID_FRONTIER_VALENCE_STATUSES:
            errors.append("frontier evidence status is unknown.")
        if "nist_electronic_configurations" not in self.source_keys:
            errors.append("NIST electronic-configuration source key is required.")
        if self.d_shell_stability is not None and (
            self.d_shell_stability not in VALID_SHELL_STABILITY_STATES
        ):
            errors.append("d-shell stability state is unknown.")
        if self.f_shell_stability is not None and (
            self.f_shell_stability not in VALID_SHELL_STABILITY_STATES
        ):
            errors.append("f-shell stability state is unknown.")
        if self.frontier_model == "period_6_s_block" and (
            self.d_shell is not None or self.f_shell is not None or self.p_shell is not None
        ):
            errors.append("period-6 s-block frontier must not expose d, f, or p shells.")
        if self.frontier_model == "lanthanide_4f_frontier" and not (
            self.f_shell or self.d_shell
        ):
            errors.append("lanthanide frontier requires f-shell or d-shell participation.")
        if self.frontier_model == "period_6_transition_frontier":
            if self.f_shell != "4f^14":
                errors.append("period-6 transition frontier must preserve filled 4f core.")
            if self.d_shell is None:
                errors.append("period-6 transition frontier requires 5d shell.")
        if self.frontier_model == "period_6_p_block_f_d_core":
            if self.f_shell != "4f^14":
                errors.append("period-6 p-block frontier must preserve filled 4f core.")
            if self.d_shell != "5d^10":
                errors.append("period-6 p-block frontier must preserve filled 5d core.")
            if self.p_shell is None:
                errors.append("period-6 p-block frontier requires 6p shell.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parse_subshells(configuration: str) -> tuple[SubshellOccupancy, ...]:
    return tuple(
        SubshellOccupancy(
            shell=int(match.group("n")),
            orbital=match.group("orbital"),
            occupancy=int(match.group("count")),
        )
        for match in _SUBSHELL_PATTERN.finditer(configuration)
    )


def _stability_for_shell(occupancy: int, capacity: int) -> str:
    if occupancy == capacity:
        return "filled_shell"
    if occupancy * 2 == capacity:
        return "half_filled_shell"
    return "open_shell"


def _latest_subshell(
    subshells: tuple[SubshellOccupancy, ...],
    orbital: str,
) -> SubshellOccupancy | None:
    matches = tuple(subshell for subshell in subshells if subshell.orbital == orbital)
    return matches[-1] if matches else None


def _frontier_model_for_atomic_number(atomic_number: int) -> str:
    if 55 <= atomic_number <= 56:
        return "period_6_s_block"
    if 57 <= atomic_number <= 71:
        return "lanthanide_4f_frontier"
    if 72 <= atomic_number <= 80:
        return "period_6_transition_frontier"
    if 81 <= atomic_number <= 86:
        return "period_6_p_block_f_d_core"
    raise KeyError(f"atomic number is outside Cs-Rn frontier span: {atomic_number}")


def _outer_shell_signature(subshells: tuple[SubshellOccupancy, ...]) -> str:
    outer_parts = tuple(
        subshell.label
        for subshell in subshells
        if subshell.shell == 6 and subshell.orbital in {"s", "p"}
    )
    return " ".join(outer_parts)


def _valence_shell_signature(
    frontier_model: str,
    subshells: tuple[SubshellOccupancy, ...],
) -> str:
    if frontier_model == "period_6_s_block":
        return _outer_shell_signature(subshells)
    if frontier_model == "period_6_p_block_f_d_core":
        return f"{_outer_shell_signature(subshells)} with filled 4f^14 5d^10 core"
    return " ".join(subshell.label for subshell in subshells)


def _frontier_signature(subshells: tuple[SubshellOccupancy, ...]) -> str:
    return " ".join(subshell.label for subshell in subshells)


def _build_frontier_valence_signature_record(
    identifier: str | int,
) -> FrontierValenceSignatureRecord:
    configuration_evidence = find_configuration_evidence_record(identifier)
    snapshot = get_snapshot_record(configuration_evidence.symbol)
    subshells = _parse_subshells(configuration_evidence.neutral_configuration)
    d_shell = _latest_subshell(subshells, "d")
    f_shell = _latest_subshell(subshells, "f")
    p_shell = _latest_subshell(subshells, "p")
    frontier_model = _frontier_model_for_atomic_number(snapshot.atomic_number)
    return FrontierValenceSignatureRecord(
        element_id=configuration_evidence.element_id,
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        neutral_configuration=configuration_evidence.neutral_configuration,
        frontier_model=frontier_model,
        frontier_signature=_frontier_signature(subshells),
        outer_shell=_outer_shell_signature(subshells),
        valence_shell_signature=_valence_shell_signature(frontier_model, subshells),
        frontier_occupancy_count=sum(subshell.occupancy for subshell in subshells),
        d_shell=d_shell.label if d_shell else None,
        d_shell_stability=(
            _stability_for_shell(d_shell.occupancy, 10) if d_shell else None
        ),
        f_shell=f_shell.label if f_shell else None,
        f_shell_stability=(
            _stability_for_shell(f_shell.occupancy, 14) if f_shell else None
        ),
        p_shell=p_shell.label if p_shell and p_shell.shell == 6 else None,
        source_keys=configuration_evidence.source_keys,
    )


@lru_cache(maxsize=1)
def list_frontier_valence_signature_records() -> tuple[FrontierValenceSignatureRecord, ...]:
    return tuple(
        _build_frontier_valence_signature_record(symbol)
        for symbol in CS_RN_PROMOTION_SYMBOLS
    )


def find_frontier_valence_signature_record(
    identifier: str | int,
) -> FrontierValenceSignatureRecord:
    identifier_text = str(identifier).strip()
    for record in list_frontier_valence_signature_records():
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.element_id
        ):
            return record
    raise KeyError(f"unknown frontier valence signature record: {identifier_text}")


def validate_frontier_valence_signature_records(
    records: tuple[FrontierValenceSignatureRecord, ...] | None = None,
) -> dict[str, Any]:
    checked_records = records if records is not None else list_frontier_valence_signature_records()
    invalid_records = tuple(record.element_id for record in checked_records if record.validate())
    observed_symbols = tuple(record.symbol for record in checked_records)
    full_span_expected = records is None or len(checked_records) == len(CS_RN_PROMOTION_SYMBOLS)
    validation_status = "frontier_valence_signature_records_validated"
    if invalid_records or (full_span_expected and observed_symbols != CS_RN_PROMOTION_SYMBOLS):
        validation_status = "frontier_valence_signature_records_rejected"
    return {
        "validation_status": validation_status,
        "record_count": len(checked_records),
        "s_block_count": sum(
            1 for record in checked_records if record.frontier_model == "period_6_s_block"
        ),
        "lanthanide_count": sum(
            1 for record in checked_records if record.frontier_model == "lanthanide_4f_frontier"
        ),
        "transition_count": sum(
            1
            for record in checked_records
            if record.frontier_model == "period_6_transition_frontier"
        ),
        "p_block_count": sum(
            1
            for record in checked_records
            if record.frontier_model == "period_6_p_block_f_d_core"
        ),
        "invalid_records": invalid_records,
        "source_keys": tuple(
            sorted({source_key for record in checked_records for source_key in record.source_keys})
        ),
    }
