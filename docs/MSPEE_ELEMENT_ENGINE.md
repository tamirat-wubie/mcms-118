# MSPEE-118 Element Engine

## Purpose

MSPEE-118 is a standalone periodic-table element engine. It turns each element
into an auditable element record with identity, laws, state, exposure, and
history.

Project lineage and historical corrections are recorded in `docs/PROJECT_HISTORY.md`.
The first-principles symbolic foundation is recorded in
`docs/SYMBOLIC_CAUSAL_FOUNDATION.md`.

```text
element_record := identity + laws + state + exposure + history
```

The engine does not claim full chemistry prediction, legal certification, production
readiness, or autonomous physical action. It currently provides a Level 1 canonical
seed pack for the first 54 elements, sourced Level 2 oxidation-state and Pauling
electronegativity values for the first 54 elements, and an identity/weight source
snapshot for all 118 named elements. It also provides Phase 3 f-block expansion
profiles for lanthanides and actinides as bounded relevance and uncertainty flags,
plus a period-5 Level 2 chemistry profile projection for Rb through Xe and a
Cs-Rn Level 1 promotion-readiness audit layer with NIST configuration evidence,
frontier/valence signatures, PubChem oxidation-state evidence, behavior tags,
relation edges, and promotion decision receipts.
The selected batch policy holds the full Cs-Rn span until Astatine has complete
physical-property evidence, preserving the contiguous Level 1 seed invariant.

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
| Level 1 | Identity, neutral electron configuration, valence signature, period/group/block, atomic weight model, source record | Implemented for Z=1..54 |
| Level 2 | Oxidation states, electronegativity, ionization energy, transition frontier, configuration audit, bond tendency, reaction-family behavior | Seed-level values implemented for Z=1..54; period-5 PubChem profile projection implemented for Z=37..54 |
| Level 3 | Isotope distribution, half-life, decay, relativistic effects, magnetism, spectra, solid-state behavior | Phase 3 f-block relevance flags implemented; exact isotope, half-life, spectra, and solid-state values remain planned |
| Atom behavior v2 | Source-backed atom profiles binding proton identity, neutron isotope state, electron charge state, force context, and matter-profile tags | Implemented for H-Zn isotope evidence records, 79 profiles |
| Atom behavior gaps | No-guess source-gap receipts and work items for missing atom behavior coverage | Implemented for 88 unresolved isotope-evidence elements |
| Readiness scoring | Deterministic score records for evidence completeness, source confidence, behavior readiness, gap priority, and constraint tension | Implemented for all 118 snapshot elements; scores do not close gaps |
| Isotope source policy | Admission rules for isotope evidence needed by atom behavior v2 isotope-only gaps | Implemented for 24 Level 1 blockers; policy alone closes zero gaps |
| Isotope source search | Evidence-collection receipts for isotope-only atom behavior blockers | Implemented for 24 Level 1 blockers; zero active candidate receipts |
| Isotope candidate evidence | Source-specific isotope rows collected before admission | No active candidate receipts after Oxygen admission; templates remain available for unresolved blockers |
| Isotope candidate admission | Historical audit receipt for canonical isotope admission | Oxygen admission receipt links the closed candidate to O-16/O-17/O-18 canonical evidence |
| Promotion readiness | Evidence-gap audit before promoting snapshot-only records | Implemented for Cs-Rn, Z=55..86 |
| Configuration evidence | Neutral and first-cation electronic configurations | Implemented for Cs-Rn, Z=55..86 |
| Frontier/valence overlay | Outer shell, inner d/f participation, p-shell context, and shell-stability flags | Implemented for Cs-Rn, Z=55..86 |
| Oxidation-state evidence | PubChem oxidation-state set and GroupBlock class | Implemented for Cs-Rn, Z=55..86 |
| Behavior tags | Controlled symbolic inference from source-backed configuration, frontier, and oxidation evidence | Implemented for Cs-Rn, Z=55..86 |
| Relation overlay | Same-position and shared-evidence relation edges | Implemented for Cs-Rn, Z=55..86 |
| Promotion decisions | Readiness-to-approval receipts before seed mutation | Implemented for Cs-Rn, Z=55..86 |
| Promotion batch policy | Span-level decision over partial versus full promotion | Implemented for Cs-Rn, Z=55..86 |

The 118-element snapshot is intentionally narrower than Level 1. It prevents
overclaiming while creating the causal spine required for later chemistry and
physics surfaces.

The period-5 Level 2 profiles remain available as a compact PubChem chemistry
projection, but Rb through Xe are now also promoted into full Level 1 seed records.

## Implemented Seed Pack

The first seed pack contains:

