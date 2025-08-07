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
      <main className="flex-1 p-4 flex">
        {domain && activeConversation ? (
          <>
            <div className="flex-1 pr-4">
              <ConversationPanel
                domain={domain}
                conversationId={activeConversation.id}
                setFiles={setFiles}
              />
            </div>
            {files.length > 0 && (
              <div className="w-80 border-l pl-4">
                <ConversationFilesPanel files={files} />
              </div>
            )}
          </>
        ) : (
          <div className="text-gray-500 italic text-center mt-20 w-full">
            Select a domain and conversation to start.
          </div>
        )}
      </main>
    </div>
  )
}
