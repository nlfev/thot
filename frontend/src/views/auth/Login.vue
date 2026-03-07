<template>
  <div class="auth-container">
    <div class="card form-card">
      <h2>{{ $t('auth.loginTitle') }}</h2>
      <p v-if="sessionNotice" class="info">{{ sessionNotice }}</p>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="otpRequired" class="info">{{ $t('auth.otpRequired') }}</p>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">{{ $t('common.username') }}</label>
          <input v-model="form.username" type="text" id="username" required />
        </div>
        <div class="form-group">
          <label for="password">{{ $t('common.password') }}</label>
          <input v-model="form.password" type="password" id="password" required />
        </div>
        <div class="form-group">
          <label for="otp">
            {{ $t('auth.otpCode') }}
            <span v-if="!otpRequired">({{ $t('common.optional') }})</span>
            <span v-else class="required">*</span>
          </label>
          <input 
            v-model="form.otpCode" 
            type="text" 
            id="otp" 
            :required="otpRequired"
            placeholder="123456"
            maxlength="6"
          />
          <small v-if="otpRequired">{{ $t('auth.enterOtpFromApp') }}</small>
        </div>
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? $t('common.loading') : $t('common.login') }}
        </button>
      </form>
      <p class="text-right mt-2">
        <router-link to="/auth/password-reset">{{ $t('auth.forgotPassword') }}</router-link>
      </p>
      <p class="text-center mt-3">
        {{ $t('auth.noAccount') }}
        <router-link to="/auth/register">{{ $t('common.register') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default defineComponent({
  name: 'Login',
  setup() {
    const authStore = useAuthStore()

    return {
      authStore,
      form: {
        username: '',
        password: '',
        otpCode: '',
      },
      error: '',
      sessionNotice: '',
      isLoading: false,
      otpRequired: false,
    }
  },
  mounted() {
    if (this.$route.query.reason === 'session-timeout') {
      this.sessionNotice = this.$t('auth.sessionTimedOut')
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true
      this.error = ''
      this.sessionNotice = ''
      this.otpRequired = false

      const success = await this.authStore.login(
        this.form.username,
        this.form.password,
        this.form.otpCode || null
      )

      if (success) {
        this.$router.push('/')
      } else {
        this.error = this.authStore.error
        
        // Check if OTP is required
        if (this.error === 'Two-factor authentication required') {
          this.otpRequired = true
          this.error = this.$t('auth.pleaseEnterOtp')
        }
      }

      this.isLoading = false
    },
  },
})
</script>

<style scoped>
/* Additional component-specific styles if needed */
</style>
