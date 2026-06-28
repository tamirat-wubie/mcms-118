import pytest

from mcms.elements import (
    get_f_block_expansion_profile,
    list_f_block_expansion_profiles,
    validate_f_block_expansion_profiles,
)


def test_phase_3_f_block_profiles_cover_lanthanides_and_actinides():
    profiles = list_f_block_expansion_profiles()
    result = validate_f_block_expansion_profiles(profiles)
    assert len(profiles) == 30
    assert result.validation_status == "f_block_expansion_profiles_validated"
    assert result.lanthanide_count == 15
    assert result.actinide_count == 15
    assert [profile.symbol for profile in profiles[:3]] == ["La", "Ce", "Pr"]
    assert [profile.symbol for profile in profiles[-3:]] == ["Md", "No", "Lr"]


def test_phase_3_lanthanide_profile_keeps_contraction_as_relevance_flag():
    lanthanum = get_f_block_expansion_profile("La")
    lutetium = get_f_block_expansion_profile("Lu")
    assert lanthanum.series == "lanthanide"
    assert lanthanum.f_shell_family == "4f"
    assert lanthanum.lanthanide_contraction_relevance is True
    assert lanthanum.radioactive_decay_relevance is False
    assert lanthanum.group is None
    assert lutetium.standard_atomic_weight_status == "single"


def test_phase_3_promethium_marks_radioactive_boundary_without_half_life_claim():
    promethium = get_f_block_expansion_profile("Pm")
    assert promethium.series == "lanthanide"
    assert promethium.standard_atomic_weight_status == "unavailable"
    assert promethium.radioactive_decay_relevance is True
    assert promethium.nuclear_state_extension_required is True
    assert promethium.heavy_element_uncertainty is True
    assert any("without assigning isotope-specific half-life" in note for note in promethium.notes)


def test_phase_3_actinide_profile_marks_instability_uncertainty_and_relativity():
    uranium = get_f_block_expansion_profile("U")
    lawrencium = get_f_block_expansion_profile("Lr")
    assert uranium.series == "actinide"
    assert uranium.f_shell_family == "5f"
    assert uranium.actinide_instability_relevance is True
    assert uranium.radioactive_decay_relevance is True
    assert uranium.heavy_element_uncertainty is True
    assert uranium.standard_atomic_weight_status == "single"
    assert lawrencium.standard_atomic_weight_status == "unavailable"
    assert lawrencium.relativistic_effect_relevance is True


def test_phase_3_rejects_non_f_block_lookup():
    with pytest.raises(KeyError):
        get_f_block_expansion_profile("Kr")
    with pytest.raises(KeyError):
        get_f_block_expansion_profile(36)
    with pytest.raises(KeyError):
        get_f_block_expansion_profile("Xx")
