<template>
  <div id="reservation" class="reservation">
    <form class="reservation-width">
      <h4>Reservation</h4>
      <div class="reservation-top">
        <h5>Price:</h5>
        <p>
          <span class="bold">{{ getPrice() }} Frs.</span>
        </p>
      </div>
      <div class="guests">
        <p>Guests:</p>
        <div class="change">
          <div class="change-btn" @click="handleGuestChange('subtract')">-</div>
          <span class="change-num">{{ guests }}</span>
          <div class="change-btn" @click="handleGuestChange('add')">+</div>
        </div>
      </div>
      <VueDatePicker
        class="datepicker"
        v-model="date"
        :clearable="true"
        :min-date="new Date()"
        :enable-time-picker="false"
        :multi-calendars="{ static: false }"
        auto-apply
        no-today
        :range="{ noDisabledRange: true }"
        :disabled-dates="disabledDates"
        placeholder="Dates ..."
        required
      >
      </VueDatePicker>
      <button v-if="res" class="book-btn" @click="changeReservation">Change booking</button>
      <button v-else class="book-btn" @click="bookReservation">Book</button>
    </form>
  </div>
</template>

<script>
import VueDatePicker from "@vuepic/vue-datepicker"
import "@vuepic/vue-datepicker/dist/main.css"
import roomService from "../services/roomService"
import authService from "../services/authService"

export default {
  name: "RoomReservation",
  components: { VueDatePicker },
  props: {
    room: {
      type: Object,
      required: true
    },
    searchDate: {
      type: Array,
      required: false
    },
    res: {
      type: Object,
      required: false
    }
  },
  data() {
    return {
      date: [this.res ? this.res.start_date : "", this.res ? this.res.end_date : ""],
      guests: this.res ? this.res.guests : 1
    }
  },
  methods: {
    handleGuestChange(action) {
      if (action === "add") {
        if (this.guests < this.room.max_guests || this.guests < 20) {
          this.guests++
        }
      } else {
        if (this.guests > 1) {
          this.guests--
        }
      }
    },
    getPrice() {
      if (this.date && this.date[0] && this.date[1] && this.date.length > 0) {
        const startDate = new Date(this.date[0])
        const endDate = new Date(this.date[1])
        const days = (endDate - startDate) / (1000 * 60 * 60 * 24)
        return this.room.price * days * this.guests
      }
      return this.room.price * this.guests
    },
    generateDateRange(start, end) {
      const dates = []
      let currentDate = new Date(start)
      const endDate = new Date(end)
      while (currentDate <= endDate) {
        dates.push(new Date(currentDate).toISOString().split("T")[0])
        currentDate.setDate(currentDate.getDate() + 1)
      }
      return dates
    },
    checkDateConflicts(dateRange, alreadyBookedDates) {
      const dates = this.generateDateRange(dateRange[0], dateRange[1])
      return dates.some((date) => alreadyBookedDates.includes(date))
    },
    async bookReservation() {
      try {
        const user = await authService.getCurrentUserId()
        const formatDate = (dateString) => {
          const date = new Date(dateString)
          date.setDate(date.getDate() + 1)
          const formattedDate = date.toISOString().split("T")[0]
          return formattedDate
        }
        const payload = {
          start_date: formatDate(this.date[0]),
          end_date: formatDate(this.date[1]),
          guests: this.guests,
          room: this.room.id,
          user: user
        }
        await roomService.createReservation(payload)
        this.$router.push({ name: "profile" })
      } catch (error) {
        console.error("Error creating reservation:", error.response ? error.response.data : error)
      }
    },
    async changeReservation() {
      try {
        const user = await authService.getCurrentUserId()
        const formatDate = (dateString) => {
          const date = new Date(dateString)
          const formattedDate = date.toISOString().split("T")[0]
          return formattedDate
        }

        const payload = {
          start_date: formatDate(this.date[0]),
          end_date: formatDate(this.date[1]),
          guests: this.guests,
          room: this.room.id,
          user: user
        }

        await roomService.updateReservation(this.res.id, payload)
        this.$router.push({ name: "profile" })
      } catch (error) {
        console.error("Error changing reservation:", error.response ? error.response.data : error)
      }
    }
  },
  created() {
    if (this.searchDate && this.searchDate.length > 0) {
      if (this.checkDateConflicts(this.searchDate, this.disabledDates)) {
        this.date = []
      } else {
        this.date = this.searchDate
      }
    }
  },
  computed: {
    disabledDates() {
      let disabledDates = []
      if (this.room.reservation && this.room.reservation.length > 0) {
        this.room.reservation.forEach((reservation) => {
          if (this.res && reservation.id !== this.res.id) {
            const startDate = new Date(reservation.start_date)
            const endDate = new Date(reservation.end_date)
            const dates = this.generateDateRange(startDate, endDate)
            disabledDates.push(...dates)
          } else {
            const startDate = new Date(reservation.start_date)
            const endDate = new Date(reservation.end_date)
            const dates = this.generateDateRange(startDate, endDate)
            disabledDates.push(...dates)
          }
        })
      }
      return disabledDates
    }
  },
  watch: {
    date(newDate) {
      this.date = newDate
      if (newDate && newDate.length === 2) {
        if (this.checkDateConflicts(newDate, this.disabledDates)) {
          this.date = []
        } else {
          localStorage.setItem("searchDate", JSON.stringify(this.date))
        }
      } else {
        localStorage.removeItem("searchDate")
      }
    }
  }
}
</script>

<style>
.reservation-top {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin: 10px auto;
}

.reservation p {
  margin: 0;
}

.reservation-top h5 {
  margin: 0;
}

.bold {
  font-weight: bold;
}

.reservation {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 1px solid #aaa;
  border-radius: 20px;
  padding: 20px 20px;
  transition: all 0.3s ease;
}

.reservation h4 {
  text-align: center;
}

.reservation .room-top {
  display: flex;
  justify-content: left;
  align-items: center;
  margin: 10px 0;
  gap: 10px;
}

.reservation-width {
  max-width: 300px;
  margin: auto;
}

.guests {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 50px;
  margin: 10px 0;
  user-select: none;
}

.reservation .change {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
  gap: 10px;
  float: right;
}

.change-btn {
  background-color: #ffffff;
  border: 1px solid #aaa;
  border-radius: 50%;
  cursor: pointer;
  width: 30px;
  height: 30px;
  padding-top: 1px;
  text-align: center;
}

.change-btn:hover {
  background-color: #f0f0f0;
}

.change-num {
  width: 25px;
  text-align: center;
}

.book-btn {
  margin: auto;
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  color: white;
  border-radius: 10px;
  outline: none;
  border: none;
  font-size: 1.2em;
  width: 100%;
  text-align: center;
  padding: 5px 0;
  transition: all 0.3s ease;
  cursor: pointer;
  font-weight: 600;
}

.book-btn:hover {
  color: #d4d4d4;
}

.datepicker {
  margin: 10px 0;
}

@media screen and (max-width: 310px) {
  .guests {
    flex-direction: column;
    gap: 10px;
    justify-content: left;
    align-items: baseline;
  }
}
</style>
