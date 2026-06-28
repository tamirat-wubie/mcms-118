from __future__ import annotations

import argparse
import json

from mcms.core.boundaries import compile_claim_boundary
from mcms.core.phases import latest_phase, load_phase_registry
from mcms.elements import (
    build_element_receipt,
    get_seed_element,
    list_seed_elements,
    validate_seed_pack,
)
from mcms.release.robust_evidence_network import analyze_robust_evidence_network


def cmd_demo() -> None:
    claim = compile_claim_boundary("NaCl is a compound made of sodium and chlorine", "source_backed_claim", 0.8)
    evidence = analyze_robust_evidence_network("release/demo", evidence_strength=0.9)
    print(json.dumps({"claim": claim.to_dict(), "robust_evidence": evidence.to_dict()}, indent=2))


def cmd_phases() -> None:
    phases = load_phase_registry()
    print(json.dumps({"count": len(phases), "latest": latest_phase()}, indent=2))


def cmd_elements(symbol: str | None, list_only: bool) -> None:
    if list_only:
        elements = list_seed_elements()
        print(
            json.dumps(
                {
                    "count": len(elements),
                    "symbols": [element.identity.symbol for element in elements],
                    "validation": validate_seed_pack().to_dict(),
                },
                indent=2,
            )
        )
        return
    if symbol:
        element = get_seed_element(symbol)
        print(
            json.dumps(
                {
                    "element": element.to_dict(),
                    "receipt": build_element_receipt(element),
                },
                indent=2,
            )
        )
        return
    print(json.dumps(validate_seed_pack().to_dict(), indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="mcms")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    sub.add_parser("phases")
    elements_parser = sub.add_parser("elements")
    elements_parser.add_argument("--symbol", help="Element symbol, name, or atomic number")
    elements_parser.add_argument("--list", action="store_true", help="List MSPEE seed elements")
    args = parser.parse_args(argv)
    if args.cmd == "demo":
        cmd_demo()
    elif args.cmd == "phases":
        cmd_phases()
    elif args.cmd == "elements":
        cmd_elements(args.symbol, args.list)


if __name__ == "__main__":
    main()
