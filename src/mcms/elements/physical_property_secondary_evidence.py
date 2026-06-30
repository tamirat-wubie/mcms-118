"""Purpose: define source-specific secondary physical-property evidence receipts.

Project scope: models field-specific secondary-source receipts that may close
physical-property gaps only after policy validation and explicit approval.
Dependencies: secondary-source policy records.
Invariants: no secondary value is admitted without a source-specific receipt;
policy records do not close gaps by themselves.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from mcms.elements.physical_property_source_policy import (
    get_physical_property_secondary_source_policy,
)

VALID_SECONDARY_EVIDENCE_VALUE_TYPES = {"measured", "estimated", "predicted"}
VALID_SECONDARY_EVIDENCE_STATUSES = {
    "secondary_evidence_candidate",
    "secondary_evidence_admitted",
    "secondary_evidence_rejected",
}
VALID_SECONDARY_EVIDENCE_DECISIONS = {
    "awaiting_source_receipt",
    "reviewed_pending_approval",
    "admit_after_review",
    "reject_after_review",
}

AT_LANL_BOILING_POINT_CANDIDATE_K = 610.15
FR_LANL_BOILING_POINT_CANDIDATE_K = 953.15
FR_WEBELEMENTS_DENSITY_CANDIDATE_G_PER_CM3 = 2.9
PA_LANL_BOILING_POINT_CANDIDATE_K = 4300.15
CF_LANL_BOILING_POINT_CANDIDATE_K = 1743.15
CF_RSC_DENSITY_CANDIDATE_G_PER_CM3 = 15.1
ES_LANL_BOILING_POINT_CANDIDATE_K = 1269.15
BK_LANL_BOILING_POINT_CANDIDATE_K = 2900.15


@dataclass(frozen=True)
class PhysicalPropertySecondaryEvidenceReceipt:
    receipt_id: str
    policy_id: str
    target_gap_receipt_id: str
    symbol: str
    atomic_number: int
    field_name: str
    normalized_value: float
    normalized_unit: str
    raw_value: str
    raw_unit: str
    value_type: str
    source_key: str
    source_authority: str
    source_title: str
    source_citation: str
    retrieval_date: str
    field_name_mapping: str
    source_license_boundary: str
    admission_status: str
    admission_decision: str
    conflict_status: str
    seed_mutation_allowed: bool
    notes: tuple[str, ...] = (
        "Secondary evidence receipts are field-specific and do not mutate seed records.",
        "Seed mutation requires separate promotion approval after gap closure.",
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        policy = get_physical_property_secondary_source_policy(self.policy_id)
        candidate_by_key = {
            candidate.source_key: candidate for candidate in policy.candidate_sources
        }
        candidate = candidate_by_key.get(self.source_key)
        if self.target_gap_receipt_id != policy.target_gap_receipt_id:
            errors.append("secondary evidence target gap must match policy target gap.")
        if self.symbol != policy.symbol:
            errors.append("secondary evidence symbol must match policy symbol.")
        if self.atomic_number != policy.atomic_number:
            errors.append("secondary evidence atomic number must match policy atomic number.")
        if self.field_name not in policy.missing_fields:
            errors.append("secondary evidence field must be missing in the target gap.")
        if candidate is None:
            errors.append("secondary evidence source key must be a policy candidate.")
        elif self.field_name not in candidate.allowed_fields:
            errors.append("secondary evidence field must be allowed by the source candidate.")
        if self.normalized_value <= 0:
            errors.append("secondary evidence normalized value must be positive.")
        if self.field_name.endswith("_k") and self.normalized_unit != "K":
            errors.append("temperature secondary evidence must normalize to kelvin.")
        if self.value_type not in VALID_SECONDARY_EVIDENCE_VALUE_TYPES:
            errors.append("secondary evidence value type is unknown.")
        if self.admission_status not in VALID_SECONDARY_EVIDENCE_STATUSES:
            errors.append("secondary evidence admission status is unknown.")
        if self.admission_decision not in VALID_SECONDARY_EVIDENCE_DECISIONS:
            errors.append("secondary evidence admission decision is unknown.")
        if self.seed_mutation_allowed:
            errors.append("secondary evidence receipt alone must not allow seed mutation.")
        required_text_fields = (
            self.raw_value,
            self.raw_unit,
            self.source_authority,
            self.source_title,
            self.source_citation,
            self.retrieval_date,
            self.field_name_mapping,
            self.source_license_boundary,
            self.conflict_status,
        )
        if any(not field for field in required_text_fields):
            errors.append("secondary evidence receipt requires complete provenance fields.")
        return errors

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["notes"] = list(self.notes)
        return payload


def list_physical_property_secondary_evidence_receipts() -> tuple[
    PhysicalPropertySecondaryEvidenceReceipt, ...
]:
    return (
        PhysicalPropertySecondaryEvidenceReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
                "Z085-At-boiling_point_k-LANL"
            ),
            policy_id="MSPEE-PHYSICAL-PROPERTY-SECONDARY-SOURCE-POLICY-Z085-At",
            target_gap_receipt_id="MSPEE-PHYSICAL-PROPERTY-GAP-Z085-At",
            symbol="At",
            atomic_number=85,
            field_name="boiling_point_k",
            normalized_value=AT_LANL_BOILING_POINT_CANDIDATE_K,
            normalized_unit="K",
            raw_value="337",
            raw_unit="degC",
            value_type="estimated",
            source_key="lanl_periodic_table_candidate",
            source_authority="Los Alamos National Laboratory",
            source_title="Periodic Table of Elements: Astatine",
            source_citation="https://periodic.lanl.gov/85.shtml",
            retrieval_date="2026-06-29",
            field_name_mapping="LANL boiling point -> boiling_point_k",
            source_license_boundary="public web reference; redistribution boundary requires citation",
            admission_status="secondary_evidence_candidate",
            admission_decision="reviewed_pending_approval",
            conflict_status=(
                "candidate value requires conflict review against other secondary "
                "sources before admission"
            ),
            seed_mutation_allowed=False,
            notes=(
                "LANL candidate normalizes 337 degC to 610.15 K.",
                "Receipt is not admitted evidence and does not close the At gap.",
            ),
        ),
        PhysicalPropertySecondaryEvidenceReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
                "Z087-Fr-boiling_point_k-LANL"
            ),
            policy_id="MSPEE-PHYSICAL-PROPERTY-SECONDARY-SOURCE-POLICY-Z087-Fr",
            target_gap_receipt_id="MSPEE-PHYSICAL-PROPERTY-GAP-Z087-Fr",
            symbol="Fr",
            atomic_number=87,
            field_name="boiling_point_k",
            normalized_value=FR_LANL_BOILING_POINT_CANDIDATE_K,
            normalized_unit="K",
            raw_value="680",
            raw_unit="degC",
            value_type="estimated",
            source_key="lanl_periodic_table_candidate",
            source_authority="Los Alamos National Laboratory",
            source_title="Periodic Table of Elements: Francium",
            source_citation="https://periodic.lanl.gov/87.shtml",
            retrieval_date="2026-06-30",
            field_name_mapping="LANL boiling point -> boiling_point_k",
            source_license_boundary="public web reference; redistribution boundary requires citation",
            admission_status="secondary_evidence_candidate",
            admission_decision="reviewed_pending_approval",
            conflict_status=(
                "candidate value requires conflict review because RSC and WebElements "
                "list different boiling-point values"
            ),
            seed_mutation_allowed=False,
            notes=(
                "LANL candidate normalizes 680 degC to 953.15 K.",
                "Receipt is not admitted evidence and does not close the Fr gap.",
            ),
        ),
        PhysicalPropertySecondaryEvidenceReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
                "Z087-Fr-density_value-WebElements"
            ),
            policy_id="MSPEE-PHYSICAL-PROPERTY-SECONDARY-SOURCE-POLICY-Z087-Fr",
            target_gap_receipt_id="MSPEE-PHYSICAL-PROPERTY-GAP-Z087-Fr",
            symbol="Fr",
            atomic_number=87,
            field_name="density_value",
            normalized_value=FR_WEBELEMENTS_DENSITY_CANDIDATE_G_PER_CM3,
            normalized_unit="g/cm^3",
            raw_value="2900",
            raw_unit="kg/m^3",
            value_type="estimated",
            source_key="web_elements_candidate",
            source_authority="WebElements",
            source_title="WebElements Periodic Table: Francium",
            source_citation="https://www.webelements.com/francium/",
            retrieval_date="2026-06-30",
            field_name_mapping="WebElements density of solid -> density_value",
            source_license_boundary="public web reference; redistribution boundary requires citation",
            admission_status="secondary_evidence_candidate",
            admission_decision="reviewed_pending_approval",
            conflict_status=(
                "candidate value requires corroboration because RSC lists density "
                "as unknown"
            ),
            seed_mutation_allowed=False,
            notes=(
                "WebElements candidate normalizes 2900 kg/m^3 to 2.9 g/cm^3.",
                "Receipt is not admitted evidence and does not close the Fr gap.",
            ),
        ),
        PhysicalPropertySecondaryEvidenceReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
                "Z091-Pa-boiling_point_k-LANL"
            ),
            policy_id="MSPEE-PHYSICAL-PROPERTY-SECONDARY-SOURCE-POLICY-Z091-Pa",
            target_gap_receipt_id="MSPEE-PHYSICAL-PROPERTY-GAP-Z091-Pa",
            symbol="Pa",
            atomic_number=91,
            field_name="boiling_point_k",
            normalized_value=PA_LANL_BOILING_POINT_CANDIDATE_K,
            normalized_unit="K",
            raw_value="4027",
            raw_unit="degC",
            value_type="estimated",
            source_key="lanl_periodic_table_candidate",
            source_authority="Los Alamos National Laboratory",
            source_title="Periodic Table of Elements: Protactinium",
            source_citation="https://periodic.lanl.gov/91.shtml",
            retrieval_date="2026-06-29",
            field_name_mapping="LANL boiling point -> boiling_point_k",
            source_license_boundary="public web reference; redistribution boundary requires citation",
            admission_status="secondary_evidence_candidate",
            admission_decision="reviewed_pending_approval",
            conflict_status=(
                "candidate value requires conflict review because RSC/WebElements "
                "list nearby but not identical boiling-point values"
            ),
            seed_mutation_allowed=False,
            notes=(
                "LANL candidate normalizes 4027 degC to 4300.15 K.",
                "Receipt is not admitted evidence and does not close the Pa gap.",
            ),
        ),
        PhysicalPropertySecondaryEvidenceReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
                "Z098-Cf-boiling_point_k-LANL"
            ),
            policy_id="MSPEE-PHYSICAL-PROPERTY-SECONDARY-SOURCE-POLICY-Z098-Cf",
            target_gap_receipt_id="MSPEE-PHYSICAL-PROPERTY-GAP-Z098-Cf",
            symbol="Cf",
            atomic_number=98,
            field_name="boiling_point_k",
            normalized_value=CF_LANL_BOILING_POINT_CANDIDATE_K,
            normalized_unit="K",
            raw_value="1470",
            raw_unit="degC",
            value_type="estimated",
            source_key="lanl_periodic_table_candidate",
            source_authority="Los Alamos National Laboratory",
            source_title="Periodic Table of Elements: Californium",
            source_citation="https://periodic.lanl.gov/98.shtml",
            retrieval_date="2026-06-30",
            field_name_mapping="LANL boiling point -> boiling_point_k",
            source_license_boundary="public web reference; redistribution boundary requires citation",
            admission_status="secondary_evidence_candidate",
            admission_decision="reviewed_pending_approval",
            conflict_status=(
                "candidate value requires corroboration because RSC lists the "
                "boiling point as unknown"
            ),
            seed_mutation_allowed=False,
            notes=(
                "LANL candidate normalizes 1470 degC to 1743.15 K.",
                "Receipt is not admitted evidence and does not close the Cf gap.",
            ),
        ),
        PhysicalPropertySecondaryEvidenceReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
                "Z098-Cf-density_value-RSC"
            ),
            policy_id="MSPEE-PHYSICAL-PROPERTY-SECONDARY-SOURCE-POLICY-Z098-Cf",
            target_gap_receipt_id="MSPEE-PHYSICAL-PROPERTY-GAP-Z098-Cf",
            symbol="Cf",
            atomic_number=98,
            field_name="density_value",
            normalized_value=CF_RSC_DENSITY_CANDIDATE_G_PER_CM3,
            normalized_unit="g/cm^3",
            raw_value="15.1",
            raw_unit="g/cm^3",
            value_type="measured",
            source_key="rsc_periodic_table_candidate",
            source_authority="Royal Society of Chemistry",
            source_title="RSC Periodic Table: Californium",
            source_citation="https://periodic-table.rsc.org/element/98/californium",
            retrieval_date="2026-06-30",
            field_name_mapping="RSC density -> density_value",
            source_license_boundary="public web reference; redistribution boundary requires citation",
            admission_status="secondary_evidence_candidate",
            admission_decision="reviewed_pending_approval",
            conflict_status=(
                "candidate value requires review against other secondary sources "
                "before admission"
            ),
            seed_mutation_allowed=False,
            notes=(
                "RSC density candidate is 15.1 g/cm^3.",
                "Receipt is not admitted evidence and does not close the Cf gap.",
            ),
        ),
        PhysicalPropertySecondaryEvidenceReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
                "Z099-Es-boiling_point_k-LANL"
            ),
            policy_id="MSPEE-PHYSICAL-PROPERTY-SECONDARY-SOURCE-POLICY-Z099-Es",
            target_gap_receipt_id="MSPEE-PHYSICAL-PROPERTY-GAP-Z099-Es",
            symbol="Es",
            atomic_number=99,
            field_name="boiling_point_k",
            normalized_value=ES_LANL_BOILING_POINT_CANDIDATE_K,
            normalized_unit="K",
            raw_value="996",
            raw_unit="degC",
            value_type="estimated",
            source_key="lanl_periodic_table_candidate",
            source_authority="Los Alamos National Laboratory",
            source_title="Periodic Table of Elements: Einsteinium",
            source_citation="https://periodic.lanl.gov/99.shtml",
            retrieval_date="2026-06-30",
            field_name_mapping="LANL boiling point -> boiling_point_k",
            source_license_boundary="public web reference; redistribution boundary requires citation",
            admission_status="secondary_evidence_candidate",
            admission_decision="reviewed_pending_approval",
            conflict_status=(
                "candidate value requires corroboration because RSC lists the "
                "boiling point as unknown"
            ),
            seed_mutation_allowed=False,
            notes=(
                "LANL candidate normalizes 996 degC to 1269.15 K.",
                "Receipt is not admitted evidence and does not close the Es gap.",
            ),
        ),
        PhysicalPropertySecondaryEvidenceReceipt(
            receipt_id=(
                "MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
                "Z097-Bk-boiling_point_k-LANL"
            ),
            policy_id="MSPEE-PHYSICAL-PROPERTY-SECONDARY-SOURCE-POLICY-Z097-Bk",
            target_gap_receipt_id="MSPEE-PHYSICAL-PROPERTY-GAP-Z097-Bk",
            symbol="Bk",
            atomic_number=97,
            field_name="boiling_point_k",
            normalized_value=BK_LANL_BOILING_POINT_CANDIDATE_K,
            normalized_unit="K",
            raw_value="2627",
            raw_unit="degC",
            value_type="estimated",
            source_key="lanl_periodic_table_candidate",
            source_authority="Los Alamos National Laboratory",
            source_title="Periodic Table of Elements: Berkelium",
            source_citation="https://periodic.lanl.gov/97.shtml",
            retrieval_date="2026-06-29",
            field_name_mapping="LANL boiling point -> boiling_point_k",
            source_license_boundary="public web reference; redistribution boundary requires citation",
            admission_status="secondary_evidence_candidate",
            admission_decision="reviewed_pending_approval",
            conflict_status=(
                "candidate value requires corroboration because RSC lists the "
                "boiling point as unknown"
            ),
            seed_mutation_allowed=False,
            notes=(
                "LANL candidate normalizes 2627 degC to 2900.15 K.",
                "Receipt is not admitted evidence and does not close the Bk gap.",
            ),
        ),
    )


def get_physical_property_secondary_evidence_receipt(
    identifier: str | int,
) -> PhysicalPropertySecondaryEvidenceReceipt:
    identifier_text = str(identifier).strip()
    for receipt in list_physical_property_secondary_evidence_receipts():
        if (
            identifier_text == str(receipt.atomic_number)
            or identifier_text.upper() == receipt.symbol.upper()
            or identifier_text == receipt.receipt_id
            or identifier_text == receipt.target_gap_receipt_id
        ):
            return receipt
    raise KeyError(f"unknown physical-property secondary evidence receipt: {identifier_text}")


def validate_physical_property_secondary_evidence_receipts(
    receipts: tuple[PhysicalPropertySecondaryEvidenceReceipt, ...] | None = None,
) -> dict[str, Any]:
    checked_receipts = (
        receipts if receipts is not None else list_physical_property_secondary_evidence_receipts()
    )
    invalid_receipts = tuple(
        receipt.receipt_id for receipt in checked_receipts if receipt.validate()
    )
    validation_status = "physical_property_secondary_evidence_receipts_validated"
    if invalid_receipts:
        validation_status = "physical_property_secondary_evidence_receipts_rejected"
    return {
        "validation_status": validation_status,
        "receipt_count": len(checked_receipts),
        "admitted_count": sum(
            1
            for receipt in checked_receipts
            if receipt.admission_status == "secondary_evidence_admitted"
        ),
        "seed_mutation_allowed_count": sum(
            1 for receipt in checked_receipts if receipt.seed_mutation_allowed
        ),
        "invalid_receipts": invalid_receipts,
    }


def build_physical_property_secondary_evidence_template(
    identifier: str | int,
    *,
    source_key: str = "nist_chemistry_webbook_candidate",
) -> dict[str, Any]:
    policy = get_physical_property_secondary_source_policy(identifier)
    if source_key not in {candidate.source_key for candidate in policy.candidate_sources}:
        raise KeyError(f"unknown secondary source candidate for policy: {source_key}")
    field_name = policy.missing_fields[0]
    return {
        "receipt_id": (
            f"MSPEE-PHYSICAL-PROPERTY-SECONDARY-EVIDENCE-"
            f"Z{policy.atomic_number:03d}-{policy.symbol}-{field_name}"
        ),
        "policy_id": policy.policy_id,
        "target_gap_receipt_id": policy.target_gap_receipt_id,
        "symbol": policy.symbol,
        "atomic_number": policy.atomic_number,
        "field_name": field_name,
        "source_key": source_key,
        "required_fields": (
            "normalized_value",
            "normalized_unit",
            "raw_value",
            "raw_unit",
            "value_type",
            "source_authority",
            "source_title",
            "source_citation",
            "retrieval_date",
            "field_name_mapping",
            "source_license_boundary",
            "conflict_status",
        ),
        "default_admission_status": "secondary_evidence_candidate",
        "default_admission_decision": "awaiting_source_receipt",
        "seed_mutation_allowed": False,
    }
