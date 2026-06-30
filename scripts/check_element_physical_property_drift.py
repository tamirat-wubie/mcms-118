"""Purpose: compare local MSPEE physical-property evidence with PubChem CSV rows.

Project scope: detects source drift for standard state, melting point, boiling
point, and density without mutating local evidence records.
Dependencies: standard-library CSV parsing, URL fetching, JSON, and mcms evidence APIs.
Invariants: measured properties remain source-backed; incomplete source rows are
not guessed; every drift is explicit.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mcms.elements import list_physical_property_evidence_records  # noqa: E402

PUBCHEM_SOURCE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV"


@dataclass(frozen=True)
class SourcePhysicalPropertyRow:
    atomic_number: int
    symbol: str
    standard_state: str
    melting_point_k: float
    boiling_point_k: float
    density_value: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PhysicalPropertyDrift:
    atomic_number: int
    symbol: str
    field: str
    local_value: Any
    source_value: Any

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parse_required_float(row: dict[str, str], key: str) -> float | None:
    value = row[key].strip()
    if not value:
        return None
    return float(value)


def parse_pubchem_physical_property_csv(csv_text: str) -> tuple[SourcePhysicalPropertyRow, ...]:
    reader = csv.DictReader(io.StringIO(csv_text))
    required_fields = {
        "AtomicNumber",
        "Symbol",
        "StandardState",
        "MeltingPoint",
        "BoilingPoint",
        "Density",
    }
    normalized_fieldnames = {
        field_name.strip().lstrip("\ufeff")
        for field_name in (reader.fieldnames or ())
    }
    if reader.fieldnames is None or not required_fields <= normalized_fieldnames:
        raise ValueError("PubChem CSV is missing required physical-property columns.")

    source_rows: list[SourcePhysicalPropertyRow] = []
    for row in reader:
        normalized_row = {
            field_name.strip().lstrip("\ufeff"): value
            for field_name, value in row.items()
            if field_name is not None
        }
        atomic_number = normalized_row["AtomicNumber"].strip()
        symbol = normalized_row["Symbol"].strip()
        standard_state = normalized_row["StandardState"].strip()
        melting_point_k = _parse_required_float(normalized_row, "MeltingPoint")
        boiling_point_k = _parse_required_float(normalized_row, "BoilingPoint")
        density_value = _parse_required_float(normalized_row, "Density")
        if not atomic_number or not symbol or not standard_state:
            continue
        if melting_point_k is None or boiling_point_k is None or density_value is None:
            continue
        source_rows.append(
            SourcePhysicalPropertyRow(
                atomic_number=int(atomic_number),
                symbol=symbol,
                standard_state=standard_state,
                melting_point_k=melting_point_k,
                boiling_point_k=boiling_point_k,
                density_value=density_value,
            )
        )
    return tuple(source_rows)


def fetch_source_csv(source_url: str) -> str:
    request = Request(
        source_url,
        headers={
            "User-Agent": "mcms-118-physical-property-drift-check/0.1 "
            "(+https://github.com/tamirat-wubie/mcms-118)"
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def _local_physical_property_records() -> dict[int, Any]:
    return {
        record.atomic_number: record
        for record in list_physical_property_evidence_records()
    }


def compare_physical_properties_to_source(
    source_rows: Sequence[SourcePhysicalPropertyRow],
    *,
    require_complete_source: bool,
) -> tuple[PhysicalPropertyDrift, ...]:
    local_by_atomic_number = _local_physical_property_records()
    source_by_atomic_number = {row.atomic_number: row for row in source_rows}
    drifts: list[PhysicalPropertyDrift] = []

    if require_complete_source:
        for atomic_number, local_record in local_by_atomic_number.items():
            if atomic_number not in source_by_atomic_number:
                drifts.append(
                    PhysicalPropertyDrift(
                        atomic_number=atomic_number,
                        symbol=local_record.symbol,
                        field="missing_source_record",
                        local_value=local_record.symbol,
                        source_value="missing",
                    )
                )

    for atomic_number, source_row in source_by_atomic_number.items():
        local_record = local_by_atomic_number.get(atomic_number)
        if local_record is None:
            continue
        comparison_fields = (
            ("symbol", local_record.symbol, source_row.symbol),
            ("standard_state", local_record.standard_state, source_row.standard_state),
            ("melting_point_k", local_record.melting_point_k, source_row.melting_point_k),
            ("boiling_point_k", local_record.boiling_point_k, source_row.boiling_point_k),
            ("density_value", local_record.density_value, source_row.density_value),
        )
        for field, local_value, source_value in comparison_fields:
            if local_value != source_value:
                drifts.append(
                    PhysicalPropertyDrift(
                        atomic_number=atomic_number,
                        symbol=local_record.symbol,
                        field=field,
                        local_value=local_value,
                        source_value=source_value,
                    )
                )

    return tuple(sorted(drifts, key=lambda drift: (drift.atomic_number, drift.field)))


def build_physical_property_drift_report(
    source_rows: Sequence[SourcePhysicalPropertyRow],
    *,
    source_url: str,
    require_complete_source: bool = True,
) -> dict[str, Any]:
    drifts = compare_physical_properties_to_source(
        source_rows,
        require_complete_source=require_complete_source,
    )
    return {
        "source_url": source_url,
        "local_count": len(_local_physical_property_records()),
        "source_count": len(source_rows),
        "drift_count": len(drifts),
        "drift_status": (
            "physical_property_evidence_drift_detected"
            if drifts
            else "physical_property_evidence_no_drift"
        ),
        "drifts": [drift.to_dict() for drift in drifts],
    }


def build_unavailable_report(source_url: str, error: Exception) -> dict[str, Any]:
    return {
        "source_url": source_url,
        "local_count": len(_local_physical_property_records()),
        "source_count": 0,
        "drift_count": 0,
        "drift_status": "physical_property_evidence_source_unavailable",
        "causal_error": f"{type(error).__name__}: {error}",
        "drifts": [],
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether local MSPEE physical-property evidence drifted from PubChem."
    )
    parser.add_argument("--source-url", default=PUBCHEM_SOURCE_URL)
    parser.add_argument(
        "--fixture-csv",
        type=Path,
        help="Read PubChem-compatible CSV from disk instead of fetching the live source.",
    )
    parser.add_argument(
        "--allow-partial-source",
        action="store_true",
        help="Compare only complete physical-property rows present in the source fixture.",
    )
    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="Exit non-zero when source drift or source unavailability is detected.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        csv_text = (
            args.fixture_csv.read_text(encoding="utf-8")
            if args.fixture_csv
            else fetch_source_csv(args.source_url)
        )
        source_rows = parse_pubchem_physical_property_csv(csv_text)
        report = build_physical_property_drift_report(
            source_rows,
            source_url=args.source_url,
            require_complete_source=not args.allow_partial_source,
        )
    except (OSError, URLError, ValueError) as error:
        report = build_unavailable_report(args.source_url, error)

    print(json.dumps(report, indent=2, sort_keys=True))
    if args.fail_on_drift and report["drift_status"] != "physical_property_evidence_no_drift":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
