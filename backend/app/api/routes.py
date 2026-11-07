from fastapi import APIRouter, Depends

from app.api.dependencies import get_chat_service
from app.api.schemas import ChatRequest, ChatResponse, HistoryResponse, MessageOut
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    result = service.chat(request.message, request.session_id)
    return ChatResponse(session_id=result.session_id, reply=result.reply)


@router.get("/sessions/{session_id}/messages", response_model=HistoryResponse)
def history(session_id: str, service: ChatService = Depends(get_chat_service)) -> HistoryResponse:
    messages = service.get_history(session_id)
    return HistoryResponse(
        session_id=session_id,
        messages=[MessageOut(role=m.role, content=m.content) for m in messages],
    )