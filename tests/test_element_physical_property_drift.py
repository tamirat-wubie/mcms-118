import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from mcms.elements import find_physical_property_evidence_record

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "check_element_physical_property_drift.py"
)
SPEC = spec_from_file_location("check_element_physical_property_drift", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
DRIFT_MODULE = module_from_spec(SPEC)
sys.modules[SPEC.name] = DRIFT_MODULE
SPEC.loader.exec_module(DRIFT_MODULE)

SourcePhysicalPropertyRow = DRIFT_MODULE.SourcePhysicalPropertyRow
build_physical_property_drift_report = DRIFT_MODULE.build_physical_property_drift_report
parse_pubchem_physical_property_csv = DRIFT_MODULE.parse_pubchem_physical_property_csv


def _fixture_csv(rows: list[tuple[str, str, str, str, str, str]]) -> str:
    body = "\n".join(
        (
            f'{atomic_number},"{symbol}","{standard_state}",'
            f'"{melting_point}","{boiling_point}","{density}"'
        )
        for (
            atomic_number,
            symbol,
            standard_state,
            melting_point,
            boiling_point,
            density,
        ) in rows
    )
    return (
        '"AtomicNumber","Symbol","StandardState","MeltingPoint","BoilingPoint","Density"\n'
        f"{body}\n"
    )


def test_parse_pubchem_physical_property_rows_skips_incomplete_values():
    source_rows = parse_pubchem_physical_property_csv(
        _fixture_csv(
            [
                ("35", "Br", "Liquid", "265.95", "331.95", "3.11"),
                ("85", "At", "Solid", "575", "", "7"),
            ]
        )
    )

    assert len(source_rows) == 1
    assert source_rows[0].symbol == "Br"
    assert source_rows[0].standard_state == "Liquid"
    assert source_rows[0].melting_point_k == 265.95
    assert source_rows[0].density_value == 3.11


def test_physical_property_drift_report_has_no_drift_for_fixture_rows():
    bromine = find_physical_property_evidence_record("Br")
    radon = find_physical_property_evidence_record("Rn")
    source_rows = tuple(
        SourcePhysicalPropertyRow(
            atomic_number=record.atomic_number,
            symbol=record.symbol,
            standard_state=record.standard_state,
            melting_point_k=record.melting_point_k,
            boiling_point_k=record.boiling_point_k,
            density_value=record.density_value,
        )
        for record in (bromine, radon)
    )
    report = build_physical_property_drift_report(
        source_rows,
        source_url="fixture://pubchem-physical",
        require_complete_source=False,
    )

    assert report["drift_status"] == "physical_property_evidence_no_drift"
    assert report["drift_count"] == 0
    assert report["source_count"] == 2
    assert report["local_count"] == 93


def test_physical_property_drift_report_detects_changed_fields():
    report = build_physical_property_drift_report(
        (
            SourcePhysicalPropertyRow(
                atomic_number=35,
                symbol="Bx",
                standard_state="Gas",
                melting_point_k=266.0,
                boiling_point_k=332.0,
                density_value=3.2,
            ),
        ),
        source_url="fixture://pubchem-physical",
        require_complete_source=False,
    )
    drift_fields = {drift["field"] for drift in report["drifts"]}

    assert report["drift_status"] == "physical_property_evidence_drift_detected"
    assert report["drift_count"] == 5
    assert drift_fields == {
        "symbol",
        "standard_state",
        "melting_point_k",
        "boiling_point_k",
        "density_value",
    }


def test_physical_property_drift_report_requires_complete_source_when_enabled():
    bromine = find_physical_property_evidence_record("Br")
    report = build_physical_property_drift_report(
        (
            SourcePhysicalPropertyRow(
                atomic_number=bromine.atomic_number,
                symbol=bromine.symbol,
                standard_state=bromine.standard_state,
                melting_point_k=bromine.melting_point_k,
                boiling_point_k=bromine.boiling_point_k,
                density_value=bromine.density_value,
            ),
        ),
        source_url="fixture://pubchem-physical",
        require_complete_source=True,
    )
    missing_fields = {drift["field"] for drift in report["drifts"]}

    assert report["drift_status"] == "physical_property_evidence_drift_detected"
    assert report["source_count"] == 1
    assert report["drift_count"] == 92
    assert missing_fields == {"missing_source_record"}
