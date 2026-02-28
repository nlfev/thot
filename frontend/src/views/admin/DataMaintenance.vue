<template>
  <div class="view-wrapper">
    <div class="view-header">
      <h1>{{ $t('admin.dataMaintenance') }}</h1>
    </div>
    <div class="view-content card">
      <p class="text-center text-muted">{{ $t('messages.comingSoon') }}</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'DataMaintenance',
})
</script>

<style scoped>
</style>
