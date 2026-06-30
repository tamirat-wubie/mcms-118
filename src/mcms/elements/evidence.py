"""Purpose: bounded MSPEE isotope and common-ion evidence records.

Project scope: stores a small source-backed evidence seed for isotope and
common-ion reasoning without claiming a complete isotope or ion-stability database.
Dependencies: local element instances, seed records, and source references.
Invariants: evidence records preserve element identity and keep measured/source
fields separate from derived state-instance counts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from mcms.elements.instances import (
    build_ion_instance,
    build_isotope_instance,
)
from mcms.elements.model import SourceReference
from mcms.elements.seed import get_seed_element
from mcms.elements.snapshot import get_snapshot_record

ISOTOPE_EVIDENCE_SOURCE_REFERENCES = (
    SourceReference(
        key="ciaaw_isotopic_compositions_2024",
        authority="CIAAW/IUPAC",
        title="Isotopic Compositions of the Elements 2024",
        url="https://www.ciaaw.org/isotopic-abundances.htm",
        version="2024",
    ),
    SourceReference(
        key="nist_atomic_weights_isotopic_compositions",
        authority="NIST",
        title="Atomic Weights and Isotopic Compositions",
        url="https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl",
        version="NIST Physical Measurement Laboratory reference table",
    ),
    SourceReference(
        key="pubchem_carbon_14_record",
        authority="PubChem/NCBI",
        title="Carbon-14 Compound Summary",
        url="https://pubchem.ncbi.nlm.nih.gov/compound/Carbon-14",
        version="source page observed 2026-06-29",
    ),
)

COMMON_ION_EVIDENCE_SOURCE_REFERENCES = (
    SourceReference(
        key="pubchem_periodic_table_properties",
        authority="PubChem/NCBI",
        title="PubChem Periodic Table of Elements CSV",
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV",
        version="source page observed 2026-06-28",
    ),
)

PHYSICAL_PROPERTY_EVIDENCE_SOURCE_REFERENCES = (
    SourceReference(
        key="pubchem_periodic_table_properties",
        authority="PubChem/NCBI",
        title="PubChem Periodic Table of Elements CSV",
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV",
        version="source page observed 2026-06-29",
    ),
)

VALID_ISOTOPE_EVIDENCE_STATUSES = {
    "stable_isotope_evidence",
    "radioisotope_evidence",
}
VALID_COMMON_ION_EVIDENCE_STATUSES = {"common_ion_candidate_evidence"}
VALID_UNRESOLVED_EVIDENCE_DOMAINS = {"isotope_evidence", "common_ion_evidence"}
VALID_UNRESOLVED_EVIDENCE_STATUSES = {"evidence_unresolved"}
VALID_STANDARD_STATES = {"Gas", "Liquid", "Solid"}
VALID_PHYSICAL_PROPERTY_EVIDENCE_STATUSES = {"physical_property_evidence"}
VALID_UNRESOLVED_PHYSICAL_PROPERTY_STATUSES = {"physical_property_evidence_unresolved"}


@dataclass(frozen=True)
class IsotopeEvidenceRecord:
    isotope_id: str
    element_id: str
    symbol: str
    atomic_number: int
    mass_number: int
    neutron_count: int
    relative_atomic_mass: str
    isotopic_composition: str | None
    half_life_value: float | None
    half_life_unit: str | None
    decay_mode: str | None
    source_keys: tuple[str, ...]
    evidence_status: str
    notes: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        isotope_instance = build_isotope_instance(self.symbol, self.mass_number)
        if self.isotope_id != isotope_instance.instance_id:
            errors.append("isotope evidence id must match canonical isotope instance id.")
        if self.element_id != isotope_instance.element_id:
            errors.append("isotope evidence element id must match isotope instance element id.")
        if self.atomic_number != isotope_instance.atomic_number:
            errors.append("isotope evidence atomic number must match isotope instance.")
        if self.neutron_count != isotope_instance.neutron_count:
            errors.append("isotope evidence neutron count must match isotope instance.")
        if not self.relative_atomic_mass:
            errors.append("relative atomic mass evidence is required.")
        if not self.source_keys:
            errors.append("isotope evidence requires at least one source key.")
        if self.evidence_status not in VALID_ISOTOPE_EVIDENCE_STATUSES:
            errors.append("isotope evidence status is unknown.")
        if self.evidence_status == "stable_isotope_evidence":
            if self.half_life_value is not None or self.decay_mode is not None:
                errors.append("stable isotope evidence must not carry decay fields.")
            if self.isotopic_composition is None:
                errors.append("stable isotope evidence requires isotopic composition.")
        if self.evidence_status == "radioisotope_evidence":
            if self.half_life_value is None or self.half_life_value <= 0:
                errors.append("radioisotope evidence requires positive half-life value.")
            if not self.half_life_unit:
                errors.append("radioisotope evidence requires half-life unit.")
            if not self.decay_mode:
                errors.append("radioisotope evidence requires decay mode.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CommonIonEvidenceRecord:
    ion_id: str
    element_id: str
    symbol: str
    atomic_number: int
    charge: int
    electron_count: int
    source_keys: tuple[str, ...]
    evidence_basis: str
    evidence_status: str = "common_ion_candidate_evidence"
    notes: tuple[str, ...] = (
        "Common-ion evidence is bounded to sourced oxidation-state support; it is not a "
        "guarantee that every compound or environment stabilizes this ion.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        ion_instance = build_ion_instance(self.symbol, self.charge)
        element = get_seed_element(self.symbol)
        if self.ion_id != ion_instance.instance_id:
            errors.append("common-ion evidence id must match canonical ion instance id.")
        if self.element_id != ion_instance.element_id:
            errors.append("common-ion element id must match ion instance element id.")
        if self.atomic_number != ion_instance.atomic_number:
            errors.append("common-ion atomic number must match ion instance.")
        if self.electron_count != ion_instance.electron_count:
            errors.append("common-ion electron count must match ion instance.")
        if self.charge not in element.state.oxidation_states:
            errors.append("common-ion charge must be present in sourced oxidation states.")
        if not self.source_keys:
            errors.append("common-ion evidence requires at least one source key.")
        if not self.evidence_basis:
            errors.append("common-ion evidence basis is required.")
        if self.evidence_status not in VALID_COMMON_ION_EVIDENCE_STATUSES:
            errors.append("common-ion evidence status is unknown.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class PhysicalPropertyEvidenceRecord:
    element_id: str
    symbol: str
    atomic_number: int
    standard_state: str
    melting_point_k: float
    boiling_point_k: float
    density_value: float
    density_unit: str
    source_keys: tuple[str, ...]
    phase_transition_note: str | None = None
    evidence_status: str = "physical_property_evidence"
    notes: tuple[str, ...] = (
        "Physical-property evidence is sourced measurement/reference data; it is not "
        "a symbolic behavior inference.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        expected_element_id = f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}"
        if self.element_id != expected_element_id:
            errors.append("physical-property element id must match snapshot element id.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("physical-property atomic number must match snapshot element.")
        if self.standard_state not in VALID_STANDARD_STATES:
            errors.append("standard state must be Gas, Liquid, or Solid.")
        if self.melting_point_k <= 0:
            errors.append("melting point must be a positive kelvin value.")
        if self.boiling_point_k <= 0:
            errors.append("boiling point must be a positive kelvin value.")
        if self.melting_point_k >= self.boiling_point_k and not self.phase_transition_note:
            errors.append(
                "melting point must be below boiling point unless a phase-transition "
                "exception note is present."
            )
        if self.density_value <= 0:
            errors.append("density must be positive.")
        if self.density_unit != "g/cm^3":
            errors.append("density unit must be g/cm^3.")
        if not self.source_keys:
            errors.append("physical-property evidence requires at least one source key.")
        if self.evidence_status not in VALID_PHYSICAL_PROPERTY_EVIDENCE_STATUSES:
            errors.append("physical-property evidence status is unknown.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class UnresolvedPhysicalPropertyEvidenceRecord:
    element_id: str
    symbol: str
    atomic_number: int
    standard_state: str
    melting_point_k: float | None
    boiling_point_k: float | None
    density_value: float | None
    missing_fields: tuple[str, ...]
    source_keys: tuple[str, ...]
    unresolved_status: str = "physical_property_evidence_unresolved"
    notes: tuple[str, ...] = (
        "Physical-property evidence is unresolved because the source row is incomplete; "
        "missing measured values are not guessed.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        expected_element_id = f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}"
        if self.element_id != expected_element_id:
            errors.append("unresolved physical-property element id must match snapshot element id.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("unresolved physical-property atomic number must match snapshot element.")
        if not self.standard_state:
            errors.append("unresolved physical-property standard state is required when source has one.")
        if not self.missing_fields:
            errors.append("unresolved physical-property record requires missing fields.")
        if self.melting_point_k is not None and self.melting_point_k <= 0:
            errors.append("unresolved melting point must be positive when present.")
        if self.boiling_point_k is not None and self.boiling_point_k <= 0:
            errors.append("unresolved boiling point must be positive when present.")
        if self.density_value is not None and self.density_value <= 0:
            errors.append("unresolved density must be positive when present.")
        if not self.source_keys:
            errors.append("unresolved physical-property evidence requires at least one source key.")
        if self.unresolved_status not in VALID_UNRESOLVED_PHYSICAL_PROPERTY_STATUSES:
            errors.append("unresolved physical-property status is unknown.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class UnresolvedEvidenceRecord:
    receipt_id: str
    element_id: str
    symbol: str
    atomic_number: int
    evidence_domain: str
    missing_evidence: tuple[str, ...]
    source_boundary: str
    unresolved_status: str = "evidence_unresolved"
    notes: tuple[str, ...] = (
        "Evidence is unresolved because this layer has not yet been sourced for the element.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        snapshot = get_snapshot_record(self.symbol)
        expected_element_id = f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}"
        expected_receipt_id = f"{expected_element_id}-{self.evidence_domain}-unresolved"
        if self.element_id != expected_element_id:
            errors.append("unresolved evidence element id must match snapshot element id.")
        if self.atomic_number != snapshot.atomic_number:
            errors.append("unresolved evidence atomic number must match snapshot element.")
        if self.receipt_id != expected_receipt_id:
            errors.append("unresolved evidence receipt id is not canonical.")
        if self.evidence_domain not in VALID_UNRESOLVED_EVIDENCE_DOMAINS:
            errors.append("unresolved evidence domain is unknown.")
        if not self.missing_evidence:
            errors.append("unresolved evidence requires missing evidence labels.")
        if not self.source_boundary:
            errors.append("unresolved evidence source boundary is required.")
        if self.unresolved_status not in VALID_UNRESOLVED_EVIDENCE_STATUSES:
            errors.append("unresolved evidence status is unknown.")
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


_ISOTOPE_EVIDENCE_ROWS = (
    {
        "symbol": "H",
        "mass_number": 1,
        "relative_atomic_mass": "1.00782503223(9)",
        "isotopic_composition": "0.999885(70)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "H",
        "mass_number": 2,
        "relative_atomic_mass": "2.01410177812(12)",
        "isotopic_composition": "0.000115(70)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "H",
        "mass_number": 3,
        "relative_atomic_mass": "3.01604928199(23)",
        "isotopic_composition": None,
        "half_life_value": 12.32,
        "half_life_unit": "years",
        "decay_mode": "beta_minus",
        "source_keys": (
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "radioisotope_evidence",
    },
    {
        "symbol": "He",
        "mass_number": 3,
        "relative_atomic_mass": "3.01602932265(22)",
        "isotopic_composition": "0.00000134(3)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "He",
        "mass_number": 4,
        "relative_atomic_mass": "4.00260325413(6)",
        "isotopic_composition": "0.99999866(3)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Li",
        "mass_number": 6,
        "relative_atomic_mass": "6.0151228874(16)",
        "isotopic_composition": "0.0759(4)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Li",
        "mass_number": 7,
        "relative_atomic_mass": "7.0160034366(45)",
        "isotopic_composition": "0.9241(4)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Be",
        "mass_number": 9,
        "relative_atomic_mass": "9.012183065(82)",
        "isotopic_composition": "1",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "B",
        "mass_number": 10,
        "relative_atomic_mass": "10.01293695(41)",
        "isotopic_composition": "0.199(7)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "B",
        "mass_number": 11,
        "relative_atomic_mass": "11.00930536(45)",
        "isotopic_composition": "0.801(7)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "C",
        "mass_number": 12,
        "relative_atomic_mass": "12.0000000(00)",
        "isotopic_composition": "0.9893(8)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "C",
        "mass_number": 13,
        "relative_atomic_mass": "13.00335483507(23)",
        "isotopic_composition": "0.0107(8)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "C",
        "mass_number": 14,
        "relative_atomic_mass": "14.0032419884(40)",
        "isotopic_composition": None,
        "half_life_value": 5730.0,
        "half_life_unit": "years",
        "decay_mode": "beta_minus",
        "source_keys": (
            "nist_atomic_weights_isotopic_compositions",
            "pubchem_carbon_14_record",
        ),
        "evidence_status": "radioisotope_evidence",
    },
    {
        "symbol": "N",
        "mass_number": 14,
        "relative_atomic_mass": "14.00307400443(20)",
        "isotopic_composition": "0.99636(20)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "N",
        "mass_number": 15,
        "relative_atomic_mass": "15.00010889888(64)",
        "isotopic_composition": "0.00364(20)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "O",
        "mass_number": 16,
        "relative_atomic_mass": "15.99491461957(17)",
        "isotopic_composition": "0.99757(16)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "O",
        "mass_number": 17,
        "relative_atomic_mass": "16.99913175650(69)",
        "isotopic_composition": "0.00038(1)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "O",
        "mass_number": 18,
        "relative_atomic_mass": "17.99915961286(76)",
        "isotopic_composition": "0.00205(14)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "F",
        "mass_number": 19,
        "relative_atomic_mass": "18.99840316273(92)",
        "isotopic_composition": "1",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ne",
        "mass_number": 20,
        "relative_atomic_mass": "19.9924401762(17)",
        "isotopic_composition": "0.9048(3)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ne",
        "mass_number": 21,
        "relative_atomic_mass": "20.993846685(41)",
        "isotopic_composition": "0.0027(1)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ne",
        "mass_number": 22,
        "relative_atomic_mass": "21.991385114(18)",
        "isotopic_composition": "0.0925(3)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Na",
        "mass_number": 23,
        "relative_atomic_mass": "22.9897692820(19)",
        "isotopic_composition": "1",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Mg",
        "mass_number": 24,
        "relative_atomic_mass": "23.985041697(14)",
        "isotopic_composition": "0.7899(4)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Mg",
        "mass_number": 25,
        "relative_atomic_mass": "24.985836976(50)",
        "isotopic_composition": "0.1000(1)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Mg",
        "mass_number": 26,
        "relative_atomic_mass": "25.982592968(31)",
        "isotopic_composition": "0.1101(3)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Al",
        "mass_number": 27,
        "relative_atomic_mass": "26.98153853(11)",
        "isotopic_composition": "1",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Si",
        "mass_number": 28,
        "relative_atomic_mass": "27.97692653465(44)",
        "isotopic_composition": "0.92223(19)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Si",
        "mass_number": 29,
        "relative_atomic_mass": "28.97649466490(52)",
        "isotopic_composition": "0.04685(8)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Si",
        "mass_number": 30,
        "relative_atomic_mass": "29.973770136(23)",
        "isotopic_composition": "0.03092(11)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "P",
        "mass_number": 31,
        "relative_atomic_mass": "30.97376199842(70)",
        "isotopic_composition": "1",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "S",
        "mass_number": 32,
        "relative_atomic_mass": "31.9720711744(14)",
        "isotopic_composition": "0.9499(26)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "S",
        "mass_number": 33,
        "relative_atomic_mass": "32.9714589098(15)",
        "isotopic_composition": "0.0075(2)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "S",
        "mass_number": 34,
        "relative_atomic_mass": "33.967867004(47)",
        "isotopic_composition": "0.0425(24)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "S",
        "mass_number": 36,
        "relative_atomic_mass": "35.96708071(20)",
        "isotopic_composition": "0.0001(1)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Cl",
        "mass_number": 35,
        "relative_atomic_mass": "34.968852682(37)",
        "isotopic_composition": "0.7576(10)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Cl",
        "mass_number": 37,
        "relative_atomic_mass": "36.965902602(55)",
        "isotopic_composition": "0.2424(10)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ar",
        "mass_number": 36,
        "relative_atomic_mass": "35.967545105(28)",
        "isotopic_composition": "0.003336(21)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ar",
        "mass_number": 38,
        "relative_atomic_mass": "37.96273211(21)",
        "isotopic_composition": "0.000629(7)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ar",
        "mass_number": 40,
        "relative_atomic_mass": "39.9623831237(24)",
        "isotopic_composition": "0.996035(25)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "K",
        "mass_number": 39,
        "relative_atomic_mass": "38.9637064864(49)",
        "isotopic_composition": "0.932581(44)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "K",
        "mass_number": 40,
        "relative_atomic_mass": "39.963998166(60)",
        "isotopic_composition": "0.000117(1)",
        "half_life_value": 1.248e9,
        "half_life_unit": "years",
        "decay_mode": "electron_capture_or_beta_decay",
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "radioisotope_evidence",
    },
    {
        "symbol": "K",
        "mass_number": 41,
        "relative_atomic_mass": "40.9618252579(41)",
        "isotopic_composition": "0.067302(44)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ca",
        "mass_number": 40,
        "relative_atomic_mass": "39.962590863(22)",
        "isotopic_composition": "0.96941(156)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ca",
        "mass_number": 42,
        "relative_atomic_mass": "41.95861783(16)",
        "isotopic_composition": "0.00647(23)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ca",
        "mass_number": 43,
        "relative_atomic_mass": "42.95876644(24)",
        "isotopic_composition": "0.00135(10)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ca",
        "mass_number": 44,
        "relative_atomic_mass": "43.95548156(35)",
        "isotopic_composition": "0.02086(110)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ca",
        "mass_number": 46,
        "relative_atomic_mass": "45.9536890(24)",
        "isotopic_composition": "0.00004(3)",
        "half_life_value": None,
        "half_life_unit": None,
        "decay_mode": None,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "stable_isotope_evidence",
    },
    {
        "symbol": "Ca",
        "mass_number": 48,
        "relative_atomic_mass": "47.95252276(13)",
        "isotopic_composition": "0.00187(21)",
        "half_life_value": 6.4e19,
        "half_life_unit": "years",
        "decay_mode": "double_beta_decay",
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": "radioisotope_evidence",
    },
)

_SC_ZN_ISOTOPE_EVIDENCE_ROWS = tuple(
    {
        "symbol": symbol,
        "mass_number": mass_number,
        "relative_atomic_mass": relative_atomic_mass,
        "isotopic_composition": isotopic_composition,
        "half_life_value": half_life_value,
        "half_life_unit": half_life_unit,
        "decay_mode": decay_mode,
        "source_keys": (
            "ciaaw_isotopic_compositions_2024",
            "nist_atomic_weights_isotopic_compositions",
        ),
        "evidence_status": (
            "radioisotope_evidence"
            if half_life_value is not None
            else "stable_isotope_evidence"
        ),
    }
    for (
        symbol,
        mass_number,
        relative_atomic_mass,
        isotopic_composition,
        half_life_value,
        half_life_unit,
        decay_mode,
    ) in (
        ("Sc", 45, "44.95590828(77)", "1", None, None, None),
        ("Ti", 46, "45.95262772(35)", "0.0825(3)", None, None, None),
        ("Ti", 47, "46.95175879(38)", "0.0744(2)", None, None, None),
        ("Ti", 48, "47.94794198(38)", "0.7372(3)", None, None, None),
        ("Ti", 49, "48.94786568(39)", "0.0541(2)", None, None, None),
        ("Ti", 50, "49.94478689(39)", "0.0518(2)", None, None, None),
        ("V", 50, "49.94715601(95)", "0.00250(4)", 1.5e17, "years", "electron_capture_or_beta_decay"),
        ("V", 51, "50.94395704(94)", "0.99750(4)", None, None, None),
        ("Cr", 50, "49.94604183(94)", "0.04345(13)", None, None, None),
        ("Cr", 52, "51.94050623(63)", "0.83789(18)", None, None, None),
        ("Cr", 53, "52.94064815(62)", "0.09501(17)", None, None, None),
        ("Cr", 54, "53.93887916(61)", "0.02365(7)", None, None, None),
        ("Mn", 55, "54.93804391(48)", "1", None, None, None),
        ("Fe", 54, "53.93960899(53)", "0.05845(35)", None, None, None),
        ("Fe", 56, "55.93493633(49)", "0.91754(36)", None, None, None),
        ("Fe", 57, "56.93539284(49)", "0.02119(10)", None, None, None),
        ("Fe", 58, "57.93327443(53)", "0.00282(4)", None, None, None),
        ("Co", 59, "58.93319429(56)", "1", None, None, None),
        ("Ni", 58, "57.93534241(52)", "0.68077(19)", None, None, None),
        ("Ni", 60, "59.93078588(52)", "0.26223(15)", None, None, None),
        ("Ni", 61, "60.93105557(52)", "0.011399(13)", None, None, None),
        ("Ni", 62, "61.92834537(55)", "0.036346(40)", None, None, None),
        ("Ni", 64, "63.92796682(58)", "0.009255(19)", None, None, None),
        ("Cu", 63, "62.92959772(56)", "0.6915(15)", None, None, None),
        ("Cu", 65, "64.92778970(71)", "0.3085(15)", None, None, None),
        ("Zn", 64, "63.92914201(71)", "0.4917(75)", None, None, None),
        ("Zn", 66, "65.92603381(94)", "0.2773(98)", None, None, None),
        ("Zn", 67, "66.92712775(96)", "0.0404(16)", None, None, None),
        ("Zn", 68, "67.92484455(98)", "0.1845(63)", None, None, None),
        ("Zn", 70, "69.9253192(21)", "0.0061(10)", None, None, None),
    )
)

_COMMON_ION_EVIDENCE_ROWS = (
    ("Na", 1),
    ("Mg", 2),
    ("Cl", -1),
    ("Ca", 2),
    ("Fe", 2),
    ("Fe", 3),
    ("Cu", 1),
    ("Cu", 2),
    ("Zn", 2),
)

_PHYSICAL_PROPERTY_EVIDENCE_ROWS = (
    ("H", "Gas", 13.81, 20.28, 8.988e-05),
    ("He", "Gas", 0.95, 4.22, 0.0001785),
    ("Li", "Solid", 453.65, 1615.0, 0.534),
    ("Be", "Solid", 1560.0, 2744.0, 1.85),
    ("B", "Solid", 2348.0, 4273.0, 2.37),
    ("C", "Solid", 3823.0, 4098.0, 2.267),
    ("N", "Gas", 63.15, 77.36, 0.0012506),
    ("O", "Gas", 54.36, 90.2, 0.001429),
    ("F", "Gas", 53.53, 85.03, 0.001696),
    ("Ne", "Gas", 24.56, 27.07, 0.0008999),
    ("Na", "Solid", 370.95, 1156.0, 0.97),
    ("Mg", "Solid", 923.0, 1363.0, 1.74),
    ("Al", "Solid", 933.437, 2792.0, 2.7),
    ("Si", "Solid", 1687.0, 3538.0, 2.3296),
    ("P", "Solid", 317.3, 553.65, 1.82),
    ("S", "Solid", 388.36, 717.75, 2.067),
    ("Cl", "Gas", 171.65, 239.11, 0.003214),
    ("Ar", "Gas", 83.8, 87.3, 0.0017837),
    ("K", "Solid", 336.53, 1032.0, 0.89),
    ("Ca", "Solid", 1115.0, 1757.0, 1.54),
    ("Sc", "Solid", 1814.0, 3109.0, 2.99),
    ("Ti", "Solid", 1941.0, 3560.0, 4.5),
    ("V", "Solid", 2183.0, 3680.0, 6.0),
    ("Cr", "Solid", 2180.0, 2944.0, 7.15),
    ("Mn", "Solid", 1519.0, 2334.0, 7.3),
    ("Fe", "Solid", 1811.0, 3134.0, 7.874),
    ("Co", "Solid", 1768.0, 3200.0, 8.86),
    ("Ni", "Solid", 1728.0, 3186.0, 8.912),
    ("Cu", "Solid", 1357.77, 2835.0, 8.933),
    ("Zn", "Solid", 692.68, 1180.0, 7.134),
    ("Ga", "Solid", 302.91, 2477.0, 5.91),
    ("Ge", "Solid", 1211.4, 3106.0, 5.323),
    (
        "As",
        "Solid",
        1090.0,
        887.0,
        5.776,
        "PubChem phase-transition values carry a melting/boiling ordering anomaly; "
        "record preserved as source evidence instead of normalized.",
    ),
    ("Se", "Solid", 493.65, 958.0, 4.809),
    ("Br", "Liquid", 265.95, 331.95, 3.11),
    ("Kr", "Gas", 115.79, 119.93, 0.003733),
    ("Rb", "Solid", 312.46, 961.0, 1.53),
    ("Sr", "Solid", 1050.0, 1655.0, 2.64),
    ("Y", "Solid", 1795.0, 3618.0, 4.47),
    ("Zr", "Solid", 2128.0, 4682.0, 6.52),
    ("Nb", "Solid", 2750.0, 5017.0, 8.57),
    ("Mo", "Solid", 2896.0, 4912.0, 10.2),
    ("Tc", "Solid", 2430.0, 4538.0, 11.0),
    ("Ru", "Solid", 2607.0, 4423.0, 12.1),
    ("Rh", "Solid", 2237.0, 3968.0, 12.4),
    ("Pd", "Solid", 1828.05, 3236.0, 12.0),
    ("Ag", "Solid", 1234.93, 2435.0, 10.501),
    ("Cd", "Solid", 594.22, 1040.0, 8.69),
    ("In", "Solid", 429.75, 2345.0, 7.31),
    ("Sn", "Solid", 505.08, 2875.0, 7.287),
    ("Sb", "Solid", 903.78, 1860.0, 6.685),
    ("Te", "Solid", 722.66, 1261.0, 6.232),
    ("I", "Solid", 386.85, 457.55, 4.93),
    ("Xe", "Gas", 161.36, 165.03, 0.005887),
    ("Cs", "Solid", 301.59, 944.0, 1.93),
    ("Ba", "Solid", 1000.0, 2170.0, 3.62),
    ("La", "Solid", 1191.0, 3737.0, 6.15),
    ("Ce", "Solid", 1071.0, 3697.0, 6.770),
    ("Pr", "Solid", 1204.0, 3793.0, 6.77),
    ("Nd", "Solid", 1294.0, 3347.0, 7.01),
    ("Pm", "Solid", 1315.0, 3273.0, 7.26),
    ("Sm", "Solid", 1347.0, 2067.0, 7.52),
    ("Eu", "Solid", 1095.0, 1802.0, 5.24),
    ("Gd", "Solid", 1586.0, 3546.0, 7.90),
    ("Tb", "Solid", 1629.0, 3503.0, 8.23),
    ("Dy", "Solid", 1685.0, 2840.0, 8.55),
    ("Ho", "Solid", 1747.0, 2973.0, 8.80),
    ("Er", "Solid", 1802.0, 3141.0, 9.07),
    ("Tm", "Solid", 1818.0, 2223.0, 9.32),
    ("Yb", "Solid", 1092.0, 1469.0, 6.90),
    ("Lu", "Solid", 1936.0, 3675.0, 9.84),
    ("Hf", "Solid", 2506.0, 4876.0, 13.3),
    ("Ta", "Solid", 3290.0, 5731.0, 16.4),
    ("W", "Solid", 3695.0, 5828.0, 19.3),
    ("Re", "Solid", 3459.0, 5869.0, 20.8),
    ("Os", "Solid", 3306.0, 5285.0, 22.57),
    ("Ir", "Solid", 2719.0, 4701.0, 22.42),
    ("Pt", "Solid", 2041.55, 4098.0, 21.46),
    ("Au", "Solid", 1337.33, 3129.0, 19.282),
    ("Hg", "Liquid", 234.32, 629.88, 13.5336),
    ("Tl", "Solid", 577.0, 1746.0, 11.8),
    ("Pb", "Solid", 600.61, 2022.0, 11.342),
    ("Bi", "Solid", 544.55, 1837.0, 9.807),
    ("Po", "Solid", 527.0, 1235.0, 9.32),
    ("Rn", "Gas", 202.0, 211.45, 0.00973),
    ("Ra", "Solid", 973.0, 1413.0, 5.0),
    ("Ac", "Solid", 1324.0, 3471.0, 10.07),
    ("Th", "Solid", 2023.0, 5061.0, 11.72),
    ("U", "Solid", 1408.0, 4404.0, 18.95),
    ("Np", "Solid", 917.0, 4175.0, 20.25),
    ("Pu", "Solid", 913.0, 3501.0, 19.84),
    ("Am", "Solid", 1449.0, 2284.0, 13.69),
    ("Cm", "Solid", 1618.0, 3400.0, 13.51),
)

_UNRESOLVED_PHYSICAL_PROPERTY_EVIDENCE_ROWS = (
    ("At", "Solid", 575.0, None, 7.0),
    ("Fr", "Solid", 300.0, None, None),
    ("Pa", "Solid", 1845.0, None, 15.37),
    ("Bk", "Solid", 1323.0, None, 14.0),
    ("Cf", "Solid", 1173.0, None, None),
    ("Es", "Solid", 1133.0, None, None),
    ("Fm", "Solid", 1800.0, None, None),
    ("Md", "Solid", 1100.0, None, None),
    ("No", "Solid", 1100.0, None, None),
    ("Lr", "Solid", 1900.0, None, None),
    ("Rf", "Solid", None, None, None),
    ("Db", "Solid", None, None, None),
    ("Sg", "Solid", None, None, None),
    ("Bh", "Solid", None, None, None),
    ("Hs", "Solid", None, None, None),
    ("Mt", "Solid", None, None, None),
    ("Ds", "Expected to be a Solid", None, None, None),
    ("Rg", "Expected to be a Solid", None, None, None),
    ("Cn", "Expected to be a Solid", None, None, None),
    ("Nh", "Expected to be a Solid", None, None, None),
    ("Fl", "Expected to be a Solid", None, None, None),
    ("Mc", "Expected to be a Solid", None, None, None),
    ("Lv", "Expected to be a Solid", None, None, None),
    ("Ts", "Expected to be a Solid", None, None, None),
    ("Og", "Expected to be a Gas", None, None, None),
)


def _build_isotope_evidence(row: dict) -> IsotopeEvidenceRecord:
    isotope_instance = build_isotope_instance(row["symbol"], row["mass_number"])
    return IsotopeEvidenceRecord(
        isotope_id=isotope_instance.instance_id,
        element_id=isotope_instance.element_id,
        symbol=isotope_instance.symbol,
        atomic_number=isotope_instance.atomic_number,
        mass_number=isotope_instance.mass_number,
        neutron_count=isotope_instance.neutron_count,
        relative_atomic_mass=row["relative_atomic_mass"],
        isotopic_composition=row["isotopic_composition"],
        half_life_value=row["half_life_value"],
        half_life_unit=row["half_life_unit"],
        decay_mode=row["decay_mode"],
        source_keys=row["source_keys"],
        evidence_status=row["evidence_status"],
    )


def _build_common_ion_evidence(symbol: str, charge: int) -> CommonIonEvidenceRecord:
    ion_instance = build_ion_instance(symbol, charge)
    return CommonIonEvidenceRecord(
        ion_id=ion_instance.instance_id,
        element_id=ion_instance.element_id,
        symbol=ion_instance.symbol,
        atomic_number=ion_instance.atomic_number,
        charge=ion_instance.charge,
        electron_count=ion_instance.electron_count,
        source_keys=("pubchem_periodic_table_properties",),
        evidence_basis="charge appears in the sourced PubChem oxidation-state set",
    )


def _build_physical_property_evidence(
    symbol: str,
    standard_state: str,
    melting_point_k: float,
    boiling_point_k: float,
    density_value: float,
    phase_transition_note: str | None = None,
) -> PhysicalPropertyEvidenceRecord:
    snapshot = get_snapshot_record(symbol)
    return PhysicalPropertyEvidenceRecord(
        element_id=f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}",
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        standard_state=standard_state,
        melting_point_k=melting_point_k,
        boiling_point_k=boiling_point_k,
        density_value=density_value,
        density_unit="g/cm^3",
        source_keys=("pubchem_periodic_table_properties",),
        phase_transition_note=phase_transition_note,
    )


def _build_unresolved_physical_property_evidence(
    symbol: str,
    standard_state: str,
    melting_point_k: float | None,
    boiling_point_k: float | None,
    density_value: float | None,
) -> UnresolvedPhysicalPropertyEvidenceRecord:
    snapshot = get_snapshot_record(symbol)
    missing_fields = tuple(
        field
        for field, value in (
            ("melting_point_k", melting_point_k),
            ("boiling_point_k", boiling_point_k),
            ("density_value", density_value),
        )
        if value is None
    )
    return UnresolvedPhysicalPropertyEvidenceRecord(
        element_id=f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}",
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        standard_state=standard_state,
        melting_point_k=melting_point_k,
        boiling_point_k=boiling_point_k,
        density_value=density_value,
        missing_fields=missing_fields,
        source_keys=("pubchem_periodic_table_properties",),
    )


def list_isotope_evidence_records() -> tuple[IsotopeEvidenceRecord, ...]:
    return tuple(
        _build_isotope_evidence(row)
        for row in (_ISOTOPE_EVIDENCE_ROWS + _SC_ZN_ISOTOPE_EVIDENCE_ROWS)
    )


def list_common_ion_evidence_records() -> tuple[CommonIonEvidenceRecord, ...]:
    return tuple(
        _build_common_ion_evidence(symbol, charge)
        for symbol, charge in _COMMON_ION_EVIDENCE_ROWS
    )


def list_physical_property_evidence_records() -> tuple[PhysicalPropertyEvidenceRecord, ...]:
    return tuple(
        _build_physical_property_evidence(*row)
        for row in _PHYSICAL_PROPERTY_EVIDENCE_ROWS
    )


def list_unresolved_physical_property_evidence_records() -> tuple[
    UnresolvedPhysicalPropertyEvidenceRecord, ...
]:
    return tuple(
        _build_unresolved_physical_property_evidence(*row)
        for row in _UNRESOLVED_PHYSICAL_PROPERTY_EVIDENCE_ROWS
    )


def _build_unresolved_evidence_record(
    symbol: str,
    evidence_domain: str,
    missing_evidence: tuple[str, ...],
    source_boundary: str,
) -> UnresolvedEvidenceRecord:
    snapshot = get_snapshot_record(symbol)
    element_id = f"MSPEE-Z{snapshot.atomic_number:03d}-{snapshot.symbol}"
    return UnresolvedEvidenceRecord(
        receipt_id=f"{element_id}-{evidence_domain}-unresolved",
        element_id=element_id,
        symbol=snapshot.symbol,
        atomic_number=snapshot.atomic_number,
        evidence_domain=evidence_domain,
        missing_evidence=missing_evidence,
        source_boundary=source_boundary,
    )


def list_unresolved_isotope_evidence_records() -> tuple[UnresolvedEvidenceRecord, ...]:
    resolved_symbols = {record.symbol for record in list_isotope_evidence_records()}
    return tuple(
        _build_unresolved_evidence_record(
            record.symbol,
            "isotope_evidence",
            (
                "stable_isotope_list",
                "radioisotope_list",
                "natural_abundance",
                "half_life_or_stability_status",
                "decay_mode_when_radioactive",
            ),
            "full isotope evidence has not yet been sourced for this element",
        )
        for record in get_all_snapshot_records_for_unresolved_evidence()
        if record.symbol not in resolved_symbols
    )


def list_unresolved_common_ion_evidence_records() -> tuple[UnresolvedEvidenceRecord, ...]:
    resolved_symbols = {record.symbol for record in list_common_ion_evidence_records()}
    return tuple(
        _build_unresolved_evidence_record(
            element.identity.symbol,
            "common_ion_evidence",
            (
                "common_ion_charge_set",
                "source_citation_for_common_ion_status",
                "stability_boundary",
            ),
            "common-ion evidence has not yet been sourced for this Level 1 element",
        )
        for element in get_all_seed_elements_for_unresolved_evidence()
        if element.identity.symbol not in resolved_symbols
    )


def get_all_snapshot_records_for_unresolved_evidence():
    from mcms.elements.snapshot import list_full_snapshot_records

    return list_full_snapshot_records()


def get_all_seed_elements_for_unresolved_evidence():
    from mcms.elements.seed import list_seed_elements

    return list_seed_elements()


def find_isotope_evidence_records(
    identifier: str | int,
    mass_number: int | None = None,
) -> tuple[IsotopeEvidenceRecord, ...]:
    identifier_text = str(identifier).strip()
    matches = tuple(
        record
        for record in list_isotope_evidence_records()
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.isotope_id
        )
        and (mass_number is None or record.mass_number == mass_number)
    )
    if not matches:
        raise KeyError(f"unknown isotope evidence record: {identifier_text}")
    return matches


def find_common_ion_evidence_records(identifier: str | int) -> tuple[CommonIonEvidenceRecord, ...]:
    identifier_text = str(identifier).strip()
    matches = tuple(
        record
        for record in list_common_ion_evidence_records()
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.ion_id
        )
    )
    if not matches:
        raise KeyError(f"unknown common-ion evidence record: {identifier_text}")
    return matches


def find_physical_property_evidence_record(identifier: str | int) -> PhysicalPropertyEvidenceRecord:
    identifier_text = str(identifier).strip()
    for record in list_physical_property_evidence_records():
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.element_id
        ):
            return record
    raise KeyError(f"unknown physical-property evidence record: {identifier_text}")


def find_unresolved_physical_property_evidence_record(
    identifier: str | int,
) -> UnresolvedPhysicalPropertyEvidenceRecord:
    identifier_text = str(identifier).strip()
    for record in list_unresolved_physical_property_evidence_records():
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.element_id
        ):
            return record
    raise KeyError(f"unknown unresolved physical-property evidence record: {identifier_text}")


def find_unresolved_isotope_evidence_record(identifier: str | int) -> UnresolvedEvidenceRecord:
    identifier_text = str(identifier).strip()
    for record in list_unresolved_isotope_evidence_records():
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.element_id
            or identifier_text == record.receipt_id
        ):
            return record
    raise KeyError(f"unknown unresolved isotope evidence record: {identifier_text}")


def find_unresolved_common_ion_evidence_record(identifier: str | int) -> UnresolvedEvidenceRecord:
    identifier_text = str(identifier).strip()
    for record in list_unresolved_common_ion_evidence_records():
        if (
            identifier_text == str(record.atomic_number)
            or identifier_text.upper() == record.symbol.upper()
            or identifier_text == record.element_id
            or identifier_text == record.receipt_id
        ):
            return record
    raise KeyError(f"unknown unresolved common-ion evidence record: {identifier_text}")


def validate_isotope_evidence_records(
    records: tuple[IsotopeEvidenceRecord, ...] | None = None,
) -> dict:
    checked_records = records if records is not None else list_isotope_evidence_records()
    invalid_records = tuple(record.isotope_id for record in checked_records if record.validate())
    return {
        "validation_status": (
            "isotope_evidence_records_validated"
            if not invalid_records
            else "isotope_evidence_records_rejected"
        ),
        "record_count": len(checked_records),
        "radioisotope_count": sum(
            1 for record in checked_records if record.evidence_status == "radioisotope_evidence"
        ),
        "invalid_records": invalid_records,
        "source_keys": tuple(
            sorted({source_key for record in checked_records for source_key in record.source_keys})
        ),
    }


def validate_common_ion_evidence_records(
    records: tuple[CommonIonEvidenceRecord, ...] | None = None,
) -> dict:
    checked_records = records if records is not None else list_common_ion_evidence_records()
    invalid_records = tuple(record.ion_id for record in checked_records if record.validate())
    return {
        "validation_status": (
            "common_ion_evidence_records_validated"
            if not invalid_records
            else "common_ion_evidence_records_rejected"
        ),
        "record_count": len(checked_records),
        "invalid_records": invalid_records,
        "source_keys": tuple(
            sorted({source_key for record in checked_records for source_key in record.source_keys})
        ),
    }


def validate_physical_property_evidence_records(
    records: tuple[PhysicalPropertyEvidenceRecord, ...] | None = None,
) -> dict:
    checked_records = (
        records if records is not None else list_physical_property_evidence_records()
    )
    invalid_records = tuple(
        record.element_id for record in checked_records if record.validate()
    )
    return {
        "validation_status": (
            "physical_property_evidence_records_validated"
            if not invalid_records
            else "physical_property_evidence_records_rejected"
        ),
        "record_count": len(checked_records),
        "standard_states": tuple(
            sorted({record.standard_state for record in checked_records})
        ),
        "invalid_records": invalid_records,
        "source_keys": tuple(
            sorted({source_key for record in checked_records for source_key in record.source_keys})
        ),
    }


def validate_unresolved_physical_property_evidence_records(
    records: tuple[UnresolvedPhysicalPropertyEvidenceRecord, ...] | None = None,
) -> dict:
    checked_records = (
        records
        if records is not None
        else list_unresolved_physical_property_evidence_records()
    )
    invalid_records = tuple(
        record.element_id for record in checked_records if record.validate()
    )
    return {
        "validation_status": (
            "unresolved_physical_property_evidence_records_validated"
            if not invalid_records
            else "unresolved_physical_property_evidence_records_rejected"
        ),
        "record_count": len(checked_records),
        "missing_field_counts": {
            "melting_point_k": sum(
                1 for record in checked_records if "melting_point_k" in record.missing_fields
            ),
            "boiling_point_k": sum(
                1 for record in checked_records if "boiling_point_k" in record.missing_fields
            ),
            "density_value": sum(
                1 for record in checked_records if "density_value" in record.missing_fields
            ),
        },
        "invalid_records": invalid_records,
        "source_keys": tuple(
            sorted({source_key for record in checked_records for source_key in record.source_keys})
        ),
    }


def validate_unresolved_evidence_records(
    records: tuple[UnresolvedEvidenceRecord, ...],
    *,
    expected_domain: str,
) -> dict:
    invalid_records = tuple(record.receipt_id for record in records if record.validate())
    wrong_domain_records = tuple(
        record.receipt_id for record in records if record.evidence_domain != expected_domain
    )
    return {
        "validation_status": (
            f"{expected_domain}_unresolved_records_validated"
            if not invalid_records and not wrong_domain_records
            else f"{expected_domain}_unresolved_records_rejected"
        ),
        "record_count": len(records),
        "invalid_records": invalid_records,
        "wrong_domain_records": wrong_domain_records,
        "source_boundaries": tuple(sorted({record.source_boundary for record in records})),
    }
