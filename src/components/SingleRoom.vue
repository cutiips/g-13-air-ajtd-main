<template>
  <div class="message-container">
    <div v-if="favoriteAddedMessage" class="confirmation-message" :class="favoriteAddedClass">
      {{ favoriteAddedMessage }}
    </div>
  </div>
  <div class="container">
    <div class="fav-btn-cont">
      <i
        class="fa-solid fa-heart"
        v-if="isLoggedIn && isFavorite"
        @click="addToFavorites(room.id)"
      ></i>
      <i
        class="fa-regular fa-heart"
        v-if="isLoggedIn && !isFavorite"
        @click="addToFavorites(room.id)"
      ></i>
    </div>
    <CCarousel
      controls
      dark
      class="carousel-single"
      v-if="room && room.pictures && room.pictures.length > 0"
    >
      <CCarouselItem v-for="(picture, idx) in room.pictures" :key="idx">
        <img :src="picture.image" alt="Room Picture" />
      </CCarouselItem>
    </CCarousel>
    <div class="details">
      <div class="details-inner">
        <div class="details-basic">
          <div class="room-top">
            <h5>{{ room.room_name }}</h5>
            <div class="star-rating">
              <i v-for="n in filledStars" :key="'filled' + n" class="fas fa-star"></i>
              <i v-if="hasHalfStar" class="fas fa-star-half-alt"></i>
              <i v-for="n in emptyStarsArray" :key="'empty' + n" class="far fa-star"></i>
            </div>
          </div>
          <p v-if="room && room.address">{{ getAddress(room.address) }}</p>
          <p v-else>Address not available</p>
          <p>{{ room.description }}</p>
        </div>
        <div class="details-features">
          <h5>Features</h5>
          <ul>
            <li v-if="room && room.pets_allowed">
              <i class="fa-solid fa-circle-check"></i> Pets allowed
            </li>
            <li v-if="room && room.smoking_allowed">
              <i class="fa-solid fa-circle-check"></i> Smoking allowed
            </li>
            <li v-if="room && room.has_elevator">
              <i class="fa-solid fa-circle-check"></i> Elevator
            </li>
            <li v-if="!room.pets_allowed && !room.smoking_allowed && !room.has_elevator">
              <i class="fa-solid fa-circle-xmark"></i> None
            </li>
          </ul>
        </div>
        <RatingList :roomId="room.id" @average-rating="updateAverageRating" />
        <ReviewList :roomId="room.id" />
      </div>
      <div class="details-inner">
        <Reservation
          class="reservation-menu"
          :room="room"
          :searchDate="searchDate"
          :res="reservation"
        />
        <MapComponent class="map" :coords="coords" v-if="room && room.address && showMap" />
      </div>
    </div>
  </div>
</template>

<script>
import { CCarousel, CCarouselItem } from "@coreui/vue"
import Reservation from "./Reservation.vue"
import MapComponent from "./MapComponent.vue"
import RatingList from "./RatingList.vue"
import ReviewList from "./ReviewList.vue"
import authService from "@/services/authService"
import roomService from "@/services/roomService"
import axios from "axios"

export default {
  name: "SingleRoom",
  components: {
    CCarousel,
    CCarouselItem,
    Reservation,
    MapComponent,
    RatingList,
    ReviewList
  },
  props: {
    room: {
      type: Object,
      required: true
    },
    searchDate: {
      type: Array,
      required: false
    },
    reservation: {
      type: Object,
      required: false
    }
  },
  data() {
    return {
      coords: [46.1759703, 6.1392327],
      showMap: false,
      filledStars: 0,
      hasHalfStar: false,
      emptyStarsArray: [],
      isFavorite: false,
      favoriteAddedMessage: "",
      favoriteAddedClass: "",
      isLoggedIn: authService.isLoggedIn()
    }
  },
  created() {
    if (this.isLoggedIn) {
      authService
        .getUser()
        .then((user) => {
          roomService
            .isFavorite(this.room.id, user.pk)
            .then((isFavorite) => {
              this.isFavorite = isFavorite
            })
            .catch((error) => {
              console.error("Error checking if room is favorite:", error)
            })
        })
        .catch((error) => {
          console.error("Error getting user:", error)
        })
    }
  },
  mounted() {
    if (this.room && this.room.address) {
      this.fetchCoordinates()
    } else {
      console.error("Room or room address is undefined in mounted")
    }
  },
  methods: {
    updateAverageRating(average) {
      this.filledStars = Math.floor(average)
      this.hasHalfStar = average % 1 >= 0.5
      this.emptyStarsArray = Array(5 - this.filledStars - (this.hasHalfStar ? 1 : 0)).fill(0)
    },
    getAddress(address) {
      return `${address[0].streetname}, ${address[0].city}, ${address[0].country}`
    },
    async fetchCoordinates() {
      if (this.room && this.room.address && this.room.address.length > 0) {
        const address = this.getAddress(this.room.address)
        try {
          const response = await axios.get("https://nominatim.openstreetmap.org/search", {
            params: {
              q: address,
              format: "json",
              limit: 1
            }
          })
          if (response.data && response.data.length > 0) {
            this.showMap = true
            const location = response.data[0]
            this.coords = [parseFloat(location.lat), parseFloat(location.lon)]
          } else {
            console.error("No coordinates found for the given address.")
          }
        } catch (error) {
          console.error("Error fetching coordinates:", error)
        }
      } else {
        console.error("Room address is undefined or empty in fetchCoordinates")
      }
    },
    async addToFavorites(roomId) {
      if (!this.isLoggedIn) {
        this.errorMessage = "User not authenticated"
        return
      }
      try {
        const user = await authService.getUser()
        const userId = user.pk

        const isFavorite = await roomService.isFavorite(roomId, userId)
        if (isFavorite) {
          const favorites = await roomService.getFavorites()
          const favoriteId = favorites.find((favorite) => favorite.room === roomId).id
          await roomService.removeFavorite(favoriteId)
          this.isFavorite = false
          this.favoriteAddedMessage = "Room removed from favorites"
          this.favoriteAddedClass = "error-message"
          setTimeout(() => {
            this.favoriteAddedMessage = ""
          }, 3000)
          return
        }

        await roomService.addToFavorites(roomId, userId)
        this.isFavorite = true
        this.favoriteAddedMessage = "Room added to favorites"
        this.favoriteAddedClass = "success-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
      } catch (error) {
        console.error("Error adding/removing favorites:", error)
        this.favoriteAddedMessage = "Erreur lors de la modifications des favoris."
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
      }
    }
  }
}
</script>

