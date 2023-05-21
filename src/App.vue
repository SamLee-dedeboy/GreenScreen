<script setup lang="ts">
import Home from './components/Home/Home.vue'
import SlideShow from './components/SlideShow/SlideShow.vue';
</script>

<template>
  <div class="app-body">
    <SlideShow></SlideShow>
    <Home></Home>
  </div>
</template>

<style scoped>
.app-body {
  width: 100vw;
  height: 100vh;
}
</style>
