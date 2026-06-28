# MCMS-118-P122 — Inhibitory GABA-A/GABA-B Receptor-State Chains, Chloride Gradient, Shunting Inhibition, Excitation/Inhibition Waveform Balance, and Soma-to-Axon Spike Initiation Boundary

## Canonical naming

```text
Project: MCMS-118 — Causal Matter Standard
Repository: mcms-118
Distribution: mcms-118
Import namespace: mcms
Phase ID: MCMS-118-P122
Slug: inhibitory-gaba-a-gaba-b-receptor-state-chains-chloride-gradient-shunting-inhibition-excitation-inhibition-waveform-bala
Metadata: docs/phase_metadata/phase_122.json
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

Model, govern, and audit: Inhibitory GABA-A/GABA-B Receptor-State Chains → Chloride Gradient → Shunting Inhibition → Excitation/Inhibition Waveform Balance → and Soma-to-Axon Spike Initiation Boundary.

## Capability chain

```text
Inhibitory GABA-A/GABA-B Receptor-State Chains → Chloride Gradient → Shunting Inhibition → Excitation/Inhibition Waveform Balance → and Soma-to-Axon Spike Initiation Boundary
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
Phase doc: docs/phases/phase_122.md
Phase metadata: docs/phase_metadata/phase_122.json
Registry: docs/PHASE_REGISTRY.json
```

## Modules

- `inhibitory_gabaa_receptor_chain.py`
- `inhibitory_gabab_receptor_chain.py`
- `chloride_gradient.py`
- `shunting_inhibition.py`
- `ei_waveform_balance.py`
- `soma_axon_spike_initiation_boundary.py`

## Status vocabulary sample

- `supported`
- `evidence_required`
- `insufficient_data`
- `safety_boundary`
- `conflict_detected`
- `review_required`
- `blocked_claim`
- `inhibitory_gabaa_receptor_chain_supported`
- `inhibitory_gabaa_receptor_chain_evidence_required`
- `inhibitory_gabaa_receptor_chain_conflict`
- `inhibitory_gabaa_receptor_chain_safety_boundary`
- `inhibitory_gabaa_receptor_chain_insufficient_data`
- `inhibitory_gabab_receptor_chain_supported`
- `inhibitory_gabab_receptor_chain_evidence_required`
- `inhibitory_gabab_receptor_chain_conflict`
- `inhibitory_gabab_receptor_chain_safety_boundary`
- `inhibitory_gabab_receptor_chain_insufficient_data`
- `chloride_gradient_supported`
- `chloride_gradient_evidence_required`
- `chloride_gradient_conflict`
- `chloride_gradient_safety_boundary`
- `chloride_gradient_insufficient_data`
- `shunting_inhibition_supported`
- `shunting_inhibition_evidence_required`
- `shunting_inhibition_conflict`
- `shunting_inhibition_safety_boundary`
- `shunting_inhibition_insufficient_data`
- `ei_waveform_balance_supported`
- `ei_waveform_balance_evidence_required`
- `ei_waveform_balance_conflict`

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
