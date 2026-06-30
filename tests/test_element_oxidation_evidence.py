import pytest

from mcms.elements import (
    find_oxidation_state_evidence_record,
    list_oxidation_state_evidence_records,
    validate_oxidation_state_evidence_records,
)


def test_oxidation_state_evidence_covers_cs_through_rn():
    records = list_oxidation_state_evidence_records()
    result = validate_oxidation_state_evidence_records(records)
    assert len(records) == 32
    assert result["validation_status"] == "oxidation_state_evidence_records_validated"
    assert result["record_count"] == 32
    assert result["variable_oxidation_state_count"] == 15
    assert result["negative_oxidation_state_count"] == 1
    assert result["zero_oxidation_state_count"] == 1
    assert records[0].symbol == "Cs"
    assert records[-1].symbol == "Rn"


def test_oxidation_state_evidence_preserves_pubchem_group_blocks():
    cesium = find_oxidation_state_evidence_record("Cs")
    cerium = find_oxidation_state_evidence_record("Ce")
    gold = find_oxidation_state_evidence_record("Au")
    astatine = find_oxidation_state_evidence_record("At")
    radon = find_oxidation_state_evidence_record("Rn")
    assert cesium.oxidation_states == (1,)
    assert cesium.pubchem_group_block == "Alkali metal"
    assert cerium.oxidation_states == (4, 3)
    assert cerium.pubchem_group_block == "Lanthanide"
    assert gold.oxidation_states == (3, 1)
    assert gold.pubchem_group_block == "Transition metal"
    assert astatine.oxidation_states == (7, 5, 3, 1, -1)
    assert astatine.pubchem_group_block == "Halogen"
    assert radon.oxidation_states == (0,)
    assert radon.pubchem_group_block == "Noble gas"


def test_oxidation_state_evidence_rejects_out_of_span_lookup():
    with pytest.raises(KeyError):
        find_oxidation_state_evidence_record("Xe")
    with pytest.raises(KeyError):
        find_oxidation_state_evidence_record(54)
    with pytest.raises(KeyError):
        find_oxidation_state_evidence_record("Xx")
