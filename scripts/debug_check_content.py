
import logging
import sys
import os
from app.services.pinecone_service import pinecone_service

# Setup logging
logging.basicConfig(level=logging.ERROR)

try:
    print("--- Checking Content of Top Matches ---")
    query = "python developer"
    results = pinecone_service.search_candidates(query, top_k=5)
    
    for i, res in enumerate(results):
        score = res.get('score', 0)
        metadata = res.get('metadata', {})
        name = metadata.get('name', 'Unknown')
        text = metadata.get('text', '')
        skills = metadata.get('skills', [])
        
        print(f"\nResult {i+1}: {name} (Score: {score:.4f})")
        print(f"Skills: {skills}")
        print(f"Text Snippet: {text[:200]}...") # Print first 200 chars

except Exception as e:
    print(f"Error: {e}")
