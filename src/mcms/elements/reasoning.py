"""Purpose: deterministic Phase 2 element reasoning helpers.

Project scope: turns validated element records into bounded explanation payloads.
Dependencies: local MSPEE seed records and dataclass serialization.
Invariants: reasoning never mutates seed records; source-backed configuration wins.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.model import MulluStandardSymbolicElement
from mcms.elements.seed import get_seed_element


@dataclass(frozen=True)
class ElementReasoningResult:
    reasoning_status: str
    reasoning_type: str
    subject_symbols: tuple[str, ...]
    question: str
    answer_lines: tuple[str, ...]
    evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["subject_symbols"] = list(self.subject_symbols)
        payload["answer_lines"] = list(self.answer_lines)
        return payload


def _outer_shell_signature(element: MulluStandardSymbolicElement) -> str:
    if element.state.frontier_signature is not None:
        return element.state.frontier_signature.outer_shell
    return element.state.neutral_electron_configuration.split()[-1]


def _frontier_evidence(element: MulluStandardSymbolicElement) -> dict[str, Any]:
    frontier_signature = element.state.frontier_signature
    return {
        "configuration": element.state.neutral_electron_configuration,
        "outer_shell": _outer_shell_signature(element),
        "d_shell": frontier_signature.d_shell if frontier_signature else None,
        "valence_model": frontier_signature.valence_model if frontier_signature else "main_group",
        "behavior_tags": list(element.state.behavior_tags),
        "oxidation_states": list(element.state.oxidation_states),
    }


def explain_configuration_choice(identifier: str | int) -> ElementReasoningResult:
    element = get_seed_element(identifier)
    audit = element.state.configuration_audit
    if audit is None:
        return ElementReasoningResult(
            reasoning_status="configuration_audit_unavailable",
            reasoning_type="configuration_choice",
            subject_symbols=(element.identity.symbol,),
            question=(
                f"Why is {element.identity.name} represented as "
                f"{element.state.neutral_electron_configuration}?"
            ),
            answer_lines=(
                "This element does not yet carry a Phase 2 configuration audit.",
                "The current representation remains the source-backed neutral configuration.",
                f"The element identity remains {element.identity.name} because "
                f"proton_count = {element.identity.proton_count}.",
            ),
            evidence={
                "source_backed_configuration": element.state.neutral_electron_configuration,
                "source_keys": list(element.source_keys()),
                "identity": element.identity.to_dict(),
            },
        )

    if audit.is_exception:
        answer_lines = (
            "Because MSPEE treats simple Aufbau filling as a candidate, not final authority.",
            f"The source-backed state is {audit.source_backed_configuration}.",
            "The conflict is recorded as a configuration exception.",
            f"The reason is {audit.exception_reason}.",
            f"The element identity remains {element.identity.name} because "
            f"proton_count = {element.identity.proton_count}.",
            "Only the electron-state representation is corrected.",
        )
    else:
        answer_lines = (
            "The simple Aufbau candidate matches the source-backed configuration.",
            f"The source-backed state is {audit.source_backed_configuration}.",
            "No configuration exception is recorded for this element.",
            f"The element identity remains {element.identity.name} because "
            f"proton_count = {element.identity.proton_count}.",
        )

    return ElementReasoningResult(
        reasoning_status="configuration_choice_explained",
        reasoning_type="configuration_choice",
        subject_symbols=(element.identity.symbol,),
        question=(
            f"Why is {element.identity.name} not represented as "
            f"{audit.simple_aufbau_candidate}?"
            if audit.is_exception
            else f"Why is {element.identity.name} represented this way?"
        ),
        answer_lines=answer_lines,
        evidence={
            "configuration_audit": audit.to_dict(),
            "neutral_electron_configuration": element.state.neutral_electron_configuration,
            "identity": element.identity.to_dict(),
            "source_keys": list(element.source_keys()),
        },
    )


def compare_outer_shell_similarity(
    left_identifier: str | int,
    right_identifier: str | int,
) -> ElementReasoningResult:
    left = get_seed_element(left_identifier)
    right = get_seed_element(right_identifier)
    left_outer_shell = _outer_shell_signature(left)
    right_outer_shell = _outer_shell_signature(right)
    surface_similarity = left_outer_shell == right_outer_shell
    left_has_d_shell = (
        left.state.frontier_signature is not None
        and left.state.frontier_signature.d_shell is not None
    )
    right_has_d_shell = (
        right.state.frontier_signature is not None
        and right.state.frontier_signature.d_shell is not None
    )
    deep_similarity = (
        surface_similarity
        and left.state.block == right.state.block
        and left_has_d_shell == right_has_d_shell
    )

    if surface_similarity and not deep_similarity:
        conclusion = "Partially, but not deeply."
        answer_lines = (
            conclusion,
            f"Surface similarity: both expose {left_outer_shell}.",
            (
                f"Deep difference: {left.identity.symbol} has "
                f"{left.state.frontier_signature.d_shell} structure and "
                f"{left.state.frontier_signature.valence_model} behavior."
                if left_has_d_shell
                else f"Deep difference: {left.identity.symbol} has no inner d-shell frontier."
            ),
            (
                f"Deep difference: {right.identity.symbol} has "
                f"{right.state.frontier_signature.d_shell} structure and "
                f"{right.state.frontier_signature.valence_model} behavior."
                if right_has_d_shell
                else f"Deep difference: {right.identity.symbol} has no inner d-shell frontier."
            ),
        )
    elif surface_similarity:
        answer_lines = (
            "They share the same outer-shell signature and the same deep frontier class.",
            f"Both expose {left_outer_shell}.",
        )
    else:
        answer_lines = (
            "They do not share the same outer-shell signature.",
            f"{left.identity.symbol} exposes {left_outer_shell}.",
            f"{right.identity.symbol} exposes {right_outer_shell}.",
        )

    return ElementReasoningResult(
        reasoning_status="outer_shell_similarity_explained",
        reasoning_type="outer_shell_similarity",
        subject_symbols=(left.identity.symbol, right.identity.symbol),
        question=(
            f"Are {left.identity.name} and {right.identity.name} similar because "
            "their outer shell looks alike?"
        ),
        answer_lines=answer_lines,
        evidence={
            left.identity.symbol: _frontier_evidence(left),
            right.identity.symbol: _frontier_evidence(right),
            "surface_similarity": surface_similarity,
            "deep_similarity": deep_similarity,
        },
    )
