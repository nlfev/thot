<template>
  <div class="view-wrapper">
    <div class="view-header">
      <h1>{{ $t('common.apiDocs') }}</h1>
    </div>
    <div class="view-content card">
      <p class="mb-3">{{ $t('messages.apiDocsInfo') }}</p>
      <iframe
        :src="`${backendUrl}/docs`"
        class="swagger-iframe"
        title="API Documentation"
      />
    </div>
  </div>
</template>

<script setup>
const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
</script>

<style scoped>
.swagger-iframe {
  width: 100%;
  height: 600px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
}

@media (max-width: 768px) {
  .swagger-iframe {
    height: 400px;
  }
}
</style>
