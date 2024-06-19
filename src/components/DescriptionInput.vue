<template>
  <div>
    <textarea v-model="description" placeholder="Enter description"></textarea>
    <button @click="saveDescription">Save</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      description: ""
    }
  },
  methods: {
    saveDescription() {
      this.$emit("descriptionChanged", this.description)
      console.log("Description:", this.description)
    }
  }
}
</script>

<style scoped>
textarea {
  width: 100%;
  height: 200px;
}
</style>
