import json
import threading
from urllib.request import urlopen

from mcms.api import build_api_server, handle_api_request


def _payload(response):
    return response.payload


def test_local_api_health_and_index_routes_are_read_only_contracts():
    index = _payload(handle_api_request("GET", "/"))
    health = _payload(handle_api_request("GET", "/health"))
    method_error = handle_api_request("POST", "/health")
    assert index["api_status"] == "mcms_local_api_ready"
    assert "GET /elements/{symbol|name|atomic_number}" in index["routes"]
    assert "GET /reasoning/configuration/Cr" in index["routes"]
    assert "GET /instances/ion/Na?charge=1" in index["routes"]
    assert "GET /instances/isotope/C?mass_number=14" in index["routes"]
    assert "GET /atom/behavior/C?mass_number=14" in index["routes"]
    assert "GET /atom/behavior/gaps/Rn" in index["routes"]
    assert "GET /atom/behavior/workplan/Rn" in index["routes"]
    assert "GET /atom/behavior/isotope-source-policy" in index["routes"]
    assert "GET /atom/behavior/isotope-source-search" in index["routes"]
    assert "GET /atom/behavior/isotope-candidate-admission/O" in index["routes"]
    assert "GET /atom/behavior/isotope-candidate-admission/Tc" in index["routes"]
    assert "GET /scoring/readiness/Tc" in index["routes"]
    assert "GET /evidence/isotopes/C?mass_number=14" in index["routes"]
    assert "GET /evidence/isotopes/unresolved/Rn" in index["routes"]
    assert "GET /evidence/common-ions/Fe" in index["routes"]
    assert "GET /evidence/common-ions/unresolved/O" in index["routes"]
    assert "GET /evidence/configurations/At" in index["routes"]
    assert "GET /evidence/oxidation-states/Au" in index["routes"]
    assert "GET /evidence/physical-properties/Br" in index["routes"]
    assert "GET /evidence/physical-properties/unresolved/At" in index["routes"]
    assert "GET /evidence/physical-properties/gaps/At" in index["routes"]
    assert "GET /evidence/physical-properties/workplan/At" in index["routes"]
    assert "GET /evidence/physical-properties/source-search/Pa" in index["routes"]
    assert "GET /evidence/physical-properties/partial-source-search/Fr" in index["routes"]
    assert "GET /evidence/physical-properties/secondary-evidence/admission/At" in index["routes"]
    assert "GET /evidence/physical-properties/conflicts/At" in index["routes"]
    assert "GET /evidence/physical-properties/corroboration/Bk" in index["routes"]
    assert "GET /evidence/physical-properties/review/Cf" in index["routes"]
    assert "GET /evidence/physical-properties/gap-closure/Cf" in index["routes"]
    assert "GET /evidence/physical-properties/closure-approval/Cf" in index["routes"]
    assert "GET /evidence/physical-properties/seed-update/Cf" in index["routes"]
    assert "GET /evidence/physical-properties/escalations/Fr" in index["routes"]
    assert "GET /evidence/physical-properties/escalation-search/Fr" in index["routes"]
    assert "GET /evidence/physical-properties/escalation-resolution/Fr" in index["routes"]
    assert "GET /evidence/physical-properties/operator-decisions/Fr" in index["routes"]
    assert "GET /evidence/physical-properties/continued-evidence/Fr" in index["routes"]
    assert "GET /evidence/physical-properties/no-candidate/Fm" in index["routes"]
    assert "GET /evidence/physical-properties/secondary-evidence/template/At" in index["routes"]
    assert "GET /evidence/physical-properties/secondary-source-policy/At" in index["routes"]
    assert "GET /frontier/cs-rn/Au" in index["routes"]
    assert "GET /behavior/cs-rn/Au" in index["routes"]
    assert "GET /relations/cs-rn/Au" in index["routes"]
    assert "GET /matter/profiles/Br" in index["routes"]
    assert "GET /promotion/cs-rn/At" in index["routes"]
    assert "GET /promotion/batch-policy" in index["routes"]
    assert "GET /promotion/partial-eligibility" in index["routes"]
    assert "GET /promotion/full-span-approval-review" in index["routes"]
    assert "GET /promotion/decisions/At" in index["routes"]
    assert "GET /phase3/f-block/U" in index["routes"]
    assert "GET /level2/period-5/Xe" in index["routes"]
    assert health["seed_count"] == 54
    assert health["snapshot_count"] == 118
    assert health["atom_behavior_profile_count"] == 178
    assert health["atom_behavior_gap_count"] == 64
    assert health["atom_behavior_gap_work_item_count"] == 64
    assert health["isotope_source_policy_count"] == 0
    assert health["isotope_source_search_receipt_count"] == 0
    assert health["isotope_candidate_evidence_receipt_count"] == 0
    assert health["isotope_candidate_admission_receipt_count"] == 2
    assert health["element_readiness_score_count"] == 118
    assert method_error.status_code == 405


