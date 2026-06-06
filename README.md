# EnterpriseAI Platform

A self-hosted, multi-modal AI backend platform built for enterprise document intelligence, autonomous agents, and LLM inference — all behind a secured API gateway.

![Platform UI](static/preview.png)

---

## Overview

Most companies want internal AI tools — document search, intelligent assistants, automated reasoning — but can't afford cloud API costs at scale or don't want sensitive data leaving their servers. EnterpriseAI Platform provides a production-grade, self-hostable alternative built entirely on open-source models and frameworks.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    EnterpriseAI Platform                 │
├─────────────────────────────────────────────────────────┤
│  Frontend UI          FastAPI + Static Files             │
├──────────────┬──────────────┬──────────────┬────────────┤
│  LLM Layer   │  RAG Layer   │  Agent Layer │  Auth Layer│
│  Groq API    │  ChromaDB    │  LangGraph   │  API Keys  │
│  Llama 3.3   │  MiniLM-L6   │  ReAct       │  Header    │
├──────────────┴──────────────┴──────────────┴────────────┤
│                     Python Backend                       │
└─────────────────────────────────────────────────────────┘
```

---

## Features

**Layer 1 — LLM Inference**

- Llama 3.3 70B via Groq API for fast, low-latency inference
- Configurable system prompts per endpoint
- REST API with structured JSON responses

**Layer 2 — RAG Pipeline**

- PDF ingestion with automatic chunking (500-char windows)
- Vector embeddings via `sentence-transformers/all-MiniLM-L6-v2`
- ChromaDB persistent vector store
- Context-aware Q&A: LLM answers only from document context

**Layer 3 — AI Agents**

- Multi-tool autonomous agent built with LangGraph (ReAct pattern)
- Tools: `search_documents`, `calculate`, `summarize_topic`
- Agent decides which tools to use and chains them automatically
- Single natural language input → multi-step reasoning output

**Layer 4 — Image Generation**

- Architecture ready for Stable Diffusion / DALL-E / Replicate integration
- Swap in any image provider via single file change

**Layer 5 — Fine-tuning**

- Custom model fine-tuning on Google Colab using Unsloth
- Domain-specific LLM adaptation workflow

**Layer 6 — API Gateway & Auth**

- API key authentication on all protected routes
- `X-API-Key` header validation
- 401/403 responses for unauthorized access
- Multi-key support with role mapping

---

## Tech Stack

| Layer           | Technology                               |
| --------------- | ---------------------------------------- |
| Backend         | Python, FastAPI, Uvicorn                 |
| LLM Inference   | Groq API, Llama 3.3 70B                  |
| Vector Database | ChromaDB                                 |
| Embeddings      | Sentence Transformers (all-MiniLM-L6-v2) |
| Agent Framework | LangGraph, LangChain                     |
| PDF Processing  | PyPDF                                    |
| Authentication  | FastAPI Security, API Key Header         |
| Frontend        | Vanilla HTML/CSS/JS (IBM Plex fonts)     |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/mdtaha-1/enterprise-ai-platform
cd enterprise-ai-platform

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install fastapi uvicorn python-dotenv python-multipart groq==0.30.0 \
    langchain-groq langchain langchain-community chromadb \
    sentence-transformers pypdf langgraph aiofiles Pillow
```

### Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
PLATFORM_API_KEY=your_chosen_api_key_here
HF_TOKEN=your_huggingface_token_here
```

### Running

```bash
uvicorn main:app --reload
```

- **API Docs**: http://127.0.0.1:8000/docs
- **Platform UI**: http://127.0.0.1:8000/ui

---

## API Reference

All endpoints require `X-API-Key` header.

### LLM Chat

```http
POST /api/v1/chat
Content-Type: application/json
X-API-Key: your_key

{ "message": "Explain transformer architecture" }
```

### RAG — Upload Document

```http
POST /api/v1/rag/upload
Content-Type: multipart/form-data
X-API-Key: your_key

file: document.pdf
```

### RAG — Query Documents

```http
POST /api/v1/rag/query
Content-Type: application/json
X-API-Key: your_key

{ "question": "What are the key terms in this contract?" }
```

### AI Agent

```http
POST /api/v1/agent/run
Content-Type: application/json
X-API-Key: your_key

{ "message": "Search my documents for payment terms and calculate 15% of the stated amount" }
```

---

## Project Structure

```
enterprise-ai-platform/
├── main.py                 # FastAPI app entry point
├── .env                    # API keys (not committed)
├── requirements.txt        # Python dependencies
├── static/
│   └── index.html          # Frontend UI
├── app/
│   ├── api/
│   │   ├── chat.py         # LLM chat endpoint
│   │   ├── rag.py          # RAG upload + query endpoints
│   │   ├── agent.py        # AI agent endpoint
│   │   └── image.py        # Image generation endpoint
│   ├── core/
│   │   ├── llm.py          # Groq LLM client
│   │   └── auth.py         # API key authentication
│   ├── rag/
│   │   └── pipeline.py     # PDF ingestion + vector search
│   ├── agents/
│   │   └── agent.py        # LangGraph ReAct agent
│   └── image/
│       └── generator.py    # Image generation module
└── data/
    ├── chroma/             # ChromaDB vector store (auto-generated)
    └── images/             # Generated images (auto-generated)
```

---

## Roadmap

- [ ] Multi-user support with JWT authentication
- [ ] Document management (list, delete, update)
- [ ] Streaming LLM responses via Server-Sent Events
- [ ] Image generation with Replicate API
- [ ] Fine-tuned model serving via vLLM
- [ ] Docker containerization
- [ ] Kubernetes deployment manifests

---

## Certificates & Learning

This project was built applying knowledge from the **AMD AI Academy** program:

- AI Agents 101: Building AI Agents with MCP and Open-Source Inference
- AI Agents 201: Design to Deployment — Multi-Agent Systems
- Introduction to AI Agents
- Introduction to RAG
- LLM Serving Inference with vLLM and MI300X GPUs
- GPU Optimization for LLM Inference
- Reinforcement Learning with Large Language Models
- Finetuning Your Own R1 Reasoning Model on Unsloth
- Diffusion Models: From Prompts to Images and Video
- Hugging Face on AMD
- Introduction to Quantization
- Introduction to LLM Architectures and AMD AI Models
- AI on AMD
- Introduction to AI on AMD AI PC

---

## Author

**Mohammed Taha Salemin**

- Portfolio: [md-taha-portfolio.vercel.app](https://md-taha-portfolio.vercel.app)
- GitHub: [github.com/mdtaha-1](https://github.com/mdtaha-1)
- Email: mohammedtaha534@gmail.com

---

## License

MIT License — free to use, modify, and distribute.
