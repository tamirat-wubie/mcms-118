from dataclasses import replace

import pytest

from mcms.elements import (
    ConfigurationAudit,
    ElementState,
    FrontierSignature,
    TransitionBehaviorKernel,
    build_element_receipt,
    build_snapshot_receipt,
    compare_outer_shell_similarity,
    explain_configuration_choice,
    get_f_block_expansion_profile,
    get_seed_element,
    get_snapshot_record,
    list_f_block_expansion_profiles,
    list_full_snapshot_records,
    list_seed_elements,
    validate_configuration_audit,
    validate_f_block_expansion_profiles,
    validate_full_snapshot,
    validate_seed_pack,
)


def test_seed_pack_contains_first_54_elements_in_order():
    elements = list_seed_elements()
    assert len(elements) == 54
    assert [element.identity.atomic_number for element in elements] == list(range(1, 55))
    assert elements[0].identity.symbol == "H"
    assert elements[-1].identity.symbol == "Xe"


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


def test_invalid_element_reports_validation_errors():
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
    assert result.element_count == 54
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


def test_configuration_audit_accepts_chromium_and_copper_exceptions():
    chromium_audit = ConfigurationAudit(
        source_backed_configuration="[Ar] 3d^5 4s^1",
        simple_aufbau_candidate="[Ar] 3d^4 4s^2",
        is_exception=True,
        exception_reason="half-filled d-shell stabilization pattern",
    )
    copper_audit = ConfigurationAudit(
        source_backed_configuration="[Ar] 3d^10 4s^1",
        simple_aufbau_candidate="[Ar] 3d^9 4s^2",
        is_exception=True,
        exception_reason="filled d-shell stabilization pattern",
    )
    conflicting_audit = ConfigurationAudit(
        source_backed_configuration="[Ar] 3d^5 4s^1",
        simple_aufbau_candidate="[Ar] 3d^4 4s^2",
    )
    assert validate_configuration_audit(chromium_audit) == []
    assert validate_configuration_audit(copper_audit) == []
    assert any("exception flag is false" in error for error in conflicting_audit.validate())


def test_phase_2_d_block_records_use_transition_frontier_kernel():
    d_block_elements = [
        get_seed_element(symbol)
        for symbol in ("Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn")
    ]
    assert all(element.state.frontier_signature is not None for element in d_block_elements)
    assert all(
        element.state.frontier_signature.valence_model == "transition_metal"
        for element in d_block_elements
    )
    assert all(element.state.frontier_signature.d_shell for element in d_block_elements)
    assert all(element.state.transition_behavior_kernel is not None for element in d_block_elements)
    assert all(element.state.validate() == [] for element in d_block_elements)


def test_phase_2_configuration_exceptions_store_candidate_and_source_backed_state():
    chromium = get_seed_element("Cr")
    copper = get_seed_element("Cu")
    iron = get_seed_element("Fe")
    assert chromium.state.configuration_audit.source_backed_configuration == "[Ar] 3d^5 4s^1"
    assert chromium.state.configuration_audit.simple_aufbau_candidate == "[Ar] 3d^4 4s^2"
    assert chromium.state.configuration_audit.is_exception is True
    assert copper.state.configuration_audit.source_backed_configuration == "[Ar] 3d^10 4s^1"
    assert copper.state.configuration_audit.simple_aufbau_candidate == "[Ar] 3d^9 4s^2"
    assert copper.state.configuration_audit.is_exception is True
    assert iron.state.configuration_audit.simple_aufbau_candidate == (
        iron.state.configuration_audit.source_backed_configuration
    )
    assert iron.state.configuration_audit.is_exception is False


def test_phase_2_distinguishes_open_half_filled_and_filled_d_shells():
    chromium = get_seed_element("Cr")
    iron = get_seed_element("Fe")
    copper = get_seed_element("Cu")
    zinc = get_seed_element("Zn")
    assert chromium.state.frontier_signature.d_shell_stability == "half_filled_d_shell"
    assert iron.state.frontier_signature.d_shell_stability == "open_d_shell"
    assert copper.state.frontier_signature.d_shell_stability == "filled_d_shell"
    assert zinc.state.frontier_signature.d_shell_stability == "filled_d_shell"
    assert len(
        {
            chromium.state.frontier_signature.d_shell_stability,
            iron.state.frontier_signature.d_shell_stability,
            copper.state.frontier_signature.d_shell_stability,
        }
    ) == 3