```text
H, He, Li, Be, B, C, N, O, F, Ne, Na, Mg, Al, Si, P, S, Cl, Ar, K, Ca,
Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Cu, Zn, Ga, Ge, As, Se, Br, Kr,
Rb, Sr, Y, Zr, Nb, Mo, Tc, Ru, Rh, Pd, Ag, Cd, In, Sn, Sb, Te, I, Xe
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
10. Frontier signature and configuration audit for Z=21..54.
11. Validation receipt.

Elements H through Xe also include a partial Level 2 promotion:

1. PubChem oxidation-state set.
2. PubChem Pauling electronegativity value when the source publishes one.
3. PubChem first-ionization-energy value in electronvolts.
4. PubChem `GroupBlock`-derived bond-tendency tags.
5. PubChem source reference in the element history.

He, Ne, and Ar carry PubChem `0` oxidation state and no electronegativity value
because the source leaves the electronegativity cell blank. Kr and Xe carry
PubChem `0` oxidation state and Pauling electronegativity values.

D-block Level 1 records use the `(n-1)d ns` valence signature and allow up to 12
tracked valence electrons. This keeps transition-metal structure explicit without
collapsing d-block behavior into the s/p-block rule.

## Ion and Isotope State Instances

Ion and isotope records are derived state instances. They do not replace the
element seed or snapshot record, and they do not change proton-count identity.

Canonical examples:

```text
MSPEE-Z011-Na-ion-plus-1
MSPEE-Z017-Cl-ion-minus-1
MSPEE-Z006-C-isotope-14
```

Validation applies the first-principles laws directly:

```text
ion_electron_count = atomic_number - charge
neutron_count = mass_number - atomic_number
```

Ion instances require a promoted Level 1 seed record because they retain the
source-backed neutral electron configuration as context. Isotope instances can be
derived from the 118-element identity snapshot because isotope identity only needs
atomic number, symbol, mass number, and neutron count at this layer. Abundance,
half-life, decay mode, and isotope-specific mass evidence remain separate future
evidence fields.

## Isotope and Common-Ion Evidence Seeds

The engine now includes a bounded evidence layer over state instances.

Isotope evidence seed:

```text
H-1, H-2, C-12, C-13, C-14
```

Each isotope evidence record includes:

| Field | Meaning |
| --- | --- |
| `isotope_id` | Canonical isotope instance ID |
| `relative_atomic_mass` | Source-backed isotope mass display |
| `isotopic_composition` | Source-backed isotopic composition when applicable |
| `half_life_value` / `half_life_unit` | Present only for radioisotope evidence |
| `decay_mode` | Present only for radioisotope evidence |
| `source_keys` | Source lineage for the evidence fields |

Common-ion evidence seed:

```text
Na+, Mg2+, Cl-, Ca2+, Fe2+, Fe3+, Cu+, Cu2+, Zn2+
```

Common-ion records are deliberately labeled as `common_ion_candidate_evidence`.
They require the charge to exist in the sourced PubChem oxidation-state set for
the element. This is not a guarantee that every compound or condition stabilizes
that ion.

Unresolved receipts are also generated for evidence domains that are not yet
fully sourced:

```text
unresolved isotope evidence: 88 snapshot elements outside the H-Zn isotope seed
unresolved common-ion evidence: 47 Level 1 seed elements outside the common-ion seed
```

These receipts make missing evidence queryable without inventing isotope tables
or common-ion stability claims.

## Physical-Property Evidence Seed

Measured physical properties are stored separately from symbolic behavior tags.
The physical-property evidence layer stores complete PubChem measured-property
rows separately from unresolved rows:

```text
complete physical-property evidence: 93 records
unresolved physical-property evidence: 25 records
```

Each record carries:

| Field | Meaning |
| --- | --- |
| `standard_state` | PubChem standard-state class: `Gas`, `Liquid`, or `Solid` |
| `melting_point_k` | Melting point in kelvin |
| `boiling_point_k` | Boiling point in kelvin |
| `density_value` | PubChem density value |
| `density_unit` | `g/cm^3` |
| `source_keys` | Source lineage for measured fields |

Validation requires positive numeric values and `melting_point_k < boiling_point_k`.
This layer is evidence, not inference. For example, bromine's liquid standard
state is stored as measured/reference evidence rather than as a behavior tag.
Arsenic is preserved with a phase-transition note because PubChem's listed
melting and boiling values violate simple ordering; the engine records the source
evidence rather than silently normalizing it. Astatine and other incomplete rows
are stored as unresolved physical-property evidence receipts instead of guessed
measured values.

Physical-property gap audit receipts sit on top of those unresolved rows. They
record which source fields are blank, whether the gap blocks a promotion span,
and the no-guess policy for the missing value. Astatine's PubChem row still has a
blank `BoilingPoint`, so `MSPEE-PHYSICAL-PROPERTY-GAP-Z085-At` blocks full Cs-Rn
seed promotion.

The secondary-source policy layer defines how gaps may be reviewed against
candidate sources. It does not import values, close gaps, or allow seed mutation
by itself.

The secondary evidence receipt workflow defines the exact source-specific receipt
shape needed to admit a missing field. It currently contains one At LANL candidate
receipt, zero admitted receipts, and a template for At `boiling_point_k`.

The LANL candidate has an admission decision of
`secondary_evidence_not_admitted_conflict`, because accessible secondary sources
do not fully agree on the At boiling point.

## Matter-Behavior Profiles

Matter-behavior profiles are the first layer that combines element identity,
symbolic state, and measured evidence into a bounded matter-facing read model.

Implemented profile coverage remains bounded to elements with full Level 1
symbolic state:

```text
H through Xe, Z=1..54
```

Profile inputs are explicit:

| Input class | Examples |
| --- | --- |
| Identity/state | `atomic_number`, `block`, `group`, `period`, `valence_shell` |
| Measured evidence | `standard_state`, `melting_point_k`, `boiling_point_k`, `density` |
| Symbolic inference | `standard_state_liquid`, `low_boiling_boundary`, `high_density_boundary` |

Profiles declare non-claims:

```text
does not predict reactions
does not model compounds
does not replace condition-specific measured data
```

This is the first matter-behavior layer, but it is still a profile/read-model
layer, not a simulator.

## Atom Behavior V2

Atom behavior v2 is the first additive layer that turns an explicit isotope
record into a single atom profile. It does not mutate element seeds, snapshot
records, isotope evidence, or matter profiles.

Implemented profile coverage is bounded to existing source-backed isotope
evidence:

```text
H-1, H-2, C-12, C-13, C-14
```

Each profile validates:

| Rule | Contract |
| --- | --- |
| Element identity | `proton_count = atomic_number` |
| Isotope state | `mass_number = proton_count + neutron_count` |
| Charge state | `electron_count = atomic_number - charge` |
| Electron behavior | neutral configuration remains source-backed context |
| Nuclear behavior | stable isotope composition or radioisotope half-life/decay evidence |
| Force context | strong, electromagnetic, weak-decay, and atom-scale gravity boundaries |

Profiles declare non-claims:

```text
does not solve electron wavefunctions
does not predict reactions
does not replace isotope-specific laboratory data
does not claim complete quantum simulation
```

Atom behavior gap receipts make missing coverage explicit. They are derived from
unresolved isotope evidence records and do not create isotope values. The current
gap split is:

| Gap class | Count | Meaning |
| --- | ---: | --- |
| `isotope_evidence` | 24 | Level 1 seed/matter profile exists; isotope evidence is the blocker |
| `isotope_evidence + level_1_seed_record + matter_behavior_profile` | 64 | Snapshot-only element needs isotope evidence plus seed/matter promotion |

Gap work items never close evidence gaps and never permit seed mutation.

Atom behavior readiness scoring:

```text
readiness scores: 118 snapshot elements
ready from admitted isotope evidence: 10 element symbols
blocked by isotope evidence only: 24 Level 1 elements
blocked by seed and matter promotion: 64 snapshot-only elements
```

Each readiness score exposes:

| Field | Meaning |
| --- | --- |
| `evidence_completeness_score` | Completeness of admitted isotope evidence fields |
| `source_confidence_score` | Source-backed confidence from admitted evidence or available source policy |
| `behavior_readiness_score` | Whether atom behavior profiles are currently available |
| `gap_priority_score` | Priority of the unresolved blocker, highest for isotope-only Level 1 gaps |
| `constraint_tension_score` | Remaining tension after evidence, source, and behavior readiness are considered |

Readiness scores are read-only planning records. They do not import isotope
values, close unresolved receipts, generate atom behavior profiles, or mutate
seed records.

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
though the active outer shell is `4s 4p`. For Y through Cd, the same transition
frontier rule applies to the `4d 5s` frontier. For In through Xe, the filled
`4d^10` core remains present behind the `5s 5p` frontier.

## Phase 3 F-Block Expansion Kernel

Phase 3 adds a standalone f-block profile layer over the existing 118-element
snapshot. It covers the 15 lanthanides and 15 actinides:

```text
lanthanides := La..Lu
actinides := Ac..Lr
```

The profile is intentionally bounded. It records f-block context and future
physics requirements without inventing isotope-specific half-lives or exact
f-orbital occupancies.

| Field | Meaning |
| --- | --- |
| `series` | `lanthanide` or `actinide` |
| `f_shell_family` | `4f` for lanthanides and `5f` for actinides |
| `standard_atomic_weight_status` | Snapshot atomic-weight model type, such as `single` or `unavailable` |
| `lanthanide_contraction_relevance` | Series-level flag for lanthanide contraction handling |
| `radioactive_decay_relevance` | Nuclear decay relevance flag; not a half-life claim |
| `actinide_instability_relevance` | Actinide-only instability flag |
| `nuclear_state_extension_required` | True when nuclear-state modeling is required before deeper claims |
| `heavy_element_uncertainty` | True for actinides and unavailable-weight f-block records |
| `relativistic_effect_relevance` | Heavy-element relativity relevance flag |

Validation requires every f-block profile to keep `group = null`, `block = "f"`,
and the correct f-shell family for its series. Radioactive profiles must require
nuclear-state extension, and heavy-element uncertainty must be paired with a
relativistic-effect relevance flag.

## Level 2 Boundary Fields

The element state contract now includes Level 2 boundary fields and sourced partial
Level 2 chemistry values for H through Xe:

| Field | Boundary |
| --- | --- |
| `oxidation_states` | Unique integers in `[-8, 9]`; populated from PubChem for Z=1..54, empty for unpromoted Level 1 records |
| `electronegativity_scale` | `null` or `pauling` |
| `electronegativity_value` | `null` or number in `[0.0, 5.0]`; populated from PubChem when available |
| `electronegativity_source_key` | Required when electronegativity value is present |
| `first_ionization_energy_ev` | `null` or number in `[0.0, 30.0]`; populated from PubChem for Z=1..54 |
| `first_ionization_energy_source_key` | Required when first ionization energy value is present |
| `bond_tendency_tags` | Controlled tag list derived from PubChem `GroupBlock` for Z=1..54 |
| `bond_tendency_source_key` | Required when bond tendency tags are present |

Electronegativity is accepted only as a complete sourced tuple: scale, value, and
source key must all be present together or all be absent. Oxidation states are
source-backed through the element history. First ionization energy is accepted only
as a complete sourced value/source-key pair. Bond tendency is accepted only as a
controlled, duplicate-free tag list with a source key. Current bond-tendency tags
are element-class classifications derived from PubChem `GroupBlock`; they are not
compound-specific reaction predictions. The JSON Schema export and Python
validator enforce the same boundaries.

## Period-5 Snapshot Level 2 Profiles

The engine now carries PubChem-backed period-5 Level 2 chemistry profiles
for Rb through Xe:

```text
Rb, Sr, Y, Zr, Nb, Mo, Tc, Ru, Rh, Pd, Ag, Cd, In, Sn, Sb, Te, I, Xe
```

Each profile contains:

| Field | Meaning |
| --- | --- |
| `oxidation_states` | PubChem oxidation-state set |
| `electronegativity_scale` | `pauling` |
| `electronegativity_value` | PubChem electronegativity value |
| `first_ionization_energy_ev` | PubChem first ionization energy in eV |
| `pubchem_group_block` | PubChem element class |
| `bond_tendency_tags` | Controlled tags derived from PubChem `GroupBlock` |
| `promotion_status` | `snapshot_level_2_chemistry_profile` |

This layer is now a compact projection over the same Rb-Xe chemistry values carried
by the Level 1 seed records. It remains useful for querying period-5 PubChem
chemistry without loading full seed payloads.

## Cs-Rn Promotion-Readiness Profiles

The engine now carries Level 1 promotion-readiness profiles for Cs through Rn:

```text
Cs, Ba, La, Ce, Pr, Nd, Pm, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu,
Hf, Ta, W, Re, Os, Ir, Pt, Au, Hg, Tl, Pb, Bi, Po, At, Rn
```

This is an audit layer, not a seed promotion. Each profile starts from the
full 118-element snapshot and records:

| Field | Meaning |
| --- | --- |
| `snapshot_available` | Whether identity and atomic-weight snapshot evidence exists |
| `physical_property_evidence_available` | Whether a complete PubChem physical-property row exists |
| `unresolved_physical_property_evidence_available` | Whether the PubChem row is incomplete |
| `f_block_profile_available` | Whether a bounded f-block expansion profile exists |
| `available_evidence` | Evidence surfaces already present in this repository |
| `required_missing_evidence` | Evidence still required for Level 1 seed promotion |
| `promotion_blockers` | Machine-readable blockers derived from missing evidence |
| `readiness_status` | `promotion_blocked_missing_source_evidence` until blockers are closed |

The profile set currently validates as:

```text
profiles: 32
blocked: 1
ready: 31
complete physical-property evidence: 31
unresolved physical-property evidence: 1
f-block profiles within span: 15
```

The key principle is source precedence. PubChem physical-property evidence and
f-block relevance flags are useful supporting surfaces, but they do not replace
NIST-backed neutral configurations, first-cation configurations, frontier
signatures, configuration audits, valence signatures, behavior tags, and relation
edges required for full Level 1 seed promotion.

## Cs-Rn Configuration Evidence

The first Cs-Rn blocker now has a bounded evidence overlay:

```text
configuration evidence records: 32
span: Cs through Rn
source: NIST electronic configurations
fields: neutral configuration, first-cation configuration, configuration audit
```

This overlay closes the configuration-evidence part of promotion readiness but
does not promote the records. Remaining Level 1 blockers are:

```text
complete_physical_property_evidence where the source row is incomplete
```

Platinum and gold are recorded as 5d-shell configuration exceptions in this
overlay. NIST also marks selected first-cation configurations in this span as
literature-identified, so those records carry a first-cation source note instead
of hiding the provenance difference.

## Cs-Rn Frontier And Valence Signatures

The second Cs-Rn blocker class now has a derived overlay:

```text
frontier/valence records: 32
span: Cs through Rn
source input: NIST neutral configuration evidence
derived fields: frontier model, frontier signature, outer shell, d shell, f shell, p shell, stability flags
```

The overlay distinguishes:

| Model | Span | Boundary |
| --- | --- | --- |
| `period_6_s_block` | Cs-Ba | outer `6s` frontier |
| `lanthanide_4f_frontier` | La-Lu | `4f`, `5d`, and `6s` participation as present |
| `period_6_transition_frontier` | Hf-Hg | filled `4f^14` core plus `5d/6s` frontier |
| `period_6_p_block_f_d_core` | Tl-Rn | outer `6s/6p` with filled `4f^14 5d^10` core |

This closes the `frontier_signature` and `valence_shell_signature` promotion
readiness blockers. It does not claim behavior tags or relation edges.

## Cs-Rn Oxidation-State Evidence

The third Cs-Rn blocker class now has a PubChem evidence overlay:

```text
oxidation-state evidence records: 32
span: Cs through Rn
source: PubChem Periodic Table CSV
fields: oxidation_states, pubchem_group_block
```

The overlay captures PubChem's oxidation-state sets without promoting the records
to full Level 1 seeds. It keeps GroupBlock as source context, not as a behavior
tag. Validation confirms:

```text
variable oxidation-state records: 15
negative oxidation-state records: 1
zero oxidation-state records: 1
```

Examples:

| Element | Oxidation states | Source class |
| --- | --- | --- |
| Cs | `1` | Alkali metal |
| Ce | `4, 3` | Lanthanide |
| Au | `3, 1` | Transition metal |
| At | `7, 5, 3, 1, -1` | Halogen |
| Rn | `0` | Noble gas |

This closes the `oxidation_state_evidence` readiness blocker. Remaining blockers
are only unresolved measured-property evidence where a PubChem row is incomplete.

## Cs-Rn Behavior Tags

The fourth Cs-Rn blocker class now has a bounded symbolic-inference overlay:

```text
behavior-tag overlay records: 32
span: Cs through Rn
inputs: NIST configuration evidence + frontier/valence overlay + PubChem oxidation-state evidence
output: controlled inferred behavior tags
```

The overlay is not measured evidence. It derives controlled tags from source-backed
inputs and keeps its basis visible. Validation confirms:

```text
variable oxidation tag records: 15
coordination relevance records: 9
f-orbital relevance records: 15
low-reactivity baseline records: 1
```

Examples:

| Element | Example inferred tags |
| --- | --- |
| Cs | `alkali_metal`, `s_block_metal`, `one_electron_loss_pathway` |
| Au | `period_6_transition_metal`, `coordination_relevance`, `filled_d_shell_context` |
| At | `halogen`, `negative_oxidation_pathway`, `heavy_p_block` |
| Rn | `noble_gas`, `closed_shell_baseline`, `low_reactivity_baseline` |

This closes the `level_1_behavior_tags` readiness blocker. The remaining general
Cs-Rn promotion blocker is now closed; At remains blocked by incomplete
physical-property evidence.

## Cs-Rn Relation Edges

The fifth Cs-Rn blocker class now has a relation-edge overlay:

```text
relation overlay records: 32
span: Cs through Rn
edge types: same_period, same_block, same_frontier_model, shared_oxidation_state, shared_behavior_tag
source inputs: snapshot position + frontier overlay + oxidation evidence + behavior overlay
```

The overlay is not a substitutability model or reaction model. It makes explicit
why two elements are adjacent in the evidence mesh. The span has no same-group
pairs because Cs-Rn contains one period row plus f-block records whose group is
unset.

This closes the `relation_edges` readiness blocker. Promotion readiness now
reports 31 Cs-Rn records as ready and keeps Astatine blocked because its measured
physical-property evidence row is incomplete.

## Cs-Rn Promotion Decision Receipts

Promotion readiness now feeds an explicit decision receipt layer:

```text
promotion decision receipts: 32
ready pending approval: 31
blocked unresolved physical property: 1
approved for seed: 0
```

The receipt layer is a governance boundary, not a data source. It records the
current promotion decision without mutating the Level 1 seed pack.

| Decision status | Meaning |
| --- | --- |
| `promotion_ready_pending_approval` | All tracked blockers are closed, but seed promotion still requires explicit approval |
| `promotion_blocked_unresolved_physical_property` | A complete measured physical-property row is still missing |
| `promotion_deferred_by_policy` | A record is neither ready nor blocked by the known physical-property gap |
| `promotion_approved_for_seed` | Reserved for a future explicit seed-mutation decision |

Gold is ready pending approval. Astatine remains blocked by unresolved physical
property evidence. This preserves source completeness and prevents readiness from
being mistaken for approval.

## Cs-Rn Promotion Batch Policy

The selected span-level policy is:

```text
policy: hold_full_cs_rn_span
seed_mutation_allowed: false
ready records: 31
blocked records: 1
blocked symbol: At
```

The policy preserves the current contiguous Level 1 seed pack. Partial promotion
of Cs through Po plus Rn would create a hole at Z=85, so the full span remains in
read-only promotion evidence until Astatine's physical-property evidence gap is
resolved.

The At physical-property gap is explicitly audited:

```text
receipt: MSPEE-PHYSICAL-PROPERTY-GAP-Z085-At
source row status: source_row_incomplete
missing field: boiling_point_k
gap status: awaiting_authoritative_source_value
blocks promotion spans: Cs-Rn
```

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
   first-54 Level 2 records carry PubChem lineage
   d-block records carry transition frontier and behavior kernel
   Cr and Cu carry configuration exception audits
   period-4 p-block records preserve filled 3d-core context
   relation edges are non-self edges
   source references include CIAAW/IUPAC and NIST

6. Validate Phase 3 f-block profiles:
   lanthanide and actinide counts are 15 each
   f-block profiles preserve snapshot identity and unset group assignment
   radioactive and heavy-element uncertainty flags require the matching extension flags

7. Validate period-5 Level 2 snapshot profiles:
   profiles cover exactly Z=37..54
   oxidation, electronegativity, ionization energy, and bond-tendency fields stay bounded
   period-5 profile projection remains consistent with promoted Level 1 records

8. Validate derived state instances:
   ion instances preserve proton-count identity
   ion electron count equals atomic_number - charge
   isotope instances preserve proton-count identity
   isotope neutron count equals mass_number - atomic_number

9. Emit:
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
python -m mcms.cli elements --symbol Na --ion-charge 1
python -m mcms.cli elements --symbol C --isotope-mass 14
python -m mcms.cli elements --symbol C --isotope-mass 14 --isotope-evidence
python -m mcms.cli elements --symbol Fe --common-ion-evidence
python -m mcms.cli elements --symbol Br --physical-property-evidence
python -m mcms.cli elements --symbol At --physical-property-gap-audit
python -m mcms.cli elements --symbol At --physical-property-secondary-source-policy
python -m mcms.cli elements --symbol At --physical-property-secondary-evidence-template
python -m mcms.cli elements --symbol Br --matter-profile
python -m mcms.cli elements --symbol Au --promotion-decision
python -m mcms.cli elements --promotion-batch-policy
python -m mcms.cli api --host 127.0.0.1 --port 8765
```

