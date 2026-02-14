from openai import OpenAI
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def explain_match(job, resume):

    prompt = f"""
    Explique por que este candidato combina com a vaga.

    VAGA:
    {job}

    CURRÍCULO:
    {resume}

    Gere:
    - Pontos fortes
    - Pontos fracos
    - Skills compatíveis
    - Avaliação final
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content
