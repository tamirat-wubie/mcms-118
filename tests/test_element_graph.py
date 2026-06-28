import json

import pytest

from mcms.cli import cmd_elements
from mcms.elements import build_element_relation_graph, list_seed_elements


def test_full_element_relation_graph_exports_all_seed_nodes_and_edges():
    graph = build_element_relation_graph()
    payload = graph.to_dict()
    seed_symbols = {element.identity.symbol for element in list_seed_elements()}
    graph_symbols = {node["symbol"] for node in payload["nodes"]}
    assert payload["graph_status"] == "element_relation_graph_exported"
    assert payload["query"]["node_count"] == 36
    assert graph_symbols == seed_symbols
    assert payload["query"]["edge_count"] == len(payload["edges"])
    assert payload["query"]["edge_count"] > payload["query"]["node_count"]


def test_symbol_relation_graph_filters_to_declared_relation_type():
    graph = build_element_relation_graph("Zn", relation_type="same_block")
    payload = graph.to_dict()
    target_symbols = {edge["target_symbol"] for edge in payload["edges"]}
    assert payload["query"]["symbol"] == "Zn"
    assert payload["query"]["relation_type"] == "same_block"
    assert payload["query"]["edge_count"] == 9
    assert target_symbols == {"Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu"}
    assert {edge["relation_type"] for edge in payload["edges"]} == {"same_block"}


def test_element_relation_graph_rejects_unknown_relation_type():
    with pytest.raises(ValueError):
        build_element_relation_graph("H", relation_type="same_shell")
    graph = build_element_relation_graph("H", relation_type="same_group")
    payload = graph.to_dict()
    assert payload["query"]["symbol"] == "H"
    assert payload["query"]["relation_type"] == "same_group"
    assert any(edge["target_symbol"] == "Li" for edge in payload["edges"])


def test_element_graph_cli_prints_filtered_graph(capsys):
    cmd_elements(
        symbol="Zn",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=True,
        relation_type="same_block",
    )
    output = json.loads(capsys.readouterr().out)
    assert output["query"]["symbol"] == "Zn"
    assert output["query"]["edge_count"] == 9
    assert output["nodes"][-1]["symbol"] == "Zn"
