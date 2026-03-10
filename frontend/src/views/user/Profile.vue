<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>{{ $t('user.profile') }}</h2>

      <!-- Success/Error Messages -->
      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="alert alert-error">
        {{ errorMessage }}
      </div>

      <!-- Profile Information Section -->
      <div class="profile-section">
        <h3>{{ $t('auth.accountInfo') }}</h3>
        
        <div class="form-group">
          <label>{{ $t('common.username') }}</label>
          <input type="text" :value="profileData.username" readonly />
        </div>

        <div class="form-group">
          <label>{{ $t('common.email') }}</label>
          <input type="email" :value="profileData.email" readonly />
        </div>

        <div class="form-group">
          <label>{{ $t('common.corporateNumber') }} ({{ $t('common.optional') }})</label>
          <input type="text" :value="profileData.corporate_number" readonly />
        </div>

        <div class="form-group">
          <label v-if="profileData.corporate_approved" class="badge badge-success">
            ✓ {{ $t('admin.approveCorporate') }}
          </label>
          <label v-else class="badge badge-pending">
            {{ $t('user.pendingApproval') }}
          </label>
        </div>
      </div>

      <!-- Account Settings Section -->
      <div class="profile-section">
        <h3>{{ $t('auth.personalInfo') }}</h3>
        
        <div class="form-row">
          <div class="form-group">
            <label for="firstName">{{ $t('common.firstName') }}</label>
            <input 
              v-model="editData.first_name" 
              type="text" 
              id="firstName"
              @focus="clearMessages"
            />
          </div>
          <div class="form-group">
            <label for="lastName">{{ $t('common.lastName') }}</label>
            <input 
              v-model="editData.last_name" 
              type="text" 
              id="lastName"
              @focus="clearMessages"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="language">{{ $t('common.language') }}</label>
          <select v-model="editData.current_language" id="language">
            <option value="en">English</option>
            <option value="de">Deutsch</option>
          </select>
        </div>

        <button 
          @click="saveProfileChanges"
          :disabled="isLoading || !hasProfileChanges"
          class="btn-primary"
        >
          {{ isLoading ? $t('common.loading') : $t('common.save') }}
        </button>
      </div>

      <!-- Password Change Section -->
      <div class="profile-section password-section">
        <h3>{{ $t('user.changePassword') }}</h3>

        <div class="form-group">
          <label for="currentPassword">{{ $t('user.currentPassword') }}</label>
          <div class="password-input-wrapper">
            <input 
              v-model="passwordForm.current_password" 
              :type="showCurrentPassword ? 'text' : 'password'" 
              id="currentPassword"
              @focus="clearMessages"
            />
            <button
              type="button"
              class="password-toggle"
              @click="showCurrentPassword = !showCurrentPassword"
              :aria-label="showCurrentPassword ? 'Hide password' : 'Show password'"
            >
              <span v-if="showCurrentPassword">👁️</span>
              <span v-else>👁️‍🗨️</span>
            </button>
          </div>
        </div>

        <div class="password-requirements">
          <p>{{ $t('auth.passwordRequirements') }}</p>
          <ul>
            <li :class="{ valid: passwordValidation.hasMinLength }">
              {{ $t('auth.minLength') }}: 10-60 {{ $t('auth.characters') }}
            </li>
            <li :class="{ valid: passwordValidation.hasUpperLower }">
              {{ $t('auth.upperLowerCase') }}
            </li>
            <li :class="{ valid: passwordValidation.hasDigitOrSpecial }">
              {{ $t('auth.digitOrSpecial') }}
            </li>
            <li :class="{ valid: passwordValidation.passwordsMatch }">
              {{ $t('auth.passwordsMustMatch') }}
            </li>
          </ul>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="newPassword">{{ $t('user.newPassword') }}</label>
            <div class="password-input-wrapper">
              <input 
                v-model="passwordForm.new_password" 
                :type="showNewPassword ? 'text' : 'password'" 
                id="newPassword"
                @input="updatePasswordValidation"
                @focus="clearMessages"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showNewPassword = !showNewPassword"
                :aria-label="showNewPassword ? 'Hide password' : 'Show password'"
              >
                <span v-if="showNewPassword">👁️</span>
                <span v-else>👁️‍🗨️</span>
              </button>
            </div>
          </div>
          <div class="form-group">
            <label for="newPasswordConfirm">{{ $t('user.confirmNewPassword') }}</label>
            <div class="password-input-wrapper">
              <input 
                v-model="passwordForm.new_password_confirm" 
                :type="showConfirmPassword ? 'text' : 'password'" 
                id="newPasswordConfirm"
                @input="updatePasswordValidation"
                @focus="clearMessages"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showConfirmPassword = !showConfirmPassword"
                :aria-label="showConfirmPassword ? 'Hide password' : 'Show password'"
              >
                <span v-if="showConfirmPassword">👁️</span>
                <span v-else>👁️‍🗨️</span>
              </button>
            </div>
          </div>
        </div>

        <button 
          @click="changePassword"
          :disabled="isLoading || !isPasswordFormValid"
          class="btn-primary"
        >
          {{ isLoading ? $t('common.loading') : $t('user.changePassword') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'
import userApi from '@/services/user'

export default defineComponent({
  name: 'Profile',
  data() {
    return {
      authStore: useAuthStore(),
      profileData: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        current_language: 'en',
        corporate_number: '',
        corporate_approved: false,
      },
      editData: {
        first_name: '',
        last_name: '',
        current_language: 'en',
      },
      passwordForm: {
        current_password: '',
        new_password: '',
        new_password_confirm: '',
      },
      passwordValidation: {
        hasMinLength: false,
        hasUpperLower: false,
        hasDigitOrSpecial: false,
        passwordsMatch: false,
      },
      successMessage: '',
      errorMessage: '',
      isLoading: false,
      showCurrentPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
    }
  },
  computed: {
    hasProfileChanges() {
      return (
        this.editData.first_name !== this.profileData.first_name ||
        this.editData.last_name !== this.profileData.last_name ||
        this.editData.current_language !== this.profileData.current_language
      )
    },
    isPasswordFormValid() {
      return (
        this.passwordForm.current_password &&
        this.passwordValidation.hasMinLength &&
        this.passwordValidation.hasUpperLower &&
        this.passwordValidation.hasDigitOrSpecial &&
        this.passwordValidation.passwordsMatch
      )
    },
  },
  methods: {
    async loadProfile() {
      try {
        this.isLoading = true
        const response = await userApi.getProfile()
        
        this.profileData = {
          username: response.username || '',
          email: response.email || '',
          first_name: response.first_name || '',
          last_name: response.last_name || '',
          current_language: response.current_language || 'en',
          corporate_number: response.corporate_number || '',
          corporate_approved: response.corporate_approved || false,
        }

        // Initialize edit data with profile data
        this.editData = {
          first_name: this.profileData.first_name,
          last_name: this.profileData.last_name,
          current_language: this.profileData.current_language,
        }
        
        this.isLoading = false
      } catch (error) {
        this.errorMessage = this.$t('messages.loadingError')
        console.error('Error loading profile:', error)
        this.isLoading = false
      }
    },

    async saveProfileChanges() {
      try {
        this.clearMessages()
        this.isLoading = true

        const response = await userApi.updateProfile({
          first_name: this.editData.first_name,
          last_name: this.editData.last_name,
          current_language: this.editData.current_language,
        })

        // Update profile data and auth store
        this.profileData = {
          ...this.profileData,
          first_name: response.first_name,
          last_name: response.last_name,
          current_language: response.current_language,
        }

        this.successMessage = this.$t('messages.saveSuccess')
        
        // Update auth store language if changed
        if (this.authStore.user) {
          this.authStore.user.current_language = response.current_language
        }

        this.isLoading = false
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || this.$t('messages.saveSuccess')
        console.error('Error updating profile:', error)
        this.isLoading = false
      }
    },

    async changePassword() {
      try {
        this.clearMessages()
        this.isLoading = true

        const response = await userApi.changePassword({
          current_password: this.passwordForm.current_password,
          new_password: this.passwordForm.new_password,
          new_password_confirm: this.passwordForm.new_password_confirm,
        })

        // Clear password form
        this.passwordForm = {
          current_password: '',
          new_password: '',
          new_password_confirm: '',
        }

        this.successMessage = this.$t('user.passwordChanged')
        this.isLoading = false
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || this.$t('messages.saveSuccess')
        console.error('Error changing password:', error)
        this.isLoading = false
      }
    },

    updatePasswordValidation() {
      const pwd = this.passwordForm.new_password
      
      this.passwordValidation.hasMinLength = pwd.length >= 10 && pwd.length <= 60
      this.passwordValidation.hasUpperLower = /[a-z]/.test(pwd) && /[A-Z]/.test(pwd)
      this.passwordValidation.hasDigitOrSpecial = /[0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(pwd)
      this.passwordValidation.passwordsMatch = pwd === this.passwordForm.new_password_confirm
    },

    clearMessages() {
      this.successMessage = ''
      this.errorMessage = ''
    },
  },

  mounted() {
    // Check if user is authenticated
    if (!this.authStore.isAuthenticated) {
      this.$router.push('/auth/login')
      return
    }

    this.loadProfile()
  },
})
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}

.profile-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

h2 {
  margin-bottom: 1.5rem;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 1rem;
}

.profile-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #f0f0f0;
}

