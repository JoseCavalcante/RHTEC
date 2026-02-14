from fastapi import APIRouter
from app.scoring.fit_score import fit_score
from app.explain.match_explainer import explain_match
from app.rag.rag_service import rag_recruiter

router = APIRouter()

@router.post("/fit-score")
def score(job: str, resume: str):
    return {"fit_score": fit_score(job, resume)}

@router.post("/explain")
def explain(job: str, resume: str):
    return {"explanation": explain_match(job, resume)}

@router.post("/rag")
def rag(question: str):
    return {"answer": rag_recruiter(question)}
