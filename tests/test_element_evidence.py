import json

import pytest

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import (
    build_physical_property_secondary_evidence_template,
    find_common_ion_evidence_records,
    find_isotope_evidence_records,
    find_physical_property_evidence_record,
    find_unresolved_common_ion_evidence_record,
    find_unresolved_isotope_evidence_record,
    find_unresolved_physical_property_evidence_record,
    get_partial_physical_property_source_search_receipt,
    get_physical_property_closure_approval_receipt,
    get_physical_property_conflict_resolution_receipt,
    get_physical_property_continued_evidence_plan,
    get_physical_property_corroboration_review_receipt,
    get_physical_property_escalation_receipt,
    get_physical_property_escalation_resolution_receipt,
    get_physical_property_escalation_search_receipt,
    get_physical_property_gap_audit_receipt,
    get_physical_property_gap_closure_decision,
    get_physical_property_gap_work_item,
    get_physical_property_no_candidate_review_receipt,
    get_physical_property_operator_decision_receipt,
    get_physical_property_review_receipt,
    get_physical_property_secondary_evidence_admission_decision,
    get_physical_property_secondary_source_policy,
    get_physical_property_seed_update_receipt,
    get_physical_property_source_search_receipt,
    list_common_ion_evidence_records,
    list_isotope_evidence_records,
    list_partial_physical_property_source_search_receipts,
    list_physical_property_closure_approval_receipts,
    list_physical_property_conflict_resolution_receipts,
    list_physical_property_continued_evidence_plans,
    list_physical_property_corroboration_review_receipts,
    list_physical_property_escalation_receipts,
    list_physical_property_escalation_resolution_receipts,
    list_physical_property_escalation_search_receipts,
    list_physical_property_evidence_records,
    list_physical_property_gap_audit_receipts,
    list_physical_property_gap_closure_decisions,
    list_physical_property_gap_work_items,
    list_physical_property_no_candidate_review_receipts,
    list_physical_property_operator_decision_receipts,
    list_physical_property_review_receipts,
    list_physical_property_secondary_evidence_admission_decisions,
    list_physical_property_secondary_evidence_receipts,
    list_physical_property_secondary_source_policies,
    list_physical_property_seed_update_receipts,
    list_physical_property_source_search_receipts,
    list_unresolved_common_ion_evidence_records,
    list_unresolved_isotope_evidence_records,
    list_unresolved_physical_property_evidence_records,
    validate_common_ion_evidence_records,
    validate_isotope_evidence_records,
    validate_partial_physical_property_source_search_receipts,
    validate_physical_property_closure_approval_receipts,
    validate_physical_property_conflict_resolution_receipts,
    validate_physical_property_continued_evidence_plans,
    validate_physical_property_corroboration_review_receipts,
    validate_physical_property_escalation_receipts,
    validate_physical_property_escalation_resolution_receipts,
    validate_physical_property_escalation_search_receipts,
    validate_physical_property_evidence_records,
    validate_physical_property_gap_audit_receipts,
    validate_physical_property_gap_closure_decisions,
    validate_physical_property_gap_work_items,
    validate_physical_property_no_candidate_review_receipts,
    validate_physical_property_operator_decision_receipts,
    validate_physical_property_review_receipts,
    validate_physical_property_secondary_evidence_admission_decisions,
    validate_physical_property_secondary_evidence_receipts,
    validate_physical_property_secondary_source_policies,
    validate_physical_property_seed_update_receipts,
    validate_physical_property_source_search_receipts,
    validate_unresolved_evidence_records,
    validate_unresolved_physical_property_evidence_records,
)


def test_isotope_evidence_records_validate_stable_and_radioactive_boundaries():
    records = list_isotope_evidence_records()
    validation = validate_isotope_evidence_records(records)
    carbon_14 = find_isotope_evidence_records("C", mass_number=14)[0]
    tritium = find_isotope_evidence_records("H", mass_number=3)[0]
    oxygen_18 = find_isotope_evidence_records("O", mass_number=18)[0]
    hydrogen_records = find_isotope_evidence_records("H")
    helium_records = find_isotope_evidence_records("He")
    nitrogen_records = find_isotope_evidence_records("N")
    oxygen_records = find_isotope_evidence_records("O")

    assert validation["validation_status"] == "isotope_evidence_records_validated"
    assert validation["record_count"] == 13
    assert validation["radioisotope_count"] == 2
    assert carbon_14.isotope_id == "MSPEE-Z006-C-isotope-14"
    assert carbon_14.neutron_count == 8
    assert carbon_14.half_life_value == 5730.0
    assert carbon_14.decay_mode == "beta_minus"
    assert tritium.half_life_value == 12.32
    assert tritium.decay_mode == "beta_minus"
    assert oxygen_18.neutron_count == 10
    assert len(hydrogen_records) == 3
    assert len(helium_records) == 2
    assert len(nitrogen_records) == 2
    assert len(oxygen_records) == 3


def test_common_ion_evidence_records_validate_against_oxidation_state_source():
    records = list_common_ion_evidence_records()
    validation = validate_common_ion_evidence_records(records)
    iron_records = find_common_ion_evidence_records("Fe")
    chloride_record = find_common_ion_evidence_records("Cl")[0]

    assert validation["validation_status"] == "common_ion_evidence_records_validated"
    assert validation["record_count"] == 9
    assert {record.charge for record in iron_records} == {2, 3}
    assert chloride_record.ion_id == "MSPEE-Z017-Cl-ion-minus-1"
    assert chloride_record.electron_count == 18
    assert chloride_record.validate() == []


def test_unresolved_isotope_and_common_ion_evidence_receipts_are_explicit():
    isotope_records = list_unresolved_isotope_evidence_records()
    common_ion_records = list_unresolved_common_ion_evidence_records()
    isotope_validation = validate_unresolved_evidence_records(
        isotope_records,
        expected_domain="isotope_evidence",
    )
    common_ion_validation = validate_unresolved_evidence_records(
        common_ion_records,
        expected_domain="common_ion_evidence",
    )
    lithium_isotope = find_unresolved_isotope_evidence_record("Li")
    oxygen_common_ion = find_unresolved_common_ion_evidence_record("O")

    assert isotope_validation["validation_status"] == (
        "isotope_evidence_unresolved_records_validated"
    )
    assert isotope_validation["record_count"] == 113
    assert common_ion_validation["validation_status"] == (
        "common_ion_evidence_unresolved_records_validated"
    )
    assert common_ion_validation["record_count"] == 47
    assert lithium_isotope.evidence_domain == "isotope_evidence"
    assert "natural_abundance" in lithium_isotope.missing_evidence
    assert oxygen_common_ion.evidence_domain == "common_ion_evidence"
    assert "common_ion_charge_set" in oxygen_common_ion.missing_evidence
    assert oxygen_common_ion.validate() == []


