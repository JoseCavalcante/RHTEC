
import os
import sys

# Ensure app is in path
sys.path.append(os.getcwd())

from app.services.pinecone_service import pinecone_service

try:
    print("Searching for candidate...")
    # Using list_all_candidates to avoid similarity threshold issues if the name is exact
    # but search_candidates is better if we want to match by query
    
    # Let's try to find by metadata filter if possible, or list all
    # Pinecone metadata filtering is precise.
    
    # Option 1: List all (up to 100) and filter in python
    results = pinecone_service.list_all_candidates(limit=100)
    
    target_name = "Ana Clara Santos"
    found = None
    
    for c in results:
        meta = c.get('metadata', {})
        if meta.get('name') == target_name:
            found = c
            break
            
    if found:
        print(f"--- START TEXT ---")
        print(found['metadata'].get('text', 'No text found'))
        print(f"--- END TEXT ---")
    else:
        print(f"Candidate '{target_name}' not found in top 100.")
        
except Exception as e:
    print(f"Error: {e}")
