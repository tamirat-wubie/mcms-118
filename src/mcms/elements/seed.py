"""Purpose: deterministic MSPEE Level 1 seed pack for the first 36 elements.

Governance scope: stores source-backed element identity, electron configuration, atomic
weight model, periodic location, relation edges, and validation receipts.
Dependencies: local MSPEE model contracts and dataclass replacement.
Invariants: first seed pack contains Z=1..36 in order; no value is inferred without a
derivation trace and source key.
"""

from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
from typing import Any

from mcms.elements.model import (
    AtomicWeightModel,
    ElementExposure,
    ElementHistory,
    ElementIdentity,
    ElementLaws,
    ElementRelationEdge,
    ElementSeedPackValidationResult,
    ElementState,
    MulluStandardSymbolicElement,
    SourceReference,
)

SOURCE_REFERENCES = (
    SourceReference(
        key="ciaaw_standard_atomic_weights_2024",
        authority="CIAAW/IUPAC",
        title="Standard Atomic Weights 2024",
        url="https://www.ciaaw.org/atomic-weights.htm",
        version="2024",
    ),
    SourceReference(
        key="nist_electronic_configurations",
        authority="NIST",
        title="Electronic Configurations of the Elements",
        url=(
            "https://www.nist.gov/pml/atomic-reference-data-electronic-structure-"
            "calculations/atomic-reference-data-electronic-8"
        ),
        version="source page observed 2026-06-28",
    ),
)

LEVEL_2_CHEMISTRY_SOURCE_REFERENCE = SourceReference(
    key="pubchem_periodic_table_properties",
    authority="PubChem/NCBI",
    title="PubChem Periodic Table of Elements CSV",
    url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV",
    version="source page observed 2026-06-28",
)

_LEVEL_2_CHEMISTRY_BY_SYMBOL: dict[str, dict[str, Any]] = {
    "H": {"oxidation_states": (1, -1), "electronegativity_value": 2.20},
    "He": {"oxidation_states": (0,), "electronegativity_value": None},
    "Li": {"oxidation_states": (1,), "electronegativity_value": 0.98},
    "Be": {"oxidation_states": (2,), "electronegativity_value": 1.57},
    "B": {"oxidation_states": (3,), "electronegativity_value": 2.04},
    "C": {"oxidation_states": (4, 2, -4), "electronegativity_value": 2.55},
    "N": {
        "oxidation_states": (5, 4, 3, 2, 1, -1, -2, -3),
        "electronegativity_value": 3.04,
    },
    "O": {"oxidation_states": (-2,), "electronegativity_value": 3.44},
    "F": {"oxidation_states": (-1,), "electronegativity_value": 3.98},
    "Ne": {"oxidation_states": (0,), "electronegativity_value": None},
    "Na": {"oxidation_states": (1,), "electronegativity_value": 0.93},
    "Mg": {"oxidation_states": (2,), "electronegativity_value": 1.31},
    "Al": {"oxidation_states": (3,), "electronegativity_value": 1.61},
    "Si": {"oxidation_states": (4, 2, -4), "electronegativity_value": 1.90},
    "P": {"oxidation_states": (5, 3, -3), "electronegativity_value": 2.19},
    "S": {"oxidation_states": (6, 4, -2), "electronegativity_value": 2.58},
    "Cl": {"oxidation_states": (7, 5, 1, -1), "electronegativity_value": 3.16},
    "Ar": {"oxidation_states": (0,), "electronegativity_value": None},
    "K": {"oxidation_states": (1,), "electronegativity_value": 0.82},
    "Ca": {"oxidation_states": (2,), "electronegativity_value": 1.00},
    "Sc": {"oxidation_states": (3,), "electronegativity_value": 1.36},
    "Ti": {"oxidation_states": (4, 3, 2), "electronegativity_value": 1.54},
    "V": {"oxidation_states": (5, 4, 3, 2), "electronegativity_value": 1.63},
    "Cr": {"oxidation_states": (6, 3, 2), "electronegativity_value": 1.66},
    "Mn": {"oxidation_states": (7, 4, 3, 2), "electronegativity_value": 1.55},
    "Fe": {"oxidation_states": (3, 2), "electronegativity_value": 1.83},
    "Co": {"oxidation_states": (3, 2), "electronegativity_value": 1.88},
    "Ni": {"oxidation_states": (3, 2), "electronegativity_value": 1.91},
    "Cu": {"oxidation_states": (2, 1), "electronegativity_value": 1.90},
    "Zn": {"oxidation_states": (2,), "electronegativity_value": 1.65},
    "Ga": {"oxidation_states": (3,), "electronegativity_value": 1.81},
    "Ge": {"oxidation_states": (4, 2), "electronegativity_value": 2.01},
    "As": {"oxidation_states": (5, 3, -3), "electronegativity_value": 2.18},
    "Se": {"oxidation_states": (6, 4, -2), "electronegativity_value": 2.55},
    "Br": {"oxidation_states": (5, 1, -1), "electronegativity_value": 2.96},
    "Kr": {"oxidation_states": (0,), "electronegativity_value": 3.00},
}


