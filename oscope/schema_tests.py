import pytest
import jsonschema

import oscope.schema as schema


def test_validator_fails():
    with pytest.raises(jsonschema.ValidationError):
        schema.validate_trace_metadata({})
    
def test_validator_success():
    valid = {
        "device": {
            "id": "foo",
            "name": "bar",
            "session": "baz",
            "time": 0
        },
        "trace": {
            "samples": 100,
            "frequency": 3000000,
            "channel": 1
        },
        "sequence": 0
    }
    schema.validate_trace_metadata(valid)
