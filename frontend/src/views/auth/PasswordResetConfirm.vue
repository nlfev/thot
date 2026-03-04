<template>
  <div class="auth-container">
    <div class="card form-card">
      <div
        v-if="loading"
        class="loading"
      >
        <p>{{ $t('common.loading') }}</p>
      </div>

      <div
        v-else-if="tokenError"
        class="error-message"
      >
        <h2>{{ $t('auth.passwordReset') }}</h2>
        <p>{{ tokenError }}</p>
        <router-link
          to="/auth/password-reset"
          class="btn btn-primary"
        >
          {{ $t('auth.passwordReset') }}
        </router-link>
      </div>

      <form
        v-else
        @submit.prevent="handleSubmit"
      >
        <h2>{{ $t('auth.passwordReset') }}</h2>

        <div class="form-group">
          <label for="newPassword">{{ $t('user.newPassword') }}</label>
          <input
            id="newPassword"
            v-model="form.newPassword"
            type="password"
            required
            minlength="10"
            maxlength="60"
          >
        </div>

        <div class="form-group">
          <label for="confirmPassword">{{ $t('user.confirmNewPassword') }}</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            minlength="10"
            maxlength="60"
          >
        </div>

        <p
          v-if="form.confirmPassword && !passwordsMatch"
          class="error-message"
        >
          {{ $t('auth.passwordsMustMatch') }}
        </p>

        <button
          type="submit"
          class="btn btn-primary"
          :disabled="isLoading || !passwordsMatch"
        >
          {{ isLoading ? $t('common.loading') : $t('common.submit') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import authService from '@/services/auth'

export default defineComponent({
  name: 'PasswordResetConfirm',
  data() {
    return {
      token: '',
      loading: true,
      isLoading: false,
      tokenError: '',
      form: {
        newPassword: '',
        confirmPassword: '',
      },
    }
  },
  computed: {
    passwordsMatch() {
      return this.form.newPassword === this.form.confirmPassword
    },
  },
  async mounted() {
    this.token = this.$route.params.token
    await this.validateToken()
  },
  methods: {
    async validateToken() {
      try {
        this.loading = true
        await authService.validatePasswordResetToken(this.token)
      } catch (error) {
        this.tokenError = error?.detail || this.$t('auth.invalidOrExpiredLink')
      } finally {
        this.loading = false
      }
    },
    async handleSubmit() {
      if (!this.passwordsMatch) {
        return
      }

      try {
        this.isLoading = true
        await authService.confirmPasswordReset(this.token, this.form.newPassword)
        alert(this.$t('auth.passwordChanged'))
        this.$router.push('/auth/login')
      } catch (error) {
        const message = error?.detail || this.$t('messages.serverError')
        alert(message)
      } finally {
        this.isLoading = false
      }
    },
  },
})
</script>

<style scoped>
</style>
