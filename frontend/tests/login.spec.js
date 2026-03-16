import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createI18n } from 'vue-i18n'

import Login from '@/views/auth/Login.vue'
import { messages } from '@/locales/messages'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

function createI18nInstance() {
  return createI18n({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages,
  })
}

describe('Login view register link visibility', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('shows register link when closed registration is disabled', () => {
    const appStore = useAppStore()
    appStore.appConfig = {
      features: {
        closedRegistration: false,
      },
    }

    const wrapper = mount(Login, {
      global: {
        plugins: [createI18nInstance()],
        mocks: {
          $route: { query: {} },
          $router: { push: vi.fn() },
        },
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    })

    expect(wrapper.text()).toContain('Register')
  })

  it('hides register link when closed registration is enabled', () => {
    const appStore = useAppStore()
    appStore.appConfig = {
      features: {
        closedRegistration: true,
      },
    }

    const wrapper = mount(Login, {
      global: {
        plugins: [createI18nInstance()],
        mocks: {
          $route: { query: {} },
          $router: { push: vi.fn() },
        },
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    })

    expect(wrapper.text()).not.toContain('Register')
  })
})

describe('Login error messaging', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  function mountLogin() {
    const appStore = useAppStore()
    appStore.appConfig = {
      features: {
        closedRegistration: false,
      },
    }

    return mount(Login, {
      global: {
        plugins: [createI18nInstance()],
        mocks: {
          $route: { query: {} },
          $router: { push: vi.fn() },
        },
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    })
  }

  it('shows temporary lock message when backend returns lock detail', async () => {
    const authStore = useAuthStore()
    authStore.login = vi.fn(async () => {
      authStore.error = 'Login temporarily locked. Please try again later'
      return false
    })

    const wrapper = mountLogin()

    wrapper.vm.form.username = 'locked-user'
    wrapper.vm.form.password = 'wrong-password'
    await wrapper.vm.handleLogin()

    expect(wrapper.text()).toContain('Login temporarily locked. Please try again later.')
    expect(wrapper.text()).not.toContain('Login failed. Please check your credentials and try again.')
  })

  it('shows generic message for all non-lock login failures', async () => {
    const authStore = useAuthStore()
    authStore.login = vi.fn(async () => {
      authStore.error = 'Invalid username or password'
      return false
    })

    const wrapper = mountLogin()

    wrapper.vm.form.username = 'wrong-user'
    wrapper.vm.form.password = 'wrong-password'
    await wrapper.vm.handleLogin()

    expect(wrapper.text()).toContain('Login failed. Please check your credentials and try again.')
    expect(wrapper.text()).not.toContain('Login temporarily locked. Please try again later.')
  })
})
