from mcms.release.adapter_sandbox_policy import evaluate_adapter_sandbox_policy
from mcms.release.http_retry_backoff_client import evaluate_http_retry_backoff
from mcms.release.github_pagination_etag_cache import evaluate_github_pagination_etag_cache
from mcms.release.sarif_severity_taxonomy import classify_sarif_severity_taxonomy
from mcms.release.signed_waiver_entries import sign_or_verify_waiver_entry
from mcms.release.compressed_evidence_archive import build_compressed_evidence_archive
from mcms.release.environment_snapshot_replay import replay_environment_snapshot
from mcms.release.robust_evidence_network import analyze_robust_evidence_network


def test_sandbox_policy_ready():
    result = evaluate_adapter_sandbox_policy("p", "opa", "opa", ["opa"], False, "readonly", [], [], 5, 1000)
    assert result.sandbox_status == "sandbox_policy_ready"


def test_retry_after_honored():
    result = evaluate_http_retry_backoff("r", 429, 0, 3, 120, None, 1000)
    assert result.retry_status == "retry_after_header_honored"


def test_github_next_page_detected():
    result = evaluate_github_pagination_etag_cache("c", "/path", 200, "", "", '<https://api.github.com/page=2>; rel="next"', 1, 10)
    assert result.cache_status == "github_next_page_detected"


def test_sarif_critical_blocks():
    result = classify_sarif_severity_taxonomy("t", "rule", "error", 9.8, False, ["security"])
    assert result.blocks_release is True
    assert result.taxonomy_status == "sarif_security_critical"


def test_signed_waiver_entry():
    result = sign_or_verify_waiver_entry("w", "sarif", "release/1/finding/1", 2000, 1000, "operator/A", b"secret")
    assert result.verified is True


def test_compressed_archive_signed():
    sections = {"opa": {}, "github": {}, "cosign": {}, "sbom": {}, "sarif": {}, "waivers": {}, "slsa": {}, "environment_snapshot": {}, "promotion_replay": {}}
    _, result = build_compressed_evidence_archive("a", "release/1", sections, "sig")
    assert result.archive_status == "compressed_archive_signature_verified"


def test_environment_replay_match():
    env = {"policy_version": "v1"}
    result = replay_environment_snapshot("s", "release/1", env, env)
    assert result.replay_status == "environment_snapshot_replay_matched"


def test_robust_network_ready():
    result = analyze_robust_evidence_network("release/1", evidence_strength=0.9)
    assert result.network_status == "reproducible_promotion_ready"
