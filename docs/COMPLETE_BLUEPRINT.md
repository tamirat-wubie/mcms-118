# MCMS-118 Complete GitHub Blueprint

This repository compiles the MCMS-118 symbolic matter, graph-governance, and release-evidence architecture into GitHub format.

## Included coverage

- Full enriched phase registry: Phase 1 through Phase 135.
- Individual phase documents with frontmatter and detailed metadata: `docs/phases/phase_001.md` through `docs/phases/phase_135.md`.
- Machine-readable per-phase metadata: `docs/phase_metadata/phase_001.json` through `docs/phase_metadata/phase_135.json`.
- Metadata schema: `docs/PHASE_METADATA_SCHEMA.json`.
- Metadata index: `docs/PHASE_METADATA_INDEX.md`.
- Generated module registry: `src/mcms/module_registry.py`.
- Enriched phase registry API: `src/mcms/phase_registry.py`.
- Module scaffolds for Phase 118 through Phase 135: `180` module files under `src/mcms/metabolism/`.
- Executable core modules for maturity, claim boundaries, receipts, and release evidence.
- Release/robust-evidence modules under `src/mcms/release/`.
- Tests and GitHub Actions CI.

## Per-phase metadata fields

Each phase now includes:

- phase identity: `phase`, `phase_id`, `slug`, `title`
- status and maturity ladder
- domain and architectural layer
- objective and capability chain
- keywords
- previous/next phase relationships
- boundary and blocked claims
- invariants
- claim typing contract
- evidence policy
- risk profile and review triggers
- artifacts: docs, metadata JSON, modules, tests, APIs, tables
- module count and status vocabulary
- input/output contracts
- implementation truth
- upgrade path
- audit metadata

## Maturity truth

- Phases 1-117 are blueprint phases with complete metadata contracts.
- Phases 118-135 include generated module files and testable contracts.
- Some modules are conservative scaffolds, not full scientific or production implementations.
- The release-governance core has runnable tests.

## Boundary

No file in this repository claims medical, legal, compliance, security-certification, customer-readiness, financial-operation, or autonomous real-world-action approval.
