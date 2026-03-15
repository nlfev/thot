<template>
  <div class="container">
    <div v-if="isAuthenticated" class="page-header text-center">
      <h1>{{ $t('common.home') }}</h1>
      <p>Welcome, {{ authStore.currentUser?.username }}!</p>
      
      <div v-if="showPendingApprovalNotice && pendingApprovalCount > 0" class="alert alert-info">
        <strong>{{ $t('home.pendingApprovalTitle') }}</strong>
        <p>{{ pendingApprovalMessage }}</p>
        <router-link to="/admin/users" class="btn btn-primary">
          {{ $t('home.viewUsers') }}
        </router-link>
      </div>
    </div>
    <div v-else class="form-container">
      <div class="card form-card">
        <div class="text-center">
          <h1>{{ appName }}</h1>
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
import { useAppStore } from '@/stores/app'
import { userService } from '@/services/user'

export default defineComponent({
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    const appStore = useAppStore()

    return {
      authStore,
      appStore,
    }
  },
  data() {
    return {
      pendingApprovalCount: 0,
    }
  },
  computed: {
    isAuthenticated() {
      return this.authStore.isAuthenticated
    },
    appName() {
      return this.appStore.getConfig('appName', APP_CONFIG.appName)
    },
    showPendingApprovalNotice() {
      return this.authStore.hasRole('support') || this.authStore.hasRole('admin')
    },
    pendingApprovalMessage() {
      const key = this.pendingApprovalCount === 1
        ? 'home.pendingApprovalMessageOne'
        : 'home.pendingApprovalMessageOther'

      return this.$t(key, { count: this.pendingApprovalCount })
    },
  },
  async mounted() {
    if (this.showPendingApprovalNotice) {
      await this.loadPendingApprovalCount()
    }
  },
  methods: {
    async loadPendingApprovalCount() {
      try {
        const data = await userService.getPendingApprovalCount()
        this.pendingApprovalCount = data.pending_approval_count || 0
      } catch (error) {
        console.error('Failed to load pending approval count:', error)
      }
    },
  },
})
</script>

<style scoped>
.alert strong {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.alert p {
  margin-bottom: 1rem;
}
</style>
