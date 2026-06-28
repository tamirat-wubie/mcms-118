# MCMS-118-P124 — Interneuron Subtype Routing, PV/SOM/VIP/Chandelier Circuit Motifs, Conductance-Based Spike Waveform, Sodium Inactivation, Potassium Recovery, and Axonal Propagation

## Canonical naming

```text
Project: MCMS-118 — Causal Matter Standard
Repository: mcms-118
Distribution: mcms-118
Import namespace: mcms
Phase ID: MCMS-118-P124
Slug: interneuron-subtype-routing-pv-som-vip-chandelier-circuit-motifs-conductance-based-spike-waveform-sodium-inactivation-po
Metadata: docs/phase_metadata/phase_124.json
```

## Status

```text
module scaffold included
Maturity: M1/M2 — module contracts/scaffolds included and registry-tested
```

## Domain and layer

```text
Domain: neurosymbolic spike, circuit, recurrent graph, and closed-loop modeling
Layer: interneuron routing, recurrent graph simulation, plasticity stack, and closed loop
```

## Objective

Model, govern, and audit: Interneuron Subtype Routing → PV/SOM/VIP/Chandelier Circuit Motifs → Conductance-Based Spike Waveform → Sodium Inactivation → Potassium Recovery.

## Capability chain

```text
Interneuron Subtype Routing → PV/SOM/VIP/Chandelier Circuit Motifs → Conductance-Based Spike Waveform → Sodium Inactivation → Potassium Recovery → and Axonal Propagation
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
Phase doc: docs/phases/phase_124.md
Phase metadata: docs/phase_metadata/phase_124.json
Registry: docs/PHASE_REGISTRY.json
```

## Modules

- `interneuron_subtype_routing.py`
- `inhibitory_circuit_motif.py`
- `compartment_inhibition_router.py`
- `vip_disinhibition_gate.py`
- `conductance_spike_waveform.py`
- `sodium_channel_inactivation.py`
- `potassium_channel_recovery.py`
- `axonal_spike_propagation.py`
- `spike_waveform_boundary.py`
- `interneuron_spike_network.py`
- `interneuron_spike_explain.py`

## Status vocabulary sample

- `supported`
- `evidence_required`
- `insufficient_data`
- `safety_boundary`
- `conflict_detected`
- `review_required`
- `blocked_claim`
- `interneuron_subtype_routing_supported`
- `interneuron_subtype_routing_evidence_required`
- `interneuron_subtype_routing_conflict`
- `interneuron_subtype_routing_safety_boundary`
- `interneuron_subtype_routing_insufficient_data`
- `inhibitory_circuit_motif_supported`
- `inhibitory_circuit_motif_evidence_required`
- `inhibitory_circuit_motif_conflict`
- `inhibitory_circuit_motif_safety_boundary`
- `inhibitory_circuit_motif_insufficient_data`
- `compartment_inhibition_router_supported`
- `compartment_inhibition_router_evidence_required`
- `compartment_inhibition_router_conflict`
- `compartment_inhibition_router_safety_boundary`
- `compartment_inhibition_router_insufficient_data`
- `vip_disinhibition_gate_supported`
- `vip_disinhibition_gate_evidence_required`
- `vip_disinhibition_gate_conflict`
- `vip_disinhibition_gate_safety_boundary`
- `vip_disinhibition_gate_insufficient_data`
- `conductance_spike_waveform_supported`
- `conductance_spike_waveform_evidence_required`
- `conductance_spike_waveform_conflict`

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
