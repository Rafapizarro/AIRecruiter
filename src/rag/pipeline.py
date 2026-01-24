from typing import Dict
from pathlib import Path

from src.embeddings.load_embeddings import load_embeddings
from src.rag.similarity_search import similarity_search
from src.rag.prompts.qa_prompt import build_prompt
from src.rag.prompts.job_fit_prompt import build_job_fit_prompt
from src.rag.generate_answer import generate_answer


def rag_pipeline(input_text: str, mode: str = "qa") -> Dict:
    """
    End-to-end RAG pipeline.

    Modes:
    - qa: recruiter questions
    - job_fit: recruiter-style job fit evaluation
    """

    EMBEDDINGS_PATH = Path("data/processed/embeddings.json")

    if not EMBEDDINGS_PATH.exists():
        return {
            "answer": "The knowledge base is not available yet.",
            "confidence": "none",
            "sources": []
        }

    # 1. Load embeddings
    embedded_chunks = load_embeddings(EMBEDDINGS_PATH)

    # 2. Retrieve relevant chunks
    retrieved_chunks = similarity_search(embedded_chunks, input_text)

    if not retrieved_chunks:
        return {
            "answer": "I couldn’t find relevant information to answer this request.",
            "confidence": "very low",
            "sources": []
        }

    # 3. Build prompt (mode-aware)
    if mode == "job_fit":
        prompt = build_job_fit_prompt(
            context_chunks=retrieved_chunks,
            job_description=input_text
        )
    else:
        prompt = build_prompt(
            context_chunks=retrieved_chunks,
            question=input_text
        )

    # 4. Generate answer (LLM)
    answer = generate_answer(prompt)

    # 5. Collect sources
    sources = list({
        chunk["metadata"]["source"] for chunk in retrieved_chunks
    })

    # 6. Confidence (retrieval-based, not judgment-based)
    top_score = retrieved_chunks[0]["score"]

    if top_score > 0.35:
        confidence = "high"
    elif top_score > 0.25:
        confidence = "medium"
    elif top_score > 0.15:
        confidence = "low"
    else:
        confidence = "very low"

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }
