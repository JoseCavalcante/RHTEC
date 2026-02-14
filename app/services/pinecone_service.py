import structlog
import uuid
import asyncio
from functools import partial
from typing import List, Dict, Optional, Any
from app.core.embeddings import embed
from app.core.pinecone_client import index
from app.core.exceptions import ServiceUnavailable
from app.core.domain import format_candidate_text
from app.services.base import BaseAIService

logger = structlog.get_logger(__name__)

class PineconeService(BaseAIService):
    def __init__(self):
        super().__init__()
        self.index = index

    async def _run_async(self, func, *args, **kwargs):
        """Runs a blocking function in a thread pool with retry logic for Pinecone calls."""
        loop = asyncio.get_running_loop()
        # Pinecone calls can also benefit from retries if they are network-bound
        return await self.call_with_retry(
            loop.run_in_executor, None, partial(func, *args, **kwargs)
        )

    async def upsert_candidate(self, rich_text: str, metadata: Optional[Dict[str, Any]] = None, candidate_id: Optional[str] = None) -> str:
        if not candidate_id:
            candidate_id = str(uuid.uuid4())
            
        if metadata is None:
            metadata = {}
            
        try:
            self.logger.info("request_embedding", candidate_id=candidate_id)
            vector = await self._run_async(embed, rich_text)
            
            self.logger.info("pinecone_upsert_started", candidate_id=candidate_id)
            await self._run_async(self.index.upsert, vectors=[(candidate_id, vector, metadata)])
            self.logger.info("pinecone_upsert_finished", candidate_id=candidate_id)
            
            return candidate_id
        except Exception as e:
            self.logger.error("pinecone_upsert_error", candidate_id=candidate_id, error=str(e))
            raise ServiceUnavailable(f"Falha ao comunicar com Pinecone: {str(e)}")

    async def get_candidate(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        try:
            result = await self._run_async(self.index.fetch, ids=[candidate_id])
            if result and result.vectors and candidate_id in result.vectors:
                return result.vectors[candidate_id]
            return None
        except Exception as e:
            self.logger.error("pinecone_fetch_error", candidate_id=candidate_id, error=str(e))
            raise ServiceUnavailable(f"Erro na busca: {str(e)}")

    async def delete_candidate(self, candidate_id: str) -> bool:
        try:
            self.logger.info("pinecone_delete_started", candidate_id=candidate_id)
            await self._run_async(self.index.delete, ids=[candidate_id])
            return True
        except Exception as e:
            self.logger.error("pinecone_delete_error", candidate_id=candidate_id, error=str(e))
            raise ServiceUnavailable(f"Erro ao deletar: {str(e)}")

    async def search_candidates(self, query: str, top_k: int = 5, min_score: float = 0.85, filter_metadata: Optional[Dict] = None) -> List[Any]:
        try:
            vector = await self._run_async(embed, query)
            params = {
                "vector": vector,
                "top_k": top_k,
                "include_metadata": True
            }
            if filter_metadata:
                params["filter"] = filter_metadata
                
            results = await self._run_async(self.index.query, **params)
            
            matches = []
            for match in results.matches:
                if match.score >= min_score:
                    matches.append(match.to_dict())
                    
            self.logger.info("pinecone_query_finished", query=query, results_count=len(matches))
            return matches
        except Exception as e:
            self.logger.error("pinecone_query_error", query=query, error=str(e))
            raise ServiceUnavailable(f"Erro na busca: {str(e)}")

    async def list_all_candidates(self, limit: int = 100) -> List[Any]:
        try:
            dummy_vector = [0.0] * self.EMBEDDING_DIMENSION 
            params = {
                "vector": dummy_vector,
                "top_k": limit,
                "include_metadata": True
            }
            results = await self._run_async(self.index.query, **params)
            return [match.to_dict() for match in results.matches]
        except Exception as e:
            self.logger.error("pinecone_list_error", error=str(e))
            raise ServiceUnavailable(f"Erro ao listar: {str(e)}")
            
pinecone_service = PineconeService()
