<template>
  <div class="center">
    <ProfileComponent :user="user" @edit="editing = true" />
  </div>
</template>

<script>
import ProfileComponent from "../components/ProfileComponent.vue"

export default {
  components: {
    ProfileComponent
  },
  data() {
    return {
      editing: false,
      user: {}
    }
  },
  methods: {
    saveChanges(updatedUser) {
      this.user = updatedUser
      this.editing = false
    }
  }
}
</script>

<style scoped>
body {
  width: 100%;
  height: 100%;
  --color: #e1e1e1;
  background-color: #f3f3f3;
  background-image: linear-gradient(
      0deg,
      transparent 24%,
      var(--color) 25%,
      var(--color) 26%,
      transparent 27%,
      transparent 74%,
      var(--color) 75%,
      var(--color) 76%,
      transparent 77%,
      transparent
    ),
    linear-gradient(
      90deg,
      transparent 24%,
      var(--color) 25%,
      var(--color) 26%,
      transparent 27%,
      transparent 74%,
      var(--color) 75%,
      var(--color) 76%,
      transparent 77%,
      transparent
    );
  background-size: 55px 55px;
}

.center {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
}

.carousel button {
  filter: invert(1);
}
</style>
