from app.services.authenticationsService import authentication_pinecone
from pinecone import ServerlessSpec


try:
    pc = authentication_pinecone()
except RuntimeError as e:
    print(f"Warning: {e}")
    pc = None

def create_index(nameBD: str):
    if not pc:
        return "Erro: Cliente Pinecone não inicializado."
        
    try:
        existing_indexes = pc.list_indexes().names()
    except Exception:
        # Fallback for older SDK versions or different response structure
        existing_indexes = [i.name for i in pc.list_indexes()]

    if nameBD not in existing_indexes:
        try:
            pc.create_index(
                name=nameBD,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            return f"Índice '{nameBD}' criado com sucesso."
        except Exception as e:
            print(f"Erro ao criar o índice: {e}")
            return f"Erro ao criar índice: {e}"
    else:
        print(f"O índice '{nameBD}' já existe.")
        return f"O índice '{nameBD}' já existe."

def list_index():
    if not pc: return {}
    response = pc.list_indexes()
    # Normalize response to dict if it's an object
    if hasattr(response, 'to_dict'):
        return response.to_dict()
    return response

def detail_index(nameIDX: str):
    if not pc: return {}
    try:
        response = pc.describe_index(name=nameIDX)
        if hasattr(response, 'to_dict'):
            return response.to_dict()
        return response
    except Exception as e:
        return f"Erro ao detalhar índice: {e}"