def test_phase_2_period_4_p_block_records_preserve_filled_d_core_context():
    p_block_elements = [
        get_seed_element(symbol) for symbol in ("Ga", "Ge", "As", "Se", "Br", "Kr")
    ]
    assert all(element.state.frontier_signature is not None for element in p_block_elements)
    assert all(element.state.frontier_signature.d_shell == "3d^10" for element in p_block_elements)
    assert all(
        element.state.frontier_signature.valence_model == "period_4_p_block_d_core"
        for element in p_block_elements
    )
    assert get_seed_element("Ga").state.frontier_signature.outer_shell == "4s^2 4p^1"
    assert get_seed_element("Kr").state.frontier_signature.p_shell == "4p^6"
    assert all(element.state.transition_behavior_kernel is None for element in p_block_elements)


def test_phase_2_transition_behavior_flags_are_separate_from_measured_properties():
    cobalt = get_seed_element("Co")
    zinc = get_seed_element("Zn")
    krypton = get_seed_element("Kr")
    assert cobalt.state.transition_behavior_kernel.magnetic_relevance is True
    assert cobalt.state.transition_behavior_kernel.catalytic_relevance is True
    assert zinc.state.transition_behavior_kernel.coordination_relevance is True
    assert zinc.state.transition_behavior_kernel.magnetic_relevance is False
    assert krypton.state.transition_behavior_kernel is None
    assert cobalt.state.first_ionization_energy_source_key == "pubchem_periodic_table_properties"


def test_phase_2_explains_chromium_configuration_exception():
    reasoning = explain_configuration_choice("Cr").to_dict()
    assert reasoning["reasoning_status"] == "configuration_choice_explained"
    assert reasoning["subject_symbols"] == ["Cr"]
    assert reasoning["evidence"]["configuration_audit"]["simple_aufbau_candidate"] == (
        "[Ar] 3d^4 4s^2"
    )
    assert reasoning["evidence"]["configuration_audit"]["source_backed_configuration"] == (
        "[Ar] 3d^5 4s^1"
    )
    assert reasoning["evidence"]["identity"]["proton_count"] == 24
    assert "simple Aufbau filling as a candidate" in reasoning["answer_lines"][0]


def test_phase_2_compares_copper_and_potassium_outer_shell_similarity():
    reasoning = compare_outer_shell_similarity("Cu", "K").to_dict()
    assert reasoning["reasoning_status"] == "outer_shell_similarity_explained"
    assert reasoning["subject_symbols"] == ["Cu", "K"]
    assert reasoning["evidence"]["surface_similarity"] is True
    assert reasoning["evidence"]["deep_similarity"] is False
    assert reasoning["evidence"]["Cu"]["d_shell"] == "3d^10"
    assert reasoning["evidence"]["K"]["d_shell"] is None
    assert reasoning["answer_lines"][0] == "Partially, but not deeply."


def test_phase_3_f_block_profiles_are_bounded_snapshot_overlays():
    profiles = list_f_block_expansion_profiles()
    validation = validate_f_block_expansion_profiles(profiles)
    lanthanum = get_f_block_expansion_profile("La")
    promethium = get_f_block_expansion_profile("Pm")
    uranium = get_f_block_expansion_profile("U")
    assert len(profiles) == 30
    assert validation.validation_status == "f_block_expansion_profiles_validated"
    assert validation.lanthanide_count == 15
    assert validation.actinide_count == 15
    assert lanthanum.series == "lanthanide"
    assert lanthanum.f_shell_family == "4f"
    assert lanthanum.group is None
    assert promethium.radioactive_decay_relevance is True
    assert promethium.nuclear_state_extension_required is True
    assert uranium.series == "actinide"
    assert uranium.f_shell_family == "5f"
    assert uranium.actinide_instability_relevance is True


