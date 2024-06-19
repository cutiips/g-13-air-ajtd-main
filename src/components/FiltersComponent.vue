<template>
  <div class="filters-cont">
    <CButton class="filters-btn" @click="visible = !visible"
      >Filters <i class="fa-solid fa-list"></i
    ></CButton>
    <CCollapse :visible="visible">
      <div class="filters-collapse">
        <div class="filters">
          <h5>Features</h5>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="pets" v-model="pets" />
            <label for="pets">Pets allowed</label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="smoking" v-model="smoking" />
            <label for="smoking">Smoking allowed</label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="elevator" v-model="elevator" />
            <label for="elevator">Elevator</label>
          </div>
        </div>
        <div class="filters">
          <h5>Price Range</h5>
          <Slider v-model="value" :min="minVal" :max="maxVal" :step="1" />
        </div>
      </div>
    </CCollapse>
  </div>
</template>
<script>
import { CCollapse, CButton } from "@coreui/vue"
import Slider from "@vueform/slider"

export default {
  props: {
    minVal: {
      type: Number,
      default: 0
    },
    maxVal: {
      type: Number,
      default: 1000
    }
  },
  components: {
    CCollapse,
    CButton,
    Slider
  },
  data() {
    return {
      visible: false,
      value: [this.minVal, this.maxVal],
      pets: false,
      smoking: false,
      elevator: false
    }
  },
  computed: {
    features() {
      return {
        pets: this.pets,
        smoking: this.smoking,
        elevator: this.elevator
      }
    }
  },
  watch: {
    value() {
      this.$emit("price-range", this.value)
    },
    features: {
      handler() {
        this.$emit("features", this.features)
      },
      deep: true
    }
  }
}
</script>

<style>
.filters-btn {
  margin: auto;
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  color: white;
  border-radius: 10px;
  outline: none;
  border: none;
}

.filters-btn:hover {
  background: linear-gradient(20deg, rgb(218, 23, 78), red 20%, rgb(245, 106, 127), magenta);
  color: #e0e0e0;
}

.filters-btn:focus {
  color: white;
  overflow: none;
}

.filters-cont {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin: 10px auto;
}

.filters-collapse {
  padding: 15px 30px;
  width: 100%;
  display: flex;
  justify-content: center;
  flex-direction: row;
  flex-wrap: wrap;
}

.filters {
  width: 250px;
  --slider-connect-bg: linear-gradient(
    20deg,
    rgb(218, 23, 78),
    red 20%,
    rgb(245, 106, 127),
    magenta
  );
  --slider-tooltip-bg: red;
}

.filters:nth-child(1) h5 {
  text-align: center;
  margin-bottom: 15px;
}

.filters:nth-child(2) h5 {
  text-align: center;
  margin-bottom: 50px;
}

.form-check-input:checked {
  background-color: magenta;
  border-color: magenta;
  border: 1px solid magenta;
}

.form-check-input:focus {
  box-shadow: none;
  border: 1px solid #dee2e6;
}

.form-check-input:checked:focus {
  box-shadow:
    inset 0 1px 2px rgba(0, 0, 0, 0.075),
    0 0 5px magenta;
  border: 1px solid magenta;
}
</style>
<style src="@vueform/slider/themes/default.css"></style>
