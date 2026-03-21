import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

FAISS_INDEX_PATH = "faiss_index/index.faiss"
METADATA_PATH    = "faiss_index/metadata.pkl"

os.makedirs("faiss_index", exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

faiss_index: faiss.Index = None
chunk_metadata: List[dict] = []

def _load_or_create_index():
    global faiss_index, chunk_metadata
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(METADATA_PATH):
        faiss_index = faiss.read_index(FAISS_INDEX_PATH)
        with open(METADATA_PATH, "rb") as f:
            chunk_metadata = pickle.load(f)
        print(f"Loaded FAISS index with {faiss_index.ntotal} vectors")
    else:
        faiss_index    = faiss.IndexFlatL2(384)
        chunk_metadata = []
        print("Created new FAISS index")

def _save_index():
    global faiss_index, chunk_metadata
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(chunk_metadata, f)
    print(f"Saved FAISS index with {faiss_index.ntotal} vectors")

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
    _load_or_create_index()
    chunks = _chunk_text(text)
    if not chunks:
        print("No chunks found in document!")
        return
    print(f"Adding {len(chunks)} chunks for document {document_id}")
    embeddings = model.encode(chunks, convert_to_numpy=True).astype("float32")
    faiss_index.add(embeddings)
    for chunk in chunks:
        chunk_metadata.append({
            "document_id": document_id,
            "filename":    filename,
            "chunk_text":  chunk
        })
    _save_index()
    print(f"FAISS now has {faiss_index.ntotal} total vectors")

def search_documents(query: str, top_k: int = 5) -> List[Tuple[dict, float]]:
    global faiss_index, chunk_metadata
    _load_or_create_index()
    print(f"Searching with {faiss_index.ntotal} vectors in index")
    if faiss_index.ntotal == 0:
        return []
    query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")
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
    _load_or_create_index()
    remaining = [m for m in chunk_metadata if m["document_id"] != document_id]
    if not remaining:
        faiss_index    = faiss.IndexFlatL2(384)
        chunk_metadata = []
        _save_index()
        return
    texts      = [m["chunk_text"] for m in remaining]
    embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")
    new_index  = faiss.IndexFlatL2(384)
    new_index.add(embeddings)
    faiss_index    = new_index
    chunk_metadata = remaining
    _save_index()

_load_or_create_index()