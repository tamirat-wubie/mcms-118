# MSPEE-118 Project History

## Purpose

This document records the project lineage from the original generated seed
package to the current repository. It separates historical intent, implemented
state, and future expansion so older descriptions do not get mistaken for current
implementation truth.

## First-Principles Boundary

The project starts from four separations:

| Question | First-principles answer |
| --- | --- |
| What makes an element itself? | Proton count, represented by atomic number |
| What changes without changing element identity? | Electron state, ion state, isotope state, and measurement context |
| What must be source-backed? | Identity, atomic weight evidence, electron configurations, and measured properties |
| What may be inferred? | Symbolic behavior flags, relation edges, and future matter-behavior profiles, with labels |

The central model is:

```text
flat periodic-table row
-> typed element record
-> source-backed validation object
-> relation graph node
-> bounded matter-behavior seed
```

Current element records are structured as:

```text
element_record := identity + laws + state + exposure + history
```

## Origin Package

The original ChatGPT-generated artifact was described as:

```text
mullusi-standard-symbolic-periodic-element-engine/
  mspee/schema.py
  mspee/validators.py
  mspee/kernels/*
  mspee/data/seed_001_020.py
  mspee/emitters/*
  tests/*
```

Its reported state was:

```text
seed elements: 20
tests: 11 passed
relation graph: 20 nodes, 136 edges
status: valid seed implementation
```

That package established the first representation boundary:

```text
element identity != ion state
element identity != isotope state
atomic weight != eternal fixed constant
source-backed fact != symbolic inference
```

## Current Repository Shape

The current repository is not the original `mspee/` package layout. It uses:

```text
src/mcms/elements/
  model.py
  seed.py
  snapshot.py
  graph.py
  schema.py
  dashboard.py
  reasoning.py
  phase3.py
  level2_snapshot.py
```

The Python package and import namespace remain `mcms` for repository continuity.
The active element-engine product boundary is MSPEE-118.

## Current Implementation Truth

| Surface | Current state |
| --- | --- |
| Level 1 seed pack | Z=1..54, H through Xe |
| Full snapshot | Z=1..118 identity, position, and atomic-weight model |
| Atomic weights | CIAAW/IUPAC-backed typed model: `single`, `interval`, or `unavailable` |
| Electron configurations | NIST-backed Level 1 seed configurations |
| Transition frontier kernel | Implemented for Sc through Zn and Y through Cd |
| Configuration exceptions | Cr and Cu store simple candidate plus source-backed state |
| Period p-block d-core context | Ga through Kr preserve filled `3d^10`; In through Xe preserve filled `4d^10` |
| Level 2 seed chemistry | H through Xe carry PubChem oxidation, electronegativity, ionization, and bond tendency fields |
| Period-5 Level 2 projection | Rb through Xe carry compact PubChem chemistry profiles |
| F-block Phase 3 profiles | La through Lu and Ac through Lr carry bounded f-block relevance flags |
| Promotion readiness | Cs through Rn carry Level 1 promotion-readiness audit profiles |
| Configuration evidence | Cs through Rn carry NIST neutral and first-cation configuration evidence |
| Frontier signatures | Cs through Rn carry derived frontier and valence-signature overlays |
| Oxidation evidence | Cs through Rn carry PubChem oxidation-state evidence |
| Behavior tags | Cs through Rn carry bounded symbolic behavior-tag overlays |
| Relation overlay | Cs through Rn carry evidence-derived relation edges |
| Promotion decisions | Cs through Rn carry decision receipts separating readiness from approval |
| Batch policy | Cs through Rn are held as a full span until At evidence is complete |
| State instances | Formal ion and isotope IDs derive electron and neutron counts without changing identity |
| Evidence seeds | H/C isotope evidence and selected common-ion candidate evidence are validated |
| Unresolved isotope/common-ion evidence | Snapshot isotope gaps and Level 1 common-ion gaps emit unresolved receipts |
| Isotope candidate evidence | Oxygen NIST isotope candidate receipt is recorded but not admitted |
| Physical-property evidence | 93 complete PubChem rows carry sourced standard-state, melting, boiling, and density values |
| Unresolved property evidence | 25 incomplete PubChem rows are recorded as unresolved receipts |
| Matter profiles | H through Xe combine identity, state, evidence, and bounded inference |
| Physical-property drift | PubChem physical-property source changes produce explicit drift reports |
| Relation graph | Level 1 same-group, same-period, and same-block graph |
| Schemas | JSON Schema for seed and snapshot records |
| API | Read-only local API for elements, snapshot, graph, dashboard, reasoning, f-block, and period-5 profiles |
| Verification | `python scripts/verify_repo.py` and `python -m pytest -q` pass |