## Validation

The repository verifier now checks the MSPEE seed pack and full snapshot shape:

```powershell
python scripts/verify_repo.py
python -m pytest tests/test_symbolic_elements.py -q
python -m pytest tests/test_element_level2_snapshot.py -q
python -m pytest tests/test_element_phase3.py -q
python -m pytest tests/test_element_snapshot_drift.py -q
```

The seed pack is valid only when:

1. It contains exactly Z=1..54 in order.
2. Every element validates with no contract errors.
3. Source references include CIAAW/IUPAC and NIST.
4. Relation edges exist and are typed.
5. First-54 Level 2 chemistry records validate and carry PubChem lineage.
6. Phase 2 records carry frontier signatures and configuration audits.
7. Chromium and copper are marked as configuration exceptions.

The full snapshot is valid only when:

1. It contains exactly Z=1..118 in order.
2. Every record validates identity, position, weight model, and source keys.
3. Unavailable atomic weights are explicit.
4. The first 54 snapshot records link to available Level 1 seed records.

The Phase 3 f-block profile set is valid only when:

1. It contains exactly 30 profiles: La..Lu and Ac..Lr.
2. Lanthanide and actinide counts are exactly 15 each.
3. Lanthanides use `4f`; actinides use `5f`.
4. Radioactive profiles require nuclear-state extension.
5. Heavy-element uncertainty requires relativistic-effect relevance.

