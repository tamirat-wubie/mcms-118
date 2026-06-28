# MSPEE-118 Element Engine

## Purpose

MSPEE-118 is a standalone periodic-table element engine. It turns each element
into an auditable element record with identity, laws, state, exposure, and
history.

```text
element_record := identity + laws + state + exposure + history
```

The engine does not claim full chemistry prediction, legal certification, production
readiness, or autonomous physical action. It currently provides a Level 1 canonical
seed pack for the first 36 elements, sourced Level 2 oxidation-state and Pauling
electronegativity values for the first 36 elements, and an identity/weight source
snapshot for all 118 named elements.

## Architecture

| Layer | Responsibility | Current implementation |
| --- | --- | --- |
| Identity | Atomic number, symbol, name, proton-count identity | `ElementIdentity` |
| Laws | Charge, isotope, shell-capacity, conservation constraints | `ElementLaws` |
| State | Electron configuration, frontier signature, configuration audit, periodic location, atomic weight model, relation edges | `ElementState` |
| Exposure | Human card, JSON view, graph-node view | `ElementExposure` |
| History | CIAAW/IUPAC and NIST source references, derivation trace, audit marker | `ElementHistory` |
| Receipt | Stable hash plus validation status | `build_element_receipt` |

## Data Levels

| Level | Scope | Status |
| --- | --- | --- |
| Snapshot | Identity, periodic position, CIAAW atomic-weight display, source status | Implemented for Z=1..118 |
| Level 1 | Identity, neutral electron configuration, valence signature, period/group/block, atomic weight model, source record | Implemented for Z=1..36 |
| Level 2 | Oxidation states, electronegativity, ionization energy, transition frontier, configuration audit, bond tendency, reaction-family behavior | Oxidation-state, Pauling electronegativity, first-ionization-energy, PubChem GroupBlock-derived bond tendency, transition frontier, and configuration-audit values implemented for Z=1..36 |
| Level 3 | Isotope distribution, half-life, decay, relativistic effects, magnetism, spectra, solid-state behavior | Planned for elements where it changes meaning |

The 118-element snapshot is intentionally narrower than Level 1. It prevents
overclaiming while creating the causal spine required for later chemistry and
physics surfaces.

## Implemented Seed Pack

The first seed pack contains:

