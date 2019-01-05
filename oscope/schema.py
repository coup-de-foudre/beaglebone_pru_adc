import time

import jsonschema

import oscope

# Schema doc for the trace metadata
TRACE_SCHEMA = {
    "type": "object",
    "properties" : {
        "samples" : {
            "type" : "number",
            "description": "The number of samples taken"    
        },
        "frequency" : {
            "type" : "number",
            "description" : "The frequency in Hertz of sampling"    
        },
        "channel": {
            "type": "number",
            "description": "The integer channel on this device."
        },
    },
    "required": ["samples", "frequency", "channel"]
}


DEVICE_SCHEMA = {
    "type": "object",
    "properties" : {
        "name" : {
            "type" : "string",
            "description": "The name of the sampling device"    
        },
        "id" : {
            "type" : "string",
            "description" : "A unique identifier for the device"    
        },
        "session" : {
            "type": "string",
            "description" : "A uuid unique to the software invocation"
        },
        "time": {
            "type": "number",
            "description": "Time in epoch seconds on the device."
        },
    },
    "required": ["name", "id", "session", "time"]
}

MESSAGE_SCHEMA = {
    "type" : "object",
    "properties" : {
        "device": DEVICE_SCHEMA,
        "trace": TRACE_SCHEMA,
        "sequence": {"type": "number"}
    },
    "required": ["device", "trace", "sequence"]
}

def validate_trace_metadata(trace: dict):
    """
    Raise a `jsonschema.ValidationError` if the trace metadata is not
    properly formed.
    """
    jsonschema.validate(trace, MESSAGE_SCHEMA)


def get_device_meta(name: str, id: str):
    return {
        "name": name,
        "id": id,
        "session": oscope.__session__,
        "time": time.time(),
    }
