from typing import Optional
from langchain_openai import ChatOpenAI
from app.schemas.resume_schema import Resume
from app.core.config import OPENAI_API_KEY
from app.services.base import BaseAIService
import structlog

logger = structlog.get_logger(__name__)

class ExtractionService(BaseAIService):
    def __init__(self):
        super().__init__(model_name=self.EXTRACTION_MODEL_DEFAULT)
        self.llm = ChatOpenAI(
            model=self.model_name, 
            temperature=0, 
            openai_api_key=OPENAI_API_KEY
        )

    async def extract(self, text: str) -> Optional[Resume]:
        """
        Extracts structured professional data from a raw resume text using LLM.
        """
        try:
            if not text or len(text) < 10:
                return None

            self.logger.info("extraction_started", text_len=len(text))
            
            # Direct generation with structured output using LangChain
            structured_llm = self.llm.with_structured_output(Resume)
            
            # Use the retry wrapper from BaseAIService
            result = await self.call_with_retry(
                structured_llm.ainvoke,
                f"Extract professional information from this resume text. Be precise and thorough:\n\n{text}"
            )
            
            self.logger.info("extraction_finished")
            return result

        except Exception as e:
            self.logger.error("extraction_failed", error=str(e))
            return None

# Singleton instance
extraction_service = ExtractionService()

async def extract_resume_data(text: str) -> Optional[Resume]:
    """Legacy function wrapper for backward compatibility."""
    return await extraction_service.extract(text)