```text
H, He, Li, Be, B, C, N, O, F, Ne, Na, Mg, Al, Si, P, S, Cl, Ar, K, Ca,
Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Cu, Zn, Ga, Ge, As, Se, Br, Kr
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
10. Phase 2 frontier signature and configuration audit for Z=21..36.
11. Validation receipt.

Elements H through Kr also include a partial Level 2 promotion:

1. PubChem oxidation-state set.
2. PubChem Pauling electronegativity value when the source publishes one.
3. PubChem first-ionization-energy value in electronvolts.
4. PubChem `GroupBlock`-derived bond-tendency tags.
5. PubChem source reference in the element history.

He, Ne, and Ar carry PubChem `0` oxidation state and no electronegativity value
because the source leaves the electronegativity cell blank. Kr carries PubChem
`0` oxidation state and a Pauling electronegativity value.

D-block Level 1 records use the `(n-1)d ns` valence signature and allow up to 12
tracked valence electrons. This keeps transition-metal structure explicit without
collapsing d-block behavior into the s/p-block rule.

## Phase 2 Transition Exception Kernel

Phase 2 adds the first transition-metal behavior boundary. It keeps the simple
main-group rule separate from the d-block rule:

```text
main_group_frontier := outer shell mostly determines behavior
transition_frontier := outer ns + inner (n-1)d jointly shape behavior
```

The `ElementState` contract now includes:

| Field | Meaning |
| --- | --- |
| `frontier_signature.outer_shell` | Outer shell contribution, for example `4s^1` or `4s^2 4p^5` |
| `frontier_signature.d_shell` | Inner d-shell contribution when present, for example `3d^5` |
| `frontier_signature.p_shell` | Period-4 p-shell contribution when present |
| `frontier_signature.valence_model` | `transition_metal`, `period_4_p_block_d_core`, or `main_group` |
| `frontier_signature.d_shell_stability` | `open_d_shell`, `half_filled_d_shell`, or `filled_d_shell` |
| `configuration_audit.source_backed_configuration` | NIST-backed neutral configuration used as authority |
| `configuration_audit.simple_aufbau_candidate` | Simple filling candidate retained for audit comparison |
| `configuration_audit.is_exception` | True when candidate and source-backed configuration conflict |
| `transition_behavior_kernel.*` | Capability relevance flags, not universal compound claims |

Chromium and copper are formal exception anchors:

| Element | Simple candidate | Source-backed state | Exception reason |
| --- | --- | --- | --- |
| Cr | `[Ar] 3d^4 4s^2` | `[Ar] 3d^5 4s^1` | half-filled d-shell stabilization pattern |
| Cu | `[Ar] 3d^9 4s^2` | `[Ar] 3d^10 4s^1` | filled d-shell stabilization pattern |

For Sc through Zn, validation requires a transition frontier signature with an
explicit d-shell and a transition behavior kernel. For Ga through Kr, validation
requires the filled `3d^10` core to remain present in the frontier signature even
though the active outer shell is `4s 4p`.

## Level 2 Boundary Fields

The element state contract now includes Level 2 boundary fields and sourced partial
Level 2 chemistry values for H through Kr:

| Field | Boundary |
| --- | --- |
| `oxidation_states` | Unique integers in `[-8, 9]`; populated from PubChem for Z=1..36, empty for unpromoted Level 1 records |
| `electronegativity_scale` | `null` or `pauling` |
| `electronegativity_value` | `null` or number in `[0.0, 5.0]`; populated from PubChem when available |
| `electronegativity_source_key` | Required when electronegativity value is present |
| `first_ionization_energy_ev` | `null` or number in `[0.0, 30.0]`; populated from PubChem for Z=1..36 |
| `first_ionization_energy_source_key` | Required when first ionization energy value is present |
| `bond_tendency_tags` | Controlled tag list derived from PubChem `GroupBlock` for Z=1..36 |
| `bond_tendency_source_key` | Required when bond tendency tags are present |

Electronegativity is accepted only as a complete sourced tuple: scale, value, and
source key must all be present together or all be absent. Oxidation states are
source-backed through the element history. First ionization energy is accepted only
as a complete sourced value/source-key pair. Bond tendency is accepted only as a
controlled, duplicate-free tag list with a source key. Current bond-tendency tags
are element-class classifications derived from PubChem `GroupBlock`; they are not
compound-specific reaction predictions. The JSON Schema export and Python
validator enforce the same boundaries.

## Full Source Snapshot

The full snapshot contains all elements Z=1..118. It stores canonical identity,
periodic position, CIAAW atomic-weight display, source keys, and snapshot status.
Elements that do not have a CIAAW standard atomic weight use:

```text
atomic_weight_model.model_type = "unavailable"
```

This includes radioactive and superheavy elements where a standard atomic weight is
not published. The snapshot does not invent electron configurations, oxidation
states, isotope distributions, or reaction behavior for elements not yet promoted
to Level 1 or higher.

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
   valence signature, frontier signature, configuration audit, atomic weight model

4. Build relation graph:
   same group, same period, same block

5. Validate:
   identity equals proton count
   neutral electron count equals atomic number
   weight model is typed
   valence count is within the block-specific Level 1 bound
   Level 2 fields stay inside oxidation, electronegativity, first-ionization-energy,
   and bond-tendency boundaries
   first-36 Level 2 records carry PubChem lineage
   d-block records carry transition frontier and behavior kernel
   Cr and Cu carry configuration exception audits
   period-4 p-block records preserve filled 3d-core context
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
python -m mcms.cli elements --full --list
python -m mcms.cli elements --full --symbol Og
python -m mcms.cli elements --schema seed
python -m mcms.cli elements --schema snapshot
python -m mcms.cli elements --schema bundle
python -m mcms.cli elements --graph
python -m mcms.cli elements --graph --symbol Zn --relation same_block
python -m mcms.cli elements --dashboard --symbol Zn --relation same_block
python -m mcms.cli api --host 127.0.0.1 --port 8765
```

## Validation

The repository verifier now checks the MSPEE seed pack and full snapshot shape:

```powershell
python scripts/verify_repo.py
python -m pytest tests/test_symbolic_elements.py -q
python -m pytest tests/test_element_snapshot_drift.py -q
```

The seed pack is valid only when:

1. It contains exactly Z=1..36 in order.
2. Every element validates with no contract errors.
3. Source references include CIAAW/IUPAC and NIST.
4. Relation edges exist and are typed.
5. First-36 Level 2 chemistry records validate and carry PubChem lineage.
6. Phase 2 records carry frontier signatures and configuration audits.
7. Chromium and copper are marked as configuration exceptions.

