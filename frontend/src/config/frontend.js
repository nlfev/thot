/**
 * Frontend Configuration
 *
 * This file provides minimal client-side configuration.
 * Most application settings are loaded dynamically from the backend
 * via GET /api/v1/config endpoint and stored in the app store.
 *
 * Use `useAppStore()` to access all configuration values in components.
 */

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export const FRONTEND_CONFIG = {
  // API Configuration
  API_BASE_URL,
  API_V1_URL: `${API_BASE_URL}/api/v1`,

  // Backend configuration endpoint
  // All other config values come from here
  CONFIG_ENDPOINT: `${API_BASE_URL}/api/v1/config`,
}

export default FRONTEND_CONFIG