def test_local_api_exposes_element_snapshot_and_schema_payloads():
    element = _payload(handle_api_request("GET", "/elements/Zn"))
    snapshot = _payload(handle_api_request("GET", "/snapshot/La"))
    schema = _payload(handle_api_request("GET", "/schemas/bundle"))
    assert element["element"]["identity"]["symbol"] == "Zn"
    assert element["receipt"]["validation_status"] == "element_seed_validated"
    assert snapshot["snapshot"]["group"] is None
    assert snapshot["receipt"]["validation_status"] == "element_snapshot_validated"
    assert "mullu_standard_symbolic_element" in schema["schema"]["schemas"]


def test_local_api_graph_query_and_error_paths_are_explicit():
    graph = _payload(handle_api_request("GET", "/graph?symbol=Zn&relation=same_block"))
    missing = handle_api_request("GET", "/elements/Xx")
    bad_relation = handle_api_request("GET", "/graph?symbol=Zn&relation=same_shell")
    assert graph["graph"]["query"]["symbol"] == "Zn"
    assert graph["graph"]["query"]["edge_count"] == 19
    assert missing.status_code == 404
    assert missing.payload["error"] == "not_found"
    assert bad_relation.status_code == 400
    assert bad_relation.payload["error"] == "bad_request"


def test_local_api_exposes_phase_2_reasoning_examples():
    chromium = _payload(handle_api_request("GET", "/reasoning/configuration/Cr"))
    similarity = _payload(handle_api_request("GET", "/reasoning/similarity?left=Cu&right=K"))
    missing_query = handle_api_request("GET", "/reasoning/similarity?left=Cu")
    assert chromium["reasoning"]["evidence"]["configuration_audit"]["is_exception"] is True
    assert chromium["reasoning"]["evidence"]["identity"]["proton_count"] == 24
    assert similarity["reasoning"]["evidence"]["surface_similarity"] is True
    assert similarity["reasoning"]["evidence"]["deep_similarity"] is False
    assert similarity["reasoning"]["answer_lines"][0] == "Partially, but not deeply."
    assert missing_query.status_code == 400


def test_local_api_exposes_ion_and_isotope_instances():
    sodium = _payload(handle_api_request("GET", "/instances/ion/Na?charge=1"))
    carbon_14 = _payload(handle_api_request("GET", "/instances/isotope/C?mass_number=14"))
    missing_charge = handle_api_request("GET", "/instances/ion/Na")
    bad_mass_number = handle_api_request("GET", "/instances/isotope/C?mass_number=5")
    assert sodium["instance"]["instance_id"] == "MSPEE-Z011-Na-ion-plus-1"
    assert sodium["instance"]["electron_count"] == 10
    assert sodium["validation_errors"] == []
    assert carbon_14["instance"]["instance_id"] == "MSPEE-Z006-C-isotope-14"
    assert carbon_14["instance"]["neutron_count"] == 8
    assert carbon_14["validation_errors"] == []
    assert missing_charge.status_code == 400
    assert missing_charge.payload["error"] == "bad_request"
    assert bad_mass_number.status_code == 400


def test_local_api_exposes_atom_behavior_profiles():
    profiles = _payload(handle_api_request("GET", "/atom/behavior"))
    carbon_14 = _payload(handle_api_request("GET", "/atom/behavior/C?mass_number=14"))
    charged_carbon_14 = _payload(
        handle_api_request("GET", "/atom/behavior/C?mass_number=14&charge=1")
    )
    ambiguous = handle_api_request("GET", "/atom/behavior/C")
    under_specified_charge = handle_api_request("GET", "/atom/behavior/C?charge=1")
    assert profiles["validation"]["profile_count"] == 178
    assert profiles["validation"]["radioisotope_profile_count"] == 6
    assert carbon_14["profile"]["profile_id"] == (
        "MSPEE-Z006-C-isotope-14-charge-neutral-0-atom-behavior-v2"
    )
    assert carbon_14["profile"]["neutron_count"] == 8
    assert "weak_decay_context=beta_minus" in carbon_14["profile"]["force_layer_basis"]
    assert charged_carbon_14["profile"]["electron_count"] == 5
    assert charged_carbon_14["profile"]["charge"] == 1
    assert ambiguous.status_code == 404
    assert under_specified_charge.status_code == 400


