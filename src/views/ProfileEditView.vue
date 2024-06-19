<template>
  <ProfileEdit @save="saveChanges" @cancel="editing = false" />
</template>

<script>
import ProfileEdit from "../components/ProfileEdit.vue"

export default {
  components: {
    ProfileEdit
  },
  data() {
    return {
      editing: false,
      user: {}
    }
  },
  methods: {
    saveChanges(updatedUser) {
      this.user = updatedUser
      this.editing = false
    }
  }
}
</script>
