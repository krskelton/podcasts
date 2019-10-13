<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <Podcasts podcasts="Podcasts:"/>
  </div>
</template>

<script>
import Podcasts from './components/Podcasts.vue'

export default {
  name: 'app',
  components: {
    Podcasts
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
