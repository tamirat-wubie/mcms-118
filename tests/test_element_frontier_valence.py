import pytest

from mcms.elements import (
    find_frontier_valence_signature_record,
    list_frontier_valence_signature_records,
    validate_frontier_valence_signature_records,
)


def test_frontier_valence_records_cover_cs_through_rn():
    records = list_frontier_valence_signature_records()
    result = validate_frontier_valence_signature_records(records)
    assert len(records) == 32
    assert result["validation_status"] == "frontier_valence_signature_records_validated"
    assert result["record_count"] == 32
    assert result["s_block_count"] == 2
    assert result["lanthanide_count"] == 15
    assert result["transition_count"] == 9
    assert result["p_block_count"] == 6
    assert records[0].symbol == "Cs"
    assert records[-1].symbol == "Rn"


def test_frontier_valence_models_s_block_lanthanide_transition_and_p_block():
    cesium = find_frontier_valence_signature_record("Cs")
    gadolinium = find_frontier_valence_signature_record("Gd")
    gold = find_frontier_valence_signature_record("Au")
    astatine = find_frontier_valence_signature_record("At")
    assert cesium.frontier_model == "period_6_s_block"
    assert cesium.outer_shell == "6s^1"
    assert cesium.valence_shell_signature == "6s^1"
    assert gadolinium.frontier_model == "lanthanide_4f_frontier"
    assert gadolinium.f_shell == "4f^7"
    assert gadolinium.f_shell_stability == "half_filled_shell"
    assert gold.frontier_model == "period_6_transition_frontier"
    assert gold.d_shell == "5d^10"
    assert gold.d_shell_stability == "filled_shell"
    assert gold.outer_shell == "6s^1"
    assert astatine.frontier_model == "period_6_p_block_f_d_core"
    assert astatine.f_shell == "4f^14"
    assert astatine.d_shell == "5d^10"
    assert astatine.p_shell == "6p^5"


def test_frontier_valence_preserves_filled_core_context_for_period_6_p_block():
    lead = find_frontier_valence_signature_record("Pb")
    radon = find_frontier_valence_signature_record("Rn")
    assert lead.valence_shell_signature == "6s^2 6p^2 with filled 4f^14 5d^10 core"
    assert lead.f_shell_stability == "filled_shell"
    assert lead.d_shell_stability == "filled_shell"
    assert radon.p_shell == "6p^6"
    assert radon.outer_shell == "6s^2 6p^6"
    assert radon.frontier_occupancy_count == 32


def test_frontier_valence_rejects_out_of_span_lookup():
    with pytest.raises(KeyError):
        find_frontier_valence_signature_record("Xe")
    with pytest.raises(KeyError):
        find_frontier_valence_signature_record(54)
    with pytest.raises(KeyError):
        find_frontier_valence_signature_record("Xx")
