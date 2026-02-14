from app.services.pinecone_service import pinecone_service
from app.core.domain import format_candidate_text
from app.schemas.resume_schema import Resume

async def ingest_resume(resume: Resume) -> str:
    """
    Processa e insere um currículo no banco vetorial.
    Refatorado para usar lógica de domínio centralizada e chamadas assíncronas.
    """
    # Create rich text using centralized domain logic (DRY)
    rich_text = format_candidate_text(
        name=resume.name,
        seniority=resume.seniority,
        skills=resume.skills,
        summary=resume.text
    )
    
    resume_data = resume.model_dump()
    # Filter out None values
    metadata = {k: v for k, v in resume_data.items() if v is not None}

    # Upsert async
    # Pass candidate_id if it exists in the schema, otherwise pinecone service generates uuid
    return await pinecone_service.upsert_candidate(
        rich_text=rich_text, 
        metadata=metadata, 
        candidate_id=resume.candidate_id
    )
