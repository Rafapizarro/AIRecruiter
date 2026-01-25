from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.rag.pipeline import rag_pipeline
import traceback

app = FastAPI()

class AskRequest(BaseModel):
    question: str = Field(..., min_length=5)
    mode: str = "qa"

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/ask")
def ask_question(payload: AskRequest):
    try:
        result = rag_pipeline(
            input_text=payload.question,
            mode=payload.mode
        )
        return JSONResponse(content=result)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
