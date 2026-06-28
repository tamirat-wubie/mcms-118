from __future__ import annotations

import json
from pathlib import Path


def load_phase_registry(path: str | Path | None = None) -> list[dict]:
    if path is None:
        path = Path(__file__).resolve().parents[3] / "docs" / "PHASE_REGISTRY.json"
    return json.loads(Path(path).read_text(encoding="utf-8"))


def latest_phase(path: str | Path | None = None) -> dict:
    phases = load_phase_registry(path)
    return max(phases, key=lambda item: item["phase"])
