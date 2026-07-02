# Architecture

MSPEE-118 is the active standalone element-engine profile in this repository.
Supporting MCMS modules remain for receipts, phase metadata, release evidence,
and future matter-behavior work, but the current science-facing boundary is the
periodic-table element engine.

## Engine Split

```text
1. Element science model
   identity, laws, state, state instances, source evidence, chemistry fields, promotion readiness, promotion decisions, batch policy, matter profiles, atom behavior profiles, and relation graph

2. Evidence and receipt model
   source references, configuration/isotope/common-ion/physical-property evidence, unresolved receipts, drift checks, and audit notes

3. Runtime and release model
   CLI, scripts, verification, schemas, release evidence, and package metadata

4. Product interface model
   JSON API, dashboard read model, graph export, and documentation
```

## Element Record

```text
element_record := identity + laws + state + exposure + history

identity = atomic number, symbol, name, proton count
laws = identity, charge, isotope, shell-capacity, and conservation rules
state = configuration, periodic position, atomic-weight model, and chemistry fields
exposure = human card, JSON, graph, dashboard, and API projections
history = source references, derivation trace, audit notes, and validation status
```

## Current Coverage

```text
Level 1 seed pack: Z=1..54, H through Xe
Full identity/weight snapshot: Z=1..118
Transition frontier kernel: Sc-Zn and Y-Cd
P-block d-core context: Ga-Kr and In-Xe
F-block profile overlay: La-Lu and Ac-Lr
Period-5 chemistry profile projection: Rb-Xe
Promotion-readiness audit profiles: Cs-Rn
Configuration evidence overlay: Cs-Rn
Frontier/valence signature overlay: Cs-Rn
Oxidation-state evidence overlay: Cs-Rn
Behavior-tag overlay: Cs-Rn
Relation-edge overlay: Cs-Rn
Promotion decision receipts: Cs-Rn
Promotion batch policy: full Cs-Rn span ready for approval review, zero seed mutation authority
Partial promotion eligibility: 32 ready Cs-Rn records exposed for review, zero seed mutation authority
Full-span promotion approval review: open for Cs-Rn, zero seed mutation authority
Ion/isotope state instances: derived electron and neutron count validators
Isotope/common-ion evidence seeds: H-Ca isotope evidence and selected common-ion candidates
Unresolved isotope/common-ion evidence: snapshot and Level 1 evidence gaps
Physical-property evidence: 94 complete rows, including admitted At secondary-source evidence
Unresolved physical-property evidence: 25 incomplete PubChem rows
Physical-property gap audits: 25 PubChem source-gap receipts, zero Cs-Rn promotion blockers
Physical-property gap workplan: 25 items, zero gap closures
Physical-property source-search receipts: 2 Pa/Bk searches with candidate receipts created
Partial physical-property source-search receipts: 7 open searches, 14 field searches
Secondary-source policy: 25 physical-property gap policies, zero gaps closed by policy alone
Secondary-source evidence: 8 At/Fr/Pa/Bk/Cf/Es candidate receipts, one At value admitted for readiness
Secondary-source admission: 8 decisions, one At gap closure, zero seed mutations
Physical-property conflict resolution: 3 At/Fr/Pa receipts, one At gap closure, zero seed mutations
Physical-property corroboration review: 4 Fr density and Bk/Cf/Es boiling-point receipts, zero gap closures
Physical-property source review: 1 Cf density receipt, zero gap closures
Physical-property gap closure: 1 Cf density decision, ready pending approval, zero seed mutations
Physical-property closure approval: 1 Cf density receipt, approval deferred, zero seed mutations
Physical-property seed update: 1 Cf density receipt, blocked by deferred approval, zero seed mutations
Physical-property escalations: 7 receipts for remaining conflict, corroboration, and approval blocks, zero seed mutations
Physical-property escalation search: 6 receipts, including Fr/Pa boiling-point investigations and Fr/Bk/Cf/Es corroboration searches
Physical-property escalation resolution: 6 recommendation receipts, zero final resolutions applied
Physical-property operator decisions: 6 deferred receipts, zero approvals or rejections applied
Physical-property continued evidence: 6 plans, zero final resolutions or seed mutations applied
Physical-property no-candidate review: 4 Fm/Md/No/Lr receipts, zero gap closures
Matter-behavior profiles: H-Xe
Atom behavior v2 profiles: 178 source-backed H-Xe isotope profiles including Tc-99 radioisotope evidence
Atom behavior v2 gaps: 64 receipts and 64 work items for unresolved isotope-backed profile coverage
Isotope source policies: zero Level 1 atom behavior isotope-only blockers, zero gaps closed by policy
Isotope source-search receipts: zero open searches and zero active candidate receipts
Isotope candidate evidence: 0 active receipts after Oxygen and Technetium admission
Isotope candidate admission: 2 O/Tc admission receipts, zero active candidate retention
Element readiness scores: 118 read-only score records for evidence completeness, source confidence, behavior readiness, gap priority, and constraint tension
```

## Boundary

The engine validates and exposes source-backed element records. It does not claim
complete reaction prediction, full quantum simulation, complete isotope physics,
laboratory certification, or score-based evidence admission.
