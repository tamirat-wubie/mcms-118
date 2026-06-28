import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from mcms.elements import get_seed_element

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_element_level2_drift.py"
SPEC = spec_from_file_location("check_element_level2_drift", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
DRIFT_MODULE = module_from_spec(SPEC)
sys.modules[SPEC.name] = DRIFT_MODULE
SPEC.loader.exec_module(DRIFT_MODULE)

SourceLevel2ChemistryRow = DRIFT_MODULE.SourceLevel2ChemistryRow
build_drift_report = DRIFT_MODULE.build_drift_report
parse_pubchem_periodic_table_csv = DRIFT_MODULE.parse_pubchem_periodic_table_csv


def _fixture_csv(rows: list[tuple[str, str, str, str]]) -> str:
    body = "\n".join(
        f'{atomic_number},"{symbol}","{electronegativity}","{oxidation_states}"'
        for atomic_number, symbol, electronegativity, oxidation_states in rows
    )
    return (
        '"AtomicNumber","Symbol","Electronegativity","OxidationStates"\n'
        f"{body}\n"
    )


def test_parse_pubchem_rows_normalizes_oxidation_states_and_blank_electronegativity():
    source_rows = parse_pubchem_periodic_table_csv(
        _fixture_csv(
            [
                ("1", "H", "2.2", "+1, -1"),
                ("18", "Ar", "", "0"),
            ]
        )
    )
    assert len(source_rows) == 2
    assert source_rows[0].oxidation_states == (1, -1)
    assert source_rows[0].electronegativity_value == 2.2
    assert source_rows[1].electronegativity_value is None


def test_level_2_drift_report_has_no_drift_for_fixture_rows():
    symbols = ("H", "O", "Ar", "Ca")
    source_rows = tuple(
        SourceLevel2ChemistryRow(
            atomic_number=get_seed_element(symbol).identity.atomic_number,
            symbol=symbol,
            oxidation_states=get_seed_element(symbol).state.oxidation_states,
            electronegativity_value=get_seed_element(symbol).state.electronegativity_value,
        )
        for symbol in symbols
    )
    report = build_drift_report(
        source_rows,
        source_url="fixture://pubchem",
        require_complete_source=False,
    )
    assert report["drift_status"] == "element_level_2_chemistry_no_drift"
    assert report["drift_count"] == 0
    assert report["source_count"] == 4
    assert report["local_count"] == 36


def test_level_2_drift_report_detects_symbol_oxidation_and_electronegativity_changes():
    report = build_drift_report(
        (
            SourceLevel2ChemistryRow(
                atomic_number=8,
                symbol="Ox",
                oxidation_states=(-2, -1),
                electronegativity_value=3.45,
            ),
        ),
        source_url="fixture://pubchem",
        require_complete_source=False,
    )
    drift_fields = {drift["field"] for drift in report["drifts"]}
    assert report["drift_status"] == "element_level_2_chemistry_drift_detected"
    assert report["drift_count"] == 3
    assert drift_fields == {"symbol", "oxidation_states", "electronegativity_value"}
    assert all(drift["atomic_number"] == 8 for drift in report["drifts"])


def test_level_2_drift_report_requires_complete_promoted_source_when_enabled():
    hydrogen = get_seed_element("H")
    report = build_drift_report(
        (
            SourceLevel2ChemistryRow(
                atomic_number=hydrogen.identity.atomic_number,
                symbol=hydrogen.identity.symbol,
                oxidation_states=hydrogen.state.oxidation_states,
                electronegativity_value=hydrogen.state.electronegativity_value,
            ),
        ),
        source_url="fixture://pubchem",
        require_complete_source=True,
    )
    missing_fields = {drift["field"] for drift in report["drifts"]}
    assert report["drift_status"] == "element_level_2_chemistry_drift_detected"
    assert report["source_count"] == 1
    assert report["drift_count"] == 35
    assert missing_fields == {"missing_source_record"}
