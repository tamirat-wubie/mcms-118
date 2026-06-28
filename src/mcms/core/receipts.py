from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json

@dataclass(frozen=True)
class Receipt:
    receipt_key: str
    receipt_type: str
    payload: dict
    previous_hash: str = ""

    def canonical_payload(self) -> str:
        return json.dumps(
            {
                "receipt_key": self.receipt_key,
                "receipt_type": self.receipt_type,
                "payload": self.payload,
                "previous_hash": self.previous_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def receipt_hash(self) -> str:
        return sha256(self.canonical_payload().encode("utf-8")).hexdigest()

    def to_dict(self) -> dict:
        return {
            "receipt_key": self.receipt_key,
            "receipt_type": self.receipt_type,
            "payload": self.payload,
            "previous_hash": self.previous_hash,
            "receipt_hash": self.receipt_hash(),
        }


def validate_hash_chain(receipts: list[Receipt]) -> bool:
    expected = ""
    for receipt in receipts:
        if receipt.previous_hash != expected:
            return False
        expected = receipt.receipt_hash()
    return True
