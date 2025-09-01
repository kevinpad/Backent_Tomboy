# src/index.py
from typing import List, Literal, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv; load_dotenv()

from google import genai
from google.genai import types

app = FastAPI(title="Gemini API local")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Role = Literal["user", "model"]

class Message(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gemini-2.5-flash"
    temperature: Optional[float] = 0.7
    thinking_budget: Optional[int] = 0

class ChatResponse(BaseModel):
    text: str

client = genai.Client()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest):
    try:
        contents = [types.Content(role=m.role, parts=[types.Part.from_text(m.content)])
                    for m in body.messages]
        resp = client.models.generate_content(
            model=body.model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=body.temperature,
                thinking_config=types.ThinkingConfig(thinking_budget=body.thinking_budget)
                if body.thinking_budget is not None else None
            ),
        )
        return ChatResponse(text=resp.text or "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
