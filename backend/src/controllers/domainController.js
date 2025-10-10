import path from 'path'
import fs from 'fs'

const BASE_DOMAIN_DIR = path.resolve('data')

// Not used anymore
export async function getDomainContexts(req, res) {
  try {
    const entries = await fs.readdir(BASE_DOMAIN_DIR, { withFileTypes: true })

    const domains = await Promise.all(
      entries
        .filter((entry) => entry.isDirectory())
        .map(async (dir) => {
          const domainPath = path.join(BASE_DOMAIN_DIR, dir.name)
          const contextPath = path.join(domainPath, 'contexts')

          let meta = {
            label: dir.name,
            description: 'No description provided.'
          }

          try {
            const metaContent = await fs.readFile(
              path.join(domainPath, 'meta.json'),
              'utf-8'
            )
            meta = JSON.parse(metaContent)
          } catch (err) {
            console.warn(`No meta.json found for domain '${dir.name}'`)
          }

          let supportedFiles = []
          try {
            const files = await fs.readdir(contextPath)
            supportedFiles = files.filter((f) =>
              /\.(json|csv|ttl|rdf|xml)$/i.test(f)
            )
          } catch (err) {
            console.warn(`No contexts folder or failed to read: ${contextPath}`)
          }

          return {
            id: dir.name,
            label: meta.label,
            description: meta.description,
            files: supportedFiles
          }
        })
    )

    res.json(domains)
  } catch (err) {
    console.error('Error listing domains:', err)
    res.status(500).json({ error: 'Failed to list domains' })
  }
}

export function listDomains(req, res) {
  const domainDirs = fs.readdirSync(BASE_DOMAIN_DIR).filter(name =>
    fs.statSync(path.join(BASE_DOMAIN_DIR, name)).isDirectory()
  )

  const domains = domainDirs.map(domain => {
    const metaPath = path.join(BASE_DOMAIN_DIR, domain, 'meta.json')
    if (fs.existsSync(metaPath)) {
      const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'))
      return { ...meta, id: domain }
    }
    return { id: domain, label: domain }
  })

  res.json(domains)
}
