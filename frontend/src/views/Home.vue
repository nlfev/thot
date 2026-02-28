<template>
  <div class="container">
    <div v-if="isAuthenticated" class="page-header text-center">
      <h1>{{ $t('common.home') }}</h1>
      <p>Welcome, {{ authStore.currentUser?.username }}!</p>
    </div>
    <div v-else class="form-container">
      <div class="card form-card">
        <div class="text-center">
          <h1>{{ appConfig.appName }}</h1>
          <p class="mb-4">Professional Database Management System</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { APP_CONFIG } from '@/config/app'

export default defineComponent({
  name: 'Home',
  setup() {
    const authStore = useAuthStore()

    return {
      authStore,
      appConfig: APP_CONFIG,
    }
  },
  computed: {
    isAuthenticated() {
      return this.authStore.isAuthenticated
    },
  },
})
</script>

<style scoped>
.btn {
  display: inline-block;
  margin: 0.5rem;
}
</style>
