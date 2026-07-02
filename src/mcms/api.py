"""Purpose: local read-only HTTP API for MSPEE element surfaces.

Project scope: exposes existing validated element, snapshot, schema, graph, and reasoning contracts.
Dependencies: Python standard-library HTTP server and local MSPEE APIs.
Invariants: API routes do not mutate state; every error response carries causal context.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

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
    compare_outer_shell_similarity,
    element_schema_bundle,
    element_seed_json_schema,
    element_snapshot_json_schema,
    explain_configuration_choice,
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
    get_f_block_expansion_profile,
    get_full_span_promotion_approval_review_receipt,
    get_isotope_candidate_admission_receipt,
    get_isotope_candidate_evidence_receipt,
    get_isotope_source_policy,
    get_isotope_source_search_receipt,
    get_partial_physical_property_source_search_receipt,
    get_partial_promotion_eligibility_receipt,
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
    validate_full_span_promotion_approval_review_receipt,
    validate_isotope_candidate_admission_receipts,
    validate_isotope_candidate_evidence_receipts,
    validate_isotope_evidence_records,
    validate_isotope_source_policies,
    validate_isotope_source_search_receipts,
    validate_matter_behavior_profiles,
    validate_oxidation_state_evidence_records,
    validate_partial_physical_property_source_search_receipts,
    validate_partial_promotion_eligibility_receipt,
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

API_STATUS = "mcms_local_api_ready"
API_VERSION = "0.1.0"


@dataclass(frozen=True)
class ApiResponse:
    status_code: int
    payload: dict[str, Any]

    def to_json_bytes(self) -> bytes:
        return json.dumps(self.payload, indent=2, sort_keys=True).encode("utf-8")


def _error_response(status_code: int, error: str, detail: str) -> ApiResponse:
    return ApiResponse(
        status_code=status_code,
        payload={
            "api_status": "mcms_local_api_error",
            "error": error,
            "detail": detail,
        },
    )


def _first_query_value(query: dict[str, list[str]], key: str) -> str | None:
    values = query.get(key, [])
    if not values:
        return None
    value = values[0].strip()
    return value or None


def _required_int_query_value(query: dict[str, list[str]], key: str) -> int:
    raw_value = _first_query_value(query, key)
    if raw_value is None:
        raise ValueError(f"missing required integer query value: {key}")
    try:
        return int(raw_value)
    except ValueError as error:
        raise ValueError(f"invalid integer query value for {key}: {raw_value}") from error


def _optional_int_query_value(
    query: dict[str, list[str]],
    key: str,
    default: int | None = None,
) -> int | None:
    raw_value = _first_query_value(query, key)
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError as error:
        raise ValueError(f"invalid integer query value for {key}: {raw_value}") from error


def _index_payload() -> dict[str, Any]:
    return {
        "api_status": API_STATUS,
        "api_version": API_VERSION,
        "routes": [
            "GET /health",
            "GET /elements",
            "GET /elements/{symbol|name|atomic_number}",
            "GET /snapshot",
            "GET /snapshot/{symbol|name|atomic_number}",
            "GET /schemas/{seed|snapshot|atom-behavior|bundle}",
            "GET /graph",
            "GET /graph?symbol=Zn&relation=same_block",
            "GET /dashboard",
            "GET /dashboard?symbol=Zn&relation=same_block",
            "GET /reasoning/configuration/Cr",
            "GET /reasoning/similarity?left=Cu&right=K",
            "GET /instances/ion/Na?charge=1",
            "GET /instances/isotope/C?mass_number=14",
            "GET /atom/behavior",
            "GET /atom/behavior/C?mass_number=14",
            "GET /atom/behavior/C?mass_number=14&charge=1",
            "GET /atom/behavior/gaps",
            "GET /atom/behavior/gaps/Rn",
            "GET /atom/behavior/workplan",
            "GET /atom/behavior/workplan/Rn",
            "GET /atom/behavior/isotope-source-policy",
            "GET /atom/behavior/isotope-source-search",
            "GET /atom/behavior/isotope-candidate-evidence",
            "GET /atom/behavior/isotope-candidate-admission",
            "GET /atom/behavior/isotope-candidate-admission/O",
            "GET /atom/behavior/isotope-candidate-admission/Tc",
            "GET /scoring/readiness",
            "GET /scoring/readiness/Tc",
            "GET /evidence/isotopes",
            "GET /evidence/isotopes/C?mass_number=14",
            "GET /evidence/isotopes/unresolved",
            "GET /evidence/isotopes/unresolved/Rn",
            "GET /evidence/common-ions",
            "GET /evidence/common-ions/Fe",
            "GET /evidence/common-ions/unresolved",
            "GET /evidence/common-ions/unresolved/O",
            "GET /evidence/configurations",
            "GET /evidence/configurations/At",
            "GET /evidence/oxidation-states",
            "GET /evidence/oxidation-states/Au",
            "GET /evidence/physical-properties",
            "GET /evidence/physical-properties/Br",
            "GET /evidence/physical-properties/unresolved",
            "GET /evidence/physical-properties/unresolved/At",
            "GET /evidence/physical-properties/gaps",
            "GET /evidence/physical-properties/gaps/At",
            "GET /evidence/physical-properties/workplan",
            "GET /evidence/physical-properties/workplan/At",
            "GET /evidence/physical-properties/source-search",
            "GET /evidence/physical-properties/source-search/Pa",
            "GET /evidence/physical-properties/partial-source-search/Fr",
            "GET /evidence/physical-properties/secondary-evidence",
            "GET /evidence/physical-properties/secondary-evidence/admission/At",
            "GET /evidence/physical-properties/conflicts/At",
            "GET /evidence/physical-properties/corroboration/Bk",
            "GET /evidence/physical-properties/review/Cf",
            "GET /evidence/physical-properties/gap-closure/Cf",
            "GET /evidence/physical-properties/closure-approval/Cf",
            "GET /evidence/physical-properties/seed-update/Cf",
            "GET /evidence/physical-properties/escalations/Fr",
            "GET /evidence/physical-properties/escalation-search/Fr",
            "GET /evidence/physical-properties/escalation-resolution/Fr",
            "GET /evidence/physical-properties/operator-decisions/Fr",
            "GET /evidence/physical-properties/continued-evidence/Fr",
            "GET /evidence/physical-properties/no-candidate/Fm",
            "GET /evidence/physical-properties/secondary-evidence/template/At",
            "GET /evidence/physical-properties/secondary-source-policy",
            "GET /evidence/physical-properties/secondary-source-policy/At",
            "GET /frontier/cs-rn",
            "GET /frontier/cs-rn/Au",
            "GET /behavior/cs-rn",
            "GET /behavior/cs-rn/Au",
            "GET /relations/cs-rn",
            "GET /relations/cs-rn/Au",
            "GET /matter/profiles",
            "GET /matter/profiles/Br",
            "GET /promotion/cs-rn",
            "GET /promotion/cs-rn/At",
            "GET /promotion/batch-policy",
            "GET /promotion/partial-eligibility",
            "GET /promotion/full-span-approval-review",
            "GET /promotion/decisions",
            "GET /promotion/decisions/At",
            "GET /phase3/f-block",
            "GET /phase3/f-block/U",
            "GET /level2/period-5",
            "GET /level2/period-5/Xe",
        ],
        "relation_types": sorted(VALID_RELATION_TYPES),
    }


def _seed_list_payload() -> dict[str, Any]:
    elements = list_seed_elements()
    return {
        "api_status": API_STATUS,
        "count": len(elements),
        "symbols": [element.identity.symbol for element in elements],
        "validation": validate_seed_pack(elements).to_dict(),
    }


def _snapshot_list_payload() -> dict[str, Any]:
    records = list_full_snapshot_records()
    return {
        "api_status": API_STATUS,
        "count": len(records),
        "symbols": [record.symbol for record in records],
        "validation": validate_full_snapshot(records).to_dict(),
    }


def _schema_payload(schema_name: str) -> dict[str, Any]:
    schema_builders = {
        "seed": element_seed_json_schema,
        "snapshot": element_snapshot_json_schema,
        "atom-behavior": atom_behavior_profile_json_schema,
        "bundle": element_schema_bundle,
    }
    if schema_name not in schema_builders:
        raise KeyError(f"unknown schema: {schema_name}")
    return {"api_status": API_STATUS, "schema": schema_builders[schema_name]()}


def _graph_payload(identifier: str | None, relation_type: str | None) -> dict[str, Any]:
    graph = build_element_relation_graph(identifier=identifier, relation_type=relation_type)
    return {"api_status": API_STATUS, "graph": graph.to_dict()}


def _dashboard_payload(identifier: str | None, relation_type: str | None) -> dict[str, Any]:
    dashboard = build_element_dashboard_view_model(
        identifier=identifier,
        relation_type=relation_type,
    )
    return {"api_status": API_STATUS, "dashboard": dashboard.to_dict()}


def _configuration_reasoning_payload(identifier: str) -> dict[str, Any]:
    reasoning = explain_configuration_choice(identifier)
    return {"api_status": API_STATUS, "reasoning": reasoning.to_dict()}


def _similarity_reasoning_payload(left: str | None, right: str | None) -> dict[str, Any]:
    if left is None or right is None:
        raise ValueError("reasoning similarity requires left and right query values.")
    reasoning = compare_outer_shell_similarity(left, right)
    return {"api_status": API_STATUS, "reasoning": reasoning.to_dict()}


def _ion_instance_payload(identifier: str, charge: int) -> dict[str, Any]:
    instance = build_ion_instance(identifier, charge)
    return {
        "api_status": API_STATUS,
        "instance": instance.to_dict(),
        "validation_errors": instance.validate(),
    }


def _isotope_instance_payload(identifier: str, mass_number: int) -> dict[str, Any]:
    instance = build_isotope_instance(identifier, mass_number)
    return {
        "api_status": API_STATUS,
        "instance": instance.to_dict(),
        "validation_errors": instance.validate(),
    }


def _isotope_evidence_list_payload() -> dict[str, Any]:
    records = list_isotope_evidence_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_evidence_records(records),
        "records": [record.to_dict() for record in records],
    }


def _isotope_evidence_payload(
    identifier: str,
    mass_number: int | None,
) -> dict[str, Any]:
    records = find_isotope_evidence_records(identifier, mass_number=mass_number)
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_evidence_records(records),
        "records": [record.to_dict() for record in records],
    }


def _unresolved_isotope_evidence_list_payload() -> dict[str, Any]:
    records = list_unresolved_isotope_evidence_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_unresolved_evidence_records(
            records,
            expected_domain="isotope_evidence",
        ),
        "records": [record.to_dict() for record in records],
    }


def _unresolved_isotope_evidence_payload(identifier: str) -> dict[str, Any]:
    record = find_unresolved_isotope_evidence_record(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_unresolved_evidence_records(
            (record,),
            expected_domain="isotope_evidence",
        ),
        "record": record.to_dict(),
    }


def _common_ion_evidence_list_payload() -> dict[str, Any]:
    records = list_common_ion_evidence_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_common_ion_evidence_records(records),
        "records": [record.to_dict() for record in records],
    }


def _unresolved_common_ion_evidence_list_payload() -> dict[str, Any]:
    records = list_unresolved_common_ion_evidence_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_unresolved_evidence_records(
            records,
            expected_domain="common_ion_evidence",
        ),
        "records": [record.to_dict() for record in records],
    }


def _unresolved_common_ion_evidence_payload(identifier: str) -> dict[str, Any]:
    record = find_unresolved_common_ion_evidence_record(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_unresolved_evidence_records(
            (record,),
            expected_domain="common_ion_evidence",
        ),
        "record": record.to_dict(),
    }


def _common_ion_evidence_payload(identifier: str) -> dict[str, Any]:
    records = find_common_ion_evidence_records(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_common_ion_evidence_records(records),
        "records": [record.to_dict() for record in records],
    }


def _configuration_evidence_list_payload() -> dict[str, Any]:
    records = list_configuration_evidence_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_configuration_evidence_records(records),
        "records": [record.to_dict() for record in records],
    }


def _configuration_evidence_payload(identifier: str) -> dict[str, Any]:
    record = find_configuration_evidence_record(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_configuration_evidence_records((record,)),
        "record": record.to_dict(),
    }


def _frontier_valence_list_payload() -> dict[str, Any]:
    records = list_frontier_valence_signature_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_frontier_valence_signature_records(records),
        "records": [record.to_dict() for record in records],
    }


def _frontier_valence_payload(identifier: str) -> dict[str, Any]:
    record = find_frontier_valence_signature_record(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_frontier_valence_signature_records((record,)),
        "record": record.to_dict(),
    }


def _oxidation_state_evidence_list_payload() -> dict[str, Any]:
    records = list_oxidation_state_evidence_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_oxidation_state_evidence_records(records),
        "records": [record.to_dict() for record in records],
    }


def _oxidation_state_evidence_payload(identifier: str) -> dict[str, Any]:
    record = find_oxidation_state_evidence_record(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_oxidation_state_evidence_records((record,)),
        "record": record.to_dict(),
    }


def _behavior_tag_overlay_list_payload() -> dict[str, Any]:
    records = list_behavior_tag_overlay_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_behavior_tag_overlay_records(records),
        "records": [record.to_dict() for record in records],
    }


def _behavior_tag_overlay_payload(identifier: str) -> dict[str, Any]:
    record = find_behavior_tag_overlay_record(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_behavior_tag_overlay_records((record,)),
        "record": record.to_dict(),
    }


def _relation_overlay_list_payload() -> dict[str, Any]:
    records = list_relation_overlay_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_relation_overlay_records(records),
        "records": [record.to_dict() for record in records],
    }


def _relation_overlay_payload(identifier: str) -> dict[str, Any]:
    record = find_relation_overlay_record(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_relation_overlay_records((record,)),
        "record": record.to_dict(),
    }


def _physical_property_evidence_list_payload() -> dict[str, Any]:
    records = list_physical_property_evidence_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_evidence_records(records),
        "records": [record.to_dict() for record in records],
    }


def _physical_property_evidence_payload(identifier: str) -> dict[str, Any]:
    record = find_physical_property_evidence_record(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_evidence_records((record,)),
        "record": record.to_dict(),
    }


def _physical_property_gap_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_gap_audit_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_gap_audit_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_gap_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_gap_audit_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_gap_audit_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_gap_workplan_list_payload() -> dict[str, Any]:
    items = list_physical_property_gap_work_items()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_gap_work_items(items),
        "items": [item.to_dict() for item in items],
    }


def _physical_property_gap_workplan_payload(identifier: str) -> dict[str, Any]:
    item = get_physical_property_gap_work_item(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_gap_work_items((item,)),
        "item": item.to_dict(),
    }


def _physical_property_source_search_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_source_search_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_source_search_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_source_search_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_source_search_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_source_search_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _partial_physical_property_source_search_list_payload() -> dict[str, Any]:
    receipts = list_partial_physical_property_source_search_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_partial_physical_property_source_search_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _partial_physical_property_source_search_payload(identifier: str) -> dict[str, Any]:
    receipt = get_partial_physical_property_source_search_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_partial_physical_property_source_search_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_secondary_source_policy_list_payload() -> dict[str, Any]:
    policies = list_physical_property_secondary_source_policies()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_secondary_source_policies(policies),
        "policies": [policy.to_dict() for policy in policies],
    }


def _physical_property_secondary_source_policy_payload(identifier: str) -> dict[str, Any]:
    policy = get_physical_property_secondary_source_policy(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_secondary_source_policies((policy,)),
        "policy": policy.to_dict(),
    }


def _physical_property_secondary_evidence_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_secondary_evidence_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_secondary_evidence_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_secondary_evidence_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_secondary_evidence_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_secondary_evidence_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_secondary_evidence_template_payload(identifier: str) -> dict[str, Any]:
    return {
        "api_status": API_STATUS,
        "template": build_physical_property_secondary_evidence_template(identifier),
    }


def _physical_property_secondary_evidence_admission_list_payload() -> dict[str, Any]:
    decisions = list_physical_property_secondary_evidence_admission_decisions()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_secondary_evidence_admission_decisions(
            decisions
        ),
        "decisions": [decision.to_dict() for decision in decisions],
    }


def _physical_property_secondary_evidence_admission_payload(identifier: str) -> dict[str, Any]:
    decision = get_physical_property_secondary_evidence_admission_decision(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_secondary_evidence_admission_decisions(
            (decision,)
        ),
        "decision": decision.to_dict(),
    }


def _physical_property_conflict_resolution_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_conflict_resolution_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_conflict_resolution_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_conflict_resolution_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_conflict_resolution_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_conflict_resolution_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_corroboration_review_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_corroboration_review_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_corroboration_review_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_corroboration_review_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_corroboration_review_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_corroboration_review_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_review_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_review_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_review_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_review_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_review_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_review_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_gap_closure_decision_list_payload() -> dict[str, Any]:
    decisions = list_physical_property_gap_closure_decisions()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_gap_closure_decisions(decisions),
        "decisions": [decision.to_dict() for decision in decisions],
    }


def _physical_property_gap_closure_decision_payload(identifier: str) -> dict[str, Any]:
    decision = get_physical_property_gap_closure_decision(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_gap_closure_decisions((decision,)),
        "decision": decision.to_dict(),
    }


def _physical_property_closure_approval_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_closure_approval_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_closure_approval_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_closure_approval_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_closure_approval_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_closure_approval_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_seed_update_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_seed_update_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_seed_update_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_seed_update_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_seed_update_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_seed_update_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_escalation_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_escalation_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_escalation_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_escalation_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_escalation_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_escalation_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_escalation_search_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_escalation_search_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_escalation_search_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_escalation_search_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_escalation_search_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_escalation_search_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_escalation_resolution_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_escalation_resolution_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_escalation_resolution_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_escalation_resolution_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_escalation_resolution_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_escalation_resolution_receipts(
            (receipt,)
        ),
        "receipt": receipt.to_dict(),
    }


def _physical_property_operator_decision_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_operator_decision_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_operator_decision_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_operator_decision_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_operator_decision_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_operator_decision_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _physical_property_continued_evidence_list_payload() -> dict[str, Any]:
    plans = list_physical_property_continued_evidence_plans()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_continued_evidence_plans(plans),
        "plans": [plan.to_dict() for plan in plans],
    }


def _physical_property_continued_evidence_payload(identifier: str) -> dict[str, Any]:
    plan = get_physical_property_continued_evidence_plan(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_continued_evidence_plans((plan,)),
        "plan": plan.to_dict(),
    }


def _physical_property_no_candidate_review_list_payload() -> dict[str, Any]:
    receipts = list_physical_property_no_candidate_review_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_no_candidate_review_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _physical_property_no_candidate_review_payload(identifier: str) -> dict[str, Any]:
    receipt = get_physical_property_no_candidate_review_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_physical_property_no_candidate_review_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _unresolved_physical_property_evidence_list_payload() -> dict[str, Any]:
    records = list_unresolved_physical_property_evidence_records()
    return {
        "api_status": API_STATUS,
        "validation": validate_unresolved_physical_property_evidence_records(records),
        "records": [record.to_dict() for record in records],
    }


def _unresolved_physical_property_evidence_payload(identifier: str) -> dict[str, Any]:
    record = find_unresolved_physical_property_evidence_record(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_unresolved_physical_property_evidence_records((record,)),
        "record": record.to_dict(),
    }


def _matter_profile_list_payload() -> dict[str, Any]:
    profiles = list_matter_behavior_profiles()
    return {
        "api_status": API_STATUS,
        "validation": validate_matter_behavior_profiles(profiles),
        "profiles": [profile.to_dict() for profile in profiles],
    }


def _matter_profile_payload(identifier: str) -> dict[str, Any]:
    profile = build_matter_behavior_profile(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_matter_behavior_profiles((profile,)),
        "profile": profile.to_dict(),
    }


def _atom_behavior_list_payload() -> dict[str, Any]:
    profiles = list_atom_behavior_profiles()
    return {
        "api_status": API_STATUS,
        "validation": validate_atom_behavior_profiles(profiles),
        "profiles": [profile.to_dict() for profile in profiles],
    }


def _atom_behavior_payload(
    identifier: str,
    mass_number: int | None,
    charge: int,
) -> dict[str, Any]:
    if mass_number is None and charge != 0:
        raise ValueError("atom behavior charge requires mass_number.")
    profile = (
        build_atom_behavior_profile(identifier, mass_number, charge=charge)
        if mass_number is not None
        else find_atom_behavior_profile(identifier, charge=charge)
    )
    return {
        "api_status": API_STATUS,
        "validation": validate_atom_behavior_profiles((profile,)),
        "profile": profile.to_dict(),
    }


def _atom_behavior_gap_list_payload() -> dict[str, Any]:
    receipts = list_atom_behavior_gap_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_atom_behavior_gap_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _atom_behavior_gap_payload(identifier: str) -> dict[str, Any]:
    receipt = get_atom_behavior_gap_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_atom_behavior_gap_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _atom_behavior_gap_workplan_list_payload() -> dict[str, Any]:
    items = list_atom_behavior_gap_work_items()
    return {
        "api_status": API_STATUS,
        "validation": validate_atom_behavior_gap_work_items(items),
        "items": [item.to_dict() for item in items],
    }


def _atom_behavior_gap_workplan_payload(identifier: str) -> dict[str, Any]:
    item = get_atom_behavior_gap_work_item(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_atom_behavior_gap_work_items((item,)),
        "item": item.to_dict(),
    }


def _isotope_source_policy_list_payload() -> dict[str, Any]:
    policies = list_isotope_source_policies()
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_source_policies(policies),
        "policies": [policy.to_dict() for policy in policies],
    }


def _isotope_source_policy_payload(identifier: str) -> dict[str, Any]:
    policy = get_isotope_source_policy(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_source_policies((policy,)),
        "policy": policy.to_dict(),
    }


def _isotope_source_search_list_payload() -> dict[str, Any]:
    receipts = list_isotope_source_search_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_source_search_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _isotope_source_search_payload(identifier: str) -> dict[str, Any]:
    receipt = get_isotope_source_search_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_source_search_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _isotope_candidate_evidence_list_payload() -> dict[str, Any]:
    receipts = list_isotope_candidate_evidence_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_candidate_evidence_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _isotope_candidate_evidence_payload(identifier: str) -> dict[str, Any]:
    receipt = get_isotope_candidate_evidence_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_candidate_evidence_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _isotope_candidate_evidence_template_payload(identifier: str) -> dict[str, Any]:
    return {
        "api_status": API_STATUS,
        "template": build_isotope_candidate_evidence_template(identifier),
    }


def _isotope_candidate_admission_list_payload() -> dict[str, Any]:
    receipts = list_isotope_candidate_admission_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_candidate_admission_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _isotope_candidate_admission_payload(identifier: str) -> dict[str, Any]:
    receipt = get_isotope_candidate_admission_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_isotope_candidate_admission_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _readiness_score_list_payload() -> dict[str, Any]:
    scores = list_element_readiness_scores()
    return {
        "api_status": API_STATUS,
        "validation": validate_element_readiness_scores(scores),
        "scores": [score.to_dict() for score in scores],
    }


def _readiness_score_payload(identifier: str) -> dict[str, Any]:
    score = get_element_readiness_score(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_element_readiness_scores((score,)),
        "score": score.to_dict(),
    }


def _cs_rn_promotion_readiness_list_payload() -> dict[str, Any]:
    profiles = list_cs_rn_promotion_readiness_profiles()
    return {
        "api_status": API_STATUS,
        "validation": validate_cs_rn_promotion_readiness_profiles(profiles).to_dict(),
        "profiles": [profile.to_dict() for profile in profiles],
    }


def _cs_rn_promotion_readiness_payload(identifier: str) -> dict[str, Any]:
    profile = get_cs_rn_promotion_readiness_profile(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_cs_rn_promotion_readiness_profiles((profile,)).to_dict(),
        "profile": profile.to_dict(),
    }


def _promotion_decision_list_payload() -> dict[str, Any]:
    receipts = list_promotion_decision_receipts()
    return {
        "api_status": API_STATUS,
        "validation": validate_promotion_decision_receipts(receipts),
        "receipts": [receipt.to_dict() for receipt in receipts],
    }


def _promotion_decision_payload(identifier: str) -> dict[str, Any]:
    receipt = get_promotion_decision_receipt(identifier)
    return {
        "api_status": API_STATUS,
        "validation": validate_promotion_decision_receipts((receipt,)),
        "receipt": receipt.to_dict(),
    }


def _promotion_batch_policy_payload() -> dict[str, Any]:
    receipt = get_promotion_batch_policy_receipt()
    return {
        "api_status": API_STATUS,
        "validation": validate_promotion_batch_policy_receipt(receipt),
        "receipt": receipt.to_dict(),
    }


def _partial_promotion_eligibility_payload() -> dict[str, Any]:
    receipt = get_partial_promotion_eligibility_receipt()
    return {
        "api_status": API_STATUS,
        "validation": validate_partial_promotion_eligibility_receipt(receipt),
        "receipt": receipt.to_dict(),
    }


def _full_span_promotion_approval_review_payload() -> dict[str, Any]:
    receipt = get_full_span_promotion_approval_review_receipt()
    return {
        "api_status": API_STATUS,
        "validation": validate_full_span_promotion_approval_review_receipt(receipt),
        "receipt": receipt.to_dict(),
    }


def _f_block_list_payload() -> dict[str, Any]:
    profiles = list_f_block_expansion_profiles()
    return {
        "api_status": API_STATUS,
        "validation": validate_f_block_expansion_profiles(profiles).to_dict(),
        "profiles": [profile.to_dict() for profile in profiles],
    }


def _f_block_profile_payload(identifier: str) -> dict[str, Any]:
    profile = get_f_block_expansion_profile(identifier)
    return {"api_status": API_STATUS, "profile": profile.to_dict()}


def _period_5_level_2_list_payload() -> dict[str, Any]:
    profiles = list_period_5_level_2_profiles()
    return {
        "api_status": API_STATUS,
        "validation": validate_period_5_level_2_profiles(profiles).to_dict(),
        "profiles": [profile.to_dict() for profile in profiles],
    }


def _period_5_level_2_profile_payload(identifier: str) -> dict[str, Any]:
    profile = get_period_5_level_2_profile(identifier)
    return {"api_status": API_STATUS, "profile": profile.to_dict()}


def handle_api_request(method: str, raw_target: str) -> ApiResponse:
    if method.upper() != "GET":
        return _error_response(
            HTTPStatus.METHOD_NOT_ALLOWED,
            "method_not_allowed",
            "Only GET is supported by the local read-only API.",
        )

    parsed_target = urlparse(raw_target)
    path_parts = [
        unquote(part)
        for part in parsed_target.path.strip("/").split("/")
        if part
    ]
    query = parse_qs(parsed_target.query)

    try:
        if not path_parts:
            return ApiResponse(HTTPStatus.OK, _index_payload())
        if path_parts == ["health"]:
            return ApiResponse(
                HTTPStatus.OK,
                {
                    "api_status": API_STATUS,
                    "seed_count": len(list_seed_elements()),
                    "snapshot_count": len(list_full_snapshot_records()),
                    "atom_behavior_profile_count": len(list_atom_behavior_profiles()),
                    "atom_behavior_gap_count": len(list_atom_behavior_gap_receipts()),
                    "atom_behavior_gap_work_item_count": len(
                        list_atom_behavior_gap_work_items()
                    ),
                    "isotope_source_policy_count": len(list_isotope_source_policies()),
                    "isotope_source_search_receipt_count": len(
                        list_isotope_source_search_receipts()
                    ),
                    "isotope_candidate_evidence_receipt_count": len(
                        list_isotope_candidate_evidence_receipts()
                    ),
                    "isotope_candidate_admission_receipt_count": len(
                        list_isotope_candidate_admission_receipts()
                    ),
                    "element_readiness_score_count": len(
                        list_element_readiness_scores()
                    ),
                },
            )
        if path_parts == ["elements"]:
            return ApiResponse(HTTPStatus.OK, _seed_list_payload())
        if len(path_parts) == 2 and path_parts[0] == "elements":
            element = get_seed_element(path_parts[1])
            return ApiResponse(
                HTTPStatus.OK,
                {
                    "api_status": API_STATUS,
                    "element": element.to_dict(),
                    "receipt": build_element_receipt(element),
                },
            )
        if path_parts == ["snapshot"]:
            return ApiResponse(HTTPStatus.OK, _snapshot_list_payload())
        if len(path_parts) == 2 and path_parts[0] == "snapshot":
            snapshot = get_snapshot_record(path_parts[1])
            return ApiResponse(
                HTTPStatus.OK,
                {
                    "api_status": API_STATUS,
                    "snapshot": snapshot.to_dict(),
                    "receipt": build_snapshot_receipt(snapshot),
                },
            )
        if len(path_parts) == 2 and path_parts[0] == "schemas":
            return ApiResponse(HTTPStatus.OK, _schema_payload(path_parts[1]))
        if path_parts == ["dashboard"]:
            return ApiResponse(
                HTTPStatus.OK,
                _dashboard_payload(
                    identifier=_first_query_value(query, "symbol"),
                    relation_type=_first_query_value(query, "relation"),
                ),
            )
        if len(path_parts) == 2 and path_parts[0] == "dashboard":
            return ApiResponse(
                HTTPStatus.OK,
                _dashboard_payload(
                    identifier=path_parts[1],
                    relation_type=_first_query_value(query, "relation"),
                ),
            )
        if path_parts == ["graph"]:
            return ApiResponse(
                HTTPStatus.OK,
                _graph_payload(
                    identifier=_first_query_value(query, "symbol"),
                    relation_type=_first_query_value(query, "relation"),
                ),
            )
        if len(path_parts) == 2 and path_parts[0] == "graph":
            return ApiResponse(
                HTTPStatus.OK,
                _graph_payload(
                    identifier=path_parts[1],
                    relation_type=_first_query_value(query, "relation"),
                ),
            )
        if len(path_parts) == 3 and path_parts[:2] == ["reasoning", "configuration"]:
            return ApiResponse(
                HTTPStatus.OK,
                _configuration_reasoning_payload(path_parts[2]),
            )
        if path_parts == ["reasoning", "similarity"]:
            return ApiResponse(
                HTTPStatus.OK,
                _similarity_reasoning_payload(
                    left=_first_query_value(query, "left"),
                    right=_first_query_value(query, "right"),
                ),
            )
        if len(path_parts) == 3 and path_parts[:2] == ["instances", "ion"]:
            return ApiResponse(
                HTTPStatus.OK,
                _ion_instance_payload(
                    identifier=path_parts[2],
                    charge=_required_int_query_value(query, "charge"),
                ),
            )
        if len(path_parts) == 3 and path_parts[:2] == ["instances", "isotope"]:
            return ApiResponse(
                HTTPStatus.OK,
                _isotope_instance_payload(
                    identifier=path_parts[2],
                    mass_number=_required_int_query_value(query, "mass_number"),
                ),
            )
        if path_parts == ["evidence", "isotopes"]:
            return ApiResponse(HTTPStatus.OK, _isotope_evidence_list_payload())
        if path_parts == ["evidence", "isotopes", "unresolved"]:
            return ApiResponse(HTTPStatus.OK, _unresolved_isotope_evidence_list_payload())
        if len(path_parts) == 4 and path_parts[:3] == ["evidence", "isotopes", "unresolved"]:
            return ApiResponse(
                HTTPStatus.OK,
                _unresolved_isotope_evidence_payload(path_parts[3]),
            )
        if len(path_parts) == 3 and path_parts[:2] == ["evidence", "isotopes"]:
            mass_number = _first_query_value(query, "mass_number")
            return ApiResponse(
                HTTPStatus.OK,
                _isotope_evidence_payload(
                    identifier=path_parts[2],
                    mass_number=int(mass_number) if mass_number is not None else None,
                ),
            )
        if path_parts == ["evidence", "common-ions"]:
            return ApiResponse(HTTPStatus.OK, _common_ion_evidence_list_payload())
        if path_parts == ["evidence", "common-ions", "unresolved"]:
            return ApiResponse(HTTPStatus.OK, _unresolved_common_ion_evidence_list_payload())
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "common-ions", "unresolved"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _unresolved_common_ion_evidence_payload(path_parts[3]),
            )
        if len(path_parts) == 3 and path_parts[:2] == ["evidence", "common-ions"]:
            return ApiResponse(HTTPStatus.OK, _common_ion_evidence_payload(path_parts[2]))
        if path_parts == ["evidence", "configurations"]:
            return ApiResponse(HTTPStatus.OK, _configuration_evidence_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["evidence", "configurations"]:
            return ApiResponse(HTTPStatus.OK, _configuration_evidence_payload(path_parts[2]))
        if path_parts == ["frontier", "cs-rn"]:
            return ApiResponse(HTTPStatus.OK, _frontier_valence_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["frontier", "cs-rn"]:
            return ApiResponse(HTTPStatus.OK, _frontier_valence_payload(path_parts[2]))
        if path_parts == ["evidence", "oxidation-states"]:
            return ApiResponse(HTTPStatus.OK, _oxidation_state_evidence_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["evidence", "oxidation-states"]:
            return ApiResponse(HTTPStatus.OK, _oxidation_state_evidence_payload(path_parts[2]))
        if path_parts == ["behavior", "cs-rn"]:
            return ApiResponse(HTTPStatus.OK, _behavior_tag_overlay_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["behavior", "cs-rn"]:
            return ApiResponse(HTTPStatus.OK, _behavior_tag_overlay_payload(path_parts[2]))
        if path_parts == ["relations", "cs-rn"]:
            return ApiResponse(HTTPStatus.OK, _relation_overlay_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["relations", "cs-rn"]:
            return ApiResponse(HTTPStatus.OK, _relation_overlay_payload(path_parts[2]))
        if path_parts == ["evidence", "physical-properties"]:
            return ApiResponse(HTTPStatus.OK, _physical_property_evidence_list_payload())
        if path_parts == ["evidence", "physical-properties", "unresolved"]:
            return ApiResponse(
                HTTPStatus.OK,
                _unresolved_physical_property_evidence_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "unresolved"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _unresolved_physical_property_evidence_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "gaps"]:
            return ApiResponse(HTTPStatus.OK, _physical_property_gap_list_payload())
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "gaps"]
        ):
            return ApiResponse(HTTPStatus.OK, _physical_property_gap_payload(path_parts[3]))
        if path_parts == ["evidence", "physical-properties", "workplan"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_gap_workplan_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "workplan"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_gap_workplan_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "source-search"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_source_search_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "source-search"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_source_search_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "partial-source-search"]:
            return ApiResponse(
                HTTPStatus.OK,
                _partial_physical_property_source_search_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "partial-source-search"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _partial_physical_property_source_search_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "secondary-evidence"]:
            return ApiResponse(HTTPStatus.OK, _physical_property_secondary_evidence_list_payload())
        if path_parts == [
            "evidence",
            "physical-properties",
            "secondary-evidence",
            "admission",
        ]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_secondary_evidence_admission_list_payload(),
            )
        if (
            len(path_parts) == 5
            and path_parts[:4]
            == ["evidence", "physical-properties", "secondary-evidence", "admission"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_secondary_evidence_admission_payload(path_parts[4]),
            )
        if path_parts == ["evidence", "physical-properties", "conflicts"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_conflict_resolution_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "conflicts"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_conflict_resolution_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "corroboration"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_corroboration_review_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "corroboration"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_corroboration_review_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "review"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_review_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "review"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_review_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "gap-closure"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_gap_closure_decision_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "gap-closure"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_gap_closure_decision_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "closure-approval"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_closure_approval_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "closure-approval"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_closure_approval_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "seed-update"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_seed_update_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "seed-update"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_seed_update_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "escalations"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_escalation_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "escalations"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_escalation_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "escalation-search"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_escalation_search_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == [
                "evidence",
                "physical-properties",
                "escalation-search",
            ]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_escalation_search_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "escalation-resolution"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_escalation_resolution_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3]
            == ["evidence", "physical-properties", "escalation-resolution"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_escalation_resolution_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "operator-decisions"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_operator_decision_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "operator-decisions"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_operator_decision_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "continued-evidence"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_continued_evidence_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "continued-evidence"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_continued_evidence_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "no-candidate"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_no_candidate_review_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "no-candidate"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_no_candidate_review_payload(path_parts[3]),
            )
        if (
            len(path_parts) == 5
            and path_parts[:4]
            == ["evidence", "physical-properties", "secondary-evidence", "template"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_secondary_evidence_template_payload(path_parts[4]),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["evidence", "physical-properties", "secondary-evidence"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_secondary_evidence_payload(path_parts[3]),
            )
        if path_parts == ["evidence", "physical-properties", "secondary-source-policy"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_secondary_source_policy_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3]
            == ["evidence", "physical-properties", "secondary-source-policy"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_secondary_source_policy_payload(path_parts[3]),
            )
        if len(path_parts) == 3 and path_parts[:2] == ["evidence", "physical-properties"]:
            return ApiResponse(
                HTTPStatus.OK,
                _physical_property_evidence_payload(path_parts[2]),
            )
        if path_parts == ["matter", "profiles"]:
            return ApiResponse(HTTPStatus.OK, _matter_profile_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["matter", "profiles"]:
            return ApiResponse(HTTPStatus.OK, _matter_profile_payload(path_parts[2]))
        if path_parts == ["atom", "behavior"]:
            return ApiResponse(HTTPStatus.OK, _atom_behavior_list_payload())
        if path_parts == ["atom", "behavior", "gaps"]:
            return ApiResponse(HTTPStatus.OK, _atom_behavior_gap_list_payload())
        if len(path_parts) == 4 and path_parts[:3] == ["atom", "behavior", "gaps"]:
            return ApiResponse(HTTPStatus.OK, _atom_behavior_gap_payload(path_parts[3]))
        if path_parts == ["atom", "behavior", "workplan"]:
            return ApiResponse(HTTPStatus.OK, _atom_behavior_gap_workplan_list_payload())
        if len(path_parts) == 4 and path_parts[:3] == ["atom", "behavior", "workplan"]:
            return ApiResponse(
                HTTPStatus.OK,
                _atom_behavior_gap_workplan_payload(path_parts[3]),
            )
        if path_parts == ["atom", "behavior", "isotope-source-policy"]:
            return ApiResponse(HTTPStatus.OK, _isotope_source_policy_list_payload())
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["atom", "behavior", "isotope-source-policy"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _isotope_source_policy_payload(path_parts[3]),
            )
        if path_parts == ["atom", "behavior", "isotope-source-search"]:
            return ApiResponse(HTTPStatus.OK, _isotope_source_search_list_payload())
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["atom", "behavior", "isotope-source-search"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _isotope_source_search_payload(path_parts[3]),
            )
        if path_parts == ["atom", "behavior", "isotope-candidate-evidence"]:
            return ApiResponse(HTTPStatus.OK, _isotope_candidate_evidence_list_payload())
        if (
            len(path_parts) == 5
            and path_parts[:4] == [
                "atom",
                "behavior",
                "isotope-candidate-evidence",
                "template",
            ]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _isotope_candidate_evidence_template_payload(path_parts[4]),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["atom", "behavior", "isotope-candidate-evidence"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _isotope_candidate_evidence_payload(path_parts[3]),
            )
        if path_parts == ["atom", "behavior", "isotope-candidate-admission"]:
            return ApiResponse(
                HTTPStatus.OK,
                _isotope_candidate_admission_list_payload(),
            )
        if (
            len(path_parts) == 4
            and path_parts[:3] == ["atom", "behavior", "isotope-candidate-admission"]
        ):
            return ApiResponse(
                HTTPStatus.OK,
                _isotope_candidate_admission_payload(path_parts[3]),
            )
        if path_parts == ["scoring", "readiness"]:
            return ApiResponse(HTTPStatus.OK, _readiness_score_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["scoring", "readiness"]:
            return ApiResponse(HTTPStatus.OK, _readiness_score_payload(path_parts[2]))
        if len(path_parts) == 3 and path_parts[:2] == ["atom", "behavior"]:
            return ApiResponse(
                HTTPStatus.OK,
                _atom_behavior_payload(
                    identifier=path_parts[2],
                    mass_number=_optional_int_query_value(query, "mass_number"),
                    charge=_optional_int_query_value(query, "charge", 0) or 0,
                ),
            )
        if path_parts == ["promotion", "cs-rn"]:
            return ApiResponse(HTTPStatus.OK, _cs_rn_promotion_readiness_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["promotion", "cs-rn"]:
            return ApiResponse(
                HTTPStatus.OK,
                _cs_rn_promotion_readiness_payload(path_parts[2]),
            )
        if path_parts == ["promotion", "batch-policy"]:
            return ApiResponse(HTTPStatus.OK, _promotion_batch_policy_payload())
        if path_parts == ["promotion", "partial-eligibility"]:
            return ApiResponse(HTTPStatus.OK, _partial_promotion_eligibility_payload())
        if path_parts == ["promotion", "full-span-approval-review"]:
            return ApiResponse(
                HTTPStatus.OK,
                _full_span_promotion_approval_review_payload(),
            )
        if path_parts == ["promotion", "decisions"]:
            return ApiResponse(HTTPStatus.OK, _promotion_decision_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["promotion", "decisions"]:
            return ApiResponse(HTTPStatus.OK, _promotion_decision_payload(path_parts[2]))
        if path_parts == ["phase3", "f-block"]:
            return ApiResponse(HTTPStatus.OK, _f_block_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["phase3", "f-block"]:
            return ApiResponse(HTTPStatus.OK, _f_block_profile_payload(path_parts[2]))
        if path_parts == ["level2", "period-5"]:
            return ApiResponse(HTTPStatus.OK, _period_5_level_2_list_payload())
        if len(path_parts) == 3 and path_parts[:2] == ["level2", "period-5"]:
            return ApiResponse(HTTPStatus.OK, _period_5_level_2_profile_payload(path_parts[2]))
    except KeyError as error:
        return _error_response(HTTPStatus.NOT_FOUND, "not_found", str(error))
    except ValueError as error:
        return _error_response(HTTPStatus.BAD_REQUEST, "bad_request", str(error))

    return _error_response(
        HTTPStatus.NOT_FOUND,
        "route_not_found",
        f"Unknown API route: {parsed_target.path}",
    )


class MCMSApiHandler(BaseHTTPRequestHandler):
    server_version = "MCMSLocalAPI/0.1"

    def do_GET(self) -> None:
        response = handle_api_request("GET", self.path)
        self._send_json_response(response, include_body=True)

    def do_HEAD(self) -> None:
        response = handle_api_request("GET", self.path)
        self._send_json_response(response, include_body=False)

    def do_POST(self) -> None:
        response = handle_api_request("POST", self.path)
        self._send_json_response(response, include_body=True)

    def _send_json_response(self, response: ApiResponse, *, include_body: bool) -> None:
        body = response.to_json_bytes()
        self.send_response(response.status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body) if include_body else 0))
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def build_api_server(host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), MCMSApiHandler)


def serve_api(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = build_api_server(host=host, port=port)
    print(f"MCMS local API listening on http://{host}:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m mcms.api")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    serve_api(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
