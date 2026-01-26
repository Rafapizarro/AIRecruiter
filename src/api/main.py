from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from src.rag.pipeline import rag_pipeline

app = FastAPI(
    title="AIRecruiter API",
    description="Recruiter-facing RAG backend for candidate evaluation",
    version="0.1.0"
)


# ---------
# Schemas
# ---------

class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        description="Recruiter question or full job description"
    )
    mode: str = Field(
        "qa",
        description="Evaluation mode: 'qa' or 'job_fit'"
    )


class AskResponse(BaseModel):
    answer: str
    confidence: str
    sources: List[str]
    fit_score: Optional[int] = None


# ---------
# Routes
# ---------

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    """
    Main inference endpoint.
    Delegates reasoning to the RAG pipeline.
    """

    try:
        result: Dict[str, Any] = rag_pipeline(
            input_text=payload.question,
            mode=payload.mode
        )

        # Defensive normalization (important)
        return {
            "answer": result.get("answer", ""),
            "confidence": result.get("confidence", "unknown"),
            "sources": result.get("sources", []),
            "fit_score": result.get("fit_score"),
        }

    except Exception as e:
        # We want explicit failure, not silent 500s
        raise HTTPException(
            status_code=500,
            detail=f"Backend error while processing request: {str(e)}"
        )
