import os
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from app.core.llm import chat

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Setup ChromaDB
chroma_client = chromadb.PersistentClient(path="./data/chroma")
collection = chroma_client.get_or_create_collection(name="documents")

def ingest_pdf(file_path: str, doc_id: str) -> int:
    """Read PDF, chunk it, embed and store in ChromaDB"""
    reader = PdfReader(file_path)
    chunks = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            # Split page into chunks of ~500 chars
            for i in range(0, len(text), 500):
                chunk = text[i:i+500].strip()
                if chunk:
                    chunks.append(chunk)

    if not chunks:
        return 0

    embeddings = embedder.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    )

    return len(chunks)

def query_documents(question: str, n_results: int = 3) -> str:
    """Find relevant chunks and answer using LLM"""
    question_embedding = embedder.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=n_results
    )

    if not results["documents"][0]:
        return "No relevant documents found."

    context = "\n\n".join(results["documents"][0])

    system_prompt = f"""You are an enterprise document assistant.
Answer the user's question using ONLY the context below.
If the answer isn't in the context, say so clearly.

CONTEXT:
{context}"""

    return chat(question, system_prompt=system_prompt)
    