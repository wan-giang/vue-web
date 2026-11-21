<script setup>
import SocialIcon from '@/components/SocialIcon.vue'

const socials = [
  { href: 'https://weibo.com/u/7861137548', className: 'social-weibo', label: '微博' },
  { href: 'https://v.douyin.com/R0CZVXm5esU/', className: 'social-douyin', label: '抖音' },
  { href: 'https://space.bilibili.com/3537104390850991', className: 'social-bilibili', label: 'B站' },
  { href: 'https://www.xiaohongshu.com/user/profile/65534da40000000002035d6f', className: 'social-xhs', label: '小红书' },
]

const personalInfo = [
  ['昵称', '小周'],
  ['生日', '2005-03-22'],
  ['星座', '白羊座'],
  ['血型', '-'],
  ['身高', '165 cm'],
  ['出生地', '中国 江苏'],
]

const memberInfo = [
  ['加入时间', '2023-05-02'],
  ['加入所属', 'SNH48 十八期生'],
  ['升格时间', '2023-08-18（当日S队公演宣布）'],
  ['最终所属', 'SNH48 S队（TEAM SII）'],
  ['所属公司', '上海丝芭文化传媒集团有限公司'],
  ['Catch Phrase', '这是新月，这是满月，这是——“周童玥”！'],
  ['应援色', '💛 黄色'],
]

const skills = [{ icon: 'fa-solid fa-music', text: '琵琶' }, { icon: 'fa-solid fa-bed', text: '睡觉' }]
const hobbies = [{ icon: 'fa-solid fa-heart', text: '美女' }, { icon: 'fa-solid fa-paw', text: '猫猫狗狗' }]

// team: 'sii' 为 Team SII 公演，'other' 为新生 / 企划公演
const stages = [
  { name: 'Team SII《48Hz》公演', period: '2026.10.10 - ', team: 'sii', current: true },
  { name: '2026全新公演企划《1&1 Anyone》公演', period: '2026.05.04 - ', team: 'other', current: true },
  { name: '《命运的X号》新生公演', period: '2023.05.02 - 2024.04.24', team: 'other' },
  { name: 'Team SII《幻镜-B版》公演', period: '2023.05.26 - 2025.02.16', team: 'sii' },
  { name: '《代号XII 2.0》新生公演', period: '2024.05.05 - 2025.03.12', team: 'other' },
  { name: 'Team SII《幻镜-C版》公演', period: '2025.02.23 - 2025.07.27', team: 'sii' },
  { name: 'Team SII《INTO THE LIGHT》公演', period: '2025.08.16 - 2026.10.02', team: 'sii' },
]

const awards = [
  { year: '2026', title: 'SNH48 GROUP 年度青春盛典', rank: 'No.41', note: '年度梦想成员奖' },
  { year: '2025', title: 'SNH48 GROUP 年度青春盛典', rank: 'No.47', note: '年度梦想成员奖' },
  { year: '2024', title: 'SNH48 GROUP 年度青春盛典', rank: 'No.53', note: '' },
]
</script>

