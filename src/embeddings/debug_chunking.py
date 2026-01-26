from src.embeddings.load_documents import load_markdown_documents
from src.embeddings.chunking import chunk_text

docs = load_markdown_documents()
chunks = chunk_text(docs)

print(f"Documents: {len(docs)}")
print(f"Chunks: {len(chunks)}")

print("\nFirst chunk metadata:")
print(chunks[0]["metadata"])

print("\nFirst chunk preview:")
print(chunks[0]["content"][:300])
