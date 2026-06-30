"""Purpose: deterministic MSPEE Level 1 seed pack for the first 54 elements.

Project scope: stores source-backed element identity, electron configuration, atomic
weight model, periodic location, relation edges, and validation receipts.
Dependencies: local MSPEE model contracts and dataclass replacement.
Invariants: seed pack contains Z=1..54 in order; no value is inferred without a
derivation trace and source key.
"""

from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
from typing import Any

from mcms.elements.model import (
    AtomicWeightModel,
    ConfigurationAudit,
    ElementExposure,
    ElementHistory,
    ElementIdentity,
    ElementLaws,
    ElementRelationEdge,
    ElementSeedPackValidationResult,
    ElementState,
    FrontierSignature,
    MulluStandardSymbolicElement,
    SourceReference,
    TransitionBehaviorKernel,
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

_BOND_TENDENCY_TAGS_BY_PUBCHEM_GROUP_BLOCK: dict[str, tuple[str, ...]] = {
    "Alkali metal": ("metallic_bonding", "ionic_bonding"),
    "Alkaline earth metal": ("metallic_bonding", "ionic_bonding"),
    "Halogen": ("covalent_bonding", "ionic_bonding", "molecular_covalent"),
    "Metalloid": ("covalent_bonding", "network_covalent"),
    "Noble gas": ("noble_gas_low_reactivity",),
    "Nonmetal": ("covalent_bonding", "molecular_covalent"),
    "Post-transition metal": ("metallic_bonding", "covalent_bonding"),
    "Transition metal": ("metallic_bonding", "coordination_complex"),
}

_PUBCHEM_GROUP_BLOCK_BY_SYMBOL: dict[str, str] = {
    "H": "Nonmetal",
    "He": "Noble gas",
    "Li": "Alkali metal",
    "Be": "Alkaline earth metal",
    "B": "Metalloid",
    "C": "Nonmetal",
    "N": "Nonmetal",
    "O": "Nonmetal",
    "F": "Halogen",
    "Ne": "Noble gas",
    "Na": "Alkali metal",
    "Mg": "Alkaline earth metal",
    "Al": "Post-transition metal",
    "Si": "Metalloid",
    "P": "Nonmetal",
    "S": "Nonmetal",
    "Cl": "Halogen",
    "Ar": "Noble gas",
    "K": "Alkali metal",
    "Ca": "Alkaline earth metal",
    "Sc": "Transition metal",
    "Ti": "Transition metal",
    "V": "Transition metal",
    "Cr": "Transition metal",
    "Mn": "Transition metal",
    "Fe": "Transition metal",
    "Co": "Transition metal",
    "Ni": "Transition metal",
    "Cu": "Transition metal",
    "Zn": "Transition metal",
    "Ga": "Post-transition metal",
    "Ge": "Metalloid",
    "As": "Metalloid",
    "Se": "Nonmetal",
    "Br": "Halogen",
    "Kr": "Noble gas",
    "Rb": "Alkali metal",
    "Sr": "Alkaline earth metal",
    "Y": "Transition metal",
    "Zr": "Transition metal",
    "Nb": "Transition metal",
    "Mo": "Transition metal",
    "Tc": "Transition metal",
    "Ru": "Transition metal",
    "Rh": "Transition metal",
    "Pd": "Transition metal",
    "Ag": "Transition metal",
    "Cd": "Transition metal",
    "In": "Post-transition metal",
    "Sn": "Post-transition metal",
    "Sb": "Metalloid",
    "Te": "Metalloid",
    "I": "Halogen",
    "Xe": "Noble gas",
}

_LEVEL_2_CHEMISTRY_BY_SYMBOL: dict[str, dict[str, Any]] = {
    "H": {
        "oxidation_states": (1, -1),
        "electronegativity_value": 2.20,
        "first_ionization_energy_ev": 13.598,
    },
    "He": {
        "oxidation_states": (0,),
        "electronegativity_value": None,
        "first_ionization_energy_ev": 24.587,
    },
    "Li": {
        "oxidation_states": (1,),
        "electronegativity_value": 0.98,
        "first_ionization_energy_ev": 5.392,
    },
    "Be": {
        "oxidation_states": (2,),
        "electronegativity_value": 1.57,
        "first_ionization_energy_ev": 9.323,
    },
    "B": {
        "oxidation_states": (3,),
        "electronegativity_value": 2.04,
        "first_ionization_energy_ev": 8.298,
    },
    "C": {
        "oxidation_states": (4, 2, -4),
        "electronegativity_value": 2.55,
        "first_ionization_energy_ev": 11.260,
    },
    "N": {
        "oxidation_states": (5, 4, 3, 2, 1, -1, -2, -3),
        "electronegativity_value": 3.04,
        "first_ionization_energy_ev": 14.534,
    },
    "O": {
        "oxidation_states": (-2,),
        "electronegativity_value": 3.44,
        "first_ionization_energy_ev": 13.618,
    },
    "F": {
        "oxidation_states": (-1,),
        "electronegativity_value": 3.98,
        "first_ionization_energy_ev": 17.423,
    },
    "Ne": {
        "oxidation_states": (0,),
        "electronegativity_value": None,
        "first_ionization_energy_ev": 21.565,
    },
    "Na": {
        "oxidation_states": (1,),
        "electronegativity_value": 0.93,
        "first_ionization_energy_ev": 5.139,
    },
    "Mg": {
        "oxidation_states": (2,),
        "electronegativity_value": 1.31,
        "first_ionization_energy_ev": 7.646,
    },
    "Al": {
        "oxidation_states": (3,),
        "electronegativity_value": 1.61,
        "first_ionization_energy_ev": 5.986,
    },
    "Si": {
        "oxidation_states": (4, 2, -4),
        "electronegativity_value": 1.90,
        "first_ionization_energy_ev": 8.152,
    },
    "P": {
        "oxidation_states": (5, 3, -3),
        "electronegativity_value": 2.19,
        "first_ionization_energy_ev": 10.487,
    },
    "S": {
        "oxidation_states": (6, 4, -2),
        "electronegativity_value": 2.58,
        "first_ionization_energy_ev": 10.360,
    },
    "Cl": {
        "oxidation_states": (7, 5, 1, -1),
        "electronegativity_value": 3.16,
        "first_ionization_energy_ev": 12.968,
    },
    "Ar": {
        "oxidation_states": (0,),
        "electronegativity_value": None,
        "first_ionization_energy_ev": 15.760,
    },
    "K": {
        "oxidation_states": (1,),
        "electronegativity_value": 0.82,
        "first_ionization_energy_ev": 4.341,
    },
    "Ca": {
        "oxidation_states": (2,),
        "electronegativity_value": 1.00,
        "first_ionization_energy_ev": 6.113,
    },
    "Sc": {
        "oxidation_states": (3,),
        "electronegativity_value": 1.36,
        "first_ionization_energy_ev": 6.561,
    },
    "Ti": {
        "oxidation_states": (4, 3, 2),
        "electronegativity_value": 1.54,
        "first_ionization_energy_ev": 6.828,
    },
    "V": {
        "oxidation_states": (5, 4, 3, 2),
        "electronegativity_value": 1.63,
        "first_ionization_energy_ev": 6.746,
    },
    "Cr": {
        "oxidation_states": (6, 3, 2),
        "electronegativity_value": 1.66,
        "first_ionization_energy_ev": 6.767,
    },
    "Mn": {
        "oxidation_states": (7, 4, 3, 2),
        "electronegativity_value": 1.55,
        "first_ionization_energy_ev": 7.434,
    },
    "Fe": {
        "oxidation_states": (3, 2),
        "electronegativity_value": 1.83,
        "first_ionization_energy_ev": 7.902,
    },
    "Co": {
        "oxidation_states": (3, 2),
        "electronegativity_value": 1.88,
        "first_ionization_energy_ev": 7.881,
    },
    "Ni": {
        "oxidation_states": (3, 2),
        "electronegativity_value": 1.91,
        "first_ionization_energy_ev": 7.640,
    },
    "Cu": {
        "oxidation_states": (2, 1),
        "electronegativity_value": 1.90,
        "first_ionization_energy_ev": 7.726,
    },
    "Zn": {
        "oxidation_states": (2,),
        "electronegativity_value": 1.65,
        "first_ionization_energy_ev": 9.394,
    },
    "Ga": {
        "oxidation_states": (3,),
        "electronegativity_value": 1.81,
        "first_ionization_energy_ev": 5.999,
    },
    "Ge": {
        "oxidation_states": (4, 2),
        "electronegativity_value": 2.01,
        "first_ionization_energy_ev": 7.900,
    },
    "As": {
        "oxidation_states": (5, 3, -3),
        "electronegativity_value": 2.18,
        "first_ionization_energy_ev": 9.815,
    },
    "Se": {
        "oxidation_states": (6, 4, -2),
        "electronegativity_value": 2.55,
        "first_ionization_energy_ev": 9.752,
    },
    "Br": {
        "oxidation_states": (5, 1, -1),
        "electronegativity_value": 2.96,
        "first_ionization_energy_ev": 11.814,
    },
    "Kr": {
        "oxidation_states": (0,),
        "electronegativity_value": 3.00,
        "first_ionization_energy_ev": 14.000,
    },
    "Rb": {
        "oxidation_states": (1,),
        "electronegativity_value": 0.82,
        "first_ionization_energy_ev": 4.177,
    },
    "Sr": {
        "oxidation_states": (2,),
        "electronegativity_value": 0.95,
        "first_ionization_energy_ev": 5.695,
    },
    "Y": {
        "oxidation_states": (3,),
        "electronegativity_value": 1.22,
        "first_ionization_energy_ev": 6.217,
    },
    "Zr": {
        "oxidation_states": (4,),
        "electronegativity_value": 1.33,
        "first_ionization_energy_ev": 6.634,
    },
    "Nb": {
        "oxidation_states": (5, 3),
        "electronegativity_value": 1.60,
        "first_ionization_energy_ev": 6.759,
    },
    "Mo": {
        "oxidation_states": (6,),
        "electronegativity_value": 2.16,
        "first_ionization_energy_ev": 7.092,
    },
    "Tc": {
        "oxidation_states": (7, 6, 4),
        "electronegativity_value": 1.90,
        "first_ionization_energy_ev": 7.280,
    },
    "Ru": {
        "oxidation_states": (3,),
        "electronegativity_value": 2.20,
        "first_ionization_energy_ev": 7.361,
    },
    "Rh": {
        "oxidation_states": (3,),
        "electronegativity_value": 2.28,
        "first_ionization_energy_ev": 7.459,
    },
    "Pd": {
        "oxidation_states": (3, 2),
        "electronegativity_value": 2.20,
        "first_ionization_energy_ev": 8.337,
    },
    "Ag": {
        "oxidation_states": (1,),
        "electronegativity_value": 1.93,
        "first_ionization_energy_ev": 7.576,
    },
    "Cd": {
        "oxidation_states": (2,),
        "electronegativity_value": 1.69,
        "first_ionization_energy_ev": 8.994,
    },
    "In": {
        "oxidation_states": (3,),
        "electronegativity_value": 1.78,
        "first_ionization_energy_ev": 5.786,
    },
    "Sn": {
        "oxidation_states": (4, 2),
        "electronegativity_value": 1.96,
        "first_ionization_energy_ev": 7.344,
    },
    "Sb": {
        "oxidation_states": (5, 3, -3),
        "electronegativity_value": 2.05,
        "first_ionization_energy_ev": 8.640,
    },
    "Te": {
        "oxidation_states": (6, 4, -2),
        "electronegativity_value": 2.10,
        "first_ionization_energy_ev": 9.010,
    },
    "I": {
        "oxidation_states": (7, 5, 1, -1),
        "electronegativity_value": 2.66,
        "first_ionization_energy_ev": 10.451,
    },
    "Xe": {
        "oxidation_states": (0,),
        "electronegativity_value": 2.60,
        "first_ionization_energy_ev": 12.130,
    },
}


def _level_2_chemistry_fields(symbol: str) -> dict[str, Any]:
    chemistry = _LEVEL_2_CHEMISTRY_BY_SYMBOL.get(symbol)
    if chemistry is None:
        return {
            "oxidation_states": (),
            "electronegativity_scale": None,
            "electronegativity_value": None,
            "electronegativity_source_key": None,
            "first_ionization_energy_ev": None,
            "first_ionization_energy_source_key": None,
            "bond_tendency_tags": (),
            "bond_tendency_source_key": None,
            "data_level": 1,
        }
    electronegativity_value = chemistry["electronegativity_value"]
    first_ionization_energy_ev = chemistry["first_ionization_energy_ev"]
    bond_tendency_tags = _BOND_TENDENCY_TAGS_BY_PUBCHEM_GROUP_BLOCK[
        _PUBCHEM_GROUP_BLOCK_BY_SYMBOL[symbol]
    ]
    if electronegativity_value is None:
        return {
            "oxidation_states": chemistry["oxidation_states"],
            "electronegativity_scale": None,
            "electronegativity_value": None,
            "electronegativity_source_key": None,
            "first_ionization_energy_ev": first_ionization_energy_ev,
            "first_ionization_energy_source_key": LEVEL_2_CHEMISTRY_SOURCE_REFERENCE.key,
            "bond_tendency_tags": bond_tendency_tags,
            "bond_tendency_source_key": LEVEL_2_CHEMISTRY_SOURCE_REFERENCE.key,
            "data_level": 2,
        }
    return {
        "oxidation_states": chemistry["oxidation_states"],
        "electronegativity_scale": "pauling",
        "electronegativity_value": electronegativity_value,
        "electronegativity_source_key": LEVEL_2_CHEMISTRY_SOURCE_REFERENCE.key,
        "first_ionization_energy_ev": first_ionization_energy_ev,
        "first_ionization_energy_source_key": LEVEL_2_CHEMISTRY_SOURCE_REFERENCE.key,
        "bond_tendency_tags": bond_tendency_tags,
        "bond_tendency_source_key": LEVEL_2_CHEMISTRY_SOURCE_REFERENCE.key,
        "data_level": 2,
    }


def _transition_phase_2_entry(
    *,
    outer_shell: str,
    d_shell: str,
    d_shell_stability: str,
    source_backed_configuration: str,
    simple_aufbau_candidate: str,
    behavior_tags: tuple[str, ...],
    exception_reason: str | None = None,
    variable_oxidation_states: bool = False,
    magnetic_relevance: bool = False,
    coordination_relevance: bool = True,
    catalytic_relevance: bool = False,
    alloy_relevance: bool = False,
    redox_relevance: bool = False,
) -> dict[str, Any]:
    return {
        "frontier_signature": FrontierSignature(
            outer_shell=outer_shell,
            d_shell=d_shell,
            valence_model="transition_metal",
            d_shell_stability=d_shell_stability,
            notes=(
                "outer ns and inner (n-1)d electrons jointly shape behavior",
                "oxidation, magnetic, coordination, catalytic, alloy, and redox fields "
                "are capability relevance markers",
            ),
        ),
        "configuration_audit": ConfigurationAudit(
            source_backed_configuration=source_backed_configuration,
            simple_aufbau_candidate=simple_aufbau_candidate,
            is_exception=simple_aufbau_candidate != source_backed_configuration,
            exception_reason=exception_reason,
        ),
        "transition_behavior_kernel": TransitionBehaviorKernel(
            variable_oxidation_states=variable_oxidation_states,
            magnetic_relevance=magnetic_relevance,
            coordination_relevance=coordination_relevance,
            catalytic_relevance=catalytic_relevance,
            alloy_relevance=alloy_relevance,
            redox_relevance=redox_relevance,
        ),
        "behavior_tags": behavior_tags,
    }


def _period_4_p_block_phase_2_entry(
    *,
    outer_shell: str,
    p_shell: str,
    source_backed_configuration: str,
    behavior_tags: tuple[str, ...],
    notes: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "frontier_signature": FrontierSignature(
            outer_shell=outer_shell,
            d_shell="3d^10",
            p_shell=p_shell,
            valence_model="period_4_p_block_d_core",
            d_shell_stability="filled_d_shell",
            notes=(
                "filled 3d core is preserved behind the period-4 p-block frontier",
            )
            + notes,
        ),
        "configuration_audit": ConfigurationAudit(
            source_backed_configuration=source_backed_configuration,
            simple_aufbau_candidate=source_backed_configuration,
        ),
        "transition_behavior_kernel": None,
        "behavior_tags": behavior_tags,
    }


def _period_5_p_block_phase_entry(
    *,
    outer_shell: str,
    p_shell: str,
    source_backed_configuration: str,
    behavior_tags: tuple[str, ...],
    notes: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "frontier_signature": FrontierSignature(
            outer_shell=outer_shell,
            d_shell="4d^10",
            p_shell=p_shell,
            valence_model="period_5_p_block_d_core",
            d_shell_stability="filled_d_shell",
            notes=(
                "filled 4d core is preserved behind the period-5 p-block frontier",
            )
            + notes,
        ),
        "configuration_audit": ConfigurationAudit(
            source_backed_configuration=source_backed_configuration,
            simple_aufbau_candidate=source_backed_configuration,
        ),
        "transition_behavior_kernel": None,
        "behavior_tags": behavior_tags,
    }


_PHASE_2_SYMBOLIC_STATE_BY_SYMBOL: dict[str, dict[str, Any]] = {
    "Sc": _transition_phase_2_entry(
        outer_shell="4s^2",
        d_shell="3d^1",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Ar] 3d^1 4s^2",
        simple_aufbau_candidate="[Ar] 3d^1 4s^2",
        behavior_tags=(
            "early_transition_metal",
            "sc_3_plus_pathway_common",
            "d_block_entry_point",
        ),
        coordination_relevance=True,
    ),
    "Ti": _transition_phase_2_entry(
        outer_shell="4s^2",
        d_shell="3d^2",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Ar] 3d^2 4s^2",
        simple_aufbau_candidate="[Ar] 3d^2 4s^2",
        behavior_tags=(
            "multiple_oxidation_states",
            "strong_oxide_forming_tendency",
            "lightweight_structural_metal",
        ),
        variable_oxidation_states=True,
        alloy_relevance=True,
        redox_relevance=True,
    ),
    "V": _transition_phase_2_entry(
        outer_shell="4s^2",
        d_shell="3d^3",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Ar] 3d^3 4s^2",
        simple_aufbau_candidate="[Ar] 3d^3 4s^2",
        behavior_tags=(
            "variable_oxidation_states",
            "redox_active",
            "transition_metal_chemistry_expressive",
        ),
        variable_oxidation_states=True,
        catalytic_relevance=True,
        redox_relevance=True,
    ),
    "Cr": _transition_phase_2_entry(
        outer_shell="4s^1",
        d_shell="3d^5",
        d_shell_stability="half_filled_d_shell",
        source_backed_configuration="[Ar] 3d^5 4s^1",
        simple_aufbau_candidate="[Ar] 3d^4 4s^2",
        exception_reason="half-filled d-shell stabilization pattern",
        behavior_tags=(
            "configuration_exception",
            "half_filled_d_shell_stabilization",
            "corrosion_resistant_alloy_relevance",
            "multiple_oxidation_states",
        ),
        variable_oxidation_states=True,
        magnetic_relevance=True,
        alloy_relevance=True,
        redox_relevance=True,
    ),
    "Mn": _transition_phase_2_entry(
        outer_shell="4s^2",
        d_shell="3d^5",
        d_shell_stability="half_filled_d_shell",
        source_backed_configuration="[Ar] 3d^5 4s^2",
        simple_aufbau_candidate="[Ar] 3d^5 4s^2",
        behavior_tags=(
            "multiple_oxidation_states",
            "redox_rich",
            "magnetic_material_relevance",
        ),
        variable_oxidation_states=True,
        magnetic_relevance=True,
        redox_relevance=True,
    ),
    "Fe": _transition_phase_2_entry(
        outer_shell="4s^2",
        d_shell="3d^6",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Ar] 3d^6 4s^2",
        simple_aufbau_candidate="[Ar] 3d^6 4s^2",
        behavior_tags=(
            "structural_civilization_metal",
            "fe_2_plus_fe_3_plus_pathways",
            "magnetic_behavior",
            "oxygen_binding_biological_relevance",
        ),
        variable_oxidation_states=True,
        magnetic_relevance=True,
        alloy_relevance=True,
        redox_relevance=True,
    ),
    "Co": _transition_phase_2_entry(
        outer_shell="4s^2",
        d_shell="3d^7",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Ar] 3d^7 4s^2",
        simple_aufbau_candidate="[Ar] 3d^7 4s^2",
        behavior_tags=(
            "magnetic_material_relevance",
            "coordination_chemistry",
            "alloy_catalyst_relevance",
        ),
        variable_oxidation_states=True,
        magnetic_relevance=True,
        catalytic_relevance=True,
        alloy_relevance=True,
        redox_relevance=True,
    ),
    "Ni": _transition_phase_2_entry(
        outer_shell="4s^2",
        d_shell="3d^8",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Ar] 3d^8 4s^2",
        simple_aufbau_candidate="[Ar] 3d^8 4s^2",
        behavior_tags=(
            "alloy_forming",
            "catalytic_relevance",
            "corrosion_resistant_material_behavior",
        ),
        variable_oxidation_states=True,
        catalytic_relevance=True,
        alloy_relevance=True,
        redox_relevance=True,
    ),
    "Cu": _transition_phase_2_entry(
        outer_shell="4s^1",
        d_shell="3d^10",
        d_shell_stability="filled_d_shell",
        source_backed_configuration="[Ar] 3d^10 4s^1",
        simple_aufbau_candidate="[Ar] 3d^9 4s^2",
        exception_reason="filled d-shell stabilization pattern",
        behavior_tags=(
            "configuration_exception",
            "filled_d_shell_stabilization",
            "high_conductivity_relevance",
            "cu_1_plus_cu_2_plus_pathways",
        ),
        variable_oxidation_states=True,
        magnetic_relevance=True,
        catalytic_relevance=True,
        alloy_relevance=True,
        redox_relevance=True,
    ),
    "Zn": _transition_phase_2_entry(
        outer_shell="4s^2",
        d_shell="3d^10",
        d_shell_stability="filled_d_shell",
        source_backed_configuration="[Ar] 3d^10 4s^2",
        simple_aufbau_candidate="[Ar] 3d^10 4s^2",
        behavior_tags=(
            "filled_d_shell",
            "zn_2_plus_pathway",
            "biologically_relevant_metal_ion",
        ),
        coordination_relevance=True,
        catalytic_relevance=True,
        alloy_relevance=True,
    ),
    "Ga": _period_4_p_block_phase_2_entry(
        outer_shell="4s^2 4p^1",
        p_shell="4p^1",
        source_backed_configuration="[Ar] 3d^10 4s^2 4p^1",
        behavior_tags=(
            "post_transition_metal",
            "low_melting_point_relevance",
            "semiconductor_material_relevance",
        ),
    ),
    "Ge": _period_4_p_block_phase_2_entry(
        outer_shell="4s^2 4p^2",
        p_shell="4p^2",
        source_backed_configuration="[Ar] 3d^10 4s^2 4p^2",
        behavior_tags=(
            "metalloid",
            "semiconductor_relevance",
            "silicon_family_relation",
        ),
    ),
    "As": _period_4_p_block_phase_2_entry(
        outer_shell="4s^2 4p^3",
        p_shell="4p^3",
        source_backed_configuration="[Ar] 3d^10 4s^2 4p^3",
        behavior_tags=(
            "metalloid",
            "toxicity_relevance",
            "multiple_oxidation_behavior",
        ),
        notes=("multiple oxidation behavior remains separate from measured Level 2 fields",),
    ),
    "Se": _period_4_p_block_phase_2_entry(
        outer_shell="4s^2 4p^4",
        p_shell="4p^4",
        source_backed_configuration="[Ar] 3d^10 4s^2 4p^4",
        behavior_tags=(
            "chalcogen",
            "trace_biological_relevance",
            "redox_behavior",
        ),
    ),
    "Br": _period_4_p_block_phase_2_entry(
        outer_shell="4s^2 4p^5",
        p_shell="4p^5",
        source_backed_configuration="[Ar] 3d^10 4s^2 4p^5",
        behavior_tags=(
            "halogen",
            "one_electron_completion_pressure",
            "liquid_halogen_reference_behavior",
        ),
    ),
    "Kr": _period_4_p_block_phase_2_entry(
        outer_shell="4s^2 4p^6",
        p_shell="4p^6",
        source_backed_configuration="[Ar] 3d^10 4s^2 4p^6",
        behavior_tags=(
            "noble_gas",
            "closed_shell",
            "low_reactivity_baseline",
        ),
        notes=("closed 4p shell creates low-reactivity baseline",),
    ),
    "Rb": {
        "frontier_signature": FrontierSignature(
            outer_shell="5s^1",
            valence_model="main_group",
            notes=("period-5 alkali-metal outer shell",),
        ),
        "configuration_audit": ConfigurationAudit(
            source_backed_configuration="[Kr] 5s^1",
            simple_aufbau_candidate="[Kr] 5s^1",
        ),
        "transition_behavior_kernel": None,
        "behavior_tags": ("alkali_metal", "period_5_s_block", "one_electron_loss_pathway"),
    },
    "Sr": {
        "frontier_signature": FrontierSignature(
            outer_shell="5s^2",
            valence_model="main_group",
            notes=("period-5 alkaline-earth outer shell",),
        ),
        "configuration_audit": ConfigurationAudit(
            source_backed_configuration="[Kr] 5s^2",
            simple_aufbau_candidate="[Kr] 5s^2",
        ),
        "transition_behavior_kernel": None,
        "behavior_tags": ("alkaline_earth_metal", "period_5_s_block", "sr_2_plus_pathway"),
    },
    "Y": _transition_phase_2_entry(
        outer_shell="5s^2",
        d_shell="4d^1",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Kr] 4d^1 5s^2",
        simple_aufbau_candidate="[Kr] 4d^1 5s^2",
        behavior_tags=("period_5_transition_metal", "y_3_plus_pathway", "rare_earth_relation"),
        coordination_relevance=True,
        alloy_relevance=True,
    ),
    "Zr": _transition_phase_2_entry(
        outer_shell="5s^2",
        d_shell="4d^2",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Kr] 4d^2 5s^2",
        simple_aufbau_candidate="[Kr] 4d^2 5s^2",
        behavior_tags=("period_5_transition_metal", "zirconium_oxide_relevance", "alloy_relevance"),
        coordination_relevance=True,
        alloy_relevance=True,
    ),
    "Nb": _transition_phase_2_entry(
        outer_shell="5s^1",
        d_shell="4d^4",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Kr] 4d^4 5s^1",
        simple_aufbau_candidate="[Kr] 4d^3 5s^2",
        exception_reason="period-5 d-shell stabilization pattern",
        behavior_tags=("configuration_exception", "period_5_transition_metal", "superalloy_relevance"),
        variable_oxidation_states=True,
        coordination_relevance=True,
        alloy_relevance=True,
        redox_relevance=True,
    ),
    "Mo": _transition_phase_2_entry(
        outer_shell="5s^1",
        d_shell="4d^5",
        d_shell_stability="half_filled_d_shell",
        source_backed_configuration="[Kr] 4d^5 5s^1",
        simple_aufbau_candidate="[Kr] 4d^4 5s^2",
        exception_reason="half-filled d-shell stabilization pattern",
        behavior_tags=("configuration_exception", "period_5_transition_metal", "high_temperature_alloy_relevance"),
        variable_oxidation_states=True,
        coordination_relevance=True,
        catalytic_relevance=True,
        alloy_relevance=True,
        redox_relevance=True,
    ),
    "Tc": _transition_phase_2_entry(
        outer_shell="5s^2",
        d_shell="4d^5",
        d_shell_stability="half_filled_d_shell",
        source_backed_configuration="[Kr] 4d^5 5s^2",
        simple_aufbau_candidate="[Kr] 4d^5 5s^2",
        behavior_tags=("period_5_transition_metal", "radioactive_element_boundary", "multiple_oxidation_states"),
        variable_oxidation_states=True,
        coordination_relevance=True,
        redox_relevance=True,
    ),
    "Ru": _transition_phase_2_entry(
        outer_shell="5s^1",
        d_shell="4d^7",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Kr] 4d^7 5s^1",
        simple_aufbau_candidate="[Kr] 4d^6 5s^2",
        exception_reason="period-5 d-shell stabilization pattern",
        behavior_tags=("configuration_exception", "period_5_transition_metal", "catalytic_relevance"),
        variable_oxidation_states=True,
        coordination_relevance=True,
        catalytic_relevance=True,
        alloy_relevance=True,
        redox_relevance=True,
    ),
    "Rh": _transition_phase_2_entry(
        outer_shell="5s^1",
        d_shell="4d^8",
        d_shell_stability="open_d_shell",
        source_backed_configuration="[Kr] 4d^8 5s^1",
        simple_aufbau_candidate="[Kr] 4d^7 5s^2",
        exception_reason="period-5 d-shell stabilization pattern",
        behavior_tags=("configuration_exception", "period_5_transition_metal", "catalytic_relevance"),
        variable_oxidation_states=True,
        coordination_relevance=True,
        catalytic_relevance=True,
        alloy_relevance=True,
    ),
    "Pd": _transition_phase_2_entry(
        outer_shell="5s^0",
        d_shell="4d^10",
        d_shell_stability="filled_d_shell",
        source_backed_configuration="[Kr] 4d^10",
        simple_aufbau_candidate="[Kr] 4d^8 5s^2",
        exception_reason="filled d-shell stabilization pattern with empty 5s outer occupancy",
        behavior_tags=("configuration_exception", "filled_d_shell", "catalytic_relevance"),
        variable_oxidation_states=True,
        coordination_relevance=True,
        catalytic_relevance=True,
        alloy_relevance=True,
    ),
    "Ag": _transition_phase_2_entry(
        outer_shell="5s^1",
        d_shell="4d^10",
        d_shell_stability="filled_d_shell",
        source_backed_configuration="[Kr] 4d^10 5s^1",
        simple_aufbau_candidate="[Kr] 4d^9 5s^2",
        exception_reason="filled d-shell stabilization pattern",
        behavior_tags=("configuration_exception", "filled_d_shell", "high_conductivity_relevance"),
        coordination_relevance=True,
        catalytic_relevance=True,
        alloy_relevance=True,
    ),
    "Cd": _transition_phase_2_entry(
        outer_shell="5s^2",
        d_shell="4d^10",
        d_shell_stability="filled_d_shell",
        source_backed_configuration="[Kr] 4d^10 5s^2",
        simple_aufbau_candidate="[Kr] 4d^10 5s^2",
        behavior_tags=("filled_d_shell", "cd_2_plus_pathway", "toxicity_relevance"),
        coordination_relevance=True,
        alloy_relevance=True,
    ),
    "In": _period_5_p_block_phase_entry(
        outer_shell="5s^2 5p^1",
        p_shell="5p^1",
        source_backed_configuration="[Kr] 4d^10 5s^2 5p^1",
        behavior_tags=("post_transition_metal", "period_5_p_block", "low_melting_point_relevance"),
    ),
    "Sn": _period_5_p_block_phase_entry(
        outer_shell="5s^2 5p^2",
        p_shell="5p^2",
        source_backed_configuration="[Kr] 4d^10 5s^2 5p^2",
        behavior_tags=("post_transition_metal", "period_5_p_block", "multiple_oxidation_behavior"),
    ),
    "Sb": _period_5_p_block_phase_entry(
        outer_shell="5s^2 5p^3",
        p_shell="5p^3",
        source_backed_configuration="[Kr] 4d^10 5s^2 5p^3",
        behavior_tags=("metalloid", "period_5_p_block", "toxicity_relevance"),
    ),
    "Te": _period_5_p_block_phase_entry(
        outer_shell="5s^2 5p^4",
        p_shell="5p^4",
        source_backed_configuration="[Kr] 4d^10 5s^2 5p^4",
        behavior_tags=("metalloid", "chalcogen", "redox_behavior"),
    ),
    "I": _period_5_p_block_phase_entry(
        outer_shell="5s^2 5p^5",
        p_shell="5p^5",
        source_backed_configuration="[Kr] 4d^10 5s^2 5p^5",
        behavior_tags=("halogen", "one_electron_completion_pressure", "heavy_halogen_behavior"),
    ),
    "Xe": _period_5_p_block_phase_entry(
        outer_shell="5s^2 5p^6",
        p_shell="5p^6",
        source_backed_configuration="[Kr] 4d^10 5s^2 5p^6",
        behavior_tags=("noble_gas", "closed_shell", "noble_gas_exception_chemistry_boundary"),
        notes=("closed 5p shell creates low-reactivity baseline with heavier noble gas exceptions",),
    ),
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


