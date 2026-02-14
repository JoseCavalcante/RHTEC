from pinecone import Pinecone
from app.core.config import PINECONE_API_KEY, PINECONE_INDEX


print("Initializing Pinecone client (LAZY)...")

_index_instance = None

def get_index():
    global _index_instance
    if _index_instance is None:
        if not PINECONE_API_KEY or PINECONE_API_KEY == "xxxx":
            print("Warning: PINECONE_API_KEY not set or invalid.")
            return None
        try:
            pc = Pinecone(api_key=PINECONE_API_KEY)
            _index_instance = pc.Index(PINECONE_INDEX)
        except Exception as e:
            print(f"Error connecting to Pinecone: {e}")
            return None
    return _index_instance

class LazyIndex:
    def __getattr__(self, name):
        real_index = get_index()
        if real_index is None:
            raise RuntimeError("Pinecone index not available. Check API key.")
        return getattr(real_index, name)

index = LazyIndex()