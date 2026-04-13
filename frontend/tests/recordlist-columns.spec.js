import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import RecordList from '../src/views/records/RecordList.vue'
vi.mock('../src/services/record', () => ({
  recordService: {
    getRecords: vi.fn(() => Promise.resolve({ data: [], total: 0 })),
    deleteRecord: vi.fn(() => Promise.resolve()),
  },
}))
import { createPinia, setActivePinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import { messages } from '../src/locales/messages'
import { useAuthStore } from '../src/stores/auth'

function createI18nInstance(locale = 'en') {
  return createI18n({
    legacy: false,
    locale,
    fallbackLocale: 'en',
    messages,
  })
}

describe('RecordList.vue role-based columns', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  function mountWithRole(role) {
    const authStore = useAuthStore()
    authStore.user = { roles: [role] }
    authStore.token = 'token'
    return mount(RecordList, {
      global: {
        plugins: [createI18nInstance()],
        mocks: {
          $t: (msg, vars) => (vars ? `${msg} ${JSON.stringify(vars)}` : msg),
        },
      },
      data() {
        return {
          records: [
            { id: 1, title: 'Test', loantype: 'Book', loantype_subtype: 'Short', restriction: 'None' },
          ],
          loading: false,
        }
      },
    })
  }

  it('shows only loantype for normal user', async () => {
    const wrapper = mountWithRole('user')
    await flushPromises()
    console.log(wrapper.html())
    expect(wrapper.html()).toContain('Book')
    expect(wrapper.html()).not.toContain('Book - Short')
  })

  it('shows loantype and subtype combined for admin', async () => {
    const wrapper = mountWithRole('admin')
    await flushPromises()
    expect(wrapper.html()).toContain('Book - Short')
  })

  it('shows loantype and subtype combined for user_bibl', async () => {
    const wrapper = mountWithRole('user_bibl')
    await flushPromises()
    expect(wrapper.html()).toContain('Book - Short')
  })
})
