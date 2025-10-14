import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_client: OpenAI | None = None

def get_openai_client() -> OpenAI:
    global _client
    if _client is None:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("Falta OPENAI_API_KEY en .env")
        _client = OpenAI(api_key=key)
    return _client

def get_default_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
