import api from "@/services/api"

export default {
  fetchReviews(roomId) {
    return api
      .get("reviews/", {
        params: {
          room: roomId
        }
      })
      .then((response) => response.data)
  },
  fetchReviewById(reviewId) {
    return api.get(`reviews/${reviewId}/`).then((response) => response.data)
  },
  createReview(payload) {
    return api.post("reviews/", payload).then((response) => response.data)
  },
  updateReview(reviewId, payload) {
    return api.put(`reviews/${reviewId}/`, payload).then((response) => response.data)
  },
  deleteReview(reviewId) {
    return api.delete(`reviews/${reviewId}/`).then((response) => response.data)
  }
}