<style>
.fav-btn-cont {
  position: relative;
  top: 40px;
  z-index: 5;
  left: 43%;
}
.star-rating .fa-star-half-stroke,
.star-rating .fa-star-half-alt,
.star-rating .fa-star {
  color: #ffd700;
}
.fa-star {
  margin-bottom: 0;
  margin-bottom: 0;
}
.bold {
  font-weight: bold;
  font-weight: bold;
}
.carousel-single img {
  width: 100%;
  height: 600px;
  max-width: 1200px;
  object-fit: cover;
  object-position: center;
  border-radius: 30px;
  transition: all 0.5s ease;
  width: 100%;
  height: 600px;
  max-width: 1200px;
  object-fit: cover;
  object-position: center;
  border-radius: 30px;
  transition: all 0.5s ease;
}
.carousel-single {
  width: 100%;
  height: 600px;
  max-width: 1200px;
  border-radius: 30px;
  transition: all 0.5s ease;
  margin: 0 auto;
}
.container {
  display: flex;
  flex-direction: column;
  justify-content: baseline;
  align-items: center;
  width: 100%;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  margin-top: 2vh;
  min-height: calc(100vh - 180px);
}
@media screen and (max-width: 1199px) {
  .carousel-single img {
    height: 500px;
  }
  .carousel-single {
    height: 500px;
  }
  .carousel-single img {
    height: 500px;
  }
  .carousel-single {
    height: 500px;
  }
}
@media screen and (max-width: 992px) {
  .carousel-single img {
    height: 400px;
  }
  .carousel-single {
    height: 400px;
  }
  .carousel-single img {
    height: 400px;
  }
  .carousel-single {
    height: 400px;
  }
}
@media screen and (max-width: 768px) {
  .carousel-single img {
    height: 300px;
  }
  .carousel-single {
    height: 300px;
  }
  .carousel-single img {
    height: 300px;
  }
  .carousel-single {
    height: 300px;
  }
}
.details {
  width: 100%;
  padding: 3vh 2vw;
  text-align: justify;
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 20px;
  max-width: 1200px;
}
.details-inner:nth-child(1) {
  width: 65%;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  width: 65%;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}
.details-inner:nth-child(2) {
  width: 35%;
  width: 35%;
}
.details-basic {
  margin-bottom: 2vh;
  margin-bottom: 2vh;
}
.details-features ul {
  list-style-type: none;
  text-align: left;
  padding-left: 15px;
  list-style-type: none;
  text-align: left;
  padding-left: 15px;
}
.room-top {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.room-top h5 {
  margin-bottom: 0;
  margin-bottom: 0;
}
.reservation-menu {
  width: 100%;
  margin: 0 auto 20px;
  width: 100%;
  margin: 0 auto 20px;
}
@media screen and (max-width: 1200px) {
  .details {
    flex-direction: column;
    gap: 0;
  }
  .details-inner:nth-child(1) {
    width: 100%;
  }
  .details-inner:nth-child(2) {
    width: 100%;
  }
  .reservation-menu {
    margin: 3vh auto;
  }
  .details {
    flex-direction: column;
    gap: 0;
  }
  .details-inner:nth-child(1) {
    width: 100%;
  }
  .details-inner:nth-child(2) {
    width: 100%;
  }
  .reservation-menu {
    margin: 3vh auto;
  }
}
@media screen and (max-width: 768px) {
  .details {
    padding: 10px;
  }
  .details-inner:nth-child(1) {
    width: 100%;
  }
  .details-inner:nth-child(2) {
    width: 100%;
  }
  .details {
    padding: 10px;
  }
  .details-inner:nth-child(1) {
    width: 100%;
  }
  .details-inner:nth-child(2) {
    width: 100%;
  }
}
.rating,
.review,
.no-review {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
  border-radius: 10px;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
  border-radius: 10px;
  background-color: #f9f9f9;
}
.rating h2,
.review h2,
.no-review h2 {
  margin-top: 20px;
  font-size: 1.5em;
  margin-top: 20px;
  font-size: 1.5em;
}
.rating p,
.review p,
.no-review p {
  font-size: 1.2em;
  margin: 5px 0;
  font-size: 1.2em;
  margin: 5px 0;
}
.rating small,
.review small {
  font-size: 0.9em;
  color: #666;
  font-size: 0.9em;
  color: #666;
}
</style>
