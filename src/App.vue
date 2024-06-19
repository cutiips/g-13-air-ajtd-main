<template>
  <div id="app">
    <AppNavBar />
    <router-view />
    <FooterComponent />
  </div>
</template>

<script>
import AppNavBar from "./components/AppNavbar.vue"
import FooterComponent from "./components/FooterComponenent.vue"

export default {
  name: "App",
  components: {
    AppNavBar,
    FooterComponent
  }
}
</script>

<style>
#app {
  height: 100vh;
}
</style>
