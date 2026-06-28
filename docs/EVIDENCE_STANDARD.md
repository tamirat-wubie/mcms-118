# Evidence Standard

Evidence is explicit and cannot silently upgrade itself.

## Evidence states

```text
missing
generated
computed
source_backed
verified
signed
checkpointed
replayed
conflicted
blocked
```

## Minimum gates

```text
source-backed claim -> evidence_strength >= 0.7
high-risk action -> approval + receipt + policy gate
release promotion -> signed evidence bundle
waiver -> signed + scoped + time-limited
secret reference -> resolved without materializing value
```
