from __future__ import annotations

import argparse
import json

from mcms.api import serve_api
from mcms.core.boundaries import compile_claim_boundary
from mcms.core.phases import latest_phase, load_phase_registry
from mcms.elements import (
    VALID_RELATION_TYPES,
    atom_behavior_profile_json_schema,
    build_atom_behavior_profile,
    build_element_dashboard_view_model,
    build_element_receipt,
    build_element_relation_graph,
    build_ion_instance,
    build_isotope_candidate_evidence_template,
    build_isotope_instance,
    build_matter_behavior_profile,
    build_physical_property_secondary_evidence_template,
    build_snapshot_receipt,
    element_schema_bundle,
    element_seed_json_schema,
    element_snapshot_json_schema,
    find_atom_behavior_profile,
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
    get_atom_behavior_gap_receipt,
    get_atom_behavior_gap_work_item,
    get_cs_rn_promotion_readiness_profile,
    get_element_readiness_score,
    get_isotope_candidate_admission_receipt,
    get_isotope_candidate_evidence_receipt,
    get_isotope_source_policy,
    get_isotope_source_search_receipt,
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
    validate_element_readiness_scores,
    validate_full_snapshot,
    validate_isotope_candidate_admission_receipts,
    validate_isotope_candidate_evidence_receipts,
    validate_isotope_source_policies,
    validate_isotope_source_search_receipts,
    validate_seed_pack,
)
from mcms.release.robust_evidence_network import analyze_robust_evidence_network


def cmd_demo() -> None:
    claim = compile_claim_boundary("NaCl is a compound made of sodium and chlorine", "source_backed_claim", 0.8)
    evidence = analyze_robust_evidence_network("release/demo", evidence_strength=0.9)
    print(json.dumps({"claim": claim.to_dict(), "robust_evidence": evidence.to_dict()}, indent=2))


def cmd_phases() -> None:
    phases = load_phase_registry()
    print(json.dumps({"count": len(phases), "latest": latest_phase()}, indent=2))


def _record_matches_identifier(record, identifier: str) -> bool:
    identifier_text = identifier.strip()
    candidate_values = (
        getattr(record, "symbol", None),
        str(getattr(record, "atomic_number", "")),
        getattr(record, "receipt_id", None),
        getattr(record, "decision_id", None),
        getattr(record, "target_receipt_id", None),
        getattr(record, "target_admission_decision_id", None),
    )
    return any(
        value is not None and identifier_text.upper() == str(value).upper()
        for value in candidate_values
    )


def _filter_records_by_identifier(records, identifier: str):
    matched_records = tuple(
        record for record in records if _record_matches_identifier(record, identifier)
    )
    if not matched_records:
        raise KeyError(f"unknown record identifier: {identifier}")
    return matched_records


