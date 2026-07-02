"""Purpose: Cs-Rn promotion decision receipts.

Project scope: records governance decisions over Cs-Rn promotion-readiness profiles
without mutating seed records.
Dependencies: promotion readiness profiles.
Invariants: readiness is not approval; blocked evidence remains explicit.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.promotion import (
    CS_RN_PROMOTION_SYMBOLS,
    get_cs_rn_promotion_readiness_profile,
)

VALID_PROMOTION_DECISION_STATUSES = {
    "promotion_ready_pending_approval",
    "promotion_blocked_unresolved_physical_property",
    "promotion_deferred_by_policy",
    "promotion_approved_for_seed",
}

VALID_PROMOTION_BATCH_POLICY_STATUSES = {
    "span_hold_pending_blocker_resolution",
    "span_ready_for_approval",
}
VALID_PARTIAL_PROMOTION_ELIGIBILITY_STATUSES = {
    "partial_review_available_seed_mutation_blocked",
    "partial_review_unavailable",
}
VALID_FULL_SPAN_APPROVAL_REVIEW_STATUSES = {
    "full_span_approval_review_open",
    "full_span_approval_review_blocked",
}
VALID_FULL_SPAN_APPROVAL_DECISIONS = {
    "full_span_promotion_approved",
    "full_span_promotion_rejected",
    "full_span_promotion_blocked",
}
VALID_FULL_SPAN_EXECUTION_PACKET_STATUSES = {
    "execution_packet_ready_not_applied",
    "execution_packet_blocked",
}


@dataclass(frozen=True)
class PromotionDecisionReceipt:
    receipt_id: str
    element_id: str
    symbol: str
    atomic_number: int
    target_level: str
    readiness_status: str
    decision_status: str
    decision_reason: str
    unresolved_blockers: tuple[str, ...]
    available_evidence: tuple[str, ...]
    approval_required: bool = True
    evidence_status: str = "promotion_decision_receipt"
    notes: tuple[str, ...] = (
        "Promotion decision receipts do not mutate Level 1 seed records.",
        "Ready records still require explicit approval before seed promotion.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.symbol not in CS_RN_PROMOTION_SYMBOLS:
            errors.append("promotion decision symbol must be in the Cs-Rn span.")
        if self.decision_status not in VALID_PROMOTION_DECISION_STATUSES:
            errors.append("promotion decision status is unknown.")
        if not self.receipt_id:
            errors.append("promotion decision receipt id is required.")
        if not self.decision_reason:
            errors.append("promotion decision reason is required.")
        if (
            self.decision_status == "promotion_ready_pending_approval"
            and self.unresolved_blockers
        ):
            errors.append("ready-pending-approval decision must not have unresolved blockers.")
        if (
            self.decision_status == "promotion_blocked_unresolved_physical_property"
            and "missing:complete_physical_property_evidence" not in self.unresolved_blockers
        ):
            errors.append("physical-property block decision requires the physical-property blocker.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["unresolved_blockers"] = list(self.unresolved_blockers)
        payload["available_evidence"] = list(self.available_evidence)
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class PromotionBatchPolicyReceipt:
    receipt_id: str
    span_id: str
    span_symbols: tuple[str, ...]
    target_level: str
    policy_status: str
    policy_decision: str
    policy_reason: str
    ready_symbols: tuple[str, ...]
    blocked_symbols: tuple[str, ...]
    blocking_receipt_ids: tuple[str, ...]
    seed_mutation_allowed: bool
    invariants_preserved: tuple[str, ...]
    evidence_status: str = "promotion_batch_policy_receipt"
    notes: tuple[str, ...] = (
        "Batch policy receipts do not mutate Level 1 seed records.",
        "The current seed pack remains contiguous through Xe.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.span_symbols != CS_RN_PROMOTION_SYMBOLS:
            errors.append("batch policy span must cover Cs through Rn in order.")
        if self.policy_status not in VALID_PROMOTION_BATCH_POLICY_STATUSES:
            errors.append("batch policy status is unknown.")
        if not self.policy_decision:
            errors.append("batch policy decision is required.")
        if not self.policy_reason:
            errors.append("batch policy reason is required.")
        if self.seed_mutation_allowed:
            errors.append("batch policy readiness must not directly allow seed mutation.")
        if self.policy_status == "span_hold_pending_blocker_resolution":
            if self.seed_mutation_allowed:
                errors.append("span hold policy must not allow seed mutation.")
            if "At" not in self.blocked_symbols:
                errors.append("current span hold must identify At as the blocker.")
        if self.policy_status == "span_ready_for_approval":
            if self.blocked_symbols:
                errors.append("ready-for-approval span must not contain blockers.")
            if self.policy_decision != "allow_full_span_approval_review":
                errors.append("ready span must route to full-span approval review.")
        if len(self.ready_symbols) + len(self.blocked_symbols) != len(self.span_symbols):
            errors.append("ready and blocked symbol counts must cover the span.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["span_symbols"] = list(self.span_symbols)
        payload["ready_symbols"] = list(self.ready_symbols)
        payload["blocked_symbols"] = list(self.blocked_symbols)
        payload["blocking_receipt_ids"] = list(self.blocking_receipt_ids)
        payload["invariants_preserved"] = list(self.invariants_preserved)
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class PartialPromotionEligibilityReceipt:
    receipt_id: str
    span_id: str
    target_level: str
    eligibility_status: str
    eligible_symbols: tuple[str, ...]
    blocked_symbols: tuple[str, ...]
    eligible_decision_receipt_ids: tuple[str, ...]
    blocking_receipt_ids: tuple[str, ...]
    batch_policy_receipt_id: str
    batch_policy_decision: str
    partial_review_allowed: bool
    seed_mutation_allowed: bool
    required_next_action: str
    invariants_preserved: tuple[str, ...]
    evidence_status: str = "partial_promotion_eligibility_receipt"
    notes: tuple[str, ...] = (
        "Partial eligibility is a review queue, not a seed-promotion action.",
        "Seed mutation remains blocked while full-span policy is held.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.eligibility_status not in VALID_PARTIAL_PROMOTION_ELIGIBILITY_STATUSES:
            errors.append("partial promotion eligibility status is unknown.")
        observed_symbols = set(self.eligible_symbols) | set(self.blocked_symbols)
        if observed_symbols != set(CS_RN_PROMOTION_SYMBOLS):
            errors.append("eligible and blocked symbols must cover Cs-Rn.")
        if set(self.eligible_symbols) & set(self.blocked_symbols):
            errors.append("eligible and blocked symbols must not overlap.")
        if len(self.eligible_symbols) != len(self.eligible_decision_receipt_ids):
            errors.append("eligible symbols must map to eligible decision receipt ids.")
        if len(self.blocked_symbols) != len(self.blocking_receipt_ids):
            errors.append("blocked symbols must map to blocking receipt ids.")
        if self.partial_review_allowed and not self.eligible_symbols:
            errors.append("partial review cannot be allowed without eligible symbols.")
        if self.seed_mutation_allowed:
            errors.append("partial eligibility must not allow seed mutation.")
        if self.batch_policy_decision == "hold_full_cs_rn_span" and not self.blocked_symbols:
            errors.append("full-span hold requires at least one blocked symbol.")
        if "readiness_is_not_approval" not in self.invariants_preserved:
            errors.append("partial eligibility must preserve readiness-is-not-approval.")
        if "no_partial_seed_hole" not in self.invariants_preserved:
            errors.append("partial eligibility must preserve no partial seed holes.")
        if not self.required_next_action:
            errors.append("partial eligibility requires a next action.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["eligible_symbols"] = list(self.eligible_symbols)
        payload["blocked_symbols"] = list(self.blocked_symbols)
        payload["eligible_decision_receipt_ids"] = list(self.eligible_decision_receipt_ids)
        payload["blocking_receipt_ids"] = list(self.blocking_receipt_ids)
        payload["invariants_preserved"] = list(self.invariants_preserved)
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class FullSpanPromotionApprovalReviewReceipt:
    receipt_id: str
    span_id: str
    target_level: str
    review_status: str
    batch_policy_receipt_id: str
    batch_policy_decision: str
    ready_symbols: tuple[str, ...]
    blocked_symbols: tuple[str, ...]
    ready_decision_receipt_ids: tuple[str, ...]
    blocking_receipt_ids: tuple[str, ...]
    approval_review_allowed: bool
    seed_mutation_allowed: bool
    required_next_action: str
    invariants_preserved: tuple[str, ...]
    evidence_status: str = "full_span_promotion_approval_review_receipt"
    notes: tuple[str, ...] = (
        "Full-span approval review is not seed mutation.",
        "Seed mutation remains blocked until a later explicit approval receipt exists.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.review_status not in VALID_FULL_SPAN_APPROVAL_REVIEW_STATUSES:
            errors.append("full-span approval review status is unknown.")
        if self.batch_policy_decision == "allow_full_span_approval_review":
            if self.review_status != "full_span_approval_review_open":
                errors.append("allowed full-span policy requires open approval review.")
            if not self.approval_review_allowed:
                errors.append("allowed full-span policy must allow approval review.")
            if self.blocked_symbols:
                errors.append("open full-span approval review must not contain blockers.")
        else:
            if self.review_status != "full_span_approval_review_blocked":
                errors.append("blocked batch policy requires blocked approval review.")
            if self.approval_review_allowed:
                errors.append("blocked full-span policy must not allow approval review.")
        if self.ready_symbols != CS_RN_PROMOTION_SYMBOLS and not self.blocked_symbols:
            errors.append("unblocked full-span review must cover Cs through Rn.")
        if len(self.ready_symbols) != len(self.ready_decision_receipt_ids):
            errors.append("ready symbols must map to ready decision receipt ids.")
        if len(self.blocked_symbols) != len(self.blocking_receipt_ids):
            errors.append("blocked symbols must map to blocking receipt ids.")
        if self.seed_mutation_allowed:
            errors.append("approval review receipt must not allow seed mutation.")
        if "readiness_is_not_approval" not in self.invariants_preserved:
            errors.append("approval review must preserve readiness-is-not-approval.")
        if "approval_review_is_not_seed_mutation" not in self.invariants_preserved:
            errors.append("approval review must preserve review-is-not-mutation.")
        if not self.required_next_action:
            errors.append("full-span approval review requires a next action.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["ready_symbols"] = list(self.ready_symbols)
        payload["blocked_symbols"] = list(self.blocked_symbols)
        payload["ready_decision_receipt_ids"] = list(self.ready_decision_receipt_ids)
        payload["blocking_receipt_ids"] = list(self.blocking_receipt_ids)
        payload["invariants_preserved"] = list(self.invariants_preserved)
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class FullSpanPromotionApprovalDecisionReceipt:
    receipt_id: str
    span_id: str
    target_level: str
    approval_decision: str
    approval_review_receipt_id: str
    approval_review_status: str
    approval_review_allowed: bool
    approved_symbols: tuple[str, ...]
    rejected_symbols: tuple[str, ...]
    blocking_receipt_ids: tuple[str, ...]
    decision_reason: str
    seed_mutation_authorized: bool
    seed_mutation_applied: bool
    required_next_action: str
    invariants_preserved: tuple[str, ...]
    evidence_status: str = "full_span_promotion_approval_decision_receipt"
    notes: tuple[str, ...] = (
        "Approval decision receipts authorize the governed execution packet.",
        "Approval is recorded separately from seed mutation application.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.approval_decision not in VALID_FULL_SPAN_APPROVAL_DECISIONS:
            errors.append("full-span approval decision status is unknown.")
        if self.approval_review_status != "full_span_approval_review_open":
            errors.append("approval decision requires an open approval-review receipt.")
        if not self.approval_review_allowed:
            errors.append("approval decision requires approval review to be allowed.")
        if self.approval_decision == "full_span_promotion_approved":
            if self.approved_symbols != CS_RN_PROMOTION_SYMBOLS:
                errors.append("approved full-span decision must approve all Cs-Rn symbols.")
            if self.rejected_symbols:
                errors.append("approved full-span decision must not reject symbols.")
            if self.blocking_receipt_ids:
                errors.append("approved full-span decision must not keep blockers.")
            if not self.seed_mutation_authorized:
                errors.append("approved full-span decision must authorize execution packet.")
        if self.approval_decision == "full_span_promotion_rejected":
            if self.approved_symbols:
                errors.append("rejected full-span decision must not approve symbols.")
            if not self.rejected_symbols:
                errors.append("rejected full-span decision must identify rejected symbols.")
            if self.seed_mutation_authorized:
                errors.append("rejected full-span decision must not authorize seed mutation.")
        if self.approval_decision == "full_span_promotion_blocked":
            if self.seed_mutation_authorized:
                errors.append("blocked full-span decision must not authorize seed mutation.")
            if not self.blocking_receipt_ids:
                errors.append("blocked full-span decision requires blocking receipt ids.")
        if self.seed_mutation_applied:
            errors.append("approval decision receipt must not apply seed mutation.")
        if "approval_decision_is_final_seed_gate" not in self.invariants_preserved:
            errors.append("approval decision must preserve final-gate invariant.")
        if "approval_is_not_seed_mutation_application" not in self.invariants_preserved:
            errors.append("approval decision must preserve approval-is-not-application.")
        if not self.decision_reason:
            errors.append("approval decision requires a reason.")
        if not self.required_next_action:
            errors.append("approval decision requires a next action.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["approved_symbols"] = list(self.approved_symbols)
        payload["rejected_symbols"] = list(self.rejected_symbols)
        payload["blocking_receipt_ids"] = list(self.blocking_receipt_ids)
        payload["invariants_preserved"] = list(self.invariants_preserved)
        payload["notes"] = list(self.notes)
        return payload


@dataclass(frozen=True)
class FullSpanPromotionExecutionPacket:
    receipt_id: str
    span_id: str
    target_level: str
    execution_status: str
    approval_decision_receipt_id: str
    approval_decision: str
    promotion_symbols: tuple[str, ...]
    planned_seed_append_symbols: tuple[str, ...]
    planned_operation: str
    current_seed_terminal_symbol: str
    target_seed_terminal_symbol: str
    planned_mutation_count: int
    seed_mutation_authorized: bool
    seed_mutation_applied: bool
    rollback_strategy: str
    required_next_action: str
    invariants_preserved: tuple[str, ...]
    evidence_status: str = "full_span_promotion_execution_packet"
    notes: tuple[str, ...] = (
        "Execution packets bind approval to a deterministic seed-promotion plan.",
        "This packet does not apply the seed mutation.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.execution_status not in VALID_FULL_SPAN_EXECUTION_PACKET_STATUSES:
            errors.append("full-span execution packet status is unknown.")
        if self.approval_decision != "full_span_promotion_approved":
            errors.append("execution packet requires approved full-span decision.")
        if self.promotion_symbols != CS_RN_PROMOTION_SYMBOLS:
            errors.append("execution packet must cover Cs through Rn in order.")
        if self.planned_seed_append_symbols != CS_RN_PROMOTION_SYMBOLS:
            errors.append("planned seed append symbols must cover Cs through Rn in order.")
        if self.planned_mutation_count != len(CS_RN_PROMOTION_SYMBOLS):
            errors.append("planned mutation count must equal the Cs-Rn span length.")
        if self.current_seed_terminal_symbol != "Xe":
            errors.append("execution packet must start from the current Xe seed boundary.")
        if self.target_seed_terminal_symbol != "Rn":
            errors.append("execution packet must target Rn as the terminal seed symbol.")
        if self.planned_operation != "append_level_1_seed_records_cs_through_rn":
            errors.append("execution packet operation is not canonical.")
        if not self.seed_mutation_authorized:
            errors.append("execution packet requires seed mutation authorization.")
        if self.seed_mutation_applied:
            errors.append("execution packet must not apply seed mutation.")
        if not self.rollback_strategy:
            errors.append("execution packet requires rollback strategy.")
        if "execution_packet_is_not_seed_mutation_application" not in self.invariants_preserved:
            errors.append("execution packet must preserve non-application invariant.")
        if "contiguous_level_1_seed_span" not in self.invariants_preserved:
            errors.append("execution packet must preserve contiguous seed span invariant.")
        if not self.required_next_action:
            errors.append("execution packet requires a next action.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["promotion_symbols"] = list(self.promotion_symbols)
        payload["planned_seed_append_symbols"] = list(self.planned_seed_append_symbols)
        payload["invariants_preserved"] = list(self.invariants_preserved)
        payload["notes"] = list(self.notes)
        return payload


def _decision_from_readiness(identifier: str | int) -> PromotionDecisionReceipt:
    profile = get_cs_rn_promotion_readiness_profile(identifier)
    if profile.readiness_status == "promotion_ready":
        decision_status = "promotion_ready_pending_approval"
        decision_reason = "all current promotion evidence blockers are closed; seed mutation awaits approval"
    elif "missing:complete_physical_property_evidence" in profile.promotion_blockers:
        decision_status = "promotion_blocked_unresolved_physical_property"
        decision_reason = "physical-property evidence is unresolved and must not be guessed"
    else:
        decision_status = "promotion_deferred_by_policy"
        decision_reason = "promotion is deferred until unresolved readiness blockers are closed"
    return PromotionDecisionReceipt(
        receipt_id=f"MSPEE-PROMOTION-DECISION-Z{profile.atomic_number:03d}-{profile.symbol}",
        element_id=profile.element_id,
        symbol=profile.symbol,
        atomic_number=profile.atomic_number,
        target_level=profile.target_level,
        readiness_status=profile.readiness_status,
        decision_status=decision_status,
        decision_reason=decision_reason,
        unresolved_blockers=profile.promotion_blockers,
        available_evidence=profile.available_evidence,
    )


def list_promotion_decision_receipts() -> tuple[PromotionDecisionReceipt, ...]:
    return tuple(_decision_from_readiness(symbol) for symbol in CS_RN_PROMOTION_SYMBOLS)


def get_promotion_decision_receipt(identifier: str | int) -> PromotionDecisionReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_promotion_decision_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.element_id
            or identifier_text == receipt.receipt_id
        ):
            return receipt
    raise KeyError(f"unknown promotion decision receipt: {identifier_text}")


def validate_promotion_decision_receipts(
    receipts: tuple[PromotionDecisionReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = receipts if receipts is not None else list_promotion_decision_receipts()
    invalid_receipts = tuple(receipt.receipt_id for receipt in checked_receipts if receipt.validate())
    observed_symbols = tuple(receipt.symbol for receipt in checked_receipts)
    full_span_expected = receipts is None or len(checked_receipts) == len(CS_RN_PROMOTION_SYMBOLS)
    validation_status = "promotion_decision_receipts_validated"
    if invalid_receipts or (full_span_expected and observed_symbols != CS_RN_PROMOTION_SYMBOLS):
        validation_status = "promotion_decision_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "ready_pending_approval_count": sum(
            1
            for receipt in checked_receipts
            if receipt.decision_status == "promotion_ready_pending_approval"
        ),
        "blocked_unresolved_physical_property_count": sum(
            1
            for receipt in checked_receipts
            if receipt.decision_status == "promotion_blocked_unresolved_physical_property"
        ),
        "approved_for_seed_count": sum(
            1
            for receipt in checked_receipts
            if receipt.decision_status == "promotion_approved_for_seed"
        ),
        "invalid_receipts": invalid_receipts,
    }


def get_promotion_batch_policy_receipt() -> PromotionBatchPolicyReceipt:
    receipts = list_promotion_decision_receipts()
    ready_receipts = tuple(
        receipt
        for receipt in receipts
        if receipt.decision_status == "promotion_ready_pending_approval"
    )
    blocked_receipts = tuple(
        receipt
        for receipt in receipts
        if receipt.decision_status != "promotion_ready_pending_approval"
    )
    if blocked_receipts:
        policy_status = "span_hold_pending_blocker_resolution"
        policy_decision = "hold_full_cs_rn_span"
        policy_reason = (
            "Level 1 seed records are kept contiguous; partial promotion would "
            "create a seed-pack gap while At remains blocked."
        )
        seed_mutation_allowed = False
    else:
        policy_status = "span_ready_for_approval"
        policy_decision = "allow_full_span_approval_review"
        policy_reason = "all Cs-Rn promotion decision receipts are ready pending approval"
        seed_mutation_allowed = False
    return PromotionBatchPolicyReceipt(
        receipt_id="MSPEE-PROMOTION-BATCH-POLICY-CS-RN",
        span_id="MSPEE-Z055-Z086-Cs-Rn",
        span_symbols=CS_RN_PROMOTION_SYMBOLS,
        target_level="level_1_seed_promotion",
        policy_status=policy_status,
        policy_decision=policy_decision,
        policy_reason=policy_reason,
        ready_symbols=tuple(receipt.symbol for receipt in ready_receipts),
        blocked_symbols=tuple(receipt.symbol for receipt in blocked_receipts),
        blocking_receipt_ids=tuple(receipt.receipt_id for receipt in blocked_receipts),
        seed_mutation_allowed=seed_mutation_allowed,
        invariants_preserved=(
            "contiguous_level_1_seed_span",
            "no_partial_seed_hole",
            "no_guessed_physical_property_evidence",
            "readiness_is_not_approval",
        ),
    )


def validate_promotion_batch_policy_receipt(
    receipt: PromotionBatchPolicyReceipt | None = None,
) -> dict[str, Any]:
    checked_receipt = receipt if receipt is not None else get_promotion_batch_policy_receipt()
    errors = tuple(checked_receipt.validate())
    validation_status = "promotion_batch_policy_receipt_validated"
    if errors:
        validation_status = "promotion_batch_policy_receipt_rejected"
    return {
        "validation_status": validation_status,
        "policy_status": checked_receipt.policy_status,
        "policy_decision": checked_receipt.policy_decision,
        "ready_count": len(checked_receipt.ready_symbols),
        "blocked_count": len(checked_receipt.blocked_symbols),
        "seed_mutation_allowed": checked_receipt.seed_mutation_allowed,
        "errors": errors,
    }


def get_partial_promotion_eligibility_receipt() -> PartialPromotionEligibilityReceipt:
    batch_policy = get_promotion_batch_policy_receipt()
    decisions = list_promotion_decision_receipts()
    eligible_decisions = tuple(
        decision
        for decision in decisions
        if decision.decision_status == "promotion_ready_pending_approval"
    )
    blocked_decisions = tuple(
        decision
        for decision in decisions
        if decision.decision_status != "promotion_ready_pending_approval"
    )
    return PartialPromotionEligibilityReceipt(
        receipt_id="MSPEE-PARTIAL-PROMOTION-ELIGIBILITY-CS-RN",
        span_id=batch_policy.span_id,
        target_level=batch_policy.target_level,
        eligibility_status=(
            "partial_review_available_seed_mutation_blocked"
            if eligible_decisions
            else "partial_review_unavailable"
        ),
        eligible_symbols=tuple(decision.symbol for decision in eligible_decisions),
        blocked_symbols=tuple(decision.symbol for decision in blocked_decisions),
        eligible_decision_receipt_ids=tuple(
            decision.receipt_id for decision in eligible_decisions
        ),
        blocking_receipt_ids=tuple(decision.receipt_id for decision in blocked_decisions),
        batch_policy_receipt_id=batch_policy.receipt_id,
        batch_policy_decision=batch_policy.policy_decision,
        partial_review_allowed=bool(eligible_decisions),
        seed_mutation_allowed=False,
        required_next_action=(
            "review ready Cs-Rn receipts; when no blockers remain, use the full-span "
            "approval path rather than partial seed mutation"
        ),
        invariants_preserved=(
            "contiguous_level_1_seed_span",
            "no_partial_seed_hole",
            "readiness_is_not_approval",
            "seed_mutation_requires_full_span_policy_release",
        ),
    )


def validate_partial_promotion_eligibility_receipt(
    receipt: PartialPromotionEligibilityReceipt | None = None,
) -> dict[str, Any]:
    checked_receipt = (
        receipt if receipt is not None else get_partial_promotion_eligibility_receipt()
    )
    errors = tuple(checked_receipt.validate())
    return {
        "validation_status": (
            "partial_promotion_eligibility_receipt_validated"
            if not errors
            else "partial_promotion_eligibility_receipt_rejected"
        ),
        "eligible_count": len(checked_receipt.eligible_symbols),
        "blocked_count": len(checked_receipt.blocked_symbols),
        "partial_review_allowed": checked_receipt.partial_review_allowed,
        "seed_mutation_allowed": checked_receipt.seed_mutation_allowed,
        "errors": errors,
    }


def get_full_span_promotion_approval_review_receipt() -> (
    FullSpanPromotionApprovalReviewReceipt
):
    batch_policy = get_promotion_batch_policy_receipt()
    decisions = list_promotion_decision_receipts()
    ready_decisions = tuple(
        decision
        for decision in decisions
        if decision.decision_status == "promotion_ready_pending_approval"
    )
    blocked_decisions = tuple(
        decision
        for decision in decisions
        if decision.decision_status != "promotion_ready_pending_approval"
    )
    review_open = batch_policy.policy_decision == "allow_full_span_approval_review"
    return FullSpanPromotionApprovalReviewReceipt(
        receipt_id="MSPEE-FULL-SPAN-PROMOTION-APPROVAL-REVIEW-CS-RN",
        span_id=batch_policy.span_id,
        target_level=batch_policy.target_level,
        review_status=(
            "full_span_approval_review_open"
            if review_open
            else "full_span_approval_review_blocked"
        ),
        batch_policy_receipt_id=batch_policy.receipt_id,
        batch_policy_decision=batch_policy.policy_decision,
        ready_symbols=tuple(decision.symbol for decision in ready_decisions),
        blocked_symbols=tuple(decision.symbol for decision in blocked_decisions),
        ready_decision_receipt_ids=tuple(
            decision.receipt_id for decision in ready_decisions
        ),
        blocking_receipt_ids=tuple(decision.receipt_id for decision in blocked_decisions),
        approval_review_allowed=review_open,
        seed_mutation_allowed=False,
        required_next_action=(
            "issue an explicit full-span approval or rejection receipt before any "
            "Cs-Rn Level 1 seed mutation"
        ),
        invariants_preserved=(
            "contiguous_level_1_seed_span",
            "readiness_is_not_approval",
            "approval_review_is_not_seed_mutation",
            "seed_mutation_requires_explicit_approval_receipt",
        ),
    )


def validate_full_span_promotion_approval_review_receipt(
    receipt: FullSpanPromotionApprovalReviewReceipt | None = None,
) -> dict[str, Any]:
    checked_receipt = (
        receipt if receipt is not None else get_full_span_promotion_approval_review_receipt()
    )
    errors = tuple(checked_receipt.validate())
    return {
        "validation_status": (
            "full_span_promotion_approval_review_receipt_validated"
            if not errors
            else "full_span_promotion_approval_review_receipt_rejected"
        ),
        "review_status": checked_receipt.review_status,
        "ready_count": len(checked_receipt.ready_symbols),
        "blocked_count": len(checked_receipt.blocked_symbols),
        "approval_review_allowed": checked_receipt.approval_review_allowed,
        "seed_mutation_allowed": checked_receipt.seed_mutation_allowed,
        "errors": errors,
    }


def get_full_span_promotion_approval_decision_receipt() -> (
    FullSpanPromotionApprovalDecisionReceipt
):
    review = get_full_span_promotion_approval_review_receipt()
    return FullSpanPromotionApprovalDecisionReceipt(
        receipt_id="MSPEE-FULL-SPAN-PROMOTION-APPROVAL-DECISION-CS-RN",
        span_id=review.span_id,
        target_level=review.target_level,
        approval_decision="full_span_promotion_approved",
        approval_review_receipt_id=review.receipt_id,
        approval_review_status=review.review_status,
        approval_review_allowed=review.approval_review_allowed,
        approved_symbols=review.ready_symbols,
        rejected_symbols=(),
        blocking_receipt_ids=review.blocking_receipt_ids,
        decision_reason=(
            "all Cs-Rn promotion receipts are ready, full-span approval review is "
            "open, and the next governed action is an execution packet"
        ),
        seed_mutation_authorized=True,
        seed_mutation_applied=False,
        required_next_action=(
            "build the governed Cs-Rn seed-promotion execution packet"
        ),
        invariants_preserved=(
            "contiguous_level_1_seed_span",
            "readiness_is_not_approval",
            "approval_review_is_not_seed_mutation",
            "approval_decision_is_final_seed_gate",
            "approval_is_not_seed_mutation_application",
        ),
    )


def validate_full_span_promotion_approval_decision_receipt(
    receipt: FullSpanPromotionApprovalDecisionReceipt | None = None,
) -> dict[str, Any]:
    checked_receipt = (
        receipt if receipt is not None else get_full_span_promotion_approval_decision_receipt()
    )
    errors = tuple(checked_receipt.validate())
    return {
        "validation_status": (
            "full_span_promotion_approval_decision_receipt_validated"
            if not errors
            else "full_span_promotion_approval_decision_receipt_rejected"
        ),
        "approval_decision": checked_receipt.approval_decision,
        "approved_count": len(checked_receipt.approved_symbols),
        "rejected_count": len(checked_receipt.rejected_symbols),
        "blocking_receipt_count": len(checked_receipt.blocking_receipt_ids),
        "seed_mutation_authorized": checked_receipt.seed_mutation_authorized,
        "seed_mutation_applied": checked_receipt.seed_mutation_applied,
        "errors": errors,
    }


def get_full_span_promotion_execution_packet() -> FullSpanPromotionExecutionPacket:
    approval = get_full_span_promotion_approval_decision_receipt()
    return FullSpanPromotionExecutionPacket(
        receipt_id="MSPEE-FULL-SPAN-PROMOTION-EXECUTION-PACKET-CS-RN",
        span_id=approval.span_id,
        target_level=approval.target_level,
        execution_status="execution_packet_ready_not_applied",
        approval_decision_receipt_id=approval.receipt_id,
        approval_decision=approval.approval_decision,
        promotion_symbols=approval.approved_symbols,
        planned_seed_append_symbols=approval.approved_symbols,
        planned_operation="append_level_1_seed_records_cs_through_rn",
        current_seed_terminal_symbol="Xe",
        target_seed_terminal_symbol="Rn",
        planned_mutation_count=len(approval.approved_symbols),
        seed_mutation_authorized=approval.seed_mutation_authorized,
        seed_mutation_applied=False,
        rollback_strategy=(
            "discard unapplied packet before seed write; after future seed write, "
            "restore prior Level 1 seed snapshot through a separate rollback receipt"
        ),
        required_next_action=(
            "apply the Cs-Rn seed append through a separate governed seed-update receipt"
        ),
        invariants_preserved=(
            "contiguous_level_1_seed_span",
            "approval_decision_is_final_seed_gate",
            "approval_is_not_seed_mutation_application",
            "execution_packet_is_not_seed_mutation_application",
            "seed_write_requires_separate_update_receipt",
        ),
    )


def validate_full_span_promotion_execution_packet(
    packet: FullSpanPromotionExecutionPacket | None = None,
) -> dict[str, Any]:
    checked_packet = (
        packet if packet is not None else get_full_span_promotion_execution_packet()
    )
    errors = tuple(checked_packet.validate())
    return {
        "validation_status": (
            "full_span_promotion_execution_packet_validated"
            if not errors
            else "full_span_promotion_execution_packet_rejected"
        ),
        "execution_status": checked_packet.execution_status,
        "promotion_count": len(checked_packet.promotion_symbols),
        "planned_mutation_count": checked_packet.planned_mutation_count,
        "seed_mutation_authorized": checked_packet.seed_mutation_authorized,
        "seed_mutation_applied": checked_packet.seed_mutation_applied,
        "current_seed_terminal_symbol": checked_packet.current_seed_terminal_symbol,
        "target_seed_terminal_symbol": checked_packet.target_seed_terminal_symbol,
        "errors": errors,
    }
