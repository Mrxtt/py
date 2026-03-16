<template>
  <div id="app">
    <template v-if="route.path === '/login'">
      <router-view />
    </template>
    <template v-else>
      <Layout>
        <router-view />
      </Layout>
    </template>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import Layout from '@/components/layout/Layout.vue';

const route = useRoute();
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
}
</style>
