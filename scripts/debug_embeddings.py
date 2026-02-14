from app.core.embeddings import embed
import numpy as np

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def debug_sim():
    text_cv = "Experiente desenvolvedor Python com 5 anos de experiência em Django e Flask. AWS e Docker."
    text_q1 = "python"
    text_q2 = "cozinheiro chefe"

    print(f"Embedding CV text: '{text_cv}'")
    v_cv = embed(text_cv)
    
    print(f"Embedding Q1: '{text_q1}'")
    v_q1 = embed(text_q1)

    print(f"Embedding Q2: '{text_q2}'")
    v_q2 = embed(text_q2)

    sim_q1 = cosine_similarity(v_cv, v_q1)
    sim_q2 = cosine_similarity(v_cv, v_q2)

    print(f"\nSimilarity CV vs '{text_q1}': {sim_q1:.4f}")
    print(f"Similarity CV vs '{text_q2}': {sim_q2:.4f}")

    print("\n--- Testing text-embedding-3-small ---")
    
    # We need to manually call the client with the new model
    from app.core.embeddings import client
    
    def embed_v3(text):
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    v_cv_3 = embed_v3(text_cv)
    v_q1_3 = embed_v3(text_q1)
    v_q2_3 = embed_v3(text_q2)

    sim_q1_3 = cosine_similarity(v_cv_3, v_q1_3)
    sim_q2_3 = cosine_similarity(v_cv_3, v_q2_3)

    print(f"Similarity CV vs '{text_q1}': {sim_q1_3:.4f}")
    print(f"Similarity CV vs '{text_q2}': {sim_q2_3:.4f}")
    
    if sim_q1_3 > sim_q2_3:
        print("BETTER: 'python' score > 'cozinheiro chefe' score")
    else:
        print("WORSE: 'python' score <= 'cozinheiro chefe' score")

if __name__ == "__main__":
    debug_sim()
