import uuid
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from ai.prompt_improver import improve_prompt, suggestions_prompt
from schemas.chat import ChatRequest, ChatResponse

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    if not request.messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message empty"
        )
    last_message = request.messages[-1].content
    result = await improve_prompt(last_message)

    suggestions = await suggestions_prompt(result)
    suggestions_list = [s.strip() for s in suggestions.split('\n') if s.strip()]

    return ChatResponse(
        id=str(uuid.uuid4()),
        content=result,
        model=request.model,
        suggestions = suggestions_list,
        usage={"total_tokens": 100}
    )
