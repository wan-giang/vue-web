<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { navItems, AVATAR_URL, SECRET_CODE } from './navItems'

const route = useRoute()
const drawerOpen = ref(false)
const scrolled = ref(false)

const isActive = (to) => (to === '/' ? route.path === '/' : route.path.startsWith(to))

const onScroll = () => {
  scrolled.value = window.scrollY > 8
}

const onKeydown = (event) => {
  if (event.key === 'Escape') drawerOpen.value = false
}

watch(() => route.fullPath, () => {
  drawerOpen.value = false
})

watch(drawerOpen, (open) => {
  document.documentElement.classList.toggle('no-scroll', open)
})

onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('keydown', onKeydown)
  document.documentElement.classList.remove('no-scroll')
})
</script>

<template>
  <header class="app-header" :class="{ 'is-scrolled': scrolled }">
    <div class="header-inner">
      <router-link to="/" class="brand" aria-label="小星云之家 首页">
        <span class="brand-avatar">
          <img :src="AVATAR_URL" alt="" />
        </span>
        <span class="brand-text">
          <span class="brand-name">小星云之家</span>
          <span class="brand-tag">Beta</span>
        </span>
      </router-link>

      <nav class="desktop-nav" aria-label="主导航">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link-item"
          :class="{ active: isActive(item.to) }"
        >
          {{ item.label }}
        </router-link>
      </nav>

      <button
        type="button"
        class="menu-button"
        :aria-expanded="drawerOpen"
        aria-label="打开菜单"
        @click="drawerOpen = !drawerOpen"
      >
        <span class="menu-bars" :class="{ open: drawerOpen }">
          <span></span><span></span><span></span>
        </span>
      </button>
    </div>
  </header>

  <Teleport to="body">
    <Transition name="fade">
      <div v-if="drawerOpen" class="drawer-mask" @click="drawerOpen = false" />
    </Transition>
    <Transition name="drawer">
      <aside v-if="drawerOpen" class="drawer" aria-label="移动端导航">
        <div class="drawer-head">
          <img :src="AVATAR_URL" alt="小周头像" class="drawer-avatar" />
          <div>
            <div class="drawer-title">小星云之家</div>
            <div class="drawer-sub">SNH48 · 周童玥粉丝站</div>
          </div>
          <button type="button" class="drawer-close" aria-label="关闭菜单" @click="drawerOpen = false">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>

        <nav class="drawer-nav">
          <router-link
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="drawer-link"
            :class="{ active: isActive(item.to) }"
          >
            <i :class="item.icon"></i>
            <span>{{ item.label }}</span>
            <i class="fa-solid fa-chevron-right drawer-chevron"></i>
          </router-link>
        </nav>

        <div class="drawer-foot">
          神秘代码 <strong>{{ SECRET_CODE }}</strong>
        </div>
      </aside>
    </Transition>
  </Teleport>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  padding-top: env(safe-area-inset-top, 0px);
  background: rgba(251, 250, 247, 0.72);
  backdrop-filter: saturate(180%) blur(16px);
  -webkit-backdrop-filter: saturate(180%) blur(16px);
  border-bottom: 1px solid transparent;
  transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
}

.app-header.is-scrolled {
  background: rgba(251, 250, 247, 0.86);
  border-bottom-color: var(--c-border);
  box-shadow: 0 6px 24px rgba(28, 25, 23, 0.05);
}

.header-inner {
  max-width: var(--container);
  margin: 0 auto;
  height: var(--header-h);
  padding: 0 var(--gutter);
  display: flex;
  align-items: center;
  gap: 24px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--c-text);
  flex-shrink: 0;
}

