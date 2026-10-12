<script setup lang="ts">
import SideBarNavigation from '@/components/sideBarNavigation.vue'
</script>

<template>
  <div class="layout">
    <SideBarNavigation />

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.layout {
  min-height: 100vh;
  width: 100%;
}

.content {
  margin-left: 250px;
  min-width: 0;
  min-height: 100vh;

  padding: 32px 24px;

  box-sizing: border-box;
}

/* ================================
   TABLET
================================ */

@media (max-width: 900px) {
  .content {
    margin-left: 76px;
    padding: 28px 20px;
  }
}

/* ================================
   MOBILE
================================ */

@media (max-width: 600px) {
  .content {
    margin-left: 0;

    padding: 16px;
    padding-bottom: 90px;
  }
}
</style>