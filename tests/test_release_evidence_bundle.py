from mcms.release.release_evidence_bundle import ReleaseEvidenceItem, build_release_evidence_bundle


def test_release_bundle_complete():
    types = ["policy_decision", "session_receipt", "abac_decision", "cicd_receipt", "artifact_signature", "sbom", "vulnerability_scan", "secret_state", "checkpoint", "restore_drill", "approval"]
    items = [ReleaseEvidenceItem(t, t, f"h-{t}", 0.9) for t in types]
    result = build_release_evidence_bundle("bundle/1", "release/1", items)
    assert result.bundle_status == "evidence_bundle_complete"
