<template>
  <div class="view-wrapper">
    <div class="view-header">
      <h1>{{ $t('user.profile') }}</h1>
    </div>
    <div class="view-content card">
      <p v-if="user">Welcome, {{ user.first_name }} {{ user.last_name }}</p>
      <!-- Profile form will be implemented here -->
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default defineComponent({
  name: 'UserProfile',
  setup() {
    const authStore = useAuthStore()

    return {
      user: authStore.currentUser,
    }
  },
})
</script>

<style scoped>
</style>
