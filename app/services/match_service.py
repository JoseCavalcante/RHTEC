from app.core.embeddings import embed
from app.core.pinecone_client import index

def search_candidates(job_description: str, top_k=5):

    vector = embed(job_description)

    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )

    return results.matches
