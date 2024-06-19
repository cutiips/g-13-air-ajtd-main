<template>
  <div class="home">
    <HomePage />
    <ListRooms
      :noPagination="noPagination"
      :searchQuery="searchQuery"
      :currentPage="currentPage"
      :perPage="14"
      @page-change="currentPage = $event"
    />
  </div>
</template>

<script>
import HomePage from "../components/HomePage.vue"
import ListRooms from "../components/ListRooms.vue"

export default {
  components: {
    HomePage,
    ListRooms
  },
  data() {
    return {
      searchQuery: "",
      currentPage: 1,
      noPagination: true
    }
  }
}
</script>

<style>
img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
</style>
