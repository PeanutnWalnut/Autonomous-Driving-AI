<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  title: string,
  subtitle: string,
}>()
</script>

<template>
  <h1>{{ title }}</h1>
  <h2>{{ subtitle }}</h2>
</template>

<style scoped>
a {
  color: #42b983;
}

label {
  margin: 0 0.5em;
  font-weight: bold;
}

code {
  background-color: #eee;
  padding: 2px 4px;
  border-radius: 4px;
  color: #304455;
}
</style>