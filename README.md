# MCMS-118 — Causal Matter Standard

**Repository:** `mcms-118`
**Python package:** `mcms-118`
**Import namespace:** `mcms`
**CLI:** `mcms`
**License:** `Apache-2.0`
**Version:** `0.1.0`

MCMS-118 is a GitHub-ready symbolic matter standard and governed release-evidence engine.
It treats every entity, claim, receipt, edge, artifact, and release decision as a governed symbolic object:

```text
𝕊ˣ := ⟨ Ιˣ, Λˣ, Σˣ, Γˣ, Hˣ ⟩
Ι = identity
Λ = laws / rules
Σ = state
Γ = interface / exposure
H = history / provenance / audit
```

## Boundary

This repository is engineering and symbolic-governance work. It does **not** claim legal compliance, security certification, production customer readiness, medical/clinical value, financial-operation readiness, autonomous real-world action approval, cognition, biological memory, AGI, or ASI.

## What is included

```text
src/mcms/core/
  maturity ladder
  claim boundary compiler
  receipt/hash-chain utilities
  phase registry helpers
  naming and standards helpers

src/mcms/release/
  release evidence bundle
  adapter sandbox policy
  HTTP retry/backoff policy
  GitHub pagination/ETag helper
  JSONSchema binding wrapper
  SARIF severity taxonomy
  signed waiver entries
  compressed evidence archive
  environment snapshot replay
  robust evidence network

src/mcms/elements/
  MSPEE-118 symbolic element contracts
  first-36 canonical element seed pack
  full 118-element identity/weight source snapshot
  source-backed element validation receipts
  same-group / same-period / same-block relation edges

src/mcms/metabolism/
  generated module contracts for Phases 118-135

docs/
  phase registry through Phase 135
  per-phase metadata JSON
  per-phase markdown docs
  naming standard
  standards profile
  architecture
  evidence standard
  release policy
  boundaries
  roadmap
  GitHub push guide
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python scripts/verify_repo.py
python -m pytest
python -m mcms.cli demo
python -m mcms.cli elements --symbol H
python -m mcms.cli elements --full --symbol Og
python -m mcms.cli elements --schema bundle
python scripts/check_element_snapshot_drift.py --fail-on-drift
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e '.[dev]'
python scripts/verify_repo.py
python -m pytest
python -m mcms.cli demo
python -m mcms.cli elements --symbol H
python -m mcms.cli elements --full --symbol Og
python -m mcms.cli elements --schema bundle
python scripts/check_element_snapshot_drift.py --fail-on-drift
```

## Push to GitHub

```bash
git init
git add .
git commit -m "initial MCMS-118 standard scaffold"
git branch -M main
git remote add origin https://github.com/tamirat-wubie/mcms-118.git
git push -u origin main
```

See `docs/PUSH_TO_GITHUB.md` for safer step-by-step instructions.

## Recommended first product slice

```text
Chemistry claim input
MSPEE element lookup
→ claim boundary compiler
→ evidence classification
→ receipt generation
→ local persistence
→ signed receipt
→ dashboard card
→ blocked-claim examples
```

## Metadata completeness

The package includes important data and metadata for every phase:

```text
docs/PHASE_REGISTRY.json
docs/phase_metadata/phase_001.json ... phase_135.json
docs/phases/phase_001.md ... phase_135.md
docs/PHASE_METADATA_SCHEMA.json
docs/PHASE_METADATA_INDEX.md
docs/MSPEE_ELEMENT_ENGINE.md
```

Each phase record includes identity, domain, layer, capability chain, previous/next links, artifacts, modules, tests, API endpoints, data tables, status vocabulary, evidence policy, blocked claims, invariants, risk profile, implementation truth, upgrade path, canonical project identity, and standards profile.
