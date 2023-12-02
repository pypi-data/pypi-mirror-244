context_schema = {
    "type": "object",
    "properties": {
        "context_check": {"type": "string", "enum": ["Out-of-context", "In-context"]},
    },
    "required": ["context_check"],
}

emotion_schema = {
    "type": "object",
    "properties": {
        "emotion_check": {"type": "string",
                          "enum": ["positive", "neutral", "confusion", "dissatisfaction", "frustration"]},
    },
    "required": ["emotion_check"]
}

intent_schema = {
    "type": "object",
    "properties": {
        "intent_check": {"type": "string",
                         "enum": ["Informational", "Navigational", "Greetings", "Follow-up", "Transactional",
                                  "Troubleshooting", "Instructional"]},
    },
    "required": ["intent_check"]
}

language_schema = {
    "type": "object",
    "properties": {
      "language_type": {"type": "string",
                          "description": "The ISO 639-1 two digit code of the language used in user-query e.g 'en', 'ur'."}
    },
    "required": ["language_type"]
}