The full snapshot is valid only when:

1. It contains exactly Z=1..118 in order.
2. Every record validates identity, position, weight model, and source keys.
3. Unavailable atomic weights are explicit.
4. The first 36 snapshot records link to available Level 1 seed records.

## JSON Schema Export

The element engine exports JSON Schema Draft 2020-12 contracts for both Level 1
seed records and full snapshot records. The schemas are explicit contracts, not
reflection output, and set `additionalProperties = false` for element payloads.

| Schema | CLI command | Contract |
| --- | --- | --- |
| Seed element | `python -m mcms.cli elements --schema seed` | `MulluStandardSymbolicElement` |
| Snapshot record | `python -m mcms.cli elements --schema snapshot` | `ElementSourceSnapshotRecord` |
| Bundle | `python -m mcms.cli elements --schema bundle` | Both schemas in one document |

The repository verifier validates the schemas and representative records:

```powershell
python scripts/verify_repo.py
python -m pytest tests/test_element_schemas.py -q
```

## Relation Graph Export

The element engine exports Level 1 relation graphs from declared same-group,
same-period, and same-block edges. Graph export is source-bounded to seed records;
snapshot-only elements are not assigned inferred graph edges.

| Query | Command | Result |
| --- | --- | --- |
| Full Level 1 graph | `python -m mcms.cli elements --graph` | All seed nodes and declared edges |
| Element graph | `python -m mcms.cli elements --graph --symbol Zn` | Zinc plus directly related target nodes |
| Typed relation graph | `python -m mcms.cli elements --graph --symbol Zn --relation same_block` | Zinc d-block neighborhood |

The repository verifier checks the Zinc same-block graph query, and focused graph
tests cover full graph export, filtered export, rejection of unknown relation
types, and CLI JSON output.

## Local API

The local API is a read-only JSON surface over the same deterministic element,
snapshot, schema, and graph functions used by the CLI. It uses the Python standard
library HTTP server and introduces no runtime web-framework dependency.

Start it with:

```powershell
python -m mcms.cli api --host 127.0.0.1 --port 8765
```

Routes:

| Route | Result |
| --- | --- |
| `GET /health` | API status, seed count, snapshot count |
| `GET /elements` | Level 1 seed symbols and validation summary |
| `GET /elements/{symbol}` | Seed element payload and receipt |
| `GET /snapshot` | Full snapshot symbols and validation summary |
| `GET /snapshot/{symbol}` | Snapshot record payload and receipt |
| `GET /schemas/{seed\|snapshot\|bundle}` | JSON Schema export |
| `GET /graph` | Full Level 1 relation graph |
| `GET /graph?symbol=Zn&relation=same_block` | Filtered graph query |
| `GET /dashboard` | Dashboard-facing overview payload |
| `GET /dashboard?symbol=Zn&relation=same_block` | Selected element dashboard payload |

Unknown routes, unknown symbols, invalid relation types, and non-GET methods
return explicit JSON error payloads.

## Dashboard View Model

The dashboard view model composes seed health, snapshot health, selected element
or snapshot cards, schema cards, graph context, and API/CLI actions into one JSON
payload for a future dashboard surface.

| Query | Command | Result |
| --- | --- | --- |
| Overview | `python -m mcms.cli elements --dashboard` | Seed/snapshot summaries, schemas, full graph context |
| Selected seed element | `python -m mcms.cli elements --dashboard --symbol Zn --relation same_block` | Zinc card plus d-block graph |
| Snapshot-only element | `python -m mcms.cli elements --dashboard --symbol Og` | Oganesson snapshot card and explicit unavailable graph state |

The dashboard view is a projection. It does not mutate element, snapshot, schema,
or graph records.

Selected seed-element cards include the Phase 2 frontier signature,
configuration audit, and transition behavior kernel when the selected element has
that layer.

## Source Drift Check

The snapshot has an explicit CIAAW drift checker. The checker compares the local
atomic number, symbol, name, and atomic-weight display against the source table
and emits JSON with a deterministic drift status.

```powershell
python scripts/check_element_snapshot_drift.py --fail-on-drift
```

The partial Level 2 chemistry layer has a separate PubChem drift checker. It
compares promoted local oxidation-state, electronegativity, first-ionization-energy,
and GroupBlock-derived bond-tendency values against the PubChem periodic-table CSV
without mutating seed records.

```powershell
python scripts/check_element_level2_drift.py --fail-on-drift
```