<template>
  <div class="page baike-page">
      <!-- 姓名 & 简介 -->
      <section class="profile surface">
        <div class="profile-cover">
          <img src="/bg.webp" alt="" />
        </div>
        <div class="profile-body">
          <p class="kicker">Member Profile</p>
          <h1 class="profile-name">周童玥</h1>
          <p class="profile-en">Zhou TongYue</p>
          <p class="profile-team">TEAM SII · SNH48 十八期生</p>

          <!-- 社交链接 -->
          <div class="baike-social-links">
            <a
              v-for="item in socials"
              :key="item.href"
              :href="item.href"
              class="baike-social-link"
              target="_blank"
              rel="noreferrer"
            >
              <SocialIcon :class-name="item.className" />
              <span>{{ item.label }}</span>
            </a>
          </div>
        </div>
      </section>

      <!-- 基本信息 -->
      <section class="baike-section">
        <h2 class="section-title">基本信息</h2>
        <div class="info-grid">
          <article class="info-card surface">
            <h3 class="info-card-title"><i class="fa-solid fa-user"></i>个人信息</h3>
            <dl class="info-list">
              <div v-for="[k, v] in personalInfo" :key="k" class="info-row">
                <dt>{{ k }}</dt>
                <dd>{{ v }}</dd>
              </div>
            </dl>
          </article>

          <article class="info-card surface">
            <h3 class="info-card-title"><i class="fa-solid fa-star"></i>成员信息</h3>
            <dl class="info-list">
              <div v-for="[k, v] in memberInfo" :key="k" class="info-row">
                <dt>{{ k }}</dt>
                <dd>{{ v }}</dd>
              </div>
            </dl>
          </article>
        </div>
      </section>

      <!-- 特长 & 兴趣爱好 -->
      <section class="baike-section">
        <h2 class="section-title">个人特长及兴趣爱好</h2>
        <div class="info-grid">
          <article class="info-card surface">
            <h3 class="info-card-title"><i class="fa-solid fa-wand-magic-sparkles"></i>个人特长</h3>
            <div class="chip-row">
              <span v-for="item in skills" :key="item.text" class="chip">
                <i :class="item.icon"></i>{{ item.text }}
              </span>
            </div>
          </article>
          <article class="info-card surface">
            <h3 class="info-card-title"><i class="fa-solid fa-heart"></i>兴趣爱好</h3>
            <div class="chip-row">
              <span v-for="item in hobbies" :key="item.text" class="chip">
                <i :class="item.icon"></i>{{ item.text }}
              </span>
            </div>
          </article>
        </div>
      </section>

      <!-- 参加过的公演 -->
      <section class="baike-section">
        <h2 class="section-title">主要参与的公演</h2>
        <ol class="stage-timeline surface">
          <li v-for="item in stages" :key="item.name" class="stage-item" :class="[item.team, { current: item.current }]">
            <span class="stage-dot"></span>
            <div class="stage-text">
              <div class="stage-name">
                {{ item.name }}
                <span v-if="item.current" class="stage-badge">进行中</span>
              </div>
              <div class="stage-period">{{ item.period }}</div>
            </div>
          </li>
        </ol>
      </section>

      <!-- 奖项 -->
      <section class="baike-section">
        <h2 class="section-title">获奖</h2>
        <div class="award-grid">
          <article v-for="a in awards" :key="a.year" class="award-card surface">
            <i class="fa-solid fa-trophy award-icon"></i>
            <div class="award-year">{{ a.year }}</div>
            <div class="award-title">{{ a.title }}</div>
            <div class="award-rank">{{ a.rank }}</div>
            <div v-if="a.note" class="award-note">{{ a.note }}</div>
          </article>
        </div>
      </section>

      <!-- 团内人物关系 -->
      <!-- <details class="relationship-collapsible mt-4 mb-4">
        <summary class="relationship-summary row justify-content-center mb-3">
          <div class="col-md-10 col-xl-8 text-center">
            <h2 class="fw-bold mb-2">团内人物关系</h2>
            <div class="relationship-hint">点击展开</div>
          </div>
        </summary>

        <div class="row justify-content-center">
          <div class="col-md-10 col-xl-8">
            <1!-- 外层卡片 --1>
            <div class="bg-light shadow-sm border-0">
              <div class="card-body p-4 p-md-5">

              <1!-- 分区标题 --1>
              <div class="mb-4">
                <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
                  <h4 class="mb-0 fw-bold">周童玥的队友</h4>
                  <span class="badge text-bg-secondary">Team SII / 新生</span>
                </div>
                <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                  <p class="text-muted mb-3">
                    周童玥在 Team SII 以及新生公演时期的队友。
                  </p>
                </div>
                <1!-- <hr class="my-3"> --1>
              </div>

              <1!-- Team SII 现队友 --1>
              <section class="border-0 bg-light-subtle mb-4">
                <div class="card-body p-4">
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
                    <h5 class="mb-0 fw-bold">Team SII 现队友</h5>
                    <span class="badge rounded-pill text-bg-primary">现</span>
                  </div>
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                    <p class="text-muted mb-3">
                      包括正式成员、兼任成员和已分配到 Team SII 的预备生。
                    </p>
                  </div>

                  <div class="d-flex flex-wrap name-wrap">
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">曹可甜、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">蒋夏羽、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">刘婧阳、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">刘诗彤、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">李婷、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">芦馨怡、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">柳雨呈、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">刘增艳、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">宁轲、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">盛乐、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">田姝丽、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">由淼、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">闫明筠、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">杨心渝、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">张雷雷、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">张倩、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">吉雅楠（预备生）、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">武博涵（Team X兼任）</span>
                  </div>
                </div>
              </section>

              <1!-- Team SII 前队友 --1>
              <section class="border-0 bg-light-subtle mb-4">
                <div class="card-body p-4">
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
                    <h5 class="mb-0 fw-bold">Team SII 前队友</h5>
                    <span class="badge rounded-pill text-bg-secondary">前</span>
                  </div>
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                    <p class="text-muted mb-3">
                      包括已毕业或退团的正式成员，以及已解除兼任的兼任成员。
                    </p>
                  </div>

                  <div class="d-flex flex-wrap name-wrap">
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">李慧、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">马玉灵、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">邵雪聪、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">朱涵佳、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">黄恩茹、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">刘倩倩（原GNZ48 Team NIII兼任）、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">彭嘉敏、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">黄怡慈（原BEJ48 Team B兼任）、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">段艺璇、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">沈小爱、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">赵天杨、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">陈雨孜</span>
                  </div>
                </div>
              </section>

              <1!-- 新生公演 前队友 --1>
              <section class="border-0 bg-light-subtle mb-5">
                <div class="card-body p-4">
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
                    <h5 class="mb-0 fw-bold">新生公演 前队友</h5>
                    <span class="badge rounded-pill text-bg-secondary">新生阶段</span>
                  </div>
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                    <p class="text-muted mb-3">
                      新生公演（《命运的X号》《代号XII 2.0》）时期队友，不包括 Team SII 成员。
                    </p>
                  </div>

                  <div class="d-flex flex-wrap name-wrap">
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">林佳怡、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">禹佳蔚、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">张月铭、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">王依柳、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">熊紫轶、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">刘小涵、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">卢晨昕、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">李虞龙若、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">温若其、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">许佳佳、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">尤可莹、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">张怡婷、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">梁怀方、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">唐程成、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">王悦垚、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">王紫澍、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">叶凡、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">张瀚引、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">陈真允一、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">罗颍宸、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">温冰冰、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">吴欣怡、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">夏奕欣、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">张曼妮、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">陈芷晴、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">潘力帼、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">陈俞希、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">金泓言、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">李妍、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">李子忻、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">杨秋野（原名孙莉）、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">肖彦竹</span>
                  </div>
                </div>
              </section>

              <1!-- 其他关系 --1>
              <div class="mb-4">
                <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-2">
                  <h4 class="mb-0 fw-bold">其他关系</h4>
                  <span class="badge text-bg-secondary">活动</span>
                </div>
                <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                  <p class="text-muted mb-3">
                    周童玥在 SNH48 GROUP 其他活动中的队友。
                  </p>
                </div>
                <1!-- <hr class="my-3"> --1>
              </div>

              <section class="border-0 bg-light-subtle mb-4">
                <div class="card-body p-4">
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
                    <h5 class="mb-0 fw-bold">《最佳拍档》第四季 拍档</h5>
                    <span class="badge rounded-pill text-bg-primary">最佳拍档</span>
                  </div>

                  <div class="d-flex flex-wrap name-wrap">
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">庄雅雯（前 BEJ48 Team E 成员）</span>
                  </div>
                </div>
              </section>
              <section class="border-0 bg-light-subtle">
                <div class="card-body p-4">
                  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3">
                    <h5 class="mb-0 fw-bold">《燃烧吧，团魂》第二季「我说的都队」社团</h5>
                    <span class="badge rounded-pill text-bg-primary">团魂</span>
                  </div>

                  <div class="d-flex flex-wrap name-wrap">
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">刘增艳、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">叶凡（SNH48 Team NII 成员）、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">张倩、</span>
                    <span class="badge rounded-pill text-dark px-0 fs-6 fw-normal">唐程成（SNH48 Team NII 成员）</span>
                    <span class="badge rounded-pill text-bg-primary fs-6">周童玥：队长</span>
                  </div>
                </div>
              </section>

              </div>
            </div>
          </div>
        </div>
      </details> -->
  </div>
