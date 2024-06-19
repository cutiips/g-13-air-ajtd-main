<template>
  <nav class="navbar navbar-expand-lg navbar-dark custom-nav-bg">
    <div class="container-fluid">
      <router-link class="navbar-brand" :to="{ name: 'home' }"
        ><img class="logo" alt="logo" src="../assets/logo/logo-color.png"
      /></router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mx-auto ustify-content-center">
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'home' }">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'rooms' }">Rooms</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" :to="{ name: 'addroom' }">Add a room</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" :to="{ name: 'profile' }">Profile</router-link>
          </li>
          <li class="nav-item" v-else>
            <router-link class="nav-link" :to="{ name: 'login' }">Login</router-link>
          </li>
          <NotificationDropdown />
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import authService from "../services/authService"
import NotificationDropdown from "./NotificationDropdown.vue"

export default {
  name: "AppNavbar",
  components: {
    NotificationDropdown
  },
  computed: {
    isLoggedIn() {
      return authService.isLoggedIn()
    }
  }
}
</script>

<style>
.custom-nav-bg {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  color: #fff;
}
.navbar {
  padding: 0;
}
ul.navbar-nav.mx-auto li {
  text-align: center;
}
ul.navbar-nav.mx-auto li .nav-link {
  white-space: nowrap;
  margin-right: 20px;
  color: #fff;
  font-size: 1.2em;
  transition: all 0.2s ease;
  font-weight: 500;
}
ul.navbar-nav.mx-auto li .nav-link:hover {
  color: #e0e0e0;
}
.navbar-toggler {
  border: none;
  box-shadow: none;
}
.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 32 32' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba(255, 255, 255, 1)' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 8h24M4 16h24M4 24h24'/%3E%3C/svg%3E");
}
.logo {
  width: 50px;
  height: auto;
}
</style>