def cmd_elements(
    symbol: str | None,
    list_only: bool,
    full_snapshot: bool,
    schema_name: str | None,
    graph_export: bool,
    dashboard_export: bool,
    relation_type: str | None,
    ion_charge: int | None = None,
    isotope_mass: int | None = None,
    isotope_evidence: bool = False,
    common_ion_evidence: bool = False,
    unresolved_common_ion_evidence: bool = False,
    physical_property_evidence: bool = False,
    unresolved_isotope_evidence: bool = False,
    unresolved_physical_property_evidence: bool = False,
    physical_property_gap_audit: bool = False,
    physical_property_gap_workplan: bool = False,
    physical_property_source_search: bool = False,
    partial_physical_property_source_search: bool = False,
    physical_property_secondary_evidence: bool = False,
    physical_property_secondary_evidence_admission: bool = False,
    physical_property_conflict_resolution: bool = False,
    physical_property_corroboration_review: bool = False,
    physical_property_review: bool = False,
    physical_property_gap_closure: bool = False,
    physical_property_closure_approval: bool = False,
    physical_property_seed_update: bool = False,
    physical_property_escalation: bool = False,
    physical_property_escalation_search: bool = False,
    physical_property_escalation_resolution: bool = False,
    physical_property_operator_decision: bool = False,
    physical_property_continued_evidence: bool = False,
    physical_property_no_candidate_review: bool = False,
    physical_property_secondary_evidence_template: bool = False,
    physical_property_secondary_source_policy: bool = False,
    matter_profile: bool = False,
    promotion_readiness: bool = False,
    configuration_evidence: bool = False,
    frontier_valence: bool = False,
    oxidation_state_evidence: bool = False,
    behavior_tags: bool = False,
    relation_overlay: bool = False,
    promotion_decision: bool = False,
    promotion_batch_policy: bool = False,
    atom_behavior: bool = False,
    atom_charge: int = 0,
    atom_behavior_gap: bool = False,
    atom_behavior_workplan: bool = False,
    isotope_source_policy: bool = False,
    isotope_source_search: bool = False,
    isotope_candidate_evidence: bool = False,
    isotope_candidate_evidence_template: bool = False,
    isotope_candidate_admission: bool = False,
    readiness_score: bool = False,
) -> None:
    if readiness_score:
        scores = (
            (get_element_readiness_score(symbol),)
            if symbol
            else list_element_readiness_scores()
        )
        print(
            json.dumps(
                {
                    "validation": validate_element_readiness_scores(scores),
                    "scores": [score.to_dict() for score in scores],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if isotope_candidate_admission:
        receipts = (
            (get_isotope_candidate_admission_receipt(symbol),)
            if symbol
            else list_isotope_candidate_admission_receipts()
        )
        print(
            json.dumps(
                {
                    "validation": validate_isotope_candidate_admission_receipts(receipts),
                    "receipts": [receipt.to_dict() for receipt in receipts],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if isotope_candidate_evidence_template:
        if symbol is None:
            raise ValueError("--isotope-candidate-evidence-template requires --symbol")
        print(
            json.dumps(
                {
                    "template": build_isotope_candidate_evidence_template(symbol),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if isotope_candidate_evidence:
        receipts = (
            (get_isotope_candidate_evidence_receipt(symbol),)
            if symbol
            else list_isotope_candidate_evidence_receipts()
        )
        print(
            json.dumps(
                {
                    "validation": validate_isotope_candidate_evidence_receipts(receipts),
                    "receipts": [receipt.to_dict() for receipt in receipts],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if isotope_source_search:
        receipts = (
            (get_isotope_source_search_receipt(symbol),)
            if symbol
            else list_isotope_source_search_receipts()
        )
        print(
            json.dumps(
                {
                    "validation": validate_isotope_source_search_receipts(receipts),
                    "receipts": [receipt.to_dict() for receipt in receipts],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if isotope_source_policy:
        policies = (
            (get_isotope_source_policy(symbol),)
            if symbol
            else list_isotope_source_policies()
        )
        print(
            json.dumps(
                {
                    "validation": validate_isotope_source_policies(policies),
                    "policies": [policy.to_dict() for policy in policies],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if atom_behavior_gap:
        receipts = (
            (get_atom_behavior_gap_receipt(symbol),)
            if symbol
            else list_atom_behavior_gap_receipts()
        )
        print(
            json.dumps(
                {
                    "validation": validate_atom_behavior_gap_receipts(receipts),
                    "receipts": [receipt.to_dict() for receipt in receipts],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if atom_behavior_workplan:
        items = (
            (get_atom_behavior_gap_work_item(symbol),)
            if symbol
            else list_atom_behavior_gap_work_items()
        )
        print(
            json.dumps(
                {
                    "validation": validate_atom_behavior_gap_work_items(items),
                    "items": [item.to_dict() for item in items],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if atom_behavior:
        if atom_charge != 0 and isotope_mass is None:
            raise ValueError("--atom-charge requires --isotope-mass")
        if symbol:
            profile = (
                build_atom_behavior_profile(
                    symbol,
                    isotope_mass,
                    charge=atom_charge,
                )
                if isotope_mass is not None
                else find_atom_behavior_profile(symbol)
            )
            profiles = (profile,)
        else:
            if atom_charge != 0:
                raise ValueError("--atom-charge requires --symbol and --isotope-mass")
            profiles = list_atom_behavior_profiles()
        print(
            json.dumps(
                {
                    "validation": validate_atom_behavior_profiles(profiles),
                    "profiles": [profile.to_dict() for profile in profiles],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if partial_physical_property_source_search:
        receipts = (
            (get_partial_physical_property_source_search_receipt(symbol),)
            if symbol
            else list_partial_physical_property_source_search_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_source_search:
        receipts = (
            (get_physical_property_source_search_receipt(symbol),)
            if symbol
            else list_physical_property_source_search_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_gap_workplan:
        items = (
            (get_physical_property_gap_work_item(symbol),)
            if symbol
            else list_physical_property_gap_work_items()
        )
        print(
            json.dumps(
                {"items": [item.to_dict() for item in items]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_conflict_resolution:
        receipts = (
            (get_physical_property_conflict_resolution_receipt(symbol),)
            if symbol
            else list_physical_property_conflict_resolution_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_corroboration_review:
        receipts = (
            (get_physical_property_corroboration_review_receipt(symbol),)
            if symbol
            else list_physical_property_corroboration_review_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_review:
        receipts = (
            (get_physical_property_review_receipt(symbol),)
            if symbol
            else list_physical_property_review_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_gap_closure:
        decisions = (
            (get_physical_property_gap_closure_decision(symbol),)
            if symbol
            else list_physical_property_gap_closure_decisions()
        )
        print(
            json.dumps(
                {"decisions": [decision.to_dict() for decision in decisions]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_closure_approval:
        receipts = (
            (get_physical_property_closure_approval_receipt(symbol),)
            if symbol
            else list_physical_property_closure_approval_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_seed_update:
        receipts = (
            (get_physical_property_seed_update_receipt(symbol),)
            if symbol
            else list_physical_property_seed_update_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_escalation:
        receipts = (
            (get_physical_property_escalation_receipt(symbol),)
            if symbol
            else list_physical_property_escalation_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_escalation_search:
        receipts = (
            (get_physical_property_escalation_search_receipt(symbol),)
            if symbol
            else list_physical_property_escalation_search_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_escalation_resolution:
        receipts = (
            (get_physical_property_escalation_resolution_receipt(symbol),)
            if symbol
            else list_physical_property_escalation_resolution_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_operator_decision:
        receipts = (
            (get_physical_property_operator_decision_receipt(symbol),)
            if symbol
            else list_physical_property_operator_decision_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_continued_evidence:
        plans = (
            (get_physical_property_continued_evidence_plan(symbol),)
            if symbol
            else list_physical_property_continued_evidence_plans()
        )
        print(
            json.dumps(
                {"plans": [plan.to_dict() for plan in plans]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_no_candidate_review:
        receipts = (
            (get_physical_property_no_candidate_review_receipt(symbol),)
            if symbol
            else list_physical_property_no_candidate_review_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_secondary_evidence_admission:
        decisions = (
            _filter_records_by_identifier(
                list_physical_property_secondary_evidence_admission_decisions(),
                symbol,
            )
            if symbol
            else list_physical_property_secondary_evidence_admission_decisions()
        )
        print(
            json.dumps(
                {"decisions": [decision.to_dict() for decision in decisions]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_secondary_evidence_template:
        if not symbol:
            raise ValueError("--physical-property-secondary-evidence-template requires --symbol")
        print(
            json.dumps(
                {"template": build_physical_property_secondary_evidence_template(symbol)},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_secondary_evidence:
        receipts = (
            _filter_records_by_identifier(
                list_physical_property_secondary_evidence_receipts(),
                symbol,
            )
            if symbol
            else list_physical_property_secondary_evidence_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_secondary_source_policy:
        policies = (
            (get_physical_property_secondary_source_policy(symbol),)
            if symbol
            else list_physical_property_secondary_source_policies()
        )
        print(
            json.dumps(
                {"policies": [policy.to_dict() for policy in policies]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_gap_audit:
        receipts = (
            (get_physical_property_gap_audit_receipt(symbol),)
            if symbol
            else list_physical_property_gap_audit_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if promotion_batch_policy:
        receipt = get_promotion_batch_policy_receipt()
        print(
            json.dumps(
                {"receipt": receipt.to_dict()},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if promotion_decision:
        receipts = (
            (get_promotion_decision_receipt(symbol),)
            if symbol
            else list_promotion_decision_receipts()
        )
        print(
            json.dumps(
                {"receipts": [receipt.to_dict() for receipt in receipts]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if relation_overlay:
        records = (
            (find_relation_overlay_record(symbol),)
            if symbol
            else list_relation_overlay_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if behavior_tags:
        records = (
            (find_behavior_tag_overlay_record(symbol),)
            if symbol
            else list_behavior_tag_overlay_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if oxidation_state_evidence:
        records = (
            (find_oxidation_state_evidence_record(symbol),)
            if symbol
            else list_oxidation_state_evidence_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if frontier_valence:
        records = (
            (find_frontier_valence_signature_record(symbol),)
            if symbol
            else list_frontier_valence_signature_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if configuration_evidence:
        records = (
            (find_configuration_evidence_record(symbol),)
            if symbol
            else list_configuration_evidence_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if promotion_readiness:
        profiles = (
            (get_cs_rn_promotion_readiness_profile(symbol),)
            if symbol
            else list_cs_rn_promotion_readiness_profiles()
        )
        print(
            json.dumps(
                {"profiles": [profile.to_dict() for profile in profiles]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if matter_profile:
        profiles = (
            (build_matter_behavior_profile(symbol),)
            if symbol
            else list_matter_behavior_profiles()
        )
        print(
            json.dumps(
                {"profiles": [profile.to_dict() for profile in profiles]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if physical_property_evidence:
        records = (
            (find_physical_property_evidence_record(symbol),)
            if symbol
            else list_physical_property_evidence_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if unresolved_isotope_evidence:
        records = (
            (find_unresolved_isotope_evidence_record(symbol),)
            if symbol
            else list_unresolved_isotope_evidence_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if unresolved_common_ion_evidence:
        records = (
            (find_unresolved_common_ion_evidence_record(symbol),)
            if symbol
            else list_unresolved_common_ion_evidence_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if unresolved_physical_property_evidence:
        records = (
            (find_unresolved_physical_property_evidence_record(symbol),)
            if symbol
            else list_unresolved_physical_property_evidence_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if isotope_evidence:
        records = (
            find_isotope_evidence_records(symbol, mass_number=isotope_mass)
            if symbol
            else list_isotope_evidence_records()
        )
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if common_ion_evidence:
        records = find_common_ion_evidence_records(symbol) if symbol else list_common_ion_evidence_records()
        print(
            json.dumps(
                {"records": [record.to_dict() for record in records]},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if ion_charge is not None:
        if not symbol:
            raise SystemExit("--ion-charge requires --symbol")
        instance = build_ion_instance(symbol, ion_charge)
        print(json.dumps({"instance": instance.to_dict()}, indent=2, sort_keys=True))
        return
    if isotope_mass is not None:
        if not symbol:
            raise SystemExit("--isotope-mass requires --symbol")
        instance = build_isotope_instance(symbol, isotope_mass)
        print(json.dumps({"instance": instance.to_dict()}, indent=2, sort_keys=True))
        return
    if schema_name:
        schema_builders = {
            "seed": element_seed_json_schema,
            "snapshot": element_snapshot_json_schema,
            "atom-behavior": atom_behavior_profile_json_schema,
            "bundle": element_schema_bundle,
        }
        print(json.dumps(schema_builders[schema_name](), indent=2, sort_keys=True))
        return
    if dashboard_export:
        dashboard = build_element_dashboard_view_model(
            identifier=symbol,
            relation_type=relation_type,
        )
        print(json.dumps(dashboard.to_dict(), indent=2, sort_keys=True))
        return
    if graph_export:
        graph = build_element_relation_graph(identifier=symbol, relation_type=relation_type)
        print(json.dumps(graph.to_dict(), indent=2, sort_keys=True))
        return
    if full_snapshot:
        if list_only:
            records = list_full_snapshot_records()
            print(
                json.dumps(
                    {
                        "count": len(records),
                        "symbols": [record.symbol for record in records],
                        "validation": validate_full_snapshot(records).to_dict(),
                    },
                    indent=2,
                )
            )
            return
        if symbol:
            record = get_snapshot_record(symbol)
            print(
                json.dumps(
                    {
                        "snapshot": record.to_dict(),
                        "receipt": build_snapshot_receipt(record),
                    },
                    indent=2,
                )
            )
            return
        print(json.dumps(validate_full_snapshot().to_dict(), indent=2))
        return
    if list_only:
        elements = list_seed_elements()
        print(
            json.dumps(
                {
                    "count": len(elements),
                    "symbols": [element.identity.symbol for element in elements],
                    "validation": validate_seed_pack().to_dict(),
                },
                indent=2,
            )
        )
        return
    if symbol:
        element = get_seed_element(symbol)
        print(
            json.dumps(
                {
                    "element": element.to_dict(),
                    "receipt": build_element_receipt(element),
                },
                indent=2,
            )
        )
        return
    print(json.dumps(validate_seed_pack().to_dict(), indent=2))


def cmd_api(host: str, port: int) -> None:
    serve_api(host=host, port=port)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="mcms")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    sub.add_parser("phases")
    api_parser = sub.add_parser("api")
    api_parser.add_argument("--host", default="127.0.0.1")
    api_parser.add_argument("--port", type=int, default=8765)
    elements_parser = sub.add_parser("elements")
    elements_parser.add_argument("--symbol", help="Element symbol, name, or atomic number")
    elements_parser.add_argument("--list", action="store_true", help="List MSPEE seed elements")
    elements_parser.add_argument(
        "--full",
        action="store_true",
        help="Use the full 118-element identity snapshot instead of the Level 1 seed pack",
    )
    elements_parser.add_argument(
        "--schema",
        choices=("seed", "snapshot", "atom-behavior", "bundle"),
        help="Print the JSON Schema contract for seed, snapshot, atom behavior, or bundle records",
    )
    elements_parser.add_argument(
        "--graph",
        action="store_true",
        help="Print the Level 1 element relation graph, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Print a dashboard-facing element read model, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--relation",
        choices=tuple(sorted(VALID_RELATION_TYPES)),
        help="Filter graph export by relation type",
    )
    elements_parser.add_argument(
        "--ion-charge",
        type=int,
        help="Build a formal ion instance for --symbol with the given nonzero charge",
    )
    elements_parser.add_argument(
        "--isotope-mass",
        type=int,
        help="Build a formal isotope instance for --symbol with the given mass number",
    )
    elements_parser.add_argument(
        "--atom-behavior",
        action="store_true",
        help="Print atom behavior v2 profiles, optionally filtered by --symbol and --isotope-mass",
    )
    elements_parser.add_argument(
        "--atom-charge",
        type=int,
        default=0,
        help="Apply a charge to --atom-behavior when --symbol and --isotope-mass are present",
    )
    elements_parser.add_argument(
        "--atom-behavior-gap",
        action="store_true",
        help="Print atom behavior v2 source-gap receipts, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--atom-behavior-workplan",
        action="store_true",
        help="Print atom behavior v2 gap work items, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--isotope-source-policy",
        action="store_true",
        help="Print isotope source policies for atom behavior v2 gaps, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--isotope-source-search",
        action="store_true",
        help="Print isotope source-search receipts for atom behavior v2 gaps, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--isotope-candidate-evidence",
        action="store_true",
        help="Print source-specific isotope candidate evidence receipts, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--isotope-candidate-evidence-template",
        action="store_true",
        help="Print an isotope candidate evidence receipt template for --symbol",
    )
    elements_parser.add_argument(
        "--isotope-candidate-admission",
        action="store_true",
        help="Print isotope candidate admission receipts, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--readiness-score",
        action="store_true",
        help="Print element readiness scores, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--isotope-evidence",
        action="store_true",
        help="Print isotope evidence records, optionally filtered by --symbol and --isotope-mass",
    )
    elements_parser.add_argument(
        "--common-ion-evidence",
        action="store_true",
        help="Print common-ion candidate evidence records, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--unresolved-isotope-evidence",
        action="store_true",
        help="Print unresolved isotope evidence receipts, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--unresolved-common-ion-evidence",
        action="store_true",
        help="Print unresolved common-ion evidence receipts, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--physical-property-evidence",
        action="store_true",
        help="Print measured physical-property evidence records, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--unresolved-physical-property-evidence",
        action="store_true",
        help="Print unresolved physical-property evidence records, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--physical-property-gap-audit",
        action="store_true",
        help="Print physical-property gap audit receipts, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--physical-property-gap-workplan",
        action="store_true",
        help="Print prioritized physical-property gap work items",
    )
    elements_parser.add_argument(
        "--physical-property-source-search",
        action="store_true",
        help="Print active physical-property source-search receipts",
    )
    elements_parser.add_argument(
        "--partial-physical-property-source-search",
        action="store_true",
        help="Print active partial physical-property source-search receipts",
    )
    elements_parser.add_argument(
        "--physical-property-secondary-source-policy",
        action="store_true",
        help="Print secondary-source admission policies for physical-property gaps",
    )
    elements_parser.add_argument(
        "--physical-property-secondary-evidence",
        action="store_true",
        help="Print admitted secondary physical-property evidence receipts",
    )
    elements_parser.add_argument(
        "--physical-property-secondary-evidence-admission",
        action="store_true",
        help="Print admission decisions for secondary physical-property evidence",
    )
    elements_parser.add_argument(
        "--physical-property-conflict-resolution",
        action="store_true",
        help="Print physical-property secondary-source conflict receipts",
    )
    elements_parser.add_argument(
        "--physical-property-corroboration-review",
        action="store_true",
        help="Print physical-property corroboration review receipts",
    )
    elements_parser.add_argument(
        "--physical-property-review",
        action="store_true",
        help="Print physical-property source review receipts",
    )
    elements_parser.add_argument(
        "--physical-property-gap-closure",
        action="store_true",
        help="Print physical-property gap-closure decisions",
    )
    elements_parser.add_argument(
        "--physical-property-closure-approval",
        action="store_true",
        help="Print physical-property closure approval receipts",
    )
    elements_parser.add_argument(
        "--physical-property-seed-update",
        action="store_true",
        help="Print physical-property seed-update receipts",
    )
    elements_parser.add_argument(
        "--physical-property-escalation",
        action="store_true",
        help="Print physical-property escalation receipts",
    )
    elements_parser.add_argument(
        "--physical-property-escalation-search",
        action="store_true",
        help="Print physical-property escalation-search receipts",
    )
    elements_parser.add_argument(
        "--physical-property-escalation-resolution",
        action="store_true",
        help="Print physical-property escalation-resolution recommendation receipts",
    )
    elements_parser.add_argument(
        "--physical-property-operator-decision",
        action="store_true",
        help="Print physical-property operator-decision receipts",
    )
    elements_parser.add_argument(
        "--physical-property-continued-evidence",
        action="store_true",
        help="Print physical-property continued-evidence plans",
    )
    elements_parser.add_argument(
        "--physical-property-no-candidate-review",
        action="store_true",
        help="Print physical-property no-candidate review receipts",
    )
    elements_parser.add_argument(
        "--physical-property-secondary-evidence-template",
        action="store_true",
        help="Print a source-specific secondary evidence receipt template for --symbol",
    )
    elements_parser.add_argument(
        "--matter-profile",
        action="store_true",
        help="Print bounded matter-behavior profiles, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--promotion-readiness",
        action="store_true",
        help="Print Cs-Rn promotion-readiness profiles, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--promotion-decision",
        action="store_true",
        help="Print Cs-Rn promotion decision receipts, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--promotion-batch-policy",
        action="store_true",
        help="Print the Cs-Rn span-level promotion batch policy receipt",
    )
    elements_parser.add_argument(
        "--configuration-evidence",
        action="store_true",
        help="Print Cs-Rn NIST configuration evidence, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--frontier-valence",
        action="store_true",
        help="Print Cs-Rn frontier and valence signatures, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--oxidation-state-evidence",
        action="store_true",
        help="Print Cs-Rn oxidation-state evidence, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--behavior-tags",
        action="store_true",
        help="Print Cs-Rn inferred behavior tag overlays, optionally filtered by --symbol",
    )
    elements_parser.add_argument(
        "--relation-overlay",
        action="store_true",
        help="Print Cs-Rn relation-edge overlays, optionally filtered by --symbol",
    )
    args = parser.parse_args(argv)
    if args.cmd == "demo":
        cmd_demo()
    elif args.cmd == "phases":
        cmd_phases()
    elif args.cmd == "api":
        cmd_api(args.host, args.port)
    elif args.cmd == "elements":
        cmd_elements(
            args.symbol,
            args.list,
            args.full,
            args.schema,
            args.graph,
            args.dashboard,
            args.relation,
            args.ion_charge,
            args.isotope_mass,
            args.isotope_evidence,
            args.common_ion_evidence,
            args.unresolved_common_ion_evidence,
            args.physical_property_evidence,
            args.unresolved_isotope_evidence,
            args.unresolved_physical_property_evidence,
            args.physical_property_gap_audit,
            args.physical_property_gap_workplan,
            args.physical_property_source_search,
            args.partial_physical_property_source_search,
            args.physical_property_secondary_evidence,
            args.physical_property_secondary_evidence_admission,
            args.physical_property_conflict_resolution,
            args.physical_property_corroboration_review,
            args.physical_property_review,
            args.physical_property_gap_closure,
            args.physical_property_closure_approval,
            args.physical_property_seed_update,
            args.physical_property_escalation,
            args.physical_property_escalation_search,
            args.physical_property_escalation_resolution,
            args.physical_property_operator_decision,
            args.physical_property_continued_evidence,
            args.physical_property_no_candidate_review,
            args.physical_property_secondary_evidence_template,
            args.physical_property_secondary_source_policy,
            args.matter_profile,
            args.promotion_readiness,
            args.configuration_evidence,
            args.frontier_valence,
            args.oxidation_state_evidence,
            args.behavior_tags,
            args.relation_overlay,
            args.promotion_decision,
            args.promotion_batch_policy,
            args.atom_behavior,
            args.atom_charge,
            args.atom_behavior_gap,
            args.atom_behavior_workplan,
            args.isotope_source_policy,
            args.isotope_source_search,
            args.isotope_candidate_evidence,
            args.isotope_candidate_evidence_template,
            args.isotope_candidate_admission,
            args.readiness_score,
        )


if __name__ == "__main__":
    main()
