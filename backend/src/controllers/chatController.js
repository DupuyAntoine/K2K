import path from 'path'
import fs from 'fs/promises'
import fssync from 'fs'
import axios from 'axios'
import { parse } from 'csv-parse'
import { extractAndSelectChunksFromContext } from '../utils/tfidf.js'
import { fetchOntology } from '../utils/sparql.js'

const DATA_BASE_DIR = path.resolve('data')
const AGENT_API_URL = process.env.AGENT_URL

async function parseCsvStream(filePath) {
  return new Promise((resolve, reject) => {
    const records = []
    const parser = parse({ columns: true, skip_empty_lines: true, relax_column_count: true })

    parser.on('readable', () => {
      let record
      while ((record = parser.read()) !== null) {
        records.push(record)
      }
    })

    parser.on('error', (err) => {
      reject(err)
    })

    parser.on('end', () => {
      resolve(records)
    })

    fssync.createReadStream(filePath).pipe(parser)
  })
}

async function loadContextFiles(contextDir) {
  try {
    const entries = await fs.readdir(contextDir, { withFileTypes: true })
    const contextData = {}

    for (const entry of entries) {
      const filePath = path.join(contextDir, entry.name)
      const ext = path.extname(entry.name).toLowerCase()
      const baseName = path.basename(entry.name, ext)

      if (ext === '.json') {
        try {
          const content = await fs.readFile(filePath, 'utf-8')
          contextData[baseName] = JSON.parse(content)
        } catch {
          console.warn(`Fichier JSON mal formé : ${entry.name}`)
        }
      } else if (ext === '.csv') {
        try {
          const records = await parseCsvStream(filePath)
          contextData[baseName] = records
        } catch (err) {
          console.warn(`Erreur de parsing CSV : ${entry.name}`, err.message)
        }
      } else if (['.rdf', '.ttl', '.xml'].includes(ext)) {
        try {
          const content = await fs.readFile(filePath, 'utf-8')
          contextData[baseName] = content
        } catch {
          console.warn(`Erreur de lecture fichier RDF-like : ${entry.name}`)
        }
      } else {
        console.warn(`Fichier ignoré (type non supporté) : ${entry.name}`)
      }
    }

    return contextData
  } catch (err) {
    console.warn("Dossier context manquant ou vide :", contextDir)
    return {}
  }
}

export async function handleUserQuery(req, res) {
  try {
    const { message, domain, conversationId } = req.body

    if (!message || !domain || !conversationId) {
      return res.status(400).json({ error: 'Missing message, domain or conversationId' })
    }

    const domainDir = path.join(DATA_BASE_DIR, domain)
    const contextDir = path.join(domainDir, 'contexts')
    const convoPath = path.join(domainDir, 'conversations', `${conversationId}.json`)

    const domainContextRaw = await loadContextFiles(contextDir)
    const reducedContext = extractAndSelectChunksFromContext(domainContextRaw, message, 10)

    let conversation = []
    try {
      const raw = await fs.readFile(convoPath, 'utf-8')
      conversation = JSON.parse(raw).messages || []
    } catch {
      console.warn(`Nouvelle conversation : ${conversationId}`)
    }

    const ontology = await fetchOntology()

    const agentRes = await axios.post(AGENT_API_URL, {
      message,
      context: reducedContext,
      history: conversation,
      ontology
    })

    const result = agentRes.data

    const updated = {
      id: conversationId,
      domain,
      messages: [
        ...conversation,
        { sender: 'user', text: message },
        { sender: 'bot', text: result.response }
      ],
      files: result.files || []
    }

    await fs.writeFile(convoPath, JSON.stringify(updated, null, 2))

    res.json({
      response: result.response,
      files: result.files || []
    })
  } catch (err) {
    console.error("Erreur dans handleUserQuery :", err)
    res.status(500).json({ error: 'Internal error' })
  }
}
