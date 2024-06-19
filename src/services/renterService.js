import api from "@/services/api"

export default {
  createRenterRating(payload) {
    return api.post(`renter-ratings/`, payload).then((response) => response.data)
  },
  fetchRenterRatings(renterId) {
    return api.get(`renter-ratings/?renter=${renterId}`).then((response) => response.data)
  },
  fetchRenterProfile(renterId) {
    return api.get(`public-profile/${renterId}/`).then((response) => response.data)
  }
}