Fixture mode supports offline review and CI-safe parser tests:

```powershell
python scripts/check_element_snapshot_drift.py --fixture-html path\to\ciaaw.html --fail-on-drift
python scripts/check_element_level2_drift.py --fixture-csv path\to\pubchem.csv --fail-on-drift
```

Drift statuses:

| Status | Meaning |
| --- | --- |
| `element_snapshot_no_drift` | Local snapshot matches the parsed source rows |
| `element_snapshot_drift_detected` | At least one source/local field differs or a required row is missing |
| `element_snapshot_source_unavailable` | The source could not be read; no local mutation was attempted |
| `element_level_2_chemistry_no_drift` | Local promoted Level 2 chemistry fields match parsed PubChem source rows |
| `element_level_2_chemistry_drift_detected` | At least one promoted Level 2 field differs or a required source row is missing |
| `element_level_2_chemistry_source_unavailable` | The PubChem source could not be read or parsed; no local mutation was attempted |

## Constructive Deltas

| Delta | Result |
| --- | --- |
| Static table cell -> symbolic object | Level 1 records now carry identity, laws, state, exposure, and history |
| Partial seed pack -> full source snapshot | All 118 element identities are now queryable |
| Atomic weight constant -> typed model | Interval weights stay intervals and single weights stay single values |
| Position-only table -> relation graph | Elements now expose same-group, same-period, and same-block edges |
| Unchecked data -> validation receipt | Every exposed seed can emit a stable hash and validation status |
| Static source snapshot -> drift-checkable source boundary | CIAAW source changes now produce explicit drift reports |
| Sourced Level 2 values -> drift-checkable chemistry boundary | PubChem source changes now produce explicit Level 2 drift reports |
| Python object contract -> JSON Schema contract | Seed and snapshot records can now be exported and externally validated |
| Embedded relation edges -> graph export | Element relation queries now produce deterministic node and edge payloads |
| CLI-only surface -> local API surface | Element lookup, schemas, and graph queries now have read-only JSON routes |
| Raw API routes -> dashboard view model | Dashboard consumers now get one composed read-only payload |
| Planned Level 2 fields -> bounded contract | Oxidation-state and electronegativity fields now reject invalid values |
| Bounded Level 2 fields -> sourced first-36 values | H through Kr now carry PubChem-backed oxidation-state, electronegativity, first-ionization-energy, and GroupBlock-derived bond-tendency values |
| Planned bond fields -> source-classified boundary | Bond-tendency tags now derive from PubChem GroupBlock classes and remain non-reaction predictions |
| Simple Aufbau output -> configuration audit | Cr and Cu store both simple candidates and NIST-backed corrected states |
| Outer-shell-only transition rule -> frontier kernel | Sc through Zn now expose outer ns plus inner 3d structure |
| Period-4 p-block shell view -> filled d-core context | Ga through Kr preserve `3d^10` behind the `4s 4p` frontier |

## Fracture Deltas Avoided

| Risk | Guard |
| --- | --- |
| Confusing ion state with element identity | Electron count changes do not mutate proton-count identity |
| Collapsing atomic-weight intervals | Interval values are stored with lower and upper bounds |
| Inferring unsupported chemistry behavior | Level 2 properties are not claimed by Level 1 seeds |
| Treating generated data as source authority | History records cite source authorities and derivation trace |
| Silent Aufbau failure | Candidate/source conflict is stored as a configuration exception |
| Flattening d-block elements into one family | Frontier signatures distinguish open, half-filled, and filled d-shell states |
| Claiming universal magnetism or catalysis | Transition behavior fields are relevance flags, not guaranteed compound behavior |

## Source Boundary

The seed implementation uses these authority anchors:

1. CIAAW/IUPAC Standard Atomic Weights 2024: `https://www.ciaaw.org/atomic-weights.htm`
2. NIST Electronic Configurations of the Elements:
   `https://www.nist.gov/pml/atomic-reference-data-electronic-structure-calculations/atomic-reference-data-electronic-8`
3. PubChem Periodic Table of Elements CSV:
   `https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV`

## Next Expansion

1. MSPEE-118 Phase 3: Lanthanide-Actinide Expansion Kernel.
2. Add f-orbital behavior, lanthanide contraction, radioactive decay handling,
   actinide instability, nuclear-state extension, heavy-element uncertainty, and
   relativistic-effect flags.
3. Continue sourced Level 2 chemistry values beyond Krypton.
