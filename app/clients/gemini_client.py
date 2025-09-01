from google import genai
from google.genai import types
from ..core.config import settings

def get_gemini_client() -> genai.Client:
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("Falta GEMINI_API_KEY en .env")
    return genai.Client(api_key=settings.GEMINI_API_KEY)

Content = types.Content
Part = types.Part
GenerateContentConfig = types.GenerateContentConfig
ThinkingConfig = types.ThinkingConfig