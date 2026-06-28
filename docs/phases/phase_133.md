# MCMS-118-P133 — Real OPA Eval Adapter, Secret Manager Connectors, GitHub Actions Adapter, Sigstore/Cosign Verification, SBOM Schema Validation, SARIF Ingestion, Waiver Workflow, SLSA Provenance Classifier, and Evidence Bundle Export

## Canonical naming

```text
Project: MCMS-118 — Causal Matter Standard
Repository: mcms-118
Distribution: mcms-118
Import namespace: mcms
Phase ID: MCMS-118-P133
Slug: real-opa-eval-adapter-secret-manager-connectors-github-actions-adapter-sigstore-cosign-verification-sbom-schema-validati
Metadata: docs/phase_metadata/phase_133.json
```

## Status

```text
module scaffold included
Maturity: M1/M2 — module contracts/scaffolds included and registry-tested
```

## Domain and layer

```text
Domain: release governance, persistence, software supply chain, and deployment evidence
Layer: real release evidence adapter normalization
```

## Objective

Model, govern, and audit: Real OPA Eval Adapter → Secret Manager Connectors → GitHub Actions Adapter → Sigstore/Cosign Verification → SBOM Schema Validation.

## Capability chain

```text
Real OPA Eval Adapter → Secret Manager Connectors → GitHub Actions Adapter → Sigstore/Cosign Verification → SBOM Schema Validation → SARIF Ingestion → Waiver Workflow → SLSA Provenance Classifier → and Evidence Bundle Export
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
Phase doc: docs/phases/phase_133.md
Phase metadata: docs/phase_metadata/phase_133.json
Registry: docs/PHASE_REGISTRY.json
```

## Modules

- `real_opa_eval_adapter.py`
- `secret_manager_connector.py`
- `github_actions_adapter.py`
- `sigstore_cosign_verifier.py`
- `sbom_schema_validator.py`
- `sarif_ingestion.py`
- `waiver_exception_workflow.py`
- `slsa_provenance_classifier.py`
- `evidence_bundle_exporter.py`
- `real_evidence_boundary.py`
- `real_release_evidence_network.py`
- `real_release_evidence_explain.py`

## Status vocabulary sample

- `supported`
- `evidence_required`
- `insufficient_data`
- `safety_boundary`
- `conflict_detected`
- `review_required`
- `blocked_claim`
- `real_opa_eval_adapter_supported`
- `real_opa_eval_adapter_evidence_required`
- `real_opa_eval_adapter_conflict`
- `real_opa_eval_adapter_safety_boundary`
- `real_opa_eval_adapter_insufficient_data`
- `secret_manager_connector_supported`
- `secret_manager_connector_evidence_required`
- `secret_manager_connector_conflict`
- `secret_manager_connector_safety_boundary`
- `secret_manager_connector_insufficient_data`
- `github_actions_adapter_supported`
- `github_actions_adapter_evidence_required`
- `github_actions_adapter_conflict`
- `github_actions_adapter_safety_boundary`
- `github_actions_adapter_insufficient_data`
- `sigstore_cosign_verifier_supported`
- `sigstore_cosign_verifier_evidence_required`
- `sigstore_cosign_verifier_conflict`
- `sigstore_cosign_verifier_safety_boundary`
- `sigstore_cosign_verifier_insufficient_data`
- `sbom_schema_validator_supported`
- `sbom_schema_validator_evidence_required`
- `sbom_schema_validator_conflict`

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
