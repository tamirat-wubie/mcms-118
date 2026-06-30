"""Purpose: NIST configuration evidence overlay for Cs-Rn promotion readiness.

Project scope: records neutral and first-cation electronic configurations for
snapshot elements 55-86 without promoting them to full Level 1 seed records.
Dependencies: local snapshot records and configuration-audit validation.
Invariants: source-backed configurations are evidence records; promotion still
requires frontier signatures, valence signatures, behavior tags, and relation edges.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.model import ConfigurationAudit, SourceReference
from mcms.elements.promotion import CS_RN_PROMOTION_SYMBOLS
from mcms.elements.snapshot import get_snapshot_record

CONFIGURATION_EVIDENCE_SOURCE_REFERENCES = (
    SourceReference(
        key="nist_electronic_configurations",
        authority="NIST",
        title="Electronic Configurations of the Elements",
        url=(
            "https://www.nist.gov/pml/atomic-reference-data-electronic-structure-"
            "calculations/atomic-reference-data-electronic-8"
        ),
        version="source page updated 2025-08-15; observed 2026-06-29",
    ),
)

VALID_CONFIGURATION_EVIDENCE_STATUSES = {"configuration_evidence"}

_SPECIAL_FIRST_CATION_LITERATURE_SYMBOLS = {
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Po",
    "At",
    "Rn",
}

_CONFIGURATION_EVIDENCE_ROWS: tuple[
    tuple[str, str, str, str | None, bool, str | None],
    ...,
] = (
    ("Cs", "[Xe] 6s^1", "[Kr] 4d^10 5s^2 5p^6", None, False, None),
    ("Ba", "[Xe] 6s^2", "[Xe] 6s^1", None, False, None),
    ("La", "[Xe] 5d^1 6s^2", "[Xe] 5d^2", None, False, None),
    ("Ce", "[Xe] 4f^1 5d^1 6s^2", "[Xe] 4f^1 5d^2", None, False, None),
    ("Pr", "[Xe] 4f^3 6s^2", "[Xe] 4f^3 6s^1", None, False, None),
    ("Nd", "[Xe] 4f^4 6s^2", "[Xe] 4f^4 6s^1", None, False, None),
    ("Pm", "[Xe] 4f^5 6s^2", "[Xe] 4f^5 6s^1", None, False, None),
    ("Sm", "[Xe] 4f^6 6s^2", "[Xe] 4f^6 6s^1", None, False, None),
    ("Eu", "[Xe] 4f^7 6s^2", "[Xe] 4f^7 6s^1", None, False, None),
    ("Gd", "[Xe] 4f^7 5d^1 6s^2", "[Xe] 4f^7 5d^1 6s^1", None, False, None),
    ("Tb", "[Xe] 4f^9 6s^2", "[Xe] 4f^9 6s^1", None, False, None),
    ("Dy", "[Xe] 4f^10 6s^2", "[Xe] 4f^10 6s^1", None, False, None),
    ("Ho", "[Xe] 4f^11 6s^2", "[Xe] 4f^11 6s^1", None, False, None),
    ("Er", "[Xe] 4f^12 6s^2", "[Xe] 4f^12 6s^1", None, False, None),
    ("Tm", "[Xe] 4f^13 6s^2", "[Xe] 4f^13 6s^1", None, False, None),
    ("Yb", "[Xe] 4f^14 6s^2", "[Xe] 4f^14 6s^1", None, False, None),
    ("Lu", "[Xe] 4f^14 5d^1 6s^2", "[Xe] 4f^14 6s^2", None, False, None),
    ("Hf", "[Xe] 4f^14 5d^2 6s^2", "[Xe] 4f^14 5d^1 6s^2", None, False, None),
    ("Ta", "[Xe] 4f^14 5d^3 6s^2", "[Xe] 4f^14 5d^3 6s^1", None, False, None),
    ("W", "[Xe] 4f^14 5d^4 6s^2", "[Xe] 4f^14 5d^4 6s^1", None, False, None),
    ("Re", "[Xe] 4f^14 5d^5 6s^2", "[Xe] 4f^14 5d^5 6s^1", None, False, None),
    ("Os", "[Xe] 4f^14 5d^6 6s^2", "[Xe] 4f^14 5d^6 6s^1", None, False, None),
    ("Ir", "[Xe] 4f^14 5d^7 6s^2", "[Xe] 4f^14 5d^7 6s^1", None, False, None),
    (
        "Pt",
        "[Xe] 4f^14 5d^9 6s^1",
        "[Xe] 4f^14 5d^9",
        "[Xe] 4f^14 5d^8 6s^2",
        True,
        "filled/near-filled 5d-shell stabilization pattern",
    ),
    (
        "Au",
        "[Xe] 4f^14 5d^10 6s^1",
        "[Xe] 4f^14 5d^10",
        "[Xe] 4f^14 5d^9 6s^2",
        True,
        "filled 5d-shell stabilization pattern",
    ),
    ("Hg", "[Xe] 4f^14 5d^10 6s^2", "[Xe] 4f^14 5d^10 6s^1", None, False, None),
    ("Tl", "[Xe] 4f^14 5d^10 6s^2 6p^1", "[Xe] 4f^14 5d^10 6s^2", None, False, None),
    (
        "Pb",
        "[Xe] 4f^14 5d^10 6s^2 6p^2",
        "[Xe] 4f^14 5d^10 6s^2 6p^1",
        None,
        False,
        None,
    ),
    (
        "Bi",
        "[Xe] 4f^14 5d^10 6s^2 6p^3",
        "[Xe] 4f^14 5d^10 6s^2 6p^2",
        None,
        False,
        None,
    ),
    (
        "Po",
        "[Xe] 4f^14 5d^10 6s^2 6p^4",
        "[Xe] 4f^14 5d^10 6s^2 6p^3",
        None,
        False,
        None,
    ),
    (
        "At",
        "[Xe] 4f^14 5d^10 6s^2 6p^5",
        "[Xe] 4f^14 5d^10 6s^2 6p^4",
        None,
        False,
        None,
    ),
    (
        "Rn",
        "[Xe] 4f^14 5d^10 6s^2 6p^6",
        "[Xe] 4f^14 5d^10 6s^2 6p^5",
        None,
        False,
        None,
    ),
)


@dataclass(frozen=True)
class ConfigurationEvidenceRecord:
    element_id: str
    symbol: str
    atomic_number: int
    neutral_configuration: str
    first_cation_configuration: str
    configuration_audit: ConfigurationAudit
    source_keys: tuple[str, ...]
    first_cation_source_note: str | None = None
    evidence_status: str = "configuration_evidence"
    notes: tuple[str, ...] = (
        "Configuration evidence is not a full Level 1 seed promotion.",
        "Frontier signatures, valence signatures, behavior tags, and relation edges remain separate.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        expected_element_id = f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}"
        if self.element_id != expected_element_id:
            errors.append("configuration evidence element id must match snapshot element id.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("configuration evidence atomic number must match snapshot element.")
        if self.symbol not in CS_RN_PROMOTION_SYMBOLS:
            errors.append("configuration evidence symbol must be in the Cs-Rn span.")
        if not self.neutral_configuration:
            errors.append("neutral configuration evidence is required.")
        if not self.first_cation_configuration:
            errors.append("first-cation configuration evidence is required.")
        if self.configuration_audit.source_backed_configuration != self.neutral_configuration:
            errors.append("configuration audit source-backed value must match neutral evidence.")
        errors.extend(self.configuration_audit.validate())
        if "nist_electronic_configurations" not in self.source_keys:
            errors.append("NIST electronic-configuration source key is required.")
        if self.evidence_status not in VALID_CONFIGURATION_EVIDENCE_STATUSES:
            errors.append("configuration evidence status is unknown.")
        if self.symbol in _SPECIAL_FIRST_CATION_LITERATURE_SYMBOLS:
            if not self.first_cation_source_note:
                errors.append("special first-cation literature note is required.")
        elif self.first_cation_source_note is not None:
            errors.append("first-cation source note is only valid for NIST special cases.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _first_cation_source_note(symbol: str) -> str | None:
    if symbol not in _SPECIAL_FIRST_CATION_LITERATURE_SYMBOLS:
        return None
    return "NIST marks this first-cation configuration as identified from literature."


def _build_configuration_evidence_record(
    row: tuple[str, str, str, str | None, bool, str | None],
) -> ConfigurationEvidenceRecord:
    (
        symbol,
        neutral_configuration,
        first_cation_configuration,
        simple_candidate,
        is_exception,
        exception_reason,
    ) = row
    snapshot = get_snapshot_record(symbol)
    return ConfigurationEvidenceRecord(
        element_id=f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}",
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        neutral_configuration=neutral_configuration,
        first_cation_configuration=first_cation_configuration,
        configuration_audit=ConfigurationAudit(
            source_backed_configuration=neutral_configuration,
            simple_aufbau_candidate=simple_candidate,
            is_exception=is_exception,
            exception_reason=exception_reason,
        ),
        source_keys=("nist_electronic_configurations",),
        first_cation_source_note=_first_cation_source_note(symbol),
    )


def list_configuration_evidence_records() -> tuple[ConfigurationEvidenceRecord, ...]:
    return tuple(_build_configuration_evidence_record(row) for row in _CONFIGURATION_EVIDENCE_ROWS)


def find_configuration_evidence_record(identifier: str | int) -> ConfigurationEvidenceRecord:
    identifier_text = str(identifier).strip()
    for record in list_configuration_evidence_records():
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.element_id
        ):
            return record
    raise KeyError(f"unknown configuration evidence record: {identifier_text}")


def validate_configuration_evidence_records(
    records: tuple[ConfigurationEvidenceRecord, ...] | None = None,
) -> dict[str, Any]:
    checked_records = records if records is not None else list_configuration_evidence_records()
    invalid_records = tuple(record.element_id for record in checked_records if record.validate())
    observed_symbols = tuple(record.symbol for record in checked_records)
    full_span_expected = records is None or len(checked_records) == len(CS_RN_PROMOTION_SYMBOLS)
    validation_status = "configuration_evidence_records_validated"
    if invalid_records or (full_span_expected and observed_symbols != CS_RN_PROMOTION_SYMBOLS):
        validation_status = "configuration_evidence_records_rejected"
    return {
        "validation_status": validation_status,
        "record_count": len(checked_records),
        "exception_count": sum(
            1 for record in checked_records if record.configuration_audit.is_exception
        ),
        "special_first_cation_literature_count": sum(
            1 for record in checked_records if record.first_cation_source_note is not None
        ),
        "invalid_records": invalid_records,
        "source_keys": tuple(
            sorted({source_key for record in checked_records for source_key in record.source_keys})
        ),
    }
