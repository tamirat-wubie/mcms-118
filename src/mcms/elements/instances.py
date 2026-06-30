"""Purpose: typed MSPEE ion and isotope state-instance contracts.

Project scope: derives non-neutral element state IDs from validated element
identity records without mutating source-backed element seeds.
Dependencies: dataclasses, Level 1 seed records, and the 118-element snapshot.
Invariants: proton-count identity is preserved; ion electron count and isotope
neutron count are derived through explicit first-principles laws.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from mcms.elements.seed import get_seed_element
from mcms.elements.snapshot import get_snapshot_record

VALID_ELEMENT_INSTANCE_STATUSES = {
    "ion_instance_validated",
    "isotope_instance_validated",
}


def _element_id(atomic_number: int, symbol: str) -> str:
    return f"MSPEE-Z{atomic_number:03d}-{symbol}"


def _charge_label(charge: int) -> str:
    if charge > 0:
        return f"plus-{charge}"
    if charge < 0:
        return f"minus-{abs(charge)}"
    return "neutral-0"


def _ion_instance_id(atomic_number: int, symbol: str, charge: int) -> str:
    return f"{_element_id(atomic_number, symbol)}-ion-{_charge_label(charge)}"


def _isotope_instance_id(atomic_number: int, symbol: str, mass_number: int) -> str:
    return f"{_element_id(atomic_number, symbol)}-isotope-{mass_number}"


@dataclass(frozen=True)
class ElementIonInstance:
    instance_id: str
    element_id: str
    symbol: str
    atomic_number: int
    proton_count: int
    charge: int
    electron_count: int
    source_element_configuration: str
    instance_status: str = "ion_instance_validated"
    derivation_trace: tuple[str, ...] = (
        "element_identity := proton_count",
        "ion_electron_count = atomic_number - charge",
        "charge changes electron state, not element identity",
    )
    notes: tuple[str, ...] = (
        "Ion instance validates electron count only; it does not claim common-ion stability.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        expected_element_id = _element_id(self.atomic_number, self.symbol)
        expected_instance_id = _ion_instance_id(self.atomic_number, self.symbol, self.charge)
        if self.atomic_number < 1 or self.atomic_number > 118:
            errors.append("atomic number must be in [1, 118].")
        if self.proton_count != self.atomic_number:
            errors.append("ion instance must preserve proton-count identity.")
        if self.element_id != expected_element_id:
            errors.append("ion element_id does not match canonical element identity.")
        if self.instance_id != expected_instance_id:
            errors.append("ion instance_id does not match canonical ion ID.")
        if self.charge == 0:
            errors.append("ion instance requires nonzero charge; use the neutral element record.")
        if abs(self.charge) > self.atomic_number:
            errors.append("ion charge magnitude exceeds atomic-number validation boundary.")
        if self.electron_count != self.atomic_number - self.charge:
            errors.append("ion electron count must equal atomic_number - charge.")
        if self.electron_count < 0:
            errors.append("ion electron count cannot be negative.")
        if not self.source_element_configuration:
            errors.append("ion instance requires source element configuration context.")
        if self.instance_status not in VALID_ELEMENT_INSTANCE_STATUSES:
            errors.append("ion instance status is unknown.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementIsotopeInstance:
    instance_id: str
    element_id: str
    symbol: str
    atomic_number: int
    proton_count: int
    mass_number: int
    neutron_count: int
    source_atomic_weight_status: str
    instance_status: str = "isotope_instance_validated"
    derivation_trace: tuple[str, ...] = (
        "element_identity := proton_count",
        "mass_number = protons + neutrons",
        "neutron_count = mass_number - atomic_number",
        "neutron changes isotope state, not element identity",
    )
    notes: tuple[str, ...] = (
        "Isotope instance validates mass-number identity only; abundance, half-life, "
        "and decay evidence remain separate future fields.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        expected_element_id = _element_id(self.atomic_number, self.symbol)
        expected_instance_id = _isotope_instance_id(
            self.atomic_number,
            self.symbol,
            self.mass_number,
        )
        if self.atomic_number < 1 or self.atomic_number > 118:
            errors.append("atomic number must be in [1, 118].")
        if self.proton_count != self.atomic_number:
            errors.append("isotope instance must preserve proton-count identity.")
        if self.element_id != expected_element_id:
            errors.append("isotope element_id does not match canonical element identity.")
        if self.instance_id != expected_instance_id:
            errors.append("isotope instance_id does not match canonical isotope ID.")
        if self.mass_number < self.atomic_number:
            errors.append("mass number must be greater than or equal to atomic number.")
        if self.neutron_count != self.mass_number - self.atomic_number:
            errors.append("neutron count must equal mass_number - atomic_number.")
        if self.neutron_count < 0:
            errors.append("neutron count cannot be negative.")
        if not self.source_atomic_weight_status:
            errors.append("isotope instance requires source atomic-weight status context.")
        if self.instance_status not in VALID_ELEMENT_INSTANCE_STATUSES:
            errors.append("isotope instance status is unknown.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


def build_ion_instance(identifier: str | int, charge: int) -> ElementIonInstance:
    if charge == 0:
        raise ValueError("ion charge must be nonzero; use the neutral element record.")
    element = get_seed_element(identifier)
    atomic_number = element.identity.atomic_number
    symbol = element.identity.symbol
    electron_count = atomic_number - charge
    instance = ElementIonInstance(
        instance_id=_ion_instance_id(atomic_number, symbol, charge),
        element_id=element.id,
        symbol=symbol,
        atomic_number=atomic_number,
        proton_count=element.identity.proton_count,
        charge=charge,
        electron_count=electron_count,
        source_element_configuration=element.state.neutral_electron_configuration,
    )
    validation_errors = instance.validate()
    if validation_errors:
        raise ValueError("; ".join(validation_errors))
    return instance


def build_isotope_instance(identifier: str | int, mass_number: int) -> ElementIsotopeInstance:
    snapshot = get_snapshot_record(identifier)
    instance = ElementIsotopeInstance(
        instance_id=_isotope_instance_id(snapshot.atomic_number, snapshot.symbol, mass_number),
        element_id=_element_id(snapshot.atomic_number, snapshot.symbol),
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        proton_count=snapshot.atomic_number,
        mass_number=mass_number,
        neutron_count=mass_number - snapshot.atomic_number,
        source_atomic_weight_status=snapshot.atomic_weight_model.model_type,
    )
    validation_errors = instance.validate()
    if validation_errors:
        raise ValueError("; ".join(validation_errors))
    return instance
