import json

from mcms.api import handle_api_request
from mcms.cli import cmd_elements
from mcms.elements import build_element_dashboard_view_model


def test_dashboard_view_model_selects_level_1_element_and_graph_context():
    dashboard = build_element_dashboard_view_model("Zn", relation_type="same_block").to_dict()
    assert dashboard["dashboard_status"] == "element_dashboard_view_model_ready"
    assert dashboard["selected_element"]["symbol"] == "Zn"
    assert dashboard["selected_snapshot"]["level_1_seed_available"] is True
    assert dashboard["selected_element"]["oxidation_states"] == [2]
    assert dashboard["selected_element"]["electronegativity"]["value"] == 1.65
    assert dashboard["selected_element"]["first_ionization_energy"]["value"] == 9.394
    assert (
        dashboard["selected_element"]["first_ionization_energy"]["source_key"]
        == "pubchem_periodic_table_properties"
    )
    assert dashboard["selected_element"]["bond_tendency"]["tags"] == []
    assert dashboard["graph"]["query"]["edge_count"] == 9
    assert len(dashboard["schema_cards"]) == 3


def test_dashboard_view_model_surfaces_seed_pack_level_2_chemistry_fields():
    dashboard = build_element_dashboard_view_model("O", relation_type="same_period").to_dict()
    element_card = dashboard["selected_element"]
    assert element_card["symbol"] == "O"
    assert element_card["oxidation_states"] == [-2]
    assert element_card["electronegativity"]["scale"] == "pauling"
    assert element_card["electronegativity"]["value"] == 3.44
    assert element_card["electronegativity"]["source_key"] == "pubchem_periodic_table_properties"


def test_dashboard_view_model_preserves_snapshot_only_boundary():
    dashboard = build_element_dashboard_view_model("Og", relation_type="same_period").to_dict()
    assert dashboard["selected_element"] is None
    assert dashboard["selected_snapshot"]["symbol"] == "Og"
    assert dashboard["selected_snapshot"]["level_1_seed_available"] is False
    assert dashboard["graph"]["graph_status"] == "element_relation_graph_unavailable_for_snapshot_only_record"
    assert dashboard["graph"]["query"]["edge_count"] == 0
    assert dashboard["actions"][1]["api_route"] == "/snapshot/Og"


def test_dashboard_cli_prints_selected_view_model(capsys):
    cmd_elements(
        symbol="Zn",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=True,
        relation_type="same_block",
    )
    output = json.loads(capsys.readouterr().out)
    assert output["query"]["symbol"] == "Zn"
    assert output["selected_element"]["validation_status"] == "element_seed_validated"
    assert output["actions"][2]["api_route"] == "/graph?symbol=Zn&relation=same_block"


def test_dashboard_api_route_returns_read_model():
    response = handle_api_request("GET", "/dashboard/Zn?relation=same_block")
    payload = response.payload["dashboard"]
    assert response.status_code == 200
    assert payload["selected_element"]["symbol"] == "Zn"
    assert payload["seed_summary"]["element_count"] == 36
    assert payload["snapshot_summary"]["element_count"] == 118
