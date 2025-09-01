from app.clients.gemini_client import (
    get_gemini_client, Content, Part, GenerateContentConfig, ThinkingConfig
)
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.roles import get_role


def _build_config(temperature: float, thinking_budget: int | None, system_prompt: str | None):
    cfg = GenerateContentConfig(
        temperature=temperature,
        thinking_config=ThinkingConfig(thinking_budget=thinking_budget)
        if thinking_budget is not None else None
    )
    # Algunas versiones soportan system_instruction; si falla, haremos prepend.
    if system_prompt:
        try:
            setattr(cfg, "system_instruction", system_prompt)
        except Exception:
            pass
    return cfg


def _prepend_system_prompt(contents: list[Content], system_prompt: str | None) -> list[Content]:
    if not system_prompt:
        return contents
    head = Content(role="user", parts=[Part.from_text(f"[SYSTEM]\n{system_prompt}")])
    return [head] + contents


def _chat_with_role_id(body: ChatRequest, role_id: str) -> ChatResponse:
    role = get_role(role_id)
    system_prompt = role.get("system_prompt") if role else None

    client = get_gemini_client()
    contents = [Content(role=m.role, parts=[Part.from_text(m.content)]) for m in body.messages]
    cfg = _build_config(body.temperature, body.thinking_budget, system_prompt)

    # Fallback si no hay system_instruction:
    if system_prompt and not getattr(cfg, "system_instruction", None):
        contents = _prepend_system_prompt(contents, system_prompt)

    resp = client.models.generate_content(model=body.model, contents=contents, config=cfg)
    return ChatResponse(text=resp.text or "")


def chat_psychology(body: ChatRequest) -> ChatResponse:
    return _chat_with_role_id(body, "psychology")


def chat_motivation(body: ChatRequest) -> ChatResponse:
    return _chat_with_role_id(body, "motivation")
