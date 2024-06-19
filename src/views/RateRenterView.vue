<template>
  <div>
    <RateRenterButton @open-modal="showModal = true" />
    <RateRenterModal
      :isVisible="showModal"
      :renterId="Number(renterId)"
      @close-modal="showModal = false"
      @rating-submitted="fetchRenterRatings"
    />
  </div>
</template>

<script>
import RateRenterButton from "@/components/RateRenterButton.vue"
import RateRenterModal from "@/components/RateRenterModal.vue"

export default {
  components: {
    RateRenterButton,
    RateRenterModal
  },
  data() {
    return {
      showModal: false,
      renterId: this.$route.params.renterId
    }
  },
  methods: {
    fetchRenterRatings() {
      this.$refs.rateRenterModal.fetchRenterRatings()
    }
  }
}
</script>
