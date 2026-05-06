club_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "bookTitle": {"type": "string"},
        "bookAuthors": {"type": "string"},
        "publicationYear": {"type": "integer"},
        "description": {"type": ["string", "null"]},
        "telegramChatLink": {"type": ["string", "null"]},
        "owner": {"type": "integer"},
        "members": {"type": "array", "items": {"type": "integer"}},
        "reviews": {"type": "array"},
        "created": {"type": "string"},
        "modified": {"type": ["string", "null"]},
    },
    "required": ["id", "bookTitle", "owner", "members", "created", "modified"],
}

clubs_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "count": {"type": "integer"},
        "next": {"type": ["string", "null"]},
        "previous": {"type": ["string", "null"]},
        "results": {"type": "array", "items": club_schema},
    },
    "required": ["count", "results"],
}