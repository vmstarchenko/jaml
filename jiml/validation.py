import jsonschema

from . import exceptions

JSONSCHEMA_DEFAULT_DRAFT = 7


def build_validator(schema, defaults):
    schema = {**defaults, **(schema or {})}
    draft = schema.pop('draft', JSONSCHEMA_DEFAULT_DRAFT)
    Validator = getattr(jsonschema, f'Draft{draft}Validator')
    Validator.check_schema(schema)
    validator = Validator(schema)
    return validator


def build_input_validator(schema):
    try:
        return build_validator(schema, {'type': 'object'})
    except Exception as e:
        raise exceptions.InputSchemaSyntaxError(e) from e


def build_output_validator(schema):
    try:
        return build_validator(schema, {})
    except Exception as e:
        raise exceptions.OutputSchemaSyntaxError(e) from e
