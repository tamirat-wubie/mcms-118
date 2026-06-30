"""Purpose: JSON Schema exports for MSPEE element and snapshot records.

Project scope: exposes stable machine contracts for source-backed element records.
Dependencies: local MSPEE model constants and standard-library deep copy.
Invariants: schemas are deterministic; exported schemas reject undeclared fields.
"""

from __future__ import annotations

from copy import deepcopy

from mcms.elements.atom_behavior import (
    ATOM_BEHAVIOR_NON_CLAIMS,
    VALID_ATOM_BEHAVIOR_STATUSES,
)
from mcms.elements.model import (
    ELECTRONEGATIVITY_MAX,
    ELECTRONEGATIVITY_MIN,
    FIRST_IONIZATION_ENERGY_MAX_EV,
    FIRST_IONIZATION_ENERGY_MIN_EV,
    OXIDATION_STATE_MAX,
    OXIDATION_STATE_MIN,
    VALID_BLOCKS,
    VALID_BOND_TENDENCY_TAGS,
    VALID_D_SHELL_STABILITY_STATES,
    VALID_ELECTRONEGATIVITY_SCALES,
    VALID_FRONTIER_VALENCE_MODELS,
    VALID_RELATION_TYPES,
    VALID_WEIGHT_MODEL_TYPES,
)
from mcms.elements.snapshot import VALID_SNAPSHOT_BLOCKS, VALID_SNAPSHOT_STATUSES

JSON_SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
ELEMENT_SCHEMA_ID = (
    "https://schemas.mullusi.com/mcms/elements/"
    "mullu-standard-symbolic-element.schema.json"
)
SNAPSHOT_SCHEMA_ID = (
    "https://schemas.mullusi.com/mcms/elements/"
    "element-source-snapshot-record.schema.json"
)
ATOM_BEHAVIOR_SCHEMA_ID = (
    "https://schemas.mullusi.com/mcms/elements/"
    "atom-behavior-profile.schema.json"
)
SCHEMA_BUNDLE_ID = "https://schemas.mullusi.com/mcms/elements/schema-bundle.json"


def _string_array() -> dict:
    return {"type": "array", "items": {"type": "string"}}


def _source_reference_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["key", "authority", "title", "url", "version"],
        "properties": {
            "key": {"type": "string", "minLength": 1},
            "authority": {"type": "string", "minLength": 1},
            "title": {"type": "string", "minLength": 1},
            "url": {"type": "string", "format": "uri", "pattern": "^https://"},
            "version": {"type": "string", "minLength": 1},
        },
    }


def _atomic_weight_model_schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "model_type",
            "display",
            "lower_bound",
            "upper_bound",
            "unit",
            "source_key",
            "notes",
        ],
        "properties": {
            "model_type": {"type": "string", "enum": sorted(VALID_WEIGHT_MODEL_TYPES)},
            "display": {"type": "string", "minLength": 1},
            "lower_bound": {"type": ["string", "null"]},
            "upper_bound": {"type": ["string", "null"]},
            "unit": {"type": "string", "const": "standard_atomic_weight"},
            "source_key": {
                "type": "string",
                "const": "ciaaw_standard_atomic_weights_2024",
            },
            "notes": _string_array(),
        },
    }


