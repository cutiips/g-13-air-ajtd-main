<template>
  <li class="nav-item dropdown">
    <a
      class="nav-link dropdown-toggle"
      href="#"
      id="navbarDropdown"
      role="button"
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      Notifications
    </a>
    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
      <li v-if="notifications.length === 0" class="dropdown-item">No notifications</li>
      <li v-for="notification in notifications" :key="notification.id" class="dropdown-item">
        {{ notification.message }}
      </li>
    </ul>
  </li>
</template>

<script>
import notificationService from "../services/notificationService"
import authService from "../services/authService"

export default {
  name: "NotificationDropdown",
  data() {
    return {
      notifications: []
    }
  },
  computed: {
    isLoggedIn() {
      return authService.isLoggedIn()
    }
  },
  created() {
    if (this.isLoggedIn) {
      this.fetchNotifications()
    }
  },
  methods: {
    async fetchNotifications() {
      try {
        const response = await notificationService.getRecentNotifications()
        this.notifications = response.data
      } catch (error) {
        console.error("Failed to fetch notifications", error)
      }
    }
  }
}
</script>
