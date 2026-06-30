import json

import pytest

from mcms.cli import cmd_elements
from mcms.elements import (
    build_atom_behavior_profile,
    find_atom_behavior_profile,
    list_atom_behavior_profiles,
    validate_atom_behavior_profiles,
)


def test_atom_behavior_profiles_preserve_identity_isotope_and_electron_rules():
    profiles = list_atom_behavior_profiles()
    validation = validate_atom_behavior_profiles(profiles)
    carbon_14 = build_atom_behavior_profile("C", 14)

    assert validation["validation_status"] == "atom_behavior_profiles_validated"
    assert validation["profile_count"] == 13
    assert validation["neutral_profile_count"] == 13
    assert validation["stable_isotope_profile_count"] == 11
    assert validation["radioisotope_profile_count"] == 2
    assert carbon_14.profile_id == (
        "MSPEE-Z006-C-isotope-14-charge-neutral-0-atom-behavior-v2"
    )
    assert carbon_14.proton_count == 6
    assert carbon_14.neutron_count == 8
    assert carbon_14.mass_number == 14
    assert carbon_14.electron_count == 6
    assert carbon_14.charge == 0
    assert carbon_14.validate() == []


def test_atom_behavior_profile_carries_bounded_quantum_force_and_matter_context():
    carbon_14 = build_atom_behavior_profile("C", 14)

    assert carbon_14.isotope_evidence_status == "radioisotope_evidence"
    assert "decay_mode=beta_minus" in carbon_14.nuclear_behavior_basis
    assert "weak_decay_context=beta_minus" in carbon_14.force_layer_basis
    assert "standard_state_solid" in carbon_14.matter_behavior_tags
    assert "profile does not solve electron wavefunctions" in carbon_14.non_claims
    assert "exact wavefunction is outside current claim boundary" in carbon_14.quantum_state_basis
    assert "pubchem_periodic_table_properties" in carbon_14.source_keys


def test_atom_behavior_profile_can_project_charged_atom_without_changing_identity():
    charged_carbon_14 = build_atom_behavior_profile("C", 14, charge=1)

    assert charged_carbon_14.profile_id == (
        "MSPEE-Z006-C-isotope-14-charge-plus-1-atom-behavior-v2"
    )
    assert charged_carbon_14.proton_count == 6
    assert charged_carbon_14.neutron_count == 8
    assert charged_carbon_14.electron_count == 5
    assert "charge=1" in charged_carbon_14.electron_behavior_basis
    assert "electron_count=5" in charged_carbon_14.electron_behavior_basis
    assert charged_carbon_14.validate() == []


def test_atom_behavior_lookup_requires_mass_number_when_symbol_is_ambiguous():
    with pytest.raises(KeyError, match="ambiguous"):
        find_atom_behavior_profile("C")

    with pytest.raises(KeyError, match="unknown isotope evidence record"):
        build_atom_behavior_profile("C", 11)


def test_element_cli_prints_atom_behavior_profile(capsys):
    cmd_elements(
        symbol="C",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        isotope_mass=14,
        atom_behavior=True,
    )
    output = json.loads(capsys.readouterr().out)

    assert output["validation"]["profile_count"] == 1
    assert output["profiles"][0]["symbol"] == "C"
    assert output["profiles"][0]["neutron_count"] == 8
    assert output["profiles"][0]["electron_count"] == 6
