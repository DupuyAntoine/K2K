import express from 'express'
import { handleUserQuery } from '../controllers/chatController.js'

const router = express.Router()

router.post('/query', handleUserQuery)

export default router
