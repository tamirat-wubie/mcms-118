from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mcms.elements import (  # noqa: E402
    list_full_snapshot_records,
    list_seed_elements,
    validate_full_snapshot,
    validate_seed_pack,
)
from mcms.module_registry import all_modules  # noqa: E402
from mcms.phase_registry import list_phases  # noqa: E402

REQUIRED_KEYS = {
    "phase", "phase_id", "slug", "title", "status", "maturity", "domain", "layer",
    "objective", "capability_chain", "relationships", "boundary", "blocked_claims", "invariants",
    "claim_types", "evidence_policy", "risk_profile", "artifacts", "modules", "module_count",
    "status_vocabulary", "inputs", "outputs", "implementation_truth", "upgrade_path", "audit_metadata",
}

STANDARD_FILES = (
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/NAMING_STANDARD.md",
    "docs/STANDARDS_PROFILE.md",
)


def main() -> None:
    phases = list_phases()
    modules = all_modules()
    elements = list_seed_elements()
    snapshot_records = list_full_snapshot_records()
    element_seed_result = validate_seed_pack(elements)
    snapshot_result = validate_full_snapshot(snapshot_records)
    assert len(phases) == 135, len(phases)
    assert len(modules) >= 180, len(modules)
    assert len(elements) == 20, len(elements)
    assert len(snapshot_records) == 118, len(snapshot_records)
    assert element_seed_result.validation_status == "element_seed_pack_validated", element_seed_result
    assert not element_seed_result.invalid_elements, element_seed_result.invalid_elements
    assert snapshot_result.validation_status == "full_element_snapshot_validated", snapshot_result
    assert not snapshot_result.invalid_elements, snapshot_result.invalid_elements
    for phase in phases:
        missing = REQUIRED_KEYS - set(phase)
        assert not missing, (phase["phase"], sorted(missing))
        assert phase["phase_id"].startswith("MCMS-118-P")
        assert phase["artifacts"]["phase_metadata_json"]
        path = Path(phase["artifacts"]["phase_metadata_json"])
        assert path.exists(), path
        disk = json.loads(path.read_text())
        assert disk["phase"] == phase["phase"]
    print(
        f"phases={len(phases)} modules={len(modules)} "
        f"metadata_files={len(phases)} element_seeds={len(elements)} "
        f"element_snapshot_records={len(snapshot_records)}"
    )


def verify_standard_files() -> None:
    for standard_file in STANDARD_FILES:
        if not Path(standard_file).exists():
            raise SystemExit(f"missing standard file: {standard_file}")
    print("standard_files=ok")


if __name__ == "__main__":
    main()
    verify_standard_files()
