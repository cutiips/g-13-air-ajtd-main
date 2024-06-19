<template>
  <div class="message-container">
    <div v-if="favoriteAddedMessage" class="confirmation-message" :class="favoriteAddedClass">
      {{ favoriteAddedMessage }}
    </div>
  </div>
  <div class="container">
    <h1 v-if="modifyRoomData">Modify Room</h1>
    <h1 v-else>Add Room</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label for="roomName">Room Name</label>
        <input type="text" id="roomName" v-model="roomData.room_name" required placeholder="Name" />
      </div>
      <div>
        <label for="description">Description</label>
        <textarea
          id="description"
          v-model="roomData.description"
          required
          placeholder="Description"
        ></textarea>
      </div>
      <div>
        <label for="price">Price</label>
        <input
          type="number"
          id="price"
          v-model="roomData.price"
          required
          step=".05"
          placeholder="Price"
          min="1"
          max="99999"
        />
      </div>
      <div class="form-check-cont">
        <div class="form-check">
          <input
            type="checkbox"
            class="form-check-input"
            id="petsAllowed"
            v-model="roomData.pets_allowed"
          />
          <label for="petsAllowed">Pets Allowed</label>
        </div>
        <div class="form-check">
          <input
            type="checkbox"
            class="form-check-input"
            id="smokingAllowed"
            v-model="roomData.smoking_allowed"
          />
          <label for="smokingAllowed">Smoking Allowed</label>
        </div>
        <div class="form-check">
          <input
            type="checkbox"
            class="form-check-input"
            id="hasElevator"
            v-model="roomData.has_elevator"
          />
          <label for="hasElevator">Has Elevator</label>
        </div>
      </div>
      <div>
        <label for="country">Country</label>
        <input
          type="text"
          id="country"
          v-model="addressData.country"
          required
          placeholder="Country"
        />
      </div>
      <div>
        <label for="city">City</label>
        <input type="text" id="city" v-model="addressData.city" required placeholder="City" />
      </div>
      <div>
        <label for="streetname">Address</label>
        <input
          type="text"
          id="streetname"
          v-model="addressData.streetname"
          required
          placeholder="Address"
        />
      </div>
      <div>
        <label for="postalCode">Postal Code</label>
        <input
          type="text"
          id="postalCode"
          v-model="addressData.postal_code"
          required
          placeholder="Postal code"
        />
      </div>
      <div>
        <label> Disabled Dates </label>
        <VueDatePicker
          class="datepicker"
          v-model="date"
          :clearable="true"
          :min-date="new Date()"
          :enable-time-picker="false"
          :multi-calendars="{ static: false }"
          no-today
          multi-dates
          placeholder="Dates ..."
        ></VueDatePicker>
      </div>
      <div>
        <label> Images </label>
        <div>
          <input
            class="invisible-input"
            type="file"
            ref="fileInput"
            multiple
            @change="handleFileInputChange"
            accept="image/png, image/jpeg, image/jpg"
          />
          <div @click="$refs.fileInput.click()" class="addimage">
            <i class="fa-solid fa-plus"></i>
          </div>
          <div v-if="pictures.length" class="image-preview-cont">
            <div v-for="(picture, index) in pictures" :key="index" class="image-preview">
              <img :src="picture.url" alt="Uploaded Image" />
              <i class="fa-solid fa-circle-xmark" @click="removeImage(index)"></i>
            </div>
          </div>
        </div>
      </div>
      <button type="submit" class="btn-addroom">Submit</button>
    </form>
  </div>
</template>

<script>
import roomService from "@/services/roomService"
import authService from "@/services/authService"
import VueDatePicker from "@vuepic/vue-datepicker"

