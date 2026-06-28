from __future__ import annotations

from dataclasses import dataclass

from .adapter_sandbox_policy import evaluate_adapter_sandbox_policy
from .http_retry_backoff_client import evaluate_http_retry_backoff
from .github_pagination_etag_cache import evaluate_github_pagination_etag_cache
from .jsonschema_binding_validator import validate_jsonschema_binding
from .sarif_severity_taxonomy import classify_sarif_severity_taxonomy
from .signed_waiver_entries import sign_or_verify_waiver_entry
from .compressed_evidence_archive import build_compressed_evidence_archive
from .environment_snapshot_replay import replay_environment_snapshot
from .reproducible_promotion_boundary import evaluate_reproducible_promotion_boundary

@dataclass
class RobustEvidenceNetworkResult:
    sandbox_policy: dict
    retry_backoff: dict
    github_cache: dict
    jsonschema_binding: dict
    sarif_taxonomy: dict
    signed_waiver: dict
    compressed_archive: dict
    environment_replay: dict
    reproducible_boundary: dict
    network_status: str
    explanation: str
    boundary: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def analyze_robust_evidence_network(release_key: str, evidence_strength: float = 0.9) -> RobustEvidenceNetworkResult:
    sandbox = evaluate_adapter_sandbox_policy("sandbox/opa", "opa", "opa", ["opa"], False, "readonly", [], [], 5, 100000)
    retry = evaluate_http_retry_backoff("request/1", 200, 0, 3, None, None, 1000)
    github = evaluate_github_pagination_etag_cache("cache/1", "/repos/o/r/actions/runs/1/artifacts", 200, "etag", "", "", 1, 10)
    schema = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
    js = validate_jsonschema_binding("schema/1", "basic", schema, {"name": "mcms"})
    sarif = classify_sarif_severity_taxonomy("sarif/1", "rule/1", "none", None, False, [])
    waiver = sign_or_verify_waiver_entry("waiver/1", "sarif", "release/1/finding/1", 2000, 1000, "operator/A", b"secret")
    sections = {"opa": {}, "github": {}, "cosign": {}, "sbom": {}, "sarif": {}, "waivers": {}, "slsa": {}, "environment_snapshot": {}, "promotion_replay": {}}
    _, archive = build_compressed_evidence_archive("archive/1", release_key, sections, "signature_hash")
    env = {"policy_version": "v1", "runner": "ubuntu"}
    env_replay = replay_environment_snapshot("snapshot/1", release_key, env, env)
    boundary = evaluate_reproducible_promotion_boundary(release_key, sandbox.sandbox_status, retry.retry_status, github.cache_status, js.binding_status, sarif.taxonomy_status, waiver.signed_waiver_status, archive.archive_status, env_replay.replay_status, evidence_strength)
    return RobustEvidenceNetworkResult(sandbox.to_dict(), retry.to_dict(), github.to_dict(), js.to_dict(), sarif.to_dict(), waiver.to_dict(), archive.to_dict(), env_replay.to_dict(), boundary.to_dict(), boundary.boundary_status, boundary.explanation, "robust_release_evidence_network_not_certification_or_customer_ready_claim")