def _weight_unavailable() -> AtomicWeightModel:
    return AtomicWeightModel(
        model_type="unavailable",
        display="unavailable",
        notes=("CIAAW does not provide a standard atomic weight for this element.",),
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
    {
        "z": 37,
        "symbol": "Rb",
        "name": "Rubidium",
        "period": 5,
        "group": 1,
        "block": "s",
        "neutral": "[Kr] 5s^1",
        "cation": "[Kr]",
        "valence_shell": "5s",
        "valence_electrons": 1,
        "weight": _weight_single("85.4678(3)"),
    },
    {
        "z": 38,
        "symbol": "Sr",
        "name": "Strontium",
        "period": 5,
        "group": 2,
        "block": "s",
        "neutral": "[Kr] 5s^2",
        "cation": "[Kr] 5s^1",
        "valence_shell": "5s",
        "valence_electrons": 2,
        "weight": _weight_single("87.62(1)"),
    },
    {
        "z": 39,
        "symbol": "Y",
        "name": "Yttrium",
        "period": 5,
        "group": 3,
        "block": "d",
        "neutral": "[Kr] 4d^1 5s^2",
        "cation": "[Kr] 4d^1 5s^1",
        "valence_shell": "4d 5s",
        "valence_electrons": 3,
        "weight": _weight_single("88.905838(2)"),
    },
    {
        "z": 40,
        "symbol": "Zr",
        "name": "Zirconium",
        "period": 5,
        "group": 4,
        "block": "d",
        "neutral": "[Kr] 4d^2 5s^2",
        "cation": "[Kr] 4d^2 5s^1",
        "valence_shell": "4d 5s",
        "valence_electrons": 4,
        "weight": _weight_single("91.222(3)"),
    },
    {
        "z": 41,
        "symbol": "Nb",
        "name": "Niobium",
        "period": 5,
        "group": 5,
        "block": "d",
        "neutral": "[Kr] 4d^4 5s^1",
        "cation": "[Kr] 4d^4",
        "valence_shell": "4d 5s",
        "valence_electrons": 5,
        "weight": _weight_single("92.90637(1)"),
    },
    {
        "z": 42,
        "symbol": "Mo",
        "name": "Molybdenum",
        "period": 5,
        "group": 6,
        "block": "d",
        "neutral": "[Kr] 4d^5 5s^1",
        "cation": "[Kr] 4d^5",
        "valence_shell": "4d 5s",
        "valence_electrons": 6,
        "weight": _weight_single("95.95(1)"),
    },
    {
        "z": 43,
        "symbol": "Tc",
        "name": "Technetium",
        "period": 5,
        "group": 7,
        "block": "d",
        "neutral": "[Kr] 4d^5 5s^2",
        "cation": "[Kr] 4d^5 5s^1",
        "valence_shell": "4d 5s",
        "valence_electrons": 7,
        "weight": _weight_unavailable(),
    },
    {
        "z": 44,
        "symbol": "Ru",
        "name": "Ruthenium",
        "period": 5,
        "group": 8,
        "block": "d",
        "neutral": "[Kr] 4d^7 5s^1",
        "cation": "[Kr] 4d^7",
        "valence_shell": "4d 5s",
        "valence_electrons": 8,
        "weight": _weight_single("101.07(2)"),
    },
    {
        "z": 45,
        "symbol": "Rh",
        "name": "Rhodium",
        "period": 5,
        "group": 9,
        "block": "d",
        "neutral": "[Kr] 4d^8 5s^1",
        "cation": "[Kr] 4d^8",
        "valence_shell": "4d 5s",
        "valence_electrons": 9,
        "weight": _weight_single("102.90549(2)"),
    },
    {
        "z": 46,
        "symbol": "Pd",
        "name": "Palladium",
        "period": 5,
        "group": 10,
        "block": "d",
        "neutral": "[Kr] 4d^10",
        "cation": "[Kr] 4d^9",
        "valence_shell": "4d 5s",
        "valence_electrons": 10,
        "weight": _weight_single("106.42(1)"),
    },
    {
        "z": 47,
        "symbol": "Ag",
        "name": "Silver",
        "period": 5,
        "group": 11,
        "block": "d",
        "neutral": "[Kr] 4d^10 5s^1",
        "cation": "[Kr] 4d^10",
        "valence_shell": "4d 5s",
        "valence_electrons": 11,
        "weight": _weight_single("107.8682(2)"),
    },
    {
        "z": 48,
        "symbol": "Cd",
        "name": "Cadmium",
        "period": 5,
        "group": 12,
        "block": "d",
        "neutral": "[Kr] 4d^10 5s^2",
        "cation": "[Kr] 4d^10 5s^1",
        "valence_shell": "4d 5s",
        "valence_electrons": 12,
        "weight": _weight_single("112.414(4)"),
    },
    {
        "z": 49,
        "symbol": "In",
        "name": "Indium",
        "period": 5,
        "group": 13,
        "block": "p",
        "neutral": "[Kr] 4d^10 5s^2 5p^1",
        "cation": "[Kr] 4d^10 5s^2",
        "valence_shell": "5s 5p",
        "valence_electrons": 3,
        "weight": _weight_single("114.818(1)"),
    },
    {
        "z": 50,
        "symbol": "Sn",
        "name": "Tin",
        "period": 5,
        "group": 14,
        "block": "p",
        "neutral": "[Kr] 4d^10 5s^2 5p^2",
        "cation": "[Kr] 4d^10 5s^2 5p^1",
        "valence_shell": "5s 5p",
        "valence_electrons": 4,
        "weight": _weight_single("118.710(7)"),
    },
    {
        "z": 51,
        "symbol": "Sb",
        "name": "Antimony",
        "period": 5,
        "group": 15,
        "block": "p",
        "neutral": "[Kr] 4d^10 5s^2 5p^3",
        "cation": "[Kr] 4d^10 5s^2 5p^2",
        "valence_shell": "5s 5p",
        "valence_electrons": 5,
        "weight": _weight_single("121.760(1)"),
    },
    {
        "z": 52,
        "symbol": "Te",
        "name": "Tellurium",
        "period": 5,
        "group": 16,
        "block": "p",
        "neutral": "[Kr] 4d^10 5s^2 5p^4",
        "cation": "[Kr] 4d^10 5s^2 5p^3",
        "valence_shell": "5s 5p",
        "valence_electrons": 6,
        "weight": _weight_single("127.60(3)"),
    },
    {
        "z": 53,
        "symbol": "I",
        "name": "Iodine",
        "period": 5,
        "group": 17,
        "block": "p",
        "neutral": "[Kr] 4d^10 5s^2 5p^5",
        "cation": "[Kr] 4d^10 5s^2 5p^4",
        "valence_shell": "5s 5p",
        "valence_electrons": 7,
        "weight": _weight_single("126.90447(3)"),
    },
    {
        "z": 54,
        "symbol": "Xe",
        "name": "Xenon",
        "period": 5,
        "group": 18,
        "block": "p",
        "neutral": "[Kr] 4d^10 5s^2 5p^6",
        "cation": "[Kr] 4d^10 5s^2 5p^5",
        "valence_shell": "5s 5p",
        "valence_electrons": 8,
        "weight": _weight_single("131.293(6)"),
    },
)


