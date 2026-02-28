<template>
  <div class="view-wrapper">
    <div class="view-header">
      <h1>{{ $t('common.dataProtection') }}</h1>
    </div>
    <div class="view-content card">
      <p>Data protection information will be placed here.</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'DataProtection',
})
</script>
