"""Minimal MCMS vertical slice demo: claim boundary + receipt."""

from __future__ import annotations

from mcms.core.boundaries import compile_claim_boundary
from mcms.core.receipts import create_receipt


def main() -> None:
    claim = "NaCl is a compound made of sodium and chlorine."
    boundary = compile_claim_boundary(claim, evidence_strength=0.8, claim_type="source_backed_claim")
    receipt = create_receipt("demo/chemistry_claim", boundary.to_dict())
    print(boundary.to_dict())
    print(receipt.to_dict())


if __name__ == "__main__":
    main()
