import json

import pytest

from mcms.cli import cmd_elements
from mcms.elements import build_ion_instance, build_isotope_instance


def test_ion_instance_preserves_identity_and_derives_electron_count():
    sodium = build_ion_instance("Na", charge=1)
    chloride = build_ion_instance("Cl", charge=-1)

    assert sodium.instance_id == "MSPEE-Z011-Na-ion-plus-1"
    assert sodium.element_id == "MSPEE-Z011-Na"
    assert sodium.proton_count == 11
    assert sodium.electron_count == 10
    assert sodium.source_element_configuration == "[Ne] 3s^1"
    assert sodium.validate() == []

    assert chloride.instance_id == "MSPEE-Z017-Cl-ion-minus-1"
    assert chloride.proton_count == 17
    assert chloride.electron_count == 18
    assert chloride.validate() == []


def test_ion_instance_rejects_neutral_and_over_removed_electron_states():
    with pytest.raises(ValueError, match="nonzero"):
        build_ion_instance("Na", charge=0)

    with pytest.raises(ValueError, match="electron count cannot be negative"):
        build_ion_instance("H", charge=2)

    with pytest.raises(KeyError, match="unknown MSPEE seed element"):
        build_ion_instance("Og", charge=1)


def test_isotope_instance_preserves_identity_and_derives_neutron_count():
    carbon_14 = build_isotope_instance("C", mass_number=14)
    hydrogen_1 = build_isotope_instance("H", mass_number=1)
    oganesson_294 = build_isotope_instance("Og", mass_number=294)

    assert carbon_14.instance_id == "MSPEE-Z006-C-isotope-14"
    assert carbon_14.element_id == "MSPEE-Z006-C"
    assert carbon_14.proton_count == 6
    assert carbon_14.neutron_count == 8
    assert carbon_14.source_atomic_weight_status == "interval"
    assert carbon_14.validate() == []

    assert hydrogen_1.neutron_count == 0
    assert hydrogen_1.validate() == []
    assert oganesson_294.proton_count == 118
    assert oganesson_294.neutron_count == 176
    assert oganesson_294.source_atomic_weight_status == "unavailable"


def test_isotope_instance_rejects_mass_number_below_identity_boundary():
    with pytest.raises(ValueError, match="mass number"):
        build_isotope_instance("C", mass_number=5)

    with pytest.raises(KeyError, match="unknown MSPEE snapshot element"):
        build_isotope_instance("Xx", mass_number=1)


def test_element_cli_prints_ion_and_isotope_instances(capsys):
    cmd_elements(
        symbol="Na",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        ion_charge=1,
    )
    sodium = json.loads(capsys.readouterr().out)

    cmd_elements(
        symbol="C",
        list_only=False,
        full_snapshot=False,
        schema_name=None,
        graph_export=False,
        dashboard_export=False,
        relation_type=None,
        isotope_mass=14,
    )
    carbon_14 = json.loads(capsys.readouterr().out)

    assert sodium["instance"]["instance_id"] == "MSPEE-Z011-Na-ion-plus-1"
    assert sodium["instance"]["electron_count"] == 10
    assert carbon_14["instance"]["instance_id"] == "MSPEE-Z006-C-isotope-14"
    assert carbon_14["instance"]["neutron_count"] == 8
