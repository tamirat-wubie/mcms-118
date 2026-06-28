# Release Policy

MCMS-118 release promotion is evidence-first.

A release candidate should include:

```text
policy decision
session receipt
ABAC decision
CI/CD workflow receipt
artifact signature
SBOM
vulnerability scan
secret state
checkpoint
restore drill
approval receipt
waiver ledger if any
promotion replay result
```

A release is blocked when required evidence is missing, stale, unsigned, unverifiable, contradicted, or outside scope.
