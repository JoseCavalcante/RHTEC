from app.services.pinecone_service import pinecone_service
from app.services.ingest_service import ingest_resume
from app.schemas.resume_schema import Resume
import time

def test_distribution():
    print("--- Score Distribution Test ---")
    
    # Ensure we have our test candidate
    try:
        candidates = pinecone_service.list_all_candidates()
        print(f"Index contains {len(candidates)} candidates.")
    except:
        pass

    queries = [
        "python developer",       # Should be high
        "software engineer",      # Should be high
        "java developer",         # Should be medium-high?
        "cozinheiro chefe",       # Should be low
        "marketing digital",      # Should be low
        "motorista de caminhao",  # Should be low
        "medico cardiologista"    # Should be low
    ]

    print(f"\n{'Query':<25} | {'Match Name':<20} | {'Score':<10}")
    print("-" * 60)

    for q in queries:
        # Search WITHOUT filter to see raw scores
        results = pinecone_service.search_candidates(q, top_k=1, min_score=0.0) 
        if results:
            best = results[0]
            name = best['metadata'].get('name', 'Unknown')
            score = best['score']
            print(f"{q:<25} | {name:<20} | {score:.4f}")
        else:
            print(f"{q:<25} | {'No results':<20} | {'N/A':<10}")

if __name__ == "__main__":
    test_distribution()
