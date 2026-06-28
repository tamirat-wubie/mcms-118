from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json

REQUIRED_EVIDENCE_ITEMS = {
    "policy_decision",
    "session_receipt",
    "abac_decision",
    "cicd_receipt",
    "artifact_signature",
    "sbom",
    "vulnerability_scan",
    "secret_state",
    "checkpoint",
    "restore_drill",
    "approval",
}

@dataclass(frozen=True)
class ReleaseEvidenceItem:
    evidence_key: str
    evidence_type: str
    evidence_hash: str
    evidence_strength: float

    def validate(self) -> list[str]:
        errors = []
        if not self.evidence_key:
            errors.append("evidence_key is required.")
        if not self.evidence_type:
            errors.append("evidence_type is required.")
        if not self.evidence_hash:
            errors.append("evidence_hash is required.")
        if self.evidence_strength < 0:
            errors.append("evidence_strength cannot be negative.")
        return errors

    def to_dict(self) -> dict:
        return self.__dict__.copy()

@dataclass
class ReleaseEvidenceBundleResult:
    bundle_key: str
    release_key: str
    evidence_count: int
    missing_evidence_types: list[str]
    bundle_hash: str
    mean_evidence_strength: float
    bundle_status: str
    evidence_items: list[dict]
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def build_release_evidence_bundle(bundle_key: str, release_key: str, evidence_items: list[ReleaseEvidenceItem], require_all: bool = True) -> ReleaseEvidenceBundleResult:
    if not bundle_key or not release_key or any(item.validate() for item in evidence_items):
        return ReleaseEvidenceBundleResult(bundle_key, release_key, len(evidence_items), [], "", 0.0, "insufficient_data", [item.to_dict() for item in evidence_items], "Release evidence bundle input is invalid.")
    present = {item.evidence_type for item in evidence_items}
    missing = sorted(REQUIRED_EVIDENCE_ITEMS - present) if require_all else []
    canonical = json.dumps([item.to_dict() for item in sorted(evidence_items, key=lambda item: item.evidence_key)], sort_keys=True, separators=(",", ":"))
    bundle_hash = sha256(canonical.encode("utf-8")).hexdigest()
    mean_strength = sum(item.evidence_strength for item in evidence_items) / len(evidence_items) if evidence_items else 0.0
    if not evidence_items:
        status = "evidence_bundle_missing_items"
        explanation = "Release evidence bundle has no evidence items."
    elif missing:
        status = "evidence_bundle_missing_items"
        explanation = "Release evidence bundle is missing required evidence types."
    elif mean_strength < 0.7:
        status = "evidence_bundle_conflict"
        explanation = "Release evidence bundle has weak evidence strength."
    else:
        status = "evidence_bundle_complete"
        explanation = "Release evidence bundle is complete."
    return ReleaseEvidenceBundleResult(bundle_key, release_key, len(evidence_items), missing, bundle_hash, mean_strength, status, [item.to_dict() for item in evidence_items], explanation)
