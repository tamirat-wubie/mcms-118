# MCMS-118-P123 — Chloride Transporters, KCC2/NKCC1 Homeostasis, Perisomatic/Dendritic/AIS Inhibition Placement, Refractory Period, and Spike-Train Generation

## Canonical naming

```text
Project: MCMS-118 — Causal Matter Standard
Repository: mcms-118
Distribution: mcms-118
Import namespace: mcms
Phase ID: MCMS-118-P123
Slug: chloride-transporters-kcc2-nkcc1-homeostasis-perisomatic-dendritic-ais-inhibition-placement-refractory-period-and-spike-
Metadata: docs/phase_metadata/phase_123.json
```

## Status

```text
module scaffold included
Maturity: M1/M2 — module contracts/scaffolds included and registry-tested
```

## Domain and layer

```text
Domain: neurosymbolic spike, circuit, recurrent graph, and closed-loop modeling
Layer: active zones, receptor chains, inhibition, chloride, and spike trains
```

## Objective

Model, govern, and audit: Chloride Transporters → KCC2/NKCC1 Homeostasis → Perisomatic/Dendritic/AIS Inhibition Placement → Refractory Period → and Spike-Train Generation.

## Capability chain

```text
Chloride Transporters → KCC2/NKCC1 Homeostasis → Perisomatic/Dendritic/AIS Inhibition Placement → Refractory Period → and Spike-Train Generation
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
Phase doc: docs/phases/phase_123.md
Phase metadata: docs/phase_metadata/phase_123.json
Registry: docs/PHASE_REGISTRY.json
```

## Modules

- `chloride_transporter_balance.py`
- `chloride_reversal_adaptation.py`
- `inhibition_placement.py`
- `ais_axoaxonic_inhibition.py`
- `refractory_period_gate.py`
- `afterhyperpolarization_adaptation.py`
- `spike_train_generator.py`
- `spike_train_metrics.py`
- `spike_train_boundary.py`
- `spike_train_network.py`
- `spike_train_explain.py`

## Status vocabulary sample

- `supported`
- `evidence_required`
- `insufficient_data`
- `safety_boundary`
- `conflict_detected`
- `review_required`
- `blocked_claim`
- `chloride_transporter_balance_supported`
- `chloride_transporter_balance_evidence_required`
- `chloride_transporter_balance_conflict`
- `chloride_transporter_balance_safety_boundary`
- `chloride_transporter_balance_insufficient_data`
- `chloride_reversal_adaptation_supported`
- `chloride_reversal_adaptation_evidence_required`
- `chloride_reversal_adaptation_conflict`
- `chloride_reversal_adaptation_safety_boundary`
- `chloride_reversal_adaptation_insufficient_data`
- `inhibition_placement_supported`
- `inhibition_placement_evidence_required`
- `inhibition_placement_conflict`
- `inhibition_placement_safety_boundary`
- `inhibition_placement_insufficient_data`
- `ais_axoaxonic_inhibition_supported`
- `ais_axoaxonic_inhibition_evidence_required`
- `ais_axoaxonic_inhibition_conflict`
- `ais_axoaxonic_inhibition_safety_boundary`
- `ais_axoaxonic_inhibition_insufficient_data`
- `refractory_period_gate_supported`
- `refractory_period_gate_evidence_required`
- `refractory_period_gate_conflict`

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
