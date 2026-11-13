import express from "express";
import cors from "cors";
import morgan from "morgan";
import dotenv from "dotenv";
import { consultarIA } from "./services/iaService.js";
import { systemPrompt } from "./prompts.js";

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
  res.json({ message: "Asistente IA API - Node.js" });
});

// 🔹 Endpoint para consulta IA
app.post("/api/consultar", async (req, res) => {
  try {
    const { pregunta, contexto } = req.body;
    if (!pregunta) return res.status(400).json({ error: "Falta el campo 'pregunta'" });

    const promptCompleto = `${systemPrompt}\n\n${contexto || ""}`;
    const respuesta = await consultarIA(pregunta, promptCompleto);

    res.json({ respuesta });
  } catch (err) {
    console.error("❌ Error en /api/consultar:", err.message);
    res.status(500).json({ error: "Error interno del servidor" });
  }
});

app.listen(PORT, () =>
  console.log(`🚀 Servidor Node ejecutándose en puerto ${PORT}`)
);
