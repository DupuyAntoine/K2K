import { useState } from "react"
import DomainSelector from "./components/DomainSelector"
import ConversationList from "./components/ConversationList"
import ConversationPanel from "./components/ConversationPanel"
import NewConversationButton from "./components/NewConversationButton"
import ConversationFilesPanel from "./components/ConversationFilesPanel"

export default function App() {
  const [domain, setDomain] = useState("")
  const [conversations, setConversations] = useState([])
  const [activeConversation, setActiveConversation] = useState(null)
  const [files, setFiles] = useState([])

  return (
    <div className="flex h-screen bg-gray-100">
      <aside className="w-72 p-4 border-r space-y-4">
        <DomainSelector
          domain={domain}
          setDomain={setDomain}
        />
        <NewConversationButton
          domain={domain}
          setConversations={setConversations}
        />
        <ConversationList
          domain={domain}
          conversations={conversations}
          setConversations={setConversations}
          onSelect={setActiveConversation}
          activeId={activeConversation?.id}
        />
      </aside>
      <main className="flex-1 p-4">
        {domain && activeConversation ? (
          <ConversationPanel
            domain={domain}
            conversationId={activeConversation.id}
            setFiles={setFiles}
          />
        ) : (
          <div className="text-gray-500 italic text-center mt-20">
            Select a domain and conversation to start.
          </div>
        )}
        {activeConversation && files.length > 0 && (
        <div className="w-1/4 bg-gray-50 overflow-y-auto border-l border-gray-300">
          <ConversationFilesPanel files={files} />
        </div>
        )}
      </main>
    </div>
  )
}
