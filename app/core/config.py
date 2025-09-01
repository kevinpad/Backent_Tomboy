import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "API-Tomboy-Unity")
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "8000"))
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()