## Source Policy

The source policy is:

```text
evaluated source evidence > classroom heuristic
official revised value > hard-coded old value
missing evidence > guessed value
```

Current source anchors:

| Source | Role |
| --- | --- |
| IUPAC public periodic table | Public periodic-table baseline |
| CIAAW Standard Atomic Weights 2024 | Atomic-weight evidence and unavailable-weight boundaries |
| NIST electronic configurations | Neutral and first-cation configuration evidence |
| PubChem periodic table CSV | Level 2 chemistry fields and `GroupBlock` classifications |

## Phase History

### Phase 0: Naming and Boundary

Applied:

```text
MSPEE-118 element-engine boundary
source-backed periodic-table records
explicit non-claims for full simulation and production readiness
```

Refinement:

```text
The project is standalone. Broader infrastructure may exist in the repo, but the
current product boundary is the periodic-table element engine.
```

### Phase 1: Seed Elements

Original target:

```text
H through Ca
```

Current state:

```text
H through Xe are Level 1 seed records
H through Xe also carry partial Level 2 PubChem chemistry fields
```

Core invariant:

```text
atomic_number = proton_count
neutral_electron_count = atomic_number
```

### Phase 2: Transition Metal Exception Kernel

Current state:

```text
Sc through Zn and Y through Cd use transition frontier signatures
Cr stores [Ar] 3d^5 4s^1 as source-backed state
Cu stores [Ar] 3d^10 4s^1 as source-backed state
simple Aufbau values remain audit candidates
```

Correction achieved:

```text
outer ns only is insufficient for transition metals
outer ns + inner (n-1)d jointly shape behavior
```

### Phase 3: Period-5 and F-Block Preparation

The historical plan treated Rb through Xe as the next full seed expansion. The
repository first implemented a safer intermediate layer:

```text
Rb through Xe = snapshot-level Level 2 chemistry profiles
not full Level 1 seed records
```

Reason:

```text
Full seed promotion requires source-backed neutral configuration,
first-cation configuration, valence signature, and relation edges.
The PubChem chemistry data alone is not enough to claim that promotion.
```

The current repository has now completed the full Rb-Xe seed promotion by adding
source-backed electron configurations, first-cation configurations, valence
signatures, configuration audits, and relation edges for Z=37..54. The compact
period-5 profile layer remains as a PubChem chemistry projection.

The f-block profile layer is also implemented as bounded relevance flags:

```text
La through Lu = lanthanide profile
Ac through Lr = actinide profile
```

It does not assign exact isotope half-lives or exact f-orbital occupancies.

The next snapshot-only span now has an explicit promotion gate:

```text
Cs through Rn = Level 1 promotion-readiness profiles
status = blocked until source-backed Level 1 evidence is added
```

This layer lists available evidence, missing evidence, and blockers before any
record is promoted into the seed pack.

The first blocker class is now partially closed:

```text
Cs through Rn = NIST configuration evidence overlay
fields = neutral configuration + first-cation configuration + configuration audit
still not full Level 1 seed promotion
```

The second blocker class is now also closed as an overlay:

