from app.core.embeddings import embed
from app.core.pinecone_client import index
from app.schemas.resume_schema import ResumeMetadata

def ingest_resume(text: str, metadata: ResumeMetadata):

    vector = embed(text)

    index.upsert([
        {
            "id": metadata.candidate_id,
            "values": vector,
            "metadata": metadata.dict()
        }
    ])

print("Resume inserido com sucesso")
