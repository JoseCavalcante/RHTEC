from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routers import candidates, resumes, rag, indexes
from app.core.logging_config import setup_logging
from app.core.middleware import LoggingMiddleware
from app.core.exceptions import AppError
import structlog

logger = structlog.get_logger(__name__)

# Initialize Structured Logging
setup_logging()

app = FastAPI(title="HR Tech AI")

# Add Middleware
app.add_middleware(LoggingMiddleware)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.error("app_error_occurred", error=str(exc), type=exc.__class__.__name__)
    status_code = getattr(exc, "status_code", 400)
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc), "type": exc.__class__.__name__}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro interno no servidor.", "type": "InternalServerError"}
    )

@app.get("/")
def health():
    return {"status":"running"}

app.include_router(candidates.router)
app.include_router(resumes.router)
app.include_router(rag.router)
app.include_router(indexes.router)