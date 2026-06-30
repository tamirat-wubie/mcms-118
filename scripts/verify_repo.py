from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mcms.api import handle_api_request  # noqa: E402
from mcms.elements import (  # noqa: E402
    build_atom_behavior_profile,
    build_element_dashboard_view_model,
    build_element_relation_graph,
    build_ion_instance,
    build_isotope_instance,
    build_matter_behavior_profile,
    build_physical_property_secondary_evidence_template,
    element_seed_json_schema,
    element_snapshot_json_schema,
    find_behavior_tag_overlay_record,
    find_common_ion_evidence_records,
    find_configuration_evidence_record,
    find_frontier_valence_signature_record,
    find_isotope_evidence_records,
    find_oxidation_state_evidence_record,
    find_physical_property_evidence_record,
    find_relation_overlay_record,
    find_unresolved_common_ion_evidence_record,
    find_unresolved_isotope_evidence_record,
    find_unresolved_physical_property_evidence_record,
    get_atom_behavior_gap_work_item,
    get_cs_rn_promotion_readiness_profile,
    get_element_readiness_score,
    get_f_block_expansion_profile,
    get_isotope_candidate_admission_receipt,
    get_partial_physical_property_source_search_receipt,
    get_period_5_level_2_profile,
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
    get_physical_property_secondary_evidence_receipt,
    get_physical_property_secondary_source_policy,
    get_physical_property_seed_update_receipt,
    get_physical_property_source_search_receipt,
    get_promotion_batch_policy_receipt,
    get_promotion_decision_receipt,
    get_seed_element,
    get_snapshot_record,
    list_atom_behavior_gap_receipts,
    list_atom_behavior_gap_work_items,
    list_atom_behavior_profiles,
    list_behavior_tag_overlay_records,
    list_common_ion_evidence_records,
    list_configuration_evidence_records,
    list_cs_rn_promotion_readiness_profiles,
    list_element_readiness_scores,
    list_f_block_expansion_profiles,
    list_frontier_valence_signature_records,
    list_full_snapshot_records,
    list_isotope_candidate_admission_receipts,
    list_isotope_candidate_evidence_receipts,
    list_isotope_evidence_records,
    list_isotope_source_policies,
    list_isotope_source_search_receipts,
    list_matter_behavior_profiles,
    list_oxidation_state_evidence_records,
    list_partial_physical_property_source_search_receipts,
    list_period_5_level_2_profiles,
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
    list_promotion_decision_receipts,
    list_relation_overlay_records,
    list_seed_elements,
    list_unresolved_common_ion_evidence_records,
    list_unresolved_isotope_evidence_records,
    list_unresolved_physical_property_evidence_records,
    validate_atom_behavior_gap_receipts,
    validate_atom_behavior_gap_work_items,
    validate_atom_behavior_profiles,
    validate_behavior_tag_overlay_records,
    validate_common_ion_evidence_records,
    validate_configuration_evidence_records,
    validate_cs_rn_promotion_readiness_profiles,
    validate_element_readiness_scores,
    validate_f_block_expansion_profiles,
    validate_frontier_valence_signature_records,
    validate_full_snapshot,
    validate_isotope_candidate_admission_receipts,
    validate_isotope_candidate_evidence_receipts,
    validate_isotope_evidence_records,
    validate_isotope_source_policies,
    validate_isotope_source_search_receipts,
    validate_matter_behavior_profiles,
    validate_oxidation_state_evidence_records,
    validate_partial_physical_property_source_search_receipts,
    validate_period_5_level_2_profiles,
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
    validate_promotion_batch_policy_receipt,
    validate_promotion_decision_receipts,
    validate_relation_overlay_records,
    validate_seed_pack,
    validate_unresolved_evidence_records,
    validate_unresolved_physical_property_evidence_records,
)
from mcms.module_registry import all_modules  # noqa: E402
from mcms.phase_registry import list_phases  # noqa: E402

DRIFT_SCRIPT_PATH = ROOT / "scripts" / "check_element_level2_drift.py"
DRIFT_SCRIPT_SPEC = importlib.util.spec_from_file_location(
    "verify_repo_level2_drift",
    DRIFT_SCRIPT_PATH,
)
assert DRIFT_SCRIPT_SPEC is not None
assert DRIFT_SCRIPT_SPEC.loader is not None
DRIFT_SCRIPT_MODULE = importlib.util.module_from_spec(DRIFT_SCRIPT_SPEC)
sys.modules[DRIFT_SCRIPT_SPEC.name] = DRIFT_SCRIPT_MODULE
DRIFT_SCRIPT_SPEC.loader.exec_module(DRIFT_SCRIPT_MODULE)
SourceLevel2ChemistryRow = DRIFT_SCRIPT_MODULE.SourceLevel2ChemistryRow
build_period_5_level_2_drift_report = DRIFT_SCRIPT_MODULE.build_period_5_level_2_drift_report

PHYSICAL_PROPERTY_DRIFT_SCRIPT_PATH = (
    ROOT / "scripts" / "check_element_physical_property_drift.py"
)
PHYSICAL_PROPERTY_DRIFT_SCRIPT_SPEC = importlib.util.spec_from_file_location(
    "verify_repo_physical_property_drift",
    PHYSICAL_PROPERTY_DRIFT_SCRIPT_PATH,
)
assert PHYSICAL_PROPERTY_DRIFT_SCRIPT_SPEC is not None
assert PHYSICAL_PROPERTY_DRIFT_SCRIPT_SPEC.loader is not None
PHYSICAL_PROPERTY_DRIFT_SCRIPT_MODULE = importlib.util.module_from_spec(
    PHYSICAL_PROPERTY_DRIFT_SCRIPT_SPEC
)
sys.modules[PHYSICAL_PROPERTY_DRIFT_SCRIPT_SPEC.name] = PHYSICAL_PROPERTY_DRIFT_SCRIPT_MODULE
PHYSICAL_PROPERTY_DRIFT_SCRIPT_SPEC.loader.exec_module(PHYSICAL_PROPERTY_DRIFT_SCRIPT_MODULE)
SourcePhysicalPropertyRow = PHYSICAL_PROPERTY_DRIFT_SCRIPT_MODULE.SourcePhysicalPropertyRow
build_physical_property_drift_report = (
    PHYSICAL_PROPERTY_DRIFT_SCRIPT_MODULE.build_physical_property_drift_report
)

REQUIRED_KEYS = {
    "phase", "phase_id", "slug", "title", "status", "maturity", "domain", "layer",
    "objective", "capability_chain", "relationships", "boundary", "blocked_claims", "invariants",
    "claim_types", "evidence_policy", "risk_profile", "artifacts", "modules", "module_count",
    "status_vocabulary", "inputs", "outputs", "implementation_truth", "upgrade_path", "audit_metadata",
}

STANDARD_FILES = (
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/NAMING_STANDARD.md",
    "docs/PROJECT_HISTORY.md",
    "docs/STANDARDS_PROFILE.md",
)


