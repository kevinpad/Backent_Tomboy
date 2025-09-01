from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_psychology, chat_motivation

router = APIRouter(tags=["chat"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/chat/psychology", response_model=ChatResponse)
def chat_psychology_endpoint(body: ChatRequest):
    try:
        return chat_psychology(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/motivation", response_model=ChatResponse)
def chat_motivation_endpoint(body: ChatRequest):
    try:
        return chat_motivation(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