def test_evidence_lookup_rejects_unknown_records():
    with pytest.raises(KeyError, match="unknown isotope evidence record"):
        find_isotope_evidence_records("Li", mass_number=7)

    with pytest.raises(KeyError, match="unknown common-ion evidence record"):
        find_common_ion_evidence_records("O")

    with pytest.raises(KeyError, match="unknown physical-property evidence record"):
        find_physical_property_evidence_record("Og")

    with pytest.raises(KeyError, match="unknown physical-property evidence record"):
        find_physical_property_evidence_record("At")


def test_physical_property_evidence_records_validate_measured_boundaries():
    records = list_physical_property_evidence_records()
    validation = validate_physical_property_evidence_records(records)
    bromine = find_physical_property_evidence_record("Br")
    krypton = find_physical_property_evidence_record("Kr")

    assert validation["validation_status"] == "physical_property_evidence_records_validated"
    assert validation["record_count"] == 93
    assert validation["standard_states"] == ("Gas", "Liquid", "Solid")
    assert bromine.standard_state == "Liquid"
    assert bromine.melting_point_k == 265.95
    assert bromine.boiling_point_k == 331.95
    assert krypton.standard_state == "Gas"
    assert krypton.density_unit == "g/cm^3"
    assert krypton.validate() == []
    mercury = find_physical_property_evidence_record("Hg")
    radon = find_physical_property_evidence_record("Rn")
    uranium = find_physical_property_evidence_record("U")
    assert mercury.standard_state == "Liquid"
    assert mercury.density_value == 13.5336
    assert radon.standard_state == "Gas"
    assert radon.boiling_point_k == 211.45
    assert uranium.standard_state == "Solid"
    assert uranium.density_value == 18.95
    arsenic = find_physical_property_evidence_record("As")
    assert arsenic.melting_point_k > arsenic.boiling_point_k
    assert arsenic.phase_transition_note is not None
    assert arsenic.validate() == []


def test_unresolved_physical_property_evidence_records_validate_missing_fields():
    records = list_unresolved_physical_property_evidence_records()
    validation = validate_unresolved_physical_property_evidence_records(records)
    astatine = find_unresolved_physical_property_evidence_record("At")
    oganesson = find_unresolved_physical_property_evidence_record("Og")

    assert validation["validation_status"] == (
        "unresolved_physical_property_evidence_records_validated"
    )
    assert validation["record_count"] == 25
    assert validation["missing_field_counts"]["boiling_point_k"] == 25
    assert astatine.missing_fields == ("boiling_point_k",)
    assert astatine.density_value == 7.0
    assert oganesson.standard_state == "Expected to be a Gas"
    assert oganesson.missing_fields == (
        "melting_point_k",
        "boiling_point_k",
        "density_value",
    )
    assert oganesson.validate() == []


def test_physical_property_gap_audit_receipts_preserve_no_guess_boundary():
    receipts = list_physical_property_gap_audit_receipts()
    validation = validate_physical_property_gap_audit_receipts(receipts)
    astatine = get_physical_property_gap_audit_receipt("At")

    assert validation["validation_status"] == "physical_property_gap_audit_receipts_validated"
    assert validation["receipt_count"] == 25
    assert validation["cs_rn_blocking_gap_count"] == 1
    assert validation["boiling_point_gap_count"] == 25
    assert astatine.source_row_status == "source_row_incomplete"
    assert astatine.gap_status == "awaiting_authoritative_source_value"
    assert astatine.blocks_promotion_spans == ("Cs-Rn",)
    assert astatine.no_guess_policy is True
    assert astatine.validate() == []


def test_physical_property_secondary_source_policy_does_not_close_gap_by_itself():
    policies = list_physical_property_secondary_source_policies()
    validation = validate_physical_property_secondary_source_policies(policies)
    astatine = get_physical_property_secondary_source_policy("At")

    assert validation["validation_status"] == (
        "physical_property_secondary_source_policies_validated"
    )
    assert validation["policy_count"] == 25
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert validation["candidate_source_count"] == 5
    assert astatine.gap_closure_status == "gap_not_closed_by_policy"
    assert astatine.seed_mutation_allowed is False
    assert astatine.target_gap_receipt_id == "MSPEE-PHYSICAL-PROPERTY-GAP-Z085-At"
    assert "operator_approval_before_seed_mutation" in astatine.admission_requirements
    assert astatine.validate() == []


def test_physical_property_secondary_evidence_receipts_start_as_unadmitted_candidate():
    receipts = list_physical_property_secondary_evidence_receipts()
    validation = validate_physical_property_secondary_evidence_receipts(receipts)
    template = build_physical_property_secondary_evidence_template("At")
    by_field = {(receipt.symbol, receipt.field_name): receipt for receipt in receipts}

    assert len(receipts) == 8
    assert validation["validation_status"] == (
        "physical_property_secondary_evidence_receipts_validated"
    )
    assert validation["receipt_count"] == 8
    assert validation["admitted_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert set(by_field) == {
        ("At", "boiling_point_k"),
        ("Fr", "boiling_point_k"),
        ("Fr", "density_value"),
        ("Pa", "boiling_point_k"),
        ("Bk", "boiling_point_k"),
        ("Cf", "boiling_point_k"),
        ("Cf", "density_value"),
        ("Es", "boiling_point_k"),
    }
    assert by_field[("At", "boiling_point_k")].normalized_value == 610.15
    assert by_field[("Fr", "boiling_point_k")].normalized_value == 953.15
    assert by_field[("Fr", "density_value")].normalized_value == 2.9
    assert by_field[("Pa", "boiling_point_k")].normalized_value == 4300.15
    assert by_field[("Bk", "boiling_point_k")].normalized_value == 2900.15
    assert by_field[("Cf", "boiling_point_k")].normalized_value == 1743.15
    assert by_field[("Cf", "density_value")].normalized_value == 15.1
    assert by_field[("Es", "boiling_point_k")].normalized_value == 1269.15
    assert by_field[("At", "boiling_point_k")].source_key == "lanl_periodic_table_candidate"
    assert by_field[("Pa", "boiling_point_k")].admission_decision == "reviewed_pending_approval"
    assert by_field[("Cf", "density_value")].seed_mutation_allowed is False
    assert by_field[("At", "boiling_point_k")].validate() == []
    assert template["symbol"] == "At"
    assert template["field_name"] == "boiling_point_k"
    assert template["source_key"] == "nist_chemistry_webbook_candidate"
    assert "source_citation" in template["required_fields"]
    assert template["seed_mutation_allowed"] is False


