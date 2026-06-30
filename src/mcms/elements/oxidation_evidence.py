"""Purpose: PubChem oxidation-state evidence overlay for Cs-Rn.

Project scope: records sourced oxidation-state sets for snapshot elements 55-86
without promoting them to full Level 1 seed records.
Dependencies: local snapshot records and shared oxidation-state constraints.
Invariants: oxidation states are evidence records; behavior tags and relation
edges remain separate promotion blockers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any

from mcms.elements.model import (
    OXIDATION_STATE_MAX,
    OXIDATION_STATE_MIN,
    SourceReference,
)
from mcms.elements.promotion import CS_RN_PROMOTION_SYMBOLS
from mcms.elements.snapshot import get_snapshot_record

OXIDATION_STATE_EVIDENCE_SOURCE_REFERENCES = (
    SourceReference(
        key="pubchem_periodic_table_properties",
        authority="PubChem/NCBI",
        title="PubChem Periodic Table of Elements CSV",
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV",
        version="source page observed 2026-06-29",
    ),
)

VALID_OXIDATION_STATE_EVIDENCE_STATUSES = {"oxidation_state_evidence"}

_OXIDATION_STATE_EVIDENCE_ROWS: tuple[tuple[str, tuple[int, ...], str], ...] = (
    ("Cs", (1,), "Alkali metal"),
    ("Ba", (2,), "Alkaline earth metal"),
    ("La", (3,), "Lanthanide"),
    ("Ce", (4, 3), "Lanthanide"),
    ("Pr", (3,), "Lanthanide"),
    ("Nd", (3,), "Lanthanide"),
    ("Pm", (3,), "Lanthanide"),
    ("Sm", (3, 2), "Lanthanide"),
    ("Eu", (3, 2), "Lanthanide"),
    ("Gd", (3,), "Lanthanide"),
    ("Tb", (3,), "Lanthanide"),
    ("Dy", (3,), "Lanthanide"),
    ("Ho", (3,), "Lanthanide"),
    ("Er", (3,), "Lanthanide"),
    ("Tm", (3,), "Lanthanide"),
    ("Yb", (3, 2), "Lanthanide"),
    ("Lu", (3,), "Lanthanide"),
    ("Hf", (4,), "Transition metal"),
    ("Ta", (5,), "Transition metal"),
    ("W", (6,), "Transition metal"),
    ("Re", (7, 6, 4), "Transition metal"),
    ("Os", (4, 3), "Transition metal"),
    ("Ir", (4, 3), "Transition metal"),
    ("Pt", (4, 2), "Transition metal"),
    ("Au", (3, 1), "Transition metal"),
    ("Hg", (2, 1), "Transition metal"),
    ("Tl", (3, 1), "Post-transition metal"),
    ("Pb", (4, 2), "Post-transition metal"),
    ("Bi", (5, 3), "Post-transition metal"),
    ("Po", (4, 2), "Metalloid"),
    ("At", (7, 5, 3, 1, -1), "Halogen"),
    ("Rn", (0,), "Noble gas"),
)


@dataclass(frozen=True)
class OxidationStateEvidenceRecord:
    element_id: str
    symbol: str
    atomic_number: int
    oxidation_states: tuple[int, ...]
    pubchem_group_block: str
    source_keys: tuple[str, ...]
    evidence_status: str = "oxidation_state_evidence"
    notes: tuple[str, ...] = (
        "Oxidation-state evidence is sourced from PubChem and remains separate from behavior tags.",
        "Presence of a listed oxidation state is not a guarantee for every compound or condition.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        expected_element_id = f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}"
        if self.element_id != expected_element_id:
            errors.append("oxidation evidence element id must match snapshot element id.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("oxidation evidence atomic number must match snapshot element.")
        if self.symbol not in CS_RN_PROMOTION_SYMBOLS:
            errors.append("oxidation evidence symbol must be in the Cs-Rn span.")
        if not self.oxidation_states:
            errors.append("oxidation evidence requires at least one oxidation state.")
        if len(set(self.oxidation_states)) != len(self.oxidation_states):
            errors.append("oxidation states must not contain duplicates.")
        for oxidation_state in self.oxidation_states:
            if oxidation_state < OXIDATION_STATE_MIN or oxidation_state > OXIDATION_STATE_MAX:
                errors.append(
                    f"oxidation states must be in [{OXIDATION_STATE_MIN}, {OXIDATION_STATE_MAX}]."
                )
        if not self.pubchem_group_block:
            errors.append("PubChem GroupBlock value is required.")
        if "pubchem_periodic_table_properties" not in self.source_keys:
            errors.append("PubChem periodic-table source key is required.")
        if self.evidence_status not in VALID_OXIDATION_STATE_EVIDENCE_STATUSES:
            errors.append("oxidation evidence status is unknown.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["oxidation_states"] = list(self.oxidation_states)
        payload["notes"] = list(self.notes)
        return payload


def _build_oxidation_state_evidence_record(
    row: tuple[str, tuple[int, ...], str],
) -> OxidationStateEvidenceRecord:
    symbol, oxidation_states, pubchem_group_block = row
    snapshot = get_snapshot_record(symbol)
    return OxidationStateEvidenceRecord(
        element_id=f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}",
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        oxidation_states=oxidation_states,
        pubchem_group_block=pubchem_group_block,
        source_keys=("pubchem_periodic_table_properties",),
    )


@lru_cache(maxsize=1)
def list_oxidation_state_evidence_records() -> tuple[OxidationStateEvidenceRecord, ...]:
    return tuple(_build_oxidation_state_evidence_record(row) for row in _OXIDATION_STATE_EVIDENCE_ROWS)


def find_oxidation_state_evidence_record(
    identifier: str | int,
) -> OxidationStateEvidenceRecord:
    identifier_text = str(identifier).strip()
    for record in list_oxidation_state_evidence_records():
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.element_id
        ):
            return record
    raise KeyError(f"unknown oxidation-state evidence record: {identifier_text}")


def validate_oxidation_state_evidence_records(
    records: tuple[OxidationStateEvidenceRecord, ...] | None = None,
) -> dict[str, Any]:
    checked_records = records if records is not None else list_oxidation_state_evidence_records()
    invalid_records = tuple(record.element_id for record in checked_records if record.validate())
    observed_symbols = tuple(record.symbol for record in checked_records)
    full_span_expected = records is None or len(checked_records) == len(CS_RN_PROMOTION_SYMBOLS)
    validation_status = "oxidation_state_evidence_records_validated"
    if invalid_records or (full_span_expected and observed_symbols != CS_RN_PROMOTION_SYMBOLS):
        validation_status = "oxidation_state_evidence_records_rejected"
    return {
        "validation_status": validation_status,
        "record_count": len(checked_records),
        "variable_oxidation_state_count": sum(
            1 for record in checked_records if len(record.oxidation_states) > 1
        ),
        "negative_oxidation_state_count": sum(
            1
            for record in checked_records
            if any(oxidation_state < 0 for oxidation_state in record.oxidation_states)
        ),
        "zero_oxidation_state_count": sum(
            1 for record in checked_records if 0 in record.oxidation_states
        ),
        "group_blocks": tuple(sorted({record.pubchem_group_block for record in checked_records})),
        "invalid_records": invalid_records,
        "source_keys": tuple(
            sorted({source_key for record in checked_records for source_key in record.source_keys})
        ),
    }
