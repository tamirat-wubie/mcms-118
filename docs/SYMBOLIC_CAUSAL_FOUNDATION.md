# Symbolic Causal Foundation

## Purpose

This document states the first-principles vision behind MSPEE-118 and the later
matter-engine trajectory. The current repository begins with chemical elements,
but the deeper goal is a general symbolic causal chain process for representing,
validating, reasoning about, and evolving structured things.

## Core Definition

A symbol is not only a mark, word, token, or label.

A symbol is a governed identity that preserves meaning through change.

```text
S := <I, L, Sigma, Gamma, H>
```

Where:

```text
I     = immutable identity / essence
L     = laws, constraints, validation rules
Sigma = mutable state / current content
Gamma = exposure boundary / interface / projection
H     = history, causal continuity, memory ledger
```

## Five Questions

Every valid symbol must answer five questions:

| Question | Symbol part |
| --- | --- |
| What makes it itself? | `I` |
| What governs its change? | `L` |
| What is its current state? | `Sigma` |
| What can be observed? | `Gamma` |
| How is continuity preserved? | `H` |

So the minimum symbolic object is:

```text
identity + law + state + interface + history
```

## Validity Kernel

A symbol is valid only when its mutable state obeys its governing laws without
violating immutable identity:

```text
valid(S) iff Sigma satisfies L over I
```

Plain meaning:

```text
state may change
identity must remain stable
law decides whether the change is allowed
history records the accepted or rejected change
```

## Lawful Change

A symbol may change only through a validated transformation:

```text
propose_delta(Sigma_t, delta, context)

if L_validate(I, Sigma_t, delta, context) = true:
    Sigma_t+1 = L_apply(Sigma_t, delta, context)
    H_t+1 = H_t + receipt(I, Sigma_t, delta, decision, Sigma_t+1)
else:
    Sigma_t+1 = Sigma_t
    H_t+1 = H_t + rejection_receipt(I, Sigma_t, delta, decision)
```

No valid edit means no state change.

## Exposure Rule

The observer does not automatically receive the whole symbol. Exposure is
controlled by `Gamma`:

```text
view = Gamma(S, observer, purpose, permission)
```

Plain meaning:

```text
Gamma exposes what is allowed without leaking what must remain protected.
```

## Information Membership

Information belongs inside a symbol only if it can be lawfully validated or
inferred:

```text
info in S iff L_inference proves info under policy
```

This is the anti-hallucination rule for the project:

```text
unsupported information is not attached as fact
missing information becomes an unresolved receipt
inference is labeled as inference
measured data is source-backed
```

## Element Instance

An element is the first concrete domain where this symbolic model is being
implemented.

```text
element_symbol := <I_element, L_element, Sigma_element, Gamma_element, H_element>
```

For an element:

| Symbol part | Element meaning |
| --- | --- |
| `I` | atomic number, symbol, name, proton-count identity |
| `L` | identity law, charge law, isotope law, shell-capacity law, validation rules |
| `Sigma` | electron configuration, atomic weight model, frontier state, evidence fields, behavior flags |
| `Gamma` | JSON, CLI, API, graph, dashboard, human card |
| `H` | source references, derivation trace, receipts, gap audits, decision records |

## Symbolic Causal Chain Process

The intended process is:

```text
Input
-> symbolize
-> validate identity
-> attach laws
-> attach state
-> attach evidence
-> detect gaps and conflicts
-> reason or compute within declared limits
-> expose answer through Gamma
-> emit receipt into H
-> compare with reality when source or experiment exists
-> refine model without breaking identity
```

This is the bridge from static element records to reasoning, computation,
prediction, testing, comparison with reality, and research workflows.

## Research Trajectory

The complete trajectory is:

```text
1. Detailed symbolic element records
2. Source-backed physical and chemical evidence
3. Computable element comparison
4. Symbolic reaction episodes
5. Symbolic compounds and species
6. Material-state representations
7. Search and discovery over the evidence graph
8. Prediction and experiment planning with explicit uncertainty
9. Reality comparison through source, measurement, or experiment
10. Causal memory and model refinement
```

## Current Implementation Boundary

The current repository is not yet the full matter engine. It is the first
verified layer:

```text
source-backed element records
identity/state separation
electron configuration audits
physical-property evidence and gaps
promotion readiness and decision receipts
read-only CLI/API exposure
repository verifier
```

Future phases must not skip this sequence:

```text
vision -> boundary -> source/evidence -> model -> validator -> tests -> exposure -> verifier
```

## Adjustment To Development Practice

Every new capability should be treated as a symbolic causal chain object:

```text
new_capability := <I, L, Sigma, Gamma, H>
```

For example, a future reaction engine must define:

```text
I     = reaction identity
L     = conservation, charge, stoichiometry, evidence rules
Sigma = reactants, products, state changes, conditions
Gamma = explanation/API/graph views
H     = source data, validation receipt, unresolved assumptions
```

The same applies to compounds, materials, predictions, experiments, and search.

## Status

```text
foundation_status = defined
first_domain_instance = element engine
current_verified_boundary = H through Xe Level 1 plus full 118 snapshot and evidence overlays
next_practical_step = source-specific secondary evidence receipt for At boiling point
```