def test_physical_property_secondary_evidence_admission_blocks_conflict():
    decisions = list_physical_property_secondary_evidence_admission_decisions()
    validation = validate_physical_property_secondary_evidence_admission_decisions(decisions)
    astatine = get_physical_property_secondary_evidence_admission_decision("At")
    francium = get_physical_property_secondary_evidence_admission_decision("Fr")
    francium_density = get_physical_property_secondary_evidence_admission_decision(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z087-Fr-density_value-WebElements"
    )
    protactinium = get_physical_property_secondary_evidence_admission_decision("Pa")
    berkelium = get_physical_property_secondary_evidence_admission_decision("Bk")
    californium_boiling = get_physical_property_secondary_evidence_admission_decision(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z098-Cf-boiling_point_k-LANL"
    )
    californium_density = get_physical_property_secondary_evidence_admission_decision(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z098-Cf-density_value-RSC"
    )
    einsteinium = get_physical_property_secondary_evidence_admission_decision(
        "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z099-Es-boiling_point_k-LANL"
    )

    assert validation["validation_status"] == (
        "physical_property_secondary_evidence_admission_decisions_validated"
    )
    assert validation["decision_count"] == 8
    assert validation["admitted_gap_closure_count"] == 0
    assert validation["conflict_blocked_count"] == 3
    assert validation["corroboration_blocked_count"] == 4
    assert validation["pending_review_count"] == 1
    assert validation["seed_mutation_allowed_count"] == 0
    assert astatine.decision_status == "secondary_evidence_not_admitted_conflict"
    assert francium.decision_status == "secondary_evidence_not_admitted_conflict"
    assert francium_density.decision_status == (
        "secondary_evidence_not_admitted_needs_corroboration"
    )
    assert protactinium.decision_status == "secondary_evidence_not_admitted_conflict"
    assert berkelium.decision_status == (
        "secondary_evidence_not_admitted_needs_corroboration"
    )
    assert californium_boiling.decision_status == (
        "secondary_evidence_not_admitted_needs_corroboration"
    )
    assert californium_density.decision_status == (
        "secondary_evidence_not_admitted_pending_review"
    )
    assert einsteinium.decision_status == (
        "secondary_evidence_not_admitted_needs_corroboration"
    )
    assert astatine.closes_gap is False
    assert francium.closes_gap is False
    assert francium_density.closes_gap is False
    assert protactinium.closes_gap is False
    assert berkelium.closes_gap is False
    assert californium_boiling.closes_gap is False
    assert californium_density.closes_gap is False
    assert einsteinium.closes_gap is False
    assert astatine.seed_mutation_allowed is False
    assert astatine.validate() == []
    assert francium.validate() == []
    assert francium_density.validate() == []
    assert protactinium.validate() == []
    assert berkelium.validate() == []
    assert californium_boiling.validate() == []
    assert californium_density.validate() == []
    assert einsteinium.validate() == []


def test_physical_property_conflict_resolution_receipt_blocks_gap_closure():
    receipts = list_physical_property_conflict_resolution_receipts()
    validation = validate_physical_property_conflict_resolution_receipts(receipts)
    astatine = get_physical_property_conflict_resolution_receipt("At")
    francium = get_physical_property_conflict_resolution_receipt("Fr")
    protactinium = get_physical_property_conflict_resolution_receipt("Pa")

    assert validation["validation_status"] == (
        "physical_property_conflict_resolution_receipts_validated"
    )
    assert validation["receipt_count"] == 3
    assert validation["blocked_pending_higher_precedence_source_count"] == 3
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert astatine.resolution_decision == "blocked_pending_higher_precedence_source"
    assert francium.resolution_decision == "blocked_pending_higher_precedence_source"
    assert protactinium.resolution_decision == "blocked_pending_higher_precedence_source"
    assert astatine.closes_gap is False
    assert francium.closes_gap is False
    assert protactinium.closes_gap is False
    assert astatine.seed_mutation_allowed is False
    assert {value.alignment_group for value in astatine.compared_values} == {
        "337_degC_cluster",
        "350_degC_cluster",
    }
    assert astatine.validate() == []
    assert {value.alignment_group for value in francium.compared_values} == {
        "953_K_cluster",
        "923_K_cluster",
    }
    assert francium.validate() == []
    assert {value.alignment_group for value in protactinium.compared_values} == {
        "4300_K_cluster",
        "4273_K_cluster",
    }
    assert protactinium.validate() == []


def test_physical_property_corroboration_review_blocks_bk_gap_closure():
    receipts = list_physical_property_corroboration_review_receipts()
    validation = validate_physical_property_corroboration_review_receipts(receipts)
    francium = get_physical_property_corroboration_review_receipt(
        "MSPEE-PHYSICAL-PROPERTY-CORROBORATION-REVIEW-Z087-Fr-density_value"
    )
    berkelium = get_physical_property_corroboration_review_receipt("Bk")
    californium = get_physical_property_corroboration_review_receipt("Cf")
    einsteinium = get_physical_property_corroboration_review_receipt("Es")

    assert validation["validation_status"] == (
        "physical_property_corroboration_review_receipts_validated"
    )
    assert validation["receipt_count"] == 4
    assert validation["blocked_pending_corroborating_source_count"] == 4
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert francium.review_decision == "blocked_pending_corroborating_source"
    assert berkelium.review_decision == "blocked_pending_corroborating_source"
    assert californium.review_decision == "blocked_pending_corroborating_source"
    assert einsteinium.review_decision == "blocked_pending_corroborating_source"
    assert francium.closes_gap is False
    assert berkelium.closes_gap is False
    assert californium.closes_gap is False
    assert einsteinium.closes_gap is False
    assert francium.seed_mutation_allowed is False
    assert berkelium.seed_mutation_allowed is False
    assert californium.seed_mutation_allowed is False
    assert einsteinium.seed_mutation_allowed is False
    assert francium.validate() == []
    assert berkelium.validate() == []
    assert californium.validate() == []
    assert einsteinium.validate() == []


