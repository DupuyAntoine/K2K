import express from 'express';
import { processQuestion, processResponse } from '../services/agentService.js';
import { selectAll } from '../services/sparqlService.js';
// import { processQuestion } from '../services/resourceService.js';

const router = express.Router();

// Route pour traiter la requête utilisateur
router.get('/query', async (req, res, next) => {
  try {
    const { request } = req.query

    const { graph } = await selectAll()

    // Appel aux agents IA pour traiter la question
    const interactionResults = await processQuestion(request, graph)
    const response = await processResponse(interactionResults)
    
    // Réponse agrégée
    res.json({
      response
    });
  } catch (error) {
    next(error)
  }
});

export default router
