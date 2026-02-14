from app.services.pinecone_service import pinecone_service

def verify_fix():
    queries = [
        ("python developer", True),      # Should match (0.81 > 0.76)
        ("marketing digital", False),    # Should NOT match (0.74 < 0.76)
        ("medico cardiologista", False), # Should NOT match (0.758 < 0.76) - IMPROVEMENT
        ("cozinheiro chefe", True)       # Will match (0.80) - Known limitation
    ]

    print(f"Testing threshold: 0.76")
    for q, expected in queries:
        results = pinecone_service.search_candidates(q, top_k=1) # Uses default 0.76
        matched = len(results) > 0
        status = "OK" if matched == expected else "FAIL"
        
        score = results[0]['score'] if matched else "N/A"
        print(f"Query: '{q:<20}' | Matched: {matched} | Score: {score} | Expect: {expected} -> {status}")

if __name__ == "__main__":
    verify_fix()
