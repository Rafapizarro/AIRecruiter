from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from src.rag.pipeline import rag_pipeline

app = FastAPI()

class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        description="Recruiter question or job description"
    )
    mode: str = Field(
        "qa",
        description="qa or job_fit"
    )

class AskResponse(BaseModel):
    answer: str
    confidence: str
    sources: List[str]
    fit_score: Optional[int] = None

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest):
    try:
        return rag_pipeline(
            input_text=payload.question,
            mode=payload.mode
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error while processing the question: {e}"
        )
