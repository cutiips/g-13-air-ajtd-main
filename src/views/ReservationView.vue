<template>
  <div class="singleRoom">
    <SingleRoom :room="reservation.roomDetails" :reservation="reservation" />
  </div>
</template>

<script>
import roomService from "../services/roomService"
import SingleRoom from "../components/SingleRoom.vue"

export default {
  name: "ReservationView",
  props: {
    resId: {
      type: String,
      required: true
    }
  },
  components: {
    SingleRoom
  },
  data() {
    return {
      reservation: {}
    }
  },
  async created() {
    try {
      const response = await roomService.fetchReservationById(this.$route.params.resId)
      this.reservation = response
      this.reservation.roomDetails = await roomService.fetchRoomById(this.reservation.room)
    } catch (error) {
      console.error("Error fetching rooms:", error)
    }
  }
}
</script>

<style lang="scss" scoped></style>
