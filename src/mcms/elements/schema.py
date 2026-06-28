"""Purpose: JSON Schema exports for MSPEE element and snapshot records.

Governance scope: exposes stable machine contracts for source-backed element records.
Dependencies: local MSPEE model constants and standard-library deep copy.
Invariants: schemas are deterministic; exported schemas reject undeclared fields.
"""

from __future__ import annotations

from copy import deepcopy

from mcms.elements.model import VALID_BLOCKS, VALID_RELATION_TYPES, VALID_WEIGHT_MODEL_TYPES
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
        "ElementState": {
            "type": "object",
            "additionalProperties": False,
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
                "oxidation_states": {"type": "array", "items": {"type": "integer"}},
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


def element_schema_bundle() -> dict:
    return {
        "$schema": JSON_SCHEMA_DRAFT,
        "$id": SCHEMA_BUNDLE_ID,
        "schemas": {
            "mullu_standard_symbolic_element": element_seed_json_schema(),
            "element_source_snapshot_record": element_snapshot_json_schema(),
        },
    }