```text
Cs through Rn = frontier and valence-signature overlay
derived from NIST neutral configuration evidence
still not oxidation-state, behavior-tag, or relation-edge promotion
```

The third blocker class is now closed as an overlay:

```text
Cs through Rn = PubChem oxidation-state evidence overlay
fields = oxidation_states + PubChem GroupBlock context
still not behavior-tag or relation-edge promotion
```

The fourth blocker class is now closed as an overlay:

```text
Cs through Rn = bounded behavior-tag overlay
inputs = configuration evidence + frontier/valence overlay + oxidation evidence
still not relation-edge promotion
```

The fifth blocker class is now closed as an overlay:

```text
Cs through Rn = relation-edge overlay
inputs = snapshot position + frontier overlay + oxidation evidence + behavior overlay
readiness result = 31 ready, At blocked by physical-property evidence gap
```

The readiness result now feeds an explicit decision receipt layer:

```text
Cs through Rn = promotion decision receipts
ready records = promotion_ready_pending_approval
At = promotion_blocked_unresolved_physical_property
approved records = 0
```

Readiness is not the same as approval. The receipts prevent silent mutation of
the Level 1 seed pack while preserving the causal reason each element can or
cannot advance.

The batch decision is now fixed:

```text
policy = hold_full_cs_rn_span
cause = At still lacks complete physical-property evidence
seed_mutation_allowed = false
invariant = Level 1 seed pack remains contiguous through Xe
```

This rejects partial promotion of the 31 ready records because it would create a
Level 1 seed-span hole at Z=85.

The At source check remains unresolved:

```text
source = PubChem Periodic Table CSV
At.BoilingPoint = blank
gap receipt = MSPEE-PHYSICAL-PROPERTY-GAP-Z085-At
gap status = awaiting_authoritative_source_value
promotion impact = blocks Cs-Rn full-span promotion
```

The governed secondary-source policy is now defined:

```text
policy count = 25
candidate source count = 5
gap closures by policy = 0
seed mutation allowed by policy = 0
```

The policy allows candidate source review, but it does not import values or close
any physical-property gap without a field-specific evidence receipt.

The field-specific receipt workflow now exists:

```text
secondary evidence receipts = 8
admitted secondary evidence = 0
seed mutation allowed = 0
At LANL candidate = 337 degC normalized to 610.15 K
Fr LANL candidate = 680 degC normalized to 953.15 K
Fr WebElements density candidate = 2900 kg/m3 normalized to 2.9 g/cm3
Pa LANL candidate = 4027 degC normalized to 4300.15 K
Bk LANL candidate = 2627 degC normalized to 2900.15 K
Cf LANL candidate = 1470 degC normalized to 1743.15 K
Cf RSC density candidate = 15.1 g/cm3
Es LANL candidate = 996 degC normalized to 1269.15 K
At admission decision = not admitted due secondary-source conflict
Fr admission decision = not admitted due secondary-source conflict
Fr density admission decision = not admitted pending corroboration
Pa admission decision = not admitted due secondary-source conflict
Bk admission decision = not admitted pending corroboration
Cf boiling-point admission decision = not admitted pending corroboration
Cf density admission decision = not admitted pending review
Es boiling-point admission decision = not admitted pending corroboration
At conflict resolution = blocked pending higher-precedence source
Fr conflict resolution = blocked pending higher-precedence source
Fr density corroboration review = blocked pending corroborating source
Pa conflict resolution = blocked pending higher-precedence source
Bk corroboration review = blocked pending corroborating source
Cf boiling-point corroboration review = blocked pending corroborating source
Cf density source review = resolved candidate after WebElements corroborates the RSC density value
Cf density gap-closure decision = ready pending operator approval, no seed mutation
Cf density closure approval = deferred, no gap closure, no seed mutation
Cf density seed update = blocked by deferred approval, no gap closure, no seed mutation
physical-property escalations = 8 conflict/corroboration/approval receipts, no gap closure
At/Fr/Pa escalation search = no higher-precedence boiling-point source found, no gap closure
Fr density corroboration search = no independent source found, no gap closure
Bk boiling-point corroboration search = no independent source found, no gap closure
Cf boiling-point corroboration search = no independent source found, no gap closure
Es boiling-point corroboration search = no independent source found, no gap closure
escalation-resolution recommendations = 7 receipts, no final resolution applied
operator decisions = 7 deferred receipts, no final resolution applied
continued-evidence plans = 7 plans, no final resolution applied
Es boiling-point corroboration review = blocked pending corroborating source
Fm no-candidate review = blocked because checked sources provide no admissible boiling-point or density value
Md no-candidate review = blocked because checked sources provide no admissible boiling-point or density value
No no-candidate review = blocked because checked sources provide no admissible boiling-point or density value
Lr no-candidate review = blocked because checked sources provide no admissible boiling-point or density value
gap workplan = 25 items, zero gap closures
source-search receipts = Pa and Bk candidate receipts created
partial-source-search receipts = 7 open searches, 14 field searches
O isotope candidate evidence = NIST O-16/O-17/O-18 candidate receipt created, no admission
At template = available for boiling_point_k
```

