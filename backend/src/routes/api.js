import express from 'express';
import { processQuestion, processExtract, processResponse, processEval } from '../services/agentService.js';
import { selectAll } from '../services/sparqlService.js';
// import { processQuestion } from '../services/resourceService.js';

const router = express.Router();

// Route pour traiter la requête utilisateur
router.get('/query', async (req, res, next) => {
  try {
    const { request } = req.query

    const { graph } = await selectAll()

    // Appel aux agents IA pour traiter la question
    const interaction = await processQuestion(request, graph)
    const files = await processExtract(interaction, graph)
    const response = await processResponse(interaction, files)

    // Réponse agrégée
    res.json({
      response
    })
  } catch (error) {
    next(error)
  }
})

router.get('/eval', async (req, res, next) => {
  try {
    const { graph } = await selectAll()

    // Appel aux agents IA pour traiter la question
    const response = await processEval(graph)

    // Réponse agrégée
    res.json({
      response
    })
  } catch (error) {
    next(error)
  }
})

export default router
