"""Purpose: record investigation work for physical-property escalations.

Project scope: captures checked sources for blocked escalation receipts before
any value is admitted or rejected.
Dependencies: physical-property escalation receipts.
Invariants: escalation-search receipts do not close gaps or mutate seed records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_escalation import (
    get_physical_property_escalation_receipt,
)

VALID_ESCALATION_SEARCH_STATUSES = {
    "higher_precedence_source_not_found",
    "higher_precedence_source_found_pending_resolution",
    "corroborating_source_not_found",
    "operator_decision_pending",
}


@dataclass(frozen=True)
class PhysicalPropertyEscalationSourceCheck:
    source_key: str
    source_authority: str
    source_url: str
    checked_field: str
    observed_value: str | None
    observed_unit: str | None
    source_result: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.source_key:
            errors.append("escalation source check requires source key.")
        if not self.source_authority:
            errors.append("escalation source check requires source authority.")
        if not self.source_url:
            errors.append("escalation source check requires source URL.")
        if not self.checked_field:
            errors.append("escalation source check requires checked field.")
        if not self.source_result:
            errors.append("escalation source check requires source result.")
        if self.observed_value and not self.observed_unit:
            errors.append("observed source value requires observed unit.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PhysicalPropertyEscalationSearchReceipt:
    search_id: str
    target_escalation_receipt_id: str
    symbol: str
    atomic_number: int
    field_name: str
    search_status: str
    source_checks: tuple[PhysicalPropertyEscalationSourceCheck, ...]
    conclusion: str
    required_next_action: str
    closes_gap: bool = False
    seed_mutation_allowed: bool = False
    evidence_status: str = "physical_property_escalation_search_receipt"
    notes: tuple[str, ...] = (
        "Escalation-search receipts document source investigation only.",
        "A search receipt cannot resolve a conflict or mutate seed evidence.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        escalation = get_physical_property_escalation_receipt(
            self.target_escalation_receipt_id
        )
        if self.symbol != escalation.symbol:
            errors.append("escalation search symbol must match target escalation.")
        if self.atomic_number != escalation.atomic_number:
            errors.append("escalation search atomic number must match target escalation.")
        if self.field_name != escalation.field_name:
            errors.append("escalation search field must match target escalation.")
        if self.search_status not in VALID_ESCALATION_SEARCH_STATUSES:
            errors.append("escalation search status is unknown.")
        if not self.source_checks:
            errors.append("escalation search requires source checks.")
        if not self.conclusion:
            errors.append("escalation search requires conclusion.")
        if not self.required_next_action:
            errors.append("escalation search requires next action.")
        if self.closes_gap:
            errors.append("escalation search must not close a gap.")
        if self.seed_mutation_allowed:
            errors.append("escalation search must not allow seed mutation.")
        if escalation.escalation_class == "higher_precedence_source_required":
            if self.search_status not in {
                "higher_precedence_source_not_found",
                "higher_precedence_source_found_pending_resolution",
            }:
                errors.append("higher-precedence escalation has incompatible search status.")
        errors.extend(
            error for source_check in self.source_checks for error in source_check.validate()
        )
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_checks"] = [
            source_check.to_dict() for source_check in self.source_checks
        ]
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_escalation_search_receipts() -> tuple[
    PhysicalPropertyEscalationSearchReceipt, ...
]:
    astatine_escalation = get_physical_property_escalation_receipt("At")
    francium_escalation = get_physical_property_escalation_receipt("Fr")
    francium_density_escalation = get_physical_property_escalation_receipt(
        "MSPEE-PHYSICAL-PROPERTY-ESCALATION-Z087-Fr-density_value"
    )
    berkelium_escalation = get_physical_property_escalation_receipt("Bk")
    californium_escalation = get_physical_property_escalation_receipt("Cf")
    einsteinium_escalation = get_physical_property_escalation_receipt("Es")
    protactinium_escalation = get_physical_property_escalation_receipt("Pa")
    return (
        PhysicalPropertyEscalationSearchReceipt(
            search_id="MSPEE-PHYSICAL-PROPERTY-ESCALATION-SEARCH-Z085-At-boiling_point_k",
            target_escalation_receipt_id=astatine_escalation.receipt_id,
            symbol=astatine_escalation.symbol,
            atomic_number=astatine_escalation.atomic_number,
            field_name=astatine_escalation.field_name,
            search_status="higher_precedence_source_not_found",
            source_checks=(
                PhysicalPropertyEscalationSourceCheck(
                    source_key="nist_chemistry_webbook_atomic_astatine",
                    source_authority="NIST Chemistry WebBook SRD 69",
                    source_url="https://webbook.nist.gov/cgi/inchi/InChI%3D1S/At",
                    checked_field="boiling_point_k",
                    observed_value=None,
                    observed_unit=None,
                    source_result="atomic At page lacks a normal boiling-point field",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="pubchem_element_astatine",
                    source_authority="PubChem",
                    source_url="https://pubchem.ncbi.nlm.nih.gov/element/Astatine",
                    checked_field="boiling_point_k",
                    observed_value="337",
                    observed_unit="degC",
                    source_result="secondary value matches LANL candidate cluster",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="rsc_periodic_table_astatine",
                    source_authority="Royal Society of Chemistry",
                    source_url="https://periodic-table.rsc.org/element/85/astatine",
                    checked_field="boiling_point_k",
                    observed_value="350",
                    observed_unit="degC",
                    source_result="secondary value conflicts with PubChem/LANL cluster",
                ),
            ),
            conclusion=(
                "No higher-precedence field-specific boiling-point source was found; "
                "At remains blocked by conflicting secondary values."
            ),
            required_next_action=(
                "locate a higher-precedence field-specific source, or create an "
                "operator-approved conflict-resolution receipt before any gap closure"
            ),
        ),
        PhysicalPropertyEscalationSearchReceipt(
            search_id="MSPEE-PHYSICAL-PROPERTY-ESCALATION-SEARCH-Z087-Fr-boiling_point_k",
            target_escalation_receipt_id=francium_escalation.receipt_id,
            symbol=francium_escalation.symbol,
            atomic_number=francium_escalation.atomic_number,
            field_name=francium_escalation.field_name,
            search_status="higher_precedence_source_not_found",
            source_checks=(
                PhysicalPropertyEscalationSourceCheck(
                    source_key="nist_chemistry_webbook_atomic_francium",
                    source_authority="NIST Chemistry WebBook SRD 69",
                    source_url="https://webbook.nist.gov/cgi/cbook.cgi?ID=C7440735&Units=SI",
                    checked_field="boiling_point_k",
                    observed_value=None,
                    observed_unit=None,
                    source_result="atomic Fr page lacks a normal boiling-point field",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="pubchem_element_francium",
                    source_authority="PubChem",
                    source_url="https://pubchem.ncbi.nlm.nih.gov/element/Francium",
                    checked_field="boiling_point_k",
                    observed_value="680",
                    observed_unit="degC",
                    source_result="secondary value matches LANL candidate cluster",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="rsc_periodic_table_francium",
                    source_authority="Royal Society of Chemistry",
                    source_url="https://periodic-table.rsc.org/element/87/francium",
                    checked_field="boiling_point_k",
                    observed_value="650",
                    observed_unit="degC",
                    source_result="secondary value conflicts with PubChem/LANL cluster",
                ),
            ),
            conclusion=(
                "No higher-precedence field-specific boiling-point source was found; "
                "Fr remains blocked by conflicting secondary values."
            ),
            required_next_action=(
                "locate a higher-precedence field-specific source, or create an "
                "operator-approved conflict-resolution receipt before any gap closure"
            ),
        ),
        PhysicalPropertyEscalationSearchReceipt(
            search_id="MSPEE-PHYSICAL-PROPERTY-ESCALATION-SEARCH-Z091-Pa-boiling_point_k",
            target_escalation_receipt_id=protactinium_escalation.receipt_id,
            symbol=protactinium_escalation.symbol,
            atomic_number=protactinium_escalation.atomic_number,
            field_name=protactinium_escalation.field_name,
            search_status="higher_precedence_source_not_found",
            source_checks=(
                PhysicalPropertyEscalationSourceCheck(
                    source_key="nist_chemistry_webbook_atomic_protactinium",
                    source_authority="NIST Chemistry WebBook SRD 69",
                    source_url="https://webbook.nist.gov/cgi/inchi/InChI%3D1S/Pa",
                    checked_field="boiling_point_k",
                    observed_value=None,
                    observed_unit=None,
                    source_result="atomic Pa page lacks a normal boiling-point field",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="pubchem_element_protactinium",
                    source_authority="PubChem",
                    source_url="https://pubchem.ncbi.nlm.nih.gov/element/Protactinium",
                    checked_field="boiling_point_k",
                    observed_value="4027",
                    observed_unit="degC",
                    source_result="secondary value matches LANL candidate cluster",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="rsc_periodic_table_protactinium",
                    source_authority="Royal Society of Chemistry",
                    source_url="https://periodic-table.rsc.org/element/91/protactinium",
                    checked_field="boiling_point_k",
                    observed_value="4000",
                    observed_unit="degC",
                    source_result="secondary value conflicts with PubChem/LANL cluster",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="webelements_protactinium",
                    source_authority="WebElements",
                    source_url="https://www.webelements.com/protactinium/",
                    checked_field="boiling_point_k",
                    observed_value="4300",
                    observed_unit="K",
                    source_result="secondary value aligns with LANL/PubChem cluster",
                ),
            ),
            conclusion=(
                "No higher-precedence field-specific boiling-point source was found; "
                "Pa remains blocked by nearby but non-identical secondary values."
            ),
            required_next_action=(
                "locate a higher-precedence field-specific source, or create an "
                "operator-approved conflict-resolution receipt before any gap closure"
            ),
        ),
        PhysicalPropertyEscalationSearchReceipt(
            search_id="MSPEE-PHYSICAL-PROPERTY-ESCALATION-SEARCH-Z087-Fr-density_value",
            target_escalation_receipt_id=francium_density_escalation.receipt_id,
            symbol=francium_density_escalation.symbol,
            atomic_number=francium_density_escalation.atomic_number,
            field_name=francium_density_escalation.field_name,
            search_status="corroborating_source_not_found",
            source_checks=(
                PhysicalPropertyEscalationSourceCheck(
                    source_key="webelements_francium",
                    source_authority="WebElements",
                    source_url="https://www.webelements.com/francium/",
                    checked_field="density_value",
                    observed_value="2900",
                    observed_unit="kg/m^3",
                    source_result="candidate value normalized elsewhere to 2.9 g/cm^3",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="rsc_periodic_table_francium",
                    source_authority="Royal Society of Chemistry",
                    source_url="https://periodic-table.rsc.org/element/87/francium",
                    checked_field="density_value",
                    observed_value=None,
                    observed_unit=None,
                    source_result="RSC lists Fr density as unknown",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="pubchem_element_francium",
                    source_authority="PubChem",
                    source_url="https://pubchem.ncbi.nlm.nih.gov/element/Francium",
                    checked_field="density_value",
                    observed_value=None,
                    observed_unit=None,
                    source_result="PubChem element page does not provide a density value",
                ),
            ),
            conclusion=(
                "No independent corroborating Fr density source was found; the "
                "WebElements candidate remains blocked."
            ),
            required_next_action=(
                "locate an independent field-specific Fr density source or record a "
                "rejection receipt before admission"
            ),
        ),
        PhysicalPropertyEscalationSearchReceipt(
            search_id="MSPEE-PHYSICAL-PROPERTY-ESCALATION-SEARCH-Z097-Bk-boiling_point_k",
            target_escalation_receipt_id=berkelium_escalation.receipt_id,
            symbol=berkelium_escalation.symbol,
            atomic_number=berkelium_escalation.atomic_number,
            field_name=berkelium_escalation.field_name,
            search_status="corroborating_source_not_found",
            source_checks=(
                PhysicalPropertyEscalationSourceCheck(
                    source_key="lanl_periodic_table_berkelium",
                    source_authority="Los Alamos National Laboratory",
                    source_url="https://periodic.lanl.gov/97.shtml",
                    checked_field="boiling_point_k",
                    observed_value="2627",
                    observed_unit="degC",
                    source_result="candidate source for Bk boiling point",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="rsc_periodic_table_berkelium",
                    source_authority="Royal Society of Chemistry",
                    source_url="https://periodic-table.rsc.org/element/97/berkelium",
                    checked_field="boiling_point_k",
                    observed_value=None,
                    observed_unit=None,
                    source_result="RSC lists Bk boiling point as unknown",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="webelements_berkelium",
                    source_authority="WebElements",
                    source_url="https://www.webelements.com/berkelium/",
                    checked_field="boiling_point_k",
                    observed_value=None,
                    observed_unit=None,
                    source_result="WebElements lists no boiling-point data for Bk",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="pubchem_element_berkelium",
                    source_authority="PubChem",
                    source_url="https://pubchem.ncbi.nlm.nih.gov/element/Berkelium",
                    checked_field="boiling_point_k",
                    observed_value="2627",
                    observed_unit="degC",
                    source_result="element page aligns with LANL cluster but is not treated as independent corroboration",
                ),
            ),
            conclusion=(
                "No independent corroborating Bk boiling-point source was found; "
                "the LANL candidate remains blocked."
            ),
            required_next_action=(
                "locate an independent field-specific Bk boiling-point source or "
                "record a rejection receipt before admission"
            ),
        ),
        PhysicalPropertyEscalationSearchReceipt(
            search_id="MSPEE-PHYSICAL-PROPERTY-ESCALATION-SEARCH-Z098-Cf-boiling_point_k",
            target_escalation_receipt_id=californium_escalation.receipt_id,
            symbol=californium_escalation.symbol,
            atomic_number=californium_escalation.atomic_number,
            field_name=californium_escalation.field_name,
            search_status="corroborating_source_not_found",
            source_checks=(
                PhysicalPropertyEscalationSourceCheck(
                    source_key="lanl_periodic_table_californium",
                    source_authority="Los Alamos National Laboratory",
                    source_url="https://periodic.lanl.gov/98.shtml",
                    checked_field="boiling_point_k",
                    observed_value="1470",
                    observed_unit="degC",
                    source_result="candidate source for Cf boiling point",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="rsc_periodic_table_californium",
                    source_authority="Royal Society of Chemistry",
                    source_url="https://periodic-table.rsc.org/element/98/californium",
                    checked_field="boiling_point_k",
                    observed_value=None,
                    observed_unit=None,
                    source_result="RSC lists Cf boiling point as unknown",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="webelements_californium",
                    source_authority="WebElements",
                    source_url="https://www.webelements.com/californium/",
                    checked_field="boiling_point_k",
                    observed_value=None,
                    observed_unit=None,
                    source_result="WebElements lists no boiling-point data for Cf",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="pubchem_element_californium",
                    source_authority="PubChem",
                    source_url="https://pubchem.ncbi.nlm.nih.gov/element/Californium",
                    checked_field="boiling_point_k",
                    observed_value="1470",
                    observed_unit="degC",
                    source_result="element page aligns with LANL cluster but is not treated as independent corroboration",
                ),
            ),
            conclusion=(
                "No independent corroborating Cf boiling-point source was found; "
                "the LANL candidate remains blocked."
            ),
            required_next_action=(
                "locate an independent field-specific Cf boiling-point source or "
                "record a rejection receipt before admission"
            ),
        ),
        PhysicalPropertyEscalationSearchReceipt(
            search_id="MSPEE-PHYSICAL-PROPERTY-ESCALATION-SEARCH-Z099-Es-boiling_point_k",
            target_escalation_receipt_id=einsteinium_escalation.receipt_id,
            symbol=einsteinium_escalation.symbol,
            atomic_number=einsteinium_escalation.atomic_number,
            field_name=einsteinium_escalation.field_name,
            search_status="corroborating_source_not_found",
            source_checks=(
                PhysicalPropertyEscalationSourceCheck(
                    source_key="lanl_periodic_table_einsteinium",
                    source_authority="Los Alamos National Laboratory",
                    source_url="https://periodic.lanl.gov/99.shtml",
                    checked_field="boiling_point_k",
                    observed_value="996",
                    observed_unit="degC",
                    source_result="candidate source for Es boiling point",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="rsc_periodic_table_einsteinium",
                    source_authority="Royal Society of Chemistry",
                    source_url="https://periodic-table.rsc.org/element/99/einsteinium",
                    checked_field="boiling_point_k",
                    observed_value=None,
                    observed_unit=None,
                    source_result="RSC lists Es boiling point as unknown",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="webelements_einsteinium",
                    source_authority="WebElements",
                    source_url="https://www.webelements.com/einsteinium/",
                    checked_field="boiling_point_k",
                    observed_value=None,
                    observed_unit=None,
                    source_result="WebElements essentials page does not provide independent boiling-point data",
                ),
                PhysicalPropertyEscalationSourceCheck(
                    source_key="pubchem_element_einsteinium",
                    source_authority="PubChem",
                    source_url="https://pubchem.ncbi.nlm.nih.gov/element/99",
                    checked_field="boiling_point_k",
                    observed_value="996",
                    observed_unit="degC",
                    source_result="element page aligns with LANL cluster but is not treated as independent corroboration",
                ),
            ),
            conclusion=(
                "No independent corroborating Es boiling-point source was found; "
                "the LANL candidate remains blocked."
            ),
            required_next_action=(
                "locate an independent field-specific Es boiling-point source or "
                "record a rejection receipt before admission"
            ),
        ),
    )


def get_physical_property_escalation_search_receipt(
    identifier: str | int,
) -> PhysicalPropertyEscalationSearchReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_escalation_search_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.search_id
            or identifier_text == receipt.target_escalation_receipt_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property escalation search receipt: {identifier_text}")


def validate_physical_property_escalation_search_receipts(
    receipts: tuple[PhysicalPropertyEscalationSearchReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts
        if receipts is not None
        else list_physical_property_escalation_search_receipts()
    )
    invalid_receipts = tuple(
        receipt.search_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_escalation_search_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_escalation_search_receipts_rejected"
    return {
        "validation_status": validation_status,
        "search_receipt_count": len(checked_receipts),
        "higher_precedence_source_not_found_count": sum(
            1
            for receipt in checked_receipts
            if receipt.search_status == "higher_precedence_source_not_found"
        ),
        "corroborating_source_not_found_count": sum(
            1
            for receipt in checked_receipts
            if receipt.search_status == "corroborating_source_not_found"
        ),
        "gap_closure_count": sum(1 for receipt in checked_receipts if receipt.closes_gap),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }
