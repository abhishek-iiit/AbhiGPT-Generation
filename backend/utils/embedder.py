from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(texts):
    """
    Generate embeddings for a list of texts using SentenceTransformer.

    Args:
        texts (List[str]): List of text strings to embed.

    Returns:
        np.ndarray: Array of embedding vectors.
    """
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings
