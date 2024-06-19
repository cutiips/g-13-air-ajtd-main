<template>
  <button @click="openModal">Rate Renter</button>
</template>

<script>
export default {
  methods: {
    openModal() {
      this.$emit("open-modal")
    }
  }
}
</script>

<style scoped>
button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}
</style>
