import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class FaissRetriever:
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2", index_path=None):
        # Load sentence transformer model
        self.embedder = SentenceTransformer(embedding_model_name)
        self.dimension = 384  # for all-MiniLM-L6-v2
        self.index = None
        self.index_path = index_path

        # Load or initialize FAISS index
        if index_path:
            self.load_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)  # L2 similarity

        self.texts = []  # Store texts alongside embeddings

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        return self.embedder.encode(texts, convert_to_numpy=True)

    def add_texts(self, texts: List[str]):
        embeddings = self.embed_texts(texts)
        self.index.add(embeddings)
        self.texts.extend(texts)
        print(f"[+] Added {len(texts)} texts to FAISS. Total: {len(self.texts)}")

    def save_index(self, path: str):
        faiss.write_index(self.index, path)

    def load_index(self, path: str):
        self.index = faiss.read_index(path)
        print(f"[✓] Loaded FAISS index from {path}")

    def retrieve(self, query: str, top_k=5) -> List[Tuple[str, float]]:
        query_embedding = self.embed_texts([query])
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if 0 <= idx < len(self.texts):  # ✅ skip invalid indices
                results.append((self.texts[idx], dist))
        return results


# ✅ Wrapper function to match `test_retrieval.py` usage
def retrieve_similar_documents(query: str, top_k: int = 5, index_path="data/faiss.index") -> List[Tuple[str, float]]:
    retriever = FaissRetriever(index_path=index_path)

    # 🔁 TEMP MOCK — replace with loading from file or DB in production
    retriever.texts = [
        "Stock markets are volatile today due to inflation fears.",
        "Nifty closed 1.2% higher amidst positive global cues.",
        "RBI policy update expected tomorrow may impact bond yields.",
        "HDFC Bank shows strong quarterly earnings beating estimates.",
        "Investors look to gold as safe haven amid market uncertainty."
    ]

    return retriever.retrieve(query, top_k=top_k)
