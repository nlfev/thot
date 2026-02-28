<template>
  <div class="view-wrapper">
    <div class="view-header">
      <h1>{{ title }}</h1>
    </div>
    <div class="view-content">
      <p>This page is under construction.</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'NotFound',
  setup() {
    return {
      title: 'Page Not Found',
    }
  },
})
</script>

<style scoped>
.view-wrapper {
  padding: 2rem;
}

.view-header {
  margin-bottom: 2rem;
}

.view-content {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}
</style>
