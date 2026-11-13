import fitz  # PyMuPDF
import json
import os
from tqdm import tqdm

PDF_DIR = "../data/pdfs"
OUTPUT_DIR = "../data/corpus_jsonl"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def chunk_text(text, max_length=800):
    words = text.split()
    chunks, current_chunk = [], []
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def process_pdfs():
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    for pdf_file in tqdm(pdf_files, desc="Procesando PDFs"):
        text = extract_text_from_pdf(os.path.join(PDF_DIR, pdf_file))
        chunks = chunk_text(text)
        output_path = os.path.join(OUTPUT_DIR, pdf_file.replace(".pdf", ".jsonl"))
        with open(output_path, "w", encoding="utf-8") as out:
            for i, chunk in enumerate(chunks):
                json.dump({"id": f"{pdf_file}-{i}", "text": chunk}, out, ensure_ascii=False)
                out.write("\n")

if __name__ == "__main__":
    process_pdfs()