def test_physical_property_review_receipt_blocks_cf_density_gap_closure():
    receipts = list_physical_property_review_receipts()
    validation = validate_physical_property_review_receipts(receipts)
    californium = get_physical_property_review_receipt("Cf")

    assert validation["validation_status"] == "physical_property_review_receipts_validated"
    assert validation["receipt_count"] == 1
    assert validation["blocked_pending_source_review_count"] == 0
    assert validation["resolved_admit_candidate_count"] == 1
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert californium.field_name == "density_value"
    assert californium.review_decision == "resolved_admit_candidate"
    assert californium.corroborating_sources_checked
    assert californium.closes_gap is False
    assert californium.seed_mutation_allowed is False
    assert californium.validate() == []


def test_physical_property_gap_closure_decision_requires_operator_approval():
    decisions = list_physical_property_gap_closure_decisions()
    validation = validate_physical_property_gap_closure_decisions(decisions)
    californium = get_physical_property_gap_closure_decision("Cf")

    assert validation["validation_status"] == "physical_property_gap_closure_decisions_validated"
    assert validation["decision_count"] == 1
    assert validation["ready_pending_operator_approval_count"] == 1
    assert validation["approved_for_seed_update_count"] == 0
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert californium.field_name == "density_value"
    assert californium.closure_status == "gap_closure_ready_pending_operator_approval"
    assert californium.closes_gap is False
    assert californium.seed_mutation_allowed is False
    assert californium.validate() == []


def test_physical_property_closure_approval_receipt_defers_seed_mutation():
    receipts = list_physical_property_closure_approval_receipts()
    validation = validate_physical_property_closure_approval_receipts(receipts)
    californium = get_physical_property_closure_approval_receipt("Cf")

    assert validation["validation_status"] == (
        "physical_property_closure_approval_receipts_validated"
    )
    assert validation["receipt_count"] == 1
    assert validation["deferred_approval_count"] == 1
    assert validation["approved_for_seed_update_count"] == 0
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert californium.field_name == "density_value"
    assert californium.approval_status == "closure_approval_deferred"
    assert californium.closes_gap is False
    assert californium.seed_mutation_allowed is False
    assert californium.validate() == []


def test_physical_property_seed_update_receipt_blocks_deferred_approval():
    receipts = list_physical_property_seed_update_receipts()
    validation = validate_physical_property_seed_update_receipts(receipts)
    californium = get_physical_property_seed_update_receipt("Cf")

    assert validation["validation_status"] == (
        "physical_property_seed_update_receipts_validated"
    )
    assert validation["receipt_count"] == 1
    assert validation["blocked_by_deferred_approval_count"] == 1
    assert validation["ready_to_apply_count"] == 0
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert validation["seed_update_applied_count"] == 0
    assert californium.field_name == "density_value"
    assert californium.update_status == "seed_update_blocked_by_deferred_approval"
    assert californium.closes_gap is False
    assert californium.seed_mutation_allowed is False
    assert californium.seed_update_applied is False
    assert californium.validate() == []


def test_physical_property_escalation_receipts_prioritize_blocked_work():
    receipts = list_physical_property_escalation_receipts()
    validation = validate_physical_property_escalation_receipts(receipts)
    astatine = get_physical_property_escalation_receipt("At")
    berkelium = get_physical_property_escalation_receipt("Bk")
    californium = get_physical_property_escalation_receipt(
        "MSPEE-PHYSICAL-PROPERTY-SEED-UPDATE-Z098-Cf-density_value"
    )

    assert validation["validation_status"] == "physical_property_escalation_receipts_validated"
    assert validation["receipt_count"] == 8
    assert validation["higher_precedence_source_required_count"] == 3
    assert validation["corroborating_source_required_count"] == 4
    assert validation["operator_approval_required_count"] == 1
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert astatine.escalation_class == "higher_precedence_source_required"
    assert astatine.priority_rank == 0
    assert berkelium.escalation_class == "corroborating_source_required"
    assert californium.escalation_class == "operator_approval_required"
    assert californium.closes_gap is False
    assert californium.seed_mutation_allowed is False
    assert astatine.validate() == []
    assert berkelium.validate() == []
    assert californium.validate() == []


