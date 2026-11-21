<script setup>
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import Notification from '@/components/Notification.vue'
</script>

<template>
  <div class="app-shell">
    <div class="app-backdrop" aria-hidden="true">
      <span class="glow glow-a"></span>
      <span class="glow glow-b"></span>
    </div>

    <AppHeader />

    <main class="app-main">
      <Notification />
      <router-view v-slot="{ Component, route }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="route.path" />
        </Transition>
      </router-view>
    </main>

    <AppFooter />
  </div>
</template>

<style>
.app-shell {
  position: relative;
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1 0 auto;
  width: 100%;
}

/* 页面背景的柔和光晕 */
.app-backdrop {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
}

.glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(90px);
  opacity: 0.55;
}

.glow-a {
  width: 560px;
  height: 560px;
  top: -220px;
  left: -160px;
  background: #ffe9a8;
}

.glow-b {
  width: 520px;
  height: 520px;
  top: -200px;
  right: -180px;
  background: #e4dcff;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.22s ease, transform 0.22s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-leave-to {
  opacity: 0;
}
</style>
