<script setup>
import { navItems, SECRET_CODE } from './navItems'

const year = new Date().getFullYear()
</script>

<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-name">小星云之家 <span class="footer-beta">Beta</span></div>
        <p class="footer-desc">由 SNH48-周童玥 的粉丝建立的，以介绍、宣传周童玥为主的网站。</p>
        <p class="footer-code">
          <i class="fa-solid fa-comment-dots"></i>
          神秘代码：<strong>{{ SECRET_CODE }}</strong>
        </p>
      </div>

      <nav class="footer-links" aria-label="页脚导航">
        <router-link v-for="item in navItems" :key="item.to" :to="item.to">
          {{ item.label }}
        </router-link>
      </nav>
    </div>

    <div class="footer-bottom">
      <span>&copy; {{ year }} 小星云之家</span>
      <span>部分资料来源：SNH48.com</span>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  margin-top: 28px;
  border-top: 1px solid var(--c-border);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.6), #fff);
  padding-bottom: env(safe-area-inset-bottom, 0px);
}

.footer-inner {
  max-width: var(--container);
  margin: 0 auto;
  padding: 28px var(--gutter) 20px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 24px 48px;
}

.footer-name {
  font-size: 18px;
  font-weight: 800;
  color: var(--c-text);
}

.footer-beta {
  margin-left: 6px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 2px 7px;
  border-radius: 999px;
  color: var(--c-accent-ink);
  background: var(--c-accent-soft);
  border: 1px solid rgba(242, 183, 5, 0.35);
  vertical-align: middle;
}

.footer-desc {
  margin: 8px 0 12px;
  color: var(--c-text-2);
  font-size: 14px;
}

.footer-code {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  padding: 6px 12px;
  border-radius: 999px;
  background: var(--c-surface-2);
  color: var(--c-text-2);
  font-size: 13px;
}

.footer-code i {
  color: var(--c-accent-strong);
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, auto);
  gap: 10px 28px;
  align-content: start;
}

.footer-links a {
  color: var(--c-text-2);
  font-size: 14px;
  text-decoration: none;
}

.footer-links a:hover {
  color: var(--c-text);
}

.footer-bottom {
  max-width: var(--container);
  margin: 0 auto;
  padding: 14px var(--gutter) 18px;
  border-top: 1px solid var(--c-border);
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 8px 16px;
  color: var(--c-text-3);
  font-size: 12px;
}

@media (max-width: 560px) {
  .footer-links {
    grid-template-columns: repeat(2, auto);
  }
}
</style>
