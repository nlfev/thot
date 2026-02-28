<template>
  <div class="view-wrapper">
    <div class="view-header">
      <h1>{{ $t('admin.userManagement') }}</h1>
    </div>
    <div class="view-content card">
      <!-- User list and management will be implemented here -->
      <p>User management interface for support/admin roles</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default defineComponent({
  name: 'UserManagement',
  setup() {
    const authStore = useAuthStore()

    return {
      authStore,
    }
  },
})
</script>

<style scoped>
</style>
