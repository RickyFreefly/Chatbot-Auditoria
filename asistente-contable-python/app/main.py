from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

# 🔹 Módulos internos (los crearás enseguida)
from app.retriever import buscar_contexto
from app.prompts import generar_respuesta

app = FastAPI(title="Asistente Contable - IA Documental")

# ========================
# 📍 Endpoint raíz
# ========================
@app.get("/")
def root():
    return {"message": "Bienvenido al Asistente Contable IA"}

# ========================
# 📂 Subir PDF a data/pdfs
# ========================
@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Guarda el PDF en la carpeta data/pdfs"""
    pdf_dir = os.path.join("data", "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, file.filename)

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    return {"status": "ok", "filename": file.filename}

# ========================
# 🤖 Consultar IA
# ========================
class Consulta(BaseModel):
    pregunta: str

@app.post("/consultar/")
async def consultar(data: Consulta):
    """
    Recibe una pregunta contable, busca contexto en los documentos,
    y genera una respuesta con IA.
    """
    try:
        pregunta = data.pregunta
        print(f"🧠 Pregunta recibida: {pregunta}")
        contexto = buscar_contexto(pregunta)
        print(f"📚 Contexto recuperado: {len(contexto)} caracteres")
        respuesta = generar_respuesta(pregunta, contexto)
        print("✅ Respuesta generada correctamente.")
        return {"pregunta": pregunta, "respuesta": respuesta}

    except Exception as e:
        import traceback
        print("❌ ERROR DETALLADO:")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
