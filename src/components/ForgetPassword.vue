<template>
  <div v-if="message" class="message-container">
    <p class="confirmed-message">{{ message }}</p>
  </div>
  <div class="info">
    <h1>Forgot password</h1>
    <form @submit.prevent="forgetPassword">
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" />
      </div>
      <button class="flip-card__btn" type="submit">Send Reset</button>
    </form>
  </div>
</template>
<script>
import authService from "../services/authService"
export default {
  data() {
    return {
      message: "",
      email: ""
    }
  },
  methods: {
    forgetPassword() {
      authService
        .forgetPassword({ email: this.email })
        .then(() => {
          this.message = "Reset link has been sent to your email."
          setTimeout(() => {
            this.message = ""
          }, 2000)
        })
        .catch((error) => {
          this.message = error.message
          setTimeout(() => {
            this.message = ""
          }, 3000)
        })
    }
  }
}
</script>
<style scoped>
.info label {
  display: block;
  font-size: 18px;
  color: var(--font-color-sub);
  margin-bottom: 10px;
}
.info input {
  display: block;
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 5px;
  border: 2px solid var(--main-color);
  background-color: var(--bg-color);
  box-shadow: 4px 4px var(--main-color);
  font-size: 15px;
  font-weight: 600;
  color: var(--font-color);
  outline: none;
}
.message-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 10vh;
  position: absolute;
  top: 0;
  left: calc(50% - 150px);
  color: red;
}
.confirmed-message {
  top: 50px;
  width: 300px;
  color: #ffffff;
  background-color: rgb(134, 223, 39);
  border: 1px solid rgb(0, 0, 0);
  padding: 20px;
  text-align: center;
  z-index: 1000;
  border-radius: 10px;
  animation:
    slideDown 0.5s,
    sandClock 5s infinite;
}
@keyframes slideDown {
  0% {
    transform: translateY(-100%);
  }
  100% {
    transform: translateY(0);
  }
}
@keyframes sandClock {
  100% {
    background-color: rgb(134, 223, 39);
  }
}
.info {
  --input-focus: #85144b;
  --font-color: #000000;
  --bg-color: #fff;
  --bg-color-alt: #666;
  --main-color: #323232;
  width: 300px;
  margin: 0 auto;
  background-color: var(--bg-color);
  padding: 20px;
  min-height: calc(100vh - 150px);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.info h1 {
  font-size: 24px;
  color: var(--font-color);
  margin-bottom: 20px;
}
.info p {
  font-size: 18px;
  color: var(--font-color-sub);
  margin-bottom: 10px;
}
.flip-card__btn {
  margin: 20px 0 20px 0;
  width: 120px;
  height: 40px;
  border-radius: 5px;
  border: 2px solid var(--main-color);
  background-color: var(--bg-color);
  box-shadow: 4px 4px var(--main-color);
  font-size: 17px;
  font-weight: 600;
  color: var(--font-color);
  cursor: pointer;
}
.flip-card__btn:hover {
  box-shadow: 0px 0px var(--main-color);
  transform: translate(3px, 3px);
}
</style>
