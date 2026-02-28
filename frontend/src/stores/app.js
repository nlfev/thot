/**
 * Pinia Store for UI/App state and global configuration
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchAppConfig } from '@/services/config'

export const useAppStore = defineStore('app', () => {
  // UI State
  const currentLanguage = ref(localStorage.getItem('language') || 'en')
  const isDarkMode = ref(localStorage.getItem('darkMode') === 'true' || false)
  const sidebarOpen = ref(true)
  const currentPage = ref(1)

  // Configuration State
  const appConfig = ref(null)
  const isConfigLoaded = ref(false)
  const configError = ref(null)
  const itemsPerPage = computed(() => appConfig.value?.itemsPerPageDefault || 10)

  // Getters
  const language = computed(() => currentLanguage.value)
  const config = computed(() => appConfig.value)

  // Actions - UI
  function setLanguage(language) {
    currentLanguage.value = language
    localStorage.setItem('language', language)
    document.documentElement.lang = language
  }

  function toggleDarkMode() {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('darkMode', isDarkMode.value)
  }

  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value
  }

  function setCurrentPage(page) {
    currentPage.value = page
  }

  // Actions - Configuration
  async function initializeConfig() {
    if (isConfigLoaded.value) return // Prevent duplicate loads

    try {
      appConfig.value = await fetchAppConfig()
      isConfigLoaded.value = true
      configError.value = null
    } catch (error) {
      configError.value = error.message
      isConfigLoaded.value = true
      console.error('Failed to initialize app config:', error)
    }
  }

  function getConfig(key, defaultValue = null) {
    if (!appConfig.value) return defaultValue
    return appConfig.value[key] ?? defaultValue
  }

  return {
    // UI State
    currentLanguage,
    isDarkMode,
    sidebarOpen,
    currentPage,
    itemsPerPage,
    // Config State
    appConfig,
    isConfigLoaded,
    configError,
    // Getters
    language,
    config,
    // UI Actions
    setLanguage,
    toggleDarkMode,
    toggleSidebar,
    setCurrentPage,
    // Config Actions
    initializeConfig,
    getConfig,
  }
})

