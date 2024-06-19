<template>
  <div>
    <input type="text" v-model="location" placeholder="Enter a location" />
    <button @click="submitLocation">Submit</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      location: ""
    }
  },
  methods: {
    submitLocation() {
      this.$emit("locationChanged", this.location)
      console.log("Location:", this.location)
    }
  }
}
</script>
