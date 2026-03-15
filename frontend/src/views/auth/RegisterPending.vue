<template>
  <div class="auth-container">
    <div class="card info-card">
      <div class="success-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
      </div>
      
      <h2>{{ $t('auth.registrationInitiated') }}</h2>
      
      <div class="info-content">
        <p class="lead">{{ $t('auth.checkYourEmail') }}</p>
        
        <div class="info-box">
          <p><strong>{{ $t('common.email') }}:</strong> {{ email }}</p>
          <p><strong>{{ $t('common.username') }}:</strong> {{ username }}</p>
        </div>
        
        <p>{{ $t('auth.registrationEmailSent', { hours: expiresInHours }) }}</p>

        <div v-if="admin" class="alert alert-info">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
          <span>{{ $t('auth.closedRegistrationAdminInfo') }}</span>
        </div>
        
        <div class="instructions">
          <h3>{{ $t('auth.whatNext') }}</h3>
          <ol>
            <li>{{ $t('auth.step1CheckEmail') }}</li>
            <li>{{ $t('auth.step2ClickLink') }}</li>
            <li>{{ $t('auth.step3CompleteRegistration') }}</li>
          </ol>
        </div>
        
        <div class="alert alert-info">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
          <span>{{ $t('auth.checkSpamFolder') }}</span>
        </div>
      </div>
      
      <div class="button-group">
        <router-link to="/auth/login" class="btn btn-primary">
          {{ $t('common.backToLogin') }}
        </router-link>
        <router-link to="/" class="btn btn-secondary">
          {{ $t('common.backToHome') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'RegisterPending',
  props: {
    username: {
      type: String,
      default: '',
    },
    email: {
      type: String,
      default: '',
    },
    expiresInHours: {
      type: Number,
      default: 24,
    },
    admin: {
      type: Boolean,
      default: false,
    },
  },
  created() {
    // Redirect to register if no email provided
    if (!this.email) {
      this.$router.replace('/auth/register')
    }
  },
})
</script>

<style scoped>
.info-card {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.success-icon {
  color: #22c55e;
  margin-bottom: 1.5rem;
}

.success-icon svg {
  width: 64px;
  height: 64px;
}

h2 {
  color: #1e40af;
  margin-bottom: 1.5rem;
  font-size: 1.75rem;
}

.info-content {
  text-align: left;
  margin: 2rem 0;
}

.lead {
  font-size: 1.125rem;
  font-weight: 500;
  text-align: center;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.info-box {
  background-color: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1.5rem 0;
}

.info-box p {
  margin: 0.5rem 0;
  color: #374151;
}

.info-box strong {
  color: #1f2937;
}

.instructions {
  margin: 2rem 0;
}

.instructions h3 {
  font-size: 1.125rem;
  color: #1f2937;
  margin-bottom: 1rem;
}

.instructions ol {
  padding-left: 1.5rem;
  color: #4b5563;
}

.instructions li {
  margin: 0.75rem 0;
  line-height: 1.6;
}

.alert svg {
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .button-group {
    flex-direction: column;
  }
  
  .button-group > * {
    width: 100%;
  }
}
</style>