def _level_2_chemistry_fields(symbol: str) -> dict[str, Any]:
    chemistry = _LEVEL_2_CHEMISTRY_BY_SYMBOL.get(symbol)
    if chemistry is None:
        return {
            "oxidation_states": (),
            "electronegativity_scale": None,
            "electronegativity_value": None,
            "electronegativity_source_key": None,
            "data_level": 1,
        }
    electronegativity_value = chemistry["electronegativity_value"]
    if electronegativity_value is None:
        return {
            "oxidation_states": chemistry["oxidation_states"],
            "electronegativity_scale": None,
            "electronegativity_value": None,
            "electronegativity_source_key": None,
            "data_level": 2,
        }
    return {
        "oxidation_states": chemistry["oxidation_states"],
        "electronegativity_scale": "pauling",
        "electronegativity_value": electronegativity_value,
        "electronegativity_source_key": LEVEL_2_CHEMISTRY_SOURCE_REFERENCE.key,
        "data_level": 2,
    }


def _weight_interval(display: str, lower_bound: str, upper_bound: str) -> AtomicWeightModel:
    return AtomicWeightModel(
        model_type="interval",
        display=display,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        notes=("interval standard atomic weight for normal materials",),
    )


def _weight_single(display: str) -> AtomicWeightModel:
    return AtomicWeightModel(
        model_type="single",
        display=display,
        notes=("single standard atomic weight with uncertainty notation when present",),
    )


