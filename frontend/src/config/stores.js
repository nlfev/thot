/**
 * Configuration for frontend stores
 */

export const STORE_CONFIG = {
  // Auth store
  AUTH: {
    TOKEN_KEY: 'access_token',
    REFRESH_TOKEN_KEY: 'refresh_token',
    USER_DATA_KEY: 'user_data',
  },

  // App store
  APP: {
    LANGUAGE_KEY: 'language',
    THEME_KEY: 'theme',
    SIDEBAR_KEY: 'sidebar_open',
  },
}

export default STORE_CONFIG
