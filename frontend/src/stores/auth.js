/**
 * Pinia Store for Authentication
 */

import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    isLoading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
    hasRole: (state) => (role) => state.user?.roles.includes(role) ?? false,
    hasPermission: (state) => (permission) => state.user?.permissions.includes(permission) ?? false,
  },

  actions: {
    async login(username, password, otpCode = null) {
      this.isLoading = true
      this.error = null

      try {
        const response = await api.post('/auth/login', {
          username,
          password,
          otp_code: otpCode,
        })

        this.token = response.data.access_token
        this.user = response.data.user
        localStorage.setItem('access_token', this.token)
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed'
        return false
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('access_token')
      delete api.defaults.headers.common['Authorization']
    },

    async register(username, email, tosAgreed, language = 'en') {
      this.isLoading = true
      this.error = null

      try {
        const response = await api.post('/auth/register', {
          username,
          email,
          tos_agreed: tosAgreed,
          language: language,
        })
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Registration failed'
        throw error.response?.data || error
      } finally {
        this.isLoading = false
      }
    },

    async resetPassword(username) {
      this.isLoading = true
      this.error = null

      try {
        await api.post('/auth/password-reset', { username })
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Password reset failed'
        return false
      } finally {
        this.isLoading = false
      }
    },

    async fetchUser() {
      if (!this.token) {
        return false
      }

      try {
        const response = await api.get('/users/profile')
        this.user = response.data
        return true
      } catch (error) {
        // Token might be invalid, clear it
        this.logout()
        return false
      }
    },

    clearError() {
      this.error = null
    },
  },
})
