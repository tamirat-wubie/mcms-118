# MSPEE-118 Element Engine

## Purpose

MSPEE-118 extends MCMS-118 from a governed release-evidence platform into a governed
symbolic matter platform. The periodic table is treated as a static compression of
matter; MSPEE turns each element into an auditable symbolic object with identity,
laws, state, exposure, and history.

```text
symbolic_element := identity + laws + state + exposure + history
```

The engine does not claim full chemistry prediction, legal certification, production
readiness, or autonomous physical action. It currently provides a Level 1 canonical
seed pack for the first 20 elements.

## Architecture

| Layer | Responsibility | Current implementation |
| --- | --- | --- |
| Identity | Atomic number, symbol, name, proton-count identity | `ElementIdentity` |
| Laws | Charge, isotope, shell-capacity, conservation constraints | `ElementLaws` |
| State | Electron configuration, periodic location, atomic weight model, relation edges | `ElementState` |
| Exposure | Human card, JSON view, graph-node view | `ElementExposure` |
| History | CIAAW/IUPAC and NIST source references, derivation trace, audit marker | `ElementHistory` |
| Receipt | Stable hash plus validation status | `build_element_receipt` |

## Data Levels

| Level | Scope | Status |
| --- | --- | --- |
| Level 1 | Identity, neutral electron configuration, valence signature, period/group/block, atomic weight model, source record | Implemented for Z=1..20 |
| Level 2 | Oxidation states, electronegativity, ionization energy, bond tendency, reaction-family behavior | Planned |
| Level 3 | Isotope distribution, half-life, decay, relativistic effects, magnetism, spectra, solid-state behavior | Planned for elements where it changes meaning |

Level 1 is intentionally narrow. It prevents overclaiming while creating the causal
spine required for later chemistry and physics surfaces.

## Implemented Seed Pack

The first seed pack contains:

```text
H, He, Li, Be, B, C, N, O, F, Ne, Na, Mg, Al, Si, P, S, Cl, Ar, K, Ca
```

Every seed record includes:

1. Canonical MSPEE id, for example `MSPEE-Z001-H`.
2. Proton-count identity rule.
3. Neutral electron count and neutral electron configuration.
4. First-cation configuration when present in the seed record.
5. Period, group, and block.
6. Valence shell and valence electron count.
7. Standard atomic weight model as either a single value or interval.
8. Same-group, same-period, and same-block relation edges.
9. Source references and derivation trace.
10. Validation receipt.

## Algorithm

```text
Input:
  source-backed element seed record

1. Build identity:
   atomic_number, symbol, name, proton_count

2. Attach laws:
   neutral charge, isotope, shell capacity, conservation constraints

3. Build state:
   neutral electron count, electron configuration, periodic location,
   valence signature, atomic weight model

4. Build relation graph:
   same group, same period, same block

5. Validate:
   identity equals proton count
   neutral electron count equals atomic number
   weight model is typed
   relation edges are non-self edges
   source references include CIAAW/IUPAC and NIST

6. Emit:
   JSON object, human view, graph node, validation receipt
```

## CLI

```powershell
python -m mcms.cli elements
python -m mcms.cli elements --list
python -m mcms.cli elements --symbol H
python -m mcms.cli elements --symbol 20
```

## Validation

The repository verifier now checks the MSPEE seed pack:

```powershell
python scripts/verify_repo.py
python -m pytest tests/test_symbolic_elements.py -q
```

The seed pack is valid only when:

1. It contains exactly Z=1..20 in order.
2. Every element validates with no governance errors.
3. Source references include CIAAW/IUPAC and NIST.
4. Relation edges exist and are typed.

## Constructive Deltas

| Delta | Result |
| --- | --- |
| Static table cell -> symbolic object | Element records now carry identity, laws, state, exposure, and history |
| Atomic weight constant -> typed model | Interval weights stay intervals and single weights stay single values |
| Position-only table -> relation graph | Elements now expose same-group, same-period, and same-block edges |
| Unchecked data -> validation receipt | Every exposed seed can emit a stable hash and validation status |

## Fracture Deltas Avoided

| Risk | Guard |
| --- | --- |
| Confusing ion state with element identity | Electron count changes do not mutate proton-count identity |
| Collapsing atomic-weight intervals | Interval values are stored with lower and upper bounds |
| Inferring unsupported chemistry behavior | Level 2 properties are not claimed by Level 1 seeds |
| Treating generated data as source authority | History records cite source authorities and derivation trace |

## Source Boundary

The seed implementation uses these authority anchors:

1. CIAAW/IUPAC Standard Atomic Weights 2024: `https://www.ciaaw.org/atomic-weights.htm`
2. NIST Electronic Configurations of the Elements:
   `https://www.nist.gov/pml/atomic-reference-data-electronic-structure-calculations/atomic-reference-data-electronic-8`

## Next Expansion

1. Add Level 2 chemical behavior fields for the first 20 elements.
2. Add deterministic import tooling for the full 118-element source pack.
3. Add JSON schema export for `MulluStandardSymbolicElement`.
4. Add graph export for element relation queries.
5. Add source drift checks that compare local seed records against pinned source snapshots.
