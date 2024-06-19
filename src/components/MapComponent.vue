<template>
  <div id="map"></div>
</template>

<script setup lang="ts">
import leaflet from "leaflet"
import { onMounted, watch } from "vue"

const props = defineProps({
  coords: {
    type: Array,
    required: true
  }
})

let map
let marker

onMounted(() => {
  map = leaflet.map("map").setView(props.coords, 13)
  leaflet
    .tileLayer("https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    })
    .addTo(map)
  marker = leaflet.marker(props.coords).addTo(map)
})

watch(
  () => props.coords,
  (newCoords) => {
    if (map && marker) {
      map.setView(newCoords, 13)
      marker.setLatLng(newCoords)
    }
  }
)
</script>

<style>
#map {
  width: 100%;
  height: 300px;
  border-radius: 30px;
}
#map img {
  border-radius: 0;
}
</style>
