/**
 * Service for Authentication API calls
 */

import api from './api'

export const authService = {
  /**
   * Register new user
   */
  async register(username, email, tosAgreed) {
    try {
      const response = await api.post('/auth/register', {
        username,
        email,
        tos_agreed: tosAgreed,
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Complete registration with password
   */
  async completeRegistration(token, data) {
    try {
      const response = await api.post(`/auth/register/confirm/${token}`, {
        first_name: data.firstName,
        last_name: data.lastName,
        password: data.password,
        password_confirm: data.passwordConfirm,
        corporate_number: data.corporateNumber,
        enable_otp: data.enableOTP || false,
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Login user
   */
  async login(username, password, otpCode = null) {
    try {
      const response = await api.post('/auth/login', {
        username,
        password,
        otp_code: otpCode,
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Logout user
   */
  async logout() {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    }
  },

  /**
   * Refresh access token
   */
  async refreshToken() {
    try {
      const response = await api.post('/auth/refresh')
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Request password reset
   */
  async requestPasswordReset(email) {
    try {
      const response = await api.post('/auth/password-reset', {
        email,
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Confirm password reset
   */
  async confirmPasswordReset(token, newPassword) {
    try {
      const response = await api.post(
        `/auth/password-reset/confirm/${token}`,
        {
          new_password: newPassword,
          new_password_confirm: newPassword,
        }
      )
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },
}

export default authService
