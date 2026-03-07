<template>
  <div class="view-wrapper">
    <div class="view-header">
      <h1>{{ $t('common.about') }}</h1>
    </div>
    <div class="view-content">
      <div class="card about-section">
        <h2>{{ $t('about.title') }}</h2>
        <p class="subtitle">
          {{ $t('about.subtitle') }}
        </p>
        <p>{{ $t('about.description') }}</p>
      </div>

      <div class="card about-section">
        <h2>{{ $t('about.versionTitle') }}</h2>
        <p><strong>{{ $t('about.version') }}:</strong> {{ version }}</p>
        <p><strong>{{ $t('about.buildDate') }}:</strong> {{ buildDate }}</p>
      </div>

      <div class="card about-section license-section">
        <h2>{{ $t('about.licenseTitle') }}</h2>
        <p>{{ $t('about.licenseText') }}</p>
        <div class="license-badge">
          <strong>AGPL-3.0-or-later</strong>
        </div>
        <p class="license-description">
          {{ $t('about.agplDescription') }}
        </p>
        <p>
          <a
            href="/LICENSE"
            target="_blank"
            rel="noopener"
            class="license-link"
          >
            {{ $t('about.viewFullLicense') }}
          </a>
        </p>
        <p class="license-info">
          {{ $t('about.agplInfo') }}
        </p>
      </div>

      <div class="card about-section">
        <h2>{{ $t('about.sourceCodeTitle') }}</h2>
        <p>{{ $t('about.sourceCodeText') }}</p>
        <div class="repo-link">
          <a
            v-if="sourceRepoUrl"
            :href="sourceRepoUrl"
            target="_blank"
            rel="noopener"
            class="button-link"
          >
            {{ $t('about.viewSource') }}
          </a>
          <button
            v-else
            type="button"
            class="button-link button-link-disabled"
            @click="openRepoPlaceholder"
          >
            {{ $t('about.viewSource') }}
          </button>
          <p class="hint">
            {{ sourceRepoUrl ? $t('about.repositoryAvailableHint') : $t('about.repositoryPlaceholder') }}
          </p>
        </div>
      </div>

      <div class="card about-section">
        <h2>{{ $t('about.thirdPartyTitle') }}</h2>
        <p>{{ $t('about.thirdPartyText') }}</p>
        <p>
          <a
            href="/THIRD_PARTY_LICENSES.md"
            target="_blank"
            rel="noopener"
            class="license-link"
          >
            {{ $t('about.viewThirdPartyLicenses') }}
          </a>
        </p>
      </div>

      <div class="card about-section">
        <h2>{{ $t('about.copyrightTitle') }}</h2>
        <p>{{ copyrightText }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  name: 'About',
  setup() {
    const { t } = useI18n()

    const version = '1.0.0'
    const buildDate = new Date().toLocaleDateString()
    const currentYear = new Date().getFullYear()

    const sourceRepoUrl = (import.meta.env.VITE_SOURCE_REPO_URL || '').trim()

    const copyrightText = computed(() => 
      t('about.copyright', { year: currentYear })
    )

    const openRepoPlaceholder = () => {
      alert(t('about.repositoryNotYetAvailable'))
    }

    return {
      version,
      buildDate,
      copyrightText,
      sourceRepoUrl,
      openRepoPlaceholder
    }
  }
})
</script>

<style scoped>
.about-section {
  margin-bottom: 2rem;
}

.about-section:last-child {
  margin-bottom: 0;
}

.subtitle {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-top: 0.5rem;
}

.license-section {
  background-color: var(--color-background-soft);
}

.license-badge {
  display: inline-block;
  background-color: var(--color-primary);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-weight: bold;
  margin: 1rem 0;
}

.license-description {
  font-style: italic;
  color: var(--color-text-secondary);
  margin: 1rem 0;
}

.license-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
}

.license-link:hover {
  text-decoration: underline;
}

.license-info {
  margin-top: 1rem;
  padding: 1rem;
  background-color: var(--color-background);
  border-left: 4px solid var(--color-primary);
  border-radius: 0.25rem;
}

.repo-link {
  margin-top: 1rem;
}

.button-link {
  display: inline-block;
  border: 0;
  background-color: var(--color-primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.25rem;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.2s;
}

.button-link:hover {
  background-color: var(--color-primary-dark);
}

.button-link-disabled {
  cursor: pointer;
}

.hint {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  font-style: italic;
}

h2 {
  color: var(--color-heading);
  margin-top: 0;
}

p {
  line-height: 1.6;
  margin: 0.5rem 0;
}
</style>
