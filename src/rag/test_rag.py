from src.embeddings.load_embeddings import load_embeddings
from src.rag.similarity_search import similarity_search

emb = load_embeddings("data/processed/embeddings.json")
res = similarity_search(emb, "What is Rafa's experience in renewable energy?")
print(res[0]["metadata"]["source"])