The period-5 Level 2 snapshot profile set is valid only when:

1. It contains exactly Z=37..54 in order.
2. Every profile references the PubChem source key.
3. Oxidation states, electronegativity, and ionization energy stay inside the
   same bounds as seed-level Level 2 values.
4. Bond tendency tags match the profile's PubChem `GroupBlock`.

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
| `GET /reasoning/configuration/Cr` | Phase 2 configuration-choice explanation |
| `GET /reasoning/similarity?left=Cu&right=K` | Phase 2 outer-shell similarity explanation |
| `GET /instances/ion/{symbol}?charge=1` | Formal ion instance and derived electron count |
| `GET /instances/isotope/{symbol}?mass_number=14` | Formal isotope instance and derived neutron count |
| `GET /atom/behavior` | Atom behavior v2 profile list and validation summary |
| `GET /atom/behavior/{symbol}?mass_number=14` | Single atom behavior v2 profile |
| `GET /atom/behavior/gaps/{symbol}` | Single atom behavior v2 gap receipt |
| `GET /atom/behavior/workplan/{symbol}` | Single atom behavior v2 gap work item |
| `GET /atom/behavior/isotope-source-policy/{symbol}` | Isotope source policy for an isotope-only atom behavior blocker |
| `GET /atom/behavior/isotope-source-search/{symbol}` | Isotope source-search receipt for an isotope-only atom behavior blocker |
| `GET /atom/behavior/isotope-candidate-evidence/{symbol}` | Source-specific isotope candidate evidence receipt pending admission |
| `GET /atom/behavior/isotope-candidate-evidence/template/{symbol}` | Isotope candidate evidence receipt template |
| `GET /atom/behavior/isotope-candidate-admission/{symbol}` | Isotope candidate admission receipt after canonical evidence closure |
| `GET /evidence/isotopes` | Isotope evidence list and validation summary |
| `GET /evidence/isotopes/{symbol}?mass_number=14` | Filtered isotope evidence |
| `GET /evidence/isotopes/unresolved` | Unresolved isotope evidence receipts |
| `GET /evidence/isotopes/unresolved/{symbol}` | Filtered unresolved isotope evidence receipt |
| `GET /evidence/common-ions` | Common-ion candidate evidence list and validation summary |
| `GET /evidence/common-ions/{symbol}` | Filtered common-ion candidate evidence |
| `GET /evidence/common-ions/unresolved` | Unresolved common-ion evidence receipts |
| `GET /evidence/common-ions/unresolved/{symbol}` | Filtered unresolved common-ion evidence receipt |
| `GET /evidence/configurations` | Cs-Rn configuration evidence list and validation summary |
| `GET /evidence/configurations/{symbol}` | Single Cs-Rn configuration evidence record |
| `GET /evidence/oxidation-states` | Cs-Rn oxidation-state evidence list and validation summary |
| `GET /evidence/oxidation-states/{symbol}` | Single Cs-Rn oxidation-state evidence record |
| `GET /evidence/physical-properties` | Physical-property evidence list and validation summary |
| `GET /evidence/physical-properties/{symbol}` | Filtered physical-property evidence |
| `GET /evidence/physical-properties/unresolved` | Unresolved physical-property evidence list |
| `GET /evidence/physical-properties/unresolved/{symbol}` | Filtered unresolved physical-property evidence |
| `GET /evidence/physical-properties/gaps` | Physical-property gap audit receipts |
| `GET /evidence/physical-properties/gaps/{symbol}` | Single physical-property gap audit receipt |
| `GET /evidence/physical-properties/workplan` | Prioritized physical-property gap work items |
| `GET /evidence/physical-properties/workplan/{symbol}` | Single physical-property gap work item |
| `GET /evidence/physical-properties/source-search` | Active physical-property source-search receipts |
| `GET /evidence/physical-properties/source-search/{symbol}` | Single physical-property source-search receipt |
| `GET /evidence/physical-properties/partial-source-search` | Active partial-property source-search receipts |
| `GET /evidence/physical-properties/partial-source-search/{symbol}` | Single partial-property source-search receipt |
| `GET /evidence/physical-properties/secondary-evidence` | Admitted secondary physical-property evidence receipts |
| `GET /evidence/physical-properties/secondary-evidence/admission/{symbol}` | Admission decision for secondary evidence |
| `GET /evidence/physical-properties/conflicts/{symbol}` | Secondary-source conflict-resolution receipt |
| `GET /evidence/physical-properties/corroboration/{symbol}` | Secondary-source corroboration-review receipt |
| `GET /evidence/physical-properties/review/{symbol}` | Secondary-source review receipt |
| `GET /evidence/physical-properties/gap-closure/{symbol}` | Secondary-source gap-closure decision |
| `GET /evidence/physical-properties/closure-approval/{symbol}` | Secondary-source closure-approval receipt |
| `GET /evidence/physical-properties/seed-update/{symbol}` | Secondary-source seed-update receipt |
| `GET /evidence/physical-properties/escalations/{symbol}` | Blocked-work escalation receipt |
| `GET /evidence/physical-properties/escalation-search/{symbol}` | Source-investigation receipt for blocked escalation |
| `GET /evidence/physical-properties/escalation-resolution/{symbol}` | Resolution recommendation receipt for blocked escalation |
| `GET /evidence/physical-properties/operator-decisions/{symbol}` | Deferred operator-decision receipt |
| `GET /evidence/physical-properties/continued-evidence/{symbol}` | Continued-evidence plan for deferred operator decision |
| `GET /evidence/physical-properties/secondary-evidence/template/{symbol}` | Secondary evidence receipt template |
| `GET /evidence/physical-properties/secondary-source-policy` | Physical-property secondary-source policies |
| `GET /evidence/physical-properties/secondary-source-policy/{symbol}` | Single secondary-source policy |
| `GET /frontier/cs-rn` | Cs-Rn frontier/valence signature list and validation summary |
| `GET /frontier/cs-rn/{symbol}` | Single Cs-Rn frontier/valence signature record |
| `GET /behavior/cs-rn` | Cs-Rn behavior-tag overlay list and validation summary |
| `GET /behavior/cs-rn/{symbol}` | Single Cs-Rn behavior-tag overlay record |
| `GET /relations/cs-rn` | Cs-Rn relation-edge overlay list and validation summary |
| `GET /relations/cs-rn/{symbol}` | Single Cs-Rn relation-edge overlay record |
| `GET /matter/profiles` | Matter-behavior profile list and validation summary |
| `GET /matter/profiles/{symbol}` | Filtered matter-behavior profile |
| `GET /promotion/cs-rn` | Cs-Rn promotion-readiness profile list and validation summary |
| `GET /promotion/cs-rn/{symbol}` | Single Cs-Rn promotion-readiness profile |
| `GET /promotion/batch-policy` | Cs-Rn span-level promotion batch policy receipt |
| `GET /promotion/decisions` | Cs-Rn promotion decision receipt list and validation summary |
| `GET /promotion/decisions/{symbol}` | Single Cs-Rn promotion decision receipt |
| `GET /phase3/f-block` | Phase 3 f-block profile list and validation summary |
| `GET /phase3/f-block/{symbol}` | Single f-block expansion profile |
| `GET /level2/period-5` | Period-5 Level 2 snapshot profile list and validation summary |
| `GET /level2/period-5/{symbol}` | Single period-5 Level 2 snapshot profile |

