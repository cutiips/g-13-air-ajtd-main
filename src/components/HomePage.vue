<template>
  <div>
    <div class="home">
      <h1>Air-AJTD</h1>
      <h4 class="undertitle">Find the perfect room for your next adventure</h4>
    </div>
    <hr class="bar" />
  </div>
</template>

<script>
export default {
  name: "HomePage",
  components: {}
}
</script>

<style scoped>
.home {
  text-align: center;
  margin: 3vh auto 0 auto;
  width: fit-content;
}
.undertitle {
  font-weight: normal;
}
.card-img-top {
  width: 50px;
  height: auto;
  margin-top: 10px;
  margin-left: auto;
  margin-right: auto;
  position: sticky;
  top: 0;
}
.card {
  width: 15rem;
  margin: 10px;
  background-color: rgb(255, 255, 255);
  border-color: rgb(133, 20, 75);
  border-width: 1px;
  color: rgb(133, 20, 75);
}
.cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.container-location {
  margin-top: 50px;
  margin-left: 50px;
  margin-right: 50px;
  background-color: rgb(238, 237, 212);
  padding: 20px;
  border-radius: 10px;
  color: rgb(133, 20, 75);
}
button {
  background-color: rgb(133, 20, 75);
  border-color: rgb(133, 20, 75);
  transition: all 0.4s ease;
  color: rgb(217, 217, 217);
}

button:hover {
  background-color: rgb(238, 237, 212);
  color: rgb(133, 20, 75);
  border-color: rgb(238, 237, 212);
}
</style>
