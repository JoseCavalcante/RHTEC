from app.services.ingest_service import ingest_resume
from app.services.pinecone_service import pinecone_service
from app.schemas.resume_schema import Resume
import time

def test_flow():
    # 1. Ingest
    print("Ingesting candidate...")
    resume = Resume(
        name="John Doe",
        text="Experiente desenvolvedor Python com 5 anos de experiência em Django e Flask. AWS e Docker.",
        skills=["Python", "Django", "Flask", "AWS"],
        seniority="Senior",
        experience_years=5
    )
    try:
        ingest_resume(resume)
        print("Ingestion successful.")
    except Exception as e:
        print(f"Ingestion failed: {e}")
        return

    # Wait for consistency - Pinecone is eventually consistent
    time.sleep(5)

    # 2. Search
    query = "desenvolvedor python"
    print(f"Searching for: '{query}'")
    try:
        results = pinecone_service.search_candidates(query, top_k=5)
        print(f"Found {len(results)} results:")
        for i, res in enumerate(results):
            score = res.get('score', 0)
            metadata = res.get('metadata', {})
            name = metadata.get('name', 'Unknown')
            print(f"{i+1}. {name} - Score: {score:.4f}")
    except Exception as e:
        print(f"Search failed: {e}")

if __name__ == "__main__":
    test_flow()
