from __future__ import annotations

from dataclasses import dataclass

@dataclass
class SARIFSeverityTaxonomyResult:
    taxonomy_key: str
    rule_id: str
    level: str
    security_severity: float | None
    suppressed: bool
    tags: list[str]
    taxonomy_status: str
    blocks_release: bool
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def classify_sarif_severity_taxonomy(taxonomy_key: str, rule_id: str, level: str, security_severity: float | None, suppressed: bool, tags: list[str]) -> SARIFSeverityTaxonomyResult:
    if not taxonomy_key or not rule_id or level not in {"none", "note", "warning", "error"}:
        return SARIFSeverityTaxonomyResult(taxonomy_key, rule_id, level, security_severity, suppressed, tags, "insufficient_data", True, "SARIF taxonomy input is invalid.")
    if suppressed:
        status="sarif_suppressed"; blocks=False; explanation="SARIF result is suppressed by approved mapping."
    elif security_severity is not None and security_severity >= 9.0:
        status="sarif_security_critical"; blocks=True; explanation="SARIF result is critical severity."
    elif security_severity is not None and security_severity >= 7.0:
        status="sarif_security_high"; blocks=True; explanation="SARIF result is high severity."
    elif level == "error":
        status="sarif_error"; blocks=True; explanation="SARIF result is error-level."
    elif level == "warning":
        status="sarif_warning"; blocks=False; explanation="SARIF result is warning-level."
    elif level == "note":
        status="sarif_note"; blocks=False; explanation="SARIF result is note-level."
    else:
        status="sarif_taxonomy_clear"; blocks=False; explanation="SARIF result does not block release."
    if "security" in tags and level == "none" and not suppressed:
        status="sarif_taxonomy_conflict"; blocks=True; explanation="SARIF result has security tag but no severity level."
    return SARIFSeverityTaxonomyResult(taxonomy_key, rule_id, level, security_severity, suppressed, tags, status, blocks, explanation)