def _element_defs() -> dict:
    return {
        "SourceReference": _source_reference_schema(),
        "AtomicWeightModel": _atomic_weight_model_schema(),
        "ElementIdentity": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "atomic_number",
                "symbol",
                "name",
                "proton_count",
                "identity_rule",
            ],
            "properties": {
                "atomic_number": {"type": "integer", "minimum": 1, "maximum": 118},
                "symbol": {"type": "string", "minLength": 1},
                "name": {"type": "string", "minLength": 1},
                "proton_count": {"type": "integer", "minimum": 1, "maximum": 118},
                "identity_rule": {
                    "type": "string",
                    "const": "element_identity := proton_count",
                },
            },
        },
        "ElementLaws": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "neutral_charge_rule",
                "isotope_rule",
                "electron_capacity_rule",
                "conservation_rules",
                "special_constraints",
            ],
            "properties": {
                "neutral_charge_rule": {"type": "string", "minLength": 1},
                "isotope_rule": {"type": "string", "minLength": 1},
                "electron_capacity_rule": {"type": "string", "minLength": 1},
                "conservation_rules": _string_array(),
                "special_constraints": _string_array(),
            },
        },
        "ElementRelationEdge": {
            "type": "object",
            "additionalProperties": False,
            "required": ["source_symbol", "target_symbol", "relation_type", "reason"],
            "properties": {
                "source_symbol": {"type": "string", "minLength": 1},
                "target_symbol": {"type": "string", "minLength": 1},
                "relation_type": {
                    "type": "string",
                    "enum": sorted(VALID_RELATION_TYPES),
                },
                "reason": {"type": "string", "minLength": 1},
            },
        },
        "FrontierSignature": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "outer_shell",
                "d_shell",
                "p_shell",
                "valence_model",
                "d_shell_stability",
                "notes",
            ],
            "properties": {
                "outer_shell": {"type": "string", "minLength": 1},
                "d_shell": {"type": ["string", "null"]},
                "p_shell": {"type": ["string", "null"]},
                "valence_model": {
                    "type": "string",
                    "enum": sorted(VALID_FRONTIER_VALENCE_MODELS),
                },
                "d_shell_stability": {
                    "type": ["string", "null"],
                    "enum": sorted(VALID_D_SHELL_STABILITY_STATES) + [None],
                },
                "notes": _string_array(),
            },
        },
        "ConfigurationAudit": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "source_backed_configuration",
                "simple_aufbau_candidate",
                "is_exception",
                "exception_reason",
            ],
            "properties": {
                "source_backed_configuration": {"type": "string", "minLength": 1},
                "simple_aufbau_candidate": {"type": ["string", "null"]},
                "is_exception": {"type": "boolean"},
                "exception_reason": {"type": ["string", "null"]},
            },
            "allOf": [
                {
                    "if": {"properties": {"is_exception": {"const": True}}},
                    "then": {
                        "properties": {
                            "simple_aufbau_candidate": {"type": "string", "minLength": 1},
                            "exception_reason": {"type": "string", "minLength": 1},
                        }
                    },
                }
            ],
        },
        "TransitionBehaviorKernel": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "variable_oxidation_states",
                "magnetic_relevance",
                "coordination_relevance",
                "catalytic_relevance",
                "alloy_relevance",
                "redox_relevance",
            ],
            "properties": {
                "variable_oxidation_states": {"type": "boolean"},
                "magnetic_relevance": {"type": "boolean"},
                "coordination_relevance": {"type": "boolean"},
                "catalytic_relevance": {"type": "boolean"},
                "alloy_relevance": {"type": "boolean"},
                "redox_relevance": {"type": "boolean"},
            },
        },
        "ElementState": {
            "type": "object",
            "additionalProperties": False,
            "allOf": [
                {
                    "oneOf": [
                        {
                            "properties": {
                                "electronegativity_scale": {"type": "null"},
                                "electronegativity_value": {"type": "null"},
                                "electronegativity_source_key": {"type": "null"},
                            }
                        },
                        {
                            "properties": {
                                "electronegativity_scale": {
                                    "type": "string",
                                    "enum": sorted(VALID_ELECTRONEGATIVITY_SCALES),
                                },
                                "electronegativity_value": {
                                    "type": "number",
                                    "minimum": ELECTRONEGATIVITY_MIN,
                                    "maximum": ELECTRONEGATIVITY_MAX,
                                },
                                "electronegativity_source_key": {"type": "string", "minLength": 1},
                            },
                            "required": [
                                "electronegativity_scale",
                                "electronegativity_value",
                                "electronegativity_source_key",
                            ],
                        },
                    ]
                },
                {
                    "oneOf": [
                        {
                            "properties": {
                                "first_ionization_energy_ev": {"type": "null"},
                                "first_ionization_energy_source_key": {"type": "null"},
                            }
                        },
                        {
                            "properties": {
                                "first_ionization_energy_ev": {
                                    "type": "number",
                                    "minimum": FIRST_IONIZATION_ENERGY_MIN_EV,
                                    "maximum": FIRST_IONIZATION_ENERGY_MAX_EV,
                                },
                                "first_ionization_energy_source_key": {
                                    "type": "string",
                                    "minLength": 1,
                                },
                            },
                            "required": [
                                "first_ionization_energy_ev",
                                "first_ionization_energy_source_key",
                            ],
                        },
                    ]
                },
                {
                    "oneOf": [
                        {
                            "properties": {
                                "bond_tendency_tags": {"type": "array", "maxItems": 0},
                                "bond_tendency_source_key": {"type": "null"},
                            }
                        },
                        {
                            "properties": {
                                "bond_tendency_tags": {
                                    "type": "array",
                                    "uniqueItems": True,
                                    "minItems": 1,
                                    "items": {
                                        "type": "string",
                                        "enum": sorted(VALID_BOND_TENDENCY_TAGS),
                                    },
                                },
                                "bond_tendency_source_key": {"type": "string", "minLength": 1},
                            },
                            "required": [
                                "bond_tendency_tags",
                                "bond_tendency_source_key",
                            ],
                        },
                    ]
                },
            ],
            "required": [
                "neutral_electron_count",
                "neutral_electron_configuration",
                "first_cation_configuration",
                "period",
                "group",
                "block",
                "valence_shell",
                "valence_electrons",
                "atomic_weight_model",
                "oxidation_states",
                "electronegativity_scale",
                "electronegativity_value",
                "electronegativity_source_key",
                "first_ionization_energy_ev",
                "first_ionization_energy_source_key",
                "bond_tendency_tags",
                "bond_tendency_source_key",
                "frontier_signature",
                "configuration_audit",
                "transition_behavior_kernel",
                "behavior_tags",
                "relation_edges",
                "data_level",
            ],
            "properties": {
                "neutral_electron_count": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 118,
                },
                "neutral_electron_configuration": {"type": "string", "minLength": 1},
                "first_cation_configuration": {"type": ["string", "null"]},
                "period": {"type": "integer", "minimum": 1, "maximum": 7},
                "group": {"type": "integer", "minimum": 1, "maximum": 18},
                "block": {"type": "string", "enum": sorted(VALID_BLOCKS)},
                "valence_shell": {"type": "string", "minLength": 1},
                "valence_electrons": {"type": "integer", "minimum": 1, "maximum": 16},
                "atomic_weight_model": {"$ref": "#/$defs/AtomicWeightModel"},
                "oxidation_states": {
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "integer",
                        "minimum": OXIDATION_STATE_MIN,
                        "maximum": OXIDATION_STATE_MAX,
                    },
                },
                "electronegativity_scale": {
                    "type": ["string", "null"],
                    "enum": sorted(VALID_ELECTRONEGATIVITY_SCALES) + [None],
                },
                "electronegativity_value": {
                    "type": ["number", "null"],
                    "minimum": ELECTRONEGATIVITY_MIN,
                    "maximum": ELECTRONEGATIVITY_MAX,
                },
                "electronegativity_source_key": {"type": ["string", "null"]},
                "first_ionization_energy_ev": {
                    "type": ["number", "null"],
                    "minimum": FIRST_IONIZATION_ENERGY_MIN_EV,
                    "maximum": FIRST_IONIZATION_ENERGY_MAX_EV,
                },
                "first_ionization_energy_source_key": {"type": ["string", "null"]},
                "bond_tendency_tags": {
                    "type": "array",
                    "uniqueItems": True,
                    "items": {
                        "type": "string",
                        "enum": sorted(VALID_BOND_TENDENCY_TAGS),
                    },
                },
                "bond_tendency_source_key": {"type": ["string", "null"]},
                "frontier_signature": {
                    "anyOf": [
                        {"type": "null"},
                        {"$ref": "#/$defs/FrontierSignature"},
                    ]
                },
                "configuration_audit": {
                    "anyOf": [
                        {"type": "null"},
                        {"$ref": "#/$defs/ConfigurationAudit"},
                    ]
                },
                "transition_behavior_kernel": {
                    "anyOf": [
                        {"type": "null"},
                        {"$ref": "#/$defs/TransitionBehaviorKernel"},
                    ]
                },
                "behavior_tags": _string_array(),
                "relation_edges": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/ElementRelationEdge"},
                },
                "data_level": {"type": "integer", "enum": [1, 2, 3]},
            },
        },
        "ElementExposure": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "human_view",
                "machine_view",
                "graph_view",
                "chemistry_view_enabled",
                "physics_view_enabled",
                "education_view_enabled",
            ],
            "properties": {
                "human_view": {"type": "string", "minLength": 1},
                "machine_view": {"type": "string", "const": "json"},
                "graph_view": {"type": "string", "pattern": "^node:element/"},
                "chemistry_view_enabled": {"type": "boolean"},
                "physics_view_enabled": {"type": "boolean"},
                "education_view_enabled": {"type": "boolean"},
            },
        },
        "ElementHistory": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "source_references",
                "derivation_trace",
                "validation_status",
                "last_audit",
                "audit_notes",
            ],
            "properties": {
                "source_references": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/SourceReference"},
                    "minItems": 1,
                },
                "derivation_trace": _string_array(),
                "validation_status": {"type": "string", "minLength": 1},
                "last_audit": {"type": "string", "minLength": 1},
                "audit_notes": _string_array(),
            },
        },
    }


