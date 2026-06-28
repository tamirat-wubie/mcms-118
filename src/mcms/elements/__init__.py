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

__all__ = [
    "AtomicWeightModel",
    "ElementExposure",
    "ElementHistory",
    "ElementIdentity",
    "ElementLaws",
    "ElementRelationEdge",
    "ElementSeedPackValidationResult",
    "ElementState",
    "MulluStandardSymbolicElement",
    "SourceReference",
    "build_element_receipt",
    "get_seed_element",
    "list_seed_elements",
    "validate_seed_pack",
]
