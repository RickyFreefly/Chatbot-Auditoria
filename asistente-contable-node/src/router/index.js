import express from "express";
import { consultarIA } from "../services/iaService.js";
import { prompts } from "../prompts.js";

const router = express.Router();

// 🔹 Mapa de palabras clave para detección automática
const temas = {
  niif: ["niif", "ifrs", "información financiera", "valor razonable", "activo", "pasivo"],
  nia: ["auditoría", "nia", "riesgo de auditoría", "evidencia", "opinión del auditor"],
  nicsp: ["sector público", "entidad gubernamental", "nicsp", "ipsas", "finanzas públicas"],
  pyme: ["niif pymes", "pymes", "empresa pequeña", "simplificada"]
};

// 🔹 Detección simple según la pregunta
function detectarTema(pregunta = "") {
  const texto = pregunta.toLowerCase();
  for (const [tema, palabras] of Object.entries(temas)) {
    if (palabras.some(p => texto.includes(p))) return tema;
  }
  return "general";
}

// 🔹 Endpoint general
router.post("/consultar", async (req, res) => {
  try {
    const { pregunta, contexto } = req.body;
    if (!pregunta) return res.status(400).json({ error: "Falta el campo 'pregunta'" });

    const tema = detectarTema(pregunta);
    const prompt = prompts[tema] || prompts.general;

    const respuesta = await consultarIA(pregunta, prompt + "\n\n" + (contexto || ""));
    res.json({ temaDetectado: tema, respuesta });
  } catch (err) {
    console.error("❌ Error en /consultar:", err.message);
    res.status(500).json({ error: "Error interno del servidor" });
  }
});

export default router;
