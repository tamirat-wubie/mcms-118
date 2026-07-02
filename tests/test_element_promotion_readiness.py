import pytest

from mcms.elements import (
    get_cs_rn_promotion_readiness_profile,
    list_cs_rn_promotion_readiness_profiles,
    validate_cs_rn_promotion_readiness_profiles,
)


def test_cs_rn_promotion_readiness_profiles_cover_atomic_span():
    profiles = list_cs_rn_promotion_readiness_profiles()
    result = validate_cs_rn_promotion_readiness_profiles(profiles)
    assert len(profiles) == 32
    assert result.validation_status == "cs_rn_promotion_readiness_profiles_validated"
    assert result.profile_count == 32
    assert result.atomic_number_span == (55, 86)
    assert result.blocked_count == 0
    assert result.ready_count == 32
    assert [profile.symbol for profile in profiles[:3]] == ["Cs", "Ba", "La"]
    assert [profile.symbol for profile in profiles[-3:]] == ["Po", "At", "Rn"]


def test_cs_rn_readiness_separates_available_and_missing_evidence():
    cesium = get_cs_rn_promotion_readiness_profile("Cs")
    assert cesium.atomic_number == 55
    assert cesium.snapshot_available is True
    assert cesium.level_1_seed_available is False
    assert cesium.physical_property_evidence_available is True
    assert cesium.f_block_profile_available is False
    assert cesium.readiness_status == "promotion_ready"
    assert "full_118_identity_snapshot" in cesium.available_evidence
    assert "nist_configuration_evidence" in cesium.available_evidence
    assert "nist_neutral_electron_configuration" not in cesium.required_missing_evidence
    assert "nist_first_cation_configuration" not in cesium.required_missing_evidence
    assert "configuration_audit" not in cesium.required_missing_evidence
    assert "frontier_valence_signature" in cesium.available_evidence
    assert "frontier_signature" not in cesium.required_missing_evidence
    assert "valence_shell_signature" not in cesium.required_missing_evidence
    assert "oxidation_state_evidence" in cesium.available_evidence
    assert "oxidation_state_evidence" not in cesium.required_missing_evidence
    assert "level_1_behavior_tags" in cesium.available_evidence
    assert "relation_edges" in cesium.available_evidence
    assert "relation_edges" not in cesium.required_missing_evidence
    assert "level_1_behavior_tags" not in cesium.required_missing_evidence
    assert cesium.readiness_status == "promotion_ready"


def test_cs_rn_readiness_marks_lanthanide_profile_without_promotion():
    lanthanum = get_cs_rn_promotion_readiness_profile("La")
    assert lanthanum.atomic_number == 57
    assert lanthanum.f_block_profile_available is True
    assert lanthanum.physical_property_evidence_available is True
    assert "f_block_expansion_profile" in lanthanum.available_evidence
    assert "nist_configuration_evidence" in lanthanum.available_evidence
    assert "frontier_valence_signature" in lanthanum.available_evidence
    assert "configuration_audit" not in lanthanum.required_missing_evidence
    assert "valence_shell_signature" not in lanthanum.required_missing_evidence
    assert "oxidation_state_evidence" not in lanthanum.required_missing_evidence
    assert "level_1_behavior_tags" not in lanthanum.required_missing_evidence
    assert "relation_edges" in lanthanum.available_evidence
    assert "relation_edges" not in lanthanum.required_missing_evidence
    assert lanthanum.readiness_status == "promotion_ready"
    assert lanthanum.promotion_blockers == ()


def test_cs_rn_readiness_keeps_resolved_source_gap_visible():
    astatine = get_cs_rn_promotion_readiness_profile("At")
    assert astatine.atomic_number == 85
    assert astatine.physical_property_evidence_available is True
    assert astatine.unresolved_physical_property_evidence_available is True
    assert "physical_property_evidence" in astatine.available_evidence
    assert "unresolved_physical_property_evidence" in astatine.available_evidence
    assert "relation_edges" in astatine.available_evidence
    assert astatine.required_missing_evidence == ()
    assert astatine.promotion_blockers == ()
    assert astatine.readiness_status == "promotion_ready"
    assert "secondary_physical_property_evidence_resolves_source_gap" in astatine.notes
    assert astatine.validate() == []


def test_cs_rn_readiness_rejects_out_of_span_lookup():
    with pytest.raises(KeyError):
        get_cs_rn_promotion_readiness_profile("Xe")
    with pytest.raises(KeyError):
        get_cs_rn_promotion_readiness_profile(54)
    with pytest.raises(KeyError):
        get_cs_rn_promotion_readiness_profile("Xx")
