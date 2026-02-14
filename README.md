# HR Tech AI Platform

Plataforma de IA voltada para recrutamento e seleção, facilitando a busca e análise de talentos através de técnicas avançadas de RAG (Retrieval-Augmented Generation).

## 🚀 Funcionalidades

- **Busca Semântica (RAG)**: Encontre candidatos com base em competências e perfil, indo além de palavras-chave simples.
- **Gestão de Candidatos**: Cadastro, listagem e detalhamento de perfis profissionais.
- **Extração de Dados**: Processamento automático de currículos em PDF e DOCX usando IA.
- **Análise & Scoring**: Avaliação automatizada de aderência de candidatos a vagas/requisitos.

## 🛠️ Tecnologias

- **Backend**: Python, FastAPI, Uvicorn.
- **Frontend**: Streamlit.
- **Vetorização & Busca**: Pinecone, OpenAI Embeddings.
- **Orquestração de LLM**: LangChain.
- **Containerização**: Docker, Docker Compose.

## ⚙️ Configuração

### Pré-requisitos
- Python 3.10+
- Docker & Docker Compose (opcional para rodar via container)
- Chave de API da OpenAI
- Configurações do Pinecone (API Key, Ambiente, Index)

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto seguindo o modelo:
```env
OPENAI_API_KEY=sua_chave_aqui
PINECONE_API_KEY=sua_chave_aqui
PINECONE_ENVIRONMENT=seu_ambiente_aqui
PINECONE_INDEX_NAME=seu_index_aqui
```

### Instalação Local
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o Backend:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```
3. Execute o Frontend:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

### Rodando com Docker
```bash
docker-compose up --build
```
O frontend estará disponível em `http://localhost:8501` e o backend em `http://localhost:8001`.

## 📁 Estrutura do Projeto

- `app/`: Lógica de backend (FastAPI, Serviços, Schemas).
- `ui/`: Interface do usuário (Streamlit).
- `data/`: Armazenamento temporário de documentos.
- `tests/`: Suíte de testes automatizados.
- `docker-compose.yml`: Configuração da infraestrutura containerizada.
