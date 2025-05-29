import os
from agents.faiss_retriever import FaissRetriever

DATA_DIR = "data/documents"  # Adjust if your text docs are elsewhere
INDEX_PATH = "data/faiss.index"

def load_text_files(directory):
    texts = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                texts.append(f.read())
    return texts

def main():
    print("Loading documents...")
    documents = load_text_files(DATA_DIR)
    print(f"Loaded {len(documents)} documents.")

    retriever = FaissRetriever()
    print("Adding documents to FAISS index...")
    retriever.add_texts(documents)

    print(f"Saving index to {INDEX_PATH}")
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    retriever.save_index(INDEX_PATH)
    print("Done.")

if __name__ == "__main__":
    main()
