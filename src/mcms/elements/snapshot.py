"""Purpose: full 118-element MSPEE identity source snapshot.

Governance scope: records canonical element identity, periodic position, and CIAAW
standard atomic-weight display for all 118 elements without claiming full Level 1
electron-state validation for elements outside the seed pack.
Dependencies: MSPEE model primitives, hashlib, and JSON canonicalization.
Invariants: snapshot has exactly Z=1..118 in order; unavailable weights are explicit;
deeper symbolic state must be supplied by a validated seed record.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from hashlib import sha256

from mcms.elements.model import AtomicWeightModel, SourceReference

SNAPSHOT_SOURCE_REFERENCES = (
    SourceReference(
        key="ciaaw_standard_atomic_weights_2024",
        authority="CIAAW/IUPAC",
        title="Standard Atomic Weights 2024",
        url="https://www.ciaaw.org/atomic-weights.htm",
        version="2024",
    ),
    SourceReference(
        key="iupac_periodic_table_elements",
        authority="IUPAC",
        title="Periodic Table of Elements",
        url="https://iupac.org/what-we-do/periodic-table-of-elements/",
        version="current source page observed 2026-06-28",
    ),
)

SNAPSHOT_SOURCE_KEYS = tuple(source.key for source in SNAPSHOT_SOURCE_REFERENCES)

VALID_SNAPSHOT_BLOCKS = {"s", "p", "d", "f"}
VALID_SNAPSHOT_STATUSES = {"identity_snapshot", "level_1_seed_available"}


@dataclass(frozen=True)
class ElementSourceSnapshotRecord:
    atomic_number: int
    symbol: str
    name: str
    period: int
    group: int | None
    block: str
    atomic_weight_model: AtomicWeightModel
    source_keys: tuple[str, ...]
    snapshot_status: str
    level_1_seed_available: bool
    notes: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.atomic_number < 1 or self.atomic_number > 118:
            errors.append("atomic number must be in [1, 118].")
        if not self.symbol:
            errors.append("symbol is required.")
        if not self.name:
            errors.append("name is required.")
        if self.period < 1 or self.period > 7:
            errors.append("period must be in [1, 7].")
        if self.group is not None and (self.group < 1 or self.group > 18):
            errors.append("group must be None or in [1, 18].")
        if self.block not in VALID_SNAPSHOT_BLOCKS:
            errors.append("block must be one of s, p, d, f.")
        if self.snapshot_status not in VALID_SNAPSHOT_STATUSES:
            errors.append("snapshot status is unknown.")
        if "ciaaw_standard_atomic_weights_2024" not in self.source_keys:
            errors.append("CIAAW source key is required.")
        if "iupac_periodic_table_elements" not in self.source_keys:
            errors.append("IUPAC periodic-table source key is required.")
        errors.extend(self.atomic_weight_model.validate())
        return errors

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ElementSnapshotValidationResult:
    element_count: int
    unavailable_weight_count: int
    level_1_seed_count: int
    invalid_elements: tuple[str, ...]
    source_keys: tuple[str, ...]
    validation_status: str

    def to_dict(self) -> dict:
        return asdict(self)


_CIAAW_SNAPSHOT_ROWS: tuple[tuple[int, str, str, str, str], ...] = (
    (1, "H", "Hydrogen", "[1.00784,1.00811]", "m"),
    (2, "He", "Helium", "4.002602(2)", "g r"),
    (3, "Li", "Lithium", "[6.938,6.997]", "m"),
    (4, "Be", "Beryllium", "9.0121831(5)", ""),
    (5, "B", "Boron", "[10.806,10.821]", "m"),
    (6, "C", "Carbon", "[12.0096,12.0116]", ""),
    (7, "N", "Nitrogen", "[14.00643,14.00728]", "m"),
    (8, "O", "Oxygen", "[15.99903,15.99977]", "m"),
    (9, "F", "Fluorine", "18.998403162(5)", ""),
    (10, "Ne", "Neon", "20.1797(6)", "g m"),
    (11, "Na", "Sodium", "22.98976928(2)", ""),
    (12, "Mg", "Magnesium", "[24.304,24.307]", ""),
    (13, "Al", "Aluminium", "26.9815384(3)", ""),
    (14, "Si", "Silicon", "[28.084,28.086]", ""),
    (15, "P", "Phosphorus", "30.973761998(5)", ""),
    (16, "S", "Sulfur", "[32.059,32.076]", ""),
    (17, "Cl", "Chlorine", "[35.446,35.457]", "m"),
    (18, "Ar", "Argon", "[39.792,39.963]", ""),
    (19, "K", "Potassium", "39.0983(1)", ""),
    (20, "Ca", "Calcium", "40.078(4)", "g"),
    (21, "Sc", "Scandium", "44.955907(4)", ""),
    (22, "Ti", "Titanium", "47.867(1)", ""),
    (23, "V", "Vanadium", "50.9415(1)", ""),
    (24, "Cr", "Chromium", "51.9961(6)", ""),
    (25, "Mn", "Manganese", "54.938043(2)", ""),
    (26, "Fe", "Iron", "55.845(2)", ""),
    (27, "Co", "Cobalt", "58.933194(3)", ""),
    (28, "Ni", "Nickel", "58.6934(4)", "r"),
    (29, "Cu", "Copper", "63.546(3)", "r"),
    (30, "Zn", "Zinc", "65.38(2)", "r"),
    (31, "Ga", "Gallium", "69.723(1)", ""),
    (32, "Ge", "Germanium", "72.630(8)", ""),
    (33, "As", "Arsenic", "74.921595(6)", ""),
    (34, "Se", "Selenium", "78.971(8)", "r"),
    (35, "Br", "Bromine", "[79.901,79.907]", ""),
    (36, "Kr", "Krypton", "83.798(2)", "g m"),
    (37, "Rb", "Rubidium", "85.4678(3)", "g"),
    (38, "Sr", "Strontium", "87.62(1)", "g r"),
    (39, "Y", "Yttrium", "88.905838(2)", ""),
    (40, "Zr", "Zirconium", "91.222(3)", "g"),
    (41, "Nb", "Niobium", "92.90637(1)", ""),
    (42, "Mo", "Molybdenum", "95.95(1)", "g"),
    (43, "Tc", "Technetium", "unavailable", ""),
    (44, "Ru", "Ruthenium", "101.07(2)", "g"),
    (45, "Rh", "Rhodium", "102.90549(2)", ""),
    (46, "Pd", "Palladium", "106.42(1)", "g"),
    (47, "Ag", "Silver", "107.8682(2)", "g"),
    (48, "Cd", "Cadmium", "112.414(4)", "g"),
    (49, "In", "Indium", "114.818(1)", ""),
    (50, "Sn", "Tin", "118.710(7)", "g"),
    (51, "Sb", "Antimony", "121.760(1)", "g"),
    (52, "Te", "Tellurium", "127.60(3)", "g"),
    (53, "I", "Iodine", "126.90447(3)", ""),
    (54, "Xe", "Xenon", "131.293(6)", "g m"),
    (55, "Cs", "Caesium", "132.90545196(6)", ""),
    (56, "Ba", "Barium", "137.327(7)", ""),
    (57, "La", "Lanthanum", "138.90547(7)", "g"),
    (58, "Ce", "Cerium", "140.116(1)", "g"),
    (59, "Pr", "Praseodymium", "140.90766(1)", ""),
    (60, "Nd", "Neodymium", "144.242(3)", "g"),
    (61, "Pm", "Promethium", "unavailable", ""),
    (62, "Sm", "Samarium", "150.36(2)", "g"),
    (63, "Eu", "Europium", "151.964(1)", "g"),
    (64, "Gd", "Gadolinium", "157.249(2)", "g"),
    (65, "Tb", "Terbium", "158.925354(7)", ""),
    (66, "Dy", "Dysprosium", "162.500(1)", "g"),
    (67, "Ho", "Holmium", "164.930329(5)", ""),
    (68, "Er", "Erbium", "167.259(3)", "g"),
    (69, "Tm", "Thulium", "168.934219(5)", ""),
    (70, "Yb", "Ytterbium", "173.045(10)", "g"),
    (71, "Lu", "Lutetium", "174.96669(5)", "g"),
    (72, "Hf", "Hafnium", "178.486(6)", "g"),
    (73, "Ta", "Tantalum", "180.94788(2)", ""),
    (74, "W", "Tungsten", "183.84(1)", ""),
    (75, "Re", "Rhenium", "186.207(1)", ""),
    (76, "Os", "Osmium", "190.23(3)", "g"),
    (77, "Ir", "Iridium", "192.217(2)", ""),
    (78, "Pt", "Platinum", "195.084(9)", ""),
    (79, "Au", "Gold", "196.966570(4)", ""),
    (80, "Hg", "Mercury", "200.592(3)", ""),
    (81, "Tl", "Thallium", "[204.382,204.385]", ""),
    (82, "Pb", "Lead", "[206.14,207.94]", ""),
    (83, "Bi", "Bismuth", "208.98040(1)", ""),
    (84, "Po", "Polonium", "unavailable", ""),
    (85, "At", "Astatine", "unavailable", ""),
    (86, "Rn", "Radon", "unavailable", ""),
    (87, "Fr", "Francium", "unavailable", ""),
    (88, "Ra", "Radium", "unavailable", ""),
    (89, "Ac", "Actinium", "unavailable", ""),
    (90, "Th", "Thorium", "232.0377(4)", "g"),
    (91, "Pa", "Protactinium", "231.03588(1)", ""),
    (92, "U", "Uranium", "238.02891(3)", "g m"),
    (93, "Np", "Neptunium", "unavailable", ""),
    (94, "Pu", "Plutonium", "unavailable", ""),
    (95, "Am", "Americium", "unavailable", ""),
    (96, "Cm", "Curium", "unavailable", ""),
    (97, "Bk", "Berkelium", "unavailable", ""),
    (98, "Cf", "Californium", "unavailable", ""),
    (99, "Es", "Einsteinium", "unavailable", ""),
    (100, "Fm", "Fermium", "unavailable", ""),
    (101, "Md", "Mendelevium", "unavailable", ""),
    (102, "No", "Nobelium", "unavailable", ""),
    (103, "Lr", "Lawrencium", "unavailable", ""),
    (104, "Rf", "Rutherfordium", "unavailable", ""),
    (105, "Db", "Dubnium", "unavailable", ""),
    (106, "Sg", "Seaborgium", "unavailable", ""),
    (107, "Bh", "Bohrium", "unavailable", ""),
    (108, "Hs", "Hassium", "unavailable", ""),
    (109, "Mt", "Meitnerium", "unavailable", ""),
    (110, "Ds", "Darmstadtium", "unavailable", ""),
    (111, "Rg", "Roentgenium", "unavailable", ""),
    (112, "Cn", "Copernicium", "unavailable", ""),
    (113, "Nh", "Nihonium", "unavailable", ""),
    (114, "Fl", "Flerovium", "unavailable", ""),
    (115, "Mc", "Moscovium", "unavailable", ""),
    (116, "Lv", "Livermorium", "unavailable", ""),
    (117, "Ts", "Tennessine", "unavailable", ""),
    (118, "Og", "Oganesson", "unavailable", ""),
)

_POSITION_BY_SYMBOL: dict[str, tuple[int, int | None, str]] = {
    "H": (1, 1, "s"),
    "He": (1, 18, "s"),
    "Li": (2, 1, "s"),
    "Be": (2, 2, "s"),
    "B": (2, 13, "p"),
    "C": (2, 14, "p"),
    "N": (2, 15, "p"),
    "O": (2, 16, "p"),
    "F": (2, 17, "p"),
    "Ne": (2, 18, "p"),
    "Na": (3, 1, "s"),
    "Mg": (3, 2, "s"),
    "Al": (3, 13, "p"),
    "Si": (3, 14, "p"),
    "P": (3, 15, "p"),
    "S": (3, 16, "p"),
    "Cl": (3, 17, "p"),
    "Ar": (3, 18, "p"),
    "K": (4, 1, "s"),
    "Ca": (4, 2, "s"),
    "Sc": (4, 3, "d"),
    "Ti": (4, 4, "d"),
    "V": (4, 5, "d"),
    "Cr": (4, 6, "d"),
    "Mn": (4, 7, "d"),
    "Fe": (4, 8, "d"),
    "Co": (4, 9, "d"),
    "Ni": (4, 10, "d"),
    "Cu": (4, 11, "d"),
    "Zn": (4, 12, "d"),
    "Ga": (4, 13, "p"),
    "Ge": (4, 14, "p"),
    "As": (4, 15, "p"),
    "Se": (4, 16, "p"),
    "Br": (4, 17, "p"),
    "Kr": (4, 18, "p"),
    "Rb": (5, 1, "s"),
    "Sr": (5, 2, "s"),
    "Y": (5, 3, "d"),
    "Zr": (5, 4, "d"),
    "Nb": (5, 5, "d"),
    "Mo": (5, 6, "d"),
    "Tc": (5, 7, "d"),
    "Ru": (5, 8, "d"),
    "Rh": (5, 9, "d"),
    "Pd": (5, 10, "d"),
    "Ag": (5, 11, "d"),
    "Cd": (5, 12, "d"),
    "In": (5, 13, "p"),
    "Sn": (5, 14, "p"),
    "Sb": (5, 15, "p"),
    "Te": (5, 16, "p"),
    "I": (5, 17, "p"),
    "Xe": (5, 18, "p"),
    "Cs": (6, 1, "s"),
    "Ba": (6, 2, "s"),
    "La": (6, None, "f"),
    "Ce": (6, None, "f"),
    "Pr": (6, None, "f"),
    "Nd": (6, None, "f"),
    "Pm": (6, None, "f"),
    "Sm": (6, None, "f"),
    "Eu": (6, None, "f"),
    "Gd": (6, None, "f"),
    "Tb": (6, None, "f"),
    "Dy": (6, None, "f"),
    "Ho": (6, None, "f"),
    "Er": (6, None, "f"),
    "Tm": (6, None, "f"),
    "Yb": (6, None, "f"),
    "Lu": (6, None, "f"),
    "Hf": (6, 4, "d"),
    "Ta": (6, 5, "d"),
    "W": (6, 6, "d"),
    "Re": (6, 7, "d"),
    "Os": (6, 8, "d"),
    "Ir": (6, 9, "d"),
    "Pt": (6, 10, "d"),
    "Au": (6, 11, "d"),
    "Hg": (6, 12, "d"),
    "Tl": (6, 13, "p"),
    "Pb": (6, 14, "p"),
    "Bi": (6, 15, "p"),
    "Po": (6, 16, "p"),
    "At": (6, 17, "p"),
    "Rn": (6, 18, "p"),
    "Fr": (7, 1, "s"),
    "Ra": (7, 2, "s"),
    "Ac": (7, None, "f"),
    "Th": (7, None, "f"),
    "Pa": (7, None, "f"),
    "U": (7, None, "f"),
    "Np": (7, None, "f"),
    "Pu": (7, None, "f"),
    "Am": (7, None, "f"),
    "Cm": (7, None, "f"),
    "Bk": (7, None, "f"),
    "Cf": (7, None, "f"),
    "Es": (7, None, "f"),
    "Fm": (7, None, "f"),
    "Md": (7, None, "f"),
    "No": (7, None, "f"),
    "Lr": (7, None, "f"),
    "Rf": (7, 4, "d"),
    "Db": (7, 5, "d"),
    "Sg": (7, 6, "d"),
    "Bh": (7, 7, "d"),
    "Hs": (7, 8, "d"),
    "Mt": (7, 9, "d"),
    "Ds": (7, 10, "d"),
    "Rg": (7, 11, "d"),
    "Cn": (7, 12, "d"),
    "Nh": (7, 13, "p"),
    "Fl": (7, 14, "p"),
    "Mc": (7, 15, "p"),
    "Lv": (7, 16, "p"),
    "Ts": (7, 17, "p"),
    "Og": (7, 18, "p"),
}

_LEVEL_1_SEED_SYMBOLS = {
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
}


def _weight_model_from_display(display: str, notes: str) -> AtomicWeightModel:
    if display == "unavailable":
        return AtomicWeightModel(
            model_type="unavailable",
            display="unavailable",
            notes=("CIAAW does not provide a standard atomic weight for this element.",),
        )
    if display.startswith("[") and display.endswith("]"):
        lower_bound, upper_bound = display.strip("[]").split(",", maxsplit=1)
        return AtomicWeightModel(
            model_type="interval",
            display=display,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            notes=tuple(note for note in ("CIAAW interval value", notes) if note),
        )
    return AtomicWeightModel(
        model_type="single",
        display=display,
        notes=tuple(note for note in ("CIAAW single value", notes) if note),
    )


@lru_cache(maxsize=1)
def list_full_snapshot_records() -> tuple[ElementSourceSnapshotRecord, ...]:
    records: list[ElementSourceSnapshotRecord] = []
    for atomic_number, symbol, name, weight_display, notes in _CIAAW_SNAPSHOT_ROWS:
        period, group, block = _POSITION_BY_SYMBOL[symbol]
        level_1_seed_available = symbol in _LEVEL_1_SEED_SYMBOLS
        records.append(
            ElementSourceSnapshotRecord(
                atomic_number=atomic_number,
                symbol=symbol,
                name=name,
                period=period,
                group=group,
                block=block,
                atomic_weight_model=_weight_model_from_display(weight_display, notes),
                source_keys=SNAPSHOT_SOURCE_KEYS,
                snapshot_status=(
                    "level_1_seed_available"
                    if level_1_seed_available
                    else "identity_snapshot"
                ),
                level_1_seed_available=level_1_seed_available,
                notes=(
                    (
                        "Lanthanide and actinide rows use group=None to avoid forcing a "
                        "disputed group assignment.",
                    )
                    if group is None
                    else ()
                ),
            )
        )
    return tuple(records)


def get_snapshot_record(identifier: str | int) -> ElementSourceSnapshotRecord:
    identifier_text = str(identifier).strip()
    if not identifier_text:
        raise KeyError("element identifier is required")
    for record in list_full_snapshot_records():
        if identifier_text == str(record.atomic_number):
            return record
        if identifier_text.upper() == record.symbol.upper():
            return record
        if identifier_text.lower() == record.name.lower():
            return record
    raise KeyError(f"unknown MSPEE snapshot element: {identifier_text}")


def validate_full_snapshot(
    records: tuple[ElementSourceSnapshotRecord, ...] | None = None,
) -> ElementSnapshotValidationResult:
    checked_records = records if records is not None else list_full_snapshot_records()
    invalid_elements = tuple(
        f"Z{record.atomic_number:03d}-{record.symbol}"
        for record in checked_records
        if record.validate()
    )
    observed_atomic_numbers = tuple(record.atomic_number for record in checked_records)
    source_keys = tuple(
        sorted({source_key for record in checked_records for source_key in record.source_keys})
    )
    validation_status = "full_element_snapshot_validated"
    if invalid_elements or observed_atomic_numbers != tuple(range(1, 119)):
        validation_status = "full_element_snapshot_rejected"
    return ElementSnapshotValidationResult(
        element_count=len(checked_records),
        unavailable_weight_count=sum(
            1
            for record in checked_records
            if record.atomic_weight_model.model_type == "unavailable"
        ),
        level_1_seed_count=sum(1 for record in checked_records if record.level_1_seed_available),
        invalid_elements=invalid_elements,
        source_keys=source_keys,
        validation_status=validation_status,
    )


def build_snapshot_receipt(record: ElementSourceSnapshotRecord) -> dict:
    record_payload = record.to_dict()
    canonical = json.dumps(record_payload, sort_keys=True, separators=(",", ":"))
    validation_errors = record.validate()
    return {
        "snapshot_id": f"MSPEE-SNAPSHOT-Z{record.atomic_number:03d}-{record.symbol}",
        "symbol": record.symbol,
        "validation_status": (
            "element_snapshot_validated" if not validation_errors else "element_snapshot_rejected"
        ),
        "validation_errors": validation_errors,
        "source_keys": record.source_keys,
        "snapshot_hash": sha256(canonical.encode("utf-8")).hexdigest(),
    }