_RAW_ELEMENT_SEEDS: tuple[dict[str, Any], ...] = (
    {
        "z": 1,
        "symbol": "H",
        "name": "Hydrogen",
        "period": 1,
        "group": 1,
        "block": "s",
        "neutral": "1s^1",
        "cation": None,
        "valence_shell": "1s",
        "valence_electrons": 1,
        "weight": _weight_interval("[1.00784, 1.00811]", "1.00784", "1.00811"),
    },
    {
        "z": 2,
        "symbol": "He",
        "name": "Helium",
        "period": 1,
        "group": 18,
        "block": "s",
        "neutral": "1s^2",
        "cation": "1s^1",
        "valence_shell": "1s",
        "valence_electrons": 2,
        "weight": _weight_single("4.002602(2)"),
    },
    {
        "z": 3,
        "symbol": "Li",
        "name": "Lithium",
        "period": 2,
        "group": 1,
        "block": "s",
        "neutral": "[He] 2s^1",
        "cation": "1s^2",
        "valence_shell": "2s",
        "valence_electrons": 1,
        "weight": _weight_interval("[6.938, 6.997]", "6.938", "6.997"),
    },
    {
        "z": 4,
        "symbol": "Be",
        "name": "Beryllium",
        "period": 2,
        "group": 2,
        "block": "s",
        "neutral": "[He] 2s^2",
        "cation": "[He] 2s^1",
        "valence_shell": "2s",
        "valence_electrons": 2,
        "weight": _weight_single("9.0121831(5)"),
    },
    {
        "z": 5,
        "symbol": "B",
        "name": "Boron",
        "period": 2,
        "group": 13,
        "block": "p",
        "neutral": "[He] 2s^2 2p^1",
        "cation": "[He] 2s^2",
        "valence_shell": "2s 2p",
        "valence_electrons": 3,
        "weight": _weight_interval("[10.806, 10.821]", "10.806", "10.821"),
    },
    {
        "z": 6,
        "symbol": "C",
        "name": "Carbon",
        "period": 2,
        "group": 14,
        "block": "p",
        "neutral": "[He] 2s^2 2p^2",
        "cation": "[He] 2s^2 2p^1",
        "valence_shell": "2s 2p",
        "valence_electrons": 4,
        "weight": _weight_interval("[12.0096, 12.0116]", "12.0096", "12.0116"),
    },
    {
        "z": 7,
        "symbol": "N",
        "name": "Nitrogen",
        "period": 2,
        "group": 15,
        "block": "p",
        "neutral": "[He] 2s^2 2p^3",
        "cation": "[He] 2s^2 2p^2",
        "valence_shell": "2s 2p",
        "valence_electrons": 5,
        "weight": _weight_interval("[14.00643, 14.00728]", "14.00643", "14.00728"),
    },
    {
        "z": 8,
        "symbol": "O",
        "name": "Oxygen",
        "period": 2,
        "group": 16,
        "block": "p",
        "neutral": "[He] 2s^2 2p^4",
        "cation": "[He] 2s^2 2p^3",
        "valence_shell": "2s 2p",
        "valence_electrons": 6,
        "weight": _weight_interval("[15.99903, 15.99977]", "15.99903", "15.99977"),
    },
    {
        "z": 9,
        "symbol": "F",
        "name": "Fluorine",
        "period": 2,
        "group": 17,
        "block": "p",
        "neutral": "[He] 2s^2 2p^5",
        "cation": "[He] 2s^2 2p^4",
        "valence_shell": "2s 2p",
        "valence_electrons": 7,
        "weight": _weight_single("18.998403162(5)"),
    },
    {
        "z": 10,
        "symbol": "Ne",
        "name": "Neon",
        "period": 2,
        "group": 18,
        "block": "p",
        "neutral": "[He] 2s^2 2p^6",
        "cation": "[He] 2s^2 2p^5",
        "valence_shell": "2s 2p",
        "valence_electrons": 8,
        "weight": _weight_single("20.1797(6)"),
    },
    {
        "z": 11,
        "symbol": "Na",
        "name": "Sodium",
        "period": 3,
        "group": 1,
        "block": "s",
        "neutral": "[Ne] 3s^1",
        "cation": "[He] 2s^2 2p^6",
        "valence_shell": "3s",
        "valence_electrons": 1,
        "weight": _weight_single("22.98976928(2)"),
    },
    {
        "z": 12,
        "symbol": "Mg",
        "name": "Magnesium",
        "period": 3,
        "group": 2,
        "block": "s",
        "neutral": "[Ne] 3s^2",
        "cation": "[Ne] 3s^1",
        "valence_shell": "3s",
        "valence_electrons": 2,
        "weight": _weight_interval("[24.304, 24.307]", "24.304", "24.307"),
    },
    {
        "z": 13,
        "symbol": "Al",
        "name": "Aluminium",
        "period": 3,
        "group": 13,
        "block": "p",
        "neutral": "[Ne] 3s^2 3p^1",
        "cation": "[Ne] 3s^2",
        "valence_shell": "3s 3p",
        "valence_electrons": 3,
        "weight": _weight_single("26.9815384(3)"),
    },
    {
        "z": 14,
        "symbol": "Si",
        "name": "Silicon",
        "period": 3,
        "group": 14,
        "block": "p",
        "neutral": "[Ne] 3s^2 3p^2",
        "cation": "[Ne] 3s^2 3p^1",
        "valence_shell": "3s 3p",
        "valence_electrons": 4,
        "weight": _weight_interval("[28.084, 28.086]", "28.084", "28.086"),
    },
    {
        "z": 15,
        "symbol": "P",
        "name": "Phosphorus",
        "period": 3,
        "group": 15,
        "block": "p",
        "neutral": "[Ne] 3s^2 3p^3",
        "cation": "[Ne] 3s^2 3p^2",
        "valence_shell": "3s 3p",
        "valence_electrons": 5,
        "weight": _weight_single("30.973761998(5)"),
    },
    {
        "z": 16,
        "symbol": "S",
        "name": "Sulfur",
        "period": 3,
        "group": 16,
        "block": "p",
        "neutral": "[Ne] 3s^2 3p^4",
        "cation": "[Ne] 3s^2 3p^3",
        "valence_shell": "3s 3p",
        "valence_electrons": 6,
        "weight": _weight_interval("[32.059, 32.076]", "32.059", "32.076"),
    },
    {
        "z": 17,
        "symbol": "Cl",
        "name": "Chlorine",
        "period": 3,
        "group": 17,
        "block": "p",
        "neutral": "[Ne] 3s^2 3p^5",
        "cation": "[Ne] 3s^2 3p^4",
        "valence_shell": "3s 3p",
        "valence_electrons": 7,
        "weight": _weight_interval("[35.446, 35.457]", "35.446", "35.457"),
    },
    {
        "z": 18,
        "symbol": "Ar",
        "name": "Argon",
        "period": 3,
        "group": 18,
        "block": "p",
        "neutral": "[Ne] 3s^2 3p^6",
        "cation": "[Ne] 3s^2 3p^5",
        "valence_shell": "3s 3p",
        "valence_electrons": 8,
        "weight": _weight_interval("[39.792, 39.963]", "39.792", "39.963"),
    },
    {
        "z": 19,
        "symbol": "K",
        "name": "Potassium",
        "period": 4,
        "group": 1,
        "block": "s",
        "neutral": "[Ar] 4s^1",
        "cation": "[Ne] 3s^2 3p^6",
        "valence_shell": "4s",
        "valence_electrons": 1,
        "weight": _weight_single("39.0983(1)"),
    },
    {
        "z": 20,
        "symbol": "Ca",
        "name": "Calcium",
        "period": 4,
        "group": 2,
        "block": "s",
        "neutral": "[Ar] 4s^2",
        "cation": "[Ar] 4s^1",
        "valence_shell": "4s",
        "valence_electrons": 2,
        "weight": _weight_single("40.078(4)"),
    },
    {
        "z": 21,
        "symbol": "Sc",
        "name": "Scandium",
        "period": 4,
        "group": 3,
        "block": "d",
        "neutral": "[Ar] 3d^1 4s^2",
        "cation": "[Ar] 3d^1 4s^1",
        "valence_shell": "3d 4s",
        "valence_electrons": 3,
        "weight": _weight_single("44.955907(4)"),
    },
    {
        "z": 22,
        "symbol": "Ti",
        "name": "Titanium",
        "period": 4,
        "group": 4,
        "block": "d",
        "neutral": "[Ar] 3d^2 4s^2",
        "cation": "[Ar] 3d^2 4s^1",
        "valence_shell": "3d 4s",
        "valence_electrons": 4,
        "weight": _weight_single("47.867(1)"),
    },
    {
        "z": 23,
        "symbol": "V",
        "name": "Vanadium",
        "period": 4,
        "group": 5,
        "block": "d",
        "neutral": "[Ar] 3d^3 4s^2",
        "cation": "[Ar] 3d^4",
        "valence_shell": "3d 4s",
        "valence_electrons": 5,
        "weight": _weight_single("50.9415(1)"),
    },
    {
        "z": 24,
        "symbol": "Cr",
        "name": "Chromium",
        "period": 4,
        "group": 6,
        "block": "d",
        "neutral": "[Ar] 3d^5 4s^1",
        "cation": "[Ar] 3d^5",
        "valence_shell": "3d 4s",
        "valence_electrons": 6,
        "weight": _weight_single("51.9961(6)"),
    },
    {
        "z": 25,
        "symbol": "Mn",
        "name": "Manganese",
        "period": 4,
        "group": 7,
        "block": "d",
        "neutral": "[Ar] 3d^5 4s^2",
        "cation": "[Ar] 3d^5 4s^1",
        "valence_shell": "3d 4s",
        "valence_electrons": 7,
        "weight": _weight_single("54.938043(2)"),
    },
    {
        "z": 26,
        "symbol": "Fe",
        "name": "Iron",
        "period": 4,
        "group": 8,
        "block": "d",
        "neutral": "[Ar] 3d^6 4s^2",
        "cation": "[Ar] 3d^6 4s^1",
        "valence_shell": "3d 4s",
        "valence_electrons": 8,
        "weight": _weight_single("55.845(2)"),
    },
    {
        "z": 27,
        "symbol": "Co",
        "name": "Cobalt",
        "period": 4,
        "group": 9,
        "block": "d",
        "neutral": "[Ar] 3d^7 4s^2",
        "cation": "[Ar] 3d^8",
        "valence_shell": "3d 4s",
        "valence_electrons": 9,
        "weight": _weight_single("58.933194(3)"),
    },
    {
        "z": 28,
        "symbol": "Ni",
        "name": "Nickel",
        "period": 4,
        "group": 10,
        "block": "d",
        "neutral": "[Ar] 3d^8 4s^2",
        "cation": "[Ar] 3d^9",
        "valence_shell": "3d 4s",
        "valence_electrons": 10,
        "weight": _weight_single("58.6934(4)"),
    },
    {
        "z": 29,
        "symbol": "Cu",
        "name": "Copper",
        "period": 4,
        "group": 11,
        "block": "d",
        "neutral": "[Ar] 3d^10 4s^1",
        "cation": "[Ar] 3d^10",
        "valence_shell": "3d 4s",
        "valence_electrons": 11,
        "weight": _weight_single("63.546(3)"),
    },
    {
        "z": 30,
        "symbol": "Zn",
        "name": "Zinc",
        "period": 4,
        "group": 12,
        "block": "d",
        "neutral": "[Ar] 3d^10 4s^2",
        "cation": "[Ar] 3d^10 4s^1",
        "valence_shell": "3d 4s",
        "valence_electrons": 12,
        "weight": _weight_single("65.38(2)"),
    },
    {
        "z": 31,
        "symbol": "Ga",
        "name": "Gallium",
        "period": 4,
        "group": 13,
        "block": "p",
        "neutral": "[Ar] 3d^10 4s^2 4p^1",
        "cation": "[Ar] 3d^10 4s^2",
        "valence_shell": "4s 4p",
        "valence_electrons": 3,
        "weight": _weight_single("69.723(1)"),
    },
    {
        "z": 32,
        "symbol": "Ge",
        "name": "Germanium",
        "period": 4,
        "group": 14,
        "block": "p",
        "neutral": "[Ar] 3d^10 4s^2 4p^2",
        "cation": "[Ar] 3d^10 4s^2 4p^1",
        "valence_shell": "4s 4p",
        "valence_electrons": 4,
        "weight": _weight_single("72.630(8)"),
    },
    {
        "z": 33,
        "symbol": "As",
        "name": "Arsenic",
        "period": 4,
        "group": 15,
        "block": "p",
        "neutral": "[Ar] 3d^10 4s^2 4p^3",
        "cation": "[Ar] 3d^10 4s^2 4p^2",
        "valence_shell": "4s 4p",
        "valence_electrons": 5,
        "weight": _weight_single("74.921595(6)"),
    },
    {
        "z": 34,
        "symbol": "Se",
        "name": "Selenium",
        "period": 4,
        "group": 16,
        "block": "p",
        "neutral": "[Ar] 3d^10 4s^2 4p^4",
        "cation": "[Ar] 3d^10 4s^2 4p^3",
        "valence_shell": "4s 4p",
        "valence_electrons": 6,
        "weight": _weight_single("78.971(8)"),
    },
    {
        "z": 35,
        "symbol": "Br",
        "name": "Bromine",
        "period": 4,
        "group": 17,
        "block": "p",
        "neutral": "[Ar] 3d^10 4s^2 4p^5",
        "cation": "[Ar] 3d^10 4s^2 4p^4",
        "valence_shell": "4s 4p",
        "valence_electrons": 7,
        "weight": _weight_interval("[79.901, 79.907]", "79.901", "79.907"),
    },
    {
        "z": 36,
        "symbol": "Kr",
        "name": "Krypton",
        "period": 4,
        "group": 18,
        "block": "p",
        "neutral": "[Ar] 3d^10 4s^2 4p^6",
        "cation": "[Ar] 3d^10 4s^2 4p^5",
        "valence_shell": "4s 4p",
        "valence_electrons": 8,
        "weight": _weight_single("83.798(2)"),
    },
)


