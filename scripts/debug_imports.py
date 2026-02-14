import sys
import time
import os

print(f"Python executable: {sys.executable}")
sys.path.append(".")

print("Attempting to import app.main...")
start = time.time()
try:
    import app.main
    print(f"Imported app.main in {time.time() - start:.4f}s")
except Exception as e:
    print(f"Failed to import app.main: {e}")

print("Attempting to import app.core.pinecone_client...")
start = time.time()
try:
    import app.core.pinecone_client
    print(f"Imported app.core.pinecone_client in {time.time() - start:.4f}s")
except Exception as e:
    print(f"Failed to import app.core.pinecone_client: {e}")
