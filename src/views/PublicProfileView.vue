<template>
  <div class="main">
    <PublicProfile :renterId="Number(renterId)" />
  </div>
</template>

<script>
import PublicProfile from "@/components/PublicProfile.vue"

export default {
  components: {
    PublicProfile
  },
  data() {
    return {
      renterId: this.$route.params.renterId
    }
  }
}
</script>
<style scoped>
.main {
  min-height: calc(100vh - 150px);
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
</style>
