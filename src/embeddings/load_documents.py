from pathlib import Path
from typing import List, Dict


def load_markdown_documents(data_dir: str = "data/raw") -> List[Dict]:
    """
    Load all markdown files from data_dir and return a list of documents
    with text content and metadata.
    """
    documents = []
    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    for md_file in data_path.glob("*.md"):
        text = md_file.read_text(encoding="utf-8")

        document = {
            "content": text,
            "metadata": {
                "source": md_file.name
            }
        }

        documents.append(document)

    return documents


if __name__ == "__main__":
    docs = load_markdown_documents()
    print(f"Loaded {len(docs)} documents")
    for doc in docs:
        print(f"- {doc['metadata']['source']}")
