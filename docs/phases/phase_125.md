# MCMS-118-P125 — Recurrent E/I Circuit Loop, Layer-Specific Routing, Synaptic Delay, Node-of-Ranvier Propagation, Axon Collateral Branching, and Population Firing Boundary

## Canonical naming

```text
Project: MCMS-118 — Causal Matter Standard
Repository: mcms-118
Distribution: mcms-118
Import namespace: mcms
Phase ID: MCMS-118-P125
Slug: recurrent-e-i-circuit-loop-layer-specific-routing-synaptic-delay-node-of-ranvier-propagation-axon-collateral-branching-a
Metadata: docs/phase_metadata/phase_125.json
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

Model, govern, and audit: Recurrent E/I Circuit Loop → Layer-Specific Routing → Synaptic Delay → Node-of-Ranvier Propagation → Axon Collateral Branching.

## Capability chain

```text
Recurrent E/I Circuit Loop → Layer-Specific Routing → Synaptic Delay → Node-of-Ranvier Propagation → Axon Collateral Branching → and Population Firing Boundary
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
Phase doc: docs/phases/phase_125.md
Phase metadata: docs/phase_metadata/phase_125.json
Registry: docs/PHASE_REGISTRY.json
```

## Modules

- `recurrent_ei_loop.py`
- `layer_specific_routing.py`
- `synaptic_delay_gate.py`
- `node_ranvier_propagation.py`
- `axon_collateral_branching.py`
- `population_firing_state.py`
- `network_synchrony_detector.py`
- `recurrent_stability_boundary.py`
- `recurrent_circuit_network.py`
- `recurrent_circuit_explain.py`

## Status vocabulary sample

- `supported`
- `evidence_required`
- `insufficient_data`
- `safety_boundary`
- `conflict_detected`
- `review_required`
- `blocked_claim`
- `recurrent_ei_loop_supported`
- `recurrent_ei_loop_evidence_required`
- `recurrent_ei_loop_conflict`
- `recurrent_ei_loop_safety_boundary`
- `recurrent_ei_loop_insufficient_data`
- `layer_specific_routing_supported`
- `layer_specific_routing_evidence_required`
- `layer_specific_routing_conflict`
- `layer_specific_routing_safety_boundary`
- `layer_specific_routing_insufficient_data`
- `synaptic_delay_gate_supported`
- `synaptic_delay_gate_evidence_required`
- `synaptic_delay_gate_conflict`
- `synaptic_delay_gate_safety_boundary`
- `synaptic_delay_gate_insufficient_data`
- `node_ranvier_propagation_supported`
- `node_ranvier_propagation_evidence_required`
- `node_ranvier_propagation_conflict`
- `node_ranvier_propagation_safety_boundary`
- `node_ranvier_propagation_insufficient_data`
- `axon_collateral_branching_supported`
- `axon_collateral_branching_evidence_required`
- `axon_collateral_branching_conflict`

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
