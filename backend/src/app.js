import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'
import chatRoutes from './routes/chatRoutes.js'
import conversationRoutes from './routes/conversationRoutes.js'
import domainRoutes from './routes/domainRoutes.js'

const app = express();
const PORT = process.env.PORT || 4000

// Middlewares
app.use(cors())
app.use(bodyParser.json())

// Routes de l'API
app.use('/api/chat', chatRoutes)
app.use('/api/conversations', conversationRoutes)
app.use('/api/domains', domainRoutes)

// Gestion globale des erreurs
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).json({ error: 'Erreur interne du serveur' })
})

app.listen(PORT, () => {
  console.log(`Backend Node.js en écoute sur le port ${PORT}`)
})
