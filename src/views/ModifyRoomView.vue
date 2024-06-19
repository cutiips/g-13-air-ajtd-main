<template>
  <div>
    <AddRoom :modifyRoomData="room" />
  </div>
</template>

<script>
import roomService from "@/services/roomService"
import authService from "@/services/authService"
import AddRoom from "../components/AddRoom.vue"
export default {
  name: "ModifyRoom",
  components: {
    AddRoom
  },
  data() {
    return {
      room: {}
    }
  },
  created() {
    this.fetchRoom()
  },
  methods: {
    fetchRoom() {
      roomService
        .fetchRoomById(this.$route.params.roomId)
        .then((response) => {
          this.room = response
          if (this.room.owner !== authService.user.value.pk) {
            this.$router.push({ name: "profile" })
          }
        })
        .catch(() => {
          this.$router.push({ name: "profile" })
        })
    }
  },
  watch: {
    room: {
      deep: true
    }
  }
}
</script>
