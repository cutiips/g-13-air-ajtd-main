<template>
  <div>
    <h2>Reviews</h2>
    <div v-if="reviews.length === 0" class="review">
      <p>No reviews yet !</p>
    </div>
    <div v-else>
      <div v-for="review in reviews" :key="review.id" class="review">
        <p>{{ review.comment }}</p>
        <small v-if="review.reviewer">
          by
          <router-link :to="'/public-profile/' + review.reviewer_id">{{
            review.reviewer
          }}</router-link>
        </small>
        <small v-else>by Unknown User</small>
      </div>
    </div>
  </div>
</template>

<script>
import reviewService from "@/services/reviewService"

export default {
  props: ["roomId"],
  data() {
    return {
      reviews: [],
      allReviews: []
    }
  },
  methods: {
    fetchReviews() {
      reviewService
        .fetchReviews()
        .then((response) => {
          this.allReviews = response.results
          this.filterReviews()
        })
        .catch((error) => {
          console.error("Error fetching reviews:", error)
        })
    },
    filterReviews() {
      if (this.roomId && this.allReviews.length > 0) {
        this.reviews = this.allReviews.filter((review) => {
          return review.room.id === this.roomId
        })
      }
    }
  },
  watch: {
    roomId: {
      handler() {
        this.filterReviews()
      },
      immediate: true
    }
  },
  created() {
    this.fetchReviews()
  }
}
</script>

<style>
.review,
.no-review {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
}
</style>
