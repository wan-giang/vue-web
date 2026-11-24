<script setup>
import PageHeader from '@/components/PageHeader.vue'
import { SECRET_CODE } from '@/components/navItems'

const features = [
  { icon: 'fa-solid fa-book-open', title: '小周百科', text: '周童玥的基本资料、特长爱好、参与公演与获奖经历。' },
  { icon: 'fa-solid fa-share-nodes', title: '社交平台', text: '微博、抖音、B站、小红书等官方与记录厅入口。' },
  { icon: 'fa-solid fa-masks-theater', title: '公演及活动', text: '所有参加过的公演及团内活动，附回放与 cut 视频。' },
]
</script>

<template>
  <div class="page about-page">
    <PageHeader
      kicker="About"
      title="关于小星云之家"
      description="小星云之家是由 SNH48-周童玥 的粉丝建立的，以介绍、宣传周童玥为主的网站。"
    />

    <section class="about-section">
      <h2 class="section-title">本站内容</h2>
      <div class="feature-grid">
        <article v-for="f in features" :key="f.title" class="feature-card surface">
          <span class="feature-icon"><i :class="f.icon"></i></span>
          <h3>{{ f.title }}</h3>
          <p>{{ f.text }}</p>
        </article>
      </div>
    </section>

    <section class="about-section">
      <h2 class="section-title">本站声明</h2>
      <div class="statement surface">
        <ul>
          <li>本站为周童玥的粉丝建立并管理，<strong>非周童玥个人官方网站</strong>。</li>
          <li>除特别注明来源的内容外，本站所有的图片、视频、音频等内容均来源于SNH48官方网站（SNH48.com）及SNH48官方社交平台。所有相关内容的版权均归原作者所有。</li>
          <li>本站仅提供周童玥相关的信息，不提供任何站内互动渠道。</li>
          <li>若对本站有任何意见或建议，或是有内容版权问题，请加入神秘代码：<strong>{{ SECRET_CODE }}</strong>，以联系网站管理员。</li>
          <li>若要与周童玥互动，请前往口袋48 App，在周童玥的口袋房间和她互动。</li>
        </ul>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-page {
  max-width: 960px;
}

.about-section {
  margin-top: 24px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.feature-card {
  padding: 24px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.feature-icon {
  display: inline-grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: var(--c-accent-soft);
  color: var(--c-accent-strong);
  font-size: 18px;
}

.feature-card h3 {
  margin: 16px 0 6px;
  font-size: 17px;
  font-weight: 700;
}

.feature-card p {
  margin: 0;
  color: var(--c-text-2);
  font-size: 14px;
  line-height: 1.7;
}

.statement {
  padding: 8px 28px;
}

.statement ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.statement li {
  position: relative;
  padding: 16px 0 16px 22px;
  color: var(--c-text-2);
  line-height: 1.7;
}

.statement li + li {
  border-top: 1px solid var(--c-border);
}

.statement li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 26px;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--c-accent);
}

.statement strong {
  color: var(--c-text);
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }

  .statement {
    padding: 4px 18px;
  }
}
</style>