This gives the project a concrete input shape for a future At boiling-point
source while preserving the boundary that a reviewed candidate is not admitted
evidence.

The LANL candidate is now formally not admitted:

```text
decision = secondary_evidence_not_admitted_conflict
cause = LANL/Chemicool/Lenntech align near 337 degC, RSC lists 350 degC
gap closure = false
seed mutation allowed = false
```

The conflict is now a first-class receipt:

```text
resolution = blocked_pending_higher_precedence_source
LANL cluster = 337 degC / 610.15 K
RSC cluster = 350 degC / 623.15 K
gap closure = false
```

### State Instance Boundary

The identity/state separation is now executable for ion and isotope examples:

```text
MSPEE-Z011-Na-ion-plus-1
MSPEE-Z017-Cl-ion-minus-1
MSPEE-Z006-C-isotope-14
```

Ion instances apply:

```text
electron_count = atomic_number - charge
```

Isotope instances apply:

```text
neutron_count = mass_number - atomic_number
```

This layer validates state identity only. It does not yet claim isotope abundance,
half-life, decay mode, isotope-specific mass, or common-ion stability evidence.

### Evidence Seed Boundary

The state-instance layer now has a first bounded evidence overlay:

```text
isotope evidence: H-1, H-2, C-12, C-13, C-14
common-ion candidate evidence: Na+, Mg2+, Cl-, Ca2+, Fe2+, Fe3+, Cu+, Cu2+, Zn2+
```

Correction achieved:

```text
derived isotope/ion counts are not measured evidence
measured isotope fields carry source keys
common-ion records are candidate evidence, not universal stability claims
unresolved isotope/common-ion gaps are explicit receipts, not silent absence
```

### Physical-Property Evidence Boundary

The measured-property layer is now separated from symbolic behavior inference:

```text
physical-property coverage: all complete PubChem rows
unresolved-property coverage: all incomplete PubChem rows
fields: standard_state, melting_point_k, boiling_point_k, density_value
source: PubChem Periodic Table CSV
```

Correction achieved:

```text
measured physical properties are evidence records
behavior tags remain symbolic/inferred unless separately sourced
standard-state examples now cover gas, liquid, and solid cases
arsenic preserves a source phase-transition anomaly with an explicit note
incomplete rows are left unresolved instead of guessed
physical-property evidence now has a dedicated PubChem drift checker
```

### Matter-Behavior Profile Boundary

The first matter-facing profile layer is now implemented for the promoted Level 1
seed elements:

```text
matter profiles: H through Xe
input chain: identity + symbolic state + measured physical evidence
output: bounded inferred matter-behavior tags
```

