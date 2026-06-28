"""Purpose: public MSPEE element-engine interface.

Project scope: exposes source-backed element seed records only.
Dependencies: local dataclass models and deterministic seed-pack builders.
Invariants: element identity is proton-count anchored; validation never mutates records.
"""

from mcms.elements.dashboard import (
    ElementDashboardViewModel,
    build_element_dashboard_view_model,
)
from mcms.elements.graph import (
    ElementGraphEdge,
    ElementGraphNode,
    ElementRelationGraph,
    build_element_relation_graph,
)
from mcms.elements.model import (
    VALID_D_SHELL_STABILITY_STATES,
    VALID_FRONTIER_VALENCE_MODELS,
    VALID_RELATION_TYPES,
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
    build_element_receipt,
    validate_configuration_audit,
)
from mcms.elements.schema import (
    element_schema_bundle,
    element_seed_json_schema,
    element_snapshot_json_schema,
)
from mcms.elements.seed import (
    get_seed_element,
    list_seed_elements,
    validate_seed_pack,
)
from mcms.elements.snapshot import (
    ElementSnapshotValidationResult,
    ElementSourceSnapshotRecord,
    build_snapshot_receipt,
    get_snapshot_record,
    list_full_snapshot_records,
    validate_full_snapshot,
)

__all__ = [
    "AtomicWeightModel",
    "ConfigurationAudit",
    "ElementExposure",
    "ElementDashboardViewModel",
    "ElementGraphEdge",
    "ElementGraphNode",
    "ElementHistory",
    "ElementIdentity",
    "ElementLaws",
    "ElementRelationEdge",
    "ElementRelationGraph",
    "ElementSeedPackValidationResult",
    "ElementSnapshotValidationResult",
    "ElementState",
    "ElementSourceSnapshotRecord",
    "FrontierSignature",
    "MulluStandardSymbolicElement",
    "SourceReference",
    "TransitionBehaviorKernel",
    "VALID_D_SHELL_STABILITY_STATES",
    "VALID_FRONTIER_VALENCE_MODELS",
    "VALID_RELATION_TYPES",
    "build_element_receipt",
    "build_element_dashboard_view_model",
    "build_element_relation_graph",
    "build_snapshot_receipt",
    "element_schema_bundle",
    "element_seed_json_schema",
    "element_snapshot_json_schema",
    "get_seed_element",
    "get_snapshot_record",
    "list_full_snapshot_records",
    "list_seed_elements",
    "validate_full_snapshot",
    "validate_configuration_audit",
    "validate_seed_pack",
]