def _make_base_element(raw_seed: dict[str, Any]) -> MulluStandardSymbolicElement:
    symbol = raw_seed["symbol"]
    atomic_number = raw_seed["z"]
    level_2_fields = _level_2_chemistry_fields(symbol)
    phase_2_fields = _PHASE_2_SYMBOLIC_STATE_BY_SYMBOL.get(symbol)
    has_level_2_chemistry = symbol in _LEVEL_2_CHEMISTRY_BY_SYMBOL
    has_phase_2_state = phase_2_fields is not None
    behavior_level_tag = (
        "mspee_level_2_chemistry_partial" if has_level_2_chemistry else "mspee_level_1_seed"
    )
    behavior_tags = (
        f"period_{raw_seed['period']}",
        f"group_{raw_seed['group']}",
        f"{raw_seed['block']}_block",
        behavior_level_tag,
    ) + (phase_2_fields["behavior_tags"] if has_phase_2_state else ())
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
            "PubChem periodic table properties -> oxidation_states, Pauling "
            "electronegativity, first_ionization_energy_ev, and GroupBlock-derived "
            "bond_tendency_tags",
        )
        if has_level_2_chemistry
        else ()
    ) + (
        (
            "Phase 2 transition exception kernel -> frontier_signature, "
            "configuration_audit, and capability flags",
            "simple Aufbau configuration remains an audit candidate; "
            "NIST-backed configuration remains authority",
        )
        if has_phase_2_state
        else ()
    )
    audit_notes = (
        "Level 1 seed does not claim full reaction prediction.",
        "Atomic weight intervals are stored as intervals, not collapsed constants.",
    ) + (
        (
            "Level 2 chemistry values are limited to oxidation-state set, Pauling "
            "electronegativity, first ionization energy, and PubChem GroupBlock-derived "
            "bond tendency tags.",
        )
        if has_level_2_chemistry
        else ()
    ) + (
        (
            "Phase 2 frontier signatures separate outer ns, inner d-shell, and "
            "period-4 p-block filled d-core context.",
            "Transition behavior fields are relevance flags, not guaranteed behavior "
            "for every compound.",
        )
        if has_phase_2_state
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
            first_ionization_energy_ev=level_2_fields["first_ionization_energy_ev"],
            first_ionization_energy_source_key=level_2_fields[
                "first_ionization_energy_source_key"
            ],
            bond_tendency_tags=level_2_fields["bond_tendency_tags"],
            bond_tendency_source_key=level_2_fields["bond_tendency_source_key"],
            frontier_signature=phase_2_fields["frontier_signature"]
            if has_phase_2_state
            else None,
            configuration_audit=phase_2_fields["configuration_audit"]
            if has_phase_2_state
            else None,
            transition_behavior_kernel=phase_2_fields["transition_behavior_kernel"]
            if has_phase_2_state
            else None,
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
    expected_atomic_numbers = tuple(range(1, 55))
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
