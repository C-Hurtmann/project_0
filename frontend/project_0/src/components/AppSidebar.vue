<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <!-- optional header content -->
    </div>
    <nav class="sidebar-menu">
      <router-link
        v-for="item in menuItems"
        :key="item.name"
        :to="item.to"
        class="menu-item"
        :class="{ active: isActiveRoute(item.to) }"
      >
        <i :class="item.iconClass"></i>
        <span>{{ item.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// Define your menu items here
const menuItems = [
  { name: 'dashboard', to: '/dashboard', label: 'Dashboard', iconClass: 'fa-solid fa-chart-line' },
  { name: 'transactions', to: '/transactions', label: 'Transactions', iconClass: 'fa-solid fa-piggy-bank' },
  { name: 'profile', to: '/profile', label: 'Profile', iconClass: 'fa-solid fa-user' },
  { name: 'settings', to: '/settings', label: 'Settings', iconClass: 'fa-solid fa-gear' },
];

// Router-based active check
function isActiveRoute(path: string) {
  return route.path === path;
}
</script>
