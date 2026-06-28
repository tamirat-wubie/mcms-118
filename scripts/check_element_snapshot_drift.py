"""Purpose: compare the local MSPEE element snapshot with the CIAAW source table.

Governance scope: detects source drift without mutating snapshot records.
Dependencies: standard-library HTML parsing, URL fetching, JSON, and mcms snapshot APIs.
Invariants: source rows are keyed by atomic number; every drift is explicit.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mcms.elements import list_full_snapshot_records  # noqa: E402

CIAAW_SOURCE_URL = "https://www.ciaaw.org/atomic-weights.htm"


@dataclass(frozen=True)
class SourceSnapshotRow:
    atomic_number: int
    symbol: str
    name: str
    atomic_weight_display: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SnapshotDrift:
    atomic_number: int
    symbol: str
    field: str
    local_value: str
    source_value: str

    def to_dict(self) -> dict:
        return asdict(self)


class CiaawTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._inside_cell = False
        self._inside_row = False
        self._current_cell: list[str] = []
        self._current_row: list[str] = []
        self.rows: list[tuple[str, ...]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self._inside_row = True
            self._current_row = []
        if self._inside_row and tag in {"td", "th"}:
            self._inside_cell = True
            self._current_cell = []

    def handle_data(self, data: str) -> None:
        if self._inside_cell:
            self._current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._inside_cell:
            self._inside_cell = False
            self._current_row.append(normalize_text("".join(self._current_cell)))
        if tag == "tr" and self._inside_row:
            self._inside_row = False
            if self._current_row:
                self.rows.append(tuple(self._current_row))


def normalize_text(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


def normalize_name(value: str) -> str:
    return normalize_text(value).title()


def normalize_atomic_weight(value: str) -> str:
    normalized = normalize_text(value).replace(" ", "")
    if normalized in {"", "-", "\u2013", "\u2014"}:
        return "unavailable"
    return normalized


def parse_ciaaw_atomic_weight_rows(html_text: str) -> tuple[SourceSnapshotRow, ...]:
    parser = CiaawTableParser()
    parser.feed(html_text)
    source_rows: list[SourceSnapshotRow] = []
    for row in parser.rows:
        if len(row) < 4:
            continue
        atomic_number_text = normalize_text(row[0])
        if not atomic_number_text.isdigit():
            continue
        source_rows.append(
            SourceSnapshotRow(
                atomic_number=int(atomic_number_text),
                symbol=normalize_text(row[1]),
                name=normalize_name(row[2]),
                atomic_weight_display=normalize_atomic_weight(row[3]),
            )
        )
    return tuple(source_rows)


def fetch_source_html(source_url: str) -> str:
    request = Request(
        source_url,
        headers={
            "User-Agent": "mcms-118-source-drift-check/0.1 (+https://github.com/tamirat-wubie/mcms-118)"
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def compare_snapshot_to_source(
    source_rows: Sequence[SourceSnapshotRow],
    *,
    require_complete_source: bool,
) -> tuple[SnapshotDrift, ...]:
    local_by_atomic_number = {
        record.atomic_number: record for record in list_full_snapshot_records()
    }
    source_by_atomic_number = {row.atomic_number: row for row in source_rows}
    drifts: list[SnapshotDrift] = []

    if require_complete_source:
        for atomic_number, local_record in local_by_atomic_number.items():
            if atomic_number not in source_by_atomic_number:
                drifts.append(
                    SnapshotDrift(
                        atomic_number=atomic_number,
                        symbol=local_record.symbol,
                        field="missing_source_record",
                        local_value=local_record.symbol,
                        source_value="missing",
                    )
                )
        for atomic_number, source_row in source_by_atomic_number.items():
            if atomic_number not in local_by_atomic_number:
                drifts.append(
                    SnapshotDrift(
                        atomic_number=atomic_number,
                        symbol=source_row.symbol,
                        field="missing_local_record",
                        local_value="missing",
                        source_value=source_row.symbol,
                    )
                )

    for atomic_number, source_row in source_by_atomic_number.items():
        local_record = local_by_atomic_number.get(atomic_number)
        if local_record is None:
            continue
        comparison_fields = (
            ("symbol", local_record.symbol, source_row.symbol),
            ("name", local_record.name, source_row.name),
            (
                "atomic_weight_display",
                local_record.atomic_weight_model.display,
                source_row.atomic_weight_display,
            ),
        )
        for field, local_value, source_value in comparison_fields:
            if local_value != source_value:
                drifts.append(
                    SnapshotDrift(
                        atomic_number=atomic_number,
                        symbol=local_record.symbol,
                        field=field,
                        local_value=local_value,
                        source_value=source_value,
                    )
                )

    return tuple(sorted(drifts, key=lambda drift: (drift.atomic_number, drift.field)))


def build_drift_report(
    source_rows: Sequence[SourceSnapshotRow],
    *,
    source_url: str,
    require_complete_source: bool = True,
) -> dict:
    drifts = compare_snapshot_to_source(
        source_rows,
        require_complete_source=require_complete_source,
    )
    return {
        "source_url": source_url,
        "local_count": len(list_full_snapshot_records()),
        "source_count": len(source_rows),
        "drift_count": len(drifts),
        "drift_status": (
            "element_snapshot_drift_detected"
            if drifts
            else "element_snapshot_no_drift"
        ),
        "drifts": [drift.to_dict() for drift in drifts],
    }


def build_unavailable_report(source_url: str, error: Exception) -> dict:
    return {
        "source_url": source_url,
        "local_count": len(list_full_snapshot_records()),
        "source_count": 0,
        "drift_count": 0,
        "drift_status": "element_snapshot_source_unavailable",
        "causal_error": f"{type(error).__name__}: {error}",
        "drifts": [],
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether the local MSPEE 118-element snapshot drifted from CIAAW."
    )
    parser.add_argument("--source-url", default=CIAAW_SOURCE_URL)
    parser.add_argument(
        "--fixture-html",
        type=Path,
        help="Read CIAAW-compatible HTML from disk instead of fetching the live source.",
    )
    parser.add_argument(
        "--allow-partial-source",
        action="store_true",
        help="Compare only rows present in the source fixture.",
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
        html_text = (
            args.fixture_html.read_text(encoding="utf-8")
            if args.fixture_html
            else fetch_source_html(args.source_url)
        )
        source_rows = parse_ciaaw_atomic_weight_rows(html_text)
        report = build_drift_report(
            source_rows,
            source_url=args.source_url,
            require_complete_source=not args.allow_partial_source,
        )
    except (OSError, URLError) as error:
        report = build_unavailable_report(args.source_url, error)

    print(json.dumps(report, indent=2, sort_keys=True))
    if args.fail_on_drift and report["drift_status"] != "element_snapshot_no_drift":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
