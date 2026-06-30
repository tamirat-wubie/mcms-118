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
Promotion batch policy: hold full Cs-Rn span pending At evidence
Ion/isotope state instances: derived electron and neutron count validators
Isotope/common-ion evidence seeds: H/He/C/N/O isotope evidence and selected common-ion candidates
Unresolved isotope/common-ion evidence: snapshot and Level 1 evidence gaps
Physical-property evidence: 93 complete PubChem rows
Unresolved physical-property evidence: 25 incomplete PubChem rows
Physical-property gap audits: 25 receipts, At blocks Cs-Rn
Physical-property gap workplan: 25 items, zero gap closures
Physical-property source-search receipts: 2 Pa/Bk searches with candidate receipts created
Partial physical-property source-search receipts: 7 open searches, 14 field searches
Secondary-source policy: 25 physical-property gap policies, zero gaps closed by policy alone
Secondary-source evidence: 8 At/Fr/Pa/Bk/Cf/Es candidate receipts, zero admitted receipts
Secondary-source admission: 8 blocked decisions, zero gap closures
Physical-property conflict resolution: 3 At/Fr/Pa receipts, zero gap closures
Physical-property corroboration review: 4 Fr density and Bk/Cf/Es boiling-point receipts, zero gap closures
Physical-property source review: 1 Cf density receipt, zero gap closures
Physical-property gap closure: 1 Cf density decision, ready pending approval, zero seed mutations
Physical-property closure approval: 1 Cf density receipt, approval deferred, zero seed mutations
Physical-property seed update: 1 Cf density receipt, blocked by deferred approval, zero seed mutations
Physical-property escalations: 8 receipts for conflict, corroboration, and approval blocks, zero seed mutations
Physical-property escalation search: 7 receipts, including At/Fr/Pa boiling-point investigations and Fr/Bk/Cf/Es corroboration searches
Physical-property escalation resolution: 7 recommendation receipts, zero final resolutions applied
Physical-property operator decisions: 7 deferred receipts, zero approvals or rejections applied
Physical-property continued evidence: 7 plans, zero final resolutions or seed mutations applied
Physical-property no-candidate review: 4 Fm/Md/No/Lr receipts, zero gap closures
Matter-behavior profiles: H-Xe
Atom behavior v2 profiles: 13 source-backed H/He/C/N/O isotope profiles
Atom behavior v2 gaps: 113 receipts and 113 work items for unresolved isotope-backed profile coverage
Isotope source policies: 49 Level 1 atom behavior isotope-only blockers, zero gaps closed by policy
Isotope source-search receipts: 49 open searches and zero active candidate receipts
Isotope candidate evidence: 0 active receipts after Oxygen admission
Isotope candidate admission: 1 Oxygen admission receipt, zero active candidate retention
```

## Boundary

The engine validates and exposes source-backed element records. It does not claim
complete reaction prediction, full quantum simulation, complete isotope physics,
or laboratory certification.
