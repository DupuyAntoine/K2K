import axios from 'axios'

// URL de l'agent IA (microservice). La variable d'environnement AGENT_URL permet de la configurer.
const AGENT_URL = process.env.AGENT_URL || 'http://localhost:5000'

export const processQuestion = async (request, graph) => {
  try {
    const response = await axios.post(`${AGENT_URL}/interact`, { request, graph })
    return response.data
  } catch (error) {
    console.error("Erreur lors de l'appel à l'agent IA:", error);
    throw error
  }
};

export const processResponse = async (request) => {
  try {
    const response = await axios.post(`${AGENT_URL}/response`, { request })
    return response.data
  } catch (error) {
    console.error("Erreur lors de l'appel à l'agent IA:", error)
    throw error
  }
};
