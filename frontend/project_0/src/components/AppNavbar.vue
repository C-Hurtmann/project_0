<template>
  <nav class="navbar navbar-expand-lg fixed-top">
    <div class="navbar-left">
      <a href="#" class="brand">
        <span class="brand-icon"><i class="fa-solid fa-chart-simple"></i></span>
        <span class="brand-text">PROJECT 0</span>
      </a>
    </div>

    <!-- <div class="navbar-breadcrumb">
      <a href="#" class="breadcrumb-item text-muted">Pages</a>
      <span class="breadcrumb-separator">/</span>
      <span class="breadcrumb-item active">Dashboard</span>
    </div> -->

    <div class="navbar-right">
      <div class="search-box">
        <i class="fa-solid fa-search search-icon"></i>
        <input type="text" placeholder="Type here…" />
      </div>
      <a href="#" class="nav-link">
        <i class="fa-solid fa-user"></i>
        <span>Sign In</span>
      </a>
      <a href="#" class="nav-link">
        <i class="fa-solid fa-cog"></i>
      </a>
      <a href="#" class="nav-link">
        <i class="fa-solid fa-bell"></i>
      </a>
    </div>
  </nav>
</template>

<script setup lang="ts">
// If you plan to add reactive props / state — you can add them here.
// For now, empty.
</script>

<style scoped>
/* Copy the CSS from your _navbar.css here */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 25px;
  background-color: #fff;
  border-bottom: 1px solid #eee;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  z-index: 1020;
  height: 56px;
}

/* ... rest of your CSS ... */

</style>
