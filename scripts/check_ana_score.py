from app.services.pinecone_service import pinecone_service

def check_ana():
    query = "python"
    print(f"Searching for '{query}' (no threshold)...")
    results = pinecone_service.search_candidates(query, top_k=5, min_score=0.0)
    
    for res in results:
        name = res['metadata'].get('name', 'Unknown')
        score = res['score']
        print(f" - {name}: {score:.4f}")

if __name__ == "__main__":
    check_ana()