def test_physical_property_escalation_search_records_at_source_attempt():
    receipts = list_physical_property_escalation_search_receipts()
    validation = validate_physical_property_escalation_search_receipts(receipts)
    astatine = get_physical_property_escalation_search_receipt("At")
    francium = get_physical_property_escalation_search_receipt("Fr")
    francium_density = get_physical_property_escalation_search_receipt(
        "MSPEE-PHYSICAL-PROPERTY-ESCALATION-SEARCH-Z087-Fr-density_value"
    )
    berkelium = get_physical_property_escalation_search_receipt("Bk")
    californium = get_physical_property_escalation_search_receipt("Cf")
    einsteinium = get_physical_property_escalation_search_receipt("Es")
    protactinium = get_physical_property_escalation_search_receipt("Pa")

    assert validation["validation_status"] == (
        "physical_property_escalation_search_receipts_validated"
    )
    assert validation["search_receipt_count"] == 7
    assert validation["higher_precedence_source_not_found_count"] == 3
    assert validation["corroborating_source_not_found_count"] == 4
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert astatine.search_status == "higher_precedence_source_not_found"
    assert {source_check.source_key for source_check in astatine.source_checks} == {
        "nist_chemistry_webbook_atomic_astatine",
        "pubchem_element_astatine",
        "rsc_periodic_table_astatine",
    }
    assert astatine.closes_gap is False
    assert astatine.seed_mutation_allowed is False
    assert francium.search_status == "higher_precedence_source_not_found"
    assert {source_check.source_key for source_check in francium.source_checks} == {
        "nist_chemistry_webbook_atomic_francium",
        "pubchem_element_francium",
        "rsc_periodic_table_francium",
    }
    assert francium.closes_gap is False
    assert francium.seed_mutation_allowed is False
    assert francium_density.search_status == "corroborating_source_not_found"
    assert {source_check.source_key for source_check in francium_density.source_checks} == {
        "webelements_francium",
        "rsc_periodic_table_francium",
        "pubchem_element_francium",
    }
    assert francium_density.closes_gap is False
    assert francium_density.seed_mutation_allowed is False
    assert berkelium.search_status == "corroborating_source_not_found"
    assert {source_check.source_key for source_check in berkelium.source_checks} == {
        "lanl_periodic_table_berkelium",
        "rsc_periodic_table_berkelium",
        "webelements_berkelium",
        "pubchem_element_berkelium",
    }
    assert berkelium.closes_gap is False
    assert berkelium.seed_mutation_allowed is False
    assert californium.search_status == "corroborating_source_not_found"
    assert {source_check.source_key for source_check in californium.source_checks} == {
        "lanl_periodic_table_californium",
        "rsc_periodic_table_californium",
        "webelements_californium",
        "pubchem_element_californium",
    }
    assert californium.closes_gap is False
    assert californium.seed_mutation_allowed is False
    assert einsteinium.search_status == "corroborating_source_not_found"
    assert {source_check.source_key for source_check in einsteinium.source_checks} == {
        "lanl_periodic_table_einsteinium",
        "rsc_periodic_table_einsteinium",
        "webelements_einsteinium",
        "pubchem_element_einsteinium",
    }
    assert einsteinium.closes_gap is False
    assert einsteinium.seed_mutation_allowed is False
    assert protactinium.search_status == "higher_precedence_source_not_found"
    assert {source_check.source_key for source_check in protactinium.source_checks} == {
        "nist_chemistry_webbook_atomic_protactinium",
        "pubchem_element_protactinium",
        "rsc_periodic_table_protactinium",
        "webelements_protactinium",
    }
    assert protactinium.closes_gap is False
    assert protactinium.seed_mutation_allowed is False
    assert astatine.validate() == []
    assert francium.validate() == []
    assert francium_density.validate() == []
    assert berkelium.validate() == []
    assert californium.validate() == []
    assert einsteinium.validate() == []
    assert protactinium.validate() == []


def test_physical_property_escalation_resolution_recommends_without_applying():
    receipts = list_physical_property_escalation_resolution_receipts()
    validation = validate_physical_property_escalation_resolution_receipts(receipts)
    astatine = get_physical_property_escalation_resolution_receipt("At")
    californium = get_physical_property_escalation_resolution_receipt("Cf")

    assert validation["validation_status"] == (
        "physical_property_escalation_resolution_receipts_validated"
    )
    assert validation["receipt_count"] == 7
    assert validation["conflict_resolution_blocked_count"] == 3
    assert validation["candidate_rejection_recommended_count"] == 4
    assert validation["final_resolution_applied_count"] == 0
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert astatine.resolution_status == (
        "conflict_resolution_blocked_pending_operator_decision"
    )
    assert californium.resolution_status == (
        "candidate_rejection_recommended_pending_operator_decision"
    )
    assert astatine.final_resolution_applied is False
    assert californium.final_resolution_applied is False
    assert astatine.closes_gap is False
    assert californium.seed_mutation_allowed is False
    assert astatine.validate() == []
    assert californium.validate() == []


def test_physical_property_operator_decisions_are_deferred():
    receipts = list_physical_property_operator_decision_receipts()
    validation = validate_physical_property_operator_decision_receipts(receipts)
    astatine = get_physical_property_operator_decision_receipt("At")
    californium = get_physical_property_operator_decision_receipt("Cf")

    assert validation["validation_status"] == (
        "physical_property_operator_decision_receipts_validated"
    )
    assert validation["receipt_count"] == 7
    assert validation["deferred_decision_count"] == 7
    assert validation["approved_resolution_count"] == 0
    assert validation["rejected_resolution_count"] == 0
    assert validation["final_resolution_applied_count"] == 0
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert astatine.operator_decision_status == "operator_decision_deferred"
    assert californium.operator_decision_status == "operator_decision_deferred"
    assert astatine.final_resolution_applied is False
    assert californium.final_resolution_applied is False
    assert astatine.closes_gap is False
    assert californium.seed_mutation_allowed is False
    assert astatine.validate() == []
    assert californium.validate() == []


def test_physical_property_continued_evidence_plans_keep_search_open():
    plans = list_physical_property_continued_evidence_plans()
    validation = validate_physical_property_continued_evidence_plans(plans)
    astatine = get_physical_property_continued_evidence_plan("At")
    californium = get_physical_property_continued_evidence_plan("Cf")

    assert validation["validation_status"] == (
        "physical_property_continued_evidence_plans_validated"
    )
    assert validation["plan_count"] == 7
    assert validation["continued_evidence_required_count"] == 7
    assert validation["higher_precedence_source_discovery_count"] == 3
    assert validation["independent_corroboration_discovery_count"] == 4
    assert validation["final_resolution_applied_count"] == 0
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert astatine.plan_class == "higher_precedence_source_discovery"
    assert californium.plan_class == "independent_corroboration_discovery"
    assert astatine.final_resolution_applied is False
    assert californium.final_resolution_applied is False
    assert astatine.closes_gap is False
    assert californium.seed_mutation_allowed is False
    assert astatine.validate() == []
    assert californium.validate() == []


