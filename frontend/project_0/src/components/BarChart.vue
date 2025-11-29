<template>
  <div class="chart-wrapper">
    <VChart :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from "vue";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
]);

provide(THEME_KEY, "darklight");

// Example monthly data
const months = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
];

const income = [
  88499.75, 77697.13, 6345.14, 25589.00, 42769.84, 44988.24, 37707.99, 43633.23, 66914.80, 26919.63, 71251.86, 0
];

const expenses = [
  81272.90, 55119.78, 32763.41, 36977.41, 36551.65, 48521.23, 52978.66, 54864.66, 56432.73, 42493.00, 55224.23, 0
];

const option = ref({
  title: {
    text: "Summary by Month",
    left: "left"
  },
  tooltip: {
    trigger: "axis",
    axisPointer: { type: "shadow" }
  },
  legend: {
    top: 20
  },
  grid: {
    left: "3%",
    right: "4%",
    bottom: "3%",
    containLabel: true
  },
  xAxis: {
    type: "category",
    data: months
  },
  yAxis: {
    type: "value"
  },
  series: [
    {
      name: "Income",
      type: "bar",
      data: income,
      barGap: 0,
      itemStyle: { color: "#6ab187" }
    },
    {
      name: "Expenses",
      type: "bar",
      data: expenses,
      itemStyle: { color: "#d32d41" }
    }
  ]
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
}
</style>