def test_local_api_exposes_phase_3_f_block_profiles():
    profiles = _payload(handle_api_request("GET", "/phase3/f-block"))
    uranium = _payload(handle_api_request("GET", "/phase3/f-block/U"))
    krypton = handle_api_request("GET", "/phase3/f-block/Kr")
    assert profiles["validation"]["profile_count"] == 30
    assert profiles["validation"]["lanthanide_count"] == 15
    assert profiles["validation"]["actinide_count"] == 15
    assert profiles["profiles"][0]["symbol"] == "La"
    assert uranium["profile"]["series"] == "actinide"
    assert uranium["profile"]["nuclear_state_extension_required"] is True
    assert krypton.status_code == 404


def test_local_api_exposes_period_5_level_2_snapshot_profiles():
    profiles = _payload(handle_api_request("GET", "/level2/period-5"))
    xenon = _payload(handle_api_request("GET", "/level2/period-5/Xe"))
    krypton = handle_api_request("GET", "/level2/period-5/Kr")
    assert profiles["validation"]["profile_count"] == 18
    assert profiles["validation"]["atomic_number_span"] == [37, 54]
    assert profiles["profiles"][0]["symbol"] == "Rb"
    assert xenon["profile"]["symbol"] == "Xe"
    assert xenon["profile"]["oxidation_states"] == [0]
    assert xenon["profile"]["bond_tendency_tags"] == ["noble_gas_low_reactivity"]
    assert krypton.status_code == 404


def test_local_api_exposes_cs_rn_promotion_readiness_profiles():
    profiles = _payload(handle_api_request("GET", "/promotion/cs-rn"))
    astatine = _payload(handle_api_request("GET", "/promotion/cs-rn/At"))
    xenon = handle_api_request("GET", "/promotion/cs-rn/Xe")
    assert profiles["validation"]["profile_count"] == 32
    assert profiles["validation"]["blocked_count"] == 0
    assert profiles["validation"]["ready_count"] == 32
    assert profiles["validation"]["physical_property_evidence_count"] == 32
    assert profiles["validation"]["unresolved_physical_property_evidence_count"] == 1
    assert profiles["profiles"][0]["symbol"] == "Cs"
    assert astatine["profile"]["symbol"] == "At"
    assert astatine["profile"]["readiness_status"] == "promotion_ready"
    assert astatine["profile"]["required_missing_evidence"] == ()
    assert xenon.status_code == 404


def test_local_api_exposes_cs_rn_promotion_decision_receipts():
    receipts = _payload(handle_api_request("GET", "/promotion/decisions"))
    gold = _payload(handle_api_request("GET", "/promotion/decisions/Au"))
    astatine = _payload(handle_api_request("GET", "/promotion/decisions/At"))
    xenon = handle_api_request("GET", "/promotion/decisions/Xe")
    assert receipts["validation"]["receipt_count"] == 32
    assert receipts["validation"]["ready_pending_approval_count"] == 32
    assert receipts["validation"]["blocked_unresolved_physical_property_count"] == 0
    assert gold["receipt"]["decision_status"] == "promotion_ready_pending_approval"
    assert astatine["receipt"]["decision_status"] == "promotion_ready_pending_approval"
    assert xenon.status_code == 404


def test_local_api_exposes_cs_rn_promotion_batch_policy():
    policy = _payload(handle_api_request("GET", "/promotion/batch-policy"))
    assert policy["validation"]["validation_status"] == (
        "promotion_batch_policy_receipt_validated"
    )
    assert policy["receipt"]["policy_decision"] == "allow_full_span_approval_review"
    assert policy["receipt"]["seed_mutation_allowed"] is False
    assert policy["receipt"]["blocked_symbols"] == []


def test_local_api_exposes_partial_promotion_eligibility():
    receipt = _payload(handle_api_request("GET", "/promotion/partial-eligibility"))

    assert receipt["validation"]["validation_status"] == (
        "partial_promotion_eligibility_receipt_validated"
    )
    assert receipt["validation"]["eligible_count"] == 32
    assert receipt["validation"]["blocked_count"] == 0
    assert receipt["receipt"]["blocked_symbols"] == []
    assert receipt["receipt"]["partial_review_allowed"] is True
    assert receipt["receipt"]["seed_mutation_allowed"] is False


