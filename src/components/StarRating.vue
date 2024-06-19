<template>
  <div class="star-rating">
    <i
      v-for="star in stars"
      :key="star"
      class="fa-star star"
      :class="{
        fas: star <= (hoverRating || currentRating),
        far: star > (hoverRating || currentRating)
      }"
      @click="setRating(star)"
      @mouseover="hoverRating = star"
      @mouseleave="hoverRating = 0"
    ></i>
  </div>
</template>

<script>
export default {
  name: "StarRating",
  props: {
    rating: {
      type: Number,
      default: 0
    },
    maxStars: {
      type: Number,
      default: 5
    }
  },
  data() {
    return {
      currentRating: this.rating,
      hoverRating: 0
    }
  },
  computed: {
    stars() {
      return Array.from({ length: this.maxStars }, (_, i) => i + 1)
    }
  },
  methods: {
    setRating(star) {
      this.currentRating = star
      this.$emit("update:rating", this.currentRating)
    }
  }
}
</script>

<style scoped>
.star-rating {
  display: flex;
  flex-wrap: nowrap;
}

.star {
  font-size: 1.3rem;
  cursor: pointer;
  transition: color 0.2s;
}
</style>
