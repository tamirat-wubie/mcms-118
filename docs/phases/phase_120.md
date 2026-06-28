# MCMS-118-P120 — Neurotransmitter Cleft Diffusion, AMPA/NMDA Receptor Binding Kinetics, Stochastic Receptor Activation, and Postsynaptic Current/Voltage Waveform Split

## Canonical naming

```text
Project: MCMS-118 — Causal Matter Standard
Repository: mcms-118
Distribution: mcms-118
Import namespace: mcms
Phase ID: MCMS-118-P120
Slug: neurotransmitter-cleft-diffusion-ampa-nmda-receptor-binding-kinetics-stochastic-receptor-activation-and-postsynaptic-cur
Metadata: docs/phase_metadata/phase_120.json
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

Model, govern, and audit: Neurotransmitter Cleft Diffusion → AMPA/NMDA Receptor Binding Kinetics → Stochastic Receptor Activation → and Postsynaptic Current/Voltage Waveform Split.

## Capability chain

```text
Neurotransmitter Cleft Diffusion → AMPA/NMDA Receptor Binding Kinetics → Stochastic Receptor Activation → and Postsynaptic Current/Voltage Waveform Split
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
Phase doc: docs/phases/phase_120.md
Phase metadata: docs/phase_metadata/phase_120.json
Registry: docs/PHASE_REGISTRY.json
```

## Modules

- `neurotransmitter_cleft_diffusion.py`
- `ampa_nmda_receptor_binding.py`
- `stochastic_receptor_activation.py`
- `postsynaptic_current_waveform.py`
- `postsynaptic_voltage_waveform.py`
- `cleft_receptor_boundary.py`

## Status vocabulary sample

- `supported`
- `evidence_required`
- `insufficient_data`
- `safety_boundary`
- `conflict_detected`
- `review_required`
- `blocked_claim`
- `neurotransmitter_cleft_diffusion_supported`
- `neurotransmitter_cleft_diffusion_evidence_required`
- `neurotransmitter_cleft_diffusion_conflict`
- `neurotransmitter_cleft_diffusion_safety_boundary`
- `neurotransmitter_cleft_diffusion_insufficient_data`
- `ampa_nmda_receptor_binding_supported`
- `ampa_nmda_receptor_binding_evidence_required`
- `ampa_nmda_receptor_binding_conflict`
- `ampa_nmda_receptor_binding_safety_boundary`
- `ampa_nmda_receptor_binding_insufficient_data`
- `stochastic_receptor_activation_supported`
- `stochastic_receptor_activation_evidence_required`
- `stochastic_receptor_activation_conflict`
- `stochastic_receptor_activation_safety_boundary`
- `stochastic_receptor_activation_insufficient_data`
- `postsynaptic_current_waveform_supported`
- `postsynaptic_current_waveform_evidence_required`
- `postsynaptic_current_waveform_conflict`
- `postsynaptic_current_waveform_safety_boundary`
- `postsynaptic_current_waveform_insufficient_data`
- `postsynaptic_voltage_waveform_supported`
- `postsynaptic_voltage_waveform_evidence_required`
- `postsynaptic_voltage_waveform_conflict`

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
