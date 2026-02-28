<template>
  <div class="view-wrapper">
    <div class="view-header">
      <h1>{{ $t('common.about') }}</h1>
    </div>
    <div class="view-content card">
      <p>{{ $t('common.appName') }} - Professional Database Management System</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'About',
})
</script>

<style scoped>
</style>