def test_physical_property_no_candidate_review_blocks_gap_closure():
    receipts = list_physical_property_no_candidate_review_receipts()
    validation = validate_physical_property_no_candidate_review_receipts(receipts)
    fermium = get_physical_property_no_candidate_review_receipt("Fm")
    mendelevium = get_physical_property_no_candidate_review_receipt("Md")
    nobelium = get_physical_property_no_candidate_review_receipt("No")
    lawrencium = get_physical_property_no_candidate_review_receipt("Lr")

    assert validation["validation_status"] == (
        "physical_property_no_candidate_review_receipts_validated"
    )
    assert validation["receipt_count"] == 4
    assert validation["blocked_no_admissible_candidate_found_count"] == 4
    assert validation["field_review_count"] == 8
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert fermium.review_decision == "blocked_no_admissible_candidate_found"
    assert mendelevium.review_decision == "blocked_no_admissible_candidate_found"
    assert nobelium.review_decision == "blocked_no_admissible_candidate_found"
    assert lawrencium.review_decision == "blocked_no_admissible_candidate_found"
    assert {review.field_name for review in fermium.field_reviews} == {
        "boiling_point_k",
        "density_value",
    }
    assert {review.field_name for review in mendelevium.field_reviews} == {
        "boiling_point_k",
        "density_value",
    }
    assert {review.field_name for review in nobelium.field_reviews} == {
        "boiling_point_k",
        "density_value",
    }
    assert {review.field_name for review in lawrencium.field_reviews} == {
        "boiling_point_k",
        "density_value",
    }
    assert fermium.closes_gap is False
    assert mendelevium.closes_gap is False
    assert nobelium.closes_gap is False
    assert lawrencium.closes_gap is False
    assert fermium.seed_mutation_allowed is False
    assert mendelevium.seed_mutation_allowed is False
    assert nobelium.seed_mutation_allowed is False
    assert lawrencium.seed_mutation_allowed is False
    assert fermium.validate() == []
    assert mendelevium.validate() == []
    assert nobelium.validate() == []
    assert lawrencium.validate() == []


def test_physical_property_gap_workplan_prioritizes_without_closing_gaps():
    items = list_physical_property_gap_work_items()
    validation = validate_physical_property_gap_work_items(items)
    astatine = get_physical_property_gap_work_item("At")
    protactinium = get_physical_property_gap_work_item("Pa")
    oganesson = get_physical_property_gap_work_item("Og")

    assert validation["validation_status"] == "physical_property_gap_work_items_validated"
    assert validation["work_item_count"] == 25
    assert validation["conflict_blocked_count"] == 1
    assert validation["single_field_source_search_count"] == 2
    assert validation["partial_property_source_search_count"] == 7
    assert validation["synthetic_superheavy_uncertainty_count"] == 15
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert items[0].symbol == "At"
    assert astatine.priority_rank == 0
    assert astatine.work_status == "conflict_blocked_promotion"
    assert protactinium.work_status == "single_field_source_search"
    assert oganesson.work_status == "synthetic_superheavy_uncertainty"
    assert astatine.validate() == []


def test_physical_property_source_search_receipts_track_pa_and_bk_without_values():
    receipts = list_physical_property_source_search_receipts()
    validation = validate_physical_property_source_search_receipts(receipts)
    protactinium = get_physical_property_source_search_receipt("Pa")
    berkelium = get_physical_property_source_search_receipt("Bk")

    assert validation["validation_status"] == (
        "physical_property_source_search_receipts_validated"
    )
    assert validation["search_receipt_count"] == 2
    assert validation["open_search_count"] == 0
    assert validation["candidate_receipt_created_count"] == 2
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert {receipt.symbol for receipt in receipts} == {"Pa", "Bk"}
    assert protactinium.field_name == "boiling_point_k"
    assert berkelium.field_name == "boiling_point_k"
    assert protactinium.search_status == "source_search_complete_candidate_receipt_created"
    assert protactinium.candidate_receipt_id.endswith("Z091-Pa-boiling_point_k-LANL")
    assert "source_url_or_citation" in protactinium.required_evidence
    assert protactinium.closes_gap is False
    assert berkelium.seed_mutation_allowed is False
    assert protactinium.validate() == []


def test_partial_physical_property_source_search_receipts_track_two_field_gaps():
    receipts = list_partial_physical_property_source_search_receipts()
    validation = validate_partial_physical_property_source_search_receipts(receipts)
    francium = get_partial_physical_property_source_search_receipt("Fr")

    assert validation["validation_status"] == (
        "partial_physical_property_source_search_receipts_validated"
    )
    assert validation["search_receipt_count"] == 7
    assert validation["open_search_count"] == 7
    assert validation["field_search_count"] == 14
    assert validation["gap_closure_count"] == 0
    assert validation["seed_mutation_allowed_count"] == 0
    assert {receipt.symbol for receipt in receipts} == {
        "Fr",
        "Cf",
        "Es",
        "Fm",
        "Md",
        "No",
        "Lr",
    }
    assert francium.missing_fields == ("boiling_point_k", "density_value")
    assert len(francium.field_searches) == 2
    assert francium.closes_gap is False
    assert francium.seed_mutation_allowed is False
    assert francium.validate() == []


