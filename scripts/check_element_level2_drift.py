"""Purpose: compare local MSPEE Level 2 chemistry values with the PubChem CSV source.

Project scope: detects source drift without mutating element seed or snapshot-overlay records.
Dependencies: standard-library CSV parsing, URL fetching, JSON, and mcms element APIs.
Invariants: local promoted Level 2 records are source-backed; every drift is explicit.
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

from mcms.elements import list_period_5_level_2_profiles, list_seed_elements  # noqa: E402

PUBCHEM_SOURCE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV"
PUBCHEM_SOURCE_KEY = "pubchem_periodic_table_properties"
_BOND_TENDENCY_TAGS_BY_PUBCHEM_GROUP_BLOCK: dict[str, tuple[str, ...]] = {
    "Alkali metal": ("metallic_bonding", "ionic_bonding"),
    "Alkaline earth metal": ("metallic_bonding", "ionic_bonding"),
    "Halogen": ("covalent_bonding", "ionic_bonding", "molecular_covalent"),
    "Metalloid": ("covalent_bonding", "network_covalent"),
    "Noble gas": ("noble_gas_low_reactivity",),
    "Nonmetal": ("covalent_bonding", "molecular_covalent"),
    "Post-transition metal": ("metallic_bonding", "covalent_bonding"),
    "Transition metal": ("metallic_bonding", "coordination_complex"),
}


@dataclass(frozen=True)
class SourceLevel2ChemistryRow:
    atomic_number: int
    symbol: str
    oxidation_states: tuple[int, ...]
    electronegativity_value: float | None
    first_ionization_energy_ev: float | None
    group_block: str
    bond_tendency_tags: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["oxidation_states"] = list(self.oxidation_states)
        payload["bond_tendency_tags"] = list(self.bond_tendency_tags)
        return payload


@dataclass(frozen=True)
class Level2ChemistryDrift:
    atomic_number: int
    symbol: str
    field: str
    local_value: Any
    source_value: Any

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_oxidation_states(value: str) -> tuple[int, ...]:
    if not value.strip():
        return ()
    states: list[int] = []
    for item in value.split(","):
        normalized = item.strip().replace("+", "")
        if not normalized:
            continue
        states.append(int(normalized))
    return tuple(states)


def normalize_electronegativity(value: str) -> float | None:
    if not value.strip():
        return None
    return float(value)


def normalize_first_ionization_energy(value: str) -> float | None:
    if not value.strip():
        return None
    return float(value)


def derive_bond_tendency_tags(group_block: str) -> tuple[str, ...]:
    return _BOND_TENDENCY_TAGS_BY_PUBCHEM_GROUP_BLOCK.get(group_block, ())


def parse_pubchem_periodic_table_csv(csv_text: str) -> tuple[SourceLevel2ChemistryRow, ...]:
    reader = csv.DictReader(io.StringIO(csv_text))
    required_fields = {
        "AtomicNumber",
        "Symbol",
        "OxidationStates",
        "Electronegativity",
        "IonizationEnergy",
        "GroupBlock",
    }
    normalized_fieldnames = {
        field_name.strip().lstrip("\ufeff")
        for field_name in (reader.fieldnames or ())
    }
    if reader.fieldnames is None or not required_fields <= normalized_fieldnames:
        raise ValueError("PubChem CSV is missing required Level 2 chemistry columns.")
    source_rows: list[SourceLevel2ChemistryRow] = []
    for row in reader:
        normalized_row = {
            field_name.strip().lstrip("\ufeff"): value
            for field_name, value in row.items()
            if field_name is not None
        }
        atomic_number = normalized_row["AtomicNumber"].strip()
        symbol = normalized_row["Symbol"].strip()
        group_block = normalized_row["GroupBlock"].strip()
        if not atomic_number or not symbol:
            continue
        source_rows.append(
            SourceLevel2ChemistryRow(
                atomic_number=int(atomic_number),
                symbol=symbol,
                oxidation_states=normalize_oxidation_states(normalized_row["OxidationStates"]),
                electronegativity_value=normalize_electronegativity(
                    normalized_row["Electronegativity"]
                ),
                first_ionization_energy_ev=normalize_first_ionization_energy(
                    normalized_row["IonizationEnergy"]
                ),
                group_block=group_block,
                bond_tendency_tags=derive_bond_tendency_tags(group_block),
            )
        )
    return tuple(source_rows)


def fetch_source_csv(source_url: str) -> str:
    request = Request(
        source_url,
        headers={
            "User-Agent": "mcms-118-level2-drift-check/0.1 (+https://github.com/tamirat-wubie/mcms-118)"
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def _local_level_2_records() -> dict[int, Any]:
    return {
        element.identity.atomic_number: element
        for element in list_seed_elements()
        if element.state.data_level == 2 and PUBCHEM_SOURCE_KEY in element.source_keys()
    }


def _local_period_5_level_2_profiles() -> dict[int, Any]:
    return {profile.atomic_number: profile for profile in list_period_5_level_2_profiles()}


def _json_ready_value(value: Any) -> Any:
    if isinstance(value, tuple):
        return list(value)
    return value


def compare_level_2_to_source(
    source_rows: Sequence[SourceLevel2ChemistryRow],
    *,
    require_complete_source: bool,
) -> tuple[Level2ChemistryDrift, ...]:
    local_by_atomic_number = _local_level_2_records()
    source_by_atomic_number = {row.atomic_number: row for row in source_rows}
    drifts: list[Level2ChemistryDrift] = []

    if require_complete_source:
        for atomic_number, local_element in local_by_atomic_number.items():
            if atomic_number not in source_by_atomic_number:
                drifts.append(
                    Level2ChemistryDrift(
                        atomic_number=atomic_number,
                        symbol=local_element.identity.symbol,
                        field="missing_source_record",
                        local_value=local_element.identity.symbol,
                        source_value="missing",
                    )
                )

    for atomic_number, source_row in source_by_atomic_number.items():
        local_element = local_by_atomic_number.get(atomic_number)
        if local_element is None:
            continue
        comparison_fields = (
            ("symbol", local_element.identity.symbol, source_row.symbol),
            (
                "oxidation_states",
                local_element.state.oxidation_states,
                source_row.oxidation_states,
            ),
            (
                "electronegativity_value",
                local_element.state.electronegativity_value,
                source_row.electronegativity_value,
            ),
            (
                "first_ionization_energy_ev",
                local_element.state.first_ionization_energy_ev,
                source_row.first_ionization_energy_ev,
            ),
            (
                "bond_tendency_tags",
                local_element.state.bond_tendency_tags,
                source_row.bond_tendency_tags,
            ),
        )
        for field, local_value, source_value in comparison_fields:
            if local_value != source_value:
                drifts.append(
                    Level2ChemistryDrift(
                        atomic_number=atomic_number,
                        symbol=local_element.identity.symbol,
                        field=field,
                        local_value=_json_ready_value(local_value),
                        source_value=_json_ready_value(source_value),
                    )
                )

    return tuple(sorted(drifts, key=lambda drift: (drift.atomic_number, drift.field)))


def compare_period_5_level_2_to_source(
    source_rows: Sequence[SourceLevel2ChemistryRow],
    *,
    require_complete_source: bool,
) -> tuple[Level2ChemistryDrift, ...]:
    local_by_atomic_number = _local_period_5_level_2_profiles()
    source_by_atomic_number = {row.atomic_number: row for row in source_rows}
    drifts: list[Level2ChemistryDrift] = []

    if require_complete_source:
        for atomic_number, local_profile in local_by_atomic_number.items():
            if atomic_number not in source_by_atomic_number:
                drifts.append(
                    Level2ChemistryDrift(
                        atomic_number=atomic_number,
                        symbol=local_profile.symbol,
                        field="missing_source_record",
                        local_value=local_profile.symbol,
                        source_value="missing",
                    )
                )

    for atomic_number, source_row in source_by_atomic_number.items():
        local_profile = local_by_atomic_number.get(atomic_number)
        if local_profile is None:
            continue
        comparison_fields = (
            ("symbol", local_profile.symbol, source_row.symbol),
            (
                "oxidation_states",
                local_profile.oxidation_states,
                source_row.oxidation_states,
            ),
            (
                "electronegativity_value",
                local_profile.electronegativity_value,
                source_row.electronegativity_value,
            ),
            (
                "first_ionization_energy_ev",
                local_profile.first_ionization_energy_ev,
                source_row.first_ionization_energy_ev,
            ),
            ("pubchem_group_block", local_profile.pubchem_group_block, source_row.group_block),
            (
                "bond_tendency_tags",
                local_profile.bond_tendency_tags,
                source_row.bond_tendency_tags,
            ),
        )
        for field, local_value, source_value in comparison_fields:
            if local_value != source_value:
                drifts.append(
                    Level2ChemistryDrift(
                        atomic_number=atomic_number,
                        symbol=local_profile.symbol,
                        field=field,
                        local_value=_json_ready_value(local_value),
                        source_value=_json_ready_value(source_value),
                    )
                )

    return tuple(sorted(drifts, key=lambda drift: (drift.atomic_number, drift.field)))


def build_drift_report(
    source_rows: Sequence[SourceLevel2ChemistryRow],
    *,
    source_url: str,
    require_complete_source: bool = True,
) -> dict[str, Any]:
    drifts = compare_level_2_to_source(
        source_rows,
        require_complete_source=require_complete_source,
    )
    return {
        "source_url": source_url,
        "local_count": len(_local_level_2_records()),
        "source_count": len(source_rows),
        "drift_count": len(drifts),
        "drift_status": (
            "element_level_2_chemistry_drift_detected"
            if drifts
            else "element_level_2_chemistry_no_drift"
        ),
        "drifts": [drift.to_dict() for drift in drifts],
    }


def build_period_5_level_2_drift_report(
    source_rows: Sequence[SourceLevel2ChemistryRow],
    *,
    source_url: str,
    require_complete_source: bool = True,
) -> dict[str, Any]:
    drifts = compare_period_5_level_2_to_source(
        source_rows,
        require_complete_source=require_complete_source,
    )
    return {
        "source_url": source_url,
        "local_count": len(_local_period_5_level_2_profiles()),
        "source_count": len(source_rows),
        "drift_count": len(drifts),
        "drift_status": (
            "period_5_level_2_snapshot_drift_detected"
            if drifts
            else "period_5_level_2_snapshot_no_drift"
        ),
        "drifts": [drift.to_dict() for drift in drifts],
    }


def build_unavailable_report(source_url: str, error: Exception, *, scope: str = "seed") -> dict[str, Any]:
    if scope == "period-5":
        return {
            "source_url": source_url,
            "local_count": len(_local_period_5_level_2_profiles()),
            "source_count": 0,
            "drift_count": 0,
            "drift_status": "period_5_level_2_snapshot_source_unavailable",
            "causal_error": f"{type(error).__name__}: {error}",
            "drifts": [],
        }
    return {
        "source_url": source_url,
        "local_count": len(_local_level_2_records()),
        "source_count": 0,
        "drift_count": 0,
        "drift_status": "element_level_2_chemistry_source_unavailable",
        "causal_error": f"{type(error).__name__}: {error}",
        "drifts": [],
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether local MSPEE Level 2 chemistry values drifted from PubChem."
    )
    parser.add_argument(
        "--scope",
        choices=("seed", "period-5"),
        default="seed",
        help=(
            "Compare first-54 seed Level 2 values, or the Rb-Xe period-5 "
            "Level 2 profile projection."
        ),
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
        csv_text = (
            args.fixture_csv.read_text(encoding="utf-8")
            if args.fixture_csv
            else fetch_source_csv(args.source_url)
        )
        source_rows = parse_pubchem_periodic_table_csv(csv_text)
        if args.scope == "period-5":
            report = build_period_5_level_2_drift_report(
                source_rows,
                source_url=args.source_url,
                require_complete_source=not args.allow_partial_source,
            )
        else:
            report = build_drift_report(
                source_rows,
                source_url=args.source_url,
                require_complete_source=not args.allow_partial_source,
            )
    except (OSError, URLError, ValueError) as error:
        report = build_unavailable_report(args.source_url, error, scope=args.scope)

    print(json.dumps(report, indent=2, sort_keys=True))
    no_drift_status = (
        "period_5_level_2_snapshot_no_drift"
        if args.scope == "period-5"
        else "element_level_2_chemistry_no_drift"
    )
    if args.fail_on_drift and report["drift_status"] != no_drift_status:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
