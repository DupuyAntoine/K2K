import { useState } from "react"
import fetch from '../api/api'

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you today ?", sender: "bot" }
  ]);
  const [input, setInput] = useState("")

  const handleSend = async () => {
    if (!input.trim()) return
    const newMessage = { text: input, sender: "user" }
    setMessages((prev) => [...prev, newMessage])
    setInput("")
    const data = await fetch(input);
    setMessages((prev) => [...prev, { text: data.responseInteraction.text, sender: "bot" }])
    setMessages((prev) => [...prev, { text: data.responseConstruction.text, sender: "bot" }])
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 p-4">
      <div className="flex-1 contents overflow-y-auto space-y-2 p-4 bg-white rounded-lg shadow">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-2 rounded-lg max-w-5xl ${
              msg.sender === "user"
                ? "bg-blue-500 text-white self-end"
                : "bg-gray-300 text-black self-start"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="flex items-center mt-4">
        <input
          type="text"
          className="flex-1 p-2 border rounded-lg"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          className="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg"
          onClick={handleSend}
        >
          Send
        </button>
      </div>
    </div>
  )
}

export default ChatInterface
