<template>
  <div>
    <label for="name">Name:</label>
    <input type="text" id="name" v-model="name" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: ""
    }
  }
}
</script>