export default {
  components: { VueDatePicker },
  name: "AddRoom",
  props: {
    modifyRoomData: {
      type: Object,
      required: false
    }
  },
  data() {
    return {
      roomData: {
        owner: "",
        room_name: "",
        description: "",
        price: "",
        pets_allowed: false,
        smoking_allowed: false,
        has_elevator: false
      },
      addressData: {
        country: "",
        city: "",
        streetname: "",
        postal_code: ""
      },
      pictures: [],
      favoriteAddedMessage: "",
      favoriteAddedClass: "",
      date: [],
      isInitialized: false
    }
  },
  computed: {
    isLoggedIn() {
      return authService.isLoggedIn()
    }
  },
  methods: {
    async submitForm() {
      if (this.modifyRoomData) {
        this.modifyRoom()
        return
      }
      if (!this.isLoggedIn) {
        this.favoriteAddedMessage = "You must be logged in to add a room."
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        this.$refs.fileInput.value = null
        return
      }
      if (!this.pictures.length) {
        this.favoriteAddedMessage = "You must add at least one picture."
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        this.$refs.fileInput.value = null
        return
      }
      if (
        !this.roomData.room_name ||
        !this.roomData.description ||
        !this.roomData.price ||
        !this.addressData.country ||
        !this.addressData.city ||
        !this.addressData.streetname ||
        !this.addressData.postal_code
      ) {
        this.favoriteAddedMessage = "All fields are required."
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        this.$refs.fileInput.value = null
        return
      }
      if (this.roomData.price < 1 || this.roomData.price > 99999) {
        this.favoriteAddedMessage = "Price must be between 1 and 99999."
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        this.$refs.fileInput.value = null
        return
      }
      try {
        const createdRoom = await roomService.createRoom(this.roomData)
        const roomId = createdRoom.id

        const addressData = { ...this.addressData, room: roomId }
        await roomService.createAddress(addressData)

        for (const picture of this.pictures) {
          const formData = new FormData()
          formData.append("image", picture.file)
          await roomService.uploadPictures(roomId, formData)
        }

        for (const date of this.date) {
          const payload = {
            user: null,
            room: roomId,
            start_date: new Date(date).toISOString().split("T")[0],
            end_date: new Date(date).toISOString().split("T")[0],
            guests: 1,
            status: "owner",
            "is_reviewed": false,
            "is_rated": false,
            "is_renter_rated": false
          }
          await roomService.createReservation(payload)
          console.log("date", date)
        }

        this.$router.push({ name: "singleroom", params: { roomId: roomId } })
      } catch (error) {
        console.error("Error creating room:", error)
        alert("An error occurred while creating the room. Please try again.")
      }
    },
    handleFileInputChange(event) {
      const files = event.target.files
      if (!files || !files.length) {
        this.favoriteAddedMessage = "Choose an image"
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        this.$refs.fileInput.value = null
        return
      }

      if (this.pictures.length + files.length > 10) {
        this.favoriteAddedMessage = "Images limited to 10"
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        this.$refs.fileInput.value = null
        return
      }

      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        const reader = new FileReader()
        const fileType = file.type
        if (fileType === "image/png" || fileType === "image/jpeg" || fileType === "image/jpg") {
          reader.onload = (e) => {
            this.pictures.push({ url: e.target.result, file })
          }
          reader.readAsDataURL(file)
        } else {
          this.favoriteAddedMessage = "Images must be in PNG, JPEG, or JPG format"
          this.favoriteAddedClass = "error-message"
          setTimeout(() => {
            this.favoriteAddedMessage = ""
          }, 3000)
          this.$refs.fileInput.value = null
          return
        }
      }

      this.$refs.fileInput.value = null
    },
    removeImage(index) {
      this.pictures.splice(index, 1)
    },
    async modifyRoom() {
      if (!this.isLoggedIn) {
        this.favoriteAddedMessage = "You must be logged in to add a room."
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        this.$refs.fileInput.value = null
        return
      }
      if (!this.pictures.length) {
        this.favoriteAddedMessage = "You must add at least one picture."
        this.favoriteAddedClass = "error-message"
        this.$refs.fileInput.value = null
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        return
      }
      if (
        !this.roomData.room_name ||
        !this.roomData.description ||
        !this.roomData.price ||
        !this.addressData.country ||
        !this.addressData.city ||
        !this.addressData.streetname ||
        !this.addressData.postal_code
      ) {
        this.favoriteAddedMessage = "All fields are required."
        this.favoriteAddedClass = "error-message"
        this.$refs.fileInput.value = null
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        return
      }
      if (this.roomData.price < 1 || this.roomData.price > 99999) {
        this.favoriteAddedMessage = "Price must be between 1 and 99999."
        this.favoriteAddedClass = "error-message"
        this.$refs.fileInput.value = null
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
        return
      }
      try {
        await roomService.updateRoom(this.modifyRoomData.id, {
          room_name: this.roomData.room_name,
          description: this.roomData.description,
          price: this.roomData.price,
          pets_allowed: this.roomData.pets_allowed,
          smoking_allowed: this.roomData.smoking_allowed,
          has_elevator: this.roomData.has_elevator,
          owner: this.roomData.owner
        })

        await roomService.updateAddress(this.modifyRoomData.address[0].id, {
          country: this.addressData.country,
          city: this.addressData.city,
          streetname: this.addressData.streetname,
          postal_code: this.addressData.postal_code
        })
        const removedPictures = this.modifyRoomData.pictures.filter(
          (picture) => !this.pictures.some((p) => p.file === picture)
        )
        for (const picture of removedPictures) {
          await roomService.deletePicture(picture.id)
        }
        for (const picture of this.pictures) {
          if (!picture.file.id) {
            const formData = new FormData()
            formData.append("image", picture.file)
            await roomService.uploadPictures(this.modifyRoomData.id, formData)
          }
        }
        const removedDates = this.modifyRoomData.reservation.filter(
          (reservation) =>
            reservation.start_date == reservation.end_date &&
            reservation.user == null &&
            reservation.status == "owner" &&
            !this.date.includes(reservation.start_date)
        )
        for (const date of removedDates) {
          await roomService.deleteReservation(date.id)
        }
        for (const date of this.date) {
          if (
            !this.modifyRoomData.reservation.some(
              (reservation) =>
                reservation.start_date == reservation.end_date &&
                reservation.user == null &&
                reservation.status == "owner" &&
                reservation.start_date == date
            )
          ) {
            await roomService.createReservation({
              start_date: new Date(date).toISOString().split("T")[0],
              end_date: new Date(date).toISOString().split("T")[0],
              status: "owner",
              room: this.modifyRoomData.id,
              user: null,
              is_rated: true,
              is_reviewed: true,
              is_renter_rated: true,
              guests: 1
            })
          }
        }
        this.$router.push({ name: "profile" })
      } catch (error) {
        this.favoriteAddedMessage = "An error occurred while modifying the room. Please try again."
        this.favoriteAddedClass = "error-message"
        setTimeout(() => {
          this.favoriteAddedMessage = ""
        }, 3000)
      }
    }
  },
  created() {
    if (this.isLoggedIn) {
      this.roomData.owner = authService.user.value.pk
    }
  },
  watch: {
    modifyRoomData: {
      deep: true,
      handler(newVal) {
        if (newVal && !this.isInitialized) {
          this.roomData = newVal
          this.addressData = newVal.address[0]
          for (const picture of newVal.pictures) {
            this.pictures.push({ url: picture.image, file: picture })
          }
          for (const reservation of newVal.reservation) {
            if (
              reservation.start_date == reservation.end_date &&
              reservation.user == null &&
              reservation.status == "owner"
            ) {
              this.date.push(new Date(reservation.start_date).toISOString().split("T")[0])
            }
          }
          this.isInitialized = true
        }
      }
    }
  }
}
</script>

