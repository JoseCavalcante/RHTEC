
import sys
import os
from dotenv import load_dotenv

# Load env from root
load_dotenv()

try:
    from app.services.index_service import list_index
    
    print(f"Checking configured index: {os.getenv('PINECONE_INDEX')}")
    indexes = list_index()
    print(f"Available indexes: {indexes}")
    
    configured_index = os.getenv('PINECONE_INDEX')
    
    # Check if configured index is in the list
    # The response structure depends on SDK version, let's handle it
    index_names = []
    if hasattr(indexes, 'names'):
        index_names = indexes.names()
    elif isinstance(indexes, list):
        # Could be a list of strings or objects
        if indexes and hasattr(indexes[0], 'name'):
            index_names = [i.name for i in indexes]
        else:
            index_names = indexes
    elif isinstance(indexes, dict) and 'indexes' in indexes:
         # New API format sometimes returns dict with 'indexes' key
         index_names = [i['name'] for i in indexes['indexes']]

    print(f"Index names found: {index_names}")
    
    if configured_index not in index_names:
        print(f"❌ Configured index '{configured_index}' NOT found in Pinecone.")
    else:
        print(f"✅ Configured index '{configured_index}' found.")
        
except Exception as e:
    print(f"Error checking indexes: {e}")
