import os, json
import numpy as np
from models.embeddings import get_embeddings
from utils.preprocess import chunk_text

METADATA_FILE = 'data/vector_metadata.json'
INDEX_FILE = 'data/faiss_index.npy'

class SimpleVectorStore:
    def __init__(self):
        self.chunks = []
        self.index = None
        if os.path.exists(METADATA_FILE) and os.path.exists(INDEX_FILE):
            try:
                with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                    self.chunks = json.load(f)
                self.index = np.load(INDEX_FILE)
            except Exception:
                self.chunks = []
                self.index = None

    def upsert_documents(self, texts):
        # texts: list[str] (full docs)
        all_chunks = []
        for t in texts:
            all_chunks.extend(chunk_text(t))
        embeddings = get_embeddings(all_chunks)
        emb_arr = np.array(embeddings).astype('float32')
        if self.index is None:
            self.index = emb_arr
        else:
            self.index = np.vstack([self.index, emb_arr])
        self.chunks.extend(all_chunks)
        os.makedirs('data', exist_ok=True)
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.chunks, f)
        np.save(INDEX_FILE, self.index)

    def retrieve(self, query, k=4):
        q_emb = np.array(get_embeddings([query])).astype('float32')
        if self.index is None or len(self.chunks) == 0:
            return []
        dists = np.linalg.norm(self.index - q_emb, axis=1)
        idx = dists.argsort()[:k]
        return [self.chunks[i] for i in idx.tolist()]
