<template>
  <div>
    <div class="message-container">
      <div v-if="favoriteAddedMessage" class="confirmation-message" :class="favoriteAddedClass">
        {{ favoriteAddedMessage }}
      </div>
    </div>

    <div class="room-container">
      <div class="container-room">
        <div class="room" v-for="(room, index) in paginatedRooms" :key="index">
          <CCarousel
            controls
            dark
            :interval="false"
            class="carousel"
            v-if="room.pictures.length > 0"
          >
            <CCarouselItem v-for="(picture, idx) in room.pictures" :key="idx">
              <img :src="picture.image" alt="Room Picture" />
            </CCarouselItem>
          </CCarousel>
          <div class="room-top">
            <h5>{{ room.room_name }}</h5>
            <div class="star-rating">
              <i
                v-for="n in getFilledStars(room.rating)"
                :key="'filled' + n"
                class="fas fa-star"
              ></i>
              <i v-if="hasHalfStar(room.rating)" class="fas fa-star-half-alt"></i>
              <i v-for="n in getEmptyStars(room.rating)" :key="'empty' + n" class="far fa-star"></i>
            </div>
          </div>
          <p>
            <span class="bold">{{ room.price }} Frs.</span>/night
          </p>
          <p v-if="room.address.length > 0">{{ getAddress(room.address) }}</p>
          <p v-else>Address not available</p>
          <div class="btn-container">
            <button class="viewroom-btn">
              <router-link class="link" :to="{ name: 'singleroom', params: { roomId: room.id } }">
                View Room
              </router-link>
            </button>
            <i
              class="fa-solid fa-heart"
              v-if="isLoggedIn && room.isFavorite"
              @click="addToFavorites(room.id)"
            ></i>
            <i
              class="fa-regular fa-heart"
              v-if="isLoggedIn && !room.isFavorite"
              @click="addToFavorites(room.id)"
            ></i>
          </div>
          <RatingList :roomId="room.id" @average-rating="updateRoomRating(index, $event)" />
        </div>
      </div>
    </div>
    <div class="pagination-container">
      <PaginationComponent
        class="pagination"
        :disabled="noPagination"
        :currentPage="currentPage"
        :totalPages="totalPages"
        @page-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
import roomService from "../services/roomService"
import { CCarousel, CCarouselItem } from "@coreui/vue"
import PaginationComponent from "./PaginationComponent.vue"
import authService from "../services/authService"
import RatingList from "./RatingList.vue"

