auth_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "access": {"type": "string"},
        "refresh": {"type": "string"},
    },
    "required": ["access", "refresh"],
}

error_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "detail": {"type": "string"},
    },
    "required": ["detail"],
}