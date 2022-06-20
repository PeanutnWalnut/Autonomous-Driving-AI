<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import Index from './components/index.vue'
</script>

<template>
  <!-- <img alt="Vue logo" src="./assets/vue_logo.png" /> -->
  <!-- <HelloWorld msg="Hello Vue 3 + TypeScript + Vite" /> -->
  
  <img class="logo" alt="PeanutnWalnut logo" src="./assets/pnw_logo.jpg" width="250"/>
  <Index title="Hello Autonomous-Driving-AI"/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

img {
}
.logo{
border-radius: 50%;
}
</style>
