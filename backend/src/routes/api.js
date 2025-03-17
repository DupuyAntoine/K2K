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
    console.log(graph)
    // Appel à l'agent IA pour traiter la question
    const responseInteraction = await processQuestion(request, graph)
    const responseConstruction = await processResponse(request)
    
    // Réponse agrégée
    res.json({
      request,
      responseInteraction,
      responseConstruction
    });
  } catch (error) {
    next(error)
  }
});

export default router