.profile-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.password-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 2px solid #f0f0f0;
}

h3 {
  margin-bottom: 1.5rem;
  color: #555;
  font-size: 1.1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

input,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  box-sizing: border-box;
}

input:readonly {
  background-color: #f9f9f9;
  color: #666;
  cursor: default;
}

input:focus,
select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.password-requirements {
  background-color: #f9f9f9;
  border-left: 4px solid #ddd;
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 4px;
}

.password-requirements p {
  margin: 0 0 0.75rem 0;
  font-weight: 500;
  color: #333;
}

.password-requirements ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.password-requirements li {
  padding: 0.25rem 0;
  color: #999;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.password-requirements li.valid {
  color: #4CAF50;
  font-weight: 500;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #45a049;
}

.btn-primary:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.alert {
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 4px;
  border-left: 4px solid;
}

.alert-success {
  background-color: #f1f8f5;
  border-color: #4CAF50;
  color: #2d5a3d;
}

.alert-error {
  background-color: #fdf1f1;
  border-color: #f44336;
  color: #902b2b;
}

.badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.badge-success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.badge-pending {
  background-color: #fff3e0;
  color: #e65100;
}

@media (max-width: 640px) {
  .profile-card {
    padding: 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  h2 {
    font-size: 1.5rem;
  }

  h3 {
    font-size: 1rem;
  }
}</style>
