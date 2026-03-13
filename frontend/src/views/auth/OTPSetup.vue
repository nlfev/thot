<template>
  <div class="auth-container">
    <div class="card form-card">
      <h2>{{ $t('auth.otpSetupTitle') }}</h2>
      <p class="info-text">
        {{ $t('auth.otpSetupDescription') }}
      </p>

      <div
        v-if="qrCode"
        class="qr-container"
      >
        <img
          :src="qrCode"
          :alt="$t('auth.otpQrAlt')"
          class="qr-image"
        >
      </div>

      <div class="manual-entry">
        <label for="manualEntry">{{ $t('auth.otpManualEntryLabel') }}</label>
        <input
          id="manualEntry"
          type="text"
          :value="manualEntry || ''"
          readonly
        >
      </div>

      <p class="hint-text">
        {{ $t('auth.otpSetupHint') }}
      </p>

      <button
        type="button"
        class="btn-primary"
        @click="goToLogin"
      >
        {{ $t('common.backToLogin') }}
      </button>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'OTPSetup',
  computed: {
    qrCode() {
      const raw = history.state?.qrCode
      if (!raw) return ''
      // Backend returns a plain base64 string – prepend the data URL prefix
      if (raw.startsWith('data:')) return raw
      return `data:image/png;base64,${raw}`
    },
    manualEntry() {
      return history.state?.manualEntry || ''
    },
  },
  methods: {
    goToLogin() {
      this.$router.push('/auth/login')
    },
  },
})
</script>

<style scoped>
.form-card {
  width: 100%;
  max-width: 480px;
}

.info-text {
  margin-bottom: 16px;
}

.qr-container {
  display: flex;
  justify-content: center;
  margin: 12px 0 18px;
}

.qr-image {
  width: 220px;
  height: 220px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  object-fit: contain;
}

.manual-entry {
  margin-bottom: 12px;
}

.manual-entry label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}

.manual-entry input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #f5f5f5;
  font-family: monospace;
}

.hint-text {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 16px;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 6px;
  background: #1976d2;
  color: #fff;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
}
</style>
