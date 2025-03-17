import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'
import apiRoutes from './routes/api.js'

const app = express();
const PORT = process.env.PORT || 4000

// Middlewares
app.use(cors());
app.use(bodyParser.json())

// Routes de l'API
app.use('/api', apiRoutes)

// Gestion globale des erreurs
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).json({ error: 'Erreur interne du serveur' })
});

app.listen(PORT, () => {
  console.log(`Backend Node.js en écoute sur le port ${PORT}`)
});