.brand-avatar {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  padding: 2px;
  background: conic-gradient(from 200deg, var(--c-accent), #ffe58a, #c9b6ff, var(--c-accent));
}

.brand-avatar img {
  width: 100%;
  height: 100%;
  border-radius: inherit;
  object-fit: cover;
  border: 2px solid #fff;
  display: block;
}

.brand-text {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.brand-name {
  font-size: 17px;
  font-weight: 800;
  letter-spacing: 0.02em;
}

.brand-tag {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 2px 7px;
  border-radius: 999px;
  color: var(--c-accent-ink);
  background: var(--c-accent-soft);
  border: 1px solid rgba(242, 183, 5, 0.35);
}

.desktop-nav {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 4px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--c-border);
}

.nav-link-item {
  position: relative;
  padding: 7px 14px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  color: var(--c-text-2);
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.2s ease, background 0.2s ease;
}

.nav-link-item:hover {
  color: var(--c-text);
  background: rgba(28, 25, 23, 0.05);
}

.nav-link-item.active {
  color: var(--c-text);
  background: var(--c-accent);
  box-shadow: 0 4px 14px rgba(242, 183, 5, 0.35);
}

.menu-button {
  display: none;
  margin-left: auto;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  border: 1px solid var(--c-border);
  background: #fff;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.menu-bars {
  position: relative;
  width: 18px;
  height: 12px;
  display: block;
}

.menu-bars span {
  position: absolute;
  left: 0;
  width: 100%;
  height: 2px;
  border-radius: 2px;
  background: var(--c-text);
  transition: transform 0.25s ease, opacity 0.2s ease, top 0.25s ease;
}

.menu-bars span:nth-child(1) { top: 0; }
.menu-bars span:nth-child(2) { top: 5px; }
.menu-bars span:nth-child(3) { top: 10px; }

.menu-bars.open span:nth-child(1) { top: 5px; transform: rotate(45deg); }
.menu-bars.open span:nth-child(2) { opacity: 0; }
.menu-bars.open span:nth-child(3) { top: 5px; transform: rotate(-45deg); }

@media (max-width: 960px) {
  .desktop-nav {
    display: none;
  }

  .menu-button {
    display: inline-flex;
  }
}

/* ===== 抽屉 ===== */
.drawer-mask {
  position: fixed;
  inset: 0;
  z-index: 1100;
  background: rgba(20, 16, 30, 0.38);
  backdrop-filter: blur(3px);
}

.drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 1101;
  width: min(320px, 86vw);
  display: flex;
  flex-direction: column;
  background: var(--c-bg);
  box-shadow: -20px 0 60px rgba(20, 16, 30, 0.18);
  padding: calc(env(safe-area-inset-top, 0px) + 20px) 16px calc(env(safe-area-inset-bottom, 0px) + 20px);
  border-radius: 24px 0 0 24px;
}

.drawer-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 4px 20px;
  border-bottom: 1px solid var(--c-border);
}

.drawer-avatar {
  width: 52px;
  height: 52px;
  border-radius: 999px;
  object-fit: cover;
  border: 2px solid var(--c-accent);
}

.drawer-title {
  font-weight: 800;
  font-size: 17px;
  color: var(--c-text);
}

.drawer-sub {
  font-size: 12px;
  color: var(--c-text-3);
}

.drawer-close {
  margin-left: auto;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid var(--c-border);
  background: #fff;
  color: var(--c-text-2);
  padding: 0;
}

.drawer-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px 0;
  flex: 1;
  overflow-y: auto;
}

.drawer-link {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 13px 14px;
  border-radius: 14px;
  color: var(--c-text-2);
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s ease, color 0.2s ease;
}

.drawer-link i:first-child {
  width: 20px;
  text-align: center;
  color: var(--c-text-3);
}

.drawer-link:hover {
  background: rgba(28, 25, 23, 0.04);
  color: var(--c-text);
}

.drawer-link.active {
  background: var(--c-accent-soft);
  color: var(--c-text);
}

.drawer-link.active i:first-child {
  color: var(--c-accent-strong);
}

.drawer-chevron {
  margin-left: auto;
  font-size: 12px;
  opacity: 0.35;
}

.drawer-foot {
  padding: 14px;
  border-radius: 14px;
  background: #fff;
  border: 1px dashed var(--c-border-strong);
  font-size: 13px;
  color: var(--c-text-2);
  text-align: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.drawer-enter-active,
.drawer-leave-active {
  transition: transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
}

.drawer-enter-from,
.drawer-leave-to {
  transform: translateX(100%);
}
</style>
