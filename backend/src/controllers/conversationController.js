import fs from 'fs/promises'
import path from 'path'
import v4 from 'uuid'

const BASE_DOMAIN_DIR = path.resolve('data')

// Fonction utilitaire pour retrouver le dossier de conversations
const getConversationDir = (domain) =>
  path.join(BASE_DOMAIN_DIR, domain, 'conversations')

export async function getConversationsByDomain(req, res) {
  const { domain } = req.params

  if (!domain) {
    return res.status(400).json({ error: 'Missing domain in request' })
  }

  const conversationPath = getConversationDir(domain)

  try {
    const files = await fs.readdir(conversationPath)
    const conversations = []

    for (const file of files) {
      if (!file.endsWith('.json')) continue

      const content = await fs.readFile(path.join(conversationPath, file), 'utf-8')
      const json = JSON.parse(content)
      conversations.push({ id: json.id, domain: json.domain })
    }

    res.json(conversations)
  } catch (err) {
    if (err.code === 'ENOENT') {
      // Aucun dossier ou fichier, retourne un tableau vide
      return res.json([])
    }

    console.error(`Error reading conversations for ${domain}:`, err)
    res.status(500).json({ error: 'Failed to read conversations' })
  }
}

export async function createConversation(req, res) {
  try {
    const { domain } = req.body
    if (!domain) return res.status(400).json({ error: 'Domain is required' })

    const id = v4()
    const conversation = {
      id,
      domain,
      messages: [],
      files: []
    }

    const conversationPath = getConversationDir(domain)
    await fs.mkdir(conversationPath, { recursive: true })

    const filePath = path.join(conversationPath, `${id}.json`)
    await fs.writeFile(filePath, JSON.stringify(conversation, null, 2))

    res.status(201).json(conversation)
  } catch (err) {
    console.error('Error creating conversation:', err)
    res.status(500).json({ error: 'Failed to create conversation' })
  }
}