def test_local_api_exposes_evidence_routes():
    isotope_list = handle_api_request("GET", "/evidence/isotopes")
    carbon_14 = handle_api_request("GET", "/evidence/isotopes/C?mass_number=14")
    unresolved_isotopes = handle_api_request("GET", "/evidence/isotopes/unresolved")
    lithium_isotope = handle_api_request("GET", "/evidence/isotopes/unresolved/Li")
    common_ion_list = handle_api_request("GET", "/evidence/common-ions")
    iron = handle_api_request("GET", "/evidence/common-ions/Fe")
    unresolved_common_ions = handle_api_request("GET", "/evidence/common-ions/unresolved")
    oxygen_common_ion = handle_api_request("GET", "/evidence/common-ions/unresolved/O")
    physical_properties = handle_api_request("GET", "/evidence/physical-properties")
    unresolved_properties = handle_api_request("GET", "/evidence/physical-properties/unresolved")
    astatine = handle_api_request("GET", "/evidence/physical-properties/unresolved/At")
    astatine_gap = handle_api_request("GET", "/evidence/physical-properties/gaps/At")
    astatine_workplan = handle_api_request(
        "GET",
        "/evidence/physical-properties/workplan/At",
    )
    protactinium_source_search = handle_api_request(
        "GET",
        "/evidence/physical-properties/source-search/Pa",
    )
    francium_partial_search = handle_api_request(
        "GET",
        "/evidence/physical-properties/partial-source-search/Fr",
    )
    astatine_policy = handle_api_request(
        "GET",
        "/evidence/physical-properties/secondary-source-policy/At",
    )
    secondary_receipts = handle_api_request(
        "GET",
        "/evidence/physical-properties/secondary-evidence",
    )
    secondary_admission = handle_api_request(
        "GET",
        "/evidence/physical-properties/secondary-evidence/admission/At",
    )
    physical_property_conflict = handle_api_request(
        "GET",
        "/evidence/physical-properties/conflicts/At",
    )
    physical_property_corroboration = handle_api_request(
        "GET",
        "/evidence/physical-properties/corroboration/Bk",
    )
    physical_property_review = handle_api_request(
        "GET",
        "/evidence/physical-properties/review/Cf",
    )
    physical_property_gap_closure = handle_api_request(
        "GET",
        "/evidence/physical-properties/gap-closure/Cf",
    )
    physical_property_closure_approval = handle_api_request(
        "GET",
        "/evidence/physical-properties/closure-approval/Cf",
    )
    physical_property_seed_update = handle_api_request(
        "GET",
        "/evidence/physical-properties/seed-update/Cf",
    )
    physical_property_escalation = handle_api_request(
        "GET",
        "/evidence/physical-properties/escalations/At",
    )
    physical_property_escalation_search = handle_api_request(
        "GET",
        "/evidence/physical-properties/escalation-search/At",
    )
    physical_property_escalation_resolution = handle_api_request(
        "GET",
        "/evidence/physical-properties/escalation-resolution/At",
    )
    physical_property_operator_decision = handle_api_request(
        "GET",
        "/evidence/physical-properties/operator-decisions/At",
    )
    physical_property_continued_evidence = handle_api_request(
        "GET",
        "/evidence/physical-properties/continued-evidence/At",
    )
    physical_property_no_candidate = handle_api_request(
        "GET",
        "/evidence/physical-properties/no-candidate/Fm",
    )
    secondary_template = handle_api_request(
        "GET",
        "/evidence/physical-properties/secondary-evidence/template/At",
    )
    bromine = handle_api_request("GET", "/evidence/physical-properties/Br")

    assert isotope_list.status_code == 200
    assert isotope_list.payload["validation"]["record_count"] == 13
    assert carbon_14.status_code == 200
    assert carbon_14.payload["records"][0]["isotope_id"] == "MSPEE-Z006-C-isotope-14"
    assert unresolved_isotopes.status_code == 200
    assert unresolved_isotopes.payload["validation"]["record_count"] == 113
    assert lithium_isotope.status_code == 200
    assert lithium_isotope.payload["record"]["evidence_domain"] == "isotope_evidence"
    assert common_ion_list.status_code == 200
    assert common_ion_list.payload["validation"]["record_count"] == 9
    assert iron.status_code == 200
    assert {record["charge"] for record in iron.payload["records"]} == {2, 3}
    assert unresolved_common_ions.status_code == 200
    assert unresolved_common_ions.payload["validation"]["record_count"] == 47
    assert oxygen_common_ion.status_code == 200
    assert oxygen_common_ion.payload["record"]["evidence_domain"] == "common_ion_evidence"
    assert physical_properties.status_code == 200
    assert physical_properties.payload["validation"]["record_count"] == 93
    assert bromine.status_code == 200
    assert bromine.payload["record"]["standard_state"] == "Liquid"
    assert bromine.payload["record"]["density_value"] == 3.11
    assert unresolved_properties.status_code == 200
    assert unresolved_properties.payload["validation"]["record_count"] == 25
    assert astatine.status_code == 200
    assert astatine.payload["record"]["missing_fields"] == ("boiling_point_k",)
    assert astatine_gap.status_code == 200
    assert astatine_gap.payload["receipt"]["blocks_promotion_spans"] == ["Cs-Rn"]
    assert astatine_gap.payload["receipt"]["no_guess_policy"] is True
    assert astatine_workplan.status_code == 200
    assert astatine_workplan.payload["item"]["work_status"] == "conflict_blocked_promotion"
    assert protactinium_source_search.status_code == 200
    assert protactinium_source_search.payload["receipt"]["search_status"] == (
        "source_search_complete_candidate_receipt_created"
    )
    assert francium_partial_search.status_code == 200
    assert francium_partial_search.payload["receipt"]["search_status"] == (
        "partial_source_search_open"
    )
    assert astatine_policy.status_code == 200
    assert astatine_policy.payload["policy"]["gap_closure_status"] == "gap_not_closed_by_policy"
    assert secondary_receipts.status_code == 200
    assert secondary_receipts.payload["validation"]["receipt_count"] == 8
    assert secondary_receipts.payload["validation"]["admitted_count"] == 0
    assert secondary_admission.status_code == 200
    assert secondary_admission.payload["decision"]["closes_gap"] is False
    assert physical_property_conflict.status_code == 200
    assert physical_property_conflict.payload["receipt"]["resolution_decision"] == (
        "blocked_pending_higher_precedence_source"
    )
    assert physical_property_corroboration.status_code == 200
    assert physical_property_corroboration.payload["receipt"]["review_decision"] == (
        "blocked_pending_corroborating_source"
    )
    assert physical_property_review.status_code == 200
    assert physical_property_review.payload["receipt"]["review_decision"] == (
        "resolved_admit_candidate"
    )
    assert physical_property_gap_closure.status_code == 200
    assert physical_property_gap_closure.payload["decision"]["closure_status"] == (
        "gap_closure_ready_pending_operator_approval"
    )
    assert physical_property_gap_closure.payload["decision"]["closes_gap"] is False
    assert physical_property_closure_approval.status_code == 200
    assert physical_property_closure_approval.payload["receipt"]["approval_status"] == (
        "closure_approval_deferred"
    )
    assert physical_property_closure_approval.payload["receipt"]["seed_mutation_allowed"] is False
    assert physical_property_seed_update.status_code == 200
    assert physical_property_seed_update.payload["receipt"]["update_status"] == (
        "seed_update_blocked_by_deferred_approval"
    )
    assert physical_property_seed_update.payload["receipt"]["seed_update_applied"] is False
    assert physical_property_escalation.status_code == 200
    assert physical_property_escalation.payload["receipt"]["escalation_class"] == (
        "higher_precedence_source_required"
    )
    assert physical_property_escalation.payload["receipt"]["closes_gap"] is False
    assert physical_property_escalation_search.status_code == 200
    assert physical_property_escalation_search.payload["receipt"]["search_status"] == (
        "higher_precedence_source_not_found"
    )
    assert physical_property_escalation_search.payload["receipt"]["closes_gap"] is False
    assert physical_property_escalation_resolution.status_code == 200
    assert physical_property_escalation_resolution.payload["receipt"]["resolution_status"] == (
        "conflict_resolution_blocked_pending_operator_decision"
    )
    assert (
        physical_property_escalation_resolution.payload["receipt"]["final_resolution_applied"]
        is False
    )
    assert physical_property_operator_decision.status_code == 200
    assert physical_property_operator_decision.payload["receipt"][
        "operator_decision_status"
    ] == "operator_decision_deferred"
    assert (
        physical_property_operator_decision.payload["receipt"]["final_resolution_applied"]
        is False
    )
    assert physical_property_continued_evidence.status_code == 200
    assert physical_property_continued_evidence.payload["plan"]["plan_status"] == (
        "continued_evidence_required"
    )
    assert physical_property_continued_evidence.payload["plan"]["closes_gap"] is False
    assert physical_property_no_candidate.status_code == 200
    assert physical_property_no_candidate.payload["receipt"]["review_decision"] == (
        "blocked_no_admissible_candidate_found"
    )
    assert secondary_template.status_code == 200
    assert secondary_template.payload["template"]["field_name"] == "boiling_point_k"


