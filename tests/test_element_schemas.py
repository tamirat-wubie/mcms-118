import json

import pytest
from jsonschema import Draft202012Validator, ValidationError

from mcms.cli import cmd_elements
from mcms.elements import (
    element_schema_bundle,
    element_seed_json_schema,
    element_snapshot_json_schema,
    get_seed_element,
    get_snapshot_record,
)


def _json_payload(payload: dict) -> dict:
    return json.loads(json.dumps(payload))


def test_element_seed_schema_validates_seed_records_and_rejects_extra_fields():
    schema = element_seed_json_schema()
    validator = Draft202012Validator(schema)
    zinc_payload = _json_payload(get_seed_element("Zn").to_dict())
    invalid_payload = {**zinc_payload, "unexpected_symbol_field": True}
    Draft202012Validator.check_schema(schema)
    validator.validate(zinc_payload)
    assert schema["title"] == "MulluStandardSymbolicElement"
    assert zinc_payload["state"]["block"] == "d"
    with pytest.raises(ValidationError):
        validator.validate(invalid_payload)


def test_snapshot_schema_validates_grouped_and_ungrouped_records():
    schema = element_snapshot_json_schema()
    validator = Draft202012Validator(schema)
    hydrogen_payload = _json_payload(get_snapshot_record("H").to_dict())
    lanthanum_payload = _json_payload(get_snapshot_record("La").to_dict())
    Draft202012Validator.check_schema(schema)
    validator.validate(hydrogen_payload)
    validator.validate(lanthanum_payload)
    assert hydrogen_payload["group"] == 1
    assert lanthanum_payload["group"] is None
    assert schema["properties"]["snapshot_status"]["enum"] == [
        "identity_snapshot",
        "level_1_seed_available",
    ]


def test_schema_bundle_exposes_both_contracts():
    bundle = element_schema_bundle()
    schema_keys = set(bundle["schemas"])
    assert bundle["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema_keys == {
        "mullu_standard_symbolic_element",
        "element_source_snapshot_record",
    }
    assert (
        bundle["schemas"]["mullu_standard_symbolic_element"]["$id"]
        != bundle["schemas"]["element_source_snapshot_record"]["$id"]
    )


def test_element_schema_cli_prints_valid_bundle(capsys):
    cmd_elements(symbol=None, list_only=False, full_snapshot=False, schema_name="bundle")
    output = json.loads(capsys.readouterr().out)
    assert output["$id"].endswith("/schema-bundle.json")
    assert "mullu_standard_symbolic_element" in output["schemas"]
    assert "element_source_snapshot_record" in output["schemas"]
