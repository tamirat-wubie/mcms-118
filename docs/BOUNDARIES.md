# MCMS Boundaries

MCMS is a symbolic engineering and governance platform.

## Allowed claims

```text
symbolic_model
source_backed_claim
computed_result
simulation_result
governance_marker
evidence_receipt
release_evidence_marker
engineering_readiness_marker
blocked_claim
unknown
```

## Blocked claims

```text
legal_compliance_claim
security_certified_claim
production_customer_ready_claim
financial_operation_claim
autonomous_real_world_action_claim
medical_or_clinical_claim
cognitive_enhancement_claim
biological_memory_claim
AGI_or_ASI_claim
```

## Default policy

```text
default = deny
read = permission required
write = permission + receipt required
repair = approval required
migration = approval + backup required
release = signed evidence bundle required
external action = human review required
high-risk claim = blocked unless explicitly allowed by boundary compiler
```
