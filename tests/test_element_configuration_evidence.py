import pytest

from mcms.elements import (
    find_configuration_evidence_record,
    list_configuration_evidence_records,
    validate_configuration_evidence_records,
)


def test_configuration_evidence_covers_cs_through_rn():
    records = list_configuration_evidence_records()
    result = validate_configuration_evidence_records(records)
    assert len(records) == 32
    assert result["validation_status"] == "configuration_evidence_records_validated"
    assert result["record_count"] == 32
    assert result["exception_count"] == 2
    assert result["special_first_cation_literature_count"] == 8
    assert records[0].symbol == "Cs"
    assert records[-1].symbol == "Rn"


def test_configuration_evidence_marks_platinum_and_gold_exceptions():
    platinum = find_configuration_evidence_record("Pt")
    gold = find_configuration_evidence_record("Au")
    assert platinum.neutral_configuration == "[Xe] 4f^14 5d^9 6s^1"
    assert platinum.configuration_audit.is_exception is True
    assert platinum.configuration_audit.simple_aufbau_candidate == "[Xe] 4f^14 5d^8 6s^2"
    assert gold.neutral_configuration == "[Xe] 4f^14 5d^10 6s^1"
    assert gold.configuration_audit.is_exception is True
    assert gold.configuration_audit.exception_reason == "filled 5d-shell stabilization pattern"


def test_configuration_evidence_preserves_special_first_cation_literature_notes():
    tantalum = find_configuration_evidence_record("Ta")
    astatine = find_configuration_evidence_record("At")
    cesium = find_configuration_evidence_record("Cs")
    assert tantalum.first_cation_source_note is not None
    assert astatine.first_cation_source_note is not None
    assert cesium.first_cation_source_note is None
    assert astatine.first_cation_configuration == "[Xe] 4f^14 5d^10 6s^2 6p^4"
    assert astatine.validate() == []


def test_configuration_evidence_rejects_out_of_span_lookup():
    with pytest.raises(KeyError):
        find_configuration_evidence_record("Xe")
    with pytest.raises(KeyError):
        find_configuration_evidence_record(54)
    with pytest.raises(KeyError):
        find_configuration_evidence_record("Xx")
