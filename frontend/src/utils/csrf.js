// src/utils/csrf.js
// Utility to read CSRF token from cookie
export function getCsrfToken() {
  const match = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/)
  return match ? decodeURIComponent(match[1]) : null
}
