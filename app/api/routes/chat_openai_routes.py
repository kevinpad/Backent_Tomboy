# app/api/routes/chat_openai_routes.py
from fastapi import APIRouter, Body
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.openai_chat_service import (
    chat_psychology_openai,
    chat_motivation_openai,
)
from app.clients.openai_client import get_openai_client, get_default_model

router = APIRouter(prefix="/chat-openai", tags=["chat-openai"])

# Ejemplo que verá Swagger para estos endpoints (OpenAI)
openai_example = {
    "messages": [
        {"role": "user", "content": "Hola, me siento triste. ¿Me ayudas?"}
    ],
    "model": "gpt-4o-mini",
    "temperature": 0.7
}

@router.get("/health")
def openai_health():
    try:
        c = get_openai_client()
        m = get_default_model()
        # ping mínimo
        _ = c.chat.completions.create(
            model=m,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1
        )
        return {"ok": True, "model": m}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}

@router.post("/psychology", response_model=ChatResponse)
def psychology(
    body: ChatRequest = Body(example=openai_example)
) -> ChatResponse:
    return chat_psychology_openai(body)

@router.post("/motivation", response_model=ChatResponse)
def motivation(
    body: ChatRequest = Body(example=openai_example)
) -> ChatResponse:
    return chat_motivation_openai(body)
