import pytest

from mcms.elements import (
    get_period_5_level_2_profile,
    list_period_5_level_2_profiles,
    validate_period_5_level_2_profiles,
)


def test_period_5_level_2_profiles_cover_rubidium_through_xenon():
    profiles = list_period_5_level_2_profiles()
    result = validate_period_5_level_2_profiles(profiles)
    assert len(profiles) == 18
    assert result.validation_status == "period_5_level_2_snapshot_profiles_validated"
    assert result.atomic_number_span == (37, 54)
    assert [profile.symbol for profile in profiles[:3]] == ["Rb", "Sr", "Y"]
    assert [profile.symbol for profile in profiles[-3:]] == ["Te", "I", "Xe"]


def test_period_5_level_2_profile_keeps_snapshot_promotion_boundary():
    rubidium = get_period_5_level_2_profile("Rb")
    zirconium = get_period_5_level_2_profile("Zr")
    assert rubidium.atomic_number == 37
    assert rubidium.source_scope == "snapshot_level_2_period_5"
    assert rubidium.promotion_status == "snapshot_level_2_chemistry_profile"
    assert rubidium.oxidation_states == (1,)
    assert rubidium.bond_tendency_tags == ("metallic_bonding", "ionic_bonding")
    assert zirconium.pubchem_group_block == "Transition metal"
    assert zirconium.bond_tendency_tags == ("metallic_bonding", "coordination_complex")


def test_period_5_level_2_profile_preserves_radioactive_and_noble_gas_boundaries():
    technetium = get_period_5_level_2_profile("Tc")
    xenon = get_period_5_level_2_profile("Xe")
    assert technetium.oxidation_states == (7, 6, 4)
    assert technetium.electronegativity_value == 1.9
    assert technetium.first_ionization_energy_ev == 7.28
    assert technetium.validate() == []
    assert xenon.oxidation_states == (0,)
    assert xenon.pubchem_group_block == "Noble gas"
    assert xenon.bond_tendency_tags == ("noble_gas_low_reactivity",)


def test_period_5_level_2_rejects_non_period_5_lookup():
    with pytest.raises(KeyError):
        get_period_5_level_2_profile("Kr")
    with pytest.raises(KeyError):
        get_period_5_level_2_profile("Cs")
    with pytest.raises(KeyError):
        get_period_5_level_2_profile("Xx")