def element_seed_json_schema() -> dict:
    return deepcopy(
        {
            "$schema": JSON_SCHEMA_DRAFT,
            "$id": ELEMENT_SCHEMA_ID,
            "title": "MulluStandardSymbolicElement",
            "type": "object",
            "additionalProperties": False,
            "required": [
                "id",
                "symbol_family",
                "identity",
                "laws",
                "state",
                "exposure",
                "history",
            ],
            "properties": {
                "id": {"type": "string", "pattern": "^MSPEE-Z[0-9]{3}-[A-Z][a-z]?$"},
                "symbol_family": {"type": "string", "const": "element"},
                "identity": {"$ref": "#/$defs/ElementIdentity"},
                "laws": {"$ref": "#/$defs/ElementLaws"},
                "state": {"$ref": "#/$defs/ElementState"},
                "exposure": {"$ref": "#/$defs/ElementExposure"},
                "history": {"$ref": "#/$defs/ElementHistory"},
            },
            "$defs": _element_defs(),
        }
    )


def element_snapshot_json_schema() -> dict:
    return deepcopy(
        {
            "$schema": JSON_SCHEMA_DRAFT,
            "$id": SNAPSHOT_SCHEMA_ID,
            "title": "ElementSourceSnapshotRecord",
            "type": "object",
            "additionalProperties": False,
            "required": [
                "atomic_number",
                "symbol",
                "name",
                "period",
                "group",
                "block",
                "atomic_weight_model",
                "source_keys",
                "snapshot_status",
                "level_1_seed_available",
                "notes",
            ],
            "properties": {
                "atomic_number": {"type": "integer", "minimum": 1, "maximum": 118},
                "symbol": {"type": "string", "minLength": 1},
                "name": {"type": "string", "minLength": 1},
                "period": {"type": "integer", "minimum": 1, "maximum": 7},
                "group": {"type": ["integer", "null"], "minimum": 1, "maximum": 18},
                "block": {"type": "string", "enum": sorted(VALID_SNAPSHOT_BLOCKS)},
                "atomic_weight_model": {"$ref": "#/$defs/AtomicWeightModel"},
                "source_keys": _string_array(),
                "snapshot_status": {
                    "type": "string",
                    "enum": sorted(VALID_SNAPSHOT_STATUSES),
                },
                "level_1_seed_available": {"type": "boolean"},
                "notes": _string_array(),
            },
            "$defs": {
                "AtomicWeightModel": _atomic_weight_model_schema(),
            },
        }
    )


