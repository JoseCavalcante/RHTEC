from app.core.pinecone_client import get_index

def check_stats():
    index = get_index()
    if index:
        try:
            stats = index.describe_index_stats()
            print("Index Stats:")
            print(stats)
        except Exception as e:
            print(f"Error describing index: {e}")

if __name__ == "__main__":
    check_stats()
