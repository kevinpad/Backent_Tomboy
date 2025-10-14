# app/services/openai_chat_service.py
from typing import List, Dict
from fastapi import HTTPException
import traceback

from app.clients.openai_client import get_openai_client, get_default_model
from app.core.roles import get_role              # lee app/config/roles.json (tu loader)
from app.schemas.chat import ChatRequest, ChatResponse  # MISMO esquema que usas con Gemini


def _to_openai_messages(body: ChatRequest, system_prompt: str | None) -> List[Dict[str, str]]:
    """
    Convierte tu ChatRequest (roles: 'user' | 'model') al formato OpenAI
    (roles: 'user' | 'assistant' | 'system') e inyecta el system prompt si existe.
    """
    msgs: List[Dict[str, str]] = []

    if system_prompt:
        msgs.append({"role": "system", "content": system_prompt})

    for m in body.messages:
        role = "assistant" if m.role == "model" else "user"
        msgs.append({"role": role, "content": m.content})

    return msgs


def _chat_openai_with_role_id(body: ChatRequest, role_id: str) -> ChatResponse:
    # 1) Obtener system prompt desde roles.json
    role = get_role(role_id)
    system_prompt: str | None = role.get("system_prompt") if role else None

    # 2) Cliente y modelo
    client = get_openai_client()
    model = body.model or get_default_model()

    # Parachoques: si por error llega un modelo de Google (ej. "gemini-*"),
    # lo ignoramos y usamos el de .env (OpenAI).
    if isinstance(model, str) and model.lower().startswith("gemini"):
        model = get_default_model()

    # 3) Preparar mensajes y llamar a OpenAI
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=_to_openai_messages(body, system_prompt),
            temperature=body.temperature if body.temperature is not None else 0.7,
            max_tokens=800,   # ajusta si quieres exponerlo en tu schema
        )
        text = completion.choices[0].message.content or ""
        return ChatResponse(text=text)

    except Exception as e:
        # Log útil en consola mientras depuras (puedes quitarlo en prod)
        print("[OpenAI ERROR]", type(e).__name__, str(e))
        traceback.print_exc()
        # Devuelve detalle útil al cliente durante desarrollo
        raise HTTPException(status_code=500, detail=f"OpenAI: {type(e).__name__}: {e}")


def chat_psychology_openai(body: ChatRequest) -> ChatResponse:
    return _chat_openai_with_role_id(body, "psychology")


def chat_motivation_openai(body: ChatRequest) -> ChatResponse:
    return _chat_openai_with_role_id(body, "motivation")
