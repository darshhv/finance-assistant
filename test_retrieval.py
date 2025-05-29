from agents.faiss_retriever import FaissRetriever

# Instantiate and load index
retriever = FaissRetriever(index_path="data/faiss.index")

# Mock texts - replace with the actual texts used to build the index
retriever.texts = [
    "Stock markets are volatile today due to inflation fears.",
    "Nifty closed 1.2% higher amidst positive global cues.",
    "RBI policy update expected tomorrow may impact bond yields.",
    "HDFC Bank shows strong quarterly earnings beating estimates.",
    "Investors look to gold as safe haven amid market uncertainty."
]

# Run query
results = retriever.retrieve("What's happening in the Indian stock market?")
for i, (text, dist) in enumerate(results, 1):
    print(f"{i}. {text} (distance: {dist:.4f})")
