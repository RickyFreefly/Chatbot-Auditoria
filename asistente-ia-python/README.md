# asistente-ia-python

Microservicio en FastAPI que implementa el pipeline RAG: extrae texto de los PDFs en `data/pdfs/`, genera embeddings y los indexa en FAISS (`app/extractor.py`, `app/embedder.py`, `app/create_index.py`), busca contexto relevante (`app/retriever.py`) y genera la respuesta con OpenAI (`app/prompts.py`).

Ver el [README principal](../README.md) para la arquitectura completa, variables de entorno y pasos de instalación, incluyendo cómo cargar un corpus propio.
