import pytest

from mcms.elements import (
    find_behavior_tag_overlay_record,
    list_behavior_tag_overlay_records,
    validate_behavior_tag_overlay_records,
)


def test_behavior_tag_overlay_covers_cs_through_rn():
    records = list_behavior_tag_overlay_records()
    result = validate_behavior_tag_overlay_records(records)
    assert len(records) == 32
    assert result["validation_status"] == "behavior_tag_overlay_records_validated"
    assert result["record_count"] == 32
    assert result["variable_oxidation_tag_count"] == 15
    assert result["coordination_relevance_count"] == 9
    assert result["f_orbital_relevance_count"] == 15
    assert result["low_reactivity_baseline_count"] == 1
    assert records[0].symbol == "Cs"
    assert records[-1].symbol == "Rn"


def test_behavior_tags_are_controlled_inference_from_evidence():
    cesium = find_behavior_tag_overlay_record("Cs")
    gold = find_behavior_tag_overlay_record("Au")
    astatine = find_behavior_tag_overlay_record("At")
    radon = find_behavior_tag_overlay_record("Rn")
    assert cesium.inferred_behavior_tags == (
        "alkali_metal",
        "s_block_metal",
        "one_electron_loss_pathway",
        "metallic_bonding_relevance",
    )
    assert "period_6_transition_metal" in gold.inferred_behavior_tags
    assert "coordination_relevance" in gold.inferred_behavior_tags
    assert "filled_d_shell_context" in gold.inferred_behavior_tags
    assert "halogen" in astatine.inferred_behavior_tags
    assert "negative_oxidation_pathway" in astatine.inferred_behavior_tags
    assert "noble_gas" in radon.inferred_behavior_tags
    assert "low_reactivity_baseline" in radon.inferred_behavior_tags


def test_behavior_tags_reject_out_of_span_lookup():
    with pytest.raises(KeyError):
        find_behavior_tag_overlay_record("Xe")
    with pytest.raises(KeyError):
        find_behavior_tag_overlay_record(54)
    with pytest.raises(KeyError):
        find_behavior_tag_overlay_record("Xx")
