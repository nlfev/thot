<template>
  <div class="auth-container">
    <div class="card form-card">
      <h2>{{ $t('auth.registerTitle') }}</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">{{ $t('common.username') }}</label>
          <input v-model="form.username" type="text" id="username" required />
          <small>{{ $t('auth.usernameHint') }}</small>
        </div>
        <div class="form-group">
          <label for="email">{{ $t('common.email') }}</label>
          <input v-model="form.email" type="email" id="email" required />
        </div>
        <div class="checkbox-group">
          <label for="tos" class="checkbox-label">
            <input v-model="form.tosAgreed" type="checkbox" id="tos" required />
            <span>{{ $t('auth.tosAgree') }}</span>
          </label>
          <a href="/terms-of-service" target="_blank">{{ $t('auth.tosLink') }}</a>
        </div>
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? $t('common.loading') : $t('common.register') }}
        </button>
      </form>
      <p class="text-center mt-3">
        {{ $t('auth.alreadyHaveAccount') }}
        <router-link to="/auth/login">{{ $t('common.login') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default defineComponent({
  name: 'Register',
  setup() {
    const authStore = useAuthStore()

    return {
      authStore,
      form: {
        username: '',
        email: '',
        tosAgreed: false,
      },
      isLoading: false,
    }
  },
  methods: {
    async handleRegister() {
      this.isLoading = true

      const success = await this.authStore.register(
        this.form.username,
        this.form.email,
        this.form.tosAgreed
      )

      if (success) {
        this.$t('messages.registrationSuccess')
        this.$router.push('/auth/login')
      }

      this.isLoading = false
    },
  },
})
</script>

<style scoped>
/* Additional component-specific styles if needed */
</style>
