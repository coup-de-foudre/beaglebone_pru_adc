import jsonschema

# Schema doc for the trace metadata
trace_schema = {
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


device_schema = {
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

trace_schema = {
    "type" : "object",
    "properties" : {
        "device": device_schema,
        "trace": trace_schema,
        "sequence": {"type": "number"}
    },
    "required": ["device", "trace", "sequence"]
}

def validate_trace_metadata(trace: dict):
    """
    Raise a validation error if the trace metadata is not
    properly formed.
    """
    jsonschema.validate(trace, trace_schema)
