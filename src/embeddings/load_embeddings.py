import json
from pathlib import Path

def load_embeddings(relative_path: str):
    path = Path(relative_path).resolve()
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    embeddings = load_embeddings("data/processed/embeddings.json")
    print(f"Loaded {len(embeddings)} embeddings")
