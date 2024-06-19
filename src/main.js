import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"
import "@fortawesome/fontawesome-free/css/all.min.css"

import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"

import authService from "@/services/authService"

const app = createApp(App)
const storedUser = localStorage.getItem("user")
if (storedUser) {
  authService.user.value = JSON.parse(storedUser)
}
app.use(router)
app.mount("#app")
