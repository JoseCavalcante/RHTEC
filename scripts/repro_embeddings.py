import sys
import os

# Ensure we can import app
sys.path.append(".")

print("Attempting to import app.core.embeddings...")
try:
    from app.core.embeddings import embed
    print("Import successful.")
    try:
        # Try to use it (will fail if client init failed with empty key, or if embed fails)
        # Actually client init with None key might not fail immediately until request is made,
        # unless OpenAI client validation checks it.
        # Let's check if client.api_key is set.
        from app.core.embeddings import client
        if not client.api_key:
             print("FAILURE: client.api_key is empty/None")
        else:
             print(f"SUCCESS: client.api_key is set (len={len(client.api_key)})")
    except Exception as e:
        print(f"FAILURE during usage check: {e}")

except Exception as e:
    print(f"FAILURE during import: {e}")
