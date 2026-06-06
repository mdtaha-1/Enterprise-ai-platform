from fastapi import APIRouter
from pydantic import BaseModel
from app.core.llm import chat

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    response = chat(request.message)
    return ChatResponse(response=response)