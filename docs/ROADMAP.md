# MSPEE Periodic Table Roadmap

## Current Product Boundary

MSPEE-118 is a standalone periodic-table element engine. The active scope is:

```text
source-backed element records
-> validated identity/state separation
-> relation graph
-> bounded chemistry profiles
-> read-only API and dashboard projections
-> symbolic causal chain process
```

See `docs/PROJECT_HISTORY.md` for the origin-to-current implementation history.
See `docs/DEVELOPMENT_MODEL_COMPARISON.md` for how sandbox phase documents are
converted into verified repository work.
See `docs/SYMBOLIC_CAUSAL_FOUNDATION.md` for the first-principles symbol model.

## Immediate Target

```text
Sandbox phase input
-> boundary classification
-> source/evidence requirement
-> typed model
-> validator and tests
-> CLI/API exposure when useful
-> verifier receipt
```

## Maturity Ladder

```text
M0 = concept only
M1 = model implemented
M2 = tests pass
M3 = persisted with receipts
M4 = signed / validated
M5 = exposed through API
M6 = visible in dashboard
M7 = demo-ready
M8 = production-engineering-ready
```

## Engine Split

```text
1. Element science model
2. Evidence / receipt model
3. Runtime / storage / release model
4. Product interface / dashboard model
```

## Completed Build Path

```text
1. Claim boundary compiler
2. Receipt ledger
3. Phase registry
4. Release evidence bundle
5. Robust evidence network
6. MSPEE first-36 element seed pack
7. Full 118-element source snapshot workflow with source-drift check
8. JSON Schema export for element and snapshot records
9. Graph export for element relation queries
10. Local API for element lookup, schemas, and graph queries
11. Dashboard-facing view model
12. Level 2 oxidation-state and electronegativity boundaries
13. Sourced Level 2 chemistry values for the first 36 elements
14. Source drift check for first-36 Level 2 chemistry values
15. Ionization-energy and bond-tendency boundary contracts
16. Sourced first-ionization-energy values for the first 36 elements
17. Transition-metal exception kernel and elements 21-36 frontier audits
18. Lanthanide-actinide expansion kernel with bounded f-block relevance flags
19. Source-backed bond-tendency classifications for the first 36 elements
20. Period-5 Level 2 chemistry profile projection for Rb-Xe
21. Source-drift checker for the Rb-Xe period-5 Level 2 snapshot overlay
22. Full Level 1 seed promotion for Rb-Xe using source-backed configurations
23. Formal ion instance IDs and validation
24. Formal isotope instance IDs and validation
25. Bounded isotope evidence seed for H-Ca isotope examples
26. Common-ion candidate evidence seed tied to sourced oxidation states
27. Measured physical-property evidence for all complete PubChem rows
28. Bounded matter-behavior profiles for H through Xe
28a. Atom behavior v2 profiles for source-backed H-Kr isotope evidence
28b. Atom behavior v2 gap receipts and workplan for unresolved isotope-backed profile coverage
28c. Isotope source policies for 18 Level 1 atom behavior isotope-only blockers
28d. Isotope source-search receipts for 18 Level 1 atom behavior isotope-only blockers
28e. Oxygen NIST isotope candidate evidence admitted into canonical isotope evidence
28f. Oxygen isotope candidate admission receipt for canonical evidence closure
28g. Element readiness scoring for evidence completeness, source confidence, behavior readiness, gap priority, and constraint tension
29. Source-drift checker for physical-property evidence
30. Unresolved physical-property evidence receipts for incomplete PubChem rows
31. Unresolved isotope and common-ion evidence receipts
32. Cs-Rn Level 1 promotion-readiness profiles
33. Cs-Rn NIST configuration evidence overlay
34. Cs-Rn frontier and valence-signature overlay
35. Cs-Rn oxidation-state evidence overlay
36. Cs-Rn bounded behavior-tag overlay
37. Cs-Rn relation-edge overlay
38. Cs-Rn promotion decision receipts
39. Cs-Rn full-span hold batch policy
40. Physical-property gap audit receipts
41. Physical-property secondary-source admission policy
42. Physical-property secondary evidence receipt workflow
43. At secondary evidence admission conflict decision
44. At physical-property conflict-resolution receipt
45. Physical-property gap workplan queue
46. Pa/Bk physical-property source-search receipts
47. Pa/Bk secondary-evidence admission decisions
48. Pa conflict-resolution and Bk corroboration-review receipts
49. Partial physical-property source-search receipts for Fr/Cf/Es/Fm/Md/No/Lr
50. Fr boiling-point candidate and conflict-resolution receipts
51. Cf candidate admission, corroboration, and source-review receipts
52. Es boiling-point candidate admission and corroboration-review receipts
53. Fm no-candidate source review receipt
54. Md no-candidate source review receipt
55. No/Lr no-candidate source review receipts
56. Fr density candidate admission and corroboration-review receipt
57. Cf density gap-closure decision pending operator approval
58. Cf density closure-approval receipt deferred
59. Cf density seed-update receipt blocked by deferred approval
60. Physical-property escalation receipts for blocked evidence work
61. At physical-property escalation-search receipt with no higher-precedence source found
62. Fr physical-property escalation-search receipt with no higher-precedence source found
63. Pa physical-property escalation-search receipt with no higher-precedence source found
64. Fr density corroboration-search receipt with no independent source found
65. Bk boiling-point corroboration-search receipt with no independent source found
66. Cf boiling-point corroboration-search receipt with no independent source found
67. Es boiling-point corroboration-search receipt with no independent source found
68. Escalation-resolution recommendation receipts for all blocked searches
69. Deferred operator-decision receipts for all blocked recommendations
70. Continued-evidence plans for deferred operator decisions
```

## Next Build Order

```text
1. Resolve Astatine physical-property evidence gap before full Cs-Rn seed promotion
2. Resolve measured-property gaps as authoritative complete values become available
3. Resolve At boiling-point conflict receipt with a higher-precedence field source
4. Execute continued-evidence plans or convert deferred operator decisions into explicit approvals/rejections
5. Decide whether to approve or reject Cf density seed update through explicit operator approval
6. Collect source-specific isotope evidence receipts under the isotope source policy
7. Continue sourced Level 2 chemistry values beyond Xenon
8. Expand matter-behavior profiles beyond Xenon after evidence coverage expands
9. Expand atom behavior v2 after isotope evidence coverage expands
10. Graph query interface for behavior, uncertainty, and source provenance
```