def test_phase_3_f_block_validation_rejects_fractured_profile():
    uranium = get_f_block_expansion_profile("U")
    fractured_profile = replace(
        uranium,
        series="lanthanide",
        f_shell_family="4f",
        actinide_instability_relevance=True,
    )
    validation = validate_f_block_expansion_profiles((fractured_profile,))
    errors = fractured_profile.validate()
    assert validation.validation_status == "f_block_expansion_profiles_rejected"
    assert validation.invalid_profiles == ("U",)
    assert any("actinide instability flag" in error for error in errors)


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
        frontier_signature=FrontierSignature(
            outer_shell="4s^2",
            d_shell="3d^10",
            valence_model="transition_metal",
            d_shell_stability="filled_d_shell",
        ),
        configuration_audit=ConfigurationAudit(
            source_backed_configuration="[Ar] 3d^10 4s^2",
            simple_aufbau_candidate="[Ar] 3d^10 4s^2",
        ),
        transition_behavior_kernel=TransitionBehaviorKernel(coordination_relevance=True),
    )
    errors = broken_zinc.validate()
    assert any("[1, 12]" in error for error in errors)
    assert valid_state.validate() == []
    assert zinc.state.block == "d"


def test_level_2_chemistry_boundaries_validate_oxidation_and_electronegativity_fields():
    zinc = get_seed_element("Zn")
    valid_level_2_state = replace(
        zinc.state,
        oxidation_states=(-2, 0, 2),
        electronegativity_scale="pauling",
        electronegativity_value=1.65,
        electronegativity_source_key="level_2_reference_seed",
        data_level=2,
    )
    duplicate_oxidation_state = replace(valid_level_2_state, oxidation_states=(0, 2, 2))
    out_of_range_oxidation_state = replace(valid_level_2_state, oxidation_states=(-9, 0, 2))
    incomplete_electronegativity = replace(
        valid_level_2_state,
        electronegativity_source_key=None,
    )
    out_of_range_electronegativity = replace(
        valid_level_2_state,
        electronegativity_value=5.1,
    )
    assert valid_level_2_state.validate() == []
    assert any("duplicates" in error for error in duplicate_oxidation_state.validate())
    assert any("[-8, 9]" in error for error in out_of_range_oxidation_state.validate())
    assert any("source key is required" in error for error in incomplete_electronegativity.validate())
    assert any("[0.0, 5.0]" in error for error in out_of_range_electronegativity.validate())


def test_level_2_chemistry_boundaries_validate_ionization_and_bond_tendency_fields():
    zinc = get_seed_element("Zn")
    valid_level_2_state = replace(
        zinc.state,
        first_ionization_energy_ev=9.39,
        first_ionization_energy_source_key="level_2_reference_seed",
        bond_tendency_tags=("metallic_bonding", "coordination_complex"),
        bond_tendency_source_key="level_2_reference_seed",
        data_level=2,
    )
    missing_ionization_source = replace(
        valid_level_2_state,
        first_ionization_energy_source_key=None,
    )
    out_of_range_ionization = replace(
        valid_level_2_state,
        first_ionization_energy_ev=30.1,
    )
    duplicate_bond_tags = replace(
        valid_level_2_state,
        bond_tendency_tags=("metallic_bonding", "metallic_bonding"),
    )
    unknown_bond_tag = replace(
        valid_level_2_state,
        bond_tendency_tags=("unsupported_bond_claim",),
    )
    missing_bond_source = replace(
        valid_level_2_state,
        bond_tendency_source_key=None,
    )
    source_without_bond_tags = replace(
        valid_level_2_state,
        bond_tendency_tags=(),
    )
    assert valid_level_2_state.validate() == []
    assert any("source key is required" in error for error in missing_ionization_source.validate())
    assert any("[0.0, 30.0] eV" in error for error in out_of_range_ionization.validate())
    assert any("duplicates" in error for error in duplicate_bond_tags.validate())
    assert any("bond tendency tag is unknown" in error for error in unknown_bond_tag.validate())
    assert any("source key is required" in error for error in missing_bond_source.validate())
    assert any("tags are required" in error for error in source_without_bond_tags.validate())


