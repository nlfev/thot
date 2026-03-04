<template>
  <div class="auth-container">
    <div class="card form-card">
      <h2>{{ $t('auth.passwordReset') }}</h2>
      <form @submit.prevent="handlePasswordReset">
        <div class="form-group">
          <label for="username">{{ $t('common.username') }}</label>
          <input v-model="form.username" type="text" id="username" required />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="isLoading">
          {{ isLoading ? $t('common.loading') : $t('common.submit') }}
        </button>
      </form>
      <p class="text-center mt-3">
        <router-link to="/auth/login">{{ $t('common.login') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default defineComponent({
  name: 'PasswordReset',
  setup() {
    const authStore = useAuthStore()

    return {
      authStore,
      form: {
        username: '',
      },
      isLoading: false,
    }
  },
  methods: {
    async handlePasswordReset() {
      this.isLoading = true

      const success = await this.authStore.resetPassword(this.form.username)

      if (success) {
        alert(this.$t('auth.resetEmailSent'))
      }

      this.isLoading = false
    },
  },
})
</script>

<style scoped>
</style>
