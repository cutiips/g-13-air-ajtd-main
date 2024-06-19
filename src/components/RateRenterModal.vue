<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-container">
      <h2>Rate Renter</h2>
      <StarRating v-model:rating="score" />
      <form @submit.prevent="submitRating">
        <label for="comment">Comment:</label>
        <textarea v-model="comment" rows="4" placeholder="Leave a comment..."></textarea>
        <div class="modal-actions">
          <button type="submit" class="submit-button">Submit</button>
          <button type="button" class="cancel-button" @click="closeModal">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import StarRating from "@/components/StarRating.vue"
import renterService from "@/services/renterService"

export default {
  components: {
    StarRating
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    renterId: {
      type: Number,
      required: true
    },
    reservationId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      score: 0,
      comment: ""
    }
  },
  methods: {
    closeModal() {
      this.$emit("close-modal")
    },
    submitRating() {
      const payload = {
        renter: this.renterId,
        score: this.score,
        comment: this.comment,
        reservation: this.reservationId
      }
      renterService
        .createRenterRating(payload)
        .then(() => {
          this.$emit("rating-submitted")
          this.closeModal()
        })
        .catch((error) => {
          console.error("Error submitting rating:", error)
        })
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  padding: 30px;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.modal-container h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.submit-button,
.cancel-button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button {
  background-color: #28a745;
  color: white;
}

.submit-button:hover {
  background-color: #218838;
}

.cancel-button {
  background-color: #dc3545;
  color: white;
}

.cancel-button:hover {
  background-color: #c82333;
}

textarea {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
}
</style>
