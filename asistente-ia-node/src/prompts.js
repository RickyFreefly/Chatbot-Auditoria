import dotenv from "dotenv";
dotenv.config();

// 🔹 Rol del asistente: configurable vía .env (SYSTEM_PROMPT) según el
// corpus que se entrene para cada proyecto; este es solo el valor por defecto.
export const systemPrompt = process.env.SYSTEM_PROMPT || `
Eres un asistente experto que responde en español basándote únicamente
en el contexto documental proporcionado.
`;