Correction achieved:

```text
profile does not predict reactions
profile does not model compounds
profile does not replace measured condition-specific data
```

## Current Constructive Deltas

| Delta | Current result |
| --- | --- |
| Idea -> runnable seed | Seed records validate and emit receipts |
| 20 elements -> 54 seed records | H through Xe are Level 1 records |
| Partial table -> full identity snapshot | All 118 named elements are queryable |
| Constant atomic weight -> typed evidence | Single, interval, and unavailable models are explicit |
| Simple shell filling -> configuration audit | Cr/Cu exceptions are first-class records |
| Visual table -> relation graph | Level 1 elements expose reasoned relation edges |
| CLI-only -> API/dashboard | Read-only JSON surfaces exist |
| f-block future idea -> bounded overlay | Lanthanide and actinide profiles exist without overclaiming |
| Beyond Kr future idea -> period-5 seed promotion | Rb-Xe now have full Level 1 seeds and compact chemistry profiles |
| Informal state examples -> validated state instances | Ion and isotope IDs now derive electron and neutron counts |
| Derived state IDs -> bounded evidence records | H/C isotope evidence and common-ion candidates carry source lineage |
| Missing isotope/common-ion data -> unresolved receipts | Evidence gaps are queryable without guessed values |
| Behavior-only matter profile -> measured evidence seed | 93 complete PubChem rows expose physical-property evidence |
| Missing measured property -> unresolved receipt | 25 incomplete PubChem rows are explicit unresolved evidence |
| Unresolved property -> gap audit | 25 source-gap receipts now separate missing source fields from promotion impact |
| Gap audit -> workplan | 25 unresolved property gaps are prioritized without closing gaps |
| Workplan -> source-search receipt | Pa and Bk now have completed source-search receipts linked to candidate evidence |
| Workplan -> partial-source-search receipt | Fr, Cf, Es, Fm, Md, No, and Lr now have two-field search receipts |
| Gap audit -> secondary-source policy | 25 policies define admission requirements without closing gaps |
| Policy -> secondary evidence workflow | At, Fr, Pa, Bk, Cf, Es, and Fr density candidates exist, with zero admitted receipts |
| Candidate -> admission decision | At, Fr, Pa, Bk, Cf, Es, and Fr density candidates are reviewed but not admitted |
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
| Evidence seed -> matter profile | H through Xe now expose bounded matter-behavior read models |
| Static property evidence -> drift-checkable property boundary | PubChem physical-property changes now produce explicit drift reports |
| Snapshot-only Cs-Rn -> promotion-readiness audit | Cs through Rn now expose missing evidence before Level 1 promotion |
| Missing Cs-Rn configuration evidence -> NIST overlay | Cs through Rn now expose neutral and first-cation configuration evidence |
| Missing Cs-Rn frontier signatures -> derived overlay | Cs through Rn now expose outer shell, d/f/p shell context, and stability flags |
| Missing Cs-Rn oxidation evidence -> PubChem overlay | Cs through Rn now expose sourced oxidation-state sets |
| Missing Cs-Rn behavior tags -> bounded inference overlay | Cs through Rn now expose controlled behavior tags with explicit basis |
| Missing Cs-Rn relation edges -> evidence mesh overlay | Cs through Rn now expose reasoned relation edges |
| Readiness result -> decision receipt | Cs through Rn now separate promotion readiness from seed-mutation approval |
| Decision ambiguity -> batch policy | Cs-Rn now have a full-span hold policy until At is resolved |

## Fracture Deltas Avoided

