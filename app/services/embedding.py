from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model once at import time
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

async def get_embedding(text: str) -> list[float]:
    # We return as list of floats to store in pgvector
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()
