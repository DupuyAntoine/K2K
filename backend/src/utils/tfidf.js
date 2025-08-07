import natural from 'natural'
import { franc } from 'franc'
import sw from 'stopword'

const tokenizer = new natural.WordTokenizer()

export function extractKeywordsFromQuery(query) {
  const lang = franc(query)
  const supported = ['en', 'fr', 'es', 'de', 'it']
  const fallbackLang = 'en'

  const queryWords = query.toLowerCase().split(/\W+/)
  const stopwords = supported.includes(lang)
    ? sw[lang] || sw[fallbackLang]
    : sw[fallbackLang]

  const filtered = sw.removeStopwords(queryWords, stopwords)

  return filtered
}

/**
 * Découpe un long texte en segments (chunks) de taille fixe (en mots)
 */
export function chunkText(text, maxWords = 200) {
  const words = text.split(/\s+/)
  const chunks = []
  for (let i = 0; i < words.length; i += maxWords) {
    const chunk = words.slice(i, i + maxWords).join(' ')
    chunks.push(chunk)
  }
  return chunks
}

/**
 * Nettoie et normalise un texte : suppression des URLs, UUIDs, ponctuation,
 * puis tokenisation avec `natural.WordTokenizer`, et recomposition
 */
export function cleanText(text) {
  const cleaned = text
    .replace(/https?:\/\/\S+/g, '') // supprime les URLs
    .replace(/\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/gi, '') // supprime UUIDs
    .replace(/[^\p{L}\p{N}\s]/gu, '') // supprime ponctuation tout en gardant les lettres Unicode
    .toLowerCase()

  const tokens = tokenizer.tokenize(cleaned)
    .filter(token => token.length > 1 && isNaN(token)) // ignore mots trop courts et chiffres

  return tokens.join(' ')
}

/**
 * Construit un modèle TF-IDF avec nettoyage cohérent des documents
 */
export function buildTfidfModel(chunks) {
  const tfidf = new natural.TfIdf()
  chunks.forEach(chunk => {
    const cleaned = cleanText(chunk)
    tfidf.addDocument(cleaned)
  })
  return tfidf
}

/**
 * Sélectionne les chunks les plus pertinents (topN) selon la similarité TF-IDF
 * TODO : amélioration nécessaire de la sélection, voir lib
 */
export function selectRelevantChunks(chunks, query, topN = 10) {
  const tfidf = buildTfidfModel(chunks)
  const cleanedQuery = cleanText(query)
  const tokenizedQuery = tokenizer.tokenize(cleanedQuery).join(' ')
  const keywords = extractKeywordsFromQuery(query)

  const scored = chunks.map((chunk, i) => {
    const baseScore = tfidf.tfidf(tokenizedQuery, i)
    const chunkClean = cleanText(chunk)

    // Boost si le chunk contient des mots-clés importants
    const keywordMatches = keywords.filter(k => chunkClean.includes(k)).length
    const boost = keywordMatches * 25 // pondération ajustable
    const finalScore = baseScore + boost

    return {
      text: chunk,
      score: finalScore,
      keywordsMatched: keywordMatches
    }
  })

  const topChunks = scored
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topN)
    .map(item => item.text)

  debugChunkScores(topChunks, query)

  return topChunks
}


/**
 * Applique chunking + sélection à un contexte brut (JSON/RDF/etc.)
 */
export function extractAndSelectChunksFromContext(rawContext, query, topN = 10) {
  const chunks = []

  for (const key in rawContext) {
    const value = rawContext[key]

    if (typeof value === 'string') {
      chunks.push(...chunkText(value))
    } else if (Array.isArray(value)) {
      for (const row of value) {
        const line = Object.values(row).join(' ')
        chunks.push(...chunkText(line))
      }
    } else if (typeof value === 'object') {
      chunks.push(...chunkText(JSON.stringify(value)))
    }
  }

  return selectRelevantChunks(chunks, query, topN)
}

/**
 * Affiche les scores TF-IDF des chunks pour debug
 */
function debugChunkScores(scoredChunks, query) {
  console.log(`\n🔍 TF-IDF scores for query: "${query}"`)
  const sorted = scoredChunks
    .filter(s => s.score > 0)
    .sort((a, b) => b.score - a.score)
  sorted.forEach(({ score, text }, i) => {
    console.log(`  [${i + 1}] Score: ${score.toFixed(4)} — Preview: "${text.slice(0, 80)}..."`)
  })
}
