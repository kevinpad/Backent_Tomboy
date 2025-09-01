from typing import List, Literal, Optional
from pydantic import BaseModel

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
