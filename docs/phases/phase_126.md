# MCMS-118-P126 — Recurrent Graph Simulator, Edge-Specific Synaptic Weights, STDP-Like Timing Plasticity, Neuromodulator Gain Control, Population Homeostasis, and Oscillation Band Classifier

## Canonical naming

```text
Project: MCMS-118 — Causal Matter Standard
Repository: mcms-118
Distribution: mcms-118
Import namespace: mcms
Phase ID: MCMS-118-P126
Slug: recurrent-graph-simulator-edge-specific-synaptic-weights-stdp-like-timing-plasticity-neuromodulator-gain-control-populat
Metadata: docs/phase_metadata/phase_126.json
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

Model, govern, and audit: Recurrent Graph Simulator → Edge-Specific Synaptic Weights → STDP-Like Timing Plasticity → Neuromodulator Gain Control → Population Homeostasis.

## Capability chain

```text
Recurrent Graph Simulator → Edge-Specific Synaptic Weights → STDP-Like Timing Plasticity → Neuromodulator Gain Control → Population Homeostasis → and Oscillation Band Classifier
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
Phase doc: docs/phases/phase_126.md
Phase metadata: docs/phase_metadata/phase_126.json
Registry: docs/PHASE_REGISTRY.json
```

## Modules

- `recurrent_graph.py`
- `edge_synaptic_weight_state.py`
- `graph_event_scheduler.py`
- `stdp_timing_plasticity.py`
- `neuromodulator_gain_control.py`
- `population_homeostasis_controller.py`
- `oscillation_band_classifier.py`
- `avalanche_criticality_detector.py`
- `long_horizon_graph_simulator.py`
- `recurrent_graph_boundary.py`
- `recurrent_graph_network.py`
- `recurrent_graph_explain.py`

## Status vocabulary sample

- `supported`
- `evidence_required`
- `insufficient_data`
- `safety_boundary`
- `conflict_detected`
- `review_required`
- `blocked_claim`
- `recurrent_graph_supported`
- `recurrent_graph_evidence_required`
- `recurrent_graph_conflict`
- `recurrent_graph_safety_boundary`
- `recurrent_graph_insufficient_data`
- `edge_synaptic_weight_state_supported`
- `edge_synaptic_weight_state_evidence_required`
- `edge_synaptic_weight_state_conflict`
- `edge_synaptic_weight_state_safety_boundary`
- `edge_synaptic_weight_state_insufficient_data`
- `graph_event_scheduler_supported`
- `graph_event_scheduler_evidence_required`
- `graph_event_scheduler_conflict`
- `graph_event_scheduler_safety_boundary`
- `graph_event_scheduler_insufficient_data`
- `stdp_timing_plasticity_supported`
- `stdp_timing_plasticity_evidence_required`
- `stdp_timing_plasticity_conflict`
- `stdp_timing_plasticity_safety_boundary`
- `stdp_timing_plasticity_insufficient_data`
- `neuromodulator_gain_control_supported`
- `neuromodulator_gain_control_evidence_required`
- `neuromodulator_gain_control_conflict`

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
