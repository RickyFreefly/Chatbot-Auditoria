import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";
import "./styles.css";

const API_URL = "http://localhost:4000/api/consultar";

function App() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "👋 ¡Hola! Soy tu asistente contable experto en NIIF, NIA y NICSP. ¿En qué puedo ayudarte hoy?" }
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput("");

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pregunta: input }),
      });
      const data = await res.json();
      const botMsg = { role: "bot", text: data.respuesta || "⚠️ No se obtuvo respuesta." };
      setMessages((msgs) => [...msgs, botMsg]);
    } catch (error) {
      setMessages((msgs) => [...msgs, { role: "bot", text: "❌ Error conectando con el servidor." }]);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">💼 Asistente Contable NIIF / NIA / NICSP</div>

      <div className="chat-body">
        {messages.map((msg, i) => (
          <motion.div
            key={i}
            className={`chat-bubble ${msg.role}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <ReactMarkdown>{msg.text}</ReactMarkdown>
          </motion.div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Escribe tu consulta contable..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Enviar</button>
      </div>
    </div>
  );
}

export default App;
