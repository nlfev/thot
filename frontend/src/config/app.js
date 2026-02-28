/**
 * Global Application Configuration Defaults
 *
 * These are fallback defaults used when:
 * 1. Backend config endpoint is unavailable
 * 2. App is loading before config is fetched
 *
 * Production values should be set on the backend via /api/config endpoint
 */

export const APP_CONFIG = {
  appName: 'NLF Database',
  appVersion: '1.0.0',
  companyName: 'Your Company',
  logoUrl: '/logo.png',
  copyrightYear: 2026,

  // UI
  itemsPerPageDefault: 10,
  itemsPerPageOptions: [10, 20, 50],

  // Security
  tokenRefreshIntervalMinutes: 55, // Refresh token 5 minutes before expiry
  sessionTimeoutMinutes: 60,

  // Features
  features: {
    otp: true,
    emailVerification: true,
    corporateApprovals: true,
  },

  // Languages
  languages: {
    en: 'English',
    de: 'Deutsch',
  },
  defaultLanguage: 'en',
}

export default APP_CONFIG
