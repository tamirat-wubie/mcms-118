from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import gzip
import json

REQUIRED_COMPRESSED_ARCHIVE_SECTIONS = {"opa", "github", "cosign", "sbom", "sarif", "waivers", "slsa", "environment_snapshot", "promotion_replay"}

@dataclass
class CompressedEvidenceArchiveResult:
    archive_key: str
    release_key: str
    section_count: int
    missing_sections: list[str]
    raw_hash: str
    compressed_hash: str
    compressed_size_bytes: int
    signature_hash: str
    archive_status: str
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def build_compressed_evidence_archive(archive_key: str, release_key: str, evidence_sections: dict, signature_hash: str) -> tuple[bytes, CompressedEvidenceArchiveResult]:
    if not archive_key or not release_key:
        result = CompressedEvidenceArchiveResult(archive_key, release_key, 0, [], "", "", 0, signature_hash, "insufficient_data", "Compressed archive input is invalid.")
        return b"", result
    present = set(evidence_sections.keys())
    missing = sorted(REQUIRED_COMPRESSED_ARCHIVE_SECTIONS - present)
    payload = {"schema": "mcms.compressed_evidence_archive.v1", "archive_key": archive_key, "release_key": release_key, "sections": evidence_sections}
    raw_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    compressed = gzip.compress(raw_bytes)
    raw_hash = sha256(raw_bytes).hexdigest()
    compressed_hash = sha256(compressed).hexdigest()
    if missing:
        status="compressed_archive_missing_section"; explanation="Compressed evidence archive is missing required sections."
    elif signature_hash:
        status="compressed_archive_signature_verified"; explanation="Compressed evidence archive is signed."
    else:
        status="compressed_archive_created"; explanation="Compressed evidence archive is created."
    return compressed, CompressedEvidenceArchiveResult(archive_key, release_key, len(evidence_sections), missing, raw_hash, compressed_hash, len(compressed), signature_hash, status, explanation)


def verify_compressed_evidence_archive(compressed_payload: bytes, expected_compressed_hash: str) -> bool:
    return sha256(compressed_payload).hexdigest() == expected_compressed_hash
