<template>
  <div></div>
</template>

<script>
import ratingService from "@/services/ratingService"

export default {
  props: ["roomId"],
  data() {
    return {
      ratings: []
    }
  },
  methods: {
    fetchRatings() {
      ratingService
        .fetchRatings()
        .then((response) => {
          this.ratings = response.results.filter((rating) => rating.room === this.roomId)
          this.emitAverageRating()
        })
        .catch((error) => {
          console.error("Error fetching ratings:", error)
        })
    },
    emitAverageRating() {
      if (this.ratings.length > 0) {
        const total = this.ratings.reduce((sum, rating) => sum + rating.score, 0)
        const average = total / this.ratings.length
        this.$emit("average-rating", average)
      } else {
        this.$emit("average-rating", 0)
      }
    }
  },
  created() {
    this.fetchRatings()
  },
  watch: {
    roomId: {
      handler() {
        this.fetchRatings()
      },
      immediate: true
    }
  }
}
</script>
