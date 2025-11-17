import os
import json
import numpy as np
import faiss
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

DATA_DIR = "../data/corpus_jsonl"
INDEX_DIR = "../data/faiss_index"
os.makedirs(INDEX_DIR, exist_ok=True)

def build_faiss_index():
    texts, ids = [], []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".jsonl"):
            with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
                for line in f:
                    record = json.loads(line)
                    ids.append(record["id"])
                    texts.append(record["text"])

    vectors = []
    for t in tqdm(texts, desc="Generando embeddings"):
        emb = client.embeddings.create(model="text-embedding-3-small", input=t)
        vectors.append(np.array(emb.data[0].embedding, dtype="float32"))

    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors))
    faiss.write_index(index, os.path.join(INDEX_DIR, "index.faiss"))

    with open(os.path.join(INDEX_DIR, "ids.json"), "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False)

if __name__ == "__main__":
    build_faiss_index()
