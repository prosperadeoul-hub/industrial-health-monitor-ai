from monitoring.integrations.llm.client import LLMClient
from monitoring.integrations.llm.schemas import validate_output


def generate_diagnostic(health_check, component) -> dict:
    client = LLMClient()
    prompt = f'Status={health_check.status} metrics={health_check.details}'
    try:
        raw = client.complete(prompt)
        data = validate_output(raw)
    except Exception:
        data = {
            'summary': 'Diagnostic unavailable',
            'findings': [],
            'recommendations': [],
            'limitations': ['LLM provider unavailable'],
        }
    # Never override official status
    data['status'] = health_check.status
    return data