</template>

<style scoped>
.baike-page {
  max-width: 1000px;
  padding-top: 20px;
}

.profile {
  overflow: hidden;
  text-align: center;
}

.profile-cover {
  background: linear-gradient(135deg, #fff5d1, #efe9ff);
}

.profile-cover img {
  display: block;
  width: 100%;
  max-width: 640px;
  height: auto;
  margin: 0 auto;
}

.profile-body {
  padding: 28px 24px 32px;
}

.profile-name {
  margin: 0;
  font-size: clamp(34px, 5vw, 48px);
  font-weight: 900;
}

.profile-en {
  margin: 4px 0 0;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--c-accent-strong);
}

.profile-team {
  margin: 8px 0 0;
  color: var(--c-text-2);
}

.baike-social-links {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.baike-social-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 999px;
  border: 1px solid var(--c-border-strong);
  background: var(--c-surface);
  color: var(--c-text);
  font-size: 14px;
  font-weight: 600;
  line-height: 1;
  text-decoration: none;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.baike-social-link:hover {
  color: var(--c-text);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.baike-social-link :deep(.social-icon) {
  font-size: 17px;
}

.baike-social-link :deep(.social-icon-image) {
  display: block;
  width: 17px;
  height: 17px;
}

.baike-section {
  margin-top: 32px;
}

.baike-section .section-title {
  text-align: center;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.info-card {
  padding: 24px;
}

.info-card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 16px;
  font-size: 16px;
  font-weight: 700;
}

.info-card-title i {
  display: inline-grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: var(--c-accent-soft);
  color: var(--c-accent-strong);
  font-size: 14px;
}

.info-list {
  margin: 0;
}

.info-row {
  display: grid;
  grid-template-columns: 96px 1fr;
  gap: 12px;
  padding: 10px 0;
  border-top: 1px solid var(--c-border);
}

.info-row dt {
  font-weight: 500;
  color: var(--c-text-3);
  font-size: 14px;
}

.info-row dd {
  margin: 0;
  color: var(--c-text);
  font-size: 14px;
  font-weight: 500;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 999px;
  background: var(--c-surface-2);
  font-weight: 600;
}

.chip i {
  color: var(--c-accent-strong);
}

.stage-timeline {
  list-style: none;
  margin: 0;
  padding: 12px 28px;
}

.stage-item {
  position: relative;
  display: flex;
  gap: 16px;
  padding: 14px 0;
}

.stage-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 34px;
  bottom: -14px;
  width: 2px;
  background: var(--c-border);
}

.stage-dot {
  flex-shrink: 0;
  margin-top: 6px;
  width: 14px;
  height: 14px;
  border-radius: 999px;
  border: 3px solid #8b7bd8;
  background: #fff;
}

.stage-item.other .stage-dot {
  border-color: var(--c-accent);
}

.stage-item.current .stage-dot {
  background: var(--c-accent);
  border-color: var(--c-accent);
  box-shadow: 0 0 0 5px rgba(242, 183, 5, 0.2);
}

.stage-name {
  font-weight: 600;
  color: var(--c-text);
}

.stage-item.current .stage-name {
  font-weight: 800;
}

.stage-badge {
  display: inline-block;
  margin-left: 6px;
  padding: 1px 8px;
  border-radius: 999px;
  background: var(--c-accent-soft);
  color: var(--c-accent-ink);
  font-size: 11px;
  font-weight: 700;
  vertical-align: 2px;
}

.stage-period {
  margin-top: 2px;
  font-size: 13px;
  color: var(--c-text-3);
  font-variant-numeric: tabular-nums;
}

.award-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.award-card {
  position: relative;
  padding: 24px;
  overflow: hidden;
}

.award-card:first-child {
  background: linear-gradient(160deg, #fff5d1 0%, #fff 70%);
  border-color: rgba(242, 183, 5, 0.4);
}

.award-icon {
  position: absolute;
  right: 18px;
  top: 18px;
  font-size: 22px;
  color: var(--c-accent);
}

.award-year {
  font-size: 13px;
  font-weight: 700;
  color: var(--c-text-3);
}

.award-title {
  margin-top: 4px;
  font-size: 14px;
  color: var(--c-text-2);
}

.award-rank {
  margin-top: 12px;
  font-size: 34px;
  font-weight: 900;
  line-height: 1;
  color: var(--c-text);
}

.award-note {
  display: inline-block;
  margin-top: 10px;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--c-accent-soft);
  color: var(--c-accent-ink);
  font-size: 12px;
  font-weight: 700;
}

@media (max-width: 768px) {
  .baike-page {
    padding-top: 12px;
  }

  .info-grid,
  .award-grid {
    grid-template-columns: 1fr;
  }

  .info-row {
    grid-template-columns: 84px 1fr;
  }

  .stage-timeline {
    padding: 8px 18px;
  }

  .baike-section {
    margin-top: 24px;
  }
}

hr {
  border-top: 1px solid #dee2e6;
}

.name-wrap{
  max-width: 720px;   /* 关键：控制一行大约 6 个 */
  margin: 0 auto;     /* 居中 */
}

.relationship-collapsible {
  display: block;
}

.relationship-collapsible summary {
  list-style: none;
  cursor: pointer;
  user-select: none;
}

.relationship-collapsible summary::-webkit-details-marker {
  display: none;
}

.relationship-collapsible summary:hover {
  opacity: 0.9;
}

.relationship-hint {
  display: inline-block;
  padding: 0.3rem 0.75rem;
  border-radius: 999px;
  background: #e9ecef;
  color: #6c757d;
  font-size: 0.8rem;
  letter-spacing: 0.04em;
  margin: 0 auto;
}

.relationship-collapsible:not([open]) .relationship-hint {
  display: inline-block;
}

.relationship-collapsible[open] .relationship-hint {
  display: none;
}
</style>