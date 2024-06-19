<template>
  <div class="pending-book" v-if="reservations.length > 0">
    <div v-if="confirmationMessage" class="confirmation-message">{{ confirmationMessage }}</div>
    <div v-for="res in reservations" :key="res.id">
      <div class="pending-booking">
        <p>{{ formatDate(res.start_date) }} - {{ formatDate(res.end_date) }}</p>
        <p>{{ res.guests }} guest{{ res.guests > 1 ? "s" : "" }}</p>
        <div>
          <button @click="acceptBooking(res)" class="viewroom-btn">Accept</button>
          <button @click="rejectBooking(res)" class="viewroom-btn">Dismiss</button>
        </div>
      </div>
      <hr class="bar" v-if="reservations.indexOf(res) !== reservations.length - 1" />
    </div>
  </div>
</template>

<script>
import roomService from "@/services/roomService"

export default {
  name: "ConfirmBooking",
  props: {
    roomId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      reservations: [],
      confirmationMessage: ""
    }
  },
  watch: {
    roomId: {
      immediate: true,
      handler(newRoomId) {
        this.fetchReservations(newRoomId)
      }
    }
  },
  methods: {
    fetchReservations(roomId) {
      roomService
        .fetchRoomById(roomId)
        .then((response) => {
          const today = new Date()
          today.setHours(0, 0, 0, 0)
          this.reservations = response.reservation.filter(
            (res) => res.status === "pending" && new Date(res.start_date) >= today
          )
        })
        .catch((error) => {
          console.error("Error fetching reservations:", error)
        })
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    acceptBooking(reservation) {
      reservation.status = "accepted"
      roomService
        .updateReservation(reservation.id, reservation)
        .then(() => {
          this.confirmationMessage = "Reservation accepted successfully!"
          setTimeout(() => {
            this.$router.push("/profile")
          }, 2000)
        })
        .catch((error) => {
          console.error("Error updating reservation:", error)
        })
    },
    rejectBooking(reservation) {
      roomService
        .deleteReservation(reservation.id)
        .then(() => {
          this.confirmationMessage = "Reservation dismissed successfully!"
          setTimeout(() => {
            this.$router.push("/profile")
          }, 2000)
        })
        .catch((error) => {
          console.error("Error deleting reservation:", error)
        })
    }
  }
}
</script>

<style scoped>
.pending-book {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
}

.pending-booking {
  display: flex;
  flex-direction: row;
  width: 40vw;
  margin: 10px 0;
  min-width: 300px;
  max-width: 800px;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
}

.pending-booking div {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 1.8vw;
}
p {
  margin: 0;
}

.confirmation-message {
  padding: 10px;
  color: #fff;
  background-color: #28a745;
  border-radius: 5px;
  text-align: center;
  animation: slideDown 0.5s ease-in-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
