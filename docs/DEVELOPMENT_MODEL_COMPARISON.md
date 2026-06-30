# Development Model Comparison

## Purpose

This document compares the original GPT sandbox development style with the
current repository development style. It defines how sandbox phase documents are
used without confusing vision, roadmap, and implemented truth.

## Simple Summary

The sandbox thread was best at invention:

```text
big concept
-> broad phase map
-> future engines
-> example reasoning
-> MVP sketch
```

The repository workflow is best at closure:

```text
small verified slice
-> typed model
-> source-backed evidence
-> tests
-> CLI/API route
-> verifier receipt
-> documentation update
```

Both are useful, but they must not be mixed.

## Comparison

| Area | GPT sandbox style | Current repository style | Adjustment |
| --- | --- | --- | --- |
| Strength | Fast architecture and phase imagination | Verified implementation and source governance | Use sandbox pages as design backlog, not proof |
| Scope | Wide: elements, reactions, compounds, materials, search, learning, UI | Narrow: element engine first, evidence gaps explicit | Keep near-term work inside element/evidence boundary |
| Evidence | Often references authorities conceptually | Requires local source record, test, drift check, or unresolved receipt | Promote only when evidence is represented in code |
| Output | Strong explanatory documents and examples | Runnable Python package, CLI/API, pytest, verifier | Convert useful examples into tests before claiming support |
| Risk | Can overstate future phases as if already built | Can move slower but preserves correctness | Use roadmap labels: planned, modeled, implemented, verified |
| Missing data | Usually described as future source need | Stored as unresolved receipts and gap policies | Continue no-guess policy |
| Product direction | Full matter engine vision | Standalone periodic-table engine first | Treat matter engine as later expansion after elements stabilize |

## What The Sandbox Got Right

The sandbox thread correctly identified the deeper trajectory:

```text
periodic table
-> element objects
-> comparison
-> reactions
-> compounds
-> materials
-> search
-> learning/planning
-> graph memory
-> API/UI
```

It also identified the right first-principles separations:

```text
element identity != electron state
element identity != isotope state
compound formula != full compound behavior
composition != material state
measured property != symbolic inference
missing evidence != false value
```

Those principles remain valid.

## What The Repository Corrected

The repository corrected the main weakness of the sandbox path: breadth without
enough implementation gates.

Current rule:

```text
planned phase != implemented capability
implemented function != verified capability
verified local data != universal scientific truth
```

Every promoted capability should have:

```text
1. typed model
2. source or explicit unresolved status
3. validation function
4. tests
5. CLI/API exposure when useful
6. verifier coverage
7. documentation update
```

## Intake Gate For Future Sandbox Phases

Every sandbox phase must pass this gate before becoming repository work:

| Gate | Question | Required result |
| --- | --- | --- |
| Boundary | What exact object is being added? | Element, ion, isotope, compound, reaction, material, query, or receipt |
| Source | What authority backs measured facts? | Source key, version, URL/citation, or unresolved receipt |
| Model | What typed record is needed? | Dataclass/schema fields and invariants |
| Non-claim | What must the engine not claim? | Explicit limits and blocked claims |
| Validation | What makes the record valid? | Validator and focused tests |
| Exposure | How is it inspected? | CLI/API/dashboard route if useful |
| Verifier | How does closure show up? | `scripts/verify_repo.py` count or assertion |

If a phase cannot pass this gate, it stays roadmap-only.

## Immediate Adjustment

The next development path should not jump directly to the full reaction,
compound, material, learning, or UI phases from the sandbox documents.

The safer trajectory is:

```text
1. Finish source governance for element gaps.
2. Complete Cs-Rn Level 1 promotion when At is resolved.
3. Extend source-backed element records toward all 118.
4. Add computable comparison over verified element fields.
5. Add simple reaction/compound layers only after element evidence is stable.
6. Move to material/search/learning/UI after compound and reaction boundaries exist.
```

## Current Decision

The sandbox documents are accepted as:

```text
vision source
architecture source
roadmap source
example source
```

They are not accepted as:

```text
implemented capability
measured evidence
source authority
test proof
production readiness
```

## Status

```text
development_model = adjusted
sandbox_role = design_backlog
repository_role = verified implementation
next_gate = source-specific secondary evidence receipt for At boiling point
```
