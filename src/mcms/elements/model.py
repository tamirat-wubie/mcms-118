"""Purpose: typed MSPEE symbolic element contracts.

Governance scope: defines auditable identity, law, state, exposure, and history fields.
Dependencies: Python dataclasses, hashlib, and JSON canonicalization.
Invariants: identity equals proton count; neutral electron count equals atomic number;
all source-backed seed records validate before platform exposure.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256

VALID_BLOCKS = {"s", "p", "d", "f"}
VALID_WEIGHT_MODEL_TYPES = {"interval", "single", "unavailable"}
VALID_RELATION_TYPES = {"same_group", "same_period", "same_block"}


@dataclass(frozen=True)
class SourceReference:
    key: str
    authority: str
    title: str
    url: str
    version: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.key:
            errors.append("source key is required.")
        if not self.authority:
            errors.append("source authority is required.")
        if not self.title:
            errors.append("source title is required.")
        if not self.url.startswith("https://"):
            errors.append("source url must be https.")
        if not self.version:
            errors.append("source version is required.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class AtomicWeightModel:
    model_type: str
    display: str
    lower_bound: str | None = None
    upper_bound: str | None = None
    unit: str = "standard_atomic_weight"
    source_key: str = "ciaaw_standard_atomic_weights_2024"
    notes: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.model_type not in VALID_WEIGHT_MODEL_TYPES:
            errors.append("atomic weight model type is unknown.")
        if not self.display:
            errors.append("atomic weight display is required.")
        if self.model_type == "interval" and not (self.lower_bound and self.upper_bound):
            errors.append("interval atomic weight requires lower and upper bounds.")
        if self.model_type == "single" and (self.lower_bound or self.upper_bound):
            errors.append("single atomic weight must not carry interval bounds.")
        if self.model_type == "unavailable" and (self.lower_bound or self.upper_bound):
            errors.append("unavailable atomic weight must not carry interval bounds.")
        if not self.source_key:
            errors.append("atomic weight source key is required.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementIdentity:
    atomic_number: int
    symbol: str
    name: str
    proton_count: int
    identity_rule: str = "element_identity := proton_count"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementLaws:
    neutral_charge_rule: str = "neutral_electron_count = atomic_number"
    isotope_rule: str = "mass_number = protons + neutrons"
    electron_capacity_rule: str = "subshell_capacity = 2(2l + 1)"
    conservation_rules: tuple[str, ...] = (
        "charge must balance in valid reaction claims",
        "nucleon count must be explicit in isotope reasoning",
        "electron count changes define ion state, not element identity",
    )
    special_constraints: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.neutral_charge_rule:
            errors.append("neutral charge rule is required.")
        if not self.isotope_rule:
            errors.append("isotope rule is required.")
        if not self.electron_capacity_rule:
            errors.append("electron capacity rule is required.")
        if not self.conservation_rules:
            errors.append("at least one conservation rule is required.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementRelationEdge:
    source_symbol: str
    target_symbol: str
    relation_type: str
    reason: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.source_symbol or not self.target_symbol:
            errors.append("relation source and target symbols are required.")
        if self.source_symbol == self.target_symbol:
            errors.append("relation edge cannot target the source element.")
        if self.relation_type not in VALID_RELATION_TYPES:
            errors.append("relation type is unknown.")
        if not self.reason:
            errors.append("relation reason is required.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementState:
    neutral_electron_count: int
    neutral_electron_configuration: str
    first_cation_configuration: str | None
    period: int
    group: int
    block: str
    valence_shell: str
    valence_electrons: int
    atomic_weight_model: AtomicWeightModel
    oxidation_states: tuple[int, ...] = ()
    behavior_tags: tuple[str, ...] = ()
    relation_edges: tuple[ElementRelationEdge, ...] = ()
    data_level: int = 1

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.neutral_electron_count <= 0:
            errors.append("neutral electron count must be positive.")
        if not self.neutral_electron_configuration:
            errors.append("neutral electron configuration is required.")
        if self.period < 1 or self.period > 7:
            errors.append("period must be in [1, 7].")
        if self.group < 1 or self.group > 18:
            errors.append("group must be in [1, 18].")
        if self.block not in VALID_BLOCKS:
            errors.append("block must be one of s, p, d, f.")
        if not self.valence_shell:
            errors.append("valence shell is required.")
        if self.valence_electrons < 1 or self.valence_electrons > 8:
            errors.append("valence electron count must be in [1, 8] for Level 1 seeds.")
        if self.data_level not in {1, 2, 3}:
            errors.append("data level must be 1, 2, or 3.")
        errors.extend(self.atomic_weight_model.validate())
        for edge in self.relation_edges:
            errors.extend(edge.validate())
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementExposure:
    human_view: str
    machine_view: str = "json"
    graph_view: str = ""
    chemistry_view_enabled: bool = True
    physics_view_enabled: bool = False
    education_view_enabled: bool = True

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.human_view:
            errors.append("human view is required.")
        if self.machine_view != "json":
            errors.append("machine view must be json.")
        if not self.graph_view.startswith("node:element/"):
            errors.append("graph view must use node:element/ prefix.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementHistory:
    source_references: tuple[SourceReference, ...]
    derivation_trace: tuple[str, ...]
    validation_status: str
    last_audit: str
    audit_notes: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.source_references:
            errors.append("at least one source reference is required.")
        for source_reference in self.source_references:
            errors.extend(source_reference.validate())
        source_keys = self.source_keys()
        if "ciaaw_standard_atomic_weights_2024" not in source_keys:
            errors.append("CIAAW atomic-weight source is required.")
        if "nist_electronic_configurations" not in source_keys:
            errors.append("NIST electron-configuration source is required.")
        if not self.derivation_trace:
            errors.append("derivation trace is required.")
        if not self.validation_status:
            errors.append("validation status is required.")
        if not self.last_audit:
            errors.append("last audit marker is required.")
        return errors

    def source_keys(self) -> tuple[str, ...]:
        return tuple(source_reference.key for source_reference in self.source_references)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class MulluStandardSymbolicElement:
    id: str
    symbol_family: str
    identity: ElementIdentity
    laws: ElementLaws
    state: ElementState
    exposure: ElementExposure
    history: ElementHistory

    def validate(self) -> list[str]:
        errors: list[str] = []
        expected_id = f"MSPEE-Z{self.identity.atomic_number:03d}-{self.identity.symbol}"
        if self.id != expected_id:
            errors.append("element id does not match MSPEE canonical id.")
        if self.symbol_family != "element":
            errors.append("symbol family must be element.")
        if self.identity.atomic_number < 1 or self.identity.atomic_number > 118:
            errors.append("atomic number must be in [1, 118].")
        if self.identity.atomic_number != self.identity.proton_count:
            errors.append("identity fracture: atomic number must equal proton count.")
        if not self.identity.symbol:
            errors.append("canonical symbol is required.")
        if not self.identity.name:
            errors.append("canonical name is required.")
        if self.state.neutral_electron_count != self.identity.atomic_number:
            errors.append("neutral electron count must equal atomic number.")
        errors.extend(self.laws.validate())
        errors.extend(self.state.validate())
        errors.extend(self.exposure.validate())
        errors.extend(self.history.validate())
        return errors

    def source_keys(self) -> tuple[str, ...]:
        return self.history.source_keys()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementSeedPackValidationResult:
    element_count: int
    relation_edge_count: int
    invalid_elements: tuple[str, ...]
    source_keys: tuple[str, ...]
    validation_status: str

    def to_dict(self) -> dict:
        return asdict(self)


def build_element_receipt(element: MulluStandardSymbolicElement) -> dict:
    element_payload = element.to_dict()
    canonical = json.dumps(element_payload, sort_keys=True, separators=(",", ":"))
    validation_errors = element.validate()
    return {
        "element_id": element.id,
        "symbol": element.identity.symbol,
        "validation_status": "element_seed_validated" if not validation_errors else "element_seed_rejected",
        "validation_errors": validation_errors,
        "source_keys": element.source_keys(),
        "element_hash": sha256(canonical.encode("utf-8")).hexdigest(),
    }
