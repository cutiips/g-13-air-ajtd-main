<template>
  <div>
    <input type="file" @change="handleFileChange" accept="image/*" multiple />
    <button @click="uploadPhotos">Upload</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFiles: []
    }
  },
  methods: {
    handleFileChange(event) {
      this.selectedFiles = Array.from(event.target.files)
    },
    uploadPhotos() {
      const formData = new FormData()
      this.selectedFiles.forEach((file, index) => {
        formData.append(`photos[${index}]`, file)
      })
      this.$emit("photosUploaded", formData)
    }
  }
}
</script>
