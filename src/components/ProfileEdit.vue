<template>
  <div class="container">
    <div class="info">
      <h1>Profile</h1>
      <div>
        <label>
          Username:
          <input v-model="user.username" placeholder="Enter your username" />
        </label>
        <label>
          Email:
          <input v-model="user.email" readonly placeholder="Your email address" />
        </label>
        <label>
          First Name:
          <input v-model="user.first_name" placeholder="Enter your first name" />
        </label>
        <label>
          Last Name:
          <input v-model="user.last_name" placeholder="Enter your last name" />
        </label>
        <div class="btn-group">
          <button class="form-btn" @click="save">Save</button>
          <button class="form-btn cancel-btn" @click="cancel">Cancel</button>
        </div>
      </div>
    </div>
    <div class="password">
      <div v-if="message" class="alert" :class="messageClass" role="alert">{{ message }}</div>

      <h1>Password</h1>
      <form @submit.prevent="changePassword">
        <div>
          <label for="newPassword">
            New Password:
            <input
              type="password"
              id="newPassword"
              v-model="newPassword"
              required
              placeholder="Enter new password"
            />
          </label>
        </div>
        <div>
          <label for="confirmPassword">
            Confirm New Password:
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              required
              placeholder="Confirm new password"
            />
          </label>
        </div>
        <div class="btn-group">
          <button class="form-btn" type="submit">Change</button>
          <button class="form-btn cancel-btn" @click="cancel">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import authService from "../services/authService"

export default {
  data() {
    return {
      user: authService.user.value,
      message: "",
      messageClass: "",
      oldPassword: "",
      newPassword: "",
      confirmPassword: ""
    }
  },
  async mounted() {
    await authService.getUser()
    this.user = authService.user.value
  },
  methods: {
    save() {
      if (!this.user.username) {
        this.showMessage("Please fill Username", "alert-danger")
        return
      }
      if (!this.user.email) {
        this.showMessage("Please fill Email", "alert-danger")
        return
      }
      authService
        .save(this.user)
        .then(() => {
          this.$router.push("/profile")
          this.showMessage("Changes saved successfully!", "alert-success")
        })
        .catch(() => {
          this.showMessage("An error occurred while saving changes", "alert-danger")
        })
    },
    changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.showMessage("Passwords do not match.", "alert-danger")
        return
      }

      authService
        .changePassword({
          new_password1: this.newPassword,
          new_password2: this.confirmPassword
        })
        .then(() => {
          this.showMessage("Password changed successfully!", "alert-success")
          setTimeout(() => {
            this.$router.push("/profile")
          }, 1000)
        })
        .catch((error) => {
          this.showMessage("Failed to change password. " + error.message, "alert-danger")
        })
    },
    showMessage(msg, type) {
      this.message = msg
      this.messageClass = type
      setTimeout(() => {
        this.message = ""
      }, 2000)
    },
    cancel() {
      this.$router.push("/profile")
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 2vh;
  padding: 20px;
  align-items: flex-start;
  background-color: #f9f9f9;
  border-radius: 10px;
}

.info {
  width: calc(50% - 20px);
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.info h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 20px;
}

.info label {
  width: 100%;
  font-size: 18px;
  color: #666;
  margin-bottom: 10px;
}

.info input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  margin-bottom: 20px;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 16px;
  color: #333;
}

.btn-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.form-btn {
  margin: 10px 5px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  color: #fff;
  cursor: pointer;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.form-btn:hover {
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  transform: translateY(-3px);
}

.cancel-btn {
  background: linear-gradient(20deg, rgb(255, 69, 0), red 20%, rgb(255, 140, 0), magenta);
}

.cancel-btn:hover {
  background: linear-gradient(20deg, rgb(238, 17, 37), red 20%, rgb(245, 106, 127), magenta);
}

.alert {
  width: 100%;
  text-align: center;
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 5px;
  transition: all 0.5s ease-in-out;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message-container {
  margin-bottom: 20px;
}

.confirmed-message {
  padding: 10px;
  color: #fff;
  background-color: #28a745;
  border-radius: 5px;
  text-align: center;
  animation: slideDown 0.5s ease-in-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.password {
  width: calc(50% - 20px);
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.password h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 20px;
}

.password label {
  width: 100%;
  font-size: 18px;
  color: #666;
  margin-bottom: 10px;
}

.password input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  margin-bottom: 20px;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 16px;
  color: #333;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    padding: 10px;
  }

  .info,
  .password {
    width: 100%;
    margin-bottom: 20px;
  }

  .info h1,
  .password h1 {
    font-size: 24px;
  }

  .info label,
  .password label {
    font-size: 16px;
  }

  .info input,
  .password input {
    font-size: 14px;
  }

  .form-btn {
    font-size: 14px;
    padding: 8px 16px;
  }
}

@media (max-width: 480px) {
  .info h1,
  .password h1 {
    font-size: 20px;
  }

  .info label,
  .password label {
    font-size: 14px;
  }

  .form-btn {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>
