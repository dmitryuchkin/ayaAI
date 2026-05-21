import uuid
from fastapi import FastAPI, HTTPException, status
from routers.users import router as users_router
from ai.prompt_improver import improve_prompt, suggestions_prompt
from schemas.chat import ChatRequest, ChatResponse

app = FastAPI()
app.include_router(users_router)

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    if not request.messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message empty"
        )
    last_message = request.messages[-1].content
    try:
        result = await improve_prompt(last_message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = 'Interna server error'
        )

    suggestions = await suggestions_prompt(result)

    return ChatResponse(
        id=str(uuid.uuid4()),
        content=result,
        model=request.model,
        suggestions = suggestions,
        usage={"total_tokens": 100}
    )
