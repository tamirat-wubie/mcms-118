"""Purpose: dashboard-facing read model for MSPEE element surfaces.

Governance scope: composes validated element, snapshot, schema, and graph payloads.
Dependencies: local MSPEE seed, snapshot, schema, graph, and receipt builders.
Invariants: dashboard views are read-only projections and never mutate source records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.graph import build_element_relation_graph
from mcms.elements.model import (
    VALID_RELATION_TYPES,
    MulluStandardSymbolicElement,
    build_element_receipt,
)
from mcms.elements.schema import (
    element_schema_bundle,
    element_seed_json_schema,
    element_snapshot_json_schema,
)
from mcms.elements.seed import get_seed_element, list_seed_elements, validate_seed_pack
from mcms.elements.snapshot import (
    ElementSourceSnapshotRecord,
    build_snapshot_receipt,
    get_snapshot_record,
    list_full_snapshot_records,
    validate_full_snapshot,
)


@dataclass(frozen=True)
class ElementDashboardViewModel:
    dashboard_status: str
    query: dict[str, Any]
    seed_summary: dict[str, Any]
    snapshot_summary: dict[str, Any]
    selected_element: dict[str, Any] | None
    selected_snapshot: dict[str, Any] | None
    schema_cards: tuple[dict[str, Any], ...]
    graph: dict[str, Any]
    actions: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["schema_cards"] = [dict(card) for card in self.schema_cards]
        payload["actions"] = [dict(action) for action in self.actions]
        return payload


def _element_card(element: MulluStandardSymbolicElement) -> dict[str, Any]:
    receipt = build_element_receipt(element)
    return {
        "card_status": "level_1_element_selected",
        "id": element.id,
        "symbol": element.identity.symbol,
        "name": element.identity.name,
        "label": f"{element.identity.name} ({element.identity.symbol})",
        "atomic_number": element.identity.atomic_number,
        "period": element.state.period,
        "group": element.state.group,
        "block": element.state.block,
        "data_level": element.state.data_level,
        "neutral_electron_configuration": element.state.neutral_electron_configuration,
        "valence_shell": element.state.valence_shell,
        "valence_electrons": element.state.valence_electrons,
        "oxidation_states": list(element.state.oxidation_states),
        "electronegativity": {
            "scale": element.state.electronegativity_scale,
            "value": element.state.electronegativity_value,
            "source_key": element.state.electronegativity_source_key,
        },
        "first_ionization_energy": {
            "unit": "eV",
            "value": element.state.first_ionization_energy_ev,
            "source_key": element.state.first_ionization_energy_source_key,
        },
        "bond_tendency": {
            "tags": list(element.state.bond_tendency_tags),
            "source_key": element.state.bond_tendency_source_key,
        },
        "validation_status": receipt["validation_status"],
        "element_hash": receipt["element_hash"],
        "source_keys": list(receipt["source_keys"]),
    }


def _snapshot_card(snapshot: ElementSourceSnapshotRecord) -> dict[str, Any]:
    receipt = build_snapshot_receipt(snapshot)
    return {
        "card_status": "snapshot_record_selected",
        "snapshot_id": receipt["snapshot_id"],
        "symbol": snapshot.symbol,
        "name": snapshot.name,
        "label": f"{snapshot.name} ({snapshot.symbol})",
        "atomic_number": snapshot.atomic_number,
        "period": snapshot.period,
        "group": snapshot.group,
        "block": snapshot.block,
        "snapshot_status": snapshot.snapshot_status,
        "level_1_seed_available": snapshot.level_1_seed_available,
        "atomic_weight": snapshot.atomic_weight_model.display,
        "validation_status": receipt["validation_status"],
        "snapshot_hash": receipt["snapshot_hash"],
        "source_keys": list(snapshot.source_keys),
    }


def _schema_cards() -> tuple[dict[str, Any], ...]:
    schema_payloads = {
        "seed": element_seed_json_schema(),
        "snapshot": element_snapshot_json_schema(),
        "bundle": element_schema_bundle(),
    }
    return tuple(
        {
            "schema_name": schema_name,
            "title": schema.get("title", "ElementSchemaBundle"),
            "schema_id": schema["$id"],
            "api_route": f"/schemas/{schema_name}",
            "cli_command": f"python -m mcms.cli elements --schema {schema_name}",
        }
        for schema_name, schema in schema_payloads.items()
    )


def _actions(symbol: str | None, *, level_1_seed_available: bool) -> tuple[dict[str, Any], ...]:
    selected_symbol = symbol or "Zn"
    selected_record_route = (
        f"/elements/{selected_symbol}"
        if level_1_seed_available
        else f"/snapshot/{selected_symbol}"
    )
    selected_record_command = (
        f"python -m mcms.cli elements --symbol {selected_symbol}"
        if level_1_seed_available
        else f"python -m mcms.cli elements --full --symbol {selected_symbol}"
    )
    return (
        {
            "label": "List Level 1 Elements",
            "api_route": "/elements",
            "cli_command": "python -m mcms.cli elements --list",
        },
        {
            "label": "Open Selected Record",
            "api_route": selected_record_route,
            "cli_command": selected_record_command,
        },
        {
            "label": "Open Selected Graph",
            "api_route": f"/graph?symbol={selected_symbol}&relation=same_block",
            "cli_command": (
                f"python -m mcms.cli elements --graph --symbol {selected_symbol} "
                "--relation same_block"
            ),
        },
        {
            "label": "Open Schema Bundle",
            "api_route": "/schemas/bundle",
            "cli_command": "python -m mcms.cli elements --schema bundle",
        },
    )


def build_element_dashboard_view_model(
    identifier: str | int | None = None,
    relation_type: str | None = None,
) -> ElementDashboardViewModel:
    seed_records = list_seed_elements()
    snapshot_records = list_full_snapshot_records()
    seed_result = validate_seed_pack(seed_records)
    snapshot_result = validate_full_snapshot(snapshot_records)

    selected_element: dict[str, Any] | None = None
    selected_snapshot: dict[str, Any] | None = None
    selected_symbol: str | None = None
    selected_level_1_available = True
    graph_identifier: str | int | None = identifier

    if identifier is not None:
        snapshot = get_snapshot_record(identifier)
        selected_snapshot = _snapshot_card(snapshot)
        selected_symbol = snapshot.symbol
        selected_level_1_available = snapshot.level_1_seed_available
        if snapshot.level_1_seed_available:
            element = get_seed_element(snapshot.symbol)
            selected_element = _element_card(element)
            graph_identifier = element.identity.symbol
        else:
            graph_identifier = None

    if identifier is not None and selected_element is None:
        graph_payload = {
            "graph_status": "element_relation_graph_unavailable_for_snapshot_only_record",
            "query": {
                "symbol": selected_symbol,
                "relation_type": relation_type,
                "node_count": 0,
                "edge_count": 0,
            },
            "nodes": [],
            "edges": [],
        }
    else:
        graph_payload = build_element_relation_graph(
            identifier=graph_identifier,
            relation_type=relation_type,
        ).to_dict()
    return ElementDashboardViewModel(
        dashboard_status="element_dashboard_view_model_ready",
        query={
            "symbol": selected_symbol,
            "relation_type": relation_type,
            "relation_options": sorted(VALID_RELATION_TYPES),
        },
        seed_summary={
            "element_count": seed_result.element_count,
            "validation_status": seed_result.validation_status,
            "relation_edge_count": seed_result.relation_edge_count,
        },
        snapshot_summary={
            "element_count": snapshot_result.element_count,
            "validation_status": snapshot_result.validation_status,
            "level_1_seed_count": snapshot_result.level_1_seed_count,
            "unavailable_weight_count": snapshot_result.unavailable_weight_count,
        },
        selected_element=selected_element,
        selected_snapshot=selected_snapshot,
        schema_cards=_schema_cards(),
        graph=graph_payload,
        actions=_actions(
            selected_symbol,
            level_1_seed_available=selected_level_1_available,
        ),
    )
