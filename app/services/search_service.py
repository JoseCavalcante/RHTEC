from typing import List, Dict, Any
from app.services.pinecone_service import pinecone_service

async def search_candidates(query: str, min_score: float = 0.85) -> List[Dict[str, Any]]:
    """
    Search for candidates using semantic similarity via Pinecone.

    Args:
        query: The search query string (e.g., job description or profile).
        min_score: The minimum similarity score threshold (default 0.82).

    Returns:
        A list of candidate dictionaries with metadata and similarity scores.
    """
    return await pinecone_service.search_candidates(query, min_score=min_score)
