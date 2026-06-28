"""Purpose: public MSPEE element-engine interface.

Governance scope: exposes source-backed symbolic element seed records only.
Dependencies: local dataclass models and deterministic seed-pack builders.
Invariants: element identity is proton-count anchored; validation never mutates records.
"""

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
    build_element_receipt,
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
    "ElementExposure",
    "ElementHistory",
    "ElementIdentity",
    "ElementLaws",
    "ElementRelationEdge",
    "ElementSeedPackValidationResult",
    "ElementSnapshotValidationResult",
    "ElementState",
    "ElementSourceSnapshotRecord",
    "MulluStandardSymbolicElement",
    "SourceReference",
    "build_element_receipt",
    "build_snapshot_receipt",
    "get_seed_element",
    "get_snapshot_record",
    "list_full_snapshot_records",
    "list_seed_elements",
    "validate_full_snapshot",
    "validate_seed_pack",
]
