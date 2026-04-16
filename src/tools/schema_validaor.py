import json
from jsonschema import validate


def load_schema(path):
    with open(path) as f:
        return json.load(f)


def validate_json(data, schema_path):
    schema = load_schema(schema_path)
    validate(instance=data, schema=schema)
    return True