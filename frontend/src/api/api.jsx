import axios from 'axios';

export async function fetchDomains() {
  const res = await fetch("http://localhost:4000/api/domains")
  print(res)
  return res.json()
}

export async function fetchConversations(domain) {
  const res = await fetch(`http://localhost:4000/api/conversations/${domain}`)
  return res.json()
}

export async function createConversation(domain) {
  console.log(domain)
  const res = await axios.post("http://localhost:4000/api/conversations", {
    domain
  })
  return res
}

export async function sendUserMessage({ message, domain, conversationId }) {
  try {
    const res = await axios.post("http://localhost:4000/api/chat/query", {
      message,
      domain,
      conversationId
    })
    return res.data
  } catch (error) {
    console.error("API error:", error)
    throw error
  }
}