export default {
  props: {
    searchQuery: {
      type: String,
      required: true
    },
    currentPage: {
      type: Number,
      required: true
    },
    perPage: {
      type: Number,
      required: true
    },
    noPagination: {
      type: Boolean,
      default: false
    },
    priceRange: {
      type: Array,
      required: false
    },
    date: {
      type: Array,
      required: false
    },
    features: {
      type: Object,
      required: false
    }
  },
  components: {
    CCarousel,
    CCarouselItem,
    PaginationComponent,
    RatingList
  },
  data() {
    return {
      rooms: [],
      favoriteAddedMessage: "",
      favoriteAddedClass: "",
      isLoggedIn: authService.isLoggedIn()
    }
  },
  async created() {
    this.$authService = authService
    this.$roomService = roomService

    try {
      const response = await roomService.fetchRooms()
      const rooms = response
      const prices = rooms.map((room) => room.price)
      const pricesRange = [Math.min(...prices), Math.max(...prices)]
      this.$emit("min-max-price", pricesRange)
      if (this.isLoggedIn) {
        const user = await authService.getUser()
        const userId = user.pk

        const favoritesStatusPromises = rooms.map(async (room) => {
          room.isFavorite = await roomService.isFavorite(room.id, userId)
          return room
        })
        this.rooms = await Promise.all(favoritesStatusPromises)
      } else {
        this.rooms = rooms
      }
    } catch (error) {
      console.error("Error fetching rooms:", error)
    }
  },
  methods: {
    getAddress(address) {
      return `${address[0].streetname}, ${address[0].city}, ${address[0].country}`
    },
    handlePageChange(pageNumber) {
      this.$emit("page-change", pageNumber)
    },
    checkFeatures(room) {
      if (!this.features) return true
      const { pets, smoking, elevator } = this.features
      if (pets && !room.pets_allowed) return false
      if (smoking && !room.smoking_allowed) return false
      if (elevator && !room.has_elevator) return false
      return true
    },
    async addToFavorites(roomId) {
      if (!this.$authService.isLoggedIn()) {
        this.errorMessage = "User not authenticated"
        return
      }
      try {
        const user = await this.$authService.getUser()
        const userId = user.pk

        const isFavorite = await this.$roomService.isFavorite(roomId, userId)
        if (isFavorite) {
          const favorites = await this.$roomService.getFavorites()
          const favoriteId = favorites.find((favorite) => favorite.room === roomId).id
          await this.$roomService.removeFavorite(favoriteId)
          this.rooms.find((room) => room.id === roomId).isFavorite = false
          this.favoriteAddedMessage = "Room removed from favorites"
          this.favoriteAddedClass = "error-message"
          setTimeout(() => {
            this.favoriteAddedMessage = ""
          }, 3000)
          return
        }

        await this.$roomService.addToFavorites(roomId, userId)
        this.rooms.find((room) => room.id === roomId).isFavorite = true
        this.favoriteAdded = true
        this.favoriteAddedMessage = "Room added to favorites"
        this.favoriteAddedClass = "success-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
      } catch (error) {
        console.error("Error adding to favorites:", error)
        this.favoriteAddedMessage = "Erreur lors de l'ajout aux favoris."
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
      }
    },
    updateRoomRating(index, average) {
      if (!isNaN(average)) {
        this.rooms = [
          ...this.rooms.slice(0, index),
          { ...this.rooms[index], rating: average },
          ...this.rooms.slice(index + 1)
        ]
      } else {
        this.rooms = [
          ...this.rooms.slice(0, index),
          { ...this.rooms[index], rating: 0 },
          ...this.rooms.slice(index + 1)
        ]
      }
    },
    getFilledStars(rating) {
      if (isNaN(rating)) return 0
      return Math.floor(rating)
    },
    hasHalfStar(rating) {
      if (isNaN(rating)) return false
      return rating % 1 >= 0.5
    },
    getEmptyStars(rating) {
      if (isNaN(rating)) return 5
      return 5 - Math.floor(rating) - (this.hasHalfStar(rating) ? 1 : 0)
    }
  },

  computed: {
    paginatedRooms() {
    const startIndex = (this.currentPage - 1) * this.perPage
    const endIndex = startIndex + this.perPage
    return this.filteredRooms.slice(startIndex, endIndex)
  },
  filteredRooms() {
    return this.rooms.filter((room) => {
      const searchQuery = this.searchQuery.toLowerCase()
      const roomName = room.room_name.toLowerCase()
      const address = this.getAddress(room.address).toLowerCase()
      const price = room.price
      const priceRange = this.priceRange || [0, Infinity]

      if (this.date && this.date.length === 2) {
        const startDate = new Date(this.date[0])
        const endDate = new Date(this.date[1])

        const hasOverlappingReservation = room.reservation.some((reservation) => {
          const reservationStartDate = new Date(reservation.start_date)
          const reservationEndDate = new Date(reservation.end_date)
          return startDate <= reservationEndDate && endDate >= reservationStartDate
        })

        if (hasOverlappingReservation) {
          return false
        }
      }

      return (
        (roomName.includes(searchQuery) || address.includes(searchQuery)) &&
        price >= priceRange[0] &&
        price <= priceRange[1] &&
        this.checkFeatures(room)
      )
    })
  },
  totalPages() {
    return Math.ceil(this.filteredRooms.length / this.perPage)
  }
  },
  mounted() {
    localStorage.removeItem("searchDate")
  }
}
</script>

<style>
.star-rating .fa-star,
.star-rating .fa-star-half-alt {
  color: #ffd700;
}
.message-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 10vh;
  position: fixed;
  top: 0;
  left: calc(50% - 150px);
  color: red;
}
.confirmation-message {
  padding: 10px;
  margin: 10px auto;
  border-radius: 5px;
  text-align: center;
  top: 50px;
  width: 300px;
  animation: slideDown 0.5s;
  z-index: 10;
}

@keyframes slideDown {
  0% {
    transform: translateY(-100%);
  }
  100% {
    transform: translateY(0);
  }
}

.success-message {
  color: green;
  background-color: #f0f9f0;
  border: 1px solid #a4de95;
}

.error-message {
  color: red;
  background-color: #f9f0f0;
  border: 1px solid #de9595;
}

.container-room {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 1vh;
  gap: 20px;
}
.carousel {
  width: 100%;
}
.carousel-control-next-icon,
.carousel-control-prev-icon {
  filter: invert(1);
}
.room {
  display: flex;
  flex-direction: column;
  justify-content: left;
  margin: 10px;
  border-radius: 10px;
  width: 300px;
  min-height: 430px;
  text-align: left;
}
.room img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 10px;
}
.room p {
  margin: 0 auto 5px 0;
  padding: 0;
}
.pagination {
  position: relative;
  bottom: 20px;
}
.room-container {
  min-height: calc(100vh - 280px);
}

.pagination-container {
  margin-top: auto;
}
.link {
  text-decoration: none;
  color: white;
}
.viewroom-btn {
  margin: 0;
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  color: white;
  border-radius: 10px;
  outline: none;
  border: none;
  padding: 5px 10px;
  width: fit-content;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}
.viewroom-btn .link {
  color: white;
  transition: all 0.3s ease;
}
.viewroom-btn:hover .link {
  color: #d4d4d4;
}
.btn-container {
  display: flex;
  justify-content: space-between;
  padding: 0;
  align-items: center;
}
@media screen and (max-width: 768px) {
  .room {
    min-height: 330px;
  }
  .room img {
    height: 200px;
  }
}
.fa-heart {
  font-size: 1.5em;
  cursor: pointer;
}
.fa-solid.fa-heart {
  color: red;
}
.fa-regular.fa-heart {
  color: black;
}
</style>
