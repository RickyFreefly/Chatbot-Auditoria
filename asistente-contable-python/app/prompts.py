# app/prompts.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generar_respuesta(pregunta: str, contexto: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 🔹 Reducir tamaño del contexto para dejar más espacio a la respuesta
    if len(contexto) > 2500:
        contexto = contexto[:2500] + "\n\n[Contexto truncado por longitud]\n"

    prompt = f"""
Eres un asistente contable experto en NIIF, NICSP y NIA.
Responde con precisión técnica y citas cuando sea posible.
Usa únicamente el siguiente contexto documental para sustentar la respuesta.

Contexto:
{contexto}

Pregunta:
{pregunta}

Respuesta:
"""

    print(f"🧠 Pregunta recibida: {pregunta}")
    print(f"📚 Longitud del contexto: {len(contexto)} caracteres")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=800  # 🔼 antes 350
        )

        print("🧾 Raw completion response:", completion)
        respuesta = completion.choices[0].message.content.strip() if completion.choices else ""
        if not respuesta:
            raise ValueError("El modelo no devolvió texto.")
        print(f"✅ Respuesta IA (gpt-5-mini): {respuesta[:150]}...")
        return respuesta

    except Exception as e:
        print(f"⚠️ Error con gpt-5-mini: {e}")
        print("➡️ Intentando con modelo de respaldo gpt-5-nano...")

        try:
            completion = client.chat.completions.create(
                model="gpt-5-nano",
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=800
            )
            respuesta = completion.choices[0].message.content.strip() if completion.choices else ""
            if not respuesta:
                raise ValueError("El modelo de respaldo tampoco devolvió texto.")
            print(f"✅ Respuesta IA (gpt-5-nano): {respuesta[:150]}...")
            return respuesta
        except Exception as e2:
            print(f"❌ Error también con gpt-5-nano: {e2}")
            return "No se obtuvo respuesta del servicio IA."
