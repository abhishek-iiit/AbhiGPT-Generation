import faiss
import numpy as np

class Retriever:
    def __init__(self, embeddings, documents):
        embeddings = np.array(embeddings).astype('float32')
        if embeddings.size == 0:
            raise ValueError("Embeddings array is empty. Ensure that embeddings are generated before initializing the Retriever.")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.documents = documents

    def retrieve(self, query_embedding, top_k=3):
        if self.index.ntotal == 0:
            raise ValueError("FAISS index is empty. Cannot perform retrieval.")
        query_embedding = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.documents[i] for i in indices[0]]
