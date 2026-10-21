import os
import urllib.request


class LLMClient:
    def __init__(self, provider=None, model=None, api_key=None, timeout=20):
        self.provider = provider or os.environ.get('LLM_PROVIDER', '')
        self.model = model or os.environ.get('LLM_MODEL', '')
        self.api_key = api_key or os.environ.get('LLM_API_KEY', '')
        self.timeout = timeout

    def complete(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError('LLM provider not configured')
        # Placeholder HTTP call; real provider integration replaces this.
        req = urllib.request.Request('https://api.example.com/v1/chat', data=prompt.encode(), method='POST')
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return resp.read().decode()
