from app.services.pinecone_service import pinecone_service
import sys

def test_search():
    query = "desenvolvedor python"
    print(f"Searching for: '{query}'")
    try:
        results = pinecone_service.search_candidates(query, top_k=10)
        print(f"Found {len(results)} results:")
        for i, res in enumerate(results):
            score = res.get('score', 0)
            metadata = res.get('metadata', {})
            name = metadata.get('name', 'Unknown')
            print(f"{i+1}. {name} - Score: {score}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
