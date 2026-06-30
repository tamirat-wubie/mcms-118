# MSPEE-118 Element Engine

**Repository:** `mcms-118`
**Python package:** `mcms-118`
**Import namespace:** `mcms`
**CLI:** `mcms`
**License:** `Apache-2.0`
**Version:** `0.1.0`

MSPEE-118 is a standalone periodic-table element engine. It turns periodic-table
rows into typed, source-backed element records with identity, laws, state,
exposure surfaces, provenance, validation, and relation graphs.

The deeper project foundation treats every represented thing as a governed
symbol:

```text
S := <I, L, Sigma, Gamma, H>
```

The element engine is the first verified domain instance of that symbolic causal
chain model.

The project is not a full chemistry simulator. It is a structured element and
matter-behavior seed: source facts remain separated from derived validation,
symbolic behavior flags, and future physics extensions.

```text
element_record := identity + laws + state + exposure + history

identity := atomic_number + symbol + name + proton_count
state := electron_configuration + periodic_position + atomic_weight_model + chemistry_fields
history := source_references + derivation_trace + audit_notes
```

## Boundary

This repository currently focuses on the standalone element engine. It does not
claim legal certification, production customer readiness, physical laboratory
validation, autonomous real-world action approval, full reaction prediction, full
quantum simulation, or complete isotope physics.

## Current Implementation

```text
src/mcms/elements/
  typed element contracts
  first-54 Level 1 seed records, H through Xe
  full 118-element identity and atomic-weight snapshot
  Phase 2 transition-metal exception kernel for Sc through Kr
  Chromium and copper configuration exception audits
  period-4 p-block filled d-core context
  Phase 3 f-block profiles for lanthanides and actinides
  period-5 Level 2 chemistry profiles for Rb through Xe
  Cs-Rn promotion-readiness profiles
  NIST configuration evidence for Cs through Rn
  frontier and valence signatures for Cs through Rn
  oxidation-state evidence for Cs through Rn
  behavior-tag overlays for Cs through Rn
  relation-edge overlays for Cs through Rn
  promotion decision receipts for Cs through Rn
  span-level Cs-Rn promotion batch policy receipt
  formal ion and isotope state-instance IDs
  bounded isotope and common-ion evidence seeds
  unresolved isotope and common-ion evidence receipts
  measured physical-property evidence for H through Po and Rn
  unresolved physical-property evidence receipts
  physical-property gap audit receipts
  physical-property gap workplan queue
  physical-property source-search receipts for Pa and Bk
  partial physical-property source-search receipts for Fr/Cf/Es/Fm/Md/No/Lr
  secondary-source policy for physical-property gaps
  secondary-source evidence receipt workflow for physical-property gaps
  admission decisions for At, Fr, Pa, Bk, Cf, Es, and Fr density secondary evidence candidates
  conflict-resolution receipts for At, Fr, and Pa secondary evidence disagreements
  corroboration-review receipts for Bk and Cf secondary evidence candidates
  physical-property source-review receipt for the Cf density candidate
  physical-property gap-closure decision for corroborated Cf density
  physical-property closure-approval receipt deferred for Cf density
  physical-property seed-update receipt blocked for Cf density
  physical-property escalation receipts for unresolved conflict, corroboration, and approval work
  physical-property escalation-search receipts for At/Fr/Pa higher-precedence investigation and Fr/Bk/Cf/Es corroboration
  physical-property escalation-resolution recommendation receipts for blocked searches
  physical-property operator-decision receipts deferred for blocked recommendations
  physical-property continued-evidence plans for deferred operator decisions
  physical-property no-candidate review receipts for Fm, Md, No, and Lr
  bounded matter-behavior profiles
  relation graph export
  JSON Schema export
  dashboard read model
  local read-only API
```

The rest of the repository contains supporting scaffolds from the broader project
history, including claim-boundary, receipt, phase-registry, and release-evidence
modules. Those surfaces are useful infrastructure, but the active science-facing
boundary is the MSPEE element engine.

## Source Anchors

MSPEE keeps source-backed values separate from inference:

| Source | Used for |
| --- | --- |
| CIAAW/IUPAC Standard Atomic Weights 2024 | Atomic-weight displays and unavailable-weight boundaries |
| NIST Electronic Configurations of the Elements | Neutral and first-cation configuration seed evidence |
| PubChem Periodic Table CSV | Oxidation states, Pauling electronegativity, ionization energy, and `GroupBlock` classes |

