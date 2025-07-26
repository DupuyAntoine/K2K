import express from 'express'
import { getConversationsByDomain, createConversation } from '../controllers/conversationController.js'

const router = express.Router()

router.get('/:domain', getConversationsByDomain)

router.post('/', createConversation)

export default router
