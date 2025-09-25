import os, glob
import numpy as np
import faiss
from openai import OpenAI
import json

class Retriever:
    def __init__(self, openai_client, docs_dir="data/docs", embedding_model="text-embedding-3-small", top_k=3):
        self.client = openai_client
        self.docs_dir = docs_dir
        self.embedding_model = embedding_model
        self.top_k = top_k
        self.ids = []
        self.metadatas = []
        self.vectors = None
        self.index = None

    def load_docs(self):
        files = sorted(glob.glob(f"{self.docs_dir}/*.txt"))
        docs = []
        for i, fpath in enumerate(files):
            with open(fpath, "r", encoding="utf-8") as f:
                text = f.read().strip()
            docs.append({"id": f"doc{i+1}", "text": text, "path": fpath})
        return docs

    def build_index(self):
        docs = self.load_docs()
        texts = [d["text"] for d in docs]
        ids = [d["id"] for d in docs]
        embeddings = []
        for t in texts:
            emb = self.client.embeddings.create(model=self.embedding_model, input=t).data[0].embedding
            embeddings.append(np.array(emb, dtype=np.float32))
        matrix = np.vstack(embeddings)
        dim = matrix.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(matrix)
        self.index = index
        self.vectors = matrix
        self.ids = ids
        self.metadatas = docs

    def query(self, q):
        q_emb = np.array(self.client.embeddings.create(model=self.embedding_model, input=q).data[0].embedding, dtype=np.float32)
        D, I = self.index.search(np.expand_dims(q_emb, 0), self.top_k)
        hits = []
        for dist, idx in zip(D[0], I[0]):
            hits.append({"id": self.ids[idx], "text": self.metadatas[idx]["text"], "distance": float(dist)})
        return hits
