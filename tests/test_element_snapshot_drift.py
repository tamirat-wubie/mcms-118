from mcms.elements import get_snapshot_record, list_full_snapshot_records
from scripts.check_element_snapshot_drift import (
    SourceSnapshotRow,
    build_drift_report,
    parse_ciaaw_atomic_weight_rows,
)


def _fixture_html(rows: list[tuple[str, str, str, str]]) -> str:
    body = "".join(
        (
            "<tr>"
            f"<td>{atomic_number}</td>"
            f"<td>{symbol}</td>"
            f"<td>{name}</td>"
            f"<td>{atomic_weight}</td>"
            "</tr>"
        )
        for atomic_number, symbol, name, atomic_weight in rows
    )
    return f"<table><tr><th>Z</th><th>Symbol</th><th>Name</th><th>Weight</th></tr>{body}</table>"


def test_parse_ciaaw_rows_normalizes_spacing_names_and_unavailable_weight():
    source_rows = parse_ciaaw_atomic_weight_rows(
        _fixture_html(
            [
                ("1", "H", "hydrogen", "[1.007 84, 1.008 11]"),
                ("43", "Tc", "technetium", "\u2014"),
            ]
        )
    )
    assert len(source_rows) == 2
    assert source_rows[0].atomic_weight_display == "[1.00784,1.00811]"
    assert source_rows[0].name == "Hydrogen"
    assert source_rows[1].atomic_weight_display == "unavailable"


def test_drift_report_has_no_drift_for_snapshot_fixture_rows():
    snapshot_rows = (
        get_snapshot_record("H"),
        get_snapshot_record("He"),
        get_snapshot_record("Tc"),
        get_snapshot_record("Og"),
    )
    source_rows = tuple(
        SourceSnapshotRow(
            atomic_number=record.atomic_number,
            symbol=record.symbol,
            name=record.name,
            atomic_weight_display=record.atomic_weight_model.display,
        )
        for record in snapshot_rows
    )
    report = build_drift_report(
        source_rows,
        source_url="fixture://ciaaw",
        require_complete_source=False,
    )
    assert report["drift_status"] == "element_snapshot_no_drift"
    assert report["drift_count"] == 0
    assert report["source_count"] == 4
    assert report["local_count"] == 118


def test_drift_report_detects_symbol_name_and_weight_changes():
    report = build_drift_report(
        (
            SourceSnapshotRow(
                atomic_number=1,
                symbol="Hx",
                name="Hydrogenium",
                atomic_weight_display="9.999",
            ),
        ),
        source_url="fixture://ciaaw",
        require_complete_source=False,
    )
    drift_fields = {drift["field"] for drift in report["drifts"]}
    assert report["drift_status"] == "element_snapshot_drift_detected"
    assert report["drift_count"] == 3
    assert drift_fields == {"symbol", "name", "atomic_weight_display"}
    assert all(drift["atomic_number"] == 1 for drift in report["drifts"])


def test_drift_report_requires_complete_source_when_enabled():
    first_two_rows = tuple(
        SourceSnapshotRow(
            atomic_number=record.atomic_number,
            symbol=record.symbol,
            name=record.name,
            atomic_weight_display=record.atomic_weight_model.display,
        )
        for record in list_full_snapshot_records()[:2]
    )
    report = build_drift_report(
        first_two_rows,
        source_url="fixture://ciaaw",
        require_complete_source=True,
    )
    missing_fields = {drift["field"] for drift in report["drifts"]}
    assert report["drift_status"] == "element_snapshot_drift_detected"
    assert report["source_count"] == 2
    assert report["drift_count"] == 116
    assert missing_fields == {"missing_source_record"}