def main() -> None:
    phases = list_phases()
    modules = all_modules()
    elements = list_seed_elements()
    snapshot_records = list_full_snapshot_records()
    element_seed_result = validate_seed_pack(elements)
    snapshot_result = validate_full_snapshot(snapshot_records)
    element_schema = element_seed_json_schema()
    snapshot_schema = element_snapshot_json_schema()
    f_block_profiles = list_f_block_expansion_profiles()
    f_block_result = validate_f_block_expansion_profiles(f_block_profiles)
    period_5_level_2_profiles = list_period_5_level_2_profiles()
    period_5_level_2_result = validate_period_5_level_2_profiles(period_5_level_2_profiles)
    isotope_evidence_records = list_isotope_evidence_records()
    isotope_evidence_result = validate_isotope_evidence_records(isotope_evidence_records)
    common_ion_evidence_records = list_common_ion_evidence_records()
    common_ion_evidence_result = validate_common_ion_evidence_records(
        common_ion_evidence_records
    )
    unresolved_isotope_evidence_records = list_unresolved_isotope_evidence_records()
    unresolved_isotope_evidence_result = validate_unresolved_evidence_records(
        unresolved_isotope_evidence_records,
        expected_domain="isotope_evidence",
    )
    unresolved_common_ion_evidence_records = list_unresolved_common_ion_evidence_records()
    unresolved_common_ion_evidence_result = validate_unresolved_evidence_records(
        unresolved_common_ion_evidence_records,
        expected_domain="common_ion_evidence",
    )
    physical_property_evidence_records = list_physical_property_evidence_records()
    physical_property_evidence_result = validate_physical_property_evidence_records(
        physical_property_evidence_records
    )
    unresolved_physical_property_evidence_records = (
        list_unresolved_physical_property_evidence_records()
    )
    unresolved_physical_property_evidence_result = (
        validate_unresolved_physical_property_evidence_records(
            unresolved_physical_property_evidence_records
        )
    )
    physical_property_gap_audit_receipts = list_physical_property_gap_audit_receipts()
    physical_property_gap_audit_result = validate_physical_property_gap_audit_receipts(
        physical_property_gap_audit_receipts
    )
    physical_property_gap_work_items = list_physical_property_gap_work_items()
    physical_property_gap_work_result = validate_physical_property_gap_work_items(
        physical_property_gap_work_items
    )
    physical_property_source_search_receipts = list_physical_property_source_search_receipts()
    physical_property_source_search_result = validate_physical_property_source_search_receipts(
        physical_property_source_search_receipts
    )
    partial_physical_property_source_search_receipts = (
        list_partial_physical_property_source_search_receipts()
    )
    partial_physical_property_source_search_result = (
        validate_partial_physical_property_source_search_receipts(
            partial_physical_property_source_search_receipts
        )
    )
    physical_property_secondary_source_policies = (
        list_physical_property_secondary_source_policies()
    )
    physical_property_secondary_source_policy_result = (
        validate_physical_property_secondary_source_policies(
            physical_property_secondary_source_policies
        )
    )
    physical_property_secondary_evidence_receipts = (
        list_physical_property_secondary_evidence_receipts()
    )
    physical_property_secondary_evidence_result = (
        validate_physical_property_secondary_evidence_receipts(
            physical_property_secondary_evidence_receipts
        )
    )
    physical_property_secondary_evidence_admission_decisions = (
        list_physical_property_secondary_evidence_admission_decisions()
    )
    physical_property_secondary_evidence_admission_result = (
        validate_physical_property_secondary_evidence_admission_decisions(
            physical_property_secondary_evidence_admission_decisions
        )
    )
    physical_property_conflict_resolution_receipts = (
        list_physical_property_conflict_resolution_receipts()
    )
    physical_property_conflict_resolution_result = (
        validate_physical_property_conflict_resolution_receipts(
            physical_property_conflict_resolution_receipts
        )
    )
    physical_property_corroboration_review_receipts = (
        list_physical_property_corroboration_review_receipts()
    )
    physical_property_corroboration_review_result = (
        validate_physical_property_corroboration_review_receipts(
            physical_property_corroboration_review_receipts
        )
    )
    physical_property_review_receipts = list_physical_property_review_receipts()
    physical_property_review_result = validate_physical_property_review_receipts(
        physical_property_review_receipts
    )
    physical_property_gap_closure_decisions = list_physical_property_gap_closure_decisions()
    physical_property_gap_closure_result = validate_physical_property_gap_closure_decisions(
        physical_property_gap_closure_decisions
    )
    physical_property_closure_approval_receipts = (
        list_physical_property_closure_approval_receipts()
    )
    physical_property_closure_approval_result = (
        validate_physical_property_closure_approval_receipts(
            physical_property_closure_approval_receipts
        )
    )
    physical_property_seed_update_receipts = list_physical_property_seed_update_receipts()
    physical_property_seed_update_result = validate_physical_property_seed_update_receipts(
        physical_property_seed_update_receipts
    )
    physical_property_escalation_receipts = list_physical_property_escalation_receipts()
    physical_property_escalation_result = validate_physical_property_escalation_receipts(
        physical_property_escalation_receipts
    )
    physical_property_escalation_search_receipts = (
        list_physical_property_escalation_search_receipts()
    )
    physical_property_escalation_search_result = (
        validate_physical_property_escalation_search_receipts(
            physical_property_escalation_search_receipts
        )
    )
    physical_property_escalation_resolution_receipts = (
        list_physical_property_escalation_resolution_receipts()
    )
    physical_property_escalation_resolution_result = (
        validate_physical_property_escalation_resolution_receipts(
            physical_property_escalation_resolution_receipts
        )
    )
    physical_property_operator_decision_receipts = (
        list_physical_property_operator_decision_receipts()
    )
    physical_property_operator_decision_result = (
        validate_physical_property_operator_decision_receipts(
            physical_property_operator_decision_receipts
        )
    )
    physical_property_continued_evidence_plans = (
        list_physical_property_continued_evidence_plans()
    )
    physical_property_continued_evidence_result = (
        validate_physical_property_continued_evidence_plans(
            physical_property_continued_evidence_plans
        )
    )
    physical_property_no_candidate_review_receipts = (
        list_physical_property_no_candidate_review_receipts()
    )
    physical_property_no_candidate_review_result = (
        validate_physical_property_no_candidate_review_receipts(
            physical_property_no_candidate_review_receipts
        )
    )
    matter_behavior_profiles = list_matter_behavior_profiles()
    matter_behavior_result = validate_matter_behavior_profiles(matter_behavior_profiles)
    atom_behavior_profiles = list_atom_behavior_profiles()
    atom_behavior_result = validate_atom_behavior_profiles(atom_behavior_profiles)
    atom_behavior_gap_receipts = list_atom_behavior_gap_receipts()
    atom_behavior_gap_result = validate_atom_behavior_gap_receipts(atom_behavior_gap_receipts)
    atom_behavior_gap_work_items = list_atom_behavior_gap_work_items()
    atom_behavior_gap_work_result = validate_atom_behavior_gap_work_items(
        atom_behavior_gap_work_items
    )
    element_readiness_scores = list_element_readiness_scores()
    element_readiness_result = validate_element_readiness_scores(
        element_readiness_scores
    )
    isotope_source_policies = list_isotope_source_policies()
    isotope_source_policy_result = validate_isotope_source_policies(
        isotope_source_policies
    )
    isotope_source_search_receipts = list_isotope_source_search_receipts()
    isotope_source_search_result = validate_isotope_source_search_receipts(
        isotope_source_search_receipts
    )
    isotope_candidate_evidence_receipts = list_isotope_candidate_evidence_receipts()
    isotope_candidate_evidence_result = validate_isotope_candidate_evidence_receipts(
        isotope_candidate_evidence_receipts
    )
    isotope_candidate_admission_receipts = list_isotope_candidate_admission_receipts()
    isotope_candidate_admission_result = validate_isotope_candidate_admission_receipts(
        isotope_candidate_admission_receipts
    )
    cs_rn_promotion_profiles = list_cs_rn_promotion_readiness_profiles()
    cs_rn_promotion_result = validate_cs_rn_promotion_readiness_profiles(
        cs_rn_promotion_profiles
    )
    configuration_evidence_records = list_configuration_evidence_records()
    configuration_evidence_result = validate_configuration_evidence_records(
        configuration_evidence_records
    )
    frontier_valence_records = list_frontier_valence_signature_records()
    frontier_valence_result = validate_frontier_valence_signature_records(
        frontier_valence_records
    )
    oxidation_state_evidence_records = list_oxidation_state_evidence_records()
    oxidation_state_evidence_result = validate_oxidation_state_evidence_records(
        oxidation_state_evidence_records
    )
    behavior_tag_records = list_behavior_tag_overlay_records()
    behavior_tag_result = validate_behavior_tag_overlay_records(behavior_tag_records)
    relation_overlay_records = list_relation_overlay_records()
    relation_overlay_result = validate_relation_overlay_records(relation_overlay_records)
    promotion_decision_receipts = list_promotion_decision_receipts()
    promotion_decision_result = validate_promotion_decision_receipts(
        promotion_decision_receipts
    )
    promotion_batch_policy = get_promotion_batch_policy_receipt()
    promotion_batch_policy_result = validate_promotion_batch_policy_receipt(
        promotion_batch_policy
    )
    element_schema_validator = Draft202012Validator(element_schema)
    snapshot_schema_validator = Draft202012Validator(snapshot_schema)
    assert len(phases) == 135, len(phases)
    assert len(modules) >= 180, len(modules)
    assert len(elements) == 54, len(elements)
    assert len(snapshot_records) == 118, len(snapshot_records)
    assert element_seed_result.validation_status == "element_seed_pack_validated", element_seed_result
    assert not element_seed_result.invalid_elements, element_seed_result.invalid_elements
    assert snapshot_result.validation_status == "full_element_snapshot_validated", snapshot_result
    assert not snapshot_result.invalid_elements, snapshot_result.invalid_elements
    assert f_block_result.validation_status == "f_block_expansion_profiles_validated", f_block_result
    assert f_block_result.profile_count == 30, f_block_result
    assert f_block_result.lanthanide_count == 15, f_block_result
    assert f_block_result.actinide_count == 15, f_block_result
    assert period_5_level_2_result.validation_status == (
        "period_5_level_2_snapshot_profiles_validated"
    ), period_5_level_2_result
    assert period_5_level_2_result.profile_count == 18, period_5_level_2_result
    assert period_5_level_2_result.atomic_number_span == (37, 54), period_5_level_2_result
    assert isotope_evidence_result["validation_status"] == "isotope_evidence_records_validated", (
        isotope_evidence_result
    )
    assert isotope_evidence_result["record_count"] == 178, isotope_evidence_result
    assert isotope_evidence_result["radioisotope_count"] == 6, isotope_evidence_result
    assert common_ion_evidence_result["validation_status"] == (
        "common_ion_evidence_records_validated"
    ), common_ion_evidence_result
    assert common_ion_evidence_result["record_count"] == 9, common_ion_evidence_result
    assert unresolved_isotope_evidence_result["validation_status"] == (
        "isotope_evidence_unresolved_records_validated"
    ), unresolved_isotope_evidence_result
    assert unresolved_isotope_evidence_result["record_count"] == 64, (
        unresolved_isotope_evidence_result
    )
    assert unresolved_common_ion_evidence_result["validation_status"] == (
        "common_ion_evidence_unresolved_records_validated"
    ), unresolved_common_ion_evidence_result
    assert unresolved_common_ion_evidence_result["record_count"] == 47, (
        unresolved_common_ion_evidence_result
    )
    assert physical_property_evidence_result["validation_status"] == (
        "physical_property_evidence_records_validated"
    ), physical_property_evidence_result
    assert physical_property_evidence_result["record_count"] == 93, (
        physical_property_evidence_result
    )
    assert physical_property_evidence_result["standard_states"] == (
        "Gas",
        "Liquid",
        "Solid",
    ), physical_property_evidence_result
    assert unresolved_physical_property_evidence_result["validation_status"] == (
        "unresolved_physical_property_evidence_records_validated"
    ), unresolved_physical_property_evidence_result
    assert unresolved_physical_property_evidence_result["record_count"] == 25, (
        unresolved_physical_property_evidence_result
    )
    assert physical_property_gap_audit_result["validation_status"] == (
        "physical_property_gap_audit_receipts_validated"
    ), physical_property_gap_audit_result
    assert physical_property_gap_audit_result["receipt_count"] == 25, (
        physical_property_gap_audit_result
    )
    assert physical_property_gap_audit_result["cs_rn_blocking_gap_count"] == 1, (
        physical_property_gap_audit_result
    )
    assert physical_property_gap_audit_result["boiling_point_gap_count"] == 25, (
        physical_property_gap_audit_result
    )
    assert physical_property_gap_work_result["validation_status"] == (
        "physical_property_gap_work_items_validated"
    ), physical_property_gap_work_result
    assert physical_property_gap_work_result["work_item_count"] == 25, (
        physical_property_gap_work_result
    )
    assert physical_property_gap_work_result["conflict_blocked_count"] == 1, (
        physical_property_gap_work_result
    )
    assert physical_property_gap_work_result["single_field_source_search_count"] == 2, (
        physical_property_gap_work_result
    )
    assert physical_property_gap_work_result["partial_property_source_search_count"] == 7, (
        physical_property_gap_work_result
    )
    assert physical_property_gap_work_result["synthetic_superheavy_uncertainty_count"] == 15, (
        physical_property_gap_work_result
    )
    assert physical_property_gap_work_result["gap_closure_count"] == 0, (
        physical_property_gap_work_result
    )
    assert physical_property_gap_work_result["seed_mutation_allowed_count"] == 0, (
        physical_property_gap_work_result
    )
    assert physical_property_source_search_result["validation_status"] == (
        "physical_property_source_search_receipts_validated"
    ), physical_property_source_search_result
    assert physical_property_source_search_result["search_receipt_count"] == 2, (
        physical_property_source_search_result
    )
    assert physical_property_source_search_result["open_search_count"] == 0, (
        physical_property_source_search_result
    )
    assert physical_property_source_search_result["candidate_receipt_created_count"] == 2, (
        physical_property_source_search_result
    )
    assert physical_property_source_search_result["gap_closure_count"] == 0, (
        physical_property_source_search_result
    )
    assert physical_property_source_search_result["seed_mutation_allowed_count"] == 0, (
        physical_property_source_search_result
    )
    assert partial_physical_property_source_search_result["validation_status"] == (
        "partial_physical_property_source_search_receipts_validated"
    ), partial_physical_property_source_search_result
    assert partial_physical_property_source_search_result["search_receipt_count"] == 7, (
        partial_physical_property_source_search_result
    )
    assert partial_physical_property_source_search_result["open_search_count"] == 7, (
        partial_physical_property_source_search_result
    )
    assert partial_physical_property_source_search_result["field_search_count"] == 14, (
        partial_physical_property_source_search_result
    )
    assert partial_physical_property_source_search_result["gap_closure_count"] == 0, (
        partial_physical_property_source_search_result
    )
    assert partial_physical_property_source_search_result["seed_mutation_allowed_count"] == 0, (
        partial_physical_property_source_search_result
    )
    assert physical_property_secondary_source_policy_result["validation_status"] == (
        "physical_property_secondary_source_policies_validated"
    ), physical_property_secondary_source_policy_result
    assert physical_property_secondary_source_policy_result["policy_count"] == 25, (
        physical_property_secondary_source_policy_result
    )
    assert physical_property_secondary_source_policy_result["gap_closure_count"] == 0, (
        physical_property_secondary_source_policy_result
    )
    assert physical_property_secondary_source_policy_result["seed_mutation_allowed_count"] == 0, (
        physical_property_secondary_source_policy_result
    )
    assert physical_property_secondary_source_policy_result["candidate_source_count"] == 5, (
        physical_property_secondary_source_policy_result
    )
    assert physical_property_secondary_evidence_result["validation_status"] == (
        "physical_property_secondary_evidence_receipts_validated"
    ), physical_property_secondary_evidence_result
    assert physical_property_secondary_evidence_result["receipt_count"] == 8, (
        physical_property_secondary_evidence_result
    )
    assert physical_property_secondary_evidence_result["admitted_count"] == 0, (
        physical_property_secondary_evidence_result
    )
    assert physical_property_secondary_evidence_result["seed_mutation_allowed_count"] == 0, (
        physical_property_secondary_evidence_result
    )
    assert physical_property_secondary_evidence_admission_result["validation_status"] == (
        "physical_property_secondary_evidence_admission_decisions_validated"
    ), physical_property_secondary_evidence_admission_result
    assert physical_property_secondary_evidence_admission_result["decision_count"] == 8, (
        physical_property_secondary_evidence_admission_result
    )
    assert physical_property_secondary_evidence_admission_result[
        "admitted_gap_closure_count"
    ] == 0, physical_property_secondary_evidence_admission_result
    assert physical_property_secondary_evidence_admission_result["conflict_blocked_count"] == 3, (
        physical_property_secondary_evidence_admission_result
    )
    assert physical_property_secondary_evidence_admission_result[
        "corroboration_blocked_count"
    ] == 4, physical_property_secondary_evidence_admission_result
    assert physical_property_secondary_evidence_admission_result[
        "pending_review_count"
    ] == 1, physical_property_secondary_evidence_admission_result
    assert physical_property_conflict_resolution_result["validation_status"] == (
        "physical_property_conflict_resolution_receipts_validated"
    ), physical_property_conflict_resolution_result
    assert physical_property_conflict_resolution_result["receipt_count"] == 3, (
        physical_property_conflict_resolution_result
    )
    assert physical_property_conflict_resolution_result[
        "blocked_pending_higher_precedence_source_count"
    ] == 3, physical_property_conflict_resolution_result
    assert physical_property_conflict_resolution_result["gap_closure_count"] == 0, (
        physical_property_conflict_resolution_result
    )
    assert physical_property_conflict_resolution_result["seed_mutation_allowed_count"] == 0, (
        physical_property_conflict_resolution_result
    )
    assert physical_property_corroboration_review_result["validation_status"] == (
        "physical_property_corroboration_review_receipts_validated"
    ), physical_property_corroboration_review_result
    assert physical_property_corroboration_review_result["receipt_count"] == 4, (
        physical_property_corroboration_review_result
    )
    assert physical_property_corroboration_review_result[
        "blocked_pending_corroborating_source_count"
    ] == 4, physical_property_corroboration_review_result
    assert physical_property_corroboration_review_result["gap_closure_count"] == 0, (
        physical_property_corroboration_review_result
    )
    assert physical_property_corroboration_review_result["seed_mutation_allowed_count"] == 0, (
        physical_property_corroboration_review_result
    )
    assert physical_property_review_result["validation_status"] == (
        "physical_property_review_receipts_validated"
    ), physical_property_review_result
    assert physical_property_review_result["receipt_count"] == 1, physical_property_review_result
    assert physical_property_review_result["blocked_pending_source_review_count"] == 0, (
        physical_property_review_result
    )
    assert physical_property_review_result["resolved_admit_candidate_count"] == 1, (
        physical_property_review_result
    )
    assert physical_property_review_result["gap_closure_count"] == 0, (
        physical_property_review_result
    )
    assert physical_property_review_result["seed_mutation_allowed_count"] == 0, (
        physical_property_review_result
    )
    assert physical_property_gap_closure_result["validation_status"] == (
        "physical_property_gap_closure_decisions_validated"
    ), physical_property_gap_closure_result
    assert physical_property_gap_closure_result["decision_count"] == 1, (
        physical_property_gap_closure_result
    )
    assert physical_property_gap_closure_result[
        "ready_pending_operator_approval_count"
    ] == 1, physical_property_gap_closure_result
    assert physical_property_gap_closure_result["approved_for_seed_update_count"] == 0, (
        physical_property_gap_closure_result
    )
    assert physical_property_gap_closure_result["gap_closure_count"] == 0, (
        physical_property_gap_closure_result
    )
    assert physical_property_gap_closure_result["seed_mutation_allowed_count"] == 0, (
        physical_property_gap_closure_result
    )
    assert physical_property_closure_approval_result["validation_status"] == (
        "physical_property_closure_approval_receipts_validated"
    ), physical_property_closure_approval_result
    assert physical_property_closure_approval_result["receipt_count"] == 1, (
        physical_property_closure_approval_result
    )
    assert physical_property_closure_approval_result["deferred_approval_count"] == 1, (
        physical_property_closure_approval_result
    )
    assert physical_property_closure_approval_result["approved_for_seed_update_count"] == 0, (
        physical_property_closure_approval_result
    )
    assert physical_property_closure_approval_result["gap_closure_count"] == 0, (
        physical_property_closure_approval_result
    )
    assert physical_property_closure_approval_result["seed_mutation_allowed_count"] == 0, (
        physical_property_closure_approval_result
    )
    assert physical_property_seed_update_result["validation_status"] == (
        "physical_property_seed_update_receipts_validated"
    ), physical_property_seed_update_result
    assert physical_property_seed_update_result["receipt_count"] == 1, (
        physical_property_seed_update_result
    )
    assert physical_property_seed_update_result["blocked_by_deferred_approval_count"] == 1, (
        physical_property_seed_update_result
    )
    assert physical_property_seed_update_result["ready_to_apply_count"] == 0, (
        physical_property_seed_update_result
    )
    assert physical_property_seed_update_result["gap_closure_count"] == 0, (
        physical_property_seed_update_result
    )
    assert physical_property_seed_update_result["seed_mutation_allowed_count"] == 0, (
        physical_property_seed_update_result
    )
    assert physical_property_seed_update_result["seed_update_applied_count"] == 0, (
        physical_property_seed_update_result
    )
    assert physical_property_escalation_result["validation_status"] == (
        "physical_property_escalation_receipts_validated"
    ), physical_property_escalation_result
    assert physical_property_escalation_result["receipt_count"] == 8, (
        physical_property_escalation_result
    )
    assert physical_property_escalation_result[
        "higher_precedence_source_required_count"
    ] == 3, physical_property_escalation_result
    assert physical_property_escalation_result["corroborating_source_required_count"] == 4, (
        physical_property_escalation_result
    )
    assert physical_property_escalation_result["operator_approval_required_count"] == 1, (
        physical_property_escalation_result
    )
    assert physical_property_escalation_result["gap_closure_count"] == 0, (
        physical_property_escalation_result
    )
    assert physical_property_escalation_result["seed_mutation_allowed_count"] == 0, (
        physical_property_escalation_result
    )
    assert physical_property_escalation_search_result["validation_status"] == (
        "physical_property_escalation_search_receipts_validated"
    ), physical_property_escalation_search_result
    assert physical_property_escalation_search_result["search_receipt_count"] == 7, (
        physical_property_escalation_search_result
    )
    assert physical_property_escalation_search_result[
        "higher_precedence_source_not_found_count"
    ] == 3, physical_property_escalation_search_result
    assert physical_property_escalation_search_result[
        "corroborating_source_not_found_count"
    ] == 4, physical_property_escalation_search_result
    assert physical_property_escalation_search_result["gap_closure_count"] == 0, (
        physical_property_escalation_search_result
    )
    assert physical_property_escalation_search_result["seed_mutation_allowed_count"] == 0, (
        physical_property_escalation_search_result
    )
    assert physical_property_escalation_resolution_result["validation_status"] == (
        "physical_property_escalation_resolution_receipts_validated"
    ), physical_property_escalation_resolution_result
    assert physical_property_escalation_resolution_result["receipt_count"] == 7, (
        physical_property_escalation_resolution_result
    )
    assert physical_property_escalation_resolution_result[
        "conflict_resolution_blocked_count"
    ] == 3, physical_property_escalation_resolution_result
    assert physical_property_escalation_resolution_result[
        "candidate_rejection_recommended_count"
    ] == 4, physical_property_escalation_resolution_result
    assert physical_property_escalation_resolution_result[
        "final_resolution_applied_count"
    ] == 0, physical_property_escalation_resolution_result
    assert physical_property_escalation_resolution_result["gap_closure_count"] == 0, (
        physical_property_escalation_resolution_result
    )
    assert physical_property_escalation_resolution_result[
        "seed_mutation_allowed_count"
    ] == 0, physical_property_escalation_resolution_result
    assert physical_property_operator_decision_result["validation_status"] == (
        "physical_property_operator_decision_receipts_validated"
    ), physical_property_operator_decision_result
    assert physical_property_operator_decision_result["receipt_count"] == 7, (
        physical_property_operator_decision_result
    )
    assert physical_property_operator_decision_result["deferred_decision_count"] == 7, (
        physical_property_operator_decision_result
    )
    assert physical_property_operator_decision_result["approved_resolution_count"] == 0, (
        physical_property_operator_decision_result
    )
    assert physical_property_operator_decision_result["rejected_resolution_count"] == 0, (
        physical_property_operator_decision_result
    )
    assert physical_property_operator_decision_result[
        "final_resolution_applied_count"
    ] == 0, physical_property_operator_decision_result
    assert physical_property_operator_decision_result["gap_closure_count"] == 0, (
        physical_property_operator_decision_result
    )
    assert physical_property_operator_decision_result["seed_mutation_allowed_count"] == 0, (
        physical_property_operator_decision_result
    )
    assert physical_property_continued_evidence_result["validation_status"] == (
        "physical_property_continued_evidence_plans_validated"
    ), physical_property_continued_evidence_result
    assert physical_property_continued_evidence_result["plan_count"] == 7, (
        physical_property_continued_evidence_result
    )
    assert physical_property_continued_evidence_result[
        "continued_evidence_required_count"
    ] == 7, physical_property_continued_evidence_result
    assert physical_property_continued_evidence_result[
        "higher_precedence_source_discovery_count"
    ] == 3, physical_property_continued_evidence_result
    assert physical_property_continued_evidence_result[
        "independent_corroboration_discovery_count"
    ] == 4, physical_property_continued_evidence_result
    assert physical_property_continued_evidence_result[
        "final_resolution_applied_count"
    ] == 0, physical_property_continued_evidence_result
    assert physical_property_continued_evidence_result["gap_closure_count"] == 0, (
        physical_property_continued_evidence_result
    )
    assert physical_property_continued_evidence_result[
        "seed_mutation_allowed_count"
    ] == 0, physical_property_continued_evidence_result
    assert physical_property_no_candidate_review_result["validation_status"] == (
        "physical_property_no_candidate_review_receipts_validated"
    ), physical_property_no_candidate_review_result
    assert physical_property_no_candidate_review_result["receipt_count"] == 4, (
        physical_property_no_candidate_review_result
    )
    assert physical_property_no_candidate_review_result[
        "blocked_no_admissible_candidate_found_count"
    ] == 4, physical_property_no_candidate_review_result
    assert physical_property_no_candidate_review_result["field_review_count"] == 8, (
        physical_property_no_candidate_review_result
    )
    assert physical_property_no_candidate_review_result["gap_closure_count"] == 0, (
        physical_property_no_candidate_review_result
    )
    assert physical_property_no_candidate_review_result["seed_mutation_allowed_count"] == 0, (
        physical_property_no_candidate_review_result
    )
    assert matter_behavior_result["validation_status"] == "matter_behavior_profiles_validated", (
        matter_behavior_result
    )
    assert matter_behavior_result["profile_count"] == 54, matter_behavior_result
    assert atom_behavior_result["validation_status"] == "atom_behavior_profiles_validated", (
        atom_behavior_result
    )
    assert atom_behavior_result["profile_count"] == 178, atom_behavior_result
    assert atom_behavior_result["neutral_profile_count"] == 178, atom_behavior_result
    assert atom_behavior_result["stable_isotope_profile_count"] == 172, atom_behavior_result
    assert atom_behavior_result["radioisotope_profile_count"] == 6, atom_behavior_result
    carbon_14_atom_behavior = build_atom_behavior_profile("C", 14)
    assert carbon_14_atom_behavior.proton_count == 6, carbon_14_atom_behavior
    assert carbon_14_atom_behavior.neutron_count == 8, carbon_14_atom_behavior
    assert carbon_14_atom_behavior.electron_count == 6, carbon_14_atom_behavior
    assert "weak_decay_context=beta_minus" in carbon_14_atom_behavior.force_layer_basis, (
        carbon_14_atom_behavior
    )
    assert atom_behavior_gap_result["validation_status"] == (
        "atom_behavior_gap_receipts_validated"
    ), atom_behavior_gap_result
    assert atom_behavior_gap_result["receipt_count"] == 64, atom_behavior_gap_result
    assert atom_behavior_gap_result["isotope_only_gap_count"] == 0, atom_behavior_gap_result
    assert atom_behavior_gap_result["seed_and_matter_gap_count"] == 64, atom_behavior_gap_result
    assert atom_behavior_gap_work_result["validation_status"] == (
        "atom_behavior_gap_work_items_validated"
    ), atom_behavior_gap_work_result
    assert atom_behavior_gap_work_result["work_item_count"] == 64, (
        atom_behavior_gap_work_result
    )
    assert atom_behavior_gap_work_result["isotope_evidence_required_count"] == 0, (
        atom_behavior_gap_work_result
    )
    assert atom_behavior_gap_work_result["seed_and_matter_profile_required_count"] == 64, (
        atom_behavior_gap_work_result
    )
    radon_atom_work = get_atom_behavior_gap_work_item("Rn")
    assert radon_atom_work.work_status == "seed_and_matter_profile_required", radon_atom_work
    assert radon_atom_work.seed_mutation_allowed is False, radon_atom_work
    assert element_readiness_result["validation_status"] == (
        "element_readiness_scores_validated"
    ), element_readiness_result
    assert element_readiness_result["score_count"] == 118, element_readiness_result
    assert element_readiness_result["ready_count"] == 54, element_readiness_result
    assert element_readiness_result["blocked_by_isotope_evidence_count"] == 0, (
        element_readiness_result
    )
    assert element_readiness_result["blocked_by_seed_and_matter_count"] == 64, (
        element_readiness_result
    )
    assert element_readiness_result["high_priority_gap_count"] == 0, (
        element_readiness_result
    )
    assert element_readiness_result["seed_mutation_allowed_count"] == 0, (
        element_readiness_result
    )
    oxygen_readiness = get_element_readiness_score("O")
    technetium_readiness = get_element_readiness_score("Tc")
    radon_readiness = get_element_readiness_score("Rn")
    assert oxygen_readiness.readiness_status == "atom_behavior_ready_from_evidence", (
        oxygen_readiness
    )
    assert oxygen_readiness.constraint_tension_score == 0.0, oxygen_readiness
    assert technetium_readiness.readiness_status == (
        "atom_behavior_ready_from_evidence"
    ), technetium_readiness
    assert technetium_readiness.gap_priority_score == 0.0, technetium_readiness
    assert technetium_readiness.constraint_tension_score == 0.0, technetium_readiness
    assert radon_readiness.readiness_status == (
        "atom_behavior_blocked_by_seed_and_matter"
    ), radon_readiness
    assert radon_readiness.gap_priority_score == 0.5, radon_readiness
    assert isotope_source_policy_result["validation_status"] == (
        "isotope_source_policies_validated"
    ), isotope_source_policy_result
    assert isotope_source_policy_result["policy_count"] == 0, (
        isotope_source_policy_result
    )
    assert isotope_source_policy_result["candidate_source_count"] == 3, (
        isotope_source_policy_result
    )
    assert isotope_source_policy_result["primary_source_candidate_count"] == 2, (
        isotope_source_policy_result
    )
    assert isotope_source_policy_result["bounded_secondary_candidate_count"] == 1, (
        isotope_source_policy_result
    )
    assert isotope_source_policy_result["gap_closure_count"] == 0, (
        isotope_source_policy_result
    )
    assert isotope_source_policy_result["atom_behavior_generation_allowed_count"] == 0, (
        isotope_source_policy_result
    )
    assert isotope_source_policy_result["seed_mutation_allowed_count"] == 0, (
        isotope_source_policy_result
    )
    assert isotope_source_search_result["validation_status"] == (
        "isotope_source_search_receipts_validated"
    ), isotope_source_search_result
    assert isotope_source_search_result["search_receipt_count"] == 0, (
        isotope_source_search_result
    )
    assert isotope_source_search_result["open_search_count"] == 0, (
        isotope_source_search_result
    )
    assert isotope_source_search_result["candidate_receipt_created_count"] == 0, (
        isotope_source_search_result
    )
    assert isotope_source_search_result["candidate_source_count"] == 0, (
        isotope_source_search_result
    )
    assert isotope_source_search_result["gap_closure_count"] == 0, (
        isotope_source_search_result
    )
    assert isotope_source_search_result[
        "atom_behavior_generation_allowed_count"
    ] == 0, isotope_source_search_result
    assert isotope_source_search_result["seed_mutation_allowed_count"] == 0, (
        isotope_source_search_result
    )
    assert isotope_candidate_evidence_result["validation_status"] == (
        "isotope_candidate_evidence_receipts_validated"
    ), isotope_candidate_evidence_result
    assert isotope_candidate_evidence_result["receipt_count"] == 0, (
        isotope_candidate_evidence_result
    )
    assert isotope_candidate_evidence_result["candidate_isotope_count"] == 0, (
        isotope_candidate_evidence_result
    )
    assert isotope_candidate_evidence_result["stable_candidate_count"] == 0, (
        isotope_candidate_evidence_result
    )
    assert isotope_candidate_evidence_result["radioisotope_candidate_count"] == 0, (
        isotope_candidate_evidence_result
    )
    assert isotope_candidate_evidence_result["admitted_count"] == 0, (
        isotope_candidate_evidence_result
    )
    assert isotope_candidate_evidence_result["gap_closure_count"] == 0, (
        isotope_candidate_evidence_result
    )
    assert isotope_candidate_evidence_result[
        "atom_behavior_generation_allowed_count"
    ] == 0, isotope_candidate_evidence_result
    assert isotope_candidate_evidence_result["seed_mutation_allowed_count"] == 0, (
        isotope_candidate_evidence_result
    )
    assert isotope_candidate_admission_result["validation_status"] == (
        "isotope_candidate_admission_receipts_validated"
    ), isotope_candidate_admission_result
    assert isotope_candidate_admission_result["receipt_count"] == 2, (
        isotope_candidate_admission_result
    )
    assert isotope_candidate_admission_result["admitted_to_canonical_count"] == 2, (
        isotope_candidate_admission_result
    )
    assert isotope_candidate_admission_result["admitted_isotope_count"] == 4, (
        isotope_candidate_admission_result
    )
    assert isotope_candidate_admission_result["active_candidate_retained_count"] == 0, (
        isotope_candidate_admission_result
    )
    assert isotope_candidate_admission_result["seed_mutation_allowed_count"] == 0, (
        isotope_candidate_admission_result
    )
    oxygen_candidate_admission = get_isotope_candidate_admission_receipt("O")
    technetium_candidate_admission = get_isotope_candidate_admission_receipt("Tc")
    assert oxygen_candidate_admission.admitted_mass_numbers == (16, 17, 18), (
        oxygen_candidate_admission
    )
    assert oxygen_candidate_admission.active_candidate_receipt_retained is False, (
        oxygen_candidate_admission
    )
    assert technetium_candidate_admission.admitted_mass_numbers == (99,), (
        technetium_candidate_admission
    )
    assert technetium_candidate_admission.active_candidate_receipt_retained is False, (
        technetium_candidate_admission
    )
    assert cs_rn_promotion_result.validation_status == (
        "cs_rn_promotion_readiness_profiles_validated"
    ), cs_rn_promotion_result
    assert cs_rn_promotion_result.profile_count == 32, cs_rn_promotion_result
    assert cs_rn_promotion_result.atomic_number_span == (55, 86), cs_rn_promotion_result
    assert cs_rn_promotion_result.blocked_count == 1, cs_rn_promotion_result
    assert cs_rn_promotion_result.ready_count == 31, cs_rn_promotion_result
    assert cs_rn_promotion_result.physical_property_evidence_count == 31, (
        cs_rn_promotion_result
    )
    assert cs_rn_promotion_result.unresolved_physical_property_evidence_count == 1, (
        cs_rn_promotion_result
    )
    assert cs_rn_promotion_result.f_block_profile_count == 15, cs_rn_promotion_result
    assert configuration_evidence_result["validation_status"] == (
        "configuration_evidence_records_validated"
    ), configuration_evidence_result
    assert configuration_evidence_result["record_count"] == 32, configuration_evidence_result
    assert configuration_evidence_result["exception_count"] == 2, configuration_evidence_result
    assert configuration_evidence_result["special_first_cation_literature_count"] == 8, (
        configuration_evidence_result
    )
    assert frontier_valence_result["validation_status"] == (
        "frontier_valence_signature_records_validated"
    ), frontier_valence_result
    assert frontier_valence_result["record_count"] == 32, frontier_valence_result
    assert frontier_valence_result["s_block_count"] == 2, frontier_valence_result
    assert frontier_valence_result["lanthanide_count"] == 15, frontier_valence_result
    assert frontier_valence_result["transition_count"] == 9, frontier_valence_result
    assert frontier_valence_result["p_block_count"] == 6, frontier_valence_result
    assert oxidation_state_evidence_result["validation_status"] == (
        "oxidation_state_evidence_records_validated"
    ), oxidation_state_evidence_result
    assert oxidation_state_evidence_result["record_count"] == 32, oxidation_state_evidence_result
    assert oxidation_state_evidence_result["variable_oxidation_state_count"] == 15, (
        oxidation_state_evidence_result
    )
    assert oxidation_state_evidence_result["negative_oxidation_state_count"] == 1, (
        oxidation_state_evidence_result
    )
    assert oxidation_state_evidence_result["zero_oxidation_state_count"] == 1, (
        oxidation_state_evidence_result
    )
    assert behavior_tag_result["validation_status"] == (
        "behavior_tag_overlay_records_validated"
    ), behavior_tag_result
    assert behavior_tag_result["record_count"] == 32, behavior_tag_result
    assert behavior_tag_result["variable_oxidation_tag_count"] == 15, behavior_tag_result
    assert behavior_tag_result["coordination_relevance_count"] == 9, behavior_tag_result
    assert behavior_tag_result["f_orbital_relevance_count"] == 15, behavior_tag_result
    assert behavior_tag_result["low_reactivity_baseline_count"] == 1, behavior_tag_result
    assert relation_overlay_result["validation_status"] == (
        "relation_overlay_records_validated"
    ), relation_overlay_result
    assert relation_overlay_result["record_count"] == 32, relation_overlay_result
    assert relation_overlay_result["edge_count"] > 0, relation_overlay_result
    assert relation_overlay_result["edge_counts_by_type"]["same_period"] == 32 * 31, (
        relation_overlay_result
    )
    assert promotion_decision_result["validation_status"] == (
        "promotion_decision_receipts_validated"
    ), promotion_decision_result
    assert promotion_decision_result["receipt_count"] == 32, promotion_decision_result
    assert promotion_decision_result["ready_pending_approval_count"] == 31, (
        promotion_decision_result
    )
    assert promotion_decision_result["blocked_unresolved_physical_property_count"] == 1, (
        promotion_decision_result
    )
    assert promotion_decision_result["approved_for_seed_count"] == 0, (
        promotion_decision_result
    )
    assert promotion_batch_policy_result["validation_status"] == (
        "promotion_batch_policy_receipt_validated"
    ), promotion_batch_policy_result
    assert promotion_batch_policy_result["policy_decision"] == "hold_full_cs_rn_span", (
        promotion_batch_policy_result
    )
    assert promotion_batch_policy_result["ready_count"] == 31, promotion_batch_policy_result
    assert promotion_batch_policy_result["blocked_count"] == 1, promotion_batch_policy_result
    assert promotion_batch_policy_result["seed_mutation_allowed"] is False, (
        promotion_batch_policy_result
    )
    Draft202012Validator.check_schema(element_schema)
    Draft202012Validator.check_schema(snapshot_schema)
    element_schema_validator.validate(json.loads(json.dumps(get_seed_element("Zn").to_dict())))
    oxygen = get_seed_element("O")
    calcium = get_seed_element("Ca")
    chromium = get_seed_element("Cr")
    copper = get_seed_element("Cu")
    zinc = get_seed_element("Zn")
    gallium = get_seed_element("Ga")
    krypton = get_seed_element("Kr")
    sodium_ion = build_ion_instance("Na", charge=1)
    chloride_ion = build_ion_instance("Cl", charge=-1)
    carbon_14 = build_isotope_instance("C", mass_number=14)
    oganesson_294 = build_isotope_instance("Og", mass_number=294)
    assert oxygen.state.data_level == 2, oxygen.state
    assert oxygen.state.oxidation_states == (-2,), oxygen.state
    assert oxygen.state.electronegativity_value == 3.44, oxygen.state
    assert "pubchem_periodic_table_properties" in oxygen.source_keys(), oxygen.source_keys()
    assert calcium.state.oxidation_states == (2,), calcium.state
    assert chromium.state.configuration_audit.is_exception is True, chromium.state
    assert chromium.state.configuration_audit.simple_aufbau_candidate == "[Ar] 3d^4 4s^2"
    assert chromium.state.frontier_signature.d_shell_stability == "half_filled_d_shell"
    assert copper.state.configuration_audit.is_exception is True, copper.state
    assert copper.state.configuration_audit.simple_aufbau_candidate == "[Ar] 3d^9 4s^2"
    assert copper.state.frontier_signature.d_shell_stability == "filled_d_shell"
    assert zinc.state.oxidation_states == (2,), zinc.state
    assert zinc.state.electronegativity_value == 1.65, zinc.state
    assert zinc.state.first_ionization_energy_ev == 9.394, zinc.state
    assert zinc.state.first_ionization_energy_source_key == "pubchem_periodic_table_properties"
    assert zinc.state.bond_tendency_tags == ("metallic_bonding", "coordination_complex")
    assert zinc.state.bond_tendency_source_key == "pubchem_periodic_table_properties"
    assert gallium.state.frontier_signature.d_shell == "3d^10", gallium.state
    assert gallium.state.frontier_signature.valence_model == "period_4_p_block_d_core"
    assert krypton.state.oxidation_states == (0,), krypton.state
    assert krypton.state.electronegativity_value == 3.00, krypton.state
    assert krypton.state.first_ionization_energy_ev == 14.000, krypton.state
    assert krypton.state.bond_tendency_tags == ("noble_gas_low_reactivity",)
    assert sodium_ion.instance_id == "MSPEE-Z011-Na-ion-plus-1", sodium_ion
    assert sodium_ion.electron_count == 10, sodium_ion
    assert sodium_ion.validate() == [], sodium_ion
    assert chloride_ion.instance_id == "MSPEE-Z017-Cl-ion-minus-1", chloride_ion
    assert chloride_ion.electron_count == 18, chloride_ion
    assert chloride_ion.validate() == [], chloride_ion
    assert carbon_14.instance_id == "MSPEE-Z006-C-isotope-14", carbon_14
    assert carbon_14.neutron_count == 8, carbon_14
    assert carbon_14.validate() == [], carbon_14
    assert oganesson_294.instance_id == "MSPEE-Z118-Og-isotope-294", oganesson_294
    assert oganesson_294.neutron_count == 176, oganesson_294
    carbon_14_evidence = find_isotope_evidence_records("C", mass_number=14)[0]
    iron_ion_evidence = find_common_ion_evidence_records("Fe")
    radon_unresolved_isotope = find_unresolved_isotope_evidence_record("Rn")
    oxygen_unresolved_common_ion = find_unresolved_common_ion_evidence_record("O")
    bromine_properties = find_physical_property_evidence_record("Br")
    radon_properties = find_physical_property_evidence_record("Rn")
    astatine_unresolved_properties = find_unresolved_physical_property_evidence_record("At")
    astatine_property_gap = get_physical_property_gap_audit_receipt("At")
    astatine_gap_work_item = get_physical_property_gap_work_item("At")
    protactinium_source_search = get_physical_property_source_search_receipt("Pa")
    berkelium_source_search = get_physical_property_source_search_receipt("Bk")
    francium_partial_source_search = get_partial_physical_property_source_search_receipt("Fr")
    astatine_secondary_source_policy = get_physical_property_secondary_source_policy("At")
    astatine_secondary_evidence_template = build_physical_property_secondary_evidence_template(
        "At"
    )
    bromine_matter_profile = build_matter_behavior_profile("Br")
    astatine_promotion_profile = get_cs_rn_promotion_readiness_profile("At")
    astatine_configuration_evidence = find_configuration_evidence_record("At")
    gold_configuration_evidence = find_configuration_evidence_record("Au")
    astatine_frontier = find_frontier_valence_signature_record("At")
    gold_frontier = find_frontier_valence_signature_record("Au")
    astatine_oxidation = find_oxidation_state_evidence_record("At")
    gold_oxidation = find_oxidation_state_evidence_record("Au")
    radon_oxidation = find_oxidation_state_evidence_record("Rn")
    astatine_behavior = find_behavior_tag_overlay_record("At")
    gold_behavior = find_behavior_tag_overlay_record("Au")
    radon_behavior = find_behavior_tag_overlay_record("Rn")
    astatine_relation = find_relation_overlay_record("At")
    gold_relation = find_relation_overlay_record("Au")
    gold_promotion_profile = get_cs_rn_promotion_readiness_profile("Au")
    astatine_decision = get_promotion_decision_receipt("At")
    gold_decision = get_promotion_decision_receipt("Au")
    assert carbon_14_evidence.isotope_id == "MSPEE-Z006-C-isotope-14", carbon_14_evidence
    assert carbon_14_evidence.half_life_value == 5730.0, carbon_14_evidence
    assert carbon_14_evidence.decay_mode == "beta_minus", carbon_14_evidence
    assert {record.charge for record in iron_ion_evidence} == {2, 3}, iron_ion_evidence
    assert radon_unresolved_isotope.evidence_domain == "isotope_evidence", (
        radon_unresolved_isotope
    )
    assert oxygen_unresolved_common_ion.evidence_domain == "common_ion_evidence", (
        oxygen_unresolved_common_ion
    )
    assert bromine_properties.standard_state == "Liquid", bromine_properties
    assert bromine_properties.melting_point_k == 265.95, bromine_properties
    assert bromine_properties.boiling_point_k == 331.95, bromine_properties
    assert astatine_unresolved_properties.missing_fields == ("boiling_point_k",), (
        astatine_unresolved_properties
    )
    assert astatine_property_gap.blocks_promotion_spans == ("Cs-Rn",), (
        astatine_property_gap
    )
    assert astatine_property_gap.no_guess_policy is True, astatine_property_gap
    assert astatine_gap_work_item.work_status == "conflict_blocked_promotion", (
        astatine_gap_work_item
    )
    assert astatine_gap_work_item.closes_gap is False, astatine_gap_work_item
    assert protactinium_source_search.search_status == (
        "source_search_complete_candidate_receipt_created"
    ), (
        protactinium_source_search
    )
    assert berkelium_source_search.search_status == (
        "source_search_complete_candidate_receipt_created"
    ), (
        berkelium_source_search
    )
    assert protactinium_source_search.closes_gap is False, protactinium_source_search
    assert berkelium_source_search.seed_mutation_allowed is False, berkelium_source_search
    assert francium_partial_source_search.search_status == "partial_source_search_open", (
        francium_partial_source_search
    )
    assert len(francium_partial_source_search.field_searches) == 2, (
        francium_partial_source_search
    )
    assert francium_partial_source_search.closes_gap is False, francium_partial_source_search
    assert astatine_secondary_source_policy.gap_closure_status == (
        "gap_not_closed_by_policy"
    ), astatine_secondary_source_policy
    assert astatine_secondary_source_policy.seed_mutation_allowed is False, (
        astatine_secondary_source_policy
    )
    assert astatine_secondary_evidence_template["field_name"] == "boiling_point_k", (
        astatine_secondary_evidence_template
    )
    astatine_secondary_evidence_candidate = get_physical_property_secondary_evidence_receipt("At")
    astatine_secondary_evidence_admission = (
        get_physical_property_secondary_evidence_admission_decision("At")
    )
    francium_secondary_evidence_admission = (
        get_physical_property_secondary_evidence_admission_decision("Fr")
    )
    francium_density_secondary_evidence_admission = (
        get_physical_property_secondary_evidence_admission_decision(
            "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z087-Fr-density_value-WebElements"
        )
    )
    protactinium_secondary_evidence_admission = (
        get_physical_property_secondary_evidence_admission_decision("Pa")
    )
    berkelium_secondary_evidence_admission = (
        get_physical_property_secondary_evidence_admission_decision("Bk")
    )
    californium_boiling_secondary_evidence_admission = (
        get_physical_property_secondary_evidence_admission_decision(
            "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z098-Cf-boiling_point_k-LANL"
        )
    )
    californium_density_secondary_evidence_admission = (
        get_physical_property_secondary_evidence_admission_decision(
            "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z098-Cf-density_value-RSC"
        )
    )
    einsteinium_secondary_evidence_admission = (
        get_physical_property_secondary_evidence_admission_decision(
            "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-ADMISSION-Z099-Es-boiling_point_k-LANL"
        )
    )
    astatine_property_conflict = get_physical_property_conflict_resolution_receipt("At")
    francium_property_conflict = get_physical_property_conflict_resolution_receipt("Fr")
    protactinium_property_conflict = get_physical_property_conflict_resolution_receipt("Pa")
    francium_density_corroboration_review = get_physical_property_corroboration_review_receipt(
        "MSPEE-PHYSICAL-PROPERTY-CORROBORATION-REVIEW-Z087-Fr-density_value"
    )
    berkelium_corroboration_review = get_physical_property_corroboration_review_receipt("Bk")
    californium_corroboration_review = get_physical_property_corroboration_review_receipt("Cf")
    einsteinium_corroboration_review = get_physical_property_corroboration_review_receipt("Es")
    californium_density_review = get_physical_property_review_receipt("Cf")
    californium_density_gap_closure = get_physical_property_gap_closure_decision("Cf")
    californium_density_closure_approval = get_physical_property_closure_approval_receipt("Cf")
    californium_density_seed_update = get_physical_property_seed_update_receipt("Cf")
    astatine_escalation = get_physical_property_escalation_receipt("At")
    berkelium_escalation = get_physical_property_escalation_receipt("Bk")
    californium_seed_update_escalation = get_physical_property_escalation_receipt(
        "MSPEE-PHYSICAL-PROPERTY-SEED-UPDATE-Z098-Cf-density_value"
    )
    astatine_escalation_search = get_physical_property_escalation_search_receipt("At")
    francium_escalation_search = get_physical_property_escalation_search_receipt("Fr")
    francium_density_escalation_search = get_physical_property_escalation_search_receipt(
        "MSPEE-PHYSICAL-PROPERTY-ESCALATION-SEARCH-Z087-Fr-density_value"
    )
    berkelium_escalation_search = get_physical_property_escalation_search_receipt("Bk")
    californium_escalation_search = get_physical_property_escalation_search_receipt("Cf")
    einsteinium_escalation_search = get_physical_property_escalation_search_receipt("Es")
    protactinium_escalation_search = get_physical_property_escalation_search_receipt("Pa")
    astatine_escalation_resolution = get_physical_property_escalation_resolution_receipt("At")
    californium_escalation_resolution = (
        get_physical_property_escalation_resolution_receipt("Cf")
    )
    astatine_operator_decision = get_physical_property_operator_decision_receipt("At")
    californium_operator_decision = get_physical_property_operator_decision_receipt("Cf")
    astatine_continued_evidence = get_physical_property_continued_evidence_plan("At")
    californium_continued_evidence = get_physical_property_continued_evidence_plan("Cf")
    fermium_no_candidate_review = get_physical_property_no_candidate_review_receipt("Fm")
    mendelevium_no_candidate_review = get_physical_property_no_candidate_review_receipt("Md")
    nobelium_no_candidate_review = get_physical_property_no_candidate_review_receipt("No")
    lawrencium_no_candidate_review = get_physical_property_no_candidate_review_receipt("Lr")
    assert astatine_secondary_evidence_candidate.normalized_value == 610.15, (
        astatine_secondary_evidence_candidate
    )
    assert astatine_secondary_evidence_candidate.source_key == (
        "lanl_periodic_table_candidate"
    ), astatine_secondary_evidence_candidate
    assert astatine_secondary_evidence_candidate.admission_status == (
        "secondary_evidence_candidate"
    ), astatine_secondary_evidence_candidate
    assert astatine_secondary_evidence_admission.decision_status == (
        "secondary_evidence_not_admitted_conflict"
    ), astatine_secondary_evidence_admission
    assert astatine_secondary_evidence_admission.closes_gap is False, (
        astatine_secondary_evidence_admission
    )
    assert francium_secondary_evidence_admission.decision_status == (
        "secondary_evidence_not_admitted_conflict"
    ), francium_secondary_evidence_admission
    assert francium_density_secondary_evidence_admission.decision_status == (
        "secondary_evidence_not_admitted_needs_corroboration"
    ), francium_density_secondary_evidence_admission
    assert francium_secondary_evidence_admission.closes_gap is False, (
        francium_secondary_evidence_admission
    )
    assert francium_density_secondary_evidence_admission.seed_mutation_allowed is False, (
        francium_density_secondary_evidence_admission
    )
    assert protactinium_secondary_evidence_admission.decision_status == (
        "secondary_evidence_not_admitted_conflict"
    ), protactinium_secondary_evidence_admission
    assert berkelium_secondary_evidence_admission.decision_status == (
        "secondary_evidence_not_admitted_needs_corroboration"
    ), berkelium_secondary_evidence_admission
    assert californium_boiling_secondary_evidence_admission.decision_status == (
        "secondary_evidence_not_admitted_needs_corroboration"
    ), californium_boiling_secondary_evidence_admission
    assert californium_density_secondary_evidence_admission.decision_status == (
        "secondary_evidence_not_admitted_pending_review"
    ), californium_density_secondary_evidence_admission
    assert einsteinium_secondary_evidence_admission.decision_status == (
        "secondary_evidence_not_admitted_needs_corroboration"
    ), einsteinium_secondary_evidence_admission
    assert protactinium_secondary_evidence_admission.closes_gap is False, (
        protactinium_secondary_evidence_admission
    )
    assert berkelium_secondary_evidence_admission.seed_mutation_allowed is False, (
        berkelium_secondary_evidence_admission
    )
    assert californium_boiling_secondary_evidence_admission.closes_gap is False, (
        californium_boiling_secondary_evidence_admission
    )
    assert californium_density_secondary_evidence_admission.seed_mutation_allowed is False, (
        californium_density_secondary_evidence_admission
    )
    assert einsteinium_secondary_evidence_admission.closes_gap is False, (
        einsteinium_secondary_evidence_admission
    )
    assert astatine_property_conflict.resolution_decision == (
        "blocked_pending_higher_precedence_source"
    ), astatine_property_conflict
    assert astatine_property_conflict.closes_gap is False, astatine_property_conflict
    assert astatine_property_conflict.seed_mutation_allowed is False, (
        astatine_property_conflict
    )
    assert francium_property_conflict.resolution_decision == (
        "blocked_pending_higher_precedence_source"
    ), francium_property_conflict
    assert francium_property_conflict.closes_gap is False, francium_property_conflict
    assert protactinium_property_conflict.resolution_decision == (
        "blocked_pending_higher_precedence_source"
    ), protactinium_property_conflict
    assert protactinium_property_conflict.closes_gap is False, protactinium_property_conflict
    assert francium_density_corroboration_review.review_decision == (
        "blocked_pending_corroborating_source"
    ), francium_density_corroboration_review
    assert francium_density_corroboration_review.closes_gap is False, (
        francium_density_corroboration_review
    )
    assert berkelium_corroboration_review.review_decision == (
        "blocked_pending_corroborating_source"
    ), berkelium_corroboration_review
    assert berkelium_corroboration_review.seed_mutation_allowed is False, (
        berkelium_corroboration_review
    )
    assert californium_corroboration_review.review_decision == (
        "blocked_pending_corroborating_source"
    ), californium_corroboration_review
    assert californium_corroboration_review.closes_gap is False, (
        californium_corroboration_review
    )
    assert einsteinium_corroboration_review.review_decision == (
        "blocked_pending_corroborating_source"
    ), einsteinium_corroboration_review
    assert einsteinium_corroboration_review.seed_mutation_allowed is False, (
        einsteinium_corroboration_review
    )
    assert californium_density_review.review_decision == (
        "resolved_admit_candidate"
    ), californium_density_review
    assert californium_density_review.closes_gap is False, californium_density_review
    assert californium_density_review.seed_mutation_allowed is False, (
        californium_density_review
    )
    assert californium_density_gap_closure.closure_status == (
        "gap_closure_ready_pending_operator_approval"
    ), californium_density_gap_closure
    assert californium_density_gap_closure.closes_gap is False, (
        californium_density_gap_closure
    )
    assert californium_density_closure_approval.approval_status == (
        "closure_approval_deferred"
    ), californium_density_closure_approval
    assert californium_density_closure_approval.seed_mutation_allowed is False, (
        californium_density_closure_approval
    )
    assert californium_density_seed_update.update_status == (
        "seed_update_blocked_by_deferred_approval"
    ), californium_density_seed_update
    assert californium_density_seed_update.seed_update_applied is False, (
        californium_density_seed_update
    )
    assert astatine_escalation.escalation_class == "higher_precedence_source_required", (
        astatine_escalation
    )
    assert berkelium_escalation.escalation_class == "corroborating_source_required", (
        berkelium_escalation
    )
    assert californium_seed_update_escalation.escalation_class == (
        "operator_approval_required"
    ), californium_seed_update_escalation
    assert californium_seed_update_escalation.closes_gap is False, (
        californium_seed_update_escalation
    )
    assert astatine_escalation_search.search_status == (
        "higher_precedence_source_not_found"
    ), astatine_escalation_search
    assert astatine_escalation_search.closes_gap is False, astatine_escalation_search
    assert francium_escalation_search.search_status == (
        "higher_precedence_source_not_found"
    ), francium_escalation_search
    assert francium_escalation_search.closes_gap is False, francium_escalation_search
    assert francium_density_escalation_search.search_status == (
        "corroborating_source_not_found"
    ), francium_density_escalation_search
    assert francium_density_escalation_search.closes_gap is False, (
        francium_density_escalation_search
    )
    assert berkelium_escalation_search.search_status == (
        "corroborating_source_not_found"
    ), berkelium_escalation_search
    assert berkelium_escalation_search.closes_gap is False, berkelium_escalation_search
    assert californium_escalation_search.search_status == (
        "corroborating_source_not_found"
    ), californium_escalation_search
    assert californium_escalation_search.closes_gap is False, (
        californium_escalation_search
    )
    assert einsteinium_escalation_search.search_status == (
        "corroborating_source_not_found"
    ), einsteinium_escalation_search
    assert einsteinium_escalation_search.closes_gap is False, einsteinium_escalation_search
    assert protactinium_escalation_search.search_status == (
        "higher_precedence_source_not_found"
    ), protactinium_escalation_search
    assert protactinium_escalation_search.closes_gap is False, (
        protactinium_escalation_search
    )
    assert astatine_escalation_resolution.resolution_status == (
        "conflict_resolution_blocked_pending_operator_decision"
    ), astatine_escalation_resolution
    assert astatine_escalation_resolution.final_resolution_applied is False, (
        astatine_escalation_resolution
    )
    assert californium_escalation_resolution.resolution_status == (
        "candidate_rejection_recommended_pending_operator_decision"
    ), californium_escalation_resolution
    assert californium_escalation_resolution.closes_gap is False, (
        californium_escalation_resolution
    )
    assert astatine_operator_decision.operator_decision_status == (
        "operator_decision_deferred"
    ), astatine_operator_decision
    assert astatine_operator_decision.final_resolution_applied is False, (
        astatine_operator_decision
    )
    assert californium_operator_decision.operator_decision_status == (
        "operator_decision_deferred"
    ), californium_operator_decision
    assert californium_operator_decision.closes_gap is False, californium_operator_decision
    assert astatine_continued_evidence.plan_class == (
        "higher_precedence_source_discovery"
    ), astatine_continued_evidence
    assert astatine_continued_evidence.closes_gap is False, astatine_continued_evidence
    assert californium_continued_evidence.plan_class == (
        "independent_corroboration_discovery"
    ), californium_continued_evidence
    assert californium_continued_evidence.seed_mutation_allowed is False, (
        californium_continued_evidence
    )
    assert fermium_no_candidate_review.review_decision == (
        "blocked_no_admissible_candidate_found"
    ), fermium_no_candidate_review
    assert fermium_no_candidate_review.closes_gap is False, fermium_no_candidate_review
    assert mendelevium_no_candidate_review.review_decision == (
        "blocked_no_admissible_candidate_found"
    ), mendelevium_no_candidate_review
    assert mendelevium_no_candidate_review.seed_mutation_allowed is False, (
        mendelevium_no_candidate_review
    )
    assert nobelium_no_candidate_review.review_decision == (
        "blocked_no_admissible_candidate_found"
    ), nobelium_no_candidate_review
    assert nobelium_no_candidate_review.closes_gap is False, nobelium_no_candidate_review
    assert lawrencium_no_candidate_review.review_decision == (
        "blocked_no_admissible_candidate_found"
    ), lawrencium_no_candidate_review
    assert lawrencium_no_candidate_review.seed_mutation_allowed is False, (
        lawrencium_no_candidate_review
    )
    assert bromine_matter_profile.standard_state == "Liquid", bromine_matter_profile
    assert "low_boiling_boundary" in bromine_matter_profile.inferred_behavior_tags, (
        bromine_matter_profile
    )
    assert astatine_promotion_profile.readiness_status == (
        "promotion_blocked_missing_source_evidence"
    ), astatine_promotion_profile
    assert astatine_promotion_profile.unresolved_physical_property_evidence_available is True, (
        astatine_promotion_profile
    )
    assert "complete_physical_property_evidence" in (
        astatine_promotion_profile.required_missing_evidence
    ), astatine_promotion_profile
    assert "nist_neutral_electron_configuration" not in (
        astatine_promotion_profile.required_missing_evidence
    ), astatine_promotion_profile
    assert "frontier_signature" not in (
        astatine_promotion_profile.required_missing_evidence
    ), astatine_promotion_profile
    assert "valence_shell_signature" not in (
        astatine_promotion_profile.required_missing_evidence
    ), astatine_promotion_profile
    assert "oxidation_state_evidence" not in (
        astatine_promotion_profile.required_missing_evidence
    ), astatine_promotion_profile
    assert "level_1_behavior_tags" not in (
        astatine_promotion_profile.required_missing_evidence
    ), astatine_promotion_profile
    assert "relation_edges" not in (
        astatine_promotion_profile.required_missing_evidence
    ), astatine_promotion_profile
    assert astatine_promotion_profile.readiness_status == (
        "promotion_blocked_missing_source_evidence"
    ), astatine_promotion_profile
    assert gold_promotion_profile.readiness_status == "promotion_ready", gold_promotion_profile
    assert gold_promotion_profile.required_missing_evidence == (), gold_promotion_profile
    assert gold_decision.decision_status == "promotion_ready_pending_approval", gold_decision
    assert astatine_decision.decision_status == (
        "promotion_blocked_unresolved_physical_property"
    ), astatine_decision
    assert promotion_batch_policy.blocked_symbols == ("At",), promotion_batch_policy
    assert promotion_batch_policy.seed_mutation_allowed is False, promotion_batch_policy
    assert astatine_configuration_evidence.neutral_configuration == (
        "[Xe] 4f^14 5d^10 6s^2 6p^5"
    ), astatine_configuration_evidence
    assert astatine_configuration_evidence.first_cation_source_note is not None, (
        astatine_configuration_evidence
    )
    assert gold_configuration_evidence.configuration_audit.is_exception is True, (
        gold_configuration_evidence
    )
    assert gold_configuration_evidence.configuration_audit.simple_aufbau_candidate == (
        "[Xe] 4f^14 5d^9 6s^2"
    )
    assert astatine_frontier.frontier_model == "period_6_p_block_f_d_core", astatine_frontier
    assert astatine_frontier.p_shell == "6p^5", astatine_frontier
    assert gold_frontier.d_shell == "5d^10", gold_frontier
    assert gold_frontier.d_shell_stability == "filled_shell", gold_frontier
    assert astatine_oxidation.oxidation_states == (7, 5, 3, 1, -1), astatine_oxidation
    assert gold_oxidation.oxidation_states == (3, 1), gold_oxidation
    assert radon_oxidation.oxidation_states == (0,), radon_oxidation
    assert "negative_oxidation_pathway" in astatine_behavior.inferred_behavior_tags, (
        astatine_behavior
    )
    assert "filled_d_shell_context" in gold_behavior.inferred_behavior_tags, gold_behavior
    assert "low_reactivity_baseline" in radon_behavior.inferred_behavior_tags, radon_behavior
    assert astatine_relation.relation_edges, astatine_relation
    assert any(edge.target_symbol == "Pt" for edge in gold_relation.relation_edges), (
        gold_relation
    )
    physical_property_drift_report = build_physical_property_drift_report(
        (
            SourcePhysicalPropertyRow(
                atomic_number=bromine_properties.atomic_number,
                symbol=bromine_properties.symbol,
                standard_state=bromine_properties.standard_state,
                melting_point_k=bromine_properties.melting_point_k,
                boiling_point_k=bromine_properties.boiling_point_k,
                density_value=bromine_properties.density_value,
            ),
            SourcePhysicalPropertyRow(
                atomic_number=radon_properties.atomic_number,
                symbol=radon_properties.symbol,
                standard_state=radon_properties.standard_state,
                melting_point_k=radon_properties.melting_point_k,
                boiling_point_k=radon_properties.boiling_point_k,
                density_value=radon_properties.density_value,
            ),
        ),
        source_url="fixture://pubchem-physical",
        require_complete_source=False,
    )
    assert (
        physical_property_drift_report["drift_status"]
        == "physical_property_evidence_no_drift"
    ), physical_property_drift_report
    assert physical_property_drift_report["local_count"] == 93, physical_property_drift_report
    level_2_zinc_payload = json.loads(json.dumps(get_seed_element("Zn").to_dict()))
    level_2_zinc_payload["state"]["oxidation_states"] = [-2, 0, 2]
    level_2_zinc_payload["state"]["electronegativity_scale"] = "pauling"
    level_2_zinc_payload["state"]["electronegativity_value"] = 1.65
    level_2_zinc_payload["state"]["electronegativity_source_key"] = "level_2_reference_seed"
    level_2_zinc_payload["state"]["data_level"] = 2
    element_schema_validator.validate(level_2_zinc_payload)
    snapshot_schema_validator.validate(json.loads(json.dumps(get_snapshot_record("La").to_dict())))
    promethium_profile = get_f_block_expansion_profile("Pm")
    uranium_profile = get_f_block_expansion_profile("U")
    assert promethium_profile.series == "lanthanide", promethium_profile
    assert promethium_profile.f_shell_family == "4f", promethium_profile
    assert promethium_profile.radioactive_decay_relevance is True, promethium_profile
    assert promethium_profile.nuclear_state_extension_required is True, promethium_profile
    assert uranium_profile.series == "actinide", uranium_profile
    assert uranium_profile.f_shell_family == "5f", uranium_profile
    assert uranium_profile.actinide_instability_relevance is True, uranium_profile
    assert uranium_profile.heavy_element_uncertainty is True, uranium_profile
    rubidium_level_2_profile = get_period_5_level_2_profile("Rb")
    xenon_level_2_profile = get_period_5_level_2_profile("Xe")
    assert rubidium_level_2_profile.atomic_number == 37, rubidium_level_2_profile
    assert rubidium_level_2_profile.oxidation_states == (1,), rubidium_level_2_profile
    assert rubidium_level_2_profile.electronegativity_value == 0.82, rubidium_level_2_profile
    assert rubidium_level_2_profile.bond_tendency_tags == (
        "metallic_bonding",
        "ionic_bonding",
    ), rubidium_level_2_profile
    assert xenon_level_2_profile.atomic_number == 54, xenon_level_2_profile
    assert xenon_level_2_profile.oxidation_states == (0,), xenon_level_2_profile
    assert xenon_level_2_profile.first_ionization_energy_ev == 12.13, xenon_level_2_profile
    assert xenon_level_2_profile.bond_tendency_tags == (
        "noble_gas_low_reactivity",
    ), xenon_level_2_profile
    period_5_drift_report = build_period_5_level_2_drift_report(
        (
            SourceLevel2ChemistryRow(
                atomic_number=rubidium_level_2_profile.atomic_number,
                symbol=rubidium_level_2_profile.symbol,
                oxidation_states=rubidium_level_2_profile.oxidation_states,
                electronegativity_value=rubidium_level_2_profile.electronegativity_value,
                first_ionization_energy_ev=rubidium_level_2_profile.first_ionization_energy_ev,
                group_block=rubidium_level_2_profile.pubchem_group_block,
                bond_tendency_tags=rubidium_level_2_profile.bond_tendency_tags,
            ),
            SourceLevel2ChemistryRow(
                atomic_number=xenon_level_2_profile.atomic_number,
                symbol=xenon_level_2_profile.symbol,
                oxidation_states=xenon_level_2_profile.oxidation_states,
                electronegativity_value=xenon_level_2_profile.electronegativity_value,
                first_ionization_energy_ev=xenon_level_2_profile.first_ionization_energy_ev,
                group_block=xenon_level_2_profile.pubchem_group_block,
                bond_tendency_tags=xenon_level_2_profile.bond_tendency_tags,
            ),
        ),
        source_url="fixture://pubchem-period-5",
        require_complete_source=False,
    )
    assert period_5_drift_report["drift_status"] == "period_5_level_2_snapshot_no_drift", (
        period_5_drift_report
    )
    assert period_5_drift_report["local_count"] == 18, period_5_drift_report
    zinc_block_graph = build_element_relation_graph("Zn", relation_type="same_block")
    assert zinc_block_graph.graph_status == "element_relation_graph_exported", zinc_block_graph
    assert zinc_block_graph.query["node_count"] == 20, zinc_block_graph.query
    assert zinc_block_graph.query["edge_count"] == 19, zinc_block_graph.query
    api_health = handle_api_request("GET", "/health")
    api_graph = handle_api_request("GET", "/graph?symbol=Zn&relation=same_block")
    api_dashboard = handle_api_request("GET", "/dashboard/Zn?relation=same_block")
    api_chromium_reasoning = handle_api_request("GET", "/reasoning/configuration/Cr")
    api_copper_potassium_reasoning = handle_api_request(
        "GET",
        "/reasoning/similarity?left=Cu&right=K",
    )
    api_sodium_ion = handle_api_request("GET", "/instances/ion/Na?charge=1")
    api_carbon_14 = handle_api_request("GET", "/instances/isotope/C?mass_number=14")
    api_carbon_14_evidence = handle_api_request("GET", "/evidence/isotopes/C?mass_number=14")
    api_radon_unresolved_isotope = handle_api_request(
        "GET",
        "/evidence/isotopes/unresolved/Rn",
    )
    api_iron_ion_evidence = handle_api_request("GET", "/evidence/common-ions/Fe")
    api_oxygen_unresolved_common_ion = handle_api_request(
        "GET",
        "/evidence/common-ions/unresolved/O",
    )
    api_astatine_configuration_evidence = handle_api_request(
        "GET",
        "/evidence/configurations/At",
    )
    api_gold_frontier = handle_api_request("GET", "/frontier/cs-rn/Au")
    api_gold_oxidation = handle_api_request("GET", "/evidence/oxidation-states/Au")
    api_gold_behavior = handle_api_request("GET", "/behavior/cs-rn/Au")
    api_gold_relation = handle_api_request("GET", "/relations/cs-rn/Au")
    api_promotion_batch_policy = handle_api_request("GET", "/promotion/batch-policy")
    api_astatine_decision = handle_api_request("GET", "/promotion/decisions/At")
    api_bromine_properties = handle_api_request("GET", "/evidence/physical-properties/Br")
    api_astatine_unresolved_properties = handle_api_request(
        "GET",
        "/evidence/physical-properties/unresolved/At",
    )
    api_astatine_property_gap = handle_api_request(
        "GET",
        "/evidence/physical-properties/gaps/At",
    )
    api_astatine_gap_workplan = handle_api_request(
        "GET",
        "/evidence/physical-properties/workplan/At",
    )
    api_protactinium_source_search = handle_api_request(
        "GET",
        "/evidence/physical-properties/source-search/Pa",
    )
    api_francium_partial_source_search = handle_api_request(
        "GET",
        "/evidence/physical-properties/partial-source-search/Fr",
    )
    api_astatine_secondary_source_policy = handle_api_request(
        "GET",
        "/evidence/physical-properties/secondary-source-policy/At",
    )
    api_secondary_evidence = handle_api_request(
        "GET",
        "/evidence/physical-properties/secondary-evidence",
    )
    api_astatine_secondary_evidence_admission = handle_api_request(
        "GET",
        "/evidence/physical-properties/secondary-evidence/admission/At",
    )
    api_protactinium_secondary_evidence_admission = handle_api_request(
        "GET",
        "/evidence/physical-properties/secondary-evidence/admission/Pa",
    )
    api_astatine_property_conflict = handle_api_request(
        "GET",
        "/evidence/physical-properties/conflicts/At",
    )
    api_francium_property_conflict = handle_api_request(
        "GET",
        "/evidence/physical-properties/conflicts/Fr",
    )
    api_francium_density_corroboration_review = handle_api_request(
        "GET",
        "/evidence/physical-properties/corroboration/"
        "MSPEE-PHYSICAL-PROPERTY-CORROBORATION-REVIEW-Z087-Fr-density_value",
    )
    api_berkelium_corroboration_review = handle_api_request(
        "GET",
        "/evidence/physical-properties/corroboration/Bk",
    )
    api_californium_corroboration_review = handle_api_request(
        "GET",
        "/evidence/physical-properties/corroboration/Cf",
    )
    api_californium_density_review = handle_api_request(
        "GET",
        "/evidence/physical-properties/review/Cf",
    )
    api_californium_density_gap_closure = handle_api_request(
        "GET",
        "/evidence/physical-properties/gap-closure/Cf",
    )
    api_californium_density_closure_approval = handle_api_request(
        "GET",
        "/evidence/physical-properties/closure-approval/Cf",
    )
    api_californium_density_seed_update = handle_api_request(
        "GET",
        "/evidence/physical-properties/seed-update/Cf",
    )
    api_astatine_escalation = handle_api_request(
        "GET",
        "/evidence/physical-properties/escalations/At",
    )
    api_astatine_escalation_search = handle_api_request(
        "GET",
        "/evidence/physical-properties/escalation-search/At",
    )
    api_astatine_escalation_resolution = handle_api_request(
        "GET",
        "/evidence/physical-properties/escalation-resolution/At",
    )
    api_astatine_operator_decision = handle_api_request(
        "GET",
        "/evidence/physical-properties/operator-decisions/At",
    )
    api_astatine_continued_evidence = handle_api_request(
        "GET",
        "/evidence/physical-properties/continued-evidence/At",
    )
    api_fermium_no_candidate_review = handle_api_request(
        "GET",
        "/evidence/physical-properties/no-candidate/Fm",
    )
    api_mendelevium_no_candidate_review = handle_api_request(
        "GET",
        "/evidence/physical-properties/no-candidate/Md",
    )
    api_nobelium_no_candidate_review = handle_api_request(
        "GET",
        "/evidence/physical-properties/no-candidate/No",
    )
    api_lawrencium_no_candidate_review = handle_api_request(
        "GET",
        "/evidence/physical-properties/no-candidate/Lr",
    )
    api_astatine_secondary_evidence_template = handle_api_request(
        "GET",
        "/evidence/physical-properties/secondary-evidence/template/At",
    )
    api_bromine_matter_profile = handle_api_request("GET", "/matter/profiles/Br")
    api_technetium_isotope_source_policy = handle_api_request(
        "GET",
        "/atom/behavior/isotope-source-policy/Tc",
    )
    api_technetium_isotope_source_search = handle_api_request(
        "GET",
        "/atom/behavior/isotope-source-search/Tc",
    )
    api_oxygen_isotope_candidate_evidence = handle_api_request(
        "GET",
        "/atom/behavior/isotope-candidate-evidence/O",
    )
    api_oxygen_isotope_candidate_admission = handle_api_request(
        "GET",
        "/atom/behavior/isotope-candidate-admission/O",
    )
    api_technetium_isotope_candidate_admission = handle_api_request(
        "GET",
        "/atom/behavior/isotope-candidate-admission/Tc",
    )
    api_technetium_isotope_candidate_template = handle_api_request(
        "GET",
        "/atom/behavior/isotope-candidate-evidence/template/Tc",
    )
    api_cs_rn_promotion_profiles = handle_api_request("GET", "/promotion/cs-rn")
    api_astatine_promotion_profile = handle_api_request("GET", "/promotion/cs-rn/At")
    api_f_block_profiles = handle_api_request("GET", "/phase3/f-block")
    api_uranium_profile = handle_api_request("GET", "/phase3/f-block/U")
    api_period_5_level_2_profiles = handle_api_request("GET", "/level2/period-5")
    api_xenon_level_2_profile = handle_api_request("GET", "/level2/period-5/Xe")
    dashboard = build_element_dashboard_view_model("Zn", relation_type="same_block")
    assert api_health.status_code == 200, api_health
    assert api_health.payload["seed_count"] == 54, api_health.payload
    assert api_health.payload["isotope_candidate_admission_receipt_count"] == 2, (
        api_health.payload
    )
    assert api_graph.status_code == 200, api_graph
    assert api_graph.payload["graph"]["query"]["edge_count"] == 19, api_graph.payload
    assert api_dashboard.status_code == 200, api_dashboard
    assert api_dashboard.payload["dashboard"]["selected_element"]["symbol"] == "Zn", api_dashboard.payload
    assert api_chromium_reasoning.status_code == 200, api_chromium_reasoning
    assert (
        api_chromium_reasoning.payload["reasoning"]["evidence"]["configuration_audit"][
            "is_exception"
        ]
        is True
    )
    assert api_copper_potassium_reasoning.status_code == 200, api_copper_potassium_reasoning
    assert (
        api_copper_potassium_reasoning.payload["reasoning"]["evidence"]["surface_similarity"]
        is True
    )
    assert (
        api_copper_potassium_reasoning.payload["reasoning"]["evidence"]["deep_similarity"]
        is False
    )
    assert api_sodium_ion.status_code == 200, api_sodium_ion
    assert api_sodium_ion.payload["instance"]["electron_count"] == 10, api_sodium_ion.payload
    assert api_carbon_14.status_code == 200, api_carbon_14
    assert api_carbon_14.payload["instance"]["neutron_count"] == 8, api_carbon_14.payload
    assert api_carbon_14_evidence.status_code == 200, api_carbon_14_evidence
    assert api_carbon_14_evidence.payload["records"][0]["half_life_value"] == 5730.0, (
        api_carbon_14_evidence.payload
    )
    assert api_radon_unresolved_isotope.status_code == 200, (
        api_radon_unresolved_isotope
    )
    assert (
        api_radon_unresolved_isotope.payload["record"]["evidence_domain"]
        == "isotope_evidence"
    )
    assert api_iron_ion_evidence.status_code == 200, api_iron_ion_evidence
    assert len(api_iron_ion_evidence.payload["records"]) == 2, api_iron_ion_evidence.payload
    assert api_oxygen_unresolved_common_ion.status_code == 200, (
        api_oxygen_unresolved_common_ion
    )
    assert (
        api_oxygen_unresolved_common_ion.payload["record"]["evidence_domain"]
        == "common_ion_evidence"
    )
    assert api_astatine_configuration_evidence.status_code == 200, (
        api_astatine_configuration_evidence
    )
    assert api_astatine_configuration_evidence.payload["record"]["symbol"] == "At", (
        api_astatine_configuration_evidence.payload
    )
    assert api_gold_frontier.status_code == 200, api_gold_frontier
    assert api_gold_frontier.payload["record"]["d_shell"] == "5d^10", (
        api_gold_frontier.payload
    )
    assert api_gold_oxidation.status_code == 200, api_gold_oxidation
    assert api_gold_oxidation.payload["record"]["oxidation_states"] == [3, 1], (
        api_gold_oxidation.payload
    )
    assert api_gold_behavior.status_code == 200, api_gold_behavior
    assert "filled_d_shell_context" in (
        api_gold_behavior.payload["record"]["inferred_behavior_tags"]
    ), api_gold_behavior.payload
    assert api_gold_relation.status_code == 200, api_gold_relation
    assert api_gold_relation.payload["record"]["relation_edges"], api_gold_relation.payload
    assert api_promotion_batch_policy.status_code == 200, api_promotion_batch_policy
    assert api_promotion_batch_policy.payload["receipt"]["policy_decision"] == (
        "hold_full_cs_rn_span"
    ), api_promotion_batch_policy.payload
    assert api_astatine_decision.status_code == 200, api_astatine_decision
    assert api_astatine_decision.payload["receipt"]["decision_status"] == (
        "promotion_blocked_unresolved_physical_property"
    ), api_astatine_decision.payload
    assert api_bromine_properties.status_code == 200, api_bromine_properties
    assert api_bromine_properties.payload["record"]["standard_state"] == "Liquid", (
        api_bromine_properties.payload
    )
    assert api_astatine_unresolved_properties.status_code == 200, (
        api_astatine_unresolved_properties
    )
    assert api_astatine_unresolved_properties.payload["record"]["missing_fields"] == (
        "boiling_point_k",
    ), api_astatine_unresolved_properties.payload
    assert api_astatine_property_gap.status_code == 200, api_astatine_property_gap
    assert api_astatine_property_gap.payload["receipt"]["blocks_promotion_spans"] == [
        "Cs-Rn"
    ], api_astatine_property_gap.payload
    assert api_astatine_gap_workplan.status_code == 200, api_astatine_gap_workplan
    assert api_astatine_gap_workplan.payload["item"]["work_status"] == (
        "conflict_blocked_promotion"
    ), api_astatine_gap_workplan.payload
    assert api_protactinium_source_search.status_code == 200, api_protactinium_source_search
    assert api_protactinium_source_search.payload["receipt"]["search_status"] == (
        "source_search_complete_candidate_receipt_created"
    ), api_protactinium_source_search.payload
    assert api_francium_partial_source_search.status_code == 200, (
        api_francium_partial_source_search
    )
    assert api_francium_partial_source_search.payload["receipt"]["search_status"] == (
        "partial_source_search_open"
    ), api_francium_partial_source_search.payload
    assert api_astatine_secondary_source_policy.status_code == 200, (
        api_astatine_secondary_source_policy
    )
    assert api_astatine_secondary_source_policy.payload["policy"]["gap_closure_status"] == (
        "gap_not_closed_by_policy"
    ), api_astatine_secondary_source_policy.payload
    assert api_secondary_evidence.status_code == 200, api_secondary_evidence
    assert api_secondary_evidence.payload["validation"]["receipt_count"] == 8, (
        api_secondary_evidence.payload
    )
    assert api_secondary_evidence.payload["validation"]["admitted_count"] == 0, (
        api_secondary_evidence.payload
    )
    assert api_astatine_secondary_evidence_admission.status_code == 200, (
        api_astatine_secondary_evidence_admission
    )
    assert api_astatine_secondary_evidence_admission.payload["decision"]["closes_gap"] is False, (
        api_astatine_secondary_evidence_admission.payload
    )
    assert api_protactinium_secondary_evidence_admission.status_code == 200, (
        api_protactinium_secondary_evidence_admission
    )
    assert api_protactinium_secondary_evidence_admission.payload["decision"][
        "decision_status"
    ] == "secondary_evidence_not_admitted_conflict", (
        api_protactinium_secondary_evidence_admission.payload
    )
    assert api_astatine_property_conflict.status_code == 200, api_astatine_property_conflict
    assert api_astatine_property_conflict.payload["receipt"]["resolution_decision"] == (
        "blocked_pending_higher_precedence_source"
    ), api_astatine_property_conflict.payload
    assert api_astatine_property_conflict.payload["receipt"]["closes_gap"] is False, (
        api_astatine_property_conflict.payload
    )
    assert api_francium_property_conflict.status_code == 200, api_francium_property_conflict
    assert api_francium_property_conflict.payload["receipt"]["resolution_decision"] == (
        "blocked_pending_higher_precedence_source"
    ), api_francium_property_conflict.payload
    assert api_francium_density_corroboration_review.status_code == 200, (
        api_francium_density_corroboration_review
    )
    assert api_francium_density_corroboration_review.payload["receipt"]["review_decision"] == (
        "blocked_pending_corroborating_source"
    ), api_francium_density_corroboration_review.payload
    assert api_berkelium_corroboration_review.status_code == 200, (
        api_berkelium_corroboration_review
    )
    assert api_berkelium_corroboration_review.payload["receipt"]["review_decision"] == (
        "blocked_pending_corroborating_source"
    ), api_berkelium_corroboration_review.payload
    assert api_californium_corroboration_review.status_code == 200, (
        api_californium_corroboration_review
    )
    assert api_californium_corroboration_review.payload["receipt"]["review_decision"] == (
        "blocked_pending_corroborating_source"
    ), api_californium_corroboration_review.payload
    assert api_californium_density_review.status_code == 200, api_californium_density_review
    assert api_californium_density_review.payload["receipt"]["review_decision"] == (
        "resolved_admit_candidate"
    ), api_californium_density_review.payload
    assert api_californium_density_gap_closure.status_code == 200, (
        api_californium_density_gap_closure
    )
    assert api_californium_density_gap_closure.payload["decision"]["closure_status"] == (
        "gap_closure_ready_pending_operator_approval"
    ), api_californium_density_gap_closure.payload
    assert api_californium_density_closure_approval.status_code == 200, (
        api_californium_density_closure_approval
    )
    assert api_californium_density_closure_approval.payload["receipt"]["approval_status"] == (
        "closure_approval_deferred"
    ), api_californium_density_closure_approval.payload
    assert api_californium_density_seed_update.status_code == 200, (
        api_californium_density_seed_update
    )
    assert api_californium_density_seed_update.payload["receipt"]["update_status"] == (
        "seed_update_blocked_by_deferred_approval"
    ), api_californium_density_seed_update.payload
    assert api_astatine_escalation.status_code == 200, api_astatine_escalation
    assert api_astatine_escalation.payload["receipt"]["escalation_class"] == (
        "higher_precedence_source_required"
    ), api_astatine_escalation.payload
    assert api_astatine_escalation_search.status_code == 200, (
        api_astatine_escalation_search
    )
    assert api_astatine_escalation_search.payload["receipt"]["search_status"] == (
        "higher_precedence_source_not_found"
    ), api_astatine_escalation_search.payload
    assert api_astatine_escalation_resolution.status_code == 200, (
        api_astatine_escalation_resolution
    )
    assert api_astatine_escalation_resolution.payload["receipt"]["resolution_status"] == (
        "conflict_resolution_blocked_pending_operator_decision"
    ), api_astatine_escalation_resolution.payload
    assert api_astatine_operator_decision.status_code == 200, api_astatine_operator_decision
    assert api_astatine_operator_decision.payload["receipt"]["operator_decision_status"] == (
        "operator_decision_deferred"
    ), api_astatine_operator_decision.payload
    assert api_astatine_continued_evidence.status_code == 200, (
        api_astatine_continued_evidence
    )
    assert api_astatine_continued_evidence.payload["plan"]["plan_status"] == (
        "continued_evidence_required"
    ), api_astatine_continued_evidence.payload
    assert api_fermium_no_candidate_review.status_code == 200, (
        api_fermium_no_candidate_review
    )
    assert api_fermium_no_candidate_review.payload["receipt"]["review_decision"] == (
        "blocked_no_admissible_candidate_found"
    ), api_fermium_no_candidate_review.payload
    assert api_mendelevium_no_candidate_review.status_code == 200, (
        api_mendelevium_no_candidate_review
    )
    assert api_mendelevium_no_candidate_review.payload["receipt"]["review_decision"] == (
        "blocked_no_admissible_candidate_found"
    ), api_mendelevium_no_candidate_review.payload
    assert api_nobelium_no_candidate_review.status_code == 200, (
        api_nobelium_no_candidate_review
    )
    assert api_nobelium_no_candidate_review.payload["receipt"]["review_decision"] == (
        "blocked_no_admissible_candidate_found"
    ), api_nobelium_no_candidate_review.payload
    assert api_lawrencium_no_candidate_review.status_code == 200, (
        api_lawrencium_no_candidate_review
    )
    assert api_lawrencium_no_candidate_review.payload["receipt"]["review_decision"] == (
        "blocked_no_admissible_candidate_found"
    ), api_lawrencium_no_candidate_review.payload
    assert api_astatine_secondary_evidence_template.status_code == 200, (
        api_astatine_secondary_evidence_template
    )
    assert api_astatine_secondary_evidence_template.payload["template"]["field_name"] == (
        "boiling_point_k"
    ), api_astatine_secondary_evidence_template.payload
    assert api_bromine_matter_profile.status_code == 200, api_bromine_matter_profile
    assert api_bromine_matter_profile.payload["profile"]["standard_state"] == "Liquid", (
        api_bromine_matter_profile.payload
    )
    assert api_technetium_isotope_source_policy.status_code == 404, (
        api_technetium_isotope_source_policy
    )
    assert api_technetium_isotope_source_search.status_code == 404, (
        api_technetium_isotope_source_search
    )
    assert api_oxygen_isotope_candidate_evidence.status_code == 404, (
        api_oxygen_isotope_candidate_evidence
    )
    assert api_oxygen_isotope_candidate_admission.status_code == 200, (
        api_oxygen_isotope_candidate_admission
    )
    assert api_oxygen_isotope_candidate_admission.payload["receipt"]["symbol"] == "O", (
        api_oxygen_isotope_candidate_admission.payload
    )
    assert api_oxygen_isotope_candidate_admission.payload["receipt"][
        "active_candidate_receipt_retained"
    ] is False, api_oxygen_isotope_candidate_admission.payload
    assert api_technetium_isotope_candidate_admission.status_code == 200, (
        api_technetium_isotope_candidate_admission
    )
    assert api_technetium_isotope_candidate_admission.payload["receipt"]["symbol"] == "Tc", (
        api_technetium_isotope_candidate_admission.payload
    )
    assert api_technetium_isotope_candidate_admission.payload["receipt"][
        "admitted_mass_numbers"
    ] == [99], api_technetium_isotope_candidate_admission.payload
    assert api_technetium_isotope_candidate_template.status_code == 404, (
        api_technetium_isotope_candidate_template
    )
    assert api_cs_rn_promotion_profiles.status_code == 200, api_cs_rn_promotion_profiles
    assert api_cs_rn_promotion_profiles.payload["validation"]["profile_count"] == 32, (
        api_cs_rn_promotion_profiles.payload
    )
    assert api_astatine_promotion_profile.status_code == 200, api_astatine_promotion_profile
    assert api_astatine_promotion_profile.payload["profile"]["symbol"] == "At", (
        api_astatine_promotion_profile.payload
    )
    assert api_astatine_promotion_profile.payload["profile"]["readiness_status"] == (
        "promotion_blocked_missing_source_evidence"
    ), api_astatine_promotion_profile.payload
    assert api_f_block_profiles.status_code == 200, api_f_block_profiles
    assert api_f_block_profiles.payload["validation"]["profile_count"] == 30, (
        api_f_block_profiles.payload
    )
    assert api_uranium_profile.status_code == 200, api_uranium_profile
    assert api_uranium_profile.payload["profile"]["series"] == "actinide", api_uranium_profile.payload
    assert (
        api_uranium_profile.payload["profile"]["nuclear_state_extension_required"]
        is True
    )
    assert api_period_5_level_2_profiles.status_code == 200, api_period_5_level_2_profiles
    assert api_period_5_level_2_profiles.payload["validation"]["profile_count"] == 18, (
        api_period_5_level_2_profiles.payload
    )
    assert api_xenon_level_2_profile.status_code == 200, api_xenon_level_2_profile
    assert api_xenon_level_2_profile.payload["profile"]["symbol"] == "Xe", (
        api_xenon_level_2_profile.payload
    )
    assert api_xenon_level_2_profile.payload["profile"]["oxidation_states"] == [0], (
        api_xenon_level_2_profile.payload
    )
    assert dashboard.dashboard_status == "element_dashboard_view_model_ready", dashboard
    assert dashboard.selected_element is not None, dashboard
    assert dashboard.graph["query"]["edge_count"] == 19, dashboard.graph
    for phase in phases:
        missing = REQUIRED_KEYS - set(phase)
        assert not missing, (phase["phase"], sorted(missing))
        assert phase["phase_id"].startswith("MCMS-118-P")
        assert phase["artifacts"]["phase_metadata_json"]
        path = Path(phase["artifacts"]["phase_metadata_json"])
        assert path.exists(), path
        disk = json.loads(path.read_text())
        assert disk["phase"] == phase["phase"]
    print(
        f"phases={len(phases)} modules={len(modules)} "
        f"metadata_files={len(phases)} element_seeds={len(elements)} "
        f"element_snapshot_records={len(snapshot_records)} "
        f"f_block_profiles={len(f_block_profiles)} "
        f"period_5_level_2_profiles={len(period_5_level_2_profiles)} "
        f"isotope_evidence_records={len(isotope_evidence_records)} "
        f"common_ion_evidence_records={len(common_ion_evidence_records)} "
        f"unresolved_isotope_evidence_records={len(unresolved_isotope_evidence_records)} "
        f"unresolved_common_ion_evidence_records="
        f"{len(unresolved_common_ion_evidence_records)} "
        f"physical_property_evidence_records={len(physical_property_evidence_records)} "
        f"unresolved_physical_property_evidence_records="
        f"{len(unresolved_physical_property_evidence_records)} "
        f"physical_property_gap_audit_receipts={len(physical_property_gap_audit_receipts)} "
        f"physical_property_gap_work_items={len(physical_property_gap_work_items)} "
        f"physical_property_source_search_receipts={len(physical_property_source_search_receipts)} "
        f"partial_physical_property_source_search_receipts="
        f"{len(partial_physical_property_source_search_receipts)} "
        f"physical_property_secondary_source_policies="
        f"{len(physical_property_secondary_source_policies)} "
        f"physical_property_secondary_evidence_receipts="
        f"{len(physical_property_secondary_evidence_receipts)} "
        f"physical_property_secondary_evidence_admission_decisions="
        f"{len(physical_property_secondary_evidence_admission_decisions)} "
        f"physical_property_conflict_resolution_receipts="
        f"{len(physical_property_conflict_resolution_receipts)} "
        f"physical_property_corroboration_review_receipts="
        f"{len(physical_property_corroboration_review_receipts)} "
        f"physical_property_review_receipts={len(physical_property_review_receipts)} "
        f"physical_property_gap_closure_decisions="
        f"{len(physical_property_gap_closure_decisions)} "
        f"physical_property_closure_approval_receipts="
        f"{len(physical_property_closure_approval_receipts)} "
        f"physical_property_seed_update_receipts="
        f"{len(physical_property_seed_update_receipts)} "
        f"physical_property_escalation_receipts="
        f"{len(physical_property_escalation_receipts)} "
        f"physical_property_escalation_search_receipts="
        f"{len(physical_property_escalation_search_receipts)} "
        f"physical_property_escalation_resolution_receipts="
        f"{len(physical_property_escalation_resolution_receipts)} "
        f"physical_property_operator_decision_receipts="
        f"{len(physical_property_operator_decision_receipts)} "
        f"physical_property_continued_evidence_plans="
        f"{len(physical_property_continued_evidence_plans)} "
        f"physical_property_no_candidate_review_receipts="
        f"{len(physical_property_no_candidate_review_receipts)} "
        f"matter_behavior_profiles={len(matter_behavior_profiles)} "
        f"atom_behavior_profiles={len(atom_behavior_profiles)} "
        f"atom_behavior_gap_receipts={len(atom_behavior_gap_receipts)} "
        f"atom_behavior_gap_work_items={len(atom_behavior_gap_work_items)} "
        f"element_readiness_scores={len(element_readiness_scores)} "
        f"isotope_source_policies={len(isotope_source_policies)} "
        f"isotope_source_search_receipts={len(isotope_source_search_receipts)} "
        f"isotope_candidate_evidence_receipts={len(isotope_candidate_evidence_receipts)} "
        f"isotope_candidate_admission_receipts={len(isotope_candidate_admission_receipts)} "
        f"cs_rn_promotion_readiness_profiles={len(cs_rn_promotion_profiles)} "
        f"configuration_evidence_records={len(configuration_evidence_records)} "
        f"frontier_valence_signature_records={len(frontier_valence_records)} "
        f"oxidation_state_evidence_records={len(oxidation_state_evidence_records)} "
        f"behavior_tag_overlay_records={len(behavior_tag_records)} "
        f"relation_overlay_records={len(relation_overlay_records)} "
        f"promotion_decision_receipts={len(promotion_decision_receipts)} "
        f"promotion_batch_policy={promotion_batch_policy.policy_decision}"
    )


def verify_standard_files() -> None:
    for standard_file in STANDARD_FILES:
        if not Path(standard_file).exists():
            raise SystemExit(f"missing standard file: {standard_file}")
    print("standard_files=ok")


if __name__ == "__main__":
    main()
    verify_standard_files()
