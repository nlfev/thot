import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

const LEGAL_DOCUMENT_TYPES = {
  imprint: 'imprint',
  dataProtection: 'data-protection',
  termsOfService: 'terms-of-service',
}

export async function fetchLegalHtml(documentType, language = 'en') {
  const normalizedType = (documentType || '').trim()
  if (!normalizedType) {
    throw new Error('Missing legal document type')
  }

  const url = `${API_BASE_URL}/api/v1/config/legal/${normalizedType}`
  const response = await axios.get(url, {
    params: { lang: language },
    responseType: 'text',
    headers: {
      Accept: 'text/html',
    },
  })

  return typeof response.data === 'string' ? response.data : ''
}

export { LEGAL_DOCUMENT_TYPES }
