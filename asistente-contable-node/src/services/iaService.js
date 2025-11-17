// src/services/iaService.js
import axios from "axios";
import dotenv from "dotenv";
dotenv.config();

export async function consultarIA(pregunta, contexto = "") {
  const IA_URL = process.env.PYTHON_URL || "http://127.0.0.1:8001";

  try {
    console.log("🌐 Enviando pregunta al microservicio IA:", IA_URL);
    const response = await axios.post(`${IA_URL}/consultar/`, { pregunta, contexto });

    console.log("✅ Respuesta recibida del microservicio IA:", response.data);

    // ✅ Manejo flexible de estructura de respuesta
    if (response.data?.respuesta) {
      return response.data.respuesta;
    }

    // Si la IA devuelve estructura diferente
    if (response.data?.data?.respuesta) {
      return response.data.data.respuesta;
    }

    console.warn("⚠️ Respuesta del microservicio sin campo 'respuesta':", response.data);
    return "No se obtuvo respuesta del servicio IA.";

  } catch (error) {
    console.error("❌ Error al conectar con el microservicio IA:", error.message);
    if (error.response) console.error("📩 Respuesta del microservicio:", error.response.data);
    if (error.code) console.error("Código:", error.code);
    throw new Error("Error al conectar con el microservicio IA");
  }
}
