import api from "@/services/api"

export default {
  fetchRatings() {
    return api.get("ratings/").then((response) => response.data)
  },
  fetchRatingById(ratingId) {
    return api.get(`ratings/${ratingId}/`).then((response) => response.data)
  },
  createRating(payload) {
    return api.post("ratings/", payload).then((response) => response.data)
  },
  updateRating(ratingId, payload) {
    return api.put(`ratings/${ratingId}/`, payload).then((response) => response.data)
  },
  deleteRating(ratingId) {
    return api.delete(`ratings/${ratingId}/`).then((response) => response.data)
  }
}
