<template>
  <div class="profile-container">
    <h2>{{ renter.username }}'s Profile</h2>
    <p>Name: {{ renter.first_name }} {{ renter.last_name }}</p>
    <div class="rating-container">
      <p>Average Rating:</p>
      <div class="stars">
        <i v-for="star in fullStars" :key="star" class="fas fa-star"></i>
        <i v-if="halfStar" class="fas fa-star-half-alt"></i>
        <i v-for="star in emptyStars" :key="star" class="far fa-star"></i>
      </div>
    </div>
  </div>
</template>

<script>
import renterService from "@/services/renterService"

export default {
  props: {
    renterId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      renter: {},
      averageRating: null,
      fullStars: 0,
      halfStar: false,
      emptyStars: 0
    }
  },
  created() {
    this.fetchRenterProfile()
  },
  methods: {
    fetchRenterProfile() {
      renterService
        .fetchRenterProfile(this.renterId)
        .then((data) => {
          this.renter = data
          this.setStars(data.average_rating || 0)
        })
        .catch((error) => {
          console.error("Error fetching renter profile:", error)
        })
    },
    setStars(rating) {
      this.fullStars = Math.floor(rating)
      this.halfStar = rating % 1 !== 0
      this.emptyStars = 5 - this.fullStars - (this.halfStar ? 1 : 0)
    }
  }
}
</script>

<style scoped>
.profile-container {
  text-align: center;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 20px auto;
}

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

p {
  font-size: 18px;
  color: #555;
  margin: 5px 0;
}

.rating-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
}

.stars {
  display: flex;
  align-items: center;
  margin-left: 10px;
}

.stars i {
  font-size: 24px;
  color: #ffd700;
  margin-right: 5px;
}
</style>
