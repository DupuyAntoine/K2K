import PropTypes from 'prop-types'
import { useEffect, useState } from "react"
import ReactMarkdown from "react-markdown"
import { sendUserMessage, fetchConversation } from "../api/api"

export default function ConversationPanel({ domain, conversationId, setFiles }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

useEffect(() => {
  if (!domain || !conversationId) return

  let cancelled = false

  const defaultBotGreeting = {
    sender: "bot",
    text: `Hello! How can I assist you today?\n\n_Disclaimer: This system is in a testing phase for Earth Observation data. Please use the shared feedback pad: https://annuel.framapad.org/p/feedbackk2k-afcw?lang=fr_`
  }

  const loadConversation = async () => {
    try {
      const data = await fetchConversation(domain, conversationId)
      if (!cancelled) {
        const history = data.messages || []
        setMessages([defaultBotGreeting, ...history])
        setFiles(data.files || [])
      }
    } catch (err) {
      console.error("Erreur chargement conversation :", err)
      if (!cancelled) {
        setMessages([defaultBotGreeting])
        setFiles([])
      }
    }
  }

  loadConversation()

  return () => {
    cancelled = true
  }
}, [domain, conversationId, setFiles])

  const handleSend = async () => {
    if (!input.trim() || !domain) return

    const userMsg = { text: input, sender: "user" }
    setMessages((prev) => [...prev, userMsg])
    setInput("")
    setLoading(true)

    try {
      const res = await sendUserMessage({
        message: input,
        domain,
        conversationId
      })

      const botMsg = {
        text: res.response || "[Empty response]",
        sender: "bot"
      }

      setMessages((prev) => [...prev, botMsg])
      setFiles(res.files || [])
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { text: "Failed to contact agent.", sender: "bot" }
      ])
      console.error("API error:", error)
      setFiles([])
    }

    setLoading(false)
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 bg-white rounded shadow space-y-2">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 rounded-xl max-w-4xl break-words whitespace-pre-wrap ${
              msg.sender === "user"
                ? "bg-blue-600 text-white self-end"
                : "bg-gray-200 text-gray-800 self-start"
            }`}
          >
            <ReactMarkdown>{msg.text}</ReactMarkdown>
          </div>
        ))}
        {loading && <p className="text-sm text-gray-500 italic">Loading...</p>}
      </div>

      <div className="flex items-center mt-4 gap-2">
        <input
          type="text"
          className="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm"
          placeholder="Ask something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          onClick={handleSend}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  )
}

ConversationPanel.propTypes = {
  domain: PropTypes.string.isRequired,
  conversationId: PropTypes.string.isRequired,
  setFiles: PropTypes.func.isRequired
}
