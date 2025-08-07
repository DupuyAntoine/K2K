import axios from 'axios'

const SPARQL_ENDPOINT = process.env.ENDPOINT_URL
const SPARQL_GRAPH = 'http://k2000.org/graph'

export async function runSparqlQuery(query) {
  const headers = {
    'Content-Type': 'application/sparql-query',
    'Accept': 'application/sparql-results+json'
  }

  const res = await axios.post(SPARQL_ENDPOINT, query, { headers })
  return res.data?.results?.bindings || []
}

function deduplicateByTriple(items) {
  const seen = new Map()
  for (const item of items) {
    const key = [item.uri, item.domain, item.range].filter(Boolean).join('|')
    if (!seen.has(key)) {
      seen.set(key, item)
    }
  }
  return Array.from(seen.values())
}

export async function fetchOntology() {
  try {
    const preferredLangs = ['en', 'fr']

    const classQuery = `
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT DISTINCT ?class ?label FROM <${SPARQL_GRAPH}> WHERE {
        ?class a owl:Class .
        OPTIONAL { ?class rdfs:label ?label . }
        OPTIONAL { ?class rdfs:comment ?description . }
      }
    `

    const objPropQuery = `
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT DISTINCT ?property ?domain ?range ?label FROM <${SPARQL_GRAPH}> WHERE {
        ?property a owl:ObjectProperty .
        OPTIONAL { ?property rdfs:domain ?domain . }
        OPTIONAL { ?property rdfs:range ?range . }
        OPTIONAL { ?property rdfs:label ?label . }
        OPTIONAL { ?class rdfs:comment ?description . }
      }
    `

    const dataPropQuery = `
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT DISTINCT ?property ?domain ?range ?label FROM <${SPARQL_GRAPH}> WHERE {
        ?property a owl:DatatypeProperty .
        OPTIONAL { ?property rdfs:domain ?domain . }
        OPTIONAL { ?property rdfs:range ?range . }
        OPTIONAL { ?property rdfs:label ?label . }
        OPTIONAL { ?class rdfs:comment ?description . }
      }
    `

    const [classResults, objPropResults, dataPropResults] = await Promise.all([
      runSparqlQuery(classQuery),
      runSparqlQuery(objPropQuery),
      runSparqlQuery(dataPropQuery)
    ])

    function filterLiteralsByLang(results, uriKey, literalKey) {
      const map = new Map()

      for (const item of results) {
        const uri = item[uriKey]?.value
        const literal = item[literalKey]

        if (!uri || !literal) continue
        const existing = map.get(uri)

        const currentLang = existing?.['xml:lang'] || ''
        const currentIndex = preferredLangs.indexOf(currentLang)
        const newLang = literal['xml:lang'] || ''
        const newIndex = preferredLangs.indexOf(newLang)

        if (!existing || (newIndex !== -1 && (currentIndex === -1 || newIndex < currentIndex))) {
          map.set(uri, literal)
        }
      }

      return map
    }

    const classLabelMap = filterLiteralsByLang(classResults, 'class', 'label')
    const classDescMap  = filterLiteralsByLang(classResults, 'class', 'description')
    const objLabelMap   = filterLiteralsByLang(objPropResults, 'property', 'label')
    const objDescMap    = filterLiteralsByLang(objPropResults, 'property', 'description')
    const dataLabelMap  = filterLiteralsByLang(dataPropResults, 'property', 'label')
    const dataDescMap   = filterLiteralsByLang(dataPropResults, 'property', 'description')

    const ontology = {
      classes: deduplicateByTriple(classResults
        .map(({ class: c }) => ({
          uri: c?.value,
          label: classLabelMap.get(c?.value)?.value || null,
          description: classDescMap.get(c?.value)?.value || null
        }))
        .filter(item => !!item.uri)
      ),

      objectProperties: deduplicateByTriple(objPropResults
        .map(({ property, domain, range }) => ({
          uri: property?.value,
          domain: domain?.value || null,
          range: range?.value || null,
          label: objLabelMap.get(property?.value)?.value || null,
          description: objDescMap.get(property?.value)?.value || null
        }))
        .filter(item => !!item.uri)
      ),

      dataProperties: deduplicateByTriple(dataPropResults
        .map(({ property, domain, range }) => ({
          uri: property?.value,
          domain: domain?.value || null,
          range: range?.value || null,
          label: dataLabelMap.get(property?.value)?.value || null,
          description: dataDescMap.get(property?.value)?.value || null
        }))
        .filter(item => !!item.uri)
      )
    }

    return summarizeOntology(ontology)
  } catch (error) {
    console.error("Erreur lors de l'extraction de l'ontologie :", error)
    return {
      classes: [],
      objectProperties: [],
      dataProperties: []
    }
  }
}

export function summarizeOntology(fullOntology) {
  function truncate(text, maxLength = 120) {
    if (!text) return null
    return text.length <= maxLength ? text : text.slice(0, maxLength).trim() + '...'
  }

  function extractLocalName(uri) {
    if (!uri) return null
    const match = uri.match(/[#\/]([^#\/]+)$/)
    return match ? match[1] : uri
  }

  function isUseful(item) {
    return item.label || extractLocalName(item.uri)
  }

  function compactClass(c) {
    if (!isUseful(c)) return null
    return {
      label: c.label || extractLocalName(c.uri),
      description: truncate(c.description)
    }
  }

  function compactProperty(p) {
    if (!isUseful(p)) return null
    return {
      label: p.label || extractLocalName(p.uri),
      domain: extractLocalName(p.domain),
      range: extractLocalName(p.range),
      description: truncate(p.description)
    }
  }

  return {
    classes: fullOntology.classes.map(compactClass).filter(Boolean),
    objectProperties: fullOntology.objectProperties.map(compactProperty).filter(Boolean),
    dataProperties: fullOntology.dataProperties.map(compactProperty).filter(Boolean)
  }
}