def atom_behavior_profile_json_schema() -> dict:
    return deepcopy(
        {
            "$schema": JSON_SCHEMA_DRAFT,
            "$id": ATOM_BEHAVIOR_SCHEMA_ID,
            "title": "AtomBehaviorProfile",
            "type": "object",
            "additionalProperties": False,
            "required": [
                "profile_id",
                "isotope_id",
                "element_id",
                "symbol",
                "atomic_number",
                "proton_count",
                "neutron_count",
                "mass_number",
                "charge",
                "electron_count",
                "isotope_evidence_status",
                "neutral_electron_configuration",
                "quantum_state_basis",
                "nuclear_behavior_basis",
                "electron_behavior_basis",
                "force_layer_basis",
                "matter_behavior_tags",
                "source_keys",
                "profile_status",
                "derivation_trace",
                "non_claims",
            ],
            "properties": {
                "profile_id": {
                    "type": "string",
                    "pattern": (
                        "^MSPEE-Z[0-9]{3}-[A-Z][a-z]?-isotope-[0-9]+-"
                        "charge-(neutral-0|plus-[0-9]+|minus-[0-9]+)-"
                        "atom-behavior-v2$"
                    ),
                },
                "isotope_id": {
                    "type": "string",
                    "pattern": "^MSPEE-Z[0-9]{3}-[A-Z][a-z]?-isotope-[0-9]+$",
                },
                "element_id": {"type": "string", "pattern": "^MSPEE-Z[0-9]{3}-[A-Z][a-z]?$"},
                "symbol": {"type": "string", "minLength": 1},
                "atomic_number": {"type": "integer", "minimum": 1, "maximum": 118},
                "proton_count": {"type": "integer", "minimum": 1, "maximum": 118},
                "neutron_count": {"type": "integer", "minimum": 0},
                "mass_number": {"type": "integer", "minimum": 1},
                "charge": {"type": "integer", "minimum": -118, "maximum": 118},
                "electron_count": {"type": "integer", "minimum": 0},
                "isotope_evidence_status": {
                    "type": "string",
                    "enum": ["radioisotope_evidence", "stable_isotope_evidence"],
                },
                "neutral_electron_configuration": {"type": "string", "minLength": 1},
                "quantum_state_basis": _string_array(),
                "nuclear_behavior_basis": _string_array(),
                "electron_behavior_basis": _string_array(),
                "force_layer_basis": _string_array(),
                "matter_behavior_tags": _string_array(),
                "source_keys": _string_array(),
                "profile_status": {
                    "type": "string",
                    "enum": sorted(VALID_ATOM_BEHAVIOR_STATUSES),
                },
                "derivation_trace": _string_array(),
                "non_claims": {
                    "type": "array",
                    "items": {"type": "string"},
                    "const": list(ATOM_BEHAVIOR_NON_CLAIMS),
                },
            },
        }
    )


def element_schema_bundle() -> dict:
    return {
        "$schema": JSON_SCHEMA_DRAFT,
        "$id": SCHEMA_BUNDLE_ID,
        "schemas": {
            "mullu_standard_symbolic_element": element_seed_json_schema(),
            "element_source_snapshot_record": element_snapshot_json_schema(),
            "atom_behavior_profile": atom_behavior_profile_json_schema(),
        },
    }
