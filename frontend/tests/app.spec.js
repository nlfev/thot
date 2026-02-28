// """
// Tests for App Store
// """

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAppStore } from '@/stores/app'

describe('App Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('should initialize with default language', () => {
    const store = useAppStore()
    expect(store.currentLanguage).toBe('en')
  })

  it('should set language', () => {
    const store = useAppStore()
    store.setLanguage('de')

    expect(store.currentLanguage).toBe('de')
    expect(localStorage.getItem('language')).toBe('de')
  })

  it('should toggle dark mode', () => {
    const store = useAppStore()
    expect(store.isDarkMode).toBe(false)

    store.toggleDarkMode()
    expect(store.isDarkMode).toBe(true)
    expect(localStorage.getItem('darkMode')).toBe('true')
  })

  it('should set items per page', () => {
    const store = useAppStore()
    store.setItemsPerPage(20)
    expect(store.itemsPerPage).toBe(20)
  })

  it('should set current page', () => {
    const store = useAppStore()
    store.setCurrentPage(3)
    expect(store.currentPage).toBe(3)
  })
})
