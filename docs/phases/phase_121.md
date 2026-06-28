# MCMS-118-P121 — Receptor-State Markov Chains, PSD Spatial Receptor Field, AMPA Desensitization Recovery, NMDA Subunit Kinetics, and Dendritic Cable Waveform Propagation

## Canonical naming

```text
Project: MCMS-118 — Causal Matter Standard
Repository: mcms-118
Distribution: mcms-118
Import namespace: mcms
Phase ID: MCMS-118-P121
Slug: receptor-state-markov-chains-psd-spatial-receptor-field-ampa-desensitization-recovery-nmda-subunit-kinetics-and-dendriti
Metadata: docs/phase_metadata/phase_121.json
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

Model, govern, and audit: Receptor-State Markov Chains → PSD Spatial Receptor Field → AMPA Desensitization Recovery → NMDA Subunit Kinetics → and Dendritic Cable Waveform Propagation.

## Capability chain

```text
Receptor-State Markov Chains → PSD Spatial Receptor Field → AMPA Desensitization Recovery → NMDA Subunit Kinetics → and Dendritic Cable Waveform Propagation
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
Phase doc: docs/phases/phase_121.md
Phase metadata: docs/phase_metadata/phase_121.json
Registry: docs/PHASE_REGISTRY.json
```

## Modules

- `receptor_state_markov_chains.py`
- `psd_spatial_receptor_field.py`
- `ampa_desensitization_recovery.py`
- `nmda_subunit_kinetics.py`
- `dendritic_cable_waveform_propagation.py`
- `receptor_markov_boundary.py`

## Status vocabulary sample

- `supported`
- `evidence_required`
- `insufficient_data`
- `safety_boundary`
- `conflict_detected`
- `review_required`
- `blocked_claim`
- `receptor_state_markov_chains_supported`
- `receptor_state_markov_chains_evidence_required`
- `receptor_state_markov_chains_conflict`
- `receptor_state_markov_chains_safety_boundary`
- `receptor_state_markov_chains_insufficient_data`
- `psd_spatial_receptor_field_supported`
- `psd_spatial_receptor_field_evidence_required`
- `psd_spatial_receptor_field_conflict`
- `psd_spatial_receptor_field_safety_boundary`
- `psd_spatial_receptor_field_insufficient_data`
- `ampa_desensitization_recovery_supported`
- `ampa_desensitization_recovery_evidence_required`
- `ampa_desensitization_recovery_conflict`
- `ampa_desensitization_recovery_safety_boundary`
- `ampa_desensitization_recovery_insufficient_data`
- `nmda_subunit_kinetics_supported`
- `nmda_subunit_kinetics_evidence_required`
- `nmda_subunit_kinetics_conflict`
- `nmda_subunit_kinetics_safety_boundary`
- `nmda_subunit_kinetics_insufficient_data`
- `dendritic_cable_waveform_propagation_supported`
- `dendritic_cable_waveform_propagation_evidence_required`
- `dendritic_cable_waveform_propagation_conflict`

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
