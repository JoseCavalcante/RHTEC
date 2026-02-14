
import logging
import sys
import os
from app.services.pinecone_service import pinecone_service
from app.core.pinecone_client import index

# Setup logging
logging.basicConfig(level=logging.INFO)

try:
    # 1. Get Index Stats
    print("--- Index Statistics ---")
    stats = index.describe_index_stats()
    print(stats)
    
    total_vectors = stats.get('total_vector_count', 0)
    print(f"Total vectors in index: {total_vectors}")

    # 2. Run a Search
    query = "python developer"
    print(f"\n--- Searching for: '{query}' ---")
    results = pinecone_service.search_candidates(query, top_k=10)
    
    print(f"Returned {len(results)} results.")
    for i, res in enumerate(results):
        # res is a dict now (from my previous fix) or object depending on import execution context (reloaded?)
        # My previous fix changed it to dict.
        
        score = res.get('score', 0)
        metadata = res.get('metadata', {})
        name = metadata.get('name', 'Unknown')
        print(f"{i+1}. {name} - Score: {score:.4f}")

except Exception as e:
    print(f"Error: {e}")
