import logging
import sys
import time
from app.services.pinecone_service import pinecone_service

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_crud():
    print("Iniciando verificação manual do CRUD Pinecone...")
    
    # 1. Create (Upsert)
    candidate_id = "test-manual-verification-" + str(int(time.time()))
    text = "Engenheiro de Software Sênior com 10 anos de experiência em Python e AWS."
    metadata = {
        "name": "Teste Manual",
        "skills": ["Python", "AWS", "Docker"],
        "experience_years": 10
    }
    
    print(f"\n[1] Testando Upsert (Create/Update)...")
    try:
        returned_id = pinecone_service.upsert_candidate(text, metadata, candidate_id)
        print(f"✅ Upsert realizado com sucesso. ID: {returned_id}")
    except Exception as e:
        print(f"❌ Erro no Upsert: {e}")
        return

    # Wait for consistency (Pinecone is eventually consistent)
    print("Aguardando 5 segundos para propagação no índice...")
    time.sleep(5)

    # 2. Read (Get)
    print(f"\n[2] Testando Get (Read)...")
    try:
        candidate = pinecone_service.get_candidate(candidate_id)
        if candidate:
            print(f"✅ Candidato recuperado: {candidate['id']}")
            print(f"   Metadata: {candidate['metadata']}")
        else:
            print(f"❌ Candidato não encontrado pelo ID.")
    except Exception as e:
        print(f"❌ Erro no Get: {e}")

    # 3. Search
    print(f"\n[3] Testando Search...")
    query = "desenvolvedor python experiente"
    try:
        results = pinecone_service.search_candidates(query, top_k=3)
        found = False
        print(f"Resultados encontrados: {len(results)}")
        for match in results:
            print(f" - ID: {match.id}, Score: {match.score}")
            if match.id == candidate_id:
                found = True
        
        if found:
            print(f"✅ Candidato de teste encontrado na busca.")
        else:
            print(f"⚠️ Candidato de teste NÃO encontrado na busca (pode ser delay de indexação).")
    except Exception as e:
        print(f"❌ Erro no Search: {e}")

    # 4. Delete
    print(f"\n[4] Testando Delete...")
    try:
        pinecone_service.delete_candidate(candidate_id)
        print(f"✅ Comando de delete enviado.")
    except Exception as e:
        print(f"❌ Erro no Delete: {e}")

    # Verify Delete
    print("Aguardando 2 segundos para verificar delete...")
    time.sleep(2)
    try:
        candidate = pinecone_service.get_candidate(candidate_id)
        if not candidate:
            print(f"✅ Candidato removido com sucesso (não encontrado).")
        else:
            print(f"❌ Candidato ainda existe após delete.")
    except Exception as e:
        print(f"❌ Erro ao verificar delete: {e}")

    print("\nVerificação concluída.")

if __name__ == "__main__":
    verify_crud()
