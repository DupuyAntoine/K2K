import PropTypes from 'prop-types'
import { useEffect } from "react"
import { fetchConversations } from "../api/api"

export default function ConversationList({ domain, conversations, setConversations, onSelect, activeId }) {

  useEffect(() => {
    if (domain) {
      fetchConversations(domain).then(setConversations)
    }
  })

  return (
    <div className="bg-white shadow rounded p-3 w-64">
      <h2 className="text-lg font-bold mb-2">Conversations</h2>
      <ul className="space-y-1 max-h-80 overflow-auto">
        {conversations.map((conv) => (
          <li
            key={conv.id}
            className={`cursor-pointer p-2 rounded ${
              conv.id === activeId ? "bg-blue-100 font-bold" : "hover:bg-gray-100"
            }`}
            onClick={() => onSelect(conv)}
          >
            {conv.title || `Conversation ${conv.id.slice(0, 6)}`}
          </li>
        ))}
      </ul>
    </div>
  );
}

ConversationList.propTypes = {
  domain: PropTypes.string.isRequired,
  conversations: PropTypes.array.isRequired,
  setConversations: PropTypes.func.isRequired,
  onSelect: PropTypes.func.isRequired,
  activeId: PropTypes.string,
}
