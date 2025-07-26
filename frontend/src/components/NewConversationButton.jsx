import PropTypes from "prop-types"
import { createConversation, fetchConversations } from "../api/api"

export default function NewConversationButton({ domain, setConversations }) {

  const handleConversationCreation = async () => {
    try {
      await createConversation(domain)
      await fetchConversations(domain).then(setConversations)
    } catch (error) {
      console.error("API error:", error)
    }
  }

  return (
    <button
      onClick={handleConversationCreation}
      className="w-full py-2 px-4 bg-green-600 text-white rounded shadow hover:bg-green-700 text-sm"
    >
      + New Conversation
    </button>
  )
}

NewConversationButton.propTypes = {
  domain: PropTypes.string.isRequired,
  setConversations: PropTypes.func.isRequired,
}
