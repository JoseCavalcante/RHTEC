
import logging
import sys
import os
import json
from datetime import date, datetime

# Ensure project root is in path
sys.path.append(os.getcwd())

# Setup logging
logging.basicConfig(level=logging.ERROR)

from app.services.pinecone_service import pinecone_service

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

try:
    print("Testing serialization of search results...")
    results = pinecone_service.search_candidates("python developer", top_k=1)
    if results:
        first = results[0]
        print(f"Type of first result: {type(first)}")
        print(f"First result content: {first}")
        
        # Try to serialize
        try:
            serialized = json.dumps(first, cls=CustomEncoder)
            print("Serialization successful!")
        except TypeError as e:
            print(f"Serialization failed: {e}")
            
            # Check if it has to_dict
            if hasattr(first, 'to_dict'):
                print("Object has to_dict method.")
                print(f"to_dict result: {first.to_dict()}")
            else:
                print("Object does NOT have to_dict method.")
    else:
        print("No results found.")

except Exception as e:
    print(f"Caught exception: {e}")
    import traceback
    traceback.print_exc()
