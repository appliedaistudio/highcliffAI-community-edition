# needed for context validation
from jsonschema import validate, ValidationError
import json

# needed to reference the json schema file from within the host application
import pkgutil


def is_validate_context(context_json) -> bool:
    # get a reference to the context schema json
    context_schema_json_file_path = 'context_schema.json'
    context_schema_json_string = pkgutil.get_data(__name__, context_schema_json_file_path).decode("utf-8")
    context_schema_json = json.loads(context_schema_json_string)

    # validate new context against the context schem
    try:
        validate(context_json, context_schema_json)
        is_valid = True

    except ValidationError:
        is_valid = False

    return is_valid
