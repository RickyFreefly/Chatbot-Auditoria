import express from "express";
import cors from "cors";
import morgan from "morgan";
import dotenv from "dotenv";
import { consultarIA } from "./services/iaService.js";
import { prompts } from "./prompts.js"; // 👈 nuevo archivo con plantillas

dotenv.config();
const app = express();

app.use(cors({
  origin: ["http://localhost:5173"], // dominio del frontend Vite
  methods: ["GET", "POST"],
  allowedHeaders: ["Content-Type"],
}));
app.use(express.json());
app.use(morgan("dev"));

const PORT = process.env.PORT || 4000;

// 🔹 Endpoint raíz
app.get("/", (req, res) => {
  res.json({ message: "Asistente Contable API - Node.js" });
});

// =======================================================
// 🧠 Nuevo bloque: detección automática del tipo de norma
// =======================================================

const temas = {
  niif: ["niif", "ifrs", "activo", "pasivo", "valor razonable", "ingresos", "arrendamiento"],
  nia: ["auditoría", "nia", "riesgo de auditoría", "evidencia", "opinión", "control interno"],
  nicsp: ["sector público", "gobierno", "nicsp", "ipsas", "entidad pública"],
  pyme: ["pyme", "pymes", "niif para pymes", "microempresa", "pequeña empresa"]
};

function detectarTema(pregunta = "") {
  const texto = pregunta.toLowerCase();
  for (const [tema, palabras] of Object.entries(temas)) {
    if (palabras.some(p => texto.includes(p))) return tema;
  }
  return "general";
}

// 🔹 Endpoint para consulta IA
app.post("/api/consultar", async (req, res) => {
  try {
    const { pregunta, contexto } = req.body;
    if (!pregunta) return res.status(400).json({ error: "Falta el campo 'pregunta'" });

    // 🧠 Detección del tipo de norma
    const tema = detectarTema(pregunta);
    const promptBase = prompts[tema] || prompts.general;
    const promptCompleto = `${promptBase}\n\n${contexto || ""}`;

    const respuesta = await consultarIA(pregunta, promptCompleto);

    res.json({
      temaDetectado: tema,
      respuesta
    });
  } catch (err) {
    console.error("❌ Error en /api/consultar:", err.message);
    res.status(500).json({ error: "Error interno del servidor" });
  }
});

app.listen(PORT, () =>
  console.log(`🚀 Servidor Node ejecutándose en puerto ${PORT}`)
);
