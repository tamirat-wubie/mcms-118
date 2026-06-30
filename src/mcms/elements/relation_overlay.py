"""Purpose: Cs-Rn relation-edge overlay.

Project scope: generates same-group, same-period, same-block, and evidence-derived
relation edges for snapshot elements 55-86 without promoting them to full seed records.
Dependencies: snapshot records, frontier/valence signatures, oxidation evidence,
and behavior-tag overlays.
Invariants: relation edges are read-only overlay records; physical-property gaps
remain separate promotion blockers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any

from mcms.elements.behavior_tags import find_behavior_tag_overlay_record
from mcms.elements.frontier_valence import find_frontier_valence_signature_record
from mcms.elements.oxidation_evidence import find_oxidation_state_evidence_record
from mcms.elements.promotion import CS_RN_PROMOTION_SYMBOLS
from mcms.elements.snapshot import get_snapshot_record

VALID_RELATION_OVERLAY_EDGE_TYPES = {
    "same_group",
    "same_period",
    "same_block",
    "same_frontier_model",
    "shared_oxidation_state",
    "shared_behavior_tag",
}
VALID_RELATION_OVERLAY_STATUSES = {"relation_edge_overlay"}


@dataclass(frozen=True)
class RelationOverlayEdge:
    source_symbol: str
    target_symbol: str
    relation_type: str
    reason: str
    evidence_basis: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.source_symbol or not self.target_symbol:
            errors.append("relation edge source and target symbols are required.")
        if self.source_symbol == self.target_symbol:
            errors.append("relation edge cannot target the source element.")
        if self.relation_type not in VALID_RELATION_OVERLAY_EDGE_TYPES:
            errors.append("relation edge type is unknown.")
        if not self.reason:
            errors.append("relation edge reason is required.")
        if not self.evidence_basis:
            errors.append("relation edge evidence basis is required.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RelationOverlayRecord:
    element_id: str
    symbol: str
    atomic_number: int
    relation_edges: tuple[RelationOverlayEdge, ...]
    source_evidence_keys: tuple[str, ...]
    evidence_status: str = "relation_edge_overlay"
    notes: tuple[str, ...] = (
        "Relation edges are generated from explicit snapshot and evidence-overlay fields.",
        "Edges are not a full reaction model and do not claim substitutability.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        expected_element_id = f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}"
        if self.element_id != expected_element_id:
            errors.append("relation overlay element id must match snapshot element id.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("relation overlay atomic number must match snapshot element.")
        if self.symbol not in CS_RN_PROMOTION_SYMBOLS:
            errors.append("relation overlay symbol must be in the Cs-Rn span.")
        if not self.relation_edges:
            errors.append("relation overlay requires at least one relation edge.")
        seen_edges: set[tuple[str, str]] = set()
        for edge in self.relation_edges:
            errors.extend(edge.validate())
            edge_key = (edge.relation_type, edge.target_symbol)
            if edge_key in seen_edges:
                errors.append("relation overlay must not duplicate relation type/target pairs.")
            seen_edges.add(edge_key)
        required_evidence = {
            "nist_electronic_configurations",
            "pubchem_periodic_table_properties",
        }
        if not required_evidence <= set(self.source_evidence_keys):
            errors.append("relation overlay requires configuration and PubChem source keys.")
        if self.evidence_status not in VALID_RELATION_OVERLAY_STATUSES:
            errors.append("relation overlay status is unknown.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["relation_edges"] = [edge.to_dict() for edge in self.relation_edges]
        payload["source_evidence_keys"] = list(self.source_evidence_keys)
        payload["notes"] = list(self.notes)
        return payload


def _add_edge(
    edges: list[RelationOverlayEdge],
    *,
    source_symbol: str,
    target_symbol: str,
    relation_type: str,
    reason: str,
    evidence_basis: str,
) -> None:
    if source_symbol == target_symbol:
        return
    edge_key = (relation_type, target_symbol)
    if any((edge.relation_type, edge.target_symbol) == edge_key for edge in edges):
        return
    edges.append(
        RelationOverlayEdge(
            source_symbol=source_symbol,
            target_symbol=target_symbol,
            relation_type=relation_type,
            reason=reason,
            evidence_basis=evidence_basis,
        )
    )


def _build_relation_overlay_record(identifier: str | int) -> RelationOverlayRecord:
    snapshot = get_snapshot_record(identifier)
    if snapshot.symbol not in CS_RN_PROMOTION_SYMBOLS:
        raise KeyError(f"element is not in the Cs-Rn relation-overlay span: {snapshot.symbol}")
    frontier = find_frontier_valence_signature_record(snapshot.symbol)
    oxidation = find_oxidation_state_evidence_record(snapshot.symbol)
    behavior = find_behavior_tag_overlay_record(snapshot.symbol)
    edges: list[RelationOverlayEdge] = []
    for target_symbol in CS_RN_PROMOTION_SYMBOLS:
        target_snapshot = get_snapshot_record(target_symbol)
        target_frontier = find_frontier_valence_signature_record(target_symbol)
        target_oxidation = find_oxidation_state_evidence_record(target_symbol)
        target_behavior = find_behavior_tag_overlay_record(target_symbol)
        if snapshot.group is not None and snapshot.group == target_snapshot.group:
            _add_edge(
                edges,
                source_symbol=snapshot.symbol,
                target_symbol=target_symbol,
                relation_type="same_group",
                reason=f"both elements are in group {snapshot.group}",
                evidence_basis="IUPAC periodic-table snapshot position",
            )
        if snapshot.period == target_snapshot.period:
            _add_edge(
                edges,
                source_symbol=snapshot.symbol,
                target_symbol=target_symbol,
                relation_type="same_period",
                reason=f"both elements are in period {snapshot.period}",
                evidence_basis="IUPAC periodic-table snapshot position",
            )
        if snapshot.block == target_snapshot.block:
            _add_edge(
                edges,
                source_symbol=snapshot.symbol,
                target_symbol=target_symbol,
                relation_type="same_block",
                reason=f"both elements are in {snapshot.block}-block",
                evidence_basis="IUPAC periodic-table snapshot position",
            )
        if frontier.frontier_model == target_frontier.frontier_model:
            _add_edge(
                edges,
                source_symbol=snapshot.symbol,
                target_symbol=target_symbol,
                relation_type="same_frontier_model",
                reason=f"both elements use {frontier.frontier_model}",
                evidence_basis="frontier_valence_signature",
            )
        shared_oxidation_states = tuple(
            state
            for state in oxidation.oxidation_states
            if state in target_oxidation.oxidation_states
        )
        if shared_oxidation_states:
            _add_edge(
                edges,
                source_symbol=snapshot.symbol,
                target_symbol=target_symbol,
                relation_type="shared_oxidation_state",
                reason=f"shared oxidation states {shared_oxidation_states}",
                evidence_basis="pubchem_periodic_table_properties",
            )
        shared_behavior_tags = tuple(
            tag
            for tag in behavior.inferred_behavior_tags
            if tag in target_behavior.inferred_behavior_tags
        )
        if shared_behavior_tags:
            _add_edge(
                edges,
                source_symbol=snapshot.symbol,
                target_symbol=target_symbol,
                relation_type="shared_behavior_tag",
                reason=f"shared behavior tags {shared_behavior_tags}",
                evidence_basis="behavior_tag_overlay",
            )
    return RelationOverlayRecord(
        element_id=f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}",
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        relation_edges=tuple(sorted(edges, key=lambda edge: (edge.relation_type, edge.target_symbol))),
        source_evidence_keys=("nist_electronic_configurations", "pubchem_periodic_table_properties"),
    )


@lru_cache(maxsize=1)
def list_relation_overlay_records() -> tuple[RelationOverlayRecord, ...]:
    return tuple(_build_relation_overlay_record(symbol) for symbol in CS_RN_PROMOTION_SYMBOLS)


def find_relation_overlay_record(identifier: str | int) -> RelationOverlayRecord:
    identifier_text = str(identifier).strip()
    for record in list_relation_overlay_records():
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.element_id
        ):
            return record
    raise KeyError(f"unknown relation overlay record: {identifier_text}")


def validate_relation_overlay_records(
    records: tuple[RelationOverlayRecord, ...] | None = None,
) -> dict[str, Any]:
    checked_records = records if records is not None else list_relation_overlay_records()
    invalid_records = tuple(record.element_id for record in checked_records if record.validate())
    observed_symbols = tuple(record.symbol for record in checked_records)
    full_span_expected = records is None or len(checked_records) == len(CS_RN_PROMOTION_SYMBOLS)
    validation_status = "relation_overlay_records_validated"
    if invalid_records or (full_span_expected and observed_symbols != CS_RN_PROMOTION_SYMBOLS):
        validation_status = "relation_overlay_records_rejected"
    edge_counts_by_type = {
        relation_type: sum(
            1
            for record in checked_records
            for edge in record.relation_edges
            if edge.relation_type == relation_type
        )
        for relation_type in sorted(VALID_RELATION_OVERLAY_EDGE_TYPES)
    }
    return {
        "validation_status": validation_status,
        "record_count": len(checked_records),
        "edge_count": sum(len(record.relation_edges) for record in checked_records),
        "edge_counts_by_type": edge_counts_by_type,
        "invalid_records": invalid_records,
        "source_evidence_keys": tuple(
            sorted({source_key for record in checked_records for source_key in record.source_evidence_keys})
        ),
    }