def _make_base_element(raw_seed: dict[str, Any]) -> MulluStandardSymbolicElement:
    symbol = raw_seed["symbol"]
    atomic_number = raw_seed["z"]
    level_2_fields = _level_2_chemistry_fields(symbol)
    has_level_2_chemistry = symbol in _LEVEL_2_CHEMISTRY_BY_SYMBOL
    behavior_level_tag = (
        "mspee_level_2_chemistry_partial" if has_level_2_chemistry else "mspee_level_1_seed"
    )
    behavior_tags = (
        f"period_{raw_seed['period']}",
        f"group_{raw_seed['group']}",
        f"{raw_seed['block']}_block",
        behavior_level_tag,
    )
    source_references = SOURCE_REFERENCES + (
        (LEVEL_2_CHEMISTRY_SOURCE_REFERENCE,) if has_level_2_chemistry else ()
    )
    derivation_trace = (
        "atomic_number -> proton_count",
        "neutral atom -> electron_count = atomic_number",
        "NIST electronic configurations -> neutral and first-cation configurations",
        "CIAAW Standard Atomic Weights 2024 -> atomic_weight_model",
        "period/group/block -> relation graph seed inputs",
    ) + (
        (
            "PubChem periodic table properties -> oxidation_states and Pauling electronegativity",
        )
        if has_level_2_chemistry
        else ()
    )
    audit_notes = (
        "Level 1 seed does not claim full reaction prediction.",
        "Atomic weight intervals are stored as intervals, not collapsed constants.",
    ) + (
        (
            "Level 2 chemistry values are limited to oxidation-state set and Pauling electronegativity.",
        )
        if has_level_2_chemistry
        else ()
    )
    human_view = (
        f"{raw_seed['name']} ({symbol}) is modeled as MSPEE element Z={atomic_number}: "
        f"identity is {atomic_number} protons; neutral configuration is "
        f"{raw_seed['neutral']}; claims remain bounded to source-backed seed data."
    )
    return MulluStandardSymbolicElement(
        id=f"MSPEE-Z{atomic_number:03d}-{symbol}",
        symbol_family="element",
        identity=ElementIdentity(
            atomic_number=atomic_number,
            symbol=symbol,
            name=raw_seed["name"],
            proton_count=atomic_number,
        ),
        laws=ElementLaws(),
        state=ElementState(
            neutral_electron_count=atomic_number,
            neutral_electron_configuration=raw_seed["neutral"],
            first_cation_configuration=raw_seed["cation"],
            period=raw_seed["period"],
            group=raw_seed["group"],
            block=raw_seed["block"],
            valence_shell=raw_seed["valence_shell"],
            valence_electrons=raw_seed["valence_electrons"],
            atomic_weight_model=raw_seed["weight"],
            oxidation_states=level_2_fields["oxidation_states"],
            electronegativity_scale=level_2_fields["electronegativity_scale"],
            electronegativity_value=level_2_fields["electronegativity_value"],
            electronegativity_source_key=level_2_fields["electronegativity_source_key"],
            behavior_tags=behavior_tags,
            data_level=level_2_fields["data_level"],
        ),
        exposure=ElementExposure(
            human_view=human_view,
            graph_view=f"node:element/{symbol}",
        ),
        history=ElementHistory(
            source_references=source_references,
            derivation_trace=derivation_trace,
            validation_status="seed_record_level_2_partial"
            if has_level_2_chemistry
            else "seed_record_level_1",
            last_audit="2026-06-28",
            audit_notes=audit_notes,
        ),
    )


