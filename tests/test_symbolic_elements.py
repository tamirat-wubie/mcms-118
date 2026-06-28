from dataclasses import replace

import pytest

from mcms.elements import (
    ElementState,
    build_element_receipt,
    build_snapshot_receipt,
    get_seed_element,
    get_snapshot_record,
    list_full_snapshot_records,
    list_seed_elements,
    validate_full_snapshot,
    validate_seed_pack,
)


def test_seed_pack_contains_first_36_elements_in_order():
    elements = list_seed_elements()
    assert len(elements) == 36
    assert [element.identity.atomic_number for element in elements] == list(range(1, 37))
    assert elements[0].identity.symbol == "H"
    assert elements[-1].identity.symbol == "Kr"


def test_hydrogen_identity_state_and_sources_are_validated():
    hydrogen = get_seed_element("H")
    receipt = build_element_receipt(hydrogen)
    assert hydrogen.validate() == []
    assert hydrogen.identity.proton_count == 1
    assert hydrogen.state.neutral_electron_configuration == "1s^1"
    assert receipt["validation_status"] == "element_seed_validated"
    assert "nist_electronic_configurations" in receipt["source_keys"]


def test_seed_pack_relation_graph_has_period_group_and_block_edges():
    sodium = get_seed_element("Na")
    relation_types = {edge.relation_type for edge in sodium.state.relation_edges}
    target_symbols = {edge.target_symbol for edge in sodium.state.relation_edges}
    assert "same_group" in relation_types
    assert "same_period" in relation_types
    assert "same_block" in relation_types
    assert {"H", "Li", "K", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"} <= target_symbols


def test_invalid_element_reports_governance_errors():
    carbon = get_seed_element("C")
    broken_identity = replace(carbon.identity, proton_count=7)
    broken_state = replace(carbon.state, neutral_electron_count=7, relation_edges=())
    broken_history = replace(carbon.history, source_references=())
    broken_carbon = replace(
        carbon,
        identity=broken_identity,
        state=broken_state,
        history=broken_history,
    )
    errors = broken_carbon.validate()
    assert any("atomic number must equal proton count" in error for error in errors)
    assert any("neutral electron count must equal atomic number" in error for error in errors)
    assert any("at least one source reference is required" in error for error in errors)
    assert build_element_receipt(broken_carbon)["validation_status"] == "element_seed_rejected"


def test_element_lookup_and_seed_pack_validation_reject_unknowns():
    result = validate_seed_pack()
    assert result.validation_status == "element_seed_pack_validated"
    assert result.element_count == 36
    assert result.relation_edge_count > 0
    with pytest.raises(KeyError):
        get_seed_element("Xx")


def test_transition_seed_records_preserve_d_block_exceptions():
    chromium = get_seed_element("Cr")
    copper = get_seed_element("Cu")
    zinc = get_seed_element("Zn")
    assert chromium.state.neutral_electron_configuration == "[Ar] 3d^5 4s^1"
    assert copper.state.neutral_electron_configuration == "[Ar] 3d^10 4s^1"
    assert zinc.state.valence_shell == "3d 4s"
    assert zinc.state.valence_electrons == 12
    assert zinc.validate() == []


def test_d_block_valence_validation_rejects_out_of_range_seed_state():
    zinc = get_seed_element("Zn")
    broken_state = replace(zinc.state, valence_electrons=13)
    broken_zinc = replace(zinc, state=broken_state)
    valid_state = ElementState(
        neutral_electron_count=30,
        neutral_electron_configuration="[Ar] 3d^10 4s^2",
        first_cation_configuration="[Ar] 3d^10 4s^1",
        period=4,
        group=12,
        block="d",
        valence_shell="3d 4s",
        valence_electrons=12,
        atomic_weight_model=zinc.state.atomic_weight_model,
    )
    errors = broken_zinc.validate()
    assert any("[1, 12]" in error for error in errors)
    assert valid_state.validate() == []
    assert zinc.state.block == "d"


def test_full_snapshot_contains_all_118_elements_in_order():
    records = list_full_snapshot_records()
    result = validate_full_snapshot(records)
    assert len(records) == 118
    assert [record.atomic_number for record in records] == list(range(1, 119))
    assert records[0].symbol == "H"
    assert records[-1].symbol == "Og"
    assert result.validation_status == "full_element_snapshot_validated"


def test_full_snapshot_keeps_unavailable_atomic_weights_explicit():
    technetium = get_snapshot_record("Tc")
    oganesson = get_snapshot_record(118)
    assert technetium.atomic_weight_model.model_type == "unavailable"
    assert oganesson.atomic_weight_model.model_type == "unavailable"
    assert technetium.level_1_seed_available is False
    assert oganesson.period == 7
    assert oganesson.group == 18


def test_snapshot_receipt_and_level_1_seed_linkage():
    hydrogen_snapshot = get_snapshot_record("Hydrogen")
    krypton_snapshot = get_snapshot_record("Kr")
    seed_symbols = {element.identity.symbol for element in list_seed_elements()}
    receipt = build_snapshot_receipt(hydrogen_snapshot)
    assert hydrogen_snapshot.level_1_seed_available is True
    assert krypton_snapshot.level_1_seed_available is True
    assert hydrogen_snapshot.snapshot_status == "level_1_seed_available"
    assert krypton_snapshot.snapshot_status == "level_1_seed_available"
    assert all(get_snapshot_record(symbol).level_1_seed_available for symbol in seed_symbols)
    assert receipt["validation_status"] == "element_snapshot_validated"
    assert "ciaaw_standard_atomic_weights_2024" in receipt["source_keys"]


def test_full_snapshot_rejects_unknown_lookup():
    result = validate_full_snapshot()
    assert result.element_count == 118
    assert result.level_1_seed_count == 36
    assert result.unavailable_weight_count == 34
    with pytest.raises(KeyError):
        get_snapshot_record("Mx")
