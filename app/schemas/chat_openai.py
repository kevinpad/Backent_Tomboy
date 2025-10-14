from typing import List, Literal, Optional
from pydantic import BaseModel

Role = Literal["user", "model"]

class Message(BaseModel):
    role: Role
    content: str

class ChatOpenAIRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = None         
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 800
    thinking_budget: Optional[int] = 0  

class ChatOpenAIResponse(BaseModel):
    text: str