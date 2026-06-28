# Security Policy

## Supported versions

This repository is currently a scaffold and early implementation package. Security fixes target the `main` branch until a stable release policy is declared.

## Reporting a vulnerability

Open a private security advisory on GitHub if available. If not available, contact the maintainer directly before creating a public issue.

Do not include secrets, tokens, private keys, production credentials, or sensitive logs in public issues.

## Security boundaries

This project does not claim security certification or legal compliance. Security features are engineering controls that must be independently reviewed before production use.

Default posture:

```text
high-risk action -> deny by default
secret value -> never log/export
signature failure -> block
restore mismatch -> block
missing evidence -> review required
```
