import json
from pathlib import Path

from mcms.phase_registry import list_phases, phase_metadata_summary

REQUIRED_KEYS = {
    "phase", "phase_id", "slug", "title", "status", "maturity", "domain", "layer",
    "objective", "capability_chain", "relationships", "boundary", "blocked_claims", "invariants",
    "claim_types", "evidence_policy", "risk_profile", "artifacts", "modules", "module_count",
    "status_vocabulary", "inputs", "outputs", "implementation_truth", "upgrade_path", "audit_metadata", "project_identity", "standards_profile", "canonical_identifiers",
}


def test_every_phase_has_enriched_metadata():
    phases = list_phases()
    assert len(phases) == 135
    for phase in phases:
        assert REQUIRED_KEYS <= set(phase)
        assert phase["phase_id"] == f"MCMS-118-P{phase['phase']:03d}"
        assert phase["boundary"]
        assert "blocked_claims" in phase
        assert "artifacts" in phase
        assert phase["artifacts"]["phase_doc"].endswith(f"phase_{phase['phase']:03d}.md")


def test_per_phase_json_files_match_registry():
    for phase in list_phases():
        path = Path(phase["artifacts"]["phase_metadata_json"])
        assert path.exists(), path
        disk = json.loads(path.read_text())
        assert disk["phase"] == phase["phase"]
        assert disk["phase_id"] == phase["phase_id"]
        assert disk["capability_chain"] == phase["capability_chain"]


def test_phase_metadata_summary_contains_core_fields():
    summary = phase_metadata_summary(135)
    assert summary["phase"] == 135
    assert summary["phase_id"] == "MCMS-118-P135"
    assert summary["module_count"] >= 1
    assert "boundary" in summary
