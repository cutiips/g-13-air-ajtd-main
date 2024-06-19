<template>
  <div class="booking">
    <h2>Confirm Booking</h2>
    <ConfirmBooking :roomId="room" />
  </div>
</template>

<script>
import ConfirmBooking from "../components/ConfirmBooking.vue"

export default {
  name: "ConfirmBookingView",
  components: {
    ConfirmBooking
  },
  data() {
    return {
      room: parseInt(this.$route.params.roomId)
    }
  }
}
</script>

<style scoped>
.booking {
  min-height: calc(100vh - 150px);
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  flex-direction: column;
}

h2 {
  margin-bottom: 5vh;
}
</style>