def _relation_edges_for(
    element: MulluStandardSymbolicElement,
    all_elements: tuple[MulluStandardSymbolicElement, ...],
) -> tuple[ElementRelationEdge, ...]:
    edges: list[ElementRelationEdge] = []
    for other_element in all_elements:
        if other_element.identity.symbol == element.identity.symbol:
            continue
        if other_element.state.group == element.state.group:
            edges.append(
                ElementRelationEdge(
                    source_symbol=element.identity.symbol,
                    target_symbol=other_element.identity.symbol,
                    relation_type="same_group",
                    reason=f"group {element.state.group}",
                )
            )
        if other_element.state.period == element.state.period:
            edges.append(
                ElementRelationEdge(
                    source_symbol=element.identity.symbol,
                    target_symbol=other_element.identity.symbol,
                    relation_type="same_period",
                    reason=f"period {element.state.period}",
                )
            )
        if other_element.state.block == element.state.block:
            edges.append(
                ElementRelationEdge(
                    source_symbol=element.identity.symbol,
                    target_symbol=other_element.identity.symbol,
                    relation_type="same_block",
                    reason=f"{element.state.block}-block",
                )
            )
    return tuple(edges)


@lru_cache(maxsize=1)
def list_seed_elements() -> tuple[MulluStandardSymbolicElement, ...]:
    base_elements = tuple(_make_base_element(raw_seed) for raw_seed in _RAW_ELEMENT_SEEDS)
    elements_with_edges: list[MulluStandardSymbolicElement] = []
    for element in base_elements:
        state_with_edges = replace(
            element.state,
            relation_edges=_relation_edges_for(element, base_elements),
        )
        elements_with_edges.append(replace(element, state=state_with_edges))
    return tuple(elements_with_edges)