def test_local_api_exposes_cs_rn_frontier_valence_records():
    records = _payload(handle_api_request("GET", "/frontier/cs-rn"))
    gold = _payload(handle_api_request("GET", "/frontier/cs-rn/Au"))
    xenon = handle_api_request("GET", "/frontier/cs-rn/Xe")
    assert records["validation"]["record_count"] == 32
    assert records["validation"]["lanthanide_count"] == 15
    assert records["validation"]["transition_count"] == 9
    assert records["records"][0]["symbol"] == "Cs"
    assert gold["record"]["frontier_model"] == "period_6_transition_frontier"
    assert gold["record"]["d_shell"] == "5d^10"
    assert gold["record"]["d_shell_stability"] == "filled_shell"
    assert xenon.status_code == 404


def test_local_api_exposes_cs_rn_oxidation_state_evidence():
    records = _payload(handle_api_request("GET", "/evidence/oxidation-states"))
    gold = _payload(handle_api_request("GET", "/evidence/oxidation-states/Au"))
    xenon = handle_api_request("GET", "/evidence/oxidation-states/Xe")
    assert records["validation"]["record_count"] == 32
    assert records["validation"]["variable_oxidation_state_count"] == 15
    assert records["validation"]["negative_oxidation_state_count"] == 1
    assert records["records"][0]["symbol"] == "Cs"
    assert gold["record"]["oxidation_states"] == [3, 1]
    assert gold["record"]["pubchem_group_block"] == "Transition metal"
    assert xenon.status_code == 404


def test_local_api_exposes_cs_rn_behavior_tag_overlays():
    records = _payload(handle_api_request("GET", "/behavior/cs-rn"))
    gold = _payload(handle_api_request("GET", "/behavior/cs-rn/Au"))
    xenon = handle_api_request("GET", "/behavior/cs-rn/Xe")
    assert records["validation"]["record_count"] == 32
    assert records["validation"]["coordination_relevance_count"] == 9
    assert records["validation"]["f_orbital_relevance_count"] == 15
    assert records["records"][0]["symbol"] == "Cs"
    assert "period_6_transition_metal" in gold["record"]["inferred_behavior_tags"]
    assert "filled_d_shell_context" in gold["record"]["inferred_behavior_tags"]
    assert xenon.status_code == 404


def test_local_api_exposes_cs_rn_relation_overlays():
    records = _payload(handle_api_request("GET", "/relations/cs-rn"))
    gold = _payload(handle_api_request("GET", "/relations/cs-rn/Au"))
    xenon = handle_api_request("GET", "/relations/cs-rn/Xe")
    assert records["validation"]["record_count"] == 32
    assert records["validation"]["edge_count"] > 0
    assert records["validation"]["edge_counts_by_type"]["same_period"] == 32 * 31
    assert gold["record"]["symbol"] == "Au"
    assert any(edge["target_symbol"] == "Pt" for edge in gold["record"]["relation_edges"])
    assert xenon.status_code == 404


def test_local_api_exposes_cs_rn_configuration_evidence():
    records = _payload(handle_api_request("GET", "/evidence/configurations"))
    astatine = _payload(handle_api_request("GET", "/evidence/configurations/At"))
    xenon = handle_api_request("GET", "/evidence/configurations/Xe")
    assert records["validation"]["record_count"] == 32
    assert records["validation"]["exception_count"] == 2
    assert records["validation"]["special_first_cation_literature_count"] == 8
    assert records["records"][0]["symbol"] == "Cs"
    assert astatine["record"]["neutral_configuration"] == (
        "[Xe] 4f^14 5d^10 6s^2 6p^5"
    )
    assert astatine["record"]["first_cation_source_note"] is not None
    assert xenon.status_code == 404


def test_local_api_http_server_serves_json_on_ephemeral_port():
    server = build_api_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urlopen(f"http://127.0.0.1:{server.server_port}/graph/Zn?relation=same_block") as response:
            payload = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
        assert payload["api_status"] == "mcms_local_api_ready"
        assert payload["graph"]["query"]["symbol"] == "Zn"
        assert payload["graph"]["query"]["edge_count"] == 19
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
