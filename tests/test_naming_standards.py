from pathlib import Path

from mcms.phase_registry import list_phases
from mcms.standards import PROJECT_IDENTITY, validate_phase_naming


def test_project_identity_is_standardized():
    assert PROJECT_IDENTITY.project_code == "MCMS-118"
    assert PROJECT_IDENTITY.repository_name == "mcms-118"
    assert PROJECT_IDENTITY.distribution_name == "mcms-118"
    assert PROJECT_IDENTITY.import_namespace == "mcms"
    assert PROJECT_IDENTITY.license == "Apache-2.0"


def test_standard_docs_exist():
    for path in [
        "LICENSE",
        "NOTICE",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "docs/NAMING_STANDARD.md",
        "docs/STANDARDS_PROFILE.md",
        "docs/ARCHITECTURE.md",
        "docs/CLAIM_BOUNDARY_STANDARD.md",
        "docs/EVIDENCE_STANDARD.md",
        "docs/RELEASE_POLICY.md",
    ]:
        assert Path(path).exists(), path


def test_every_phase_uses_canonical_naming():
    for phase in list_phases():
        assert validate_phase_naming(phase), phase["phase_id"]
        assert phase["project_identity"]["repository_name"] == "mcms-118"
        assert phase["standards_profile"]["policy_posture"].startswith("deny")
        assert phase["canonical_identifiers"]["phase_id"] == phase["phase_id"]
