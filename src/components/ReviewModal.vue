<template>
  <div class="modal-overlay">
    <div class="modal-container">
      <h2>Add Review</h2>
      <textarea
        v-model="review.comment"
        placeholder="Write your review"
        class="review-input"
      ></textarea>
      <div class="modal-actions">
        <button class="submit-button" @click="submitReview">Submit</button>
        <button class="cancel-button" @click="$emit('close')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["reservation"],
  data() {
    return {
      review: {
        comment: ""
      }
    }
  },
  methods: {
    submitReview() {
      this.$emit("submit", this.review)
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
.review-input {
  width: 100%;
  height: 100px;
  padding: 10px;
  margin-bottom: 20px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  resize: none;
}
.modal-actions {
  display: flex;
  justify-content: space-between;
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
</style>
