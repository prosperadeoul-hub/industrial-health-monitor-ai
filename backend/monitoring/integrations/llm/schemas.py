import json

REQUIRED_KEYS = {'summary', 'findings', 'recommendations', 'limitations'}


def validate_output(raw: str) -> dict:
    data = json.loads(raw)
    if not isinstance(data, dict) or not REQUIRED_KEYS.issubset(data.keys()):
        raise ValueError('Invalid LLM output schema')
    return data
