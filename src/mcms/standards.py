from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectIdentity:
    project_code: str
    canonical_name: str
    repository_name: str
    distribution_name: str
    import_namespace: str
    cli_name: str
    license: str
    version: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


PROJECT_IDENTITY = ProjectIdentity(
    project_code='MCMS-118',
    canonical_name='MCMS-118 — Causal Matter Standard',
    repository_name='mcms-118',
    distribution_name='mcms-118',
    import_namespace='mcms',
    cli_name='mcms',
    license='Apache-2.0',
    version='0.1.0',
)

PHASE_ID_PREFIX = "MCMS-118-P"
PHASE_DOC_PATTERN = "docs/phases/phase_{phase:03d}.md"
PHASE_METADATA_PATTERN = "docs/phase_metadata/phase_{phase:03d}.json"

BLOCKED_CLAIMS = {
    "legal_compliance_claim",
    "security_certified_claim",
    "production_customer_ready_claim",
    "medical_claim",
    "neurological_or_cognitive_claim",
    "diagnostic_or_treatment_claim",
    "financial_operation_claim",
    "autonomous_real_world_action_claim",
    "AGI_claim",
    "ASI_claim",
}


def expected_phase_id(phase: int) -> str:
    return f"{PHASE_ID_PREFIX}{phase:03d}"


def expected_phase_doc(phase: int) -> str:
    return PHASE_DOC_PATTERN.format(phase=phase)


def expected_phase_metadata(phase: int) -> str:
    return PHASE_METADATA_PATTERN.format(phase=phase)


def validate_phase_naming(record: dict) -> bool:
    phase = int(record["phase"])
    return (
        record.get("phase_id") == expected_phase_id(phase)
        and record.get("artifacts", {}).get("phase_doc") == expected_phase_doc(phase)
        and record.get("artifacts", {}).get("phase_metadata_json") == expected_phase_metadata(phase)
    )
