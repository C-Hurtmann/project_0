<template>
  <div class="app-layout">
    <AppNavbar />
    <div class="layout-body">
      <div class="container-fluid main-content">
        <div class="row h-100">
          <AppSidebar />
          <main class="content-wrapper">
            <div class="board">
              <router-view />
            </div>
          </main>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppNavbar from './components/AppNavbar.vue'
import AppSidebar from './components/AppSidebar.vue'
</script>

<style>
/* layout container rules — could also live in base.css */
.app-layout, .layout-body {
  display: flex;
  height: 100vh;          /* full viewport height */
  overflow: hidden;
}

.layout-body {
  flex: 1;
  display: flex;
}
</style>
