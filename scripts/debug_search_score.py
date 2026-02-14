
import os
import sys

# Ensure app is in path
sys.path.append(os.getcwd())

from app.services.pinecone_service import pinecone_service

try:
    # Query used by the user
    query = "Desenvolvedora backend com experiencia em UX"
    
    print(f"Searching for: '{query}'")
    
    # We want to see ALL results to check scores, so we lower min_score to 0
    results = pinecone_service.search_candidates(query, top_k=100, min_score=0.0)
    
    print(f"Found {len(results)} candidates.")
    
    for c in results:
        meta = c.get('metadata', {})
        name = meta.get('name', 'Unknown')
        score = c.get('score', 0.0)
        
        # Highlight our target
        prefix = ">>> " if "Ana Clara" in name else "    "
        print(f"{prefix}{name}: {score:.4f}")
        
except Exception as e:
    print(f"Error: {e}")
