<template>
  <div class="chart-wrapper" style="width: 400px; height: 400px;">
    <VChart :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';

// Register only the parts you need
use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);

// Provide theme (optional)
provide(THEME_KEY, 'darklight');

// Sample data
const MAX_SLICES = 10;

// Mock data
const rawData = [
  { name: 'Wires, money orders', value: 9628.61 },
  { name: 'Financial institutions', value: 8158.69 },
  { name: 'Medical and dental labs', value: 5455.00 },
  { name: 'Convenience stores and Specialy markets', value: 2830.41 },
  { name: 'Grocery stores and Supermarkets', value: 2194.34 },
  { name: 'Eating places and restaurants', value: 1817.00 },
  { name: 'Medical services', value: 1800.00 },
  { name: 'Orthpedic goods and Posthelic devices', value: 1775.55 },
  { name: 'Taxicabs', value: 1549.00 },
  { name: 'Fast Food Restaurants', value: 1480.00 },
  { name: 'Drug stores and Pharmacies', value: 1058.73 },
  { name: 'Pet Shops and Supplies', value: 853.74 },


];
const sortedData = rawData.slice().sort((a, b) => b.value - a.value);

const total = sortedData.reduce((acc, cur) => acc + cur.value, 0);

const top = sortedData.slice(0, MAX_SLICES);
const others = sortedData.slice(MAX_SLICES);
const othersValue = others.reduce((sum, item) => sum + item.value, 0);

const dataForChart = [
  ...top,
  { name: 'Others', value: othersValue }
];

// Chart building
const option = ref({
  color: ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600', '#805300', '#c0a980', '#8097c0', '#c08097', '#97c080', '#cccccc'],
  title: {
    text: 'Expences on {month}',
    left: 'left'
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)',
    appendToBody: true,
    confine: false
  },
  series: [
    {
      name: 'Expence item',
      type: 'pie',
      radius: ['40%', '70%'],
      data: dataForChart,
      clockwise: true,
      labelLine: {show: false},
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      label: {
        show: true,
        position: 'center',
        formatter: `Total\n${total}`,  // Or: `${total} items`, or include text
        fontSize: 24,
        color: '#000'
      }

    }
  ]
});


</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  overflow: visible;
  position: relative;
}
</style>
