
import os
import sys
import time

# Ensure app is in path
sys.path.append(os.getcwd())

from app.services.pinecone_service import pinecone_service
from app.core.embeddings import embed

def reindex_all():
    print("Starting re-indexing process...")
    
    # 1. List all candidates
    try:
        # Fetching all candidates (limit 1000 properly)
        candidates = pinecone_service.list_all_candidates(limit=1000)
        print(f"Found {len(candidates)} candidates to re-index.")
        
        for cand in candidates:
            c_id = cand['id']
            meta = cand['metadata']
            
            name = meta.get('name', 'Unknown')
            seniority = meta.get('seniority', 'N/A')
            # Skills might be list or string depending on how it was stored
            skills = meta.get('skills', [])
            if isinstance(skills, str):
                # If stored as string representation of list
                pass 
            
            # Pinecone returns list as list
            if isinstance(skills, list):
                skills_str = ", ".join(skills)
            else:
                skills_str = str(skills)
                
            text = meta.get('text', '')
            
            # Construct Rich Text
            rich_text = f"Name: {name} | Seniority: {seniority} | Skills: {skills_str} | Summary: {text}"
            
            print(f"Re-indexing: {name} ({c_id})...")
            
            # Upsert (this will generate new embedding for rich_text)
            # We use the existing metadata
            pinecone_service.upsert_candidate(rich_text, meta, c_id)
            
            # Sleep briefly to avoid rate limits if necessary
            time.sleep(0.2)
            
        print("Re-indexing complete!")
        
    except Exception as e:
        print(f"Error during re-indexing: {e}")

if __name__ == "__main__":
    reindex_all()