Source drift checkers are included for CIAAW atomic-weight snapshot data and
PubChem Level 2 chemistry data.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e '.[dev]'
python scripts\verify_repo.py
python -m pytest -q
```

Useful element commands:

```powershell
python -m mcms.cli elements --symbol H
python -m mcms.cli elements --symbol Zn
python -m mcms.cli elements --full --symbol Og
python -m mcms.cli elements --schema bundle
python -m mcms.cli elements --graph --symbol Zn --relation same_block
python -m mcms.cli elements --dashboard --symbol Zn --relation same_block
python -m mcms.cli elements --symbol Na --ion-charge 1
python -m mcms.cli elements --symbol C --isotope-mass 14
python -m mcms.cli elements --symbol C --isotope-mass 14 --atom-behavior
python -m mcms.cli elements --symbol O --atom-behavior-gap
python -m mcms.cli elements --symbol Rn --atom-behavior-workplan
python -m mcms.cli elements --symbol O --isotope-source-policy
python -m mcms.cli elements --symbol O --isotope-source-search
python -m mcms.cli elements --symbol O --isotope-candidate-evidence
python -m mcms.cli elements --symbol C --isotope-mass 14 --isotope-evidence
python -m mcms.cli elements --symbol Fe --common-ion-evidence
python -m mcms.cli elements --symbol At --configuration-evidence
python -m mcms.cli elements --symbol Au --frontier-valence
python -m mcms.cli elements --symbol Au --oxidation-state-evidence
python -m mcms.cli elements --symbol Au --behavior-tags
python -m mcms.cli elements --symbol Au --relation-overlay
python -m mcms.cli elements --symbol Br --physical-property-evidence
python -m mcms.cli elements --symbol At --physical-property-gap-audit
python -m mcms.cli elements --symbol At --physical-property-secondary-source-policy
python -m mcms.cli elements --symbol At --physical-property-secondary-evidence-template
python -m mcms.cli elements --symbol Br --matter-profile
python -m mcms.cli elements --symbol At --promotion-readiness
python -m mcms.cli elements --symbol Au --promotion-decision
python -m mcms.cli elements --promotion-batch-policy
python -m mcms.cli api --host 127.0.0.1 --port 8765
```

Source drift checks:

```powershell
python scripts\check_element_snapshot_drift.py --fail-on-drift
python scripts\check_element_level2_drift.py --fail-on-drift
python scripts\check_element_level2_drift.py --scope period-5 --fail-on-drift
python scripts\check_element_physical_property_drift.py --fail-on-drift
```

## Local API

Start the API:

```powershell
python -m mcms.cli api --host 127.0.0.1 --port 8765
```

Key routes:

| Route | Result |
| --- | --- |
| `GET /health` | API status and record counts |
| `GET /elements` | Level 1 seed symbols and validation summary |
| `GET /elements/{symbol}` | Level 1 seed record and receipt |
| `GET /snapshot` | Full 118-element snapshot summary |
| `GET /snapshot/{symbol}` | Snapshot identity and atomic-weight record |
| `GET /schemas/{seed\|snapshot\|atom-behavior\|bundle}` | JSON Schema export |
| `GET /graph?symbol=Zn&relation=same_block` | Filtered relation graph |
| `GET /dashboard?symbol=Zn&relation=same_block` | Dashboard read model |
| `GET /reasoning/configuration/Cr` | Chromium configuration exception explanation |
| `GET /reasoning/similarity?left=Cu&right=K` | Copper/potassium similarity explanation |
| `GET /instances/ion/Na?charge=1` | Formal ion instance with derived electron count |
| `GET /instances/isotope/C?mass_number=14` | Formal isotope instance with derived neutron count |
| `GET /atom/behavior/C?mass_number=14` | Atom behavior v2 profile with identity, isotope, electron, force, and non-claim boundaries |
| `GET /atom/behavior/gaps/O` | Atom behavior v2 source-gap receipt for missing isotope-backed profile coverage |
| `GET /atom/behavior/workplan/Rn` | Atom behavior v2 gap work item with dependency blockers |
| `GET /atom/behavior/isotope-source-policy/O` | Isotope source policy for atom behavior v2 isotope-only blockers |
| `GET /atom/behavior/isotope-source-search/O` | Isotope evidence source-search receipt under the atom behavior v2 policy |
| `GET /atom/behavior/isotope-candidate-evidence/O` | Source-specific Oxygen isotope candidate receipt pending admission |
| `GET /evidence/isotopes/C?mass_number=14` | Isotope evidence record, including C-14 half-life boundary |
| `GET /evidence/isotopes/unresolved/O` | Unresolved isotope evidence receipt |
| `GET /evidence/common-ions/Fe` | Common-ion candidate evidence from sourced oxidation states |
| `GET /evidence/common-ions/unresolved/O` | Unresolved common-ion evidence receipt |
| `GET /evidence/configurations/At` | NIST configuration evidence for Cs-Rn promotion readiness |
| `GET /evidence/oxidation-states/Au` | PubChem oxidation-state evidence for Cs-Rn promotion readiness |
| `GET /evidence/physical-properties/Br` | Measured physical-property evidence |
| `GET /evidence/physical-properties/unresolved/At` | Unresolved physical-property evidence receipt |
| `GET /evidence/physical-properties/gaps/At` | Physical-property gap audit receipt |
| `GET /evidence/physical-properties/workplan/At` | Prioritized physical-property gap work item |
| `GET /evidence/physical-properties/source-search/Pa` | Active physical-property source-search receipt |
| `GET /evidence/physical-properties/partial-source-search/Fr` | Active partial-property source-search receipt |
| `GET /evidence/physical-properties/secondary-evidence/admission/At` | Admission decision for secondary evidence |
| `GET /evidence/physical-properties/conflicts/At` | Conflict-resolution receipt for secondary evidence |
| `GET /evidence/physical-properties/corroboration/Bk` | Corroboration-review receipt for secondary evidence |
| `GET /evidence/physical-properties/review/Cf` | Source-review receipt for secondary evidence |
| `GET /evidence/physical-properties/gap-closure/Cf` | Gap-closure decision for reviewed secondary evidence |
| `GET /evidence/physical-properties/closure-approval/Cf` | Closure-approval receipt for reviewed secondary evidence |
| `GET /evidence/physical-properties/seed-update/Cf` | Blocked seed-update receipt for reviewed secondary evidence |
| `GET /evidence/physical-properties/escalations/At` | Escalation receipt for blocked physical-property work |
| `GET /evidence/physical-properties/escalation-search/At` | Source-investigation receipt for blocked escalation work |
| `GET /evidence/physical-properties/escalation-resolution/At` | Resolution recommendation receipt for blocked escalation work |
| `GET /evidence/physical-properties/operator-decisions/At` | Deferred operator-decision receipt for blocked recommendation |
| `GET /evidence/physical-properties/continued-evidence/At` | Continued-evidence plan for deferred operator decision |
| `GET /evidence/physical-properties/escalation-search/Fr` | Source-investigation receipt for blocked escalation work |
| `GET /evidence/physical-properties/escalation-search/Pa` | Source-investigation receipt for blocked escalation work |
| `GET /evidence/physical-properties/no-candidate/Fm` | No-candidate review receipt for secondary evidence |
| `GET /evidence/physical-properties/no-candidate/Md` | No-candidate review receipt for secondary evidence |
| `GET /evidence/physical-properties/no-candidate/No` | No-candidate review receipt for secondary evidence |
| `GET /evidence/physical-properties/no-candidate/Lr` | No-candidate review receipt for secondary evidence |
| `GET /evidence/physical-properties/secondary-evidence/template/At` | Secondary evidence receipt template |
| `GET /evidence/physical-properties/secondary-source-policy/At` | Secondary-source admission policy |
| `GET /frontier/cs-rn/Au` | Frontier and valence signature overlay |
| `GET /behavior/cs-rn/Au` | Bounded behavior-tag overlay |
| `GET /relations/cs-rn/Au` | Relation-edge overlay |
| `GET /matter/profiles/Br` | Bounded matter-behavior profile |
| `GET /promotion/cs-rn` | Cs-Rn Level 1 promotion-readiness audit profiles |
| `GET /promotion/cs-rn/At` | Single promotion-readiness audit profile |
| `GET /promotion/batch-policy` | Cs-Rn span-level promotion policy receipt |
| `GET /promotion/decisions/Au` | Promotion decision receipt, pending approval |
| `GET /promotion/decisions/At` | Promotion decision receipt, blocked by unresolved property evidence |
| `GET /phase3/f-block` | Lanthanide/actinide profile list |
| `GET /level2/period-5` | Rb-Xe snapshot Level 2 chemistry profiles |

## Documentation

```text
docs/MSPEE_ELEMENT_ENGINE.md   current element-engine specification
docs/SYMBOLIC_CAUSAL_FOUNDATION.md  first-principles symbolic model
docs/PROJECT_HISTORY.md        origin-to-current project history
docs/ROADMAP.md                next build order
docs/DEVELOPMENT_MODEL_COMPARISON.md  sandbox-vs-repository development model
docs/NAMING_STANDARD.md        naming and compatibility rules
```

## Verification Status

The repository verifier checks the element engine, snapshot, schemas, relation
graph, API routes, f-block profiles, and period-5 chemistry overlay:

```text
element_seeds=54
element_snapshot_records=118
f_block_profiles=30
period_5_level_2_profiles=18
isotope_evidence_records=5
common_ion_evidence_records=9
unresolved_isotope_evidence_records=116
unresolved_common_ion_evidence_records=47
physical_property_evidence_records=93
unresolved_physical_property_evidence_records=25
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
matter_behavior_profiles=54
atom_behavior_profiles=5
atom_behavior_gap_receipts=116
atom_behavior_gap_work_items=116
isotope_source_policies=52
isotope_source_search_receipts=52
isotope_candidate_evidence_receipts=1
cs_rn_promotion_readiness_profiles=32
configuration_evidence_records=32
frontier_valence_signature_records=32
oxidation_state_evidence_records=32
behavior_tag_overlay_records=32
relation_overlay_records=32
promotion_decision_receipts=32
promotion_batch_policy=hold_full_cs_rn_span
```
