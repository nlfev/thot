<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-left">
        <span v-if="authStore.isAuthenticated">
          {{ authStore.currentUser?.username }} ({{ authStore.currentUser?.roles?.join(', ') }})
        </span>
        <span v-else>
          {{ $t('common.login') }}
        </span>
      </div>
      <div class="footer-right">
        <span>© {{ currentYear }} . {{ $t('common.copyright', { year: currentYear, company: appConfig.companyName }) }} powered by {{ appConfig.companyName }}</span>
      </div>
    </div>
  </footer>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { APP_CONFIG } from '@/config/app'

export default defineComponent({
  name: 'AppFooter',
  setup() {
    const authStore = useAuthStore()

    return {
      authStore,
      appConfig: APP_CONFIG,
      currentYear: new Date().getFullYear(),
    }
  },
})
</script>

<style scoped>
.app-footer {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
  border-top: 1px solid #ddd;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
}
</style>
