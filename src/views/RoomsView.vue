<template lang="">
  <div>
    <SearchBar @search="handleSearch" @date-changed="updateDate" />
    <FiltersComponent
      @features="features = $event"
      @price-range="priceRange = $event"
      :minVal="minPrice"
      :maxVal="maxPrice"
    />
    <hr class="bar" />
    <ListRooms
      :noPagination="noPagination"
      :searchQuery="searchQuery"
      :currentPage="currentPage"
      :perPage="30"
      :priceRange="priceRange"
      :date="date"
      :features="features"
      @page-change="currentPage = $event"
      @min-max-price="(minPrice = $event[0]), (maxPrice = $event[1])"
    />
  </div>
</template>

<script>
import SearchBar from "../components/SearchBar.vue"
import ListRooms from "../components/ListRooms.vue"
import FiltersComponent from "../components/FiltersComponent.vue"

export default {
  name: "RoomsView",
  components: { SearchBar, ListRooms, FiltersComponent },
  data() {
    return {
      searchQuery: "",
      currentPage: 1,
      noPagination: false,
      date: [],
      priceRange: [0, 1000],
      minPrice: 0,
      maxPrice: 1000,
      features: []
    }
  },
  watch: {
    date(newDate) {
      localStorage.setItem("searchDate", JSON.stringify(newDate))
    }
  },
  methods: {
    handleSearch(searchValue) {
      this.searchQuery = searchValue
      this.currentPage = 1
    },
    updateDate(newDate) {
      this.date = newDate
    }
  }
}
</script>

<style>
.bar {
  width: 95%;
  margin: 20px auto;
  border: 1px solid #aaa;
}
</style>
