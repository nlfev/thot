import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

async function navigateTo(path) {
  await router.push(path)
  await router.isReady()
}

describe('record access routes', () => {
  beforeEach(async () => {
    setActivePinia(createPinia())
    localStorage.clear()

    const authStore = useAuthStore()
    authStore.token = 'test-token'
    authStore.user = {
      id: 'user-1',
      username: 'reader',
      roles: ['user'],
      permissions: [],
    }

    await router.push('/')
  })

  it('allows a regular authenticated user to open a record detail route', async () => {
    await navigateTo('/records/123')

    expect(router.currentRoute.value.fullPath).toBe('/records/123')
  })

  it('keeps record creation blocked for a regular authenticated user', async () => {
    await navigateTo('/records/new')

    expect(router.currentRoute.value.name).toBe('Home')
  })
})