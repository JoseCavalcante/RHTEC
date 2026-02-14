from fastapi import APIRouter, HTTPException
from app.services.rag_service import rag_answer
from app.core.exceptions import AppError

router = APIRouter()

@router.get("/rag", tags=["RAG"])
async def rag(q: str):
    try:
        return {"answer": await rag_answer(q)}
    except AppError as e:
        raise HTTPException(status_code=503, detail=str(e))