def test_element_cli_prints_evidence_records(capsys):
    cmd_elements(
        symbol="C",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        isotope_mass=14,
        isotope_evidence=True,
    )
    isotope_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Fe",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        common_ion_evidence=True,
    )
    common_ion_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Li",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        unresolved_isotope_evidence=True,
    )
    unresolved_isotope_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="O",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        unresolved_common_ion_evidence=True,
    )
    unresolved_common_ion_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Br",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_evidence=True,
    )
    property_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="At",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        unresolved_physical_property_evidence=True,
    )
    unresolved_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="At",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_conflict_resolution=True,
    )
    conflict_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Bk",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_corroboration_review=True,
    )
    corroboration_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Cf",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_review=True,
    )
    review_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Cf",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_gap_closure=True,
    )
    gap_closure_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Cf",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_closure_approval=True,
    )
    closure_approval_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Cf",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_seed_update=True,
    )
    seed_update_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="At",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_escalation=True,
    )
    escalation_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="At",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_escalation_search=True,
    )
    escalation_search_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="At",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_escalation_resolution=True,
    )
    escalation_resolution_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="At",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_operator_decision=True,
    )
    operator_decision_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="At",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_continued_evidence=True,
    )
    continued_evidence_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Cf",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_secondary_evidence=True,
    )
    secondary_evidence_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Fm",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_no_candidate_review=True,
    )
    no_candidate_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="At",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_gap_workplan=True,
    )
    workplan_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Pa",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        physical_property_source_search=True,
    )
    source_search_output = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="Fr",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        partial_physical_property_source_search=True,
    )
    partial_search_output = json.loads(capsys.readouterr().out)

    assert isotope_output["records"][0]["isotope_id"] == "MSPEE-Z006-C-isotope-14"
    assert isotope_output["records"][0]["decay_mode"] == "beta_minus"
    assert {record["charge"] for record in common_ion_output["records"]} == {2, 3}
    assert unresolved_isotope_output["records"][0]["evidence_domain"] == "isotope_evidence"
    assert unresolved_common_ion_output["records"][0]["evidence_domain"] == (
        "common_ion_evidence"
    )
    assert property_output["records"][0]["standard_state"] == "Liquid"
    assert property_output["records"][0]["boiling_point_k"] == 331.95
    assert unresolved_output["records"][0]["symbol"] == "At"
    assert unresolved_output["records"][0]["missing_fields"] == ["boiling_point_k"]
    assert conflict_output["receipts"][0]["resolution_decision"] == (
        "blocked_pending_higher_precedence_source"
    )
    assert corroboration_output["receipts"][0]["review_decision"] == (
        "blocked_pending_corroborating_source"
    )
    assert review_output["receipts"][0]["review_decision"] == "resolved_admit_candidate"
    assert gap_closure_output["decisions"][0]["closure_status"] == (
        "gap_closure_ready_pending_operator_approval"
    )
    assert closure_approval_output["receipts"][0]["approval_status"] == (
        "closure_approval_deferred"
    )
    assert seed_update_output["receipts"][0]["update_status"] == (
        "seed_update_blocked_by_deferred_approval"
    )
    assert seed_update_output["receipts"][0]["seed_update_applied"] is False
    assert escalation_output["receipts"][0]["escalation_class"] == (
        "higher_precedence_source_required"
    )
    assert escalation_output["receipts"][0]["closes_gap"] is False
    assert escalation_search_output["receipts"][0]["search_status"] == (
        "higher_precedence_source_not_found"
    )
    assert escalation_search_output["receipts"][0]["closes_gap"] is False
    assert escalation_resolution_output["receipts"][0]["resolution_status"] == (
        "conflict_resolution_blocked_pending_operator_decision"
    )
    assert escalation_resolution_output["receipts"][0]["final_resolution_applied"] is False
    assert operator_decision_output["receipts"][0]["operator_decision_status"] == (
        "operator_decision_deferred"
    )
    assert operator_decision_output["receipts"][0]["final_resolution_applied"] is False
    assert continued_evidence_output["plans"][0]["plan_status"] == (
        "continued_evidence_required"
    )
    assert continued_evidence_output["plans"][0]["closes_gap"] is False
    assert {receipt["field_name"] for receipt in secondary_evidence_output["receipts"]} == {
        "boiling_point_k",
        "density_value",
    }
    assert no_candidate_output["receipts"][0]["review_decision"] == (
        "blocked_no_admissible_candidate_found"
    )
    assert workplan_output["items"][0]["work_status"] == "conflict_blocked_promotion"
    assert source_search_output["receipts"][0]["search_status"] == (
        "source_search_complete_candidate_receipt_created"
    )
    assert partial_search_output["receipts"][0]["search_status"] == (
        "partial_source_search_open"
    )
