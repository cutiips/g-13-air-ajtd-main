<template>
  <div>
    <label for="price">Price:</label>
    <input type="number" id="price" v-model="price" @input="handleInput" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      price: 0
    }
  },
  methods: {
    handleInput() {
      this.$emit("priceChanged", this.price)
    }
  }
}
</script>