Unknown routes, unknown symbols, invalid relation types, and non-GET methods
return explicit JSON error payloads.

## Phase 2 Reasoning Examples

The element engine exposes deterministic reasoning helpers for the two Phase 2
questions in the source document:

```powershell
@'
from mcms.elements import compare_outer_shell_similarity, explain_configuration_choice

print(explain_configuration_choice("Cr").to_dict())
print(compare_outer_shell_similarity("Cu", "K").to_dict())
'@ | python -
```

The configuration explanation reports simple Aufbau as a candidate, keeps the
NIST-backed configuration as authority, records Cr/Cu conflicts as exceptions,
and preserves identity through proton count. The similarity explanation can mark
Cu and K as superficially similar through `4s^1` while separating copper's filled
`3d^10` transition-metal frontier from potassium's main-group frontier.

## Phase 3 F-Block Profiles

The Phase 3 f-block layer is a bounded overlay on the 118-element snapshot for
the lanthanides and actinides. It adds series-level frontier flags, radioactive
relevance, nuclear-state extension requirements, heavy-element uncertainty, and
relativistic-effect relevance without assigning exact isotope half-lives or exact
f-orbital occupancies.

```powershell
@'
from mcms.elements import get_f_block_expansion_profile, validate_f_block_expansion_profiles

print(validate_f_block_expansion_profiles().to_dict())
print(get_f_block_expansion_profile("U").to_dict())
'@ | python -
```

The validation contract expects 30 profiles: 15 lanthanides and 15 actinides.
Promethium and the actinides carry radioactive relevance. Actinide profiles also
carry nuclear-state extension and heavy-element uncertainty flags.

## Cs-Rn Promotion Readiness

The promotion-readiness layer exposes the evidence gap before expanding the
Level 1 seed pack beyond Xe:

```powershell
@'
from mcms.elements import (
    get_cs_rn_promotion_readiness_profile,
    validate_cs_rn_promotion_readiness_profiles,
)

print(validate_cs_rn_promotion_readiness_profiles().to_dict())
print(get_cs_rn_promotion_readiness_profile("At").to_dict())
'@ | python -
```

The validation contract expects 32 profiles spanning atomic numbers 55 through
86. It now reports 31 ready profiles and one blocked profile. Astatine remains
blocked because PubChem does not publish a complete physical-property row in the
local evidence snapshot.

## Promotion Decision Receipts

The promotion-decision layer is inspectable independently:

```powershell
@'
from mcms.elements import (
    get_promotion_decision_receipt,
    validate_promotion_decision_receipts,
)

print(validate_promotion_decision_receipts())
print(get_promotion_decision_receipt("Au").to_dict())
print(get_promotion_decision_receipt("At").to_dict())
'@ | python -
```

The validation contract expects 32 receipts: 31 ready pending approval, one
blocked by unresolved physical-property evidence, and zero approved seed
mutations.

The batch policy is inspectable independently:

```powershell
python -m mcms.cli elements --promotion-batch-policy
```

It currently reports `hold_full_cs_rn_span` and `seed_mutation_allowed = false`.

## Physical-Property Gap Audits

The physical-property gap audit layer is inspectable independently:

```powershell
@'
from mcms.elements import (
    get_physical_property_gap_audit_receipt,
    validate_physical_property_gap_audit_receipts,
)

print(validate_physical_property_gap_audit_receipts())
print(get_physical_property_gap_audit_receipt("At").to_dict())
'@ | python -
```

The validation contract expects 25 gap receipts, all with missing boiling-point
evidence. Only At blocks the Cs-Rn promotion span.

## Secondary-Source Policy

The physical-property secondary-source policy layer is inspectable independently:

```powershell
@'
from mcms.elements import (
    get_physical_property_secondary_source_policy,
    validate_physical_property_secondary_source_policies,
)

print(validate_physical_property_secondary_source_policies())
print(get_physical_property_secondary_source_policy("At").to_dict())
'@ | python -
```

The validation contract expects 25 policies. Each policy lists candidate source
classes and admission requirements. The policy closes zero gaps and allows zero
seed mutations; a field-specific evidence receipt is still required before any
missing value can be admitted.

## Physical-Property Gap Workplan

The gap workplan orders unresolved measured-property work without closing any
gap:

```text
work_items = 25
conflict_blocked_promotion = 1
single_field_source_search = 2
partial_property_source_search = 7
synthetic_superheavy_uncertainty = 15
gap closure = 0
```

The source-search receipt layer opens the next two single-field searches:

```text
source_search_receipts = 2
targets = Pa, Bk
field = boiling_point_k
status = source_search_complete_candidate_receipt_created
gap closure = 0
```

