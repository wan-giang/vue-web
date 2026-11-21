<script setup>
defineProps({
  kicker: { type: String, default: '' },
  title: { type: String, required: true },
  description: { type: String, default: '' },
})
</script>

<template>
  <header class="page-header">
    <p v-if="kicker" class="kicker">{{ kicker }}</p>
    <h1 class="page-title">{{ title }}</h1>
    <p v-if="description" class="page-desc">{{ description }}</p>
    <slot />
  </header>
</template>

<style scoped>
.page-header {
  position: relative;
  text-align: center;
  padding: 28px 0 20px;
}

.page-title {
  margin: 0;
  font-size: clamp(30px, 4.6vw, 44px);
  font-weight: 800;
  letter-spacing: -0.01em;
  line-height: 1.15;
  color: var(--c-text);
}

.page-desc {
  max-width: 640px;
  margin: 10px auto 0;
  color: var(--c-text-2);
  font-size: 15px;
  line-height: 1.75;
}

@media (max-width: 768px) {
  .page-header {
    padding: 18px 0 14px;
  }
}
</style>
