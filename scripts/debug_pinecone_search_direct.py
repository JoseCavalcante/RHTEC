
import logging
import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

# Setup logging
logging.basicConfig(level=logging.ERROR)

from app.services.pinecone_service import pinecone_service

try:
    print("Testing pinecone_service.search_candidates()...")
    results = pinecone_service.search_candidates("python developer", top_k=2)
    print(f"Results: {len(results)}")
    for r in results:
        print(r)
except Exception as e:
    print(f"Caught exception type: {type(e)}")
    print(f"Exception message: {e}")
    import traceback
    traceback.print_exc()
