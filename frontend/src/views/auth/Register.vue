<template>
  <div class="auth-container">
    <div class="card form-card">
      <h2>{{ $t('auth.registerTitle') }}</h2>
      <div v-if="errorMessage" class="error-box" role="alert">
        {{ errorMessage }}
      </div>
      <div v-if="isClosedRegistration && !canCreateClosedRegistration" class="info-box" role="status">
        <p class="info-title">{{ $t('auth.registrationRestrictedTitle') }}</p>
        <p>{{ $t('auth.registrationRestrictedMessage') }}</p>
        <p>{{ $t('auth.registrationRestrictedHint') }}</p>
        <router-link to="/auth/login" class="link-action">
          {{ $t('common.login') }}
        </router-link>
      </div>
      <form v-else @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">{{ $t('common.username') }}</label>
          <input v-model="form.username" type="text" id="username" required />
          <small>{{ $t('auth.usernameHint') }}</small>
        </div>
        <div class="form-group">
          <label for="email">{{ $t('common.email') }}</label>
          <input v-model="form.email" type="email" id="email" required />
        </div>
        <div v-if="!isClosedRegistration" class="checkbox-group">
          <label for="tos" class="checkbox-label">
            <input v-model="form.tosAgreed" type="checkbox" id="tos" required />
            <span>{{ $t('auth.tosAgree') }}</span>
          </label>
          <a href="/terms-of-service" target="_blank">{{ $t('auth.tosLink') }}</a>
        </div>
        <div v-else class="info-box compact" role="note">
          <p>{{ $t('auth.closedRegistrationAdminInfo') }}</p>
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
import { defineComponent, reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

export default defineComponent({
  name: 'Register',
  setup() {
    const authStore = useAuthStore()
    const appStore = useAppStore()

    return {
      authStore,
      appStore,
      form: reactive({
        username: '',
        email: '',
        tosAgreed: false,
      }),
      isLoading: ref(false),
      errorMessage: ref(''),
    }
  },
  computed: {
    isClosedRegistration() {
      return this.appStore.config?.features?.closedRegistration ?? false
    },
    canCreateClosedRegistration() {
      return this.authStore.hasRole('support') || this.authStore.hasRole('admin')
    },
  },
  methods: {
    async handleRegister() {
      if (this.isClosedRegistration && !this.canCreateClosedRegistration) {
        return
      }

      const normalizedUsername = this.form.username.trim()
      if (normalizedUsername.length < 5) {
        this.errorMessage = this.$t('validation.username')
        return
      }

      const normalizedEmail = this.form.email.trim()

      this.isLoading = true
      this.errorMessage = ''

      try {
        const response = await this.authStore.register(
          normalizedUsername,
          normalizedEmail,
          this.isClosedRegistration ? false : this.form.tosAgreed,
          this.$i18n.locale
        )

        this.form.username = normalizedUsername
        this.form.email = normalizedEmail

        this.$router.push({
          name: 'RegisterPending',
          query: {
            username: normalizedUsername,
            email: normalizedEmail,
            expiresInHours: String(response?.expires_in_hours || 24),
            admin: String(Boolean(response?.admin)),
          },
        })
      } catch (error) {
        const detail = error?.detail
        this.errorMessage = typeof detail === 'string'
          ? detail
          : this.$t('auth.registrationFailed')
      } finally {
        this.isLoading = false
      }
    },
  },
})
</script>

<style scoped>
.error-box {
  background: #fef2f2;
  border: 1px solid #fca5a5;
  color: #991b1b;
  border-radius: 0.375rem;
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
}

.info-box {
  background: #eff6ff;
  border: 1px solid #93c5fd;
  color: #1e3a8a;
  border-radius: 0.375rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.info-box.compact {
  padding: 0.75rem 1rem;
}

.info-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.link-action {
  display: inline-block;
  margin-top: 0.75rem;
}
</style>
