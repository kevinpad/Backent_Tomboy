# app/services/chat_service.py
from app.clients.gemini_client import get_gemini_client
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.roles import get_role


def _build_config(temperature: float, thinking_budget: int | None, system_prompt: str | None) -> dict:
    cfg: dict = {"temperature": temperature}
    if thinking_budget is not None:
        cfg["thinking_config"] = {"thinking_budget": thinking_budget}
    if system_prompt:
        # si tu versión soporta system_instruction, lo usa; si no, haremos prepend
        cfg["system_instruction"] = system_prompt
    return cfg


def _prepend_system_if_needed(contents: list[dict], cfg: dict, system_prompt: str | None) -> list[dict]:
    has_sys = cfg.get("system_instruction")
    if system_prompt and not has_sys:
        head = {"role": "user", "parts": [{"text": system_prompt}]}
        return [head] + contents
    return contents


def _chat_with_role_id(body: ChatRequest, role_id: str) -> ChatResponse:
    role = get_role(role_id)
    system_prompt = role.get("system_prompt") if role else None

    client = get_gemini_client()

    # ✅ Usa diccionarios: cada mensaje -> {"role": ..., "parts": [{"text": "..."}]}
    contents = [
        {"role": m.role, "parts": [{"text": m.content}]}
        for m in body.messages
    ]

    cfg = _build_config(body.temperature, body.thinking_budget, system_prompt)
    contents = _prepend_system_if_needed(contents, cfg, system_prompt)

    resp = client.models.generate_content(
        model=body.model,
        contents=contents,
        config=cfg,
    )
    return ChatResponse(text=(getattr(resp, "text", "") or ""))


def chat_psychology(body: ChatRequest) -> ChatResponse:
    return _chat_with_role_id(body, "psychology")


def chat_motivation(body: ChatRequest) -> ChatResponse:
    return _chat_with_role_id(body, "motivation")