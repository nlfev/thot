import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import { nextTick } from 'vue'

import Register from '@/views/auth/Register.vue'
import RegisterConfirm from '@/views/auth/RegisterConfirm.vue'
import { messages } from '@/locales/messages'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import authApi from '@/services/auth'

vi.mock('@/services/auth', () => ({
  default: {
    getRegistrationConfirm: vi.fn(),
    confirmRegistration: vi.fn(),
  },
}))

function createI18nInstance() {
  return createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages,
  })
}

async function flushPromises() {
  await Promise.resolve()
  await Promise.resolve()
}

describe('Registration flow', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('hides ToS in step 1 during closed registration for support users', async () => {
    const appStore = useAppStore()
    appStore.appConfig = {
      features: {
        closedRegistration: true,
      },
    }

    const authStore = useAuthStore()
    authStore.user = { roles: ['support'] }
    authStore.token = 'token'
    authStore.register = vi.fn().mockResolvedValue({
      expires_in_hours: 24,
      admin: true,
    })

    const push = vi.fn()
    const wrapper = mount(Register, {
      global: {
        plugins: [createI18nInstance()],
        mocks: {
          $router: { push },
        },
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    })

    expect(wrapper.find('#tos').exists()).toBe(false)
    expect(wrapper.text()).toContain('Terms of Service will be confirmed in the next registration step.')

    await wrapper.find('#username').setValue('new-user')
    await wrapper.find('#email').setValue('new@example.com')
    await wrapper.find('form').trigger('submit.prevent')

    expect(authStore.register).toHaveBeenCalledWith('new-user', 'new@example.com', false, 'en')
    expect(push).toHaveBeenCalledWith({
      name: 'RegisterPending',
      query: {
        username: 'new-user',
        email: 'new@example.com',
        expiresInHours: '24',
        admin: 'true',
      },
    })
  })

  it('requires and submits ToS in confirmation step for admin registrations', async () => {
    authApi.getRegistrationConfirm.mockResolvedValue({
      data: {
        username: 'invited-user',
        email: 'invited@example.com',
        admin: true,
      },
    })
    authApi.confirmRegistration.mockResolvedValue({ data: {} })

    const push = vi.fn()
    const wrapper = mount(RegisterConfirm, {
      global: {
        plugins: [createI18nInstance()],
        mocks: {
          $route: { params: { token: 'confirm-token' } },
          $router: { push },
        },
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    })

    await flushPromises()
    await nextTick()

    expect(wrapper.vm.loading).toBe(false)
    expect(wrapper.vm.registrationData.admin).toBe(true)
    expect(wrapper.find('#tosAgreed').exists()).toBe(true)

    await wrapper.find('#firstName').setValue('Invited')
    await wrapper.find('#lastName').setValue('User')
    await wrapper.find('#password').setValue('ValidPass123!')
    await wrapper.find('#passwordConfirm').setValue('ValidPass123!')
    await wrapper.find('#tosAgreed').setValue(true)
    await wrapper.find('form').trigger('submit.prevent')

    expect(authApi.confirmRegistration).toHaveBeenCalledWith('confirm-token', expect.objectContaining({
      tos_agreed: true,
    }))
    expect(push).toHaveBeenCalledWith('/auth/login')
  })
})