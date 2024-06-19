import api from "@/services/api"
import { ref } from "vue"

let user = ref()

export default {
  user,
  login(payload) {
    if (!payload.username || !payload.password) {
      return Promise.reject("Username and password are required.")
    }
    return api.post(`dj-rest-auth/login/`, payload).then((response) => {
      user.value = response.data.user
      localStorage.setItem("user", JSON.stringify(response.data.user))
      return response.data.user
    })
  },
  logout() {
    return api.post(`dj-rest-auth/logout/`).then((response) => {
      user.value = undefined
      localStorage.removeItem("user")
      return response.data
    })
  },
  register(payload) {
    if (!payload.username) {
      return Promise.reject(new Error("Username is required."))
    }
    if (!payload.email) {
      return Promise.reject(new Error("Email is required."))
    }
    if (!payload.password1) {
      return Promise.reject(new Error("Password is required."))
    }
    if (!payload.password2) {
      return Promise.reject(new Error("Password confirmation is required."))
    }
    if (payload.password1 !== payload.password2) {
      return Promise.reject(new Error("Passwords do not match."))
    }

    return api
      .post(`dj-rest-auth/registration/`, payload)
      .then((response) => {
        user.value = response.data.user
        return response.data.user
      })
      .catch((error) => {
        let errorMessage = "An error occurred."
        if (error.response.data) {
          errorMessage = Object.values(error.response.data).join(" ")
        }
        throw new Error(errorMessage)
      })
  },
  getUser() {
    if (!this.isLoggedIn()) {
      return Promise.resolve(null)
    } else {
      return api
        .get(`dj-rest-auth/user/`)
        .then((response) => {
          user.value = response.data
          return response.data
        })
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            console.warn("User is not authenticated")
          } else {
            console.error("Error fetching user details:", error)
          }
          return Promise.reject(error)
        })
    }
  },
  getUsernameById(userId) {
    return api.get(`/users/${userId}/`).then((response) => response.data.username)
  },
  isLoggedIn() {
    return !!user.value
  },
  save() {
    const userData = {
      username: user.value.username,
      email: user.value.email,
      groups: user.value.groups,
      first_name: user.value.first_name,
      last_name: user.value.last_name
    }

    return api
      .put(`users/${user.value.pk}/`, userData)
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        if (error.response.status === 400) {
          return Promise.reject("Invalid data. Please check your input.")
        } else if (error.response.status === 401) {
          return Promise.reject("Unauthorized. Please login again.")
        } else {
          return Promise.reject("An error occurred while saving your information.")
        }
      })
  },
  confirmEmail(payload) {
    return api
      .post(`api/account-confirm-email/${payload.key}/`, payload)
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        let errorMessage = "An error occurred."
        if (error.response.data) {
          errorMessage = Object.values(error.response.data).join(" ")
        }
        throw new Error(errorMessage)
      })
  },
  changePassword(payload) {
    return api
      .post(`dj-rest-auth/password/change/`, payload)
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        let errorMessage = "An error occurred while changing password."
        if (error.response && error.response.data) {
          errorMessage = Object.values(error.response.data).join(" ")
        }
        throw new Error(errorMessage)
      })
  },
  forgetPassword(payload) {
    return api
      .post(`dj-rest-auth/password/reset/`, payload)
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        let errorMessage = "An error occurred while sending the reset password email."
        if (error.response && error.response.data) {
          errorMessage = Object.values(error.response.data).join(" ")
        }
        throw new Error(errorMessage)
      })
  },
  resetPasswordConfirm() {
    let url = new URL(window.location.href)
    let pathParts = url.pathname.split("/")
    let uid = pathParts[pathParts.length - 3]
    let token = pathParts[pathParts.length - 2]
    let newPassword = url.searchParams.get("newPassword")

    let payload = {
      new_password1: newPassword,
      new_password2: newPassword,
      uid: uid,
      token: token
    }

    return api
      .post(`dj-rest-auth/password/reset/confirm/`, payload)
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        let errorMessage = "An error occurred while resetting the password."
        if (error.response && error.response.data) {
          errorMessage = Object.values(error.response.data).join(" ")
        }
        throw new Error(errorMessage)
      })
  },
  getCurrentUserId() {
    return this.getUser().then((user) => (user ? user.pk : null))
  }
}
