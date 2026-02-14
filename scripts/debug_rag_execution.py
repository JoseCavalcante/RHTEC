
import os
import sys
import traceback

# Ensure app is in path
sys.path.append(os.getcwd())

from app.services.rag_service import rag_answer

try:
    question = "Qual candidata na sua opinião se adapta melhor como um engenheiro de IA ?"
    print(f"Testing RAG with question: '{question}'")
    
    answer = rag_answer(question)
    
    print("\n--- RAG Response ---")
    print(answer)
    print("--------------------")
    
except Exception:
    print("\n--- RAG FAILED ---")
    traceback.print_exc()
