from __future__ import annotations

from dataclasses import dataclass

ALLOWED_CLAIM_TYPES = {
    "observed_fact",
    "source_backed_claim",
    "computed_result",
    "symbolic_simulation",
    "prediction",
    "proposal",
    "governance_marker",
    "release_evidence_marker",
    "engineering_readiness_marker",
    "unknown",
}

BLOCKED_CLAIM_TYPES = {
    "legal_compliance_claim",
    "security_certified_claim",
    "production_customer_ready_claim",
    "financial_operation_claim",
    "autonomous_real_world_action_claim",
    "medical_or_clinical_claim",
    "cognitive_enhancement_claim",
    "biological_memory_claim",
    "AGI_or_ASI_claim",
}

@dataclass(frozen=True)
class ClaimBoundaryResult:
    claim_text: str
    claim_type: str
    allowed: bool
    status: str
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def compile_claim_boundary(claim_text: str, claim_type: str, evidence_strength: float = 0.0) -> ClaimBoundaryResult:
    if not claim_text or not claim_type or evidence_strength < 0:
        return ClaimBoundaryResult(claim_text, claim_type, False, "insufficient_data", "Claim input is invalid.")
    if claim_type in BLOCKED_CLAIM_TYPES:
        return ClaimBoundaryResult(claim_text, claim_type, False, "blocked_claim", "Claim type is blocked by MCMS boundary.")
    if claim_type not in ALLOWED_CLAIM_TYPES:
        return ClaimBoundaryResult(claim_text, claim_type, False, "unknown_claim_type", "Claim type is unknown and denied by default.")
    if claim_type == "source_backed_claim" and evidence_strength < 0.7:
        return ClaimBoundaryResult(claim_text, claim_type, False, "evidence_required", "Source-backed claim needs stronger evidence.")
    return ClaimBoundaryResult(claim_text, claim_type, True, "claim_allowed", "Claim is allowed within symbolic boundary.")
