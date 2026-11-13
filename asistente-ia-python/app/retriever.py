import faiss
import numpy as np
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

INDEX_PATH = "data/faiss_index/index.faiss"
IDS_PATH = "data/faiss_index/ids.json"
CORPUS_PATH = "data/corpus_jsonl/corpus.jsonl"

def search(query, top_k=5):
    """Realiza la búsqueda semántica en FAISS y devuelve fragmentos relevantes"""
    # 🔹 Crear embedding de la pregunta
    emb = client.embeddings.create(model="text-embedding-3-small", input=query)
    query_vec = np.array(emb.data[0].embedding, dtype="float32").reshape(1, -1)

    # 🔹 Cargar índice FAISS
    index = faiss.read_index(INDEX_PATH)
    D, I = index.search(query_vec, top_k)

    # 🔹 Leer IDs de los fragmentos
    with open(IDS_PATH, "r", encoding="utf-8") as f:
        ids = json.load(f)

    # 🔹 Leer corpus completo una sola vez (más eficiente)
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = [json.loads(line) for line in f]

    # 🔹 Recuperar fragmentos relevantes
    results = []
    for idx in I[0]:
        file_id = ids[idx]
        match = next((r for r in corpus if r["id"] == file_id), None)
        if match:
            results.append(match["text"])

    return results


def buscar_contexto(pregunta: str) -> str:
    """Compatibilidad con main.py"""
    resultados = search(pregunta, top_k=5)
    contexto = "\n".join(resultados)
    return contexto
