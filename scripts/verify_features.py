from app.services.pinecone_service import pinecone_service
from app.services.ingest_service import ingest_resume
from app.schemas.resume_schema import Resume
import time

def verify_features():
    print("--- Verifying Candidate Listing ---")
    try:
        candidates = pinecone_service.list_all_candidates()
        print(f"Candidates found: {len(candidates)}")
        for i, c in enumerate(candidates):
             meta = c.get('metadata', {})
             print(f"{i+1}. {meta.get('name', 'Unknown')} (ID: {c.get('id')})")
             print(f"   Text: {meta.get('text', '')[:100]}...")
             print(f"   Skills: {meta.get('skills', [])}")
    except Exception as e:
        print(f" Listing failed: {e}")

    print("\n--- Verifying Search Score Filtering ---")
    # Query that should match
    query_match = "python"
    print(f"Searching for '{query_match}' (min_score=0.7)")
    results_match = pinecone_service.search_candidates(query_match, min_score=0.7)
    print(f"Matches found: {len(results_match)}")
    for res in results_match:
        print(f" - {res['metadata'].get('name')}: {res['score']}")

    # Query that should NOT match (irrelevant)
    query_no_match = "cozinheiro chefe" 
    print(f"\nSearching for '{query_no_match}' (min_score=0.7)")
    results_no_match = pinecone_service.search_candidates(query_no_match, min_score=0.7)
    print(f"Matches found: {len(results_no_match)}")
    if len(results_no_match) == 0:
        print("SUCCESS: Irrelevant results filtered out.")
    else:
        print("FAILURE: Irrelevant results returned.")
        for res in results_no_match:
             print(f" - {res['metadata'].get('name')}: {res['score']}")

if __name__ == "__main__":
    verify_features()
