import pytest

from mcms.elements import (
    find_relation_overlay_record,
    list_relation_overlay_records,
    validate_relation_overlay_records,
)


def test_relation_overlay_covers_cs_through_rn():
    records = list_relation_overlay_records()
    result = validate_relation_overlay_records(records)
    assert len(records) == 32
    assert result["validation_status"] == "relation_overlay_records_validated"
    assert result["record_count"] == 32
    assert result["edge_count"] > 0
    assert result["edge_counts_by_type"]["same_period"] == 32 * 31
    assert result["edge_counts_by_type"]["same_frontier_model"] > 0
    assert result["edge_counts_by_type"]["shared_oxidation_state"] > 0
    assert result["edge_counts_by_type"]["shared_behavior_tag"] > 0
    assert records[0].symbol == "Cs"
    assert records[-1].symbol == "Rn"


def test_relation_overlay_generates_multiple_evidence_based_relations():
    gold = find_relation_overlay_record("Au")
    edge_types = {edge.relation_type for edge in gold.relation_edges}
    shared_behavior_targets = {
        edge.target_symbol for edge in gold.relation_edges if edge.relation_type == "shared_behavior_tag"
    }
    assert "same_period" in edge_types
    assert "same_block" in edge_types
    assert "same_frontier_model" in edge_types
    assert "shared_oxidation_state" in edge_types
    assert "shared_behavior_tag" in edge_types
    assert "Pt" in shared_behavior_targets
    assert gold.validate() == []


def test_relation_overlay_rejects_out_of_span_lookup():
    with pytest.raises(KeyError):
        find_relation_overlay_record("Xe")
    with pytest.raises(KeyError):
        find_relation_overlay_record(54)
    with pytest.raises(KeyError):
        find_relation_overlay_record("Xx")
