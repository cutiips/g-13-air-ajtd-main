<template>
  <div class="info">
    <div v-if="ConfirmedMessage" class="message-container">
      <div class="confirmed-message">{{ ConfirmedMessage }}</div>
    </div>
    <div v-if="ErrorMessage" class="message-container">
      <div class="error-message">{{ ErrorMessage }}</div>
    </div>

    <h1>Reset Passwordd</h1>
    <input
      v-model="password1"
      class="flip-card__input"
      placeholder="New Password"
      type="password"
    />
    <input
      v-model="password2"
      class="flip-card__input"
      placeholder="Confirm New Password"
      type="password"
    />
    <button @click="resetPassword" class="flip-card__btn" type="button">Reset</button>
  </div>
</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      uid: null,
      token: null,
      password1: "",
      password2: "",
      ConfirmedMessage: "",
      ErrorMessage: ""
    }
  },
  methods: {
    resetPassword() {
      const payload = {
        uid: this.uid,
        token: this.token,
        new_password1: this.password1,
        new_password2: this.password2
      }
      axios
        .post("/api/dj-rest-auth/password/reset/confirm/", payload)
        .then(() => {
          this.ConfirmedMessage = "Password has been reset successfully."
          setTimeout(() => {
            this.ConfirmedMessage = ""
            this.$router.push({ name: "login" })
          }, 2000)
        })
        .catch((error) => {
          if (error.response) {
            this.ErrorMessage = `The link is expired or invalid. Please request a new link.`
          } else {
            this.ErrorMessage = error.message
          }
          setTimeout(() => {
            this.ErrorMessage = ""
          }, 2000)
        })
    }
  },
  created() {
    this.uid = this.$route.params.uid
    this.token = this.$route.params.token
  }
}
</script>

<style scoped>
.info {
  --input-focus: black;
  --font-color: #323232;
  --font-color-sub: #666;
  --bg-color: #fff;
  --bg-color-alt: #666;
  --main-color: #323232;
  width: 300px;
  margin: 0 auto;
  padding: 30px 20px;
  background-color: var(--bg-color);
  border-radius: 10px;
  border: 2px solid var(--main-color);
  box-shadow: 4px 4px var(--main-color);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.info h1 {
  font-size: 28px;
  color: var(--font-color);
  margin-bottom: 20px;
  font-weight: 900;
}

.info input {
  width: 250px;
  height: 40px;
  border-radius: 5px;
  border: 2px solid var(--main-color);
  background-color: var(--bg-color);
  box-shadow: 4px 4px var(--main-color);
  font-size: 15px;
  font-weight: 600;
  color: var(--font-color);
  padding: 5px 10px;
  margin-bottom: 20px;
  outline: none;
}

.info input::placeholder {
  color: var(--font-color-sub);
  opacity: 0.8;
}

.info input:focus {
  border: 2px solid var(--input-focus);
}

.message-container {
  margin-bottom: 20px;
  animation: slideDown 0.5s ease-out;
}

.confirmed-message,
.error-message {
  padding: 15px;
  border-radius: 5px;
  text-align: center;
  font-weight: bold;
  color: #fff;
}

.confirmed-message {
  background-color: #28a745;
}

.error-message {
  background-color: #dc3545;
}

@keyframes slideDown {
  0% {
    transform: translateY(-10px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.flip-card__btn {
  margin: 20px 0;
  width: 120px;
  height: 40px;
  border-radius: 5px;
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  border: 2px solid var(--main-color);
  box-shadow: 4px 4px var(--main-color);
  font-size: 17px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.flip-card__btn:hover {
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  transform: translateY(-3px);
}
</style>
