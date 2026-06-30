"""Purpose: define secondary-source admission policy for physical-property gaps.

Project scope: records how incomplete PubChem physical-property rows may be
closed by a governed secondary source without silently importing substitute
values.
Dependencies: physical-property gap audit receipts.
Invariants: policy approval is separate from evidence import; no gap closes until
source provenance, units, condition, and conflict handling are explicit.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_gap import (
    get_physical_property_gap_audit_receipt,
    list_physical_property_gap_audit_receipts,
)

VALID_SECONDARY_SOURCE_CANDIDATE_STATUSES = {
    "candidate_requires_review",
    "not_applicable_for_current_gap",
}
VALID_SECONDARY_SOURCE_POLICY_STATUSES = {"secondary_source_policy_defined"}
VALID_GAP_CLOSURE_STATUSES = {"gap_not_closed_by_policy"}


@dataclass(frozen=True)
class PhysicalPropertySecondarySourceCandidate:
    source_key: str
    authority: str
    title: str
    admission_status: str
    allowed_fields: tuple[str, ...]
    required_evidence: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.source_key:
            errors.append("secondary source candidate key is required.")
        if not self.authority:
            errors.append("secondary source candidate authority is required.")
        if not self.title:
            errors.append("secondary source candidate title is required.")
        if self.admission_status not in VALID_SECONDARY_SOURCE_CANDIDATE_STATUSES:
            errors.append("secondary source candidate admission status is unknown.")
        if not self.allowed_fields:
            errors.append("secondary source candidate requires at least one allowed field.")
        if "source_url_or_citation" not in self.required_evidence:
            errors.append("secondary source candidate requires source citation evidence.")
        if "unit_normalization_to_kelvin_or_g_per_cm3" not in self.required_evidence:
            errors.append("secondary source candidate requires unit-normalization evidence.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["allowed_fields"] = list(self.allowed_fields)
        payload["required_evidence"] = list(self.required_evidence)
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class PhysicalPropertySecondarySourcePolicy:
    policy_id: str
    policy_status: str
    target_gap_receipt_id: str
    symbol: str
    atomic_number: int
    missing_fields: tuple[str, ...]
    candidate_sources: tuple[PhysicalPropertySecondarySourceCandidate, ...]
    admission_requirements: tuple[str, ...]
    conflict_resolution_order: tuple[str, ...]
    gap_closure_status: str
    seed_mutation_allowed: bool
    required_next_action: str
    notes: tuple[str, ...] = (
        "This policy authorizes review of secondary sources; it does not import values.",
        "A physical-property gap remains open until a source-specific evidence record is added.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.policy_id:
            errors.append("secondary-source policy id is required.")
        if self.policy_status not in VALID_SECONDARY_SOURCE_POLICY_STATUSES:
            errors.append("secondary-source policy status is unknown.")
        if self.gap_closure_status not in VALID_GAP_CLOSURE_STATUSES:
            errors.append("gap closure status is unknown.")
        if self.seed_mutation_allowed:
            errors.append("secondary-source policy alone must not allow seed mutation.")
        if not self.missing_fields:
            errors.append("secondary-source policy requires missing fields.")
        if not self.candidate_sources:
            errors.append("secondary-source policy requires candidate sources.")
        if "field_specific_source_receipt" not in self.admission_requirements:
            errors.append("policy requires a field-specific source receipt before closure.")
        if "primary_source_precedence" not in self.conflict_resolution_order:
            errors.append("policy requires primary-source precedence.")
        for candidate in self.candidate_sources:
            errors.extend(candidate.validate())
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["missing_fields"] = list(self.missing_fields)
        payload["candidate_sources"] = [
            candidate.to_dict() for candidate in self.candidate_sources
        ]
        payload["admission_requirements"] = list(self.admission_requirements)
        payload["conflict_resolution_order"] = list(self.conflict_resolution_order)
        payload["notes"] = list(self.notes)
        return payload


_COMMON_REQUIRED_EVIDENCE = (
    "source_url_or_citation",
    "field_name_mapping",
    "unit_normalization_to_kelvin_or_g_per_cm3",
    "value_type_measured_estimated_or_predicted",
    "retrieval_date",
    "license_or_usage_boundary",
)

_CANDIDATE_SOURCES = (
    PhysicalPropertySecondarySourceCandidate(
        source_key="lanl_periodic_table_candidate",
        authority="Los Alamos National Laboratory",
        title="LANL Periodic Table of Elements",
        admission_status="candidate_requires_review",
        allowed_fields=("boiling_point_k",),
        required_evidence=_COMMON_REQUIRED_EVIDENCE,
        notes=(
            "Candidate source is useful when PubChem CSV is blank but must be "
            "reviewed for estimated-value status and conflicts.",
        ),
    ),
    PhysicalPropertySecondarySourceCandidate(
        source_key="nist_chemistry_webbook_candidate",
        authority="NIST",
        title="NIST Chemistry WebBook",
        admission_status="candidate_requires_review",
        allowed_fields=("boiling_point_k",),
        required_evidence=_COMMON_REQUIRED_EVIDENCE,
        notes=(
            "Candidate source must provide an element-specific row for the requested field.",
        ),
    ),
    PhysicalPropertySecondarySourceCandidate(
        source_key="crc_handbook_candidate",
        authority="CRC Press",
        title="CRC Handbook of Chemistry and Physics",
        admission_status="candidate_requires_review",
        allowed_fields=("boiling_point_k", "melting_point_k", "density_value"),
        required_evidence=_COMMON_REQUIRED_EVIDENCE,
        notes=("Candidate source requires edition/version citation.",),
    ),
    PhysicalPropertySecondarySourceCandidate(
        source_key="rsc_periodic_table_candidate",
        authority="Royal Society of Chemistry",
        title="RSC Periodic Table",
        admission_status="candidate_requires_review",
        allowed_fields=("boiling_point_k", "melting_point_k", "density_value"),
        required_evidence=_COMMON_REQUIRED_EVIDENCE,
        notes=("Candidate source remains secondary to PubChem for this project.",),
    ),
    PhysicalPropertySecondarySourceCandidate(
        source_key="web_elements_candidate",
        authority="WebElements",
        title="WebElements Periodic Table",
        admission_status="candidate_requires_review",
        allowed_fields=("boiling_point_k", "melting_point_k", "density_value"),
        required_evidence=_COMMON_REQUIRED_EVIDENCE,
        notes=("Candidate source remains secondary to PubChem for this project.",),
    ),
)


def _build_secondary_source_policy(identifier: str | int) -> PhysicalPropertySecondarySourcePolicy:
    gap_receipt = get_physical_property_gap_audit_receipt(identifier)
    return PhysicalPropertySecondarySourcePolicy(
        policy_id=(
            f"MSPEE-PHYSICAL-PROPERTY-SECONDARY-SOURCE-POLICY-"
            f"Z{gap_receipt.atomic_number:03d}-{gap_receipt.symbol}"
        ),
        policy_status="secondary_source_policy_defined",
        target_gap_receipt_id=gap_receipt.receipt_id,
        symbol=gap_receipt.symbol,
        atomic_number=gap_receipt.atomic_number,
        missing_fields=gap_receipt.missing_fields,
        candidate_sources=_CANDIDATE_SOURCES,
        admission_requirements=(
            "field_specific_source_receipt",
            "source_authority_and_version",
            "source_url_or_citation",
            "retrieval_date",
            "unit_normalization_to_kelvin_or_g_per_cm3",
            "value_type_measured_estimated_or_predicted",
            "conflict_receipt_if_primary_source_disagrees",
            "operator_approval_before_seed_mutation",
        ),
        conflict_resolution_order=(
            "primary_source_precedence",
            "field_specific_secondary_source_if_primary_blank",
            "conflict_receipt_required_for_disagreement",
            "unresolved_status_if_no_admissible_source",
        ),
        gap_closure_status="gap_not_closed_by_policy",
        seed_mutation_allowed=False,
        required_next_action=(
            "collect a field-specific secondary-source receipt for the missing physical "
            "property and validate it against this policy"
        ),
    )


def list_physical_property_secondary_source_policies() -> tuple[
    PhysicalPropertySecondarySourcePolicy, ...
]:
    return tuple(
        _build_secondary_source_policy(receipt.receipt_id)
        for receipt in list_physical_property_gap_audit_receipts()
    )


def get_physical_property_secondary_source_policy(
    identifier: str | int,
) -> PhysicalPropertySecondarySourcePolicy:
    identifier_text = str(identifier).strip()
    for policy in list_physical_property_secondary_source_policies():
        if (
            identifier_text == str(policy.atomic_number)
            or identifier_text.upper() == policy.symbol.upper()
            or identifier_text == policy.target_gap_receipt_id
            or identifier_text == policy.policy_id
        ):
            return policy
    raise KeyError(f"unknown physical-property secondary-source policy: {identifier_text}")


def validate_physical_property_secondary_source_policies(
    policies: tuple[PhysicalPropertySecondarySourcePolicy, ...] | None = None,
) -> dict[str, Any]:
    checked_policies = (
        policies if policies is not None else list_physical_property_secondary_source_policies()
    )
    invalid_policies = tuple(policy.policy_id for policy in checked_policies if policy.validate())
    validation_status = "physical_property_secondary_source_policies_validated"
    if invalid_policies:
        validation_status = "physical_property_secondary_source_policies_rejected"
    return {
        "validation_status": validation_status,
        "policy_count": len(checked_policies),
        "gap_closure_count": sum(
            1
            for policy in checked_policies
            if policy.gap_closure_status != "gap_not_closed_by_policy"
        ),
        "seed_mutation_allowed_count": sum(
            1 for policy in checked_policies if policy.seed_mutation_allowed
        ),
        "candidate_source_count": len(_CANDIDATE_SOURCES),
        "invalid_policies": invalid_policies,
    }