def test_first_54_seed_records_carry_source_backed_level_2_chemistry_values():
    source_key = "pubchem_periodic_table_properties"
    seed_symbols = [element.identity.symbol for element in list_seed_elements()]
    hydrogen = get_seed_element("H")
    oxygen = get_seed_element("O")
    chlorine = get_seed_element("Cl")
    argon = get_seed_element("Ar")
    calcium = get_seed_element("Ca")
    titanium = get_seed_element("Ti")
    zinc = get_seed_element("Zn")
    krypton = get_seed_element("Kr")
    rubidium = get_seed_element("Rb")
    xenon = get_seed_element("Xe")
    assert len(seed_symbols) == 54
    assert all(get_seed_element(symbol).state.data_level == 2 for symbol in seed_symbols)
    assert all(source_key in get_seed_element(symbol).source_keys() for symbol in seed_symbols)
    assert all(
        get_seed_element(symbol).state.bond_tendency_source_key == source_key
        for symbol in seed_symbols
    )
    assert hydrogen.state.oxidation_states == (1, -1)
    assert hydrogen.state.electronegativity_value == 2.20
    assert oxygen.state.oxidation_states == (-2,)
    assert oxygen.state.electronegativity_value == 3.44
    assert chlorine.state.oxidation_states == (7, 5, 1, -1)
    assert chlorine.state.electronegativity_value == 3.16
    assert argon.state.oxidation_states == (0,)
    assert argon.state.electronegativity_value is None
    assert calcium.state.oxidation_states == (2,)
    assert calcium.state.electronegativity_value == 1.00
    assert titanium.state.oxidation_states == (4, 3, 2)
    assert titanium.state.electronegativity_value == 1.54
    assert zinc.state.oxidation_states == (2,)
    assert zinc.state.electronegativity_value == 1.65
    assert zinc.state.first_ionization_energy_ev == 9.394
    assert zinc.state.first_ionization_energy_source_key == source_key
    assert zinc.state.bond_tendency_tags == ("metallic_bonding", "coordination_complex")
    assert zinc.state.bond_tendency_source_key == source_key
    assert krypton.state.oxidation_states == (0,)
    assert krypton.state.electronegativity_value == 3.00
    assert krypton.state.first_ionization_energy_ev == 14.000
    assert krypton.state.bond_tendency_tags == ("noble_gas_low_reactivity",)
    assert rubidium.state.oxidation_states == (1,)
    assert rubidium.state.electronegativity_value == 0.82
    assert rubidium.state.first_ionization_energy_ev == 4.177
    assert xenon.state.oxidation_states == (0,)
    assert xenon.state.electronegativity_value == 2.60
    assert xenon.state.first_ionization_energy_ev == 12.130
    assert all(get_seed_element(symbol).validate() == [] for symbol in seed_symbols)


def test_first_54_bond_tendency_tags_are_derived_from_pubchem_group_block_classes():
    hydrogen = get_seed_element("H")
    fluorine = get_seed_element("F")
    calcium = get_seed_element("Ca")
    zinc = get_seed_element("Zn")
    silicon = get_seed_element("Si")
    krypton = get_seed_element("Kr")
    zirconium = get_seed_element("Zr")
    iodine = get_seed_element("I")
    assert hydrogen.state.bond_tendency_tags == ("covalent_bonding", "molecular_covalent")
    assert fluorine.state.bond_tendency_tags == (
        "covalent_bonding",
        "ionic_bonding",
        "molecular_covalent",
    )
    assert calcium.state.bond_tendency_tags == ("metallic_bonding", "ionic_bonding")
    assert zinc.state.bond_tendency_tags == ("metallic_bonding", "coordination_complex")
    assert silicon.state.bond_tendency_tags == ("covalent_bonding", "network_covalent")
    assert krypton.state.bond_tendency_tags == ("noble_gas_low_reactivity",)
    assert zirconium.state.bond_tendency_tags == ("metallic_bonding", "coordination_complex")
    assert iodine.state.bond_tendency_tags == (
        "covalent_bonding",
        "ionic_bonding",
        "molecular_covalent",
    )


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
    assert technetium.level_1_seed_available is True
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
    assert result.level_1_seed_count == 54
    assert result.unavailable_weight_count == 34
    with pytest.raises(KeyError):
        get_snapshot_record("Mx")
