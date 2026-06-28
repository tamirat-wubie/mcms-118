# Standards Profile

MCMS-118 uses a practical engineering standards profile, not a certification claim.

## Repository standards

```text
src-layout Python package
pytest test suite
machine-readable JSON registries
Markdown docs
GitHub Actions CI
Apache-2.0 license
security policy
contribution guide
changelog
citation metadata
```

## Governance standards

```text
deny by default for high-risk actions
append-only receipts
hash-chain ledgers
explicit evidence strength
no silent evidence upgrades
blocked claims remain blocked
secrets never materialize into receipts
waivers must be scoped, time-limited, and signed
```

## Maturity ladder

```text
M0 = concept / blueprint documented
M1 = module contract or scaffold implemented
M2 = tests pass for contract behavior
M3 = persisted with receipts
M4 = signed / governed
M5 = API exposed
M6 = dashboard visible
M7 = demo-ready
M8 = production-engineering-ready
```

## Readiness separation

Demo-ready means a safe local demo works with sample data.
Production-engineering-ready requires real authentication, real storage, backups, restore verification, monitoring, incident response, and independent review.
