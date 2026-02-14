import time
import uuid
import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        
        # Add request_id to contextvars so it's included in all logs for this request
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)
        
        start_time = time.perf_counter()
        
        logger.info(
            "request_started",
            path=request.url.path,
            method=request.method,
        )
        
        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            
            logger.info(
                "request_finished",
                path=request.url.path,
                method=request.method,
                status_code=response.status_code,
                duration=f"{process_time:.4f}s",
            )
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            process_time = time.perf_counter() - start_time
            logger.error(
                "request_failed",
                path=request.url.path,
                method=request.method,
                error=str(e),
                duration=f"{process_time:.4f}s",
            )
            raise
