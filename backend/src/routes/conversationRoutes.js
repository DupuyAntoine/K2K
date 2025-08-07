import express from 'express'
import { getConversationsByDomain, createConversation, getConversationById } from '../controllers/conversationController.js'

const router = express.Router()

router.get('/:domain', getConversationsByDomain)
router.get('/:domain/:id', getConversationById)
router.post('/', createConversation)

export default router
