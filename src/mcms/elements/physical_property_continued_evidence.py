"""Purpose: plan continued evidence work for deferred operator decisions.

Project scope: converts deferred physical-property operator decisions into
bounded next-action plans.
Dependencies: physical-property operator-decision receipts.
Invariants: continued-evidence plans do not approve, reject, close gaps, or
mutate seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_operator_decision import (
    get_physical_property_operator_decision_receipt,
    list_physical_property_operator_decision_receipts,
)

VALID_CONTINUED_EVIDENCE_PLAN_STATUSES = {
    "continued_evidence_required",
}

VALID_CONTINUED_EVIDENCE_PLAN_CLASSES = {
    "higher_precedence_source_discovery",
    "independent_corroboration_discovery",
}


@dataclass(frozen=True)
class PhysicalPropertyContinuedEvidencePlan:
    plan_id: str
    target_operator_decision_receipt_id: str
    symbol: str
    atomic_number: int
    field_name: str
    plan_status: str
    plan_class: str
    search_objective: str
    required_source_qualities: tuple[str, ...]
    blocked_until: str
    final_resolution_applied: bool
    closes_gap: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "physical_property_continued_evidence_plan"
    notes: tuple[str, ...] = (
        "Continued-evidence plans are work plans, not final evidence decisions.",
        "Plans preserve unresolved status until a later source or operator receipt resolves it.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        decision = get_physical_property_operator_decision_receipt(
            self.target_operator_decision_receipt_id
        )
        if self.symbol != decision.symbol:
            errors.append("continued-evidence plan symbol must match operator decision.")
        if self.atomic_number != decision.atomic_number:
            errors.append(
                "continued-evidence plan atomic number must match operator decision."
            )
        if self.field_name != decision.field_name:
            errors.append("continued-evidence plan field must match operator decision.")
        if decision.operator_decision_status != "operator_decision_deferred":
            errors.append("continued-evidence plan requires deferred operator decision.")
        if self.plan_status not in VALID_CONTINUED_EVIDENCE_PLAN_STATUSES:
            errors.append("continued-evidence plan status is unknown.")
        if self.plan_class not in VALID_CONTINUED_EVIDENCE_PLAN_CLASSES:
            errors.append("continued-evidence plan class is unknown.")
        if not self.search_objective:
            errors.append("continued-evidence plan requires search objective.")
        if not self.required_source_qualities:
            errors.append("continued-evidence plan requires source qualities.")
        if not self.blocked_until:
            errors.append("continued-evidence plan requires blocked-until condition.")
        if self.final_resolution_applied:
            errors.append("continued-evidence plan must not apply final resolution.")
        if self.closes_gap:
            errors.append("continued-evidence plan must not close gap.")
        if self.seed_mutation_allowed:
            errors.append("continued-evidence plan must not allow seed mutation.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["required_source_qualities"] = list(self.required_source_qualities)
        payload["notes"] = list(self.notes)
        return payload


def _plan_class_for_field(symbol: str, field_name: str) -> str:
    if symbol in {"At", "Fr", "Pa"} and field_name == "boiling_point_k":
        return "higher_precedence_source_discovery"
    return "independent_corroboration_discovery"


def _build_continued_evidence_plan(
    operator_decision_receipt_id: str,
) -> PhysicalPropertyContinuedEvidencePlan:
    decision = get_physical_property_operator_decision_receipt(operator_decision_receipt_id)
    plan_class = _plan_class_for_field(decision.symbol, decision.field_name)
    if plan_class == "higher_precedence_source_discovery":
        search_objective = (
            "find a higher-precedence field-specific source that can resolve the "
            f"{decision.symbol} {decision.field_name} conflict"
        )
        required_source_qualities = (
            "field-specific physical-property source",
            "higher precedence than conflicting secondary references",
            "explicit value, unit, and value-type classification",
            "citation or stable source URL",
        )
        blocked_until = "higher-precedence evidence or explicit operator conflict resolution"
    else:
        search_objective = (
            "find an independent corroborating field-specific source for the "
            f"{decision.symbol} {decision.field_name} candidate"
        )
        required_source_qualities = (
            "independent from the candidate source cluster",
            "field-specific physical-property source",
            "explicit value, unit, and value-type classification",
            "citation or stable source URL",
        )
        blocked_until = "independent corroboration or explicit operator rejection"
    return PhysicalPropertyContinuedEvidencePlan(
        plan_id=decision.receipt_id.replace(
            "OPERATOR-DECISION",
            "CONTINUED-EVIDENCE",
        ),
        target_operator_decision_receipt_id=decision.receipt_id,
        symbol=decision.symbol,
        atomic_number=decision.atomic_number,
        field_name=decision.field_name,
        plan_status="continued_evidence_required",
        plan_class=plan_class,
        search_objective=search_objective,
        required_source_qualities=required_source_qualities,
        blocked_until=blocked_until,
        final_resolution_applied=False,
    )


def list_physical_property_continued_evidence_plans() -> tuple[
    PhysicalPropertyContinuedEvidencePlan, ...
]:
    return tuple(
        _build_continued_evidence_plan(receipt.receipt_id)
        for receipt in list_physical_property_operator_decision_receipts()
    )


def get_physical_property_continued_evidence_plan(
    identifier: str | int,
) -> PhysicalPropertyContinuedEvidencePlan:
    identifier_text = str(identifier).strip()
    for plan in list_physical_property_continued_evidence_plans():
        if (
            identifier_text == str(plan.atomic_number)
            or identifier_text.upper() == plan.symbol.upper()
            or identifier_text == plan.plan_id
            or identifier_text == plan.target_operator_decision_receipt_id
        ):
            return plan
    raise KeyError(f"unknown physical-property continued-evidence plan: {identifier_text}")


def validate_physical_property_continued_evidence_plans(
    plans: tuple[PhysicalPropertyContinuedEvidencePlan, ...] | None = None,
) -> dict[str, Any]:
    checked_plans = (
        plans if plans is not None else list_physical_property_continued_evidence_plans()
    )
    invalid_plans = tuple(plan.plan_id for plan in checked_plans if plan.validate())
    validation_status = "physical_property_continued_evidence_plans_validated"
    if invalid_plans:
        validation_status = "physical_property_continued_evidence_plans_rejected"
    return {
        "validation_status": validation_status,
        "plan_count": len(checked_plans),
        "continued_evidence_required_count": sum(
            1 for plan in checked_plans if plan.plan_status == "continued_evidence_required"
        ),
        "higher_precedence_source_discovery_count": sum(
            1
            for plan in checked_plans
            if plan.plan_class == "higher_precedence_source_discovery"
        ),
        "independent_corroboration_discovery_count": sum(
            1
            for plan in checked_plans
            if plan.plan_class == "independent_corroboration_discovery"
        ),
        "final_resolution_applied_count": sum(
            1 for plan in checked_plans if plan.final_resolution_applied
        ),
        "gap_closure_count": sum(1 for plan in checked_plans if plan.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for plan in checked_plans if plan.seed_mutation_allowed
        ),
        "invalid_plans": invalid_plans,
    }
