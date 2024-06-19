<template>
  <div v-if="!disabled" class="pagination">
    <button @click="goToFirstPage" :disabled="currentPage === 1" class="first">First</button>
    <button @click="previousPage" :disabled="currentPage === 1">&laquo;</button>
    <span v-for="pageNumber in visiblePages" :key="pageNumber">
      <button @click="goToPage(pageNumber)" :class="{ active: pageNumber === currentPage }">
        {{ pageNumber }}
      </button>
    </span>
    <button @click="nextPage" :disabled="currentPage === totalPages">&raquo;</button>
    <button @click="goToLastPage" :disabled="currentPage === totalPages" class="last">Last</button>
  </div>
</template>

<script>
export default {
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    visiblePages() {
      const pageNumbers = []
      let startPage = Math.max(1, this.currentPage - 1)
      let endPage = Math.min(this.totalPages, startPage + 2)

      while (startPage <= endPage) {
        pageNumbers.push(startPage)
        startPage++
      }

      return pageNumbers
    }
  },
  methods: {
    goToPage(pageNumber) {
      this.$emit("page-change", pageNumber)
    },
    goToFirstPage() {
      this.$emit("page-change", 1)
    },
    goToLastPage() {
      this.$emit("page-change", this.totalPages)
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.$emit("page-change", this.currentPage - 1)
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.$emit("page-change", this.currentPage + 1)
      }
    }
  }
}
</script>

<style>
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  margin: 0;
  border: 1px solid #ccc;
  outline: none;
  background-color: #f1f1f1;
}

.pagination button:hover {
  background-color: #f1f1f1;
}

.pagination button:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.first {
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
}

.last {
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
}

.pagination button.active {
  background-color: red;
  border: 1px solid red;
  color: white;
}
</style>
