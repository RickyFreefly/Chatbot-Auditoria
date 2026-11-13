import os
import json
import numpy as np
import faiss
import fitz  # PyMuPDF
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv

# ===========================
# 🔹 Configuración
# ===========================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PDF_DIR = "data/pdfs"
FAISS_DIR = "data/faiss_index"
CORPUS_DIR = "data/corpus_jsonl"

os.makedirs(FAISS_DIR, exist_ok=True)
os.makedirs(CORPUS_DIR, exist_ok=True)

INDEX_PATH = os.path.join(FAISS_DIR, "index.faiss")
IDS_PATH = os.path.join(FAISS_DIR, "ids.json")
CORPUS_PATH = os.path.join(CORPUS_DIR, "corpus.jsonl")

# ===========================
# 🔹 Extracción y Embedding
# ===========================
vectors = []
ids = []
records = []
id_counter = 0

print("📘 Leyendo documentos desde:", PDF_DIR)

for pdf_file in tqdm(os.listdir(PDF_DIR)):
    if not pdf_file.endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_DIR, pdf_file)
    print(f"\n📄 Procesando {pdf_file}...")

    try:
        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(doc):
            text = page.get_text("text").strip()

            if not text:
                continue

            chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]

            for chunk in chunks:
                emb = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=chunk
                )
                vector = np.array(emb.data[0].embedding, dtype="float32")
                vector_id = f"{pdf_file}-{page_num}-{id_counter}"

                vectors.append(vector)
                ids.append(vector_id)
                records.append({
                    "id": vector_id,
                    "pdf": pdf_file,
                    "page": page_num,
                    "text": chunk
                })

                id_counter += 1

    except Exception as e:
        print(f"⚠️ Error procesando {pdf_file}: {e}")

# ===========================
# 🔹 Guardar resultados
# ===========================
if vectors:
    # Crear índice FAISS
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.vstack(vectors))
    faiss.write_index(index, INDEX_PATH)

    # Guardar IDs
    with open(IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False, indent=2)

    # Guardar corpus
    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("\n✅ Índice FAISS y corpus generados con éxito:")
    print(f"📦 {INDEX_PATH}")
    print(f"🧾 {IDS_PATH}")
    print(f"📚 {CORPUS_PATH}")
    print(f"📊 Total de fragmentos indexados: {len(ids)}")

else:
    print("⚠️ No se generaron embeddings. Revisa los archivos PDF.")
