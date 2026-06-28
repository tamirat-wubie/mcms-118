from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import hmac
import json

@dataclass
class SignedWaiverEntryResult:
    waiver_key: str
    target_gate: str
    scope_key: str
    expires_at_ms: int
    now_ms: int
    signer_key: str
    entry_hash: str
    signature: str
    verified: bool
    signed_waiver_status: str
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def canonical_waiver_payload(waiver_key: str, target_gate: str, scope_key: str, expires_at_ms: int, signer_key: str) -> bytes:
    return json.dumps({"waiver_key": waiver_key, "target_gate": target_gate, "scope_key": scope_key, "expires_at_ms": expires_at_ms, "signer_key": signer_key}, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_or_verify_waiver_entry(waiver_key: str, target_gate: str, scope_key: str, expires_at_ms: int, now_ms: int, signer_key: str, secret_key: bytes, expected_signature: str = "") -> SignedWaiverEntryResult:
    if not waiver_key or not target_gate or not scope_key or expires_at_ms < 0 or now_ms < 0 or not signer_key or not secret_key:
        return SignedWaiverEntryResult(waiver_key, target_gate, scope_key, expires_at_ms, now_ms, signer_key, "", "", False, "insufficient_data", "Signed waiver input is invalid.")
    payload = canonical_waiver_payload(waiver_key, target_gate, scope_key, expires_at_ms, signer_key)
    entry_hash = sha256(payload).hexdigest()
    signature = hmac.new(secret_key, payload, sha256).hexdigest()
    if now_ms > expires_at_ms:
        status="waiver_entry_expired"; verified=False; explanation="Waiver entry is expired."
    elif scope_key in {"*", "global", "all"}:
        status="waiver_entry_scope_invalid"; verified=False; explanation="Waiver entry scope is invalid."
    elif expected_signature:
        verified = hmac.compare_digest(signature, expected_signature)
        status = "waiver_entry_verified" if verified else "waiver_entry_signature_invalid"
        explanation = "Waiver entry signature verified." if verified else "Waiver entry signature is invalid."
    else:
        verified=True; status="waiver_entry_signed"; explanation="Waiver entry signature is created."
    return SignedWaiverEntryResult(waiver_key, target_gate, scope_key, expires_at_ms, now_ms, signer_key, entry_hash, signature, verified, status, explanation)
