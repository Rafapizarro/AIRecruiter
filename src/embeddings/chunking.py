from typing import List, Dict

def chunk_text(
    documents: List[Dict],
    chunk_size: int = 300,
    overlap: int = 50
) -> List[Dict]:
    """
    Split documents into overlapping chunks.

    Each chunk keeps metadata about its source.
    """
    chunks = []

    for doc in documents:
        words = doc["content"].split()
        source = doc["metadata"]["source"]

        start = 0
        chunk_index = 0

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append({
                "content": chunk_text,
                "metadata": {
                    "source": source,
                    "chunk_index": chunk_index
                }
            })

            start += chunk_size - overlap
            chunk_index += 1

    return chunks