The partial-source-search layer opens two-field searches:

```text
partial_source_search_receipts = 7
targets = Fr, Cf, Es, Fm, Md, No, Lr
field_searches = 14
gap closure = 0
```

## Secondary Evidence Receipts

The secondary evidence receipt workflow is inspectable independently:

```powershell
@'
from mcms.elements import (
    build_physical_property_secondary_evidence_template,
    validate_physical_property_secondary_evidence_receipts,
)

print(validate_physical_property_secondary_evidence_receipts())
print(build_physical_property_secondary_evidence_template("At"))
'@ | python -
```

The validation contract currently expects eight reviewed candidate receipts:
At, Fr boiling point, Fr density, Pa, Bk, Es, and two Cf field candidates.
Zero receipts are admitted. The At
template defines the fields required before another candidate source can be reviewed.

The admission decision layer records why the LANL candidates are not admitted:

```text
At decision: secondary_evidence_not_admitted_conflict
Fr decision: secondary_evidence_not_admitted_conflict
Fr density decision: secondary_evidence_not_admitted_needs_corroboration
Pa decision: secondary_evidence_not_admitted_conflict
Bk decision: secondary_evidence_not_admitted_needs_corroboration
Cf boiling decision: secondary_evidence_not_admitted_needs_corroboration
Cf density decision: secondary_evidence_not_admitted_pending_review
Es decision: secondary_evidence_not_admitted_needs_corroboration
gap closures: 0
seed mutations: 0
```

The conflict-resolution receipt records the compared source values:

```text
At resolution: blocked_pending_higher_precedence_source
Fr resolution: blocked_pending_higher_precedence_source
Pa resolution: blocked_pending_higher_precedence_source
At conflict: LANL 337 degC / 610.15 K vs RSC 350 degC / 623.15 K
Fr conflict: LANL 680 degC / 953.15 K vs RSC 650 degC / 923.15 K
Pa conflict: LANL 4027 degC / 4300.15 K vs RSC 4000 degC / 4273.15 K
seed mutation allowed: false
```

The corroboration-review receipts record the Fr density plus Bk, Cf, and Es
boiling-point candidate boundaries:

```text
Fr density review: blocked_pending_corroborating_source
candidate: WebElements 2900 kg/m3 / 2.9 g/cm3
checked source: RSC lists density as unknown
Bk review: blocked_pending_corroborating_source
candidate: LANL 2627 degC / 2900.15 K
checked source: RSC lists boiling point as unknown
Cf review: blocked_pending_corroborating_source
candidate: LANL 1470 degC / 1743.15 K
checked source: RSC lists boiling point as unknown
Es review: blocked_pending_corroborating_source
candidate: LANL 996 degC / 1269.15 K
checked source: RSC lists boiling point as unknown
gap closure: false
```

The source-review receipt records the Cf density candidate boundary:

```text
Cf density review: resolved_admit_candidate
candidate: RSC 15.1 g/cm3
corroborating source: WebElements 15100 kg/m3 / 15.1 g/cm3
gap closure: false
```

The gap-closure decision records the governed approval boundary:

```text
Cf density closure: gap_closure_ready_pending_operator_approval
candidate: 15.1 g/cm3
gap closure: false
seed mutation allowed: false
next action: approve or reject through a governed seed-update receipt
```

The closure-approval receipt records the final approval boundary:

```text
Cf density closure approval: closure_approval_deferred
gap closure: false
seed mutation allowed: false
next action: issue approved or rejected closure approval before seed update
```

The seed-update receipt records the mutation boundary:

```text
Cf density seed update: seed_update_blocked_by_deferred_approval
gap closure: false
seed mutation allowed: false
seed update applied: false
next action: issue approved closure approval before seed update
```

The escalation receipts record the remaining operator work:

```text
higher-precedence source required: At, Fr, Pa
corroborating source required: Fr density, Bk boiling point, Cf boiling point, Es boiling point
operator approval required: Cf density seed update
gap closure: false
seed mutation allowed: false
```

The At, Fr, and Pa escalation-search receipts record the source-investigation boundary:

```text
At boiling point search: higher_precedence_source_not_found
checked: NIST Chemistry WebBook atomic At page
checked: PubChem element Astatine, 337 degC cluster
checked: RSC Astatine, 350 degC cluster
Fr boiling point search: higher_precedence_source_not_found
checked: NIST Chemistry WebBook atomic Fr page
checked: PubChem element Francium, 680 degC cluster
checked: RSC Francium, 650 degC cluster
Pa boiling point search: higher_precedence_source_not_found
checked: NIST Chemistry WebBook atomic Pa page
checked: PubChem element Protactinium, 4027 degC cluster
checked: RSC Protactinium, 4000 degC cluster
checked: WebElements Protactinium, 4300 K cluster
gap closure: false
seed mutation allowed: false
```

The Fr density corroboration-search receipt records:

```text
Fr density search: corroborating_source_not_found
candidate: WebElements 2900 kg/m3
checked: RSC density unknown
checked: PubChem density unavailable
gap closure: false
seed mutation allowed: false
```

The Bk boiling-point corroboration-search receipt records:

```text
Bk boiling point search: corroborating_source_not_found
candidate: LANL 2627 degC
checked: RSC boiling point unknown
checked: WebElements no boiling-point data
checked: PubChem aligns with LANL cluster but is not independent corroboration
gap closure: false
seed mutation allowed: false
```

The Cf and Es boiling-point corroboration-search receipts record:

```text
Cf boiling point search: corroborating_source_not_found
candidate: LANL 1470 degC
checked: RSC boiling point unknown
checked: WebElements no boiling-point data
checked: PubChem aligns with LANL cluster but is not independent corroboration

Es boiling point search: corroborating_source_not_found
candidate: LANL 996 degC
checked: RSC boiling point unknown
checked: WebElements no independent boiling-point data
checked: PubChem aligns with LANL cluster but is not independent corroboration

gap closure: false
seed mutation allowed: false
```

The escalation-resolution receipts recommend next action without applying it:

```text
At/Fr/Pa conflicts: conflict_resolution_blocked_pending_operator_decision
Fr/Bk/Cf/Es uncorroborated candidates: candidate_rejection_recommended_pending_operator_decision
final resolution applied: false
gap closure: false
seed mutation allowed: false
```

The operator-decision receipts add the final approval slot while keeping it deferred:

```text
operator decision status: operator_decision_deferred
approved resolutions: 0
rejected resolutions: 0
final resolution applied: false
gap closure: false
seed mutation allowed: false
```

The continued-evidence plans convert deferred decisions into bounded next work:

```text
At/Fr/Pa: higher_precedence_source_discovery
Fr/Bk/Cf/Es: independent_corroboration_discovery
continued evidence required: true
final resolution applied: false
gap closure: false
seed mutation allowed: false
```

The no-candidate review receipts record the Fm, Md, No, and Lr checked-source boundaries:

```text
Fm review: blocked_no_admissible_candidate_found
fields checked: boiling_point_k, density_value
checked sources: LANL, RSC, WebElements
Md review: blocked_no_admissible_candidate_found
fields checked: boiling_point_k, density_value
checked sources: LANL, RSC, WebElements
No review: blocked_no_admissible_candidate_found
fields checked: boiling_point_k, density_value
checked sources: LANL, RSC, WebElements
Lr review: blocked_no_admissible_candidate_found
fields checked: boiling_point_k, density_value
checked sources: LANL, RSC, WebElements
gap closure: false
seed mutation allowed: false
```

## Configuration Evidence

The Cs-Rn configuration overlay is inspectable independently:

```powershell
@'
from mcms.elements import (
    find_configuration_evidence_record,
    validate_configuration_evidence_records,
)

print(validate_configuration_evidence_records())
print(find_configuration_evidence_record("Au").to_dict())
'@ | python -
```

The validation contract expects 32 records, with platinum and gold marked as
configuration exceptions. The overlay uses NIST as configuration authority and
keeps first-cation literature notes visible for the NIST special cases.

## Frontier And Valence Overlay

