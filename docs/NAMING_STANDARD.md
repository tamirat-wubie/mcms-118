# Naming Standard

## Canonical Identity

```text
Project code: MSPEE-118
Canonical name: MSPEE-118 Element Engine
Formal name: Mullusi Standard Symbolic Periodic Element Engine
Repository name: mcms-118
Distribution package: mcms-118
Python import namespace: mcms
CLI command: mcms
License: Apache-2.0
Version: 0.1.0
```

`mcms-118` and `mcms` remain repository/package compatibility names. The active
standalone element-engine identity is `MSPEE-118`.

## File Naming

```text
phase id: MCMS-118-P###
phase markdown: docs/phases/phase_###.md
phase metadata: docs/phase_metadata/phase_###.json
element module: src/mcms/elements/<snake_case>.py
test: tests/test_<snake_case>.py
```

The existing phase registry still uses `MCMS-118-P###` identifiers for continuity.
Do not rename generated phase metadata unless a migration plan updates every
registry, test, and verifier reference.

## Naming Rules

- Use `MSPEE-118` as the public element-engine project code.
- Use `MSPEE-118 Element Engine` as the readable project name.
- Use `mcms-118` for the GitHub repository and Python distribution package.
- Use `mcms` for Python imports and CLI namespace.
- Use `snake_case` for Python modules and test files.
- Use `kebab-case` only for repository names, slugs, and URLs.
- Keep unsupported chemistry, physics, and production claims explicit in every
  phase and release artifact.