def get_seed_element(identifier: str | int) -> MulluStandardSymbolicElement:
    identifier_text = str(identifier).strip()
    if not identifier_text:
        raise KeyError("element identifier is required")
    for element in list_seed_elements():
        if identifier_text == str(element.identity.atomic_number):
            return element
        if identifier_text.upper() == element.identity.symbol.upper():
            return element
        if identifier_text.lower() == element.identity.name.lower():
            return element
    raise KeyError(f"unknown MSPEE seed element: {identifier_text}")


def validate_seed_pack(
    elements: tuple[MulluStandardSymbolicElement, ...] | None = None,
) -> ElementSeedPackValidationResult:
    checked_elements = elements if elements is not None else list_seed_elements()
    invalid_elements = tuple(
        element.id for element in checked_elements if element.validate()
    )
    source_keys = tuple(
        sorted({source_key for element in checked_elements for source_key in element.source_keys()})
    )
    relation_edge_count = sum(len(element.state.relation_edges) for element in checked_elements)
    expected_atomic_numbers = tuple(range(1, 37))
    observed_atomic_numbers = tuple(element.identity.atomic_number for element in checked_elements)
    status = "element_seed_pack_validated"
    if invalid_elements or observed_atomic_numbers != expected_atomic_numbers:
        status = "element_seed_pack_rejected"
    return ElementSeedPackValidationResult(
        element_count=len(checked_elements),
        relation_edge_count=relation_edge_count,
        invalid_elements=invalid_elements,
        source_keys=source_keys,
        validation_status=status,
    )