The Cs-Rn frontier/valence overlay is inspectable independently:

```powershell
@'
from mcms.elements import (
    find_frontier_valence_signature_record,
    validate_frontier_valence_signature_records,
)

print(validate_frontier_valence_signature_records())
print(find_frontier_valence_signature_record("Au").to_dict())
'@ | python -
```

The validation contract expects 32 records: 2 s-block, 15 lanthanide, 9
period-6 transition-frontier, and 6 p-block records. Period-6 p-block records
preserve filled `4f^14 5d^10` core context behind the `6s/6p` shell.

## Oxidation-State Evidence

The Cs-Rn oxidation-state overlay is inspectable independently:

```powershell
@'
from mcms.elements import (
    find_oxidation_state_evidence_record,
    validate_oxidation_state_evidence_records,
)

print(validate_oxidation_state_evidence_records())
print(find_oxidation_state_evidence_record("Au").to_dict())
'@ | python -
```

The validation contract expects 32 records. It keeps oxidation states as sourced
evidence and does not claim that every listed state is stable in every compound
or condition.

## Behavior-Tag Overlay

The Cs-Rn behavior overlay is inspectable independently:

```powershell
@'
from mcms.elements import (
    find_behavior_tag_overlay_record,
    validate_behavior_tag_overlay_records,
)

print(validate_behavior_tag_overlay_records())
print(find_behavior_tag_overlay_record("Au").to_dict())
'@ | python -
```

The validation contract expects 32 records. Behavior tags are controlled symbolic
inference and remain separate from measured physical properties and relation edges.

## Relation-Edge Overlay

The Cs-Rn relation overlay is inspectable independently:

```powershell
@'
from mcms.elements import (
    find_relation_overlay_record,
    validate_relation_overlay_records,
)

print(validate_relation_overlay_records())
print(find_relation_overlay_record("Au").to_dict())
'@ | python -
```

The validation contract expects 32 records and a nonzero edge count. Edges are
generated from explicit fields and remain separate from compound behavior claims.

## Period-5 Level 2 Profiles

The period-5 Level 2 layer exposes compact sourced chemistry profiles for the
elements immediately after Kr:

```powershell
@'
from mcms.elements import get_period_5_level_2_profile, validate_period_5_level_2_profiles

print(validate_period_5_level_2_profiles().to_dict())
print(get_period_5_level_2_profile("Xe").to_dict())
'@ | python -
```

The validation contract expects 18 profiles spanning atomic numbers 37 through
54. These profiles carry PubChem oxidation states, Pauling electronegativity,
first ionization energy, PubChem `GroupBlock`, and derived bond-tendency tags.

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
without mutating seed records. The same checker also supports the Rb-Xe period-5
snapshot overlay through `--scope period-5`.

The physical-property evidence layer has its own PubChem drift checker. It
compares standard state, melting point, boiling point, and density for complete
local evidence records. Incomplete source rows remain skipped rather than guessed.

```powershell
python scripts/check_element_level2_drift.py --fail-on-drift
python scripts/check_element_level2_drift.py --scope period-5 --fail-on-drift
python scripts/check_element_physical_property_drift.py --fail-on-drift
```

Fixture mode supports offline review and CI-safe parser tests:

