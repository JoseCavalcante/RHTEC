
import os
import sys
import numpy as np
from dotenv import load_dotenv

# Ensure app is in path
sys.path.append(os.getcwd())

from app.core.embeddings import embed
from app.core.pinecone_client import index

try:
    target_name = "Ana Clara Santos"
    
    # 1. Fetch current stored vector
    print(f"Fetching vector for '{target_name}'...")
    # We need the ID. Let's find ID by name again or assume we know it?
    # Better to find it.
    
    # Using a dummy vector to list
    results = index.query(
        vector=[0.0]*1536,
        top_k=100,
        include_metadata=True
    )
    
    candidate = None
    for m in results.matches:
        if m.metadata.get('name') == target_name:
            candidate = m
            break
            
    if not candidate:
        print("Candidate not found in index.")
        sys.exit(1)
        
    stored_vector = candidate.values
    # If values are empty/not returned by query (depends on implementation, sometimes query doesn't return values unless requested? 
    # Pinecone: include_values=True default is False? 
    
    # Let's fetch specifically with ID to get values
    cid = candidate.id
    fetch_res = index.fetch(ids=[cid])
    if cid not in fetch_res.vectors:
        print("Error fetching vector by ID.")
        sys.exit(1)
        
    stored_vector = fetch_res.vectors[cid].values
    text = fetch_res.vectors[cid].metadata.get('text', '')
    
    print(f"Retrieved text: {text[:50]}...")
    
    # 2. Embed the text again
    print("Generating new embedding for text...")
    new_vector = embed(text)
    
    # 3. Compare
    # Cosine similarity
    def cosine_similarity(v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        
    sim = cosine_similarity(stored_vector, new_vector)
    print(f"Similarity between stored and new vector: {sim:.4f}")
    
    if sim > 0.99:
        print("Vectors match! The model thinks this text is irrelevant.")
    else:
        print("Vectors DO NOT match! The stored vector is outdated or corrupted.")
        
except Exception as e:
    print(f"Error: {e}")
