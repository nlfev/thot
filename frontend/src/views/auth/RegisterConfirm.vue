<template>
  <div class="auth-container">
    <div class="card form-card">
      <div v-if="loading" class="loading">
        <p>{{ $t('common.loading') }}...</p>
      </div>
      
      <div v-else-if="error" class="error-message">
        <h2>{{ $t('auth.registrationError') }}</h2>
        <p>{{ error }}</p>
        <p v-if="expiredError" class="info">
          {{ $t('auth.expiredLinkInfo') }}
        </p>
        <router-link to="/auth/register" class="btn">
          {{ $t('auth.restartRegistration') }}
        </router-link>
      </div>

      <form v-else @submit.prevent="handleConfirm">
        <h2>{{ $t('auth.completeRegistration') }}</h2>
        
        <div class="form-section">
          <h4>{{ $t('auth.accountInfo') }}</h4>
          <div class="form-group">
            <label>{{ $t('common.username') }}</label>
            <input type="text" :value="registrationData.username" readonly />
          </div>
          <div class="form-group">
            <label>{{ $t('common.email') }}</label>
            <input type="email" :value="registrationData.email" readonly />
          </div>
        </div>

        <div class="form-section">
          <h4>{{ $t('auth.personalInfo') }}</h4>
          <div class="form-group">
            <label for="firstName">{{ $t('common.firstName') }}</label>
            <input 
              v-model="form.firstName" 
              type="text" 
              id="firstName" 
              required 
            />
          </div>
          <div class="form-group">
            <label for="lastName">{{ $t('common.lastName') }}</label>
            <input 
              v-model="form.lastName" 
              type="text" 
              id="lastName" 
              required 
            />
          </div>
        </div>

        <div class="form-section">
          <h4>{{ $t('auth.passwordInfo') }}</h4>
          <div class="password-requirements">
            <p>{{ $t('auth.passwordRequirements') }}</p>
            <ul>
              <li :class="{ valid: hasMinLength }">
                {{ $t('auth.minLength') }}: 10-60 {{ $t('auth.characters') }}
              </li>
              <li :class="{ valid: hasUpperLower }">
                {{ $t('auth.upperLowerCase') }}
              </li>
              <li :class="{ valid: hasDigitOrSpecial }">
                {{ $t('auth.digitOrSpecial') }}
              </li>
            </ul>
          </div>
          <div class="form-group">
            <label for="password">{{ $t('common.password') }}</label>
            <div class="password-input-wrapper">
              <input 
                v-model="form.password" 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                required 
                @input="updatePasswordValidation"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
              >
                <span v-if="showPassword">👁️</span>
                <span v-else>👁️‍🗨️</span>
              </button>
            </div>
          </div>
          <div class="form-group">
            <label for="passwordConfirm">{{ $t('auth.confirmPassword') }}</label>
            <div class="password-input-wrapper">
              <input 
                v-model="form.passwordConfirm" 
                :type="showPasswordConfirm ? 'text' : 'password'" 
                id="passwordConfirm" 
                required 
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPasswordConfirm = !showPasswordConfirm"
                :aria-label="showPasswordConfirm ? 'Hide password' : 'Show password'"
              >
                <span v-if="showPasswordConfirm">👁️</span>
                <span v-else>👁️‍🗨️</span>
              </button>
            </div>
            <small v-if="form.password && form.passwordConfirm && form.password !== form.passwordConfirm" class="error">
              {{ $t('auth.passwordsMustMatch') }}
            </small>
          </div>
        </div>

        <div class="form-section">
          <div class="form-group">
            <label for="corporateNumber">{{ $t('common.corporateNumber') }} ({{ $t('auth.optional') }})</label>
            <input 
              v-model="form.corporateNumber" 
              type="text" 
              id="corporateNumber" 
            />
          </div>
        </div>

        <div class="form-section">
          <div class="checkbox-group">
            <label for="enableOtp" class="checkbox-label">
              <input 
                v-model="form.enableOtp" 
                type="checkbox" 
                id="enableOtp" 
              />
              <span>{{ $t('auth.enableOtp') }}</span>
            </label>
            <small>{{ $t('auth.otpInfo') }}</small>
          </div>
        </div>

        <button 
          type="submit" 
          :disabled="isLoading || !isFormValid"
          class="btn-primary"
        >
          {{ isLoading ? $t('common.loading') : $t('auth.completeRegistration') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import authApi from '@/services/auth'

export default defineComponent({
  name: 'RegisterConfirm',
  data() {
    return {
      token: '',
      registrationData: {
        username: '',
        email: '',
      },
      form: {
        firstName: '',
        lastName: '',
        password: '',
        passwordConfirm: '',
        corporateNumber: '',
        enableOtp: false,
      },
      loading: true,
      isLoading: false,
      error: null,
      expiredError: false,
      hasMinLength: false,
      hasUpperLower: false,
      hasDigitOrSpecial: false,
      showPassword: false,
      showPasswordConfirm: false,
    }
  },
  computed: {
    passwordsMatch() {
      return this.form.password === this.form.passwordConfirm
    },
    isFormValid() {
      return (
        this.form.firstName.trim() &&
        this.form.lastName.trim() &&
        this.hasMinLength &&
        this.hasUpperLower &&
        this.hasDigitOrSpecial &&
        this.passwordsMatch &&
        !this.error
      )
    },
  },
  mounted() {
    this.token = this.$route.params.token
    this.loadRegistrationData()
  },
  methods: {
    async loadRegistrationData() {
      try {
        this.loading = true
        const response = await authApi.getRegistrationConfirm(this.token)
        this.registrationData = {
          username: response.data.username,
          email: response.data.email,
        }
      } catch (err) {
        this.error = err.response?.data?.detail || this.$t('auth.invalidOrExpiredLink')
        if (err.response?.status === 400) {
          this.expiredError = true
        }
      } finally {
        this.loading = false
      }
    },
    updatePasswordValidation() {
      const pwd = this.form.password
      this.hasMinLength = pwd.length >= 10 && pwd.length <= 60
      this.hasUpperLower = /[A-Z]/.test(pwd) && /[a-z]/.test(pwd)
      this.hasDigitOrSpecial = /[\d!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(pwd)
    },
    async handleConfirm() {
      if (!this.isFormValid) {
        return
      }

      this.isLoading = true
      try {
        const response = await authApi.confirmRegistration(this.token, {
          first_name: this.form.firstName,
          last_name: this.form.lastName,
          password: this.form.password,
          password_confirm: this.form.passwordConfirm,
          corporate_number: this.form.corporateNumber,
          enable_otp: this.form.enableOtp,
          current_language: this.$i18n.locale,
        })

        if (response.data.otp_setup) {
          // If OTP is enabled, redirect to OTP setup page
          this.$router.push({
            name: 'OTPSetup',
            params: {
              qrCode: response.data.otp_setup.qr_code,
              manualEntry: response.data.otp_setup.manual_entry,
            }
          })
        } else {
          // Registration successful, redirect to login
          this.$router.push('/auth/login')
        }
      } catch (err) {
        this.error = err.response?.data?.detail || this.$t('auth.registrationFailed')
      } finally {
        this.isLoading = false
      }
    },
  },
})
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.form-card {
  width: 100%;
  max-width: 600px;
}

h2 {
  margin-bottom: 30px;
  text-align: center;
}

.form-section {
  margin-bottom: 25px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.form-section h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  color: #666;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  font-size: 14px;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input-wrapper input {
  flex: 1;
  padding-right: 3rem;
}

.password-toggle {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.password-toggle:hover {
  opacity: 1;
}

.password-toggle:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
  border-radius: 4px;
}

input[readonly] {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.password-requirements {
  padding: 12px;
  background-color: #fff3e0;
  border-left: 4px solid #ff9800;
  border-radius: 4px;
  margin-bottom: 15px;
}

.password-requirements p {
  margin: 0 0 8px 0;
  font-weight: 500;
  font-size: 13px;
  color: #e65100;
}

.password-requirements ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.password-requirements li {
  padding: 4px 0;
  font-size: 13px;
  color: #666;
}

.password-requirements li.valid {
  color: #4caf50;
  font-weight: 500;
}

.password-requirements li::before {
  content: "○ ";
  margin-right: 5px;
}

.password-requirements li.valid::before {
  content: "✓ ";
  color: #4caf50;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-weight: 500;
  cursor: pointer;
}

.checkbox-label input {
  margin-right: 10px;
  cursor: pointer;
}

.checkbox-label input + span {
  flex: 1;
}

small {
  display: block;
  margin-top: 5px;
  font-size: 12px;
  color: #999;
}

small.error {
  color: #f44336;
  font-weight: 500;
}

button {
  width: 100%;
  padding: 12px;
  margin-top: 20px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #2196f3;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #1976d2;
}

.btn-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loading,
.error-message {
  text-align: center;
  padding: 40px 20px;
}

.error-message {
  color: #f44336;
}

.error-message p {
  margin: 10px 0;
}

.error-message p.info {
  color: #1976d2;
  margin-top: 20px;
  margin-bottom: 20px;
}

.error-message .btn {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #2196f3;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.error-message .btn:hover {
  background-color: #1976d2;
}
</style>
