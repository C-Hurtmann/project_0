<template>
  <!-- Example: placeholder cards -->
  <div class="card card-rectangle shadow-sm">
    <div class="card-body">
      <!-- here you could embed a chart component -->
      Dashboard content 1
    </div>
  </div>
  <div class="card card-square shadow-sm">
    <div class="card-body">
      <PieChart />
    </div>
  </div>
  <!-- add more cards or use v‑for to render dynamic cards -->
</template>

<script setup lang="ts">
// If you have dynamic data/plots, you could fetch or compute them here
import PieChart from '../components/PieChart.vue'
</script>

<style scoped>
/* reuse your .board, .card, etc. styles — you can include them globally via base.css */
</style>
