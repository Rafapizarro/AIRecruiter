import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_documents(chunks: List[Dict]) -> List[Dict]:
    embedded_chunks = []

    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["content"]
        )

        embedding = response.data[0].embedding

        embedded_chunks.append({
            "content": chunk["content"],
            "embedding": embedding,
            "metadata": chunk["metadata"]
        })

    return embedded_chunks


def save_embeddings(embedded_chunks, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(embedded_chunks, f, ensure_ascii=False, indent=2)


from src.embeddings.load_documents import load_markdown_documents
from src.embeddings.chunking import chunk_text
from pathlib import Path
import json

if __name__ == "__main__":
    documents = load_markdown_documents("data/raw")
    chunks = chunk_text(documents)

    embedded_chunks = embed_documents(chunks)

    output_path = Path("data/processed/embeddings.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(embedded_chunks, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(embedded_chunks)} embeddings")
