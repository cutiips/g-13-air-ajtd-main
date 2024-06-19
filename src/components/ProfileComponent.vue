<template>
  <div class="container">
    <div class="info">
      <h2>Profile</h2>
      <div v-if="confirmed || alreadyConfirmed" class="message-container">
        <p v-if="confirmed" class="confirmed-message">Your email has been confirmed</p>
        <p v-if="alreadyConfirmed" class="confirmed-message">Your email is already confirmed</p>
      </div>
      <p>
        Welcome, <strong>{{ first_name }} {{ last_name }}</strong>
      </p>
      <p>Your username: {{ username }}</p>
      <p>Your e-mail: {{ email }}</p>
      <button class="btn" @click="editProfile">Edit</button>
      <button class="btn btn-logout" @click="logout">Logout</button>
    </div>

    <div class="reservations">
      <h2>Current Reservations</h2>
      <div v-if="currentReservations.length > 0">
        <CCarousel controls dark :interval="false" :key="carouselKey">
          <CCarouselItem v-for="(reservation, index) in currentReservations" :key="index">
            <div class="carousel-element">
              <h3>{{ reservation.roomDetails.room_name }}</h3>

              <p v-if="reservation.status == 'pending'" class="status-pending">
                <i class="fa-solid fa-triangle-exclamation"></i> Waiting for confirmation
              </p>

              <p v-if="reservation.status == 'accepted'" class="status-accepted">
                <i class="fa-solid fa-check"></i> Confirmed
              </p>

              <CCarousel class="inner-carousel">
                <CCarouselItem
                  v-for="picture in reservation.roomDetails.pictures"
                  :key="picture.id"
                >
                  <img :src="picture.image" alt="Room picture" />
                </CCarouselItem>
              </CCarousel>
              <div class="res-info">
                <div>
                  <p>
                    {{ dateFormat(reservation.start_date) }} -
                    {{ dateFormat(reservation.end_date) }} | {{ reservation.guests }} guest{{
                      reservation.guests > 1 ? "s" : ""
                    }}
                  </p>
                </div>
                <button class="btn btn-details">
                  <router-link
                    class="link"
                    :to="{ name: 'reservation', params: { resId: reservation.id } }"
                    >Details</router-link
                  >
                </button>
              </div>
            </div>
          </CCarouselItem>
        </CCarousel>
      </div>
      <div v-else>
        <h2>You don't have any current reservations.</h2>
      </div>
    </div>

    <div class="reservations">
      <h2>Past Reservations Made by You</h2>
      <div v-if="pastReservations.length > 0">
        <CCarousel controls dark :interval="false" :key="carouselKey">
          <CCarouselItem v-for="(reservation, index) in pastReservations" :key="index">
            <div class="carousel-element">
              <h3>{{ reservation.roomDetails.room_name }}</h3>
              <CCarousel class="inner-carousel">
                <CCarouselItem
                  v-for="picture in reservation.roomDetails.pictures"
                  :key="picture.id"
                >
                  <img :src="picture.image" alt="Room picture" />
                </CCarouselItem>
              </CCarousel>
              <div class="res-info">
                <div>
                  <p>
                    {{ dateFormat(reservation.start_date) }} -
                    {{ dateFormat(reservation.end_date) }} | {{ reservation.guests }} guest{{
                      reservation.guests > 1 ? "s" : ""
                    }}
                  </p>
                </div>
                <div class="res-info-btn">
                  <button
                    class="btn btn-review"
                    v-if="!reservation.is_reviewed"
                    @click="showReviewModal(reservation)"
                  >
                    <span class="link"> Add Review </span>
                  </button>
                  <button
                    class="btn btn-rating"
                    v-if="!reservation.is_rated"
                    @click="showRatingModal(reservation)"
                  >
                    <span class="link"> Add Rating </span>
                  </button>

                  <button class="btn btn-details">
                    <router-link
                      class="link"
                      :to="{ name: 'singleroom', params: { roomId: reservation.roomDetails.id } }"
                    >
                      Details
                    </router-link>
                  </button>
                </div>
              </div>
            </div>
          </CCarouselItem>
        </CCarousel>
      </div>
      <div v-else>
        <h2>You don't have any past reservations.</h2>
      </div>
    </div>

    <div class="reservations">
      <h2>Past Reservations for Your Rooms</h2>
      <div v-if="pastReservationsForOwnedRooms.length > 0">
        <CCarousel controls dark :interval="false" :key="carouselKey">
          <CCarouselItem v-for="(reservation, index) in pastReservationsForOwnedRooms" :key="index">
            <div class="carousel-element">
              <h3>{{ reservation.roomDetails.room_name }}</h3>
              <CCarousel class="inner-carousel">
                <CCarouselItem
                  v-for="picture in reservation.roomDetails.pictures"
                  :key="picture.id"
                >
                  <img :src="picture.image" alt="Room picture" />
                </CCarouselItem>
              </CCarousel>
              <div class="res-info">
                <div>
                  <p>
                    {{ dateFormat(reservation.start_date) }} -
                    {{ dateFormat(reservation.end_date) }} | {{ reservation.guests }} guest{{
                      reservation.guests > 1 ? "s" : ""
                    }}
                  </p>

                  <p>
                    Renter:
                    <router-link :to="'/public-profile/' + reservation.userId">{{
                      reservation.username
                    }}</router-link>
                  </p>
                </div>
                <div class="res-info-btn">
                  <button
                    class="btn btn-rating"
                    v-if="!reservation.is_renter_rated"
                    @click="showRenterRatingModal(reservation)"
                  >
                    <span class="link"> Rate Renter </span>
                  </button>

                  <button class="btn btn-details">
                    <router-link
                      class="link"
                      :to="{ name: 'singleroom', params: { roomId: reservation.roomDetails.id } }"
                    >
                      Details
                    </router-link>
                  </button>
                </div>
              </div>
            </div>
          </CCarouselItem>
        </CCarousel>
      </div>
      <div v-else>
        <h2>You don't have any past reservations for your rooms.</h2>
      </div>
    </div>

    <div class="rooms">
      <div v-if="rooms.length">
        <h2>Your Rooms</h2>
        <CCarousel :key="carouselKey" controls dark :interval="false" v-if="rooms.length > 0">
          <CCarouselItem v-for="(room, index) in rooms" :key="index">
            <div class="carousel-element">
              <h3>{{ room.room_name }}</h3>
              <CCarousel class="inner-carousel">
                <CCarouselItem v-for="picture in room.pictures" :key="picture.id">
                  <img :src="picture.image" alt="Room picture" />
                </CCarouselItem>
              </CCarousel>
              <div class="res-info">
                <div class="res-info-btn">
                  <button class="btn btn-modify">
                    <router-link
                      class="link"
                      :to="{ name: 'modifyroom', params: { roomId: room.id } }"
                      >Modify</router-link
                    >
                  </button>
                  <button
                    class="btn btn-pending"
                    v-if="room.reservation.filter((res) => res.status === 'pending').length > 0"
                  >
                    <router-link
                      class="link"
                      :to="{ name: 'confirm-book', params: { roomId: room.id } }"
                      >Pending</router-link
                    >
                  </button>
                  <button class="btn btn-delete" @click="deleteRoom(room.id)">
                    <span class="link"> Delete </span>
                  </button>
                </div>
              </div>
            </div>
          </CCarouselItem>
        </CCarousel>
      </div>
      <div v-else>
        <h2>You don't have any rooms yet.</h2>
      </div>
    </div>

    <div class="favorite">
      <h2>Favorites</h2>
      <div v-if="isLoadingFavorites">
        <p>Loading favorites...</p>
      </div>
      <div v-if="favorites.length > 0">
        <CCarousel :key="carouselKey" controls dark :interval="false">
          <CCarouselItem v-for="favorite in favorites" :key="favorite.id">
            <div class="carousel-element">
              <div class="fav-title">
                <div></div>
                <h3>{{ favorite.roomDetails.room_name }}</h3>
                <i
                  class="fa-solid fa-heart"
                  @click="removeFavorite(favorite.id)"
                  alt="Remove from favorites"
                ></i>
              </div>
              <CCarousel class="inner-carousel">
                <CCarouselItem v-for="picture in favorite.roomDetails.pictures" :key="picture.id">
                  <img :src="picture.image" alt="Room picture" />
                </CCarouselItem>
              </CCarousel>
            </div>
          </CCarouselItem>
        </CCarousel>
      </div>
      <div v-else>
        <h2>You have no favorites.</h2>
      </div>
    </div>

    <ReviewModal
      v-if="showReview"
      :reservation="selectedReservation"
      @close="closeReviewModal"
      @submit="submitReview"
    />
    <RatingModal
      v-if="showRating"
      :reservation="selectedReservation"
      @close="closeRatingModal"
      @submit="submitRating"
    />
    <RateRenterModal
      v-if="showRenterRating"
      :isVisible="showRenterRating"
      :renterId="selectedReservation.userId"
      :reservationId="selectedReservation.id"
      @close-modal="closeRenterRatingModal"
      @rating-submitted="markReservationAsRenterRated"
    />
  </div>
