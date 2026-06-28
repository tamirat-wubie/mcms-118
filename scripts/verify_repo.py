from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mcms.phase_registry import list_phases
from mcms.module_registry import all_modules

REQUIRED_KEYS = {
    "phase", "phase_id", "slug", "title", "status", "maturity", "domain", "layer",
    "objective", "capability_chain", "relationships", "boundary", "blocked_claims", "invariants",
    "claim_types", "evidence_policy", "risk_profile", "artifacts", "modules", "module_count",
    "status_vocabulary", "inputs", "outputs", "implementation_truth", "upgrade_path", "audit_metadata",
}


def main() -> None:
    phases = list_phases()
    modules = all_modules()
    assert len(phases) == 135, len(phases)
    assert len(modules) >= 180, len(modules)
    for phase in phases:
        missing = REQUIRED_KEYS - set(phase)
        assert not missing, (phase["phase"], sorted(missing))
        assert phase["phase_id"].startswith("MCMS-118-P")
        assert phase["artifacts"]["phase_metadata_json"]
        path = Path(phase["artifacts"]["phase_metadata_json"])
        assert path.exists(), path
        disk = json.loads(path.read_text())
        assert disk["phase"] == phase["phase"]
    print(f"phases={len(phases)} modules={len(modules)} metadata_files={len(phases)}")


if __name__ == "__main__":
    main()


# Standard naming checks appended by package standardization.
from pathlib import Path as _Path
for _p in ["LICENSE", "SECURITY.md", "CONTRIBUTING.md", "docs/NAMING_STANDARD.md", "docs/STANDARDS_PROFILE.md"]:
    if not _Path(_p).exists():
        raise SystemExit(f"missing standard file: {_p}")
print("standard_files=ok")
