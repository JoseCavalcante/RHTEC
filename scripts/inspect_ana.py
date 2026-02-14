from app.services.pinecone_service import pinecone_service

def inspect_ana():
    # ID from previous output
    ana_id = "54b86495-df3e-4a36-8a64-045a7a4279cb" 
    
    print(f"Fetching vector for ID: {ana_id}")
    try:
        # We need to access the underlying index to fetch vectors directly
        # The service exposes 'get_candidate' which returns the vector dict
        vector_data = pinecone_service.get_candidate(ana_id)
        
        if vector_data:
            vec = vector_data.get('values', [])
            meta = vector_data.get('metadata', {})
            print(f"Found candidate: {meta.get('name')}")
            print(f"Vector length: {len(vec)}")
            print(f"First 5 dimensions: {vec[:5]}")
            
            # Check for zeros
            zeros = [x for x in vec if x == 0.0]
            print(f"Number of exact zeros in vector: {len(zeros)}")
        else:
            print("Candidate not found in index.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_ana()
