import api from "@/services/api"

export default {
  async getRecentNotifications() {
    return api.get("/notifications/recent")
  }
}