| Risk | Guard |
| --- | --- |
| Treating atomic weight as eternal | Atomic weights are source-backed and versioned |
| Treating ion state as element identity | Identity remains proton-count based |
| Treating isotope state as element identity | Isotope state changes neutron count, not proton identity |
| Treating simple Aufbau as authority | NIST-backed configuration wins |
| Claiming all transition metals behave the same | Frontier signatures distinguish d-shell states |
| Claiming measured facts from inferred tags | Source fields and inference flags are separated |
| Promoting incomplete data | Rb-Xe promotion required source-backed Level 1 fields; Cs-Rn promotion requires decision receipts |
| Inventing f-block precision | Phase 3 f-block profiles are bounded relevance flags |
| Treating common-ion candidates as guaranteed behavior | Candidate evidence is separated from universal stability claims |
| Treating missing isotope/common-ion data as invisible | Unresolved receipts make evidence gaps explicit |
| Mixing measured property with symbolic behavior | Physical properties are stored as separate source-backed evidence |
| Treating profile as simulator | Matter profiles declare reaction and compound non-claims |
| Silently skipping Cs-Rn gaps | Promotion-readiness profiles preserve explicit blockers |
| Treating evidence overlay as promotion | Cs-Rn remain blocked until behavior and relation layers exist |
| Treating frontier overlay as full chemistry | Frontier signatures remain structural overlays, not behavior tags or relation edges |
| Treating oxidation evidence as universal behavior | Oxidation states remain source evidence, not guaranteed compound behavior |
| Treating behavior tags as measured fact | Tags are labeled as symbolic inference and carry source-evidence basis |
| Treating relation edges as substitutability | Relation edges carry reasons and do not claim equivalent compound behavior |
| Treating readiness as approval | Decision receipts require explicit approval before seed mutation |
| Creating a Level 1 seed hole | Batch policy holds the span instead of promoting 31 records around At |
| Treating a blank source field as zero | Gap audit records `source_row_incomplete` and enforces no-guess policy |
| Treating policy as evidence | Secondary-source policy closes zero gaps and allows zero seed mutations |
| Treating a candidate as admitted evidence | Admission decision blocks LANL because secondary sources conflict |
| Treating a conflict as resolved | Conflict receipt keeps At blocked pending higher-precedence evidence |

## Verification Commands

```powershell
python scripts\verify_repo.py
python -m pytest -q
```

Expected verifier summary:

```text
element_seeds=54
element_snapshot_records=118
f_block_profiles=30
period_5_level_2_profiles=18
physical_property_gap_audit_receipts=25
physical_property_gap_work_items=25
physical_property_source_search_receipts=2
partial_physical_property_source_search_receipts=7
physical_property_secondary_source_policies=25
physical_property_secondary_evidence_receipts=8
physical_property_secondary_evidence_admission_decisions=8
physical_property_conflict_resolution_receipts=3
physical_property_corroboration_review_receipts=4
physical_property_review_receipts=1
physical_property_gap_closure_decisions=1
physical_property_closure_approval_receipts=1
physical_property_seed_update_receipts=1
physical_property_escalation_receipts=8
physical_property_escalation_search_receipts=7
physical_property_escalation_resolution_receipts=7
physical_property_operator_decision_receipts=7
physical_property_continued_evidence_plans=7
physical_property_no_candidate_review_receipts=4
isotope_candidate_evidence_receipts=1
promotion_decision_receipts=32
promotion_batch_policy=hold_full_cs_rn_span
standard_files=ok
```

## Next Build Boundary

The strongest next step is not to claim "all matter" yet. The next stable
engineering steps are:

```text
1. Resolve Astatine physical-property evidence gap before full Cs-Rn seed promotion.
2. Resolve measured-property gaps as complete authoritative values become available.
3. Resolve At boiling-point conflict receipt with a higher-precedence field source.
4. Collect field-specific candidate evidence for partial-property targets without gap closure.
5. Find higher-precedence Pa evidence and corroborating Bk evidence before any gap closure.
6. Expand isotope evidence beyond H/C with sourced abundance, half-life, and decay data.
7. Continue sourced Level 2 chemistry values beyond Xenon.
8. Expand matter-behavior profiles as identity, state, measured property, and environment coverage grows.
```
