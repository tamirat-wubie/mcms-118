from __future__ import annotations

from dataclasses import dataclass

MATURITY = {
    "M0": "concept only",
    "M1": "symbolic model implemented",
    "M2": "tests pass",
    "M3": "persisted with receipts",
    "M4": "signed / governed",
    "M5": "exposed through API",
    "M6": "visible in dashboard",
    "M7": "demo-ready",
    "M8": "production-engineering-ready",
}

@dataclass(frozen=True)
class CapabilityMaturity:
    capability_key: str
    level: str
    evidence: str = ""

    def validate(self) -> bool:
        return bool(self.capability_key) and self.level in MATURITY

    def to_dict(self) -> dict:
        return {
            "capability_key": self.capability_key,
            "level": self.level,
            "meaning": MATURITY.get(self.level, "unknown"),
            "evidence": self.evidence,
            "valid": self.validate(),
        }
