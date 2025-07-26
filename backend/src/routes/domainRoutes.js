import express from 'express'
import { listDomains, getDomainContexts } from '../controllers/domainController.js'

const router = express.Router()

router.get('/', listDomains)

router.get('/:domain/contexts', getDomainContexts)

export default router
