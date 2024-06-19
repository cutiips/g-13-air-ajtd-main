<template>
  <div class="wrapper">
    <div class="card-switch">
      <label class="switch">
        <input type="checkbox" class="toggle" />
        <span class="slider"></span>
        <span class="card-side"></span>
        <div class="flip-card__inner">
          <div class="flip-card__front">
            <div class="title">Log in</div>
            <form class="flip-card__form" @submit.prevent="login">
              <input
                class="flip-card__input"
                v-model="username"
                name="username"
                placeholder="Username"
                type="text"
              />
              <input
                class="flip-card__input"
                v-model="password"
                name="password"
                placeholder="Password"
                type="password"
              />
              <div class="error-message">
                <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
              </div>
              <button class="flip-card__btn" type="submit">Log In</button>
            </form>
            <router-link to="forget-password">Forgot password?</router-link>
          </div>
          <div class="flip-card__back">
            <div class="title">Sign up</div>
            <form class="flip-card__form" @submit.prevent="register">
              <input
                v-model="username"
                class="flip-card__input"
                placeholder="Username"
                type="username"
              />
              <input v-model="email" class="flip-card__input" placeholder="Email" type="email" />

              <input
                v-model="password1"
                class="flip-card__input"
                name="password1"
                placeholder="Password"
                type="password"
              />
              <input
                v-model="password2"
                class="flip-card__input"
                name="password2"
                placeholder="Confirm Password"
                type="password"
              />
              <div class="error-message" v-if="signUpMessage">
                <p class="error">{{ signUpMessage }}</p>
              </div>
              <button class="flip-card__btn" type="submit">Sign Up</button>
            </form>
          </div>
        </div>
      </label>
    </div>
  </div>
</template>

<script>
import authService from "../services/authService"

export default {
  data() {
    return {
      username: "",
      password: "",
      email: "",
      password1: "",
      password2: "",
      errorMessage: "",
      signUpMessage: ""
    }
  },
  methods: {
    login() {
      if (!this.username || !this.password) {
        this.errorMessage = "Please fill in all fields"
        return
      }
      authService
        .login({ username: this.username, password: this.password })
        .then(() => {
          this.$router.push({ name: "profile" })
        })
        .catch(() => {
          this.errorMessage = "Invalid username or password"
        })
    },
    register() {
      authService
        .register({
          username: this.username,
          password1: this.password1,
          password2: this.password2,
          email: this.email
        })
        .then(() => {
          this.$router.push({ name: "profile" })
        })
        .catch((error) => {
          this.signUpMessage = error.message
        })
    }
  }
}
</script>

<style scoped>
*,
*:before,
*:after {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.error-message {
  color: red;
  font-weight: 600;
  border: none;
  background-color: transparent;
}
.wrapper {
  --input-focus: black;
  --font-color: #323232;
  --font-color-sub: #666;
  --bg-color: #fff;
  --bg-color-alt: #666;
  --main-color: #323232;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 150px);
}
.switch {
  transform: translateY(-200px);
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 30px;
  width: 50px;
  height: 20px;
}

.card-side::before {
  position: absolute;
  content: "Log in";
  left: -70px;
  top: 0;
  width: 100px;
  text-decoration: underline;
  color: var(--font-color);
  font-weight: 600;
}

.card-side::after {
  position: absolute;
  content: "Sign up";
  left: 70px;
  top: 0;
  width: 100px;
  text-decoration: none;
  color: var(--font-color);
  font-weight: 600;
}

.toggle {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  box-sizing: border-box;
  border-radius: 5px;
  border: 2px solid var(--main-color);
  box-shadow: 4px 4px var(--main-color);
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--bg-colorcolor);
  transition: 0.3s;
}

.slider:before {
  box-sizing: border-box;
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  border: 2px solid var(--main-color);
  border-radius: 5px;
  left: -2px;
  bottom: 2px;
  background-color: var(--bg-color);
  box-shadow: 0 3px 0 var(--main-color);
  transition: 0.3s;
}

.toggle:checked + .slider {
  background-color: var(--input-focus);
}

.toggle:checked + .slider:before {
  transform: translateX(30px);
}

.toggle:checked ~ .card-side:before {
  text-decoration: none;
}

.toggle:checked ~ .card-side:after {
  text-decoration: underline;
}
.flip-card__inner {
  width: 300px;
  height: 350px;
  position: relative;
  background-color: transparent;
  perspective: 1000px;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
}

.toggle:checked ~ .flip-card__inner {
  transform: rotateY(180deg);
}

.toggle:checked ~ .flip-card__front {
  box-shadow: none;
}

.flip-card__front,
.flip-card__back {
  padding: 20px;
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  background: #ffffff;
  gap: 20px;
  border-radius: 5px;
  border: 2px solid var(--main-color);
  box-shadow: 4px 4px var(--main-color);
}

.flip-card__back {
  width: 100%;
  transform: rotateY(180deg);
}

.flip-card__form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.title {
  margin: 20px 0 20px 0;
  font-size: 25px;
  font-weight: 900;
  text-align: center;
  color: var(--main-color);
}

.flip-card__input {
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
  outline: none;
}

.flip-card__input::placeholder {
  color: var(--font-color-sub);
  opacity: 0.8;
}

.flip-card__input:focus {
  border: 2px solid var(--input-focus);
}

.flip-card__btn:active,
.button-confirm:active {
  box-shadow: 0px 0px var(--main-color);
  transform: translate(3px, 3px);
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
</style>
