import axios from 'axios';

const API_URL = "http://localhost:4000/api/query"
const EVAL_URL = "http://localhost:4000/api/eval"

export const fetch = async (req) => {
  try {
    // Appel à l'API backend
    const response = await axios.get(API_URL, {
      params: { request: req }
    })
    return response.data
  } catch (error) {
    console.error("Erreur lors de l'appel à l'API:", error)
  }
}

export const evaluation = async () => {
  try {
    const response = await axios.get(EVAL_URL)
    return response
  } catch (error) {
    console.error("Erreur lors de l'appel à l'API:", error)
  }
}
