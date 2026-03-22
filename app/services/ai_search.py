import faiss
import pickle
import os
from typing import List, Tuple

FAISS_INDEX_PATH = "faiss_index/index.faiss"
METADATA_PATH    = "faiss_index/metadata.pkl"

os.makedirs("faiss_index", exist_ok=True)

faiss_index = None
chunk_metadata: List[dict] = []
model = None

def get_model():
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

def _load_or_create_index():
    global faiss_index, chunk_metadata
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(METADATA_PATH):
        faiss_index = faiss.read_index(FAISS_INDEX_PATH)
        with open(METADATA_PATH, "rb") as f:
            chunk_metadata = pickle.load(f)
    else:
        faiss_index    = faiss.IndexFlatL2(384)
        chunk_metadata = []

def _save_index():
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(chunk_metadata, f)

def _chunk_text(text: str, chunk_size: int = 300) -> List[str]:
    words  = text.split()
    chunks = []
    step   = chunk_size - 50
    for i in range(0, len(words), step):
        chunk = " ".join(words[i: i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def add_document_to_index(document_id: int, filename: str, text: str):
    global faiss_index, chunk_metadata
    if faiss_index is None:
        _load_or_create_index()
    chunks = _chunk_text(text)
    if not chunks:
        return
    embeddings = get_model().encode(chunks, convert_to_numpy=True).astype("float32")
    faiss_index.add(embeddings)
    for chunk in chunks:
        chunk_metadata.append({
            "document_id": document_id,
            "filename":    filename,
            "chunk_text":  chunk
        })
    _save_index()

def search_documents(query: str, top_k: int = 5) -> List[Tuple[dict, float]]:
    global faiss_index, chunk_metadata
    if faiss_index is None:
        _load_or_create_index()
    if faiss_index.ntotal == 0:
        return []
    query_embedding = get_model().encode([query], convert_to_numpy=True).astype("float32")
    k = min(top_k, faiss_index.ntotal)
    distances, indices = faiss_index.search(query_embedding, k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        results.append((chunk_metadata[idx], float(dist)))
    return results

def remove_document_from_index(document_id: int):
    global faiss_index, chunk_metadata
    if faiss_index is None:
        _load_or_create_index()
    remaining = [m for m in chunk_metadata if m["document_id"] != document_id]
    if not remaining:
        faiss_index    = faiss.IndexFlatL2(384)
        chunk_metadata = []
        _save_index()
        return
    texts      = [m["chunk_text"] for m in remaining]
    embeddings = get_model().encode(texts, convert_to_numpy=True).astype("float32")
    new_index  = faiss.IndexFlatL2(384)
    new_index.add(embeddings)
    faiss_index    = new_index
    chunk_metadata = remaining
    _save_index()