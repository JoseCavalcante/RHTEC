import structlog
import json
from openai import AsyncOpenAI
from app.core.config import OPENAI_API_KEY
from app.services.search_service import search_candidates
from app.core.exceptions import ServiceUnavailable
from app.core.prompts import RAG_SYSTEM_PROMPT, RAG_USER_PROMPT
from app.services.base import BaseAIService

logger = structlog.get_logger(__name__)

class RagService(BaseAIService):
    def __init__(self):
        super().__init__(model_name=self.LLM_MODEL_DEFAULT)
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def answer(self, question: str) -> str:
        try:
            self.logger.info("rag_request_started", question=question)
            
            # Use a slightly more specific search
            matches = await search_candidates(question, min_score=0.70)

            # Context optimization: filter labels and convert to clean strings
            context_items = []
            for m in matches:
                meta = m.get('metadata', {})
                # Keep only essential fields to reduce noise and tokens
                clean_meta = {
                    "nome": meta.get("name"),
                    "senioridade": meta.get("seniority"),
                    "skills": meta.get("skills"),
                    "experiencia_anos": meta.get("experience_years"),
                    "resumo": meta.get("text")[:1000] # Limit summary length
                }
                context_items.append(json.dumps(clean_meta, ensure_ascii=False))

            context = "\n---\n".join(context_items)
            
            if not context:
                self.logger.info("rag_no_context_found", question=question)
                return "Não encontrei candidatos que correspondam ao perfil solicitado ou informações suficientes para responder."

            system_message = RAG_SYSTEM_PROMPT.format(context=context)
            user_message = RAG_USER_PROMPT.format(question=question)

            self.logger.info("openai_completion_started", context_len=len(context))
            
            # Wrapper call with retry logic
            r = await self.call_with_retry(
                self.client.chat.completions.create,
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2
            )
            
            self.logger.info("openai_completion_finished")
            return r.choices[0].message.content
            
        except Exception as e:
            self.logger.error("rag_error", question=question, error=str(e))
            if isinstance(e, ServiceUnavailable):
                raise
            raise ServiceUnavailable(f"Erro no serviço de RAG: {str(e)}")

# Singleton instance
rag_service = RagService()

async def rag_answer(question: str) -> str:
    """Legacy function wrapper for backward compatibility."""
    return await rag_service.answer(question)