```powershell
python scripts/check_element_snapshot_drift.py --fixture-html path\to\ciaaw.html --fail-on-drift
python scripts/check_element_level2_drift.py --fixture-csv path\to\pubchem.csv --fail-on-drift
python scripts/check_element_level2_drift.py --scope period-5 --fixture-csv path\to\pubchem.csv --fail-on-drift
python scripts/check_element_physical_property_drift.py --fixture-csv path\to\pubchem.csv --fail-on-drift
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
| `period_5_level_2_snapshot_no_drift` | Local Rb-Xe snapshot Level 2 profiles match parsed PubChem source rows |
| `period_5_level_2_snapshot_drift_detected` | At least one Rb-Xe profile field differs or a required source row is missing |
| `period_5_level_2_snapshot_source_unavailable` | The PubChem source could not be read or parsed for the period-5 overlay |
| `physical_property_evidence_no_drift` | Local physical-property evidence matches complete parsed PubChem source rows |
| `physical_property_evidence_drift_detected` | At least one local physical-property field differs or a required complete source row is missing |
| `physical_property_evidence_source_unavailable` | The PubChem source could not be read or parsed for physical-property evidence |

## Constructive Deltas

| Delta | Result |
| --- | --- |
| Static table cell -> symbolic object | Level 1 records now carry identity, laws, state, exposure, and history |
| Partial seed pack -> full source snapshot | All 118 element identities are now queryable |
| Atomic weight constant -> typed model | Interval weights stay intervals and single weights stay single values |
| Position-only table -> relation graph | Elements now expose same-group, same-period, and same-block edges |
| Unchecked data -> validation receipt | Every exposed seed can emit a stable hash and validation status |
| Static source snapshot -> drift-checkable source boundary | CIAAW source changes now produce explicit drift reports |
| Sourced Level 2 values -> drift-checkable chemistry boundary | PubChem source changes now produce explicit seed and period-5 Level 2 drift reports |
| Physical-property evidence -> drift-checkable property boundary | PubChem physical-property source changes now produce explicit drift reports |
| Python object contract -> JSON Schema contract | Seed and snapshot records can now be exported and externally validated |
| Embedded relation edges -> graph export | Element relation queries now produce deterministic node and edge payloads |
| CLI-only surface -> local API surface | Element lookup, schemas, and graph queries now have read-only JSON routes |
| Raw API routes -> dashboard view model | Dashboard consumers now get one composed read-only payload |
| Planned Level 2 fields -> bounded contract | Oxidation-state and electronegativity fields now reject invalid values |
| Bounded Level 2 fields -> sourced first-54 values | H through Xe now carry PubChem-backed oxidation-state, electronegativity, first-ionization-energy, and GroupBlock-derived bond-tendency values |
| Planned bond fields -> source-classified boundary | Bond-tendency tags now derive from PubChem GroupBlock classes and remain non-reaction predictions |
| Simple Aufbau output -> configuration audit | Cr and Cu store both simple candidates and NIST-backed corrected states |
| Outer-shell-only transition rule -> frontier kernel | Sc through Zn now expose outer ns plus inner 3d structure |
| Period-4 p-block shell view -> filled d-core context | Ga through Kr preserve `3d^10` behind the `4s 4p` frontier |
| Planned f-block expansion -> bounded Phase 3 profiles | Lanthanides and actinides now expose f-shell, nuclear, uncertainty, and relativity relevance flags |
| Level 2 stops at Kr -> period-5 seed promotion | Rb through Xe now carry full Level 1 seed records plus period-5 Level 2 profile projections |
| Informal ion/isotope examples -> formal state instances | Ion and isotope IDs now validate derived electron and neutron counts |
| State instances -> bounded evidence records | H-Ca isotope evidence and selected common-ion candidates now carry source lineage |
| Missing isotope/common-ion data -> unresolved receipts | Snapshot isotope gaps and Level 1 common-ion gaps are queryable without guessed data |
| Symbolic behavior tags -> measured property evidence | 93 complete PubChem physical-property rows now carry sourced standard-state, melting, boiling, and density fields |
| Missing measured property -> unresolved receipt | 25 incomplete PubChem physical-property rows now emit explicit unresolved evidence records |
| Unresolved property -> gap audit | 25 source-gap receipts now expose missing fields and promotion impact |
| Gap audit -> workplan | 25 unresolved property gaps are prioritized without closing gaps |
| Workplan -> source-search receipt | Pa and Bk now have completed source-search receipts linked to candidate evidence |
| Workplan -> partial-source-search receipt | Fr, Cf, Es, Fm, Md, No, and Lr now have two-field search receipts |
| Gap audit -> secondary-source policy | 25 policies define admission requirements without importing values |
| Policy -> secondary evidence workflow | At, Fr boiling point, Fr density, Pa, Bk, Cf, and Es candidates exist, with zero admitted receipts |
| Candidate -> admission decision | At, Fr boiling point, Fr density, Pa, Bk, Cf, and Es candidates are reviewed but not admitted |
| Admission decision -> conflict receipt | At, Fr, and Pa source disagreements are recorded as blocking receipts |
| Admission decision -> corroboration receipt | Bk, Cf, and Es boiling-point lack of corroboration is recorded as blocking receipts |
| Admission decision -> source-review receipt | Cf density is corroborated but still requires governed gap-closure approval |
| Source-review receipt -> gap-closure decision | Cf density is ready pending operator approval, with zero seed mutation |
| Closure-approval receipt -> seed-update receipt | Cf density seed update is blocked by deferred approval, preserving seed data |
| Blocked receipts -> escalation receipts | At/Fr/Pa conflicts, Fr/Bk/Cf/Es corroboration blocks, and Cf approval are now queryable work items |
| At/Fr/Pa escalation -> escalation-search receipts | NIST/PubChem/RSC/WebElements source checks leave conflicts blocked pending higher-precedence evidence or explicit resolution |
| Fr density escalation -> corroboration-search receipt | WebElements remains uncorroborated by RSC or PubChem, so admission stays blocked |
| Bk boiling-point escalation -> corroboration-search receipt | LANL candidate remains uncorroborated by independent RSC/WebElements evidence |
| Cf boiling-point escalation -> corroboration-search receipt | LANL candidate remains uncorroborated by independent RSC/WebElements evidence |
| Es boiling-point escalation -> corroboration-search receipt | LANL candidate remains uncorroborated by independent RSC/WebElements evidence |
| Escalation-search receipts -> resolution recommendations | Conflicts remain blocked and uncorroborated candidates are recommended for operator-reviewed rejection |
| Resolution recommendations -> operator decisions | All operator decisions are deferred until explicit approval or rejection is recorded |
| Deferred operator decisions -> continued-evidence plans | Blocked recommendations now carry bounded search plans without final resolution or seed mutation |
| Gap-closure decision -> closure-approval receipt | Cf density approval is deferred, preserving the unresolved seed boundary |
| Partial source search -> no-candidate receipt | Fm, Md, No, and Lr checked-source absence is recorded without guessing values |
| Evidence records -> matter profiles | H through Xe now expose bounded matter-behavior read models |
| Atom behavior gaps -> isotope source policy | 24 isotope-only blockers now define CIAAW/IUPAC and NIST primary candidates plus PubChem bounded secondary context, with zero gap closure |
| Isotope source policy -> source-search receipts | 24 isotope-only blockers now have open source-search receipts; active candidate receipts are zero after Oxygen admission |
| Gap receipts -> readiness scoring | 118 snapshot elements now expose readiness, source confidence, gap priority, and constraint tension without closing gaps |
| Oxygen candidate evidence -> canonical isotope evidence | O-16/O-17/O-18 are admitted as source-backed isotope evidence, removing Oxygen from isotope-only blocker queues |
| Oxygen admission -> historical receipt | Oxygen canonical closure is recorded with zero active candidate retention and zero seed mutation authority |
| Snapshot-only Cs-Rn -> promotion-readiness audit | Cs through Rn now expose evidence gaps before Level 1 promotion |
| Configuration blocker -> source evidence overlay | Cs through Rn now carry NIST neutral and first-cation configuration evidence |
| Frontier blocker -> derived signature overlay | Cs through Rn now carry frontier and valence-signature records |
| Oxidation blocker -> source evidence overlay | Cs through Rn now carry PubChem oxidation-state evidence |
| Behavior blocker -> controlled inference overlay | Cs through Rn now carry bounded behavior-tag records |
| Relation blocker -> evidence mesh overlay | Cs through Rn now carry relation-edge records |
| Readiness result -> decision receipt | Cs through Rn now separate promotion readiness from explicit seed approval |
| Decision ambiguity -> batch policy | Cs-Rn now hold the full span until At evidence is complete |

## Fracture Deltas Avoided

| Risk | Guard |
| --- | --- |
| Confusing ion state with element identity | Electron count changes do not mutate proton-count identity |
| Confusing isotope state with element identity | Neutron count changes do not mutate proton-count identity |
| Collapsing atomic-weight intervals | Interval values are stored with lower and upper bounds |
| Inferring unsupported chemistry behavior | Level 2 properties are not claimed by Level 1 seeds |
| Treating generated data as source authority | History records cite source authorities and derivation trace |
| Silent Aufbau failure | Candidate/source conflict is stored as a configuration exception |
| Flattening d-block elements into one family | Frontier signatures distinguish open, half-filled, and filled d-shell states |
| Claiming universal magnetism or catalysis | Transition behavior fields are relevance flags, not guaranteed compound behavior |
| Inventing unsupported f-block precision | Phase 3 flags do not assign exact isotope half-lives or exact f-orbital occupancies |
| Promoting incomplete records to full seeds | Rb-Xe seed promotion includes source-backed electron-state records, not chemistry fields alone |
| Treating common-ion candidates as universal stability | Common-ion evidence is tied to sourced oxidation states and labeled as candidate evidence |
| Treating missing evidence as absent from the system | Unresolved isotope and common-ion receipts preserve explicit gap state |
| Mixing measured properties with symbolic inference | Physical properties are separate evidence records with source lineage |
| Forcing every phase value into simple order | Arsenic preserves the source phase-transition anomaly with an explicit note |
| Inventing missing measured properties | Incomplete PubChem rows are represented as unresolved records, not guessed values |
| Treating profiles as simulation | Matter profiles declare non-claims and remain bounded read models |
| Silently skipping Cs-Rn evidence gaps | Promotion-readiness profiles list missing evidence and blockers |
| Treating configuration evidence as full promotion | Cs-Rn records remain blocked until behavior and relation layers are added |
| Treating frontier signatures as full chemistry | Frontier overlay does not claim oxidation states, behavior tags, or relation edges |
| Treating oxidation states as universal behavior | Oxidation evidence is source data, not a guarantee for every compound or condition |
| Treating inferred behavior as measured fact | Behavior tags are labeled as symbolic inference with explicit basis |
| Treating relation edges as substitutability | Relation edges carry reasons and do not claim equivalent behavior |
| Treating readiness as approval | Promotion decision receipts keep seed mutation behind explicit approval |
| Creating a Level 1 seed hole | Batch policy holds the span instead of promoting 31 records around At |
| Treating blank source fields as data | Gap audits enforce no-guess policy for incomplete physical-property rows |
| Treating policy as evidence | Secondary-source policy closes zero gaps and allows zero seed mutations |
| Treating a candidate as admitted evidence | Admission decision blocks LANL because secondary sources conflict |
| Treating a conflict as resolved | Conflict receipt keeps At blocked pending higher-precedence evidence |

## Source Boundary

The seed implementation uses these authority anchors:

1. CIAAW/IUPAC Standard Atomic Weights 2024: `https://www.ciaaw.org/atomic-weights.htm`
2. NIST Electronic Configurations of the Elements:
   `https://www.nist.gov/pml/atomic-reference-data-electronic-structure-calculations/atomic-reference-data-electronic-8`
3. PubChem Periodic Table of Elements CSV:
   `https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV`
4. CIAAW Isotopic Compositions of the Elements 2024:
   `https://www.ciaaw.org/isotopic-abundances.htm`
5. NIST Atomic Weights and Isotopic Compositions:
   `https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl`
6. PubChem Carbon-14 record:
   `https://pubchem.ncbi.nlm.nih.gov/compound/Carbon-14`

## Next Expansion

1. Resolve Astatine physical-property evidence gap before full Cs-Rn seed promotion.
2. Resolve measured-property gaps as complete authoritative values become available.
3. Resolve At boiling-point conflict receipt with a higher-precedence field source.
4. Promote Phase 3 from relevance flags to source-backed f-block state records
   where authoritative configuration and isotope data are available.
5. Expand isotope evidence beyond the H/C seed with abundance, half-life, decay-mode,
   and nuclear-state source lineage.
6. Continue sourced Level 2 chemistry and measured-property expansion beyond Xe.
