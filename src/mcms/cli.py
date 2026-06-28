from __future__ import annotations

import argparse
import json

from mcms.core.boundaries import compile_claim_boundary
from mcms.core.phases import latest_phase, load_phase_registry
from mcms.release.robust_evidence_network import analyze_robust_evidence_network


def cmd_demo() -> None:
    claim = compile_claim_boundary("NaCl is a compound made of sodium and chlorine", "source_backed_claim", 0.8)
    evidence = analyze_robust_evidence_network("release/demo", evidence_strength=0.9)
    print(json.dumps({"claim": claim.to_dict(), "robust_evidence": evidence.to_dict()}, indent=2))


def cmd_phases() -> None:
    phases = load_phase_registry()
    print(json.dumps({"count": len(phases), "latest": latest_phase()}, indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="mcms")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    sub.add_parser("phases")
    args = parser.parse_args(argv)
    if args.cmd == "demo":
        cmd_demo()
    elif args.cmd == "phases":
        cmd_phases()


if __name__ == "__main__":
    main()
