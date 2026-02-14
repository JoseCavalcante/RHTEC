import asyncio
import structlog
from app.services.ingest_service import ingest_resume
from app.services.search_service import search_candidates
from app.services.rag_service import rag_answer
from app.schemas.resume_schema import Resume
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()
logger = structlog.get_logger()

async def smoke_test():
    logger.info("Starting Async Smoke Test...")
    
    # 1. Test Ingestion
    test_resume = Resume(
        name="Candidato de Teste",
        skills=["Python", "FastAPI", "AsyncIO"],
        seniority="Sênior",
        experience_years=10,
        text="Desenvolvedor com vasta experiência em sistemas assíncronos e arquitetura distribuída.",
        candidate_id="smoke-test-id-001"
    )
    
    try:
        logger.info("Testing Ingestion...")
        await ingest_resume(test_resume)
        logger.info("Ingestion successful.")
        
        # 2. Test Search
        logger.info("Testing Search...")
        results = await search_candidates("Desenvolvedor FastAPI Sênior")
        logger.info("Search finished", total_results=len(results))
        
        if results:
            logger.info("First result", name=results[0]['metadata'].get('name'))
        
        # 3. Test RAG
        logger.info("Testing RAG Query...")
        answer = await rag_answer("Quais os diferenciais do candidato de teste?")
        logger.info("RAG Answer Received:")
        print(f"\n{answer}\n")
        
        logger.info("Smoke Test Completed Successfully! 🚀")
        
    except Exception as e:
        logger.error("Smoke Test Failed", error=str(e))

if __name__ == "__main__":
    asyncio.run(smoke_test())
