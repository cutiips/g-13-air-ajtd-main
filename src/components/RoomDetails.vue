<template>
  <div class="review-cont">
    <CCarousel
      controls
      dark
      class="carousel-single"
      v-if="room.pictures && room.pictures.length > 0"
    >
      <CCarouselItem v-for="(picture, idx) in room.pictures" :key="idx">
        <img :src="picture.image" alt="Room Picture" />
      </CCarouselItem>
    </CCarousel>
    <div class="review-info">
      <div>
        <h1>{{ room.room_name }}</h1>
        <p>Price: {{ room.price }} Frs./night</p>

        <ReviewList :roomId="room.id" ref="reviewList" />
        <RatingList :roomId="room.id" ref="ratingList" />
      </div>

      <form @submit.prevent="addReviewAndRating">
        <h2>Add a Review</h2>
        <textarea v-model="newReview.comment" placeholder="Write your review"></textarea>
        <h2>Add a Rating</h2>
        <StarRating v-model:rating="userRating" />
        <button type="submit">Submit Rating</button>
      </form>
    </div>
  </div>
</template>

<script>
import reviewService from "@/services/reviewService"
import ratingService from "@/services/ratingService"
import ReviewList from "@/components/ReviewList.vue"
import RatingList from "@/components/RatingList.vue"
import roomService from "@/services/roomService"
import StarRating from "@/components/StarRating.vue"
import { CCarousel, CCarouselItem } from "@coreui/vue"
import authService from "../services/authService"

export default {
  components: {
    ReviewList,
    RatingList,
    StarRating,
    CCarousel,
    CCarouselItem
  },
  data() {
    return {
      room: {},
      newReview: {
        comment: ""
      },
      userRating: 0
    }
  },
  methods: {
    fetchRoom() {
      const roomId = this.$route.params.roomId
      roomService.fetchRoomById(roomId).then((data) => {
        this.room = data
      })
    },
    addReviewAndRating() {
      const reviewPayload = {
        comment: this.newReview.comment,
        room: this.room.id,
        user: authService.user.value.pk
      }

      const ratingPayload = {
        score: this.userRating,
        room: this.room.id,
        user: authService.user.value.pk
      }

      const addReview = reviewService.createReview(reviewPayload)
      const addRating = ratingService.createRating(ratingPayload)

      Promise.all([addReview, addRating])
        .then(() => {
          this.newReview.comment = ""
          this.userRating = 0
          this.$refs.reviewList.fetchReviews()
          this.$refs.ratingList.fetchRatings()
        })
        .catch((error) => {
          console.error("Error adding review and rating:", error)
        })
    }
  },
  created() {
    this.fetchRoom()
  }
}
</script>
<style scoped>
.review-cont {
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 150px);
  max-width: 1200px;
  margin: 0 auto;
}

.review-info {
  max-width: 1200px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 0 2vw;
}

.carousel-single {
  margin: 2vh auto;
}
</style>
