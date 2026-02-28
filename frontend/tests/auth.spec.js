// """
// Tests for Auth Store
// """

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('should initialize with no user', () => {
    const store = useAuthStore()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('should check if authenticated', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)

    store.token = 'test-token'
    expect(store.isAuthenticated).toBe(true)
  })

  it('should check if user has role', () => {
    const store = useAuthStore()
    store.user = {
      id: '123',
      username: 'testuser',
      roles: ['admin', 'user'],
      permissions: [],
    }

    expect(store.hasRole('admin')).toBe(true)
    expect(store.hasRole('support')).toBe(false)
  })

  it('should check if user has permission', () => {
    const store = useAuthStore()
    store.user = {
      id: '123',
      username: 'testuser',
      roles: [],
      permissions: ['user:read', 'user:write'],
    }

    expect(store.hasPermission('user:read')).toBe(true)
    expect(store.hasPermission('admin:write')).toBe(false)
  })

  it('should logout', () => {
    const store = useAuthStore()
    store.token = 'test-token'
    store.user = { id: '123', username: 'testuser' }

    store.logout()

    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(localStorage.getItem('access_token')).toBeNull()
  })
})
