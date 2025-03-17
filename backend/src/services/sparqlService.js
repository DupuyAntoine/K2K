import axios from 'axios'


const ENDPOINT_URL = process.env.ENDPOINT_URL || 'http://localhost:8890'

export const selectAll = async () => {
  try {
    const query = `
      SELECT  ?s ?p ?o
      WHERE {
        ?s ?p ?o
      }
    `
    const params={
      "default-graph": "", "should-sponge": "soft", "query": query,
      "debug": "on", "timeout": "", "format": "application/sparql-results+json",
      "save": "display", "fname": ""
    }

    let querypart="";
    for(let k in params) {
      querypart+=k+"="+encodeURIComponent(params[k])+"&"
    }
    
    const request = ENDPOINT_URL + '?' + querypart;
    const response = await axios.get(request, { query })
    return response.data;
  } catch (error) {
    console.error("Erreur lors de l'appel à l'agent IA:", error)
    throw error
  }
}
