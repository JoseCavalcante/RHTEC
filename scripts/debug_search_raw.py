
import os
import sys

# Ensure app is in path
sys.path.append(os.getcwd())

from app.core.embeddings import embed
from app.core.pinecone_client import index

try:
    query = "desenvolvedor backend com experiencia em UX"
    vector = embed(query)
    
    print(f"Querying for: '{query}'")
    
    # Raw query to Pinecone
    results = index.query(
        vector=vector,
        top_k=100,
        include_metadata=True
    )
    
    print(f"Total Matches: {len(results.matches)}")
    
    for match in results.matches:
        name = match.metadata.get('name', 'Unknown')
        score = match.score
        print(f"{name}: {score:.4f}")

except Exception as e:
    print(f"Error: {e}")
