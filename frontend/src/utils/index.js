/**
 * Utility functions for the frontend
 */

export const formatDate = (date, locale = 'en') => {
  if (!date) return ''
  const dateObj = new Date(date)
  return dateObj.toLocaleDateString(locale)
}

export const formatDateTime = (date, locale = 'en') => {
  if (!date) return ''
  const dateObj = new Date(date)
  return dateObj.toLocaleString(locale)
}

export const truncateString = (str, length = 50) => {
  if (!str) return ''
  return str.length > length ? str.substring(0, length) + '...' : str
}

export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export const validatePassword = (password) => {
  // At least 10 characters, 1 uppercase, 1 lowercase, 1 digit or special char
  const minLength = password.length >= 10
  const hasUppercase = /[A-Z]/.test(password)
  const hasLowercase = /[a-z]/.test(password)
  const hasDigitOrSpecial = /[\d!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)

  return minLength && hasUppercase && hasLowercase && hasDigitOrSpecial
}

export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

export const sleep = (ms) => {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export default {
  formatDate,
  formatDateTime,
  truncateString,
  validateEmail,
  validatePassword,
  debounce,
  sleep,
}
