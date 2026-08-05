import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) {
      alert("Please enter a message.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Something went wrong.");
      }

      const data = await response.json();

      setReply(data.reply);
      setMessage("");
    } catch (err) {
      console.error("Error:", err);

      if (err.message === "Failed to fetch") {
        alert(
          "Cannot connect to the FastAPI backend.\n\nMake sure:\n1. FastAPI is running.\n2. The backend is on port 8000.\n3. CORS is enabled."
        );
      } else {
        alert(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="container">
      <h1>🤖 AI SaaS ChatGPT</h1>

      <textarea
        rows="6"
        placeholder="Ask anything..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <br />

      <button onClick={sendMessage} disabled={loading}>
        {loading ? "Thinking..." : "Send"}
      </button>

      <h3>AI Response</h3>

      <div className="response">
        {loading ? (
          <p>Generating response...</p>
        ) : reply ? (
          <p>{reply}</p>
        ) : (
          <p>No response yet.</p>
        )}
      </div>
    </div>
  );
}

export default App;