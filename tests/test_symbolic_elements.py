from dataclasses import replace

import pytest

from mcms.elements import (
    build_element_receipt,
    get_seed_element,
    list_seed_elements,
    validate_seed_pack,
)


def test_seed_pack_contains_first_20_elements_in_order():
    elements = list_seed_elements()
    assert len(elements) == 20
    assert [element.identity.atomic_number for element in elements] == list(range(1, 21))
    assert elements[0].identity.symbol == "H"
    assert elements[-1].identity.symbol == "Ca"


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
    assert result.element_count == 20
    assert result.relation_edge_count > 0
    with pytest.raises(KeyError):
        get_seed_element("Xx")
