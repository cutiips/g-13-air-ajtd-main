<template>
  <div class="singleRoom">
    <SingleRoom v-if="room && room.address" :room="room" :searchDate="searchDate" />
  </div>
</template>

<script>
import roomService from "@/services/roomService"
import SingleRoom from "@/components/SingleRoom.vue"

export default {
  name: "SingleRoomView",
  props: {
    roomId: {
      type: String,
      required: true
    }
  },
  components: {
    SingleRoom
  },
  data() {
    return {
      searchDate: JSON.parse(localStorage.getItem("searchDate")) || [],
      room: null
    }
  },
  async created() {
    try {
      const response = await roomService.fetchRoomById(this.$route.params.roomId)
      this.room = response
    } catch (error) {
      console.error("Error fetching rooms:", error)
    }
  }
}
</script>

<style>
.singleRoom {
  min-height: calc(100vh - 200px);
}
</style>
