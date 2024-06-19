import { createRouter, createWebHashHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import LoginView from "../views/LoginView.vue"
import ProfileView from "../views/ProfileView.vue"
import authService from "../services/authService"
import RoomsView from "../views/RoomsView.vue"
import ForgetPasswordView from "../views/ForgetPasswordView.vue"
import NewPasswordView from "../views/NewPasswordView.vue"
import SingleRoomView from "../views/SingleRoomView.vue"
import RoomDetail from "../views/RoomDetail.vue"
import ReservationView from "../views/ReservationView.vue"
import ModifyRoomView from "../views/ModifyRoomView.vue"
import AddRoomView from "../views/AddRoomView.vue"
import RateRenterView from "../views/RateRenterView.vue"
import PublicProfileView from "../views/PublicProfileView.vue"
import ConfirmBookingView from "../views/ConfirmBookingView.vue"
import ProfileEditView from "../views/ProfileEditView.vue"

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView
  },
  {
    path: "/rooms",
    name: "rooms",
    component: RoomsView
  },
  {
    path: "/room/:roomId",
    name: "singleroom",
    component: SingleRoomView,
    props: true
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    beforeEnter: (to, from, next) => {
      if (authService.isLoggedIn()) {
        next({ name: "profile" })
      } else {
        next()
      }
    }
  },
  {
    path: "/profile",
    name: "profile",
    component: ProfileView,
    beforeEnter: (to, from, next) => {
      if (authService.isLoggedIn()) {
        next()
      } else {
        next({ name: "login" })
      }
    }
  },
  {
    path: "/forget-password",
    name: "forget-password",
    component: ForgetPasswordView
  },
  {
    path: "/new-password/:uid/:token",
    name: "new-password",
    component: NewPasswordView
  },
  {
    path: "/addroom",
    name: "addroom",
    beforeEnter: (to, from, next) => {
      if (authService.isLoggedIn()) {
        next()
      } else {
        next({ name: "login" })
      }
    },
    component: AddRoomView
  },
  {
    path: "/room/review/:roomId",
    name: "room-detail",
    component: RoomDetail
  },
  {
    path: "/reservation/:resId",
    name: "reservation",
    component: ReservationView,
    props: true
  },
  {
    path: "/modifyroom/:roomId",
    name: "modifyroom",
    component: ModifyRoomView,
    beforeEnter: (to, from, next) => {
      if (authService.isLoggedIn()) {
        next()
      } else {
        next({ name: "login" })
      }
    },
    props: true
  },
  {
    path: "/rate-renter/:renterId",
    name: "rate-renter",
    component: RateRenterView
  },
  {
    path: "/public-profile/:renterId",
    name: "public-profile",
    component: PublicProfileView
  },
  {
    path: "/confirm-book/:roomId",
    name: "confirm-book",
    component: ConfirmBookingView,
    beforeEnter: (to, from, next) => {
      if (authService.isLoggedIn()) {
        next()
      } else {
        next({ name: "login" })
      }
    }
  },
  {
    path: "/profile-edit",
    name: "profile-edit",
    component: ProfileEditView,
    beforeEnter: (to, from, next) => {
      if (authService.isLoggedIn()) {
        next()
      } else {
        next({ name: "login" })
      }
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
