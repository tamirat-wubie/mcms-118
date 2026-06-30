"""Purpose: Cs-Rn bounded behavior-tag overlay.

Project scope: derives Level 1 behavior tags for snapshot elements 55-86 from
configuration, frontier/valence, oxidation-state, and physical-property evidence.
Dependencies: local evidence overlays and snapshot identity records.
Invariants: behavior tags are symbolic inference, not measured source facts; relation
edges remain a separate promotion blocker.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any

from mcms.elements.frontier_valence import find_frontier_valence_signature_record
from mcms.elements.oxidation_evidence import find_oxidation_state_evidence_record
from mcms.elements.promotion import CS_RN_PROMOTION_SYMBOLS
from mcms.elements.snapshot import get_snapshot_record

VALID_BEHAVIOR_TAG_STATUSES = {"behavior_tag_overlay"}
VALID_CSRN_BEHAVIOR_TAGS = {
    "alkali_metal",
    "alkaline_earth_metal",
    "closed_shell_baseline",
    "coordination_relevance",
    "covalent_boundary_relevance",
    "filled_d_shell_context",
    "filled_f_shell_context",
    "f_orbital_relevance",
    "halogen",
    "heavy_p_block",
    "lanthanide_series",
    "low_reactivity_baseline",
    "metallic_bonding_relevance",
    "metalloid",
    "negative_oxidation_pathway",
    "noble_gas",
    "one_electron_completion_pressure",
    "one_electron_loss_pathway",
    "open_f_shell_context",
    "period_6_transition_metal",
    "plus_three_pathway_relevance",
    "post_transition_metal",
    "s_block_metal",
    "variable_oxidation_states",
}

_GROUP_BLOCK_TAGS: dict[str, tuple[str, ...]] = {
    "Alkali metal": (
        "alkali_metal",
        "s_block_metal",
        "one_electron_loss_pathway",
        "metallic_bonding_relevance",
    ),
    "Alkaline earth metal": (
        "alkaline_earth_metal",
        "s_block_metal",
        "metallic_bonding_relevance",
    ),
    "Lanthanide": (
        "lanthanide_series",
        "f_orbital_relevance",
        "plus_three_pathway_relevance",
        "metallic_bonding_relevance",
    ),
    "Transition metal": (
        "period_6_transition_metal",
        "coordination_relevance",
        "metallic_bonding_relevance",
    ),
    "Post-transition metal": (
        "post_transition_metal",
        "heavy_p_block",
        "metallic_bonding_relevance",
    ),
    "Metalloid": (
        "metalloid",
        "heavy_p_block",
        "covalent_boundary_relevance",
    ),
    "Halogen": (
        "halogen",
        "heavy_p_block",
        "one_electron_completion_pressure",
        "covalent_boundary_relevance",
    ),
    "Noble gas": (
        "noble_gas",
        "closed_shell_baseline",
        "low_reactivity_baseline",
    ),
}


@dataclass(frozen=True)
class BehaviorTagOverlayRecord:
    element_id: str
    symbol: str
    atomic_number: int
    inferred_behavior_tags: tuple[str, ...]
    inference_basis: tuple[str, ...]
    source_evidence_keys: tuple[str, ...]
    evidence_status: str = "behavior_tag_overlay"
    notes: tuple[str, ...] = (
        "Behavior tags are controlled symbolic inference over source-backed evidence.",
        "Tags are not measured properties and do not guarantee behavior in every compound.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        expected_element_id = f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}"
        if self.element_id != expected_element_id:
            errors.append("behavior tag element id must match snapshot element id.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("behavior tag atomic number must match snapshot element.")
        if self.symbol not in CS_RN_PROMOTION_SYMBOLS:
            errors.append("behavior tag symbol must be in the Cs-Rn span.")
        if not self.inferred_behavior_tags:
            errors.append("behavior tag overlay requires at least one tag.")
        if len(set(self.inferred_behavior_tags)) != len(self.inferred_behavior_tags):
            errors.append("behavior tags must not contain duplicates.")
        for tag in self.inferred_behavior_tags:
            if tag not in VALID_CSRN_BEHAVIOR_TAGS:
                errors.append("behavior tag is unknown.")
        if not self.inference_basis:
            errors.append("behavior tag overlay requires inference basis.")
        required_evidence = {
            "nist_electronic_configurations",
            "pubchem_periodic_table_properties",
        }
        if not required_evidence <= set(self.source_evidence_keys):
            errors.append("behavior tag overlay requires configuration and PubChem source keys.")
        if self.evidence_status not in VALID_BEHAVIOR_TAG_STATUSES:
            errors.append("behavior tag evidence status is unknown.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["inferred_behavior_tags"] = list(self.inferred_behavior_tags)
        payload["inference_basis"] = list(self.inference_basis)
        payload["source_evidence_keys"] = list(self.source_evidence_keys)
        payload["notes"] = list(self.notes)
        return payload


def _deduplicate(tags: tuple[str, ...]) -> tuple[str, ...]:
    unique: list[str] = []
    for tag in tags:
        if tag not in unique:
            unique.append(tag)
    return tuple(unique)


def _build_behavior_tag_overlay_record(identifier: str | int) -> BehaviorTagOverlayRecord:
    oxidation = find_oxidation_state_evidence_record(identifier)
    frontier = find_frontier_valence_signature_record(identifier)
    snapshot = get_snapshot_record(oxidation.symbol)
    tags: list[str] = list(_GROUP_BLOCK_TAGS[oxidation.pubchem_group_block])
    if len(oxidation.oxidation_states) > 1:
        tags.append("variable_oxidation_states")
    if any(oxidation_state < 0 for oxidation_state in oxidation.oxidation_states):
        tags.append("negative_oxidation_pathway")
    if frontier.d_shell_stability == "filled_shell":
        tags.append("filled_d_shell_context")
    if frontier.f_shell_stability == "filled_shell":
        tags.append("filled_f_shell_context")
    elif frontier.f_shell is not None:
        tags.append("open_f_shell_context")
    return BehaviorTagOverlayRecord(
        element_id=oxidation.element_id,
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        inferred_behavior_tags=_deduplicate(tuple(tags)),
        inference_basis=(
            f"PubChem GroupBlock={oxidation.pubchem_group_block}",
            f"oxidation_states={oxidation.oxidation_states}",
            f"frontier_model={frontier.frontier_model}",
            f"d_shell={frontier.d_shell}",
            f"f_shell={frontier.f_shell}",
        ),
        source_evidence_keys=tuple(
            sorted(set(oxidation.source_keys + frontier.source_keys))
        ),
    )


@lru_cache(maxsize=1)
def list_behavior_tag_overlay_records() -> tuple[BehaviorTagOverlayRecord, ...]:
    return tuple(
        _build_behavior_tag_overlay_record(symbol)
        for symbol in CS_RN_PROMOTION_SYMBOLS
    )


def find_behavior_tag_overlay_record(identifier: str | int) -> BehaviorTagOverlayRecord:
    identifier_text = str(identifier).strip()
    for record in list_behavior_tag_overlay_records():
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.element_id
        ):
            return record
    raise KeyError(f"unknown behavior tag overlay record: {identifier_text}")


def validate_behavior_tag_overlay_records(
    records: tuple[BehaviorTagOverlayRecord, ...] | None = None,
) -> dict[str, Any]:
    checked_records = records if records is not None else list_behavior_tag_overlay_records()
    invalid_records = tuple(record.element_id for record in checked_records if record.validate())
    observed_symbols = tuple(record.symbol for record in checked_records)
    full_span_expected = records is None or len(checked_records) == len(CS_RN_PROMOTION_SYMBOLS)
    validation_status = "behavior_tag_overlay_records_validated"
    if invalid_records or (full_span_expected and observed_symbols != CS_RN_PROMOTION_SYMBOLS):
        validation_status = "behavior_tag_overlay_records_rejected"
    return {
        "validation_status": validation_status,
        "record_count": len(checked_records),
        "variable_oxidation_tag_count": sum(
            1 for record in checked_records if "variable_oxidation_states" in record.inferred_behavior_tags
        ),
        "coordination_relevance_count": sum(
            1 for record in checked_records if "coordination_relevance" in record.inferred_behavior_tags
        ),
        "f_orbital_relevance_count": sum(
            1 for record in checked_records if "f_orbital_relevance" in record.inferred_behavior_tags
        ),
        "low_reactivity_baseline_count": sum(
            1 for record in checked_records if "low_reactivity_baseline" in record.inferred_behavior_tags
        ),
        "invalid_records": invalid_records,
        "source_evidence_keys": tuple(
            sorted({source_key for record in checked_records for source_key in record.source_evidence_keys})
        ),
    }
