from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="Кто говорит user/assistant/system")
    content: str = Field(..., description="Сообщение")

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = Field(default="gpt-3.5-turbo", description="Модель")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Креативность (0-2)")
    max_tokens: Optional[int] = Field(default=None, description="Максимум токенов")

class ChatResponse(BaseModel):
    id: str
    content: str
    model: str
    suggestions: List[str]
    usage: dict
