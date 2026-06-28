# Contributing

Contributions should preserve the MCMS-118 boundary model.

## Required checks

Before opening a pull request:

```bash
python scripts/verify_repo.py
python -m pytest
```

## Naming rules

- Repository: `mcms-118`
- Distribution package: `mcms-118`
- Python import namespace: `mcms`
- Phase ID: `MCMS-118-P###`
- Phase docs: `docs/phases/phase_###.md`
- Phase metadata: `docs/phase_metadata/phase_###.json`
- Module names: `snake_case.py`
- Tests: `tests/test_<module>.py`

## Claim boundaries

Never convert a symbolic simulation, proposal, computed result, or governance marker into a measured fact without explicit evidence and receipt gates.

Do not add claims of legal compliance, security certification, production customer readiness, medical/clinical value, financial operation readiness, AGI, ASI, or autonomous real-world-action approval.
