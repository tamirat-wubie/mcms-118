from __future__ import annotations

from dataclasses import dataclass

@dataclass
class ReproduciblePromotionBoundaryResult:
    release_key: str
    sandbox_status: str
    retry_status: str
    github_cache_status: str
    jsonschema_status: str
    sarif_taxonomy_status: str
    waiver_status: str
    archive_status: str
    environment_replay_status: str
    evidence_strength: float
    boundary_status: str
    allowed_claim: str
    blocked_claims: list[str]
    explanation: str
    boundary: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def evaluate_reproducible_promotion_boundary(release_key: str, sandbox_status: str, retry_status: str, github_cache_status: str, jsonschema_status: str, sarif_taxonomy_status: str, waiver_status: str, archive_status: str, environment_replay_status: str, evidence_strength: float, safety_blocked: bool = False) -> ReproduciblePromotionBoundaryResult:
    blocked = ["legal_compliance_claim", "security_certified_claim", "production_customer_ready_claim", "financial_operation_claim", "autonomous_real_world_action_claim"]
    if evidence_strength < 0:
        status="insufficient_data"; allowed="none"; explanation="evidence_strength cannot be negative."
    elif safety_blocked:
        status="reproducible_promotion_safety_blocked"; allowed="safety_boundary_only"; explanation="Reproducible promotion path is safety-blocked."
    elif evidence_strength < 0.7:
        status="evidence_required"; allowed="placeholder_only"; explanation="Evidence is too weak for reproducible promotion marker."
    elif sandbox_status != "sandbox_policy_ready":
        status="sandbox_blocks_replay"; allowed="sandbox_block_marker"; explanation="Sandbox policy blocks replay."
    elif retry_status in {"retry_budget_exhausted", "non_retryable_error", "retry_safety_boundary"}:
        status="retry_blocks_replay"; allowed="retry_block_marker"; explanation="HTTP retry/backoff state blocks replay."
    elif github_cache_status in {"github_pagination_conflict", "github_cache_safety_boundary"}:
        status="github_cache_blocks_replay"; allowed="github_cache_block_marker"; explanation="GitHub pagination/cache state blocks replay."
    elif jsonschema_status not in {"jsonschema_validation_passed", "jsonschema_binding_available"}:
        status="schema_blocks_replay"; allowed="schema_block_marker"; explanation="JSONSchema binding blocks replay."
    elif sarif_taxonomy_status in {"sarif_security_critical", "sarif_security_high", "sarif_error", "sarif_taxonomy_conflict"} and waiver_status not in {"waiver_entry_verified", "waiver_entry_signed"}:
        status="sarif_taxonomy_blocks_replay"; allowed="sarif_taxonomy_block_marker"; explanation="SARIF taxonomy blocks replay without signed waiver."
    elif waiver_status in {"waiver_entry_signature_invalid", "waiver_entry_expired", "waiver_entry_scope_invalid"}:
        status="waiver_signature_blocks_replay"; allowed="waiver_signature_block_marker"; explanation="Signed waiver entry blocks replay."
    elif archive_status not in {"compressed_archive_signature_verified", "compressed_archive_hash_verified", "compressed_archive_created"}:
        status="archive_blocks_replay"; allowed="archive_block_marker"; explanation="Compressed evidence archive blocks replay."
    elif environment_replay_status != "environment_snapshot_replay_matched":
        status="environment_snapshot_blocks_replay"; allowed="environment_snapshot_block_marker"; explanation="Environment snapshot replay blocks reproducibility."
    else:
        status="reproducible_promotion_ready"; allowed="reproducible_promotion_engineering_marker"; explanation="Promotion decision is reproducible under evidence, policy, and environment snapshot."
    return ReproduciblePromotionBoundaryResult(release_key, sandbox_status, retry_status, github_cache_status, jsonschema_status, sarif_taxonomy_status, waiver_status, archive_status, environment_replay_status, evidence_strength, status, allowed, blocked, explanation, "reproducible_promotion_marker_not_certification_or_customer_ready_claim")
