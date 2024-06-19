<template>
  <form class="search-bar" @submit.prevent="research">
    <div class="inputContainer">
      <input type="text" v-model="search" placeholder="Location ..." />
    </div>
    <div class="inputContainer">
      <VueDatePicker
        class="datepicker"
        v-model="date"
        :clearable="true"
        :min-date="new Date()"
        :enable-time-picker="false"
        :multi-calendars="{ static: false }"
        auto-apply
        no-today
        range
        placeholder="Dates ..."
      ></VueDatePicker>
    </div>
    <button class="btnSearch" type="submit">
      <i class="fa-solid fa-magnifying-glass"></i>
    </button>
  </form>
</template>
<script>
import VueDatePicker from "@vuepic/vue-datepicker"
import "@vuepic/vue-datepicker/dist/main.css"

export default {
  components: { VueDatePicker },
  data() {
    return {
      search: "",
      date: [],
      guests: 0
    }
  },
  methods: {
    research() {
      this.$emit("search", this.search)
      this.$emit("date-changed", this.date)
    }
  }
}
</script>
<style>
.search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  width: fit-content;
  border: 1px solid #aaa;
  border-radius: 30px;
  margin: 20px auto;
  height: 50px;
}
.search-bar .inputContainer {
  height: 100%;
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: row;
  gap: 3px;
}
.search-bar .inputContainer:nth-child(1) {
  width: 50%;
  border-top-left-radius: 30px;
  border-bottom-left-radius: 30px;
}
.search-bar .inputContainer:nth-child(2) {
  width: 60%;
}
.search-bar input {
  font-size: 1em;
  border: none;
}
.search-bar input[type="text"] {
  width: 100%;
  padding: 5px 10px 5px 25px;
  border-top-left-radius: 30px;
  border-bottom-left-radius: 30px;
}
.search-bar input:focus {
  outline: none;
  background-color: #f4f4f4;
}
.search-bar .inputContainer:focus-within {
  background-color: #f4f4f4;
}
.search-bar .inputContainer:focus-within input {
  outline: none;
  background-color: #f4f4f4;
}
.search-bar .datepicker {
  font-size: 1em;
  border: none;
}
.search-bar .datepicker:focus {
  outline: none;
  background-color: #f4f4f4;
}
.search-bar .datepicker:focus input {
  outline: none;
  background-color: #f4f4f4;
}
.search-bar .datepicker:focus-within {
  background-color: #f4f4f4;
}
.search-bar .inputContainer:nth-child(2) {
  border-left: 1px solid #aaa;
}
.search-bar .btnSearch {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  border: none;
  border-top-right-radius: 30px;
  border-bottom-right-radius: 30px;
  cursor: pointer;
  width: 70px;
  height: 50px;
  color: #fff;
  font-size: 1.3em;
  transition: all 0.3s ease;
}
.search-bar .btnSearch:hover {
  color: #d4d4d4;
}
@media screen and (max-width: 600px) {
  .search-bar {
    flex-direction: column;
    width: 90%;
    gap: 10px;
    padding: 10px;
    margin: 20px auto;
    height: fit-content;
    border: none;
  }
  .search-bar .inputContainer {
    width: 100%;
    padding: 5px;
    border-radius: 30px;
    border: 1px solid #aaa;
    height: 50px;
  }
  .search-bar .inputContainer:nth-child(1) {
    width: 100%;
    padding-left: 0;
  }
  .search-bar .inputContainer:nth-child(2) {
    width: 100%;
  }
  .search-bar .btnSearch {
    border-radius: 30px;
    width: 60%;
    height: fit-content;
    padding: 5px;
  }
  .search-bar .dp__input {
    border-radius: 30px;
  }
  .search-bar .inputContainer input[type="text"] {
    width: 100%;
    border-radius: 30px;
    padding: 5px 20px;
  }
  .search-bar .datepicker {
    border-radius: 30px;
  }
}
</style>
