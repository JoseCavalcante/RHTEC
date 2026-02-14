import structlog
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import openai
from app.core.exceptions import ServiceUnavailable

from app.core import config

logger = structlog.get_logger(__name__)

class BaseAIService:
    """
    Base class for all AI services.
    Provides common retry logic and telemetry.
    """
    
    # Centralized Configuration from config.py
    LLM_MODEL_DEFAULT = config.LLM_MODEL_DEFAULT
    EXTRACTION_MODEL_DEFAULT = config.EXTRACTION_MODEL_DEFAULT
    EMBEDDING_DIMENSION = config.EMBEDDING_DIMENSION

    def __init__(self, model_name: str = config.LLM_MODEL_DEFAULT):
        self.model_name = model_name
        self.logger = logger.bind(service=self.__class__.__name__, model=self.model_name)

    @staticmethod
    def _log_before_sleep(retry_state):
        logger.info(
            "ai_service_retry",
            attempt=retry_state.attempt_number,
            wait=retry_state.next_action.sleep,
            exception=str(retry_state.outcome.exception())
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((
            openai.RateLimitError,
            openai.APIConnectionError,
            openai.APITimeoutError,
            openai.InternalServerError
        )),
        before_sleep=_log_before_sleep,
        reraise=True
    )

    async def call_with_retry(self, func, *args, **kwargs):
        """
        Executes an LLM or external service call with exponential backoff.
        """
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            self.logger.error("ai_service_call_failed", error=str(e))
            raise