</template>

<script>
import authService from "../services/authService"
import roomService from "../services/roomService"
import { CCarousel, CCarouselItem } from "@coreui/vue"
import ReviewModal from "./ReviewModal.vue"
import RatingModal from "./RatingModal.vue"
import RateRenterModal from "./RateRenterModal.vue"

export default {
  components: {
    CCarousel,
    CCarouselItem,
    ReviewModal,
    RatingModal,
    RateRenterModal
  },
  data() {
    return {
      first_name: "",
      last_name: "",
      username: "",
      email: "",
      confirmed: false,
      alreadyConfirmed: false,
      id: "",
      rooms: [],
      favorites: [],
      isLoadingFavorites: false,
      carouselKey: 0,
      currentReservations: [],
      pastReservations: [],
      pastReservationsForOwnedRooms: [],
      showReview: false,
      showRating: false,
      selectedReservation: null,
      showRenterRating: false,
      ownerId: "",
      userId: ""
    }
  },
  computed: {
    filteredPastReservations() {
      const filtered = this.pastReservationsForOwnedRooms.filter(
        (reservation) => !reservation.is_renter_rated && reservation.ownerId === this.id
      )
      return filtered
    }
  },
  created() {
    this.fetchUserData()
    this.loadFavorites()
  },
  methods: {
    editProfile() {
      this.$router.push({ name: "profile-edit" })
    },
    deleteRoom(roomId) {
      roomService
        .deleteRoom(roomId)
        .then(() => {
          const roomIndex = this.rooms.findIndex((room) => room.id === roomId)
          if (roomIndex !== -1) {
            this.rooms.splice(roomIndex, 1)
            this.carouselKey++
          }
        })
        .catch((error) => {
          console.error("Error deleting room:", error)
        })
    },
    fetchUserData() {
      authService
        .getUser()
        .then((response) => {
          this.first_name = response.first_name
          this.last_name = response.last_name
          this.username = response.username
          this.email = response.email
          this.id = response.pk
          return roomService.fetchRoomByOwner(response.pk)
        })
        .then((response) => {
          if (Array.isArray(response)) {
            this.rooms = response
            return this.fetchReservations()
          } else {
            console.error("Unexpected response from fetchRoomsByOwner:", response)
          }
        })
        .catch(() => {
          this.$router.push({ name: "login" })
        })
    },
    showRenterRatingModal(reservation) {
      this.selectedReservation = reservation
      this.showRenterRating = true
    },
    closeRenterRatingModal() {
      this.selectedReservation = null
      this.showRenterRating = false
    },
    markReservationAsRenterRated() {
      this.selectedReservation.is_renter_rated = true
      roomService
        .markReservationAsRenterRated(this.selectedReservation.id)
        .then(() => {
          this.closeRenterRatingModal()
          this.fetchReservations()
        })
        .catch((error) => {
          console.error("Error marking reservation as renter rated:", error)
        })
    },
    async fetchReservations() {
      try {
        const currentReservations = await roomService.fetchCurrentReservations()
        const currentReservationsWithDetails = await Promise.all(
          currentReservations.map(async (reservation) => {
            const roomDetails = await roomService.fetchRoomById(reservation.room)
            reservation.roomDetails = roomDetails
            reservation.ownerId = roomDetails.owner
            return reservation
          })
        )
        this.currentReservations = currentReservationsWithDetails.filter(
          (reservation) => reservation.status === "pending" || reservation.status === "accepted"
        )

        const pastReservations = await roomService.fetchPastReservations()
        const pastReservationsWithDetails = await Promise.all(
          pastReservations.map(async (reservation) => {
            const roomDetails = await roomService.fetchRoomById(reservation.room)
            reservation.roomDetails = roomDetails
            reservation.ownerId = roomDetails.owner
            return reservation
          })
        )
        this.pastReservations = pastReservationsWithDetails.filter(
          (reservation) => reservation.status === "accepted"
        )

        const pastReservationsForOwnedRooms = await roomService.fetchPastReservationsByRoomOwner(
          this.id
        )
        const pastReservationsForOwnedRoomsWithDetails = await Promise.all(
          pastReservationsForOwnedRooms.map(async (reservation) => {
            const roomDetails = await roomService.fetchRoomById(reservation.room)
            reservation.roomDetails = roomDetails
            reservation.ownerId = roomDetails.owner
            return reservation
          })
        )
        this.pastReservationsForOwnedRooms = pastReservationsForOwnedRoomsWithDetails.filter(
          (reservation) => reservation.status === "accepted"
        )

        await Promise.all(
          this.pastReservationsForOwnedRooms.map(async (reservation) => {
            reservation.username = await this.getUsername(reservation.userId)
          })
        )
      } catch (error) {
        console.error("Error fetching reservations:", error)
      }
    },
    logout() {
      authService
        .logout()
        .then(() => {
          this.$router.push({ name: "login" })
        })
        .catch(() => {
          this.$router.push({ name: "login" })
        })
    },
    getUserId() {
      authService
        .getUser()
        .then((response) => {
          this.userId = response.pk
        })
        .catch((error) => {
          console.error("Error fetching user ID:", error)
        })
    },
    getUsername(userId) {
      try {
        const username = authService.getUsernameById(userId)
        return username
      } catch (error) {
        console.error("Error fetching username:", error)
      }
    },
    loadFavorites() {
      this.isLoadingFavorites = true
      roomService
        .getFavorites()
        .then((response) => {
          this.favorites = response
        })
        .catch((error) => {
          console.error("Error fetching favorites:", error)
        })
        .finally(() => {
          this.isLoadingFavorites = false
        })
    },
    removeFavorite(favoriteId) {
      if (!favoriteId) {
        console.error("Favorite ID is undefined")
        return
      }

      roomService
        .removeFavorite(favoriteId)
        .then(() => {
          this.carouselKey++
          this.favorites = this.favorites.filter(
            (fav) => fav.id.toString() !== favoriteId.toString()
          )
        })
        .catch((error) => {
          console.error("Error removing favorite:", error)
        })
    },
    dateFormat(date) {
      return new Date(date).toLocaleDateString()
    },
    checkConfirmationStatus() {
      const query = this.$route.query
      this.confirmed = query.confirmed === "true"
      this.alreadyConfirmed = query.already_confirmed === "true"
    },
    showReviewModal(reservation) {
      this.selectedReservation = reservation
      this.showReview = true
    },
    closeReviewModal() {
      this.selectedReservation = null
      this.showReview = false
    },
    submitReview(review) {
      if (!this.selectedReservation || !this.selectedReservation.room) {
        console.error("selectedReservation or room is undefined")
        return
      }

      const roomId = this.selectedReservation.room
      roomService
        .submitReview(roomId, review)
        .then(() => {
          return roomService.markReservationAsReviewed(this.selectedReservation.id)
        })
        .then(() => {
          this.selectedReservation.is_reviewed = true
          this.closeReviewModal()
        })
        .catch((error) => {
          console.error("Error submitting review:", error)
        })
    },
    showRatingModal(reservation) {
      this.selectedReservation = reservation
      this.showRating = true
    },
    closeRatingModal() {
      this.selectedReservation = null
      this.showRating = false
    },
    submitRating(rating) {
      if (!this.selectedReservation || !this.selectedReservation.room) {
        console.error("selectedReservation or room is undefined")
        return
      }

      const roomId = this.selectedReservation.room
      roomService
        .submitRating(roomId, rating)
        .then(() => {
          return roomService.markReservationAsRated(this.selectedReservation.id)
        })
        .then(() => {
          this.selectedReservation.is_rated = true
          this.closeRatingModal()
        })
        .catch((error) => {
          console.error("Error submitting rating:", error)
        })
    }
  },
  mounted() {
    this.checkConfirmationStatus()
    if (this.confirmed || this.alreadyConfirmed) {
      setTimeout(() => {
        this.confirmed = false
        this.alreadyConfirmed = false
        window.history.replaceState({}, document.title, "/#/profile")
      }, 2000)
    }
    this.fetchUserData()
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 2vh;
  padding: 20px;
  align-items: flex-start;
  background-color: #f9f9f9;
  border-radius: 10px;
}

.info {
  width: calc(50% - 20px);
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.info h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 20px;
}

.info p {
  font-size: 18px;
  color: #666;
  margin-bottom: 10px;
}

.info strong {
  color: #000;
}

.btn {
  margin: 10px 5px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  color: #fff;
  cursor: pointer;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.btn:hover {
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  transform: translateY(-3px);
}

.btn-logout {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
}

.btn-logout:hover {
  background: linear-gradient(20deg, rgb(255, 69, 0), red 20%, rgb(255, 140, 0), magenta);
}

.message-container {
  margin-bottom: 20px;
}

.confirmed-message {
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

.reservations,
.rooms {
  width: calc(50% - 20px);
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.reservations h2,
.rooms h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.status-pending {
  color: #ffc107;
  font-weight: bold;
  margin-bottom: 10px;
}

.status-accepted {
  color: #71dc2e;
  font-weight: bold;
  margin-bottom: 10px;
}

.carousel-element {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.carousel-element h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 10px;
}

.carousel-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  position: relative;
}

.inner-carousel {
  width: 100%;
  margin-bottom: 20px;
  position: relative;
}

.inner-carousel img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
}

.inner-carousel .carousel-item {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.inner-carousel .carousel-item img {
  width: 100%;
  max-width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
  transition: none !important;
}

.carousel-control-prev,
.carousel-control-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  color: #fff;
}

.carousel-control-prev {
  left: 10px;
}

.carousel-control-next {
  right: 10px;
}

.res-info {
  text-align: center;
}

.res-info p {
  font-size: 16px;
  color: #666;
  margin-bottom: 10px;
}

.res-info-btn {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.btn-details {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
}

.btn-details:hover {
  background: linear-gradient(20deg, rgb(238, 17, 37), red 20%, rgb(245, 106, 127), magenta);
}

.btn-review {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
}

.btn-review:hover {
  background: linear-gradient(20deg, rgb(255, 69, 0), red 20%, rgb(255, 140, 0), magenta);
}

.btn-rating {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
}

.btn-rating:hover {
  background: linear-gradient(20deg, rgb(238, 17, 37), red 20%, rgb(245, 106, 127), magenta);
}

.btn-modify {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
}

.btn-modify:hover {
  background: linear-gradient(20deg, rgb(255, 69, 0), red 20%, rgb(255, 140, 0), magenta);
}

.btn-pending {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
}

.btn-pending:hover {
  background: linear-gradient(20deg, rgb(238, 17, 37), red 20%, rgb(245, 106, 127), magenta);
}

.btn-delete {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
}

.btn-delete:hover {
  background: linear-gradient(20deg, rgb(255, 69, 0), red 20%, rgb(255, 140, 0), magenta);
}

.favorite {
  width: calc(50% - 20px);
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.favorite h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.fav-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 10px;
  padding: 0 30px;
}

.fav-title h3 {
  font-size: 20px;
  color: #333;
}

.fa-heart {
  color: #dc3545;
  cursor: pointer;
}

.fa-heart:hover {
  color: #c82333;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    padding: 10px;
  }

  .info,
  .reservations,
  .favorite,
  .rooms {
    width: 100%;
    margin-bottom: 20px;
  }

  .info,
  .reservations,
  .favorite,
  .rooms {
    padding: 10px;
  }

  .res-info {
    padding: 0;
  }
}

@media (max-width: 480px) {
  .info h2,
  .reservations h2,
  .favorite h2,
  .rooms h2 {
    font-size: 20px;
  }

  .info p,
  .reservations p,
  .favorite p,
  .rooms p {
    font-size: 14px;
  }

  .btn {
    font-size: 14px;
    padding: 8px 16px;
  }
}

@media screen and (max-width: 991px) {
  .inner-carousel img {
    height: 25vh;
  }
}
</style>
