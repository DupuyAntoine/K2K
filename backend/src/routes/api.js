import express from 'express';
import { processQuestion } from '../services/agentService.js';

const router = express.Router();

// Route pour traiter la requête utilisateur
router.get('/query', async (req, res, next) => {
  try {
    const { request } = req.query;
    
    // Appel à l'agent IA pour traiter la question
    const aiResponse = await processQuestion(request);
    
    // Réponse agrégée
    res.json({
      request,
      aiResponse
    });
  } catch (error) {
    next(error);
  }
});

export default router;
