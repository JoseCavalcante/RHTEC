
import os
import sys

# Ensure app is in path
sys.path.append(os.getcwd())

from app.services.pinecone_service import pinecone_service

try:
    # Query used by the user in RAG
    query = "Qual candidata na sua opinião se adapta melhor como um engenheiro de IA ?"
    
    print(f"RAG Question: '{query}'")
    
    # Check scores with low threshold to see what WOULD be returned vs what IS returned (0.82)
    results = pinecone_service.search_candidates(query, top_k=10, min_score=0.0)
    
    print(f"Total candidates found (min_score=0.0): {len(results)}")
    
    print("-" * 30)
    print("Candidates and their scores:")
    for c in results:
        meta = c.get('metadata', {})
        name = meta.get('name', 'Unknown')
        score = c.get('score', 0.0)
        
        status = "✅ INCLUDED" if score >= 0.82 else "❌ EXCLUDED (score < 0.82)"
        
        print(f"{name}: {score:.4f} => {status}")
        
except Exception as e:
    print(f"Error: {e}")
