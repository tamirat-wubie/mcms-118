"""Purpose: deterministic graph export for MSPEE Level 1 element relations.

Governance scope: exposes source-backed same-group, same-period, and same-block edges.
Dependencies: local MSPEE seed records and dataclass serialization.
Invariants: graph nodes are seed-backed elements; edges are declared relation records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from mcms.elements.model import VALID_RELATION_TYPES, MulluStandardSymbolicElement
from mcms.elements.seed import get_seed_element, list_seed_elements


@dataclass(frozen=True)
class ElementGraphNode:
    id: str
    seed_id: str
    symbol: str
    name: str
    atomic_number: int
    period: int
    group: int
    block: str
    data_level: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementGraphEdge:
    source: str
    target: str
    source_symbol: str
    target_symbol: str
    relation_type: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementRelationGraph:
    graph_status: str
    query: dict
    nodes: tuple[ElementGraphNode, ...]
    edges: tuple[ElementGraphEdge, ...]

    def to_dict(self) -> dict:
        return {
            "graph_status": self.graph_status,
            "query": self.query,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
        }


def _node_id(symbol: str) -> str:
    return f"element/{symbol}"


def _node_for_element(element: MulluStandardSymbolicElement) -> ElementGraphNode:
    return ElementGraphNode(
        id=_node_id(element.identity.symbol),
        seed_id=element.id,
        symbol=element.identity.symbol,
        name=element.identity.name,
        atomic_number=element.identity.atomic_number,
        period=element.state.period,
        group=element.state.group,
        block=element.state.block,
        data_level=element.state.data_level,
    )


def _edge_from_relation(
    source_symbol: str,
    target_symbol: str,
    relation_type: str,
    reason: str,
) -> ElementGraphEdge:
    return ElementGraphEdge(
        source=_node_id(source_symbol),
        target=_node_id(target_symbol),
        source_symbol=source_symbol,
        target_symbol=target_symbol,
        relation_type=relation_type,
        reason=reason,
    )


def build_element_relation_graph(
    identifier: str | int | None = None,
    relation_type: str | None = None,
) -> ElementRelationGraph:
    if relation_type is not None and relation_type not in VALID_RELATION_TYPES:
        raise ValueError(f"unknown element relation type: {relation_type}")

    all_elements = list_seed_elements()
    all_by_symbol = {element.identity.symbol: element for element in all_elements}
    source_elements = (
        (get_seed_element(identifier),) if identifier is not None else all_elements
    )

    edges: list[ElementGraphEdge] = []
    included_symbols = {element.identity.symbol for element in source_elements}
    for element in source_elements:
        for relation_edge in element.state.relation_edges:
            if relation_type is not None and relation_edge.relation_type != relation_type:
                continue
            included_symbols.add(relation_edge.target_symbol)
            edges.append(
                _edge_from_relation(
                    source_symbol=relation_edge.source_symbol,
                    target_symbol=relation_edge.target_symbol,
                    relation_type=relation_edge.relation_type,
                    reason=relation_edge.reason,
                )
            )

    nodes = tuple(
        _node_for_element(all_by_symbol[symbol])
        for symbol in sorted(
            included_symbols,
            key=lambda observed_symbol: all_by_symbol[observed_symbol].identity.atomic_number,
        )
    )
    sorted_edges = tuple(
        sorted(
            edges,
            key=lambda edge: (
                all_by_symbol[edge.source_symbol].identity.atomic_number,
                edge.relation_type,
                all_by_symbol[edge.target_symbol].identity.atomic_number,
            ),
        )
    )
    return ElementRelationGraph(
        graph_status="element_relation_graph_exported",
        query={
            "symbol": None if identifier is None else get_seed_element(identifier).identity.symbol,
            "relation_type": relation_type,
            "node_count": len(nodes),
            "edge_count": len(sorted_edges),
        },
        nodes=nodes,
        edges=sorted_edges,
    )
