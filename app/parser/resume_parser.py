from openai import OpenAI
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_resume(text: str):
    prompt = f"Extraia nome, skills, senioridade e anos de experiência:\n{text}"
    r = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )
    return r.choices[0].message.content
