# MCMS-118-P128 — Persistent Graph Memory, Trace Compression/Forgotten-State Policy, Conflict-Aware Replay Selection, Action-Effect Feedback Receipts, Environment State Model, and Closed-Loop Governance Ledger

## Canonical naming

```text
Project: MCMS-118 — Causal Matter Standard
Repository: mcms-118
Distribution: mcms-118
Import namespace: mcms
Phase ID: MCMS-118-P128
Slug: persistent-graph-memory-trace-compression-forgotten-state-policy-conflict-aware-replay-selection-action-effect-feedback-
Metadata: docs/phase_metadata/phase_128.json
```

## Status

```text
module scaffold included
Maturity: M1/M2 — module contracts/scaffolds included and registry-tested
```

## Domain and layer

```text
Domain: release governance, persistence, software supply chain, and deployment evidence
Layer: persistent graph memory and closed-loop audit ledger
```

## Objective

Model, govern, and audit: Persistent Graph Memory → Trace Compression/Forgotten-State Policy → Conflict-Aware Replay Selection → Action-Effect Feedback Receipts → Environment State Model.

## Capability chain

```text
Persistent Graph Memory → Trace Compression/Forgotten-State Policy → Conflict-Aware Replay Selection → Action-Effect Feedback Receipts → Environment State Model → and Closed-Loop Governance Ledger
```

## Boundary

Symbolic matter, biochemical/bioelectrical graph, governance, release-evidence, and deployment-engineering modeling only. This phase does not claim medical, neurological, cognitive, diagnostic, treatment, legal compliance, security certification, customer readiness, financial-operation readiness, or autonomous real-world-action approval.

## Blocked claims

- `medical_claim`
- `neurological_or_cognitive_claim`
- `diagnostic_or_treatment_claim`
- `legal_compliance_claim`
- `security_certified_claim`
- `production_customer_ready_claim`
- `financial_operation_claim`
- `autonomous_real_world_action_claim`

## Standards profile

```text
Naming standard: NS-1.0.0
Metadata schema: 1.1.0
Policy posture: deny by default for high-risk actions and blocked claims
Receipt policy: append-only hash-addressed receipts
Secret policy: secret values must never be materialized into docs, logs, receipts, or exported evidence
Readiness separation: demo-ready and production-engineering-ready are separate states
```

## Artifacts

```text
Phase doc: docs/phases/phase_128.md
Phase metadata: docs/phase_metadata/phase_128.json
Registry: docs/PHASE_REGISTRY.json
```

## Modules

- `persistent_graph_memory.py`
- `append_only_event_log.py`
- `trace_compression_policy.py`
- `forgetting_retention_policy.py`
- `conflict_aware_replay_selection.py`
- `action_decision_receipt.py`
- `action_effect_feedback_receipt.py`
- `environment_state_model.py`
- `governance_ledger.py`
- `closed_loop_audit_network.py`
- `closed_loop_audit_explain.py`

## Status vocabulary sample

- `supported`
- `evidence_required`
- `insufficient_data`
- `safety_boundary`
- `conflict_detected`
- `review_required`
- `blocked_claim`
- `persistent_graph_memory_supported`
- `persistent_graph_memory_evidence_required`
- `persistent_graph_memory_conflict`
- `persistent_graph_memory_safety_boundary`
- `persistent_graph_memory_insufficient_data`
- `append_only_event_log_supported`
- `append_only_event_log_evidence_required`
- `append_only_event_log_conflict`
- `append_only_event_log_safety_boundary`
- `append_only_event_log_insufficient_data`
- `trace_compression_policy_supported`
- `trace_compression_policy_evidence_required`
- `trace_compression_policy_conflict`
- `trace_compression_policy_safety_boundary`
- `trace_compression_policy_insufficient_data`
- `forgetting_retention_policy_supported`
- `forgetting_retention_policy_evidence_required`
- `forgetting_retention_policy_conflict`
- `forgetting_retention_policy_safety_boundary`
- `forgetting_retention_policy_insufficient_data`
- `conflict_aware_replay_selection_supported`
- `conflict_aware_replay_selection_evidence_required`
- `conflict_aware_replay_selection_conflict`

## Evidence policy

```json
{
  "minimum_source_backed_evidence_strength": 0.7,
  "weak_evidence_status": "evidence_required",
  "computed_result_rule": "computed results cannot be promoted to measured facts without source-backed evidence",
  "prediction_rule": "predictions remain predictions until separate observation/verification receipts exist",
  "secret_rule": "secret values must never be written into receipts, logs, docs, or exports"
}
```

## Implementation truth

Generated module-contract phase: module files, importable scaffolds, registry metadata, and contract tests are included; deep domain implementation can replace scaffolds without changing metadata contracts.

## Upgrade path

- replace scaffold logic with domain-specific implementation
- add focused invariant tests
- add persistence receipts
- add signature/governance checks
- expose API endpoint
- surface dashboard card
- create demo fixture
- run release evidence gate before promotion
