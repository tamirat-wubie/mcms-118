from __future__ import annotations

from dataclasses import dataclass

@dataclass
class JSONSchemaBindingValidatorResult:
    validation_key: str
    schema_kind: str
    library_available: bool
    validation_error_count: int
    error_paths: list[str]
    binding_status: str
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def validate_jsonschema_binding(validation_key: str, schema_kind: str, schema: dict, instance: dict) -> JSONSchemaBindingValidatorResult:
    if not validation_key or not schema_kind or not schema or instance is None:
        return JSONSchemaBindingValidatorResult(validation_key, schema_kind, False, 0, [], "insufficient_data", "JSONSchema binding input is invalid.")
    try:
        import jsonschema
    except Exception:
        return JSONSchemaBindingValidatorResult(validation_key, schema_kind, False, 0, [], "jsonschema_library_missing", "jsonschema library is not available.")
    try:
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        validator = validator_cls(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    except jsonschema.exceptions.SchemaError as exc:
        return JSONSchemaBindingValidatorResult(validation_key, schema_kind, True, 1, [str(exc.path)], "jsonschema_schema_error", "JSON schema itself is invalid.")
    except Exception as exc:
        return JSONSchemaBindingValidatorResult(validation_key, schema_kind, True, 1, ["unknown"], "jsonschema_instance_error", f"JSON instance validation failed unexpectedly: {type(exc).__name__}")
    paths = [".".join(str(part) for part in error.path) or "$" for error in errors]
    if errors:
        return JSONSchemaBindingValidatorResult(validation_key, schema_kind, True, len(errors), paths, "jsonschema_validation_failed", "JSON instance failed schema validation.")
    return JSONSchemaBindingValidatorResult(validation_key, schema_kind, True, 0, [], "jsonschema_validation_passed", "JSON instance passed schema validation.")
