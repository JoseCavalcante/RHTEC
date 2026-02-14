from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.pinecone_service import pinecone_service
from app.services.search_service import search_candidates
from app.schemas.resume_schema import UpdateResume
from app.core.exceptions import AppError
from app.core.domain import format_candidate_text

router = APIRouter()

@router.get("/search", tags=["Candidates"])
async def search(q: str, min_score: float = 0.85) -> List[Dict[str, Any]]:
    """
    Search for candidates based on a natural language query.
    """
    try:
        return await search_candidates(q, min_score=min_score)
    except AppError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/candidates", tags=["Candidates"])
async def get_candidates() -> List[Dict[str, Any]]:
    """
    List all candidates currently indexed in the system.
    """
    try:
        return await pinecone_service.list_all_candidates()
    except AppError as e:
         raise HTTPException(status_code=500, detail=str(e))

@router.delete("/candidates/{candidate_id}", tags=["Candidates"])
async def delete_candidate(candidate_id: str) -> Dict[str, str]:
    """
    Remove a candidate from the index by their ID.
    """
    try:
        return await pinecone_service.delete_candidate(candidate_id)
    except AppError as e:
         raise HTTPException(status_code=500, detail=str(e))

@router.put("/candidates/{candidate_id}", tags=["Candidates"])
async def update_candidate(candidate_id: str, resume: UpdateResume) -> Dict[str, Any]:
    """
    Update an existing candidate's information and re-index.
    """
    try:
        # Prepare metadata for update
        metadata = {
            "name": resume.name,
            "skills": resume.skills,
            "seniority": resume.seniority,
            "experience_years": resume.experience_years,
            "text": resume.text
        }
        
        # Use Centralized Domain Logic to format the text representation
        rich_text = format_candidate_text(
            name=resume.name,
            seniority=resume.seniority,
            skills=resume.skills,
            summary=resume.text
        )

        return await pinecone_service.upsert_candidate(rich_text, metadata, candidate_id)
    except AppError as e:
         raise HTTPException(status_code=500, detail=str(e))