<style scoped>
.datepicker {
  --dp-border-radius: 30px;
  --dp-border-color: #aaa;
  margin: 0;
}
.container {
  max-width: 700px;
  margin: auto;
  padding: 20px;
  min-height: calc(100vh - 150px);
}
form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  max-width: 1000px;
  min-width: 300px;
}
form div {
  display: flex;
  flex-direction: column;
  width: 100%;
}
form div input[type="text"],
form div input[type="number"],
form div textarea {
  width: 100%;
  max-width: 700px;
  min-width: 300px;
  padding: 5px 10px;
  border-radius: 30px;
  border: 1px solid #aaa;
}
form div textarea {
  padding: 10px;
  min-height: 46px;
  border-radius: 15px;
}
form label {
  font-weight: 600;
  margin-bottom: 5px;
  padding-left: 10px;
}
.form-check {
  display: block;
  width: 100%;
}
.form-check-cont {
  display: flex;
  flex-direction: column;
  width: auto;
  margin: auto;
}
.form-check-cont label {
  padding: 0;
  font-weight: normal;
}
.login-message {
  text-align: center;
  margin-top: 50px;
  /* Adjust as needed */
}
h1 {
  text-align: center;
}
.invisible-input {
  display: none;
}
.addimage {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 70px;
  height: 70px;
  border: 2px dashed #aaa;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1.7em;
  margin: auto;
}
.addimage:hover {
  background-color: #f4f4f4;
}
.image-preview-cont {
  display: flex;
  flex-direction: row;
  justify-content: center;
  flex-wrap: wrap;
  column-gap: 10px;
}
.image-preview {
  display: flex;
  flex-direction: column-reverse;
  justify-content: center;
  width: fit-content;
}
.image-preview img {
  width: 100px;
  height: 100px;
  border-radius: 10px;
  object-fit: cover;
}
.image-preview i {
  font-size: 1.5em;
  cursor: pointer;
  position: relative;
  top: 1.2em;
  left: calc(100% - 1.2em);
  color: #fff;
  width: min-content;
  text-align: right;
}
.image-preview i:hover {
  color: #aaa;
}
.btn-addroom {
  margin: 20px auto;
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  color: white;
  border-radius: 10px;
  outline: none;
  border: none;
  font-size: 1.2em;
  width: 80%;
  text-align: center;
  padding: 5px 0;
  transition: all 0.3s ease;
  cursor: pointer;
  font-weight: 600;
}
.btn-addroom:hover {
  color: #d4d4d4;
}
</style>
