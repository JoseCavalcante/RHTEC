# Arquitetura do Sistema - HR Tech AI Platform

Este documento descreve a arquitetura técnica, os componentes principais e os fluxos de dados da plataforma HR Tech AI.

## 🏗️ Visão Geral

A plataforma segue uma arquitetura cliente-servidor moderna, separando a interface do usuário (Frontend) da lógica de negócios e processamento de IA (Backend).

```mermaid
graph TD
    User((Usuário))
    FE[Frontend - Streamlit]
    BE[Backend - FastAPI]
    VDB[(Vector DB - Pinecone)]
    LLM[AI Engine - OpenAI]
    FILE[Storage - Local/Volume]

    User --> FE
    FE --> BE
    BE --> VDB
    BE --> LLM
    BE --> FILE
```

## 🧩 Componentes Principais

### 1. Frontend (Streamlit)
- Localizado em `ui/`.
- Responsável pela renderização da interface, captura de inputs do usuário e exibição de resultados.
- Comunica-se com o backend via `ui/api_client.py`.

### 2. Backend (FastAPI)
- Localizado em `app/`.
- **API Layer**: Define os endpoints REST (`app/api/routers/`).
- **Core Layer**: Configurações, exceções, middleware e logs (`app/core/`).
- **Service Layer**: Lógica de negócio e orquestração (`app/services/`).

### 3. Vetorização & Busca (Pinecone)
- Armazena as representações vetoriais (embeddings) dos currículos.
- Permite a busca por similaridade semântica.

### 4. Orquestração de IA (LangChain & OpenAI)
- Orquestra chamadas LLM para extração de dados e geração de respostas (RAG).

## 🔄 Fluxos de Dados

### Fluxo de RAG (Busca e Resposta)

```mermaid
sequenceDiagram
    participant U as Usuário
    participant FE as Frontend
    participant BE as Backend
    participant SD as Search Service
    participant PC as Pinecone
    participant AI as OpenAI

    U->>FE: Faz uma pergunta profissional
    FE->>BE: POST /rag/answer
    BE->>SD: Pesquisa candidatos relevantes
    SD->>PC: Query por similaridade (Embeddings)
    PC-->>SD: Retorna Top K Matches (Metadata)
    SD-->>BE: Retorna Contexto Consolidado
    BE->>AI: Envia Prompt (Contexto + Pergunta)
    AI-->>BE: Retorna Resposta Gerada
    BE-->>FE: Retorna Resposta Formatada
    FE-->>U: Exibe resposta na UI
```

### Fluxo de Ingestão de Documentos

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant BE as Backend
    participant EX as Extraction Service
    participant IN as Ingest Service
    participant PC as Pinecone

    FE->>BE: Upload de PDF/DOCX
    BE->>EX: Extrai Texto (IA/OCR)
    EX-->>BE: Retorna Dados Estruturados
    BE->>IN: Inicia Ingestão
    IN->>PC: Adiciona/Atualiza Vetores e Metadados
    PC-->>IN: OK
    IN-->>BE: Confirmação
    BE-->>FE: Feedback de Sucesso
```

## 🛡️ Padrões de Design & Resiliência

- **AI Resilience**: Implementação de retries automáticos com backoff exponencial para chamadas de API externas via `BaseAIService`.
- **Singleton Services**: Instâncias globais de serviços para persistência de estado e eficiência de recursos.
- **Structured Logging**: Uso de `structlog` para rastreabilidade de requisições e diagnósticos precisos.
- **Middleware**: Interceptação de requisições para logs de performance (Middleware de Logging).

## 🗄️ Gerenciamento de Dados

- **Documentos**: Localizados temporariamente em `data/` para processamento.
- **Metadados**: Persistidos no Pinecone junto aos vetores para facilitar a filtragem durante a busca.
