import api from "@/services/api"
import authService from "@/services/authService"

export default {
  async fetchRooms() {
    let allRooms = [];
    let nextUrl = 'rooms/';
  
    while (nextUrl) {
      try {
        const response = await api.get(nextUrl);
        const data = response.data;
        allRooms = allRooms.concat(data.results);
        nextUrl = data.next ? data.next.replace('http://127.0.0.1:8000/api/', '') : null;
      } catch (error) {
        console.error("Error fetching rooms:", error);
        break;
      }
    }
  
    return allRooms;
  },
  fetchRoomById(roomId) {
    return api.get(`rooms/${roomId}/`).then((response) => response.data)
  },
  async createRoom(roomDetails) {
    try {
      const userId = await authService.getCurrentUserId()
      if (!userId) {
        throw new Error("User is not logged in.")
      }

      const payload = {
        owner: userId,
        room_name: roomDetails.room_name,
        description: roomDetails.description,
        price: roomDetails.price,
        pets_allowed: roomDetails.pets_allowed,
        smoking_allowed: roomDetails.smoking_allowed,
        has_elevator: roomDetails.has_elevator
      }

      const response = await api.post("rooms/", payload)
      return response.data
    } catch (error) {
      console.error("Error creating room:", error)
      throw error
    }
  },
  updateRoom(roomId, payload) {
    return api.put(`rooms/${roomId}/`, payload).then((response) => response.data)
  },
  deleteRoom(roomId) {
    return api.delete(`rooms/${roomId}/`).then((response) => response.data)
  },
  async createRoomFolder(folderPath) {
    try {
      const response = await api.post("folders/", { path: folderPath })
      return response.data
    } catch (error) {
      console.error("Error creating folder:", error)
      throw error
    }
  },
  async uploadPictures(roomId, formData) {
    try {
      formData.append("room", roomId)
      const response = await api.post("pictures/", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
      return response.data
    } catch (error) {
      console.error("Error uploading pictures:", error)
      throw error
    }
  },
  createAddress(addressData) {
    return api.post(`address/`, addressData).then((response) => response.data)
  },
  updateAddress(addressId, addressData) {
    return api.put(`address/${addressId}/`, addressData).then((response) => response.data)
  },
  fetchRoomByOwner(ownerId) {
    return api.get(`/rooms/ownerid/${ownerId}`).then((response) => response.data)
  },
  createReservation(reservationData) {
    return api.post(`reservations/`, reservationData).then((response) => response.data)
  },
  deleteReservation(reservationId) {
    return api.delete(`reservations/${reservationId}/`).then((response) => response.data)
  },
  fetchReservationByUser(userId) {
    return api.get(`reservations/userid/${userId}/`).then((response) => response.data)
  },
  fetchReservationById(reservationId) {
    return api.get(`reservations/${reservationId}/`).then((response) => response.data)
  },
  updateReservation(reservationId, payload) {
    return api.put(`reservations/${reservationId}/`, payload).then((response) => response.data)
  },
  addFavorite(roomId) {
    return api
      .post(`favorites/`, { roomId })
      .then((response) => response.data)
      .catch((error) => {
        console.error("Error adding favorite:", error)
        throw error
      })
  },
  async removeFavorite(favoriteId) {
    if (!favoriteId) {
      console.error("Favorite ID is undefined")
      return
    }

    const favorites = await this.getAllFavorites()
    const favorite = favorites.find((fav) => fav.id === favoriteId)

    if (favorite) {
      return api
        .delete(`favorites/${favoriteId}/`)
        .then((response) => response.data)
        .catch((error) => {
          console.error("Error removing favorite:", error)
          throw error
        })
    }
  },
  async getAllFavorites() {
    let favorites = []
    let url = `favorites/`

    while (url) {
      const response = await api.get(url)
      const data = response.data
      favorites = favorites.concat(data.results)
      url = data.next
    }

    return favorites
  },
  getFavorites() {
    return authService.getUser().then((currentUser) => {
      return this.getAllFavorites()
        .then((favorites) => {
          favorites = favorites.filter((favorite) => favorite.user === currentUser.pk)
          return this.fetchRooms().then((rooms) => {
            if (rooms && Array.isArray(rooms.results)) {
              rooms = rooms.results
            } else {
              rooms = []
            }
            const detailedFavorites = favorites.map((favorite) => {
              const roomDetails = rooms.find((room) => room.id === favorite.room)
              return {
                ...favorite,
                roomDetails
              }
            })
            return detailedFavorites
          })
        })
        .catch((error) => {
          if (error.response && error.response.status === 500) {
            console.error("Server error when getting favorites:", error)
          } else {
            console.error("Error getting favorites:", error)
          }
          throw error
        })
    })
  },
  async addToFavorites(roomId) {
    const currentUser = await authService.getUser()
    const favorites = await this.getAllFavorites()
    const isFavorite = favorites.find(
      (favorite) => favorite.user === currentUser.pk && favorite.room === roomId
    )

    if (isFavorite) {
      return Promise.reject(new Error("Room already in favorites"))
    }

    return api
      .post(`favorites/`, { room: roomId, user: currentUser.pk })
      .then((response) => response.data)
      .catch((error) => {
        console.error("Error adding room to favorites:", error)
        throw error
      })
  },
  async isFavorite(roomId, userId) {
    try {
      const response = await api.get(`/favorites/`)
      return response.data.results.some(
        (favorite) => favorite.user === userId && favorite.room === roomId
      )
    } catch (error) {
      console.error("Error checking favorite status:", error)
      throw error
    }
  },
  fetchCurrentReservations() {
    return api.get(`reservations/current/`).then((response) => response.data)
  },
  fetchPastReservations() {
    return api.get(`reservations/past/`).then((response) => response.data)
  },
  submitReview(roomId, review) {
    return api.post("reviews/", { room: roomId, ...review }).then((response) => response.data)
  },
  submitRating(roomId, rating) {
    return api.post("ratings/", { room: roomId, ...rating }).then((response) => response.data)
  },
  markReservationAsReviewed(reservationId) {
    return api
      .post(`reservations/${reservationId}/mark_as_reviewed/`)
      .then((response) => response.data)
  },
  markReservationAsRated(reservationId) {
    return api
      .post(`reservations/${reservationId}/mark_as_rated/`)
      .then((response) => response.data)
  },
  fetchPastReservationsByOwner() {
    return api.get(`reservations/past_by_owner/`).then((response) => response.data)
  },
  markReservationAsRenterRated(reservationId) {
    return api
      .post(`reservations/${reservationId}/mark_as_renter_rated/`)
      .then((response) => response.data)
  },
  fetchPastReservationsByRoomOwner(ownerId) {
    return api.get(`reservations/past_by_owner/${ownerId}`).then((response) => response.data)
  }
}
