from openai import OpenAI
from app.core.embeddings import embed
from app.core.pinecone_client import index
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def rag_recruiter(question):

    q_vec = embed(question)

    results = index.query(
        vector=q_vec,
        top_k=5,
        include_metadata=True
    )

    context = "\n".join([m.metadata.get("name","") + str(m.metadata.get("skills","")) for m in results.matches])

    prompt = f"""
    Use os candidatos abaixo para responder:

    {context}

    Pergunta:
    {question}
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content
