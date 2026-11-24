<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import { useApi } from '@/composables/fetch'
import {
  getStageCodeLabel,
  getStageLogo,
  resolvePublicImg,
  BILIBILI_VIDEO_BASE
} from '@/utils/stageMeta'

const { apiFetch } = useApi()

const loading = ref(true)
const loadError = ref('')
const units = ref([])

// date 为 YYYYMMDD 整数
const toDateNumber = (date) => Number(String(date ?? '').trim()) || 0
const byDateDesc = (a, b) => toDateNumber(b.date) - toDateNumber(a.date)

const formatDate = (date) => {
  const s = String(date ?? '').trim()
  return /^\d{8}$/.test(s) ? `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}` : s
}

// 转换日期格式
const formatCNDateFromYYYYMMDD = (dateStr) => {
  if (!dateStr || dateStr.length !== 8) return ''

  const y = dateStr.slice(0, 4)
  const m = parseInt(dateStr.slice(4, 6), 10)
  const d = parseInt(dateStr.slice(6, 8), 10)

  return `${y}年${m}月${d}日`
}

const isMv = (item) => String(item.type || '').trim().toLowerCase() === 'mv'

// 优先用 img，没有则回退到所属公演 logo
const getItemImg = (item) => resolvePublicImg(item.img) || getStageLogo(item.stage_code)

const getVideoUrl = (url) => {
  const value = String(url || '').trim()
  if (!value) return null
  return /^https?:\/\//.test(value) ? value : BILIBILI_VIDEO_BASE + value
}

// details 为 JSON（可能是对象或字符串），取其中的 notes
const getNotes = (item) => {
  let details = item.details
  if (typeof details === 'string') {
    try {
      details = JSON.parse(details)
    } catch {
      return ''
    }
  }
  const notes = details && typeof details === 'object' ? details.notes : ''
  return notes === undefined || notes === null ? '' : String(notes).trim()
}

// 手机端点按切换备注，点页面其它地方关闭
const openNoteId = ref(null)
const toggleNote = (id) => {
  openNoteId.value = openNoteId.value === id ? null : id
}
const closeNote = () => {
  openNoteId.value = null
}

const mvList = computed(() => units.value.filter(isMv).sort(byDateDesc))

// unit 按 stage_code 分组，组内按日期降序；组之间按各组最新日期降序
const unitGroups = computed(() => {
  const groups = new Map()
  units.value
    .filter(item => !isMv(item))
    .forEach(item => {
      const code = String(item.stage_code || '').trim()
      if (!groups.has(code)) groups.set(code, [])
      groups.get(code).push(item)
    })

  return [...groups.entries()]
    .map(([code, items]) => ({
      code,
      label: getStageCodeLabel(code),
      items: items.sort(byDateDesc)
    }))
    .sort((a, b) => byDateDesc(a.items[0], b.items[0]))
})

const unitCount = computed(() => unitGroups.value.reduce((sum, g) => sum + g.items.length, 0))

const loadUnits = async () => {
  loading.value = true
  loadError.value = ''
  try {
    const { ok, data } = await apiFetch('/units')
    if (!ok) {
      loadError.value = data?.message || data?.error || '未知错误'
      return
    }
    units.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('加载失败', e)
    loadError.value = '网络错误'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUnits()
  document.addEventListener('click', closeNote)
})

onUnmounted(() => {
  document.removeEventListener('click', closeNote)
})
</script>

<template>
  <div class="page">
    <PageHeader
      kicker="Units & MV"
      title="舞台和MV"
      description="本站收录的周童玥参加的公演 Unit 舞台及 MV。"
    />

    <section class="featured surface">
      <div class="featured-head">
        <span class="featured-badge"><i class="fa-solid fa-play me-1"></i>精选视频</span>
        <h2 class="featured-title">Team SII《48Hz》首演 周童玥Unit《Up To You（真相背后）》</h2>
      </div>
    <div class="video-wrapper">
      <iframe
        src="https://player.bilibili.com/player.html?isOutside=true&aid=117416856196521&bvid=BV1YSpu6gEHF&cid=42650371492&p=1"
        scrolling="no"
        frameborder="0"
        allowfullscreen
      ></iframe>
    </div>
      <p class="featured-note">*视频来源于B站。相关推荐视频列表由B站自动生成，与本站无关，亦不代表本站立场。</p>
    </section>

    <div class="unit-groups">
      <div v-if="loading" class="unit-loading">
        <span class="spinner-border spinner-border-sm me-2"></span>正在加载…
      </div>
      <div v-else-if="loadError" class="unit-loading">❌ 请求失败：{{ loadError }}</div>

      <template v-else>
        <!-- MV -->
        <section v-if="mvList.length">
          <h3 class="group-title">
            <span>MV</span>
            <span class="group-count">{{ mvList.length }}</span>
          </h3>
          <ul class="list-group unit-list mb-3">
            <li v-for="item in mvList" :key="item.id" class="list-group-item">
              <div class="unit-row">
                <div class="unit-img">
                  <img v-if="getItemImg(item)" :src="getItemImg(item)" :alt="item.title" loading="lazy" />
                  <i v-else class="fa-solid fa-film"></i>
                </div>
                <div class="unit-title-col">
                  <div class="unit-title">{{ item.title }}</div>
                  <div class="unit-date text-muted small mt-1">
                    <span>发布日期：{{ formatCNDateFromYYYYMMDD(item.date) }}</span>
                    <span
                      v-if="getNotes(item)"
                      class="note-tip"
                      :class="{ 'is-open': openNoteId === item.id }"
                      role="button"
                      tabindex="0"
                      aria-label="查看备注"
                      @click.stop="toggleNote(item.id)"
                      @keyup.enter.stop="toggleNote(item.id)"
                    >
                      <i class="fa-solid fa-circle-info"></i>
                      <span class="note-bubble" role="tooltip">{{ getNotes(item) }}</span>
                    </span>
                  </div>
                </div>
                <div class="unit-actions">
                  <a
                    :href="getVideoUrl(item.url)"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="btn btn-sm"
                    :class="item.url ? 'btn-primary' : 'btn-secondary disabled'"
                    :tabindex="!item.url ? -1 : null"
                    :aria-disabled="!item.url"
                  >观看视频</a>
                </div>
              </div>
            </li>
          </ul>
        </section>

        <!-- Unit：按公演分子目录 -->
        <section v-if="unitGroups.length">
          <h3 class="group-title">
            <span>Units</span>
            <span class="group-count">{{ unitCount }}</span>
          </h3>
          <div v-for="group in unitGroups" :key="group.code" class="sub-group">
            <h4 class="sub-group-title">
              <img v-if="getStageLogo(group.code)" :src="getStageLogo(group.code)" :alt="`${group.label} logo`" class="sub-group-logo" />
              <span>{{ group.label }}</span>
              <span class="group-count">{{ group.items.length }}</span>
            </h4>
            <ul class="list-group unit-list mb-3">
              <li v-for="item in group.items" :key="item.id" class="list-group-item">
                <div class="unit-row">
                  <div class="unit-img">
                    <img v-if="getItemImg(item)" :src="getItemImg(item)" :alt="item.title" loading="lazy" />
                    <i v-else class="fa-solid fa-music"></i>
                  </div>
                  <div class="unit-title-col">
                    <div class="unit-title">{{ item.title }}</div>
                    <div class="unit-date text-muted small mt-1">
                    <span>首演：{{ formatCNDateFromYYYYMMDD(item.date) }}</span>
                    <span
                      v-if="getNotes(item)"
                      class="note-tip"
                      :class="{ 'is-open': openNoteId === item.id }"
                      role="button"
                      tabindex="0"
                      aria-label="查看备注"
                      @click.stop="toggleNote(item.id)"
                      @keyup.enter.stop="toggleNote(item.id)"
                    >
                      <i class="fa-solid fa-circle-info"></i>
                      <span class="note-bubble" role="tooltip">{{ getNotes(item) }}</span>
                    </span>
                  </div>
                  </div>
                  <div class="unit-actions">
                    <a
                      :href="getVideoUrl(item.url)"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="btn btn-sm"
                      :class="item.url ? 'btn-primary' : 'btn-secondary disabled'"
                      :tabindex="!item.url ? -1 : null"
                      :aria-disabled="!item.url"
                    >观看视频</a>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </section>

        <div v-if="!mvList.length && !unitGroups.length" class="unit-loading">暂无数据</div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.featured {
  max-width: 720px;
  margin: 0 auto 8px;
  text-align: center;
  padding: 16px;
}

.featured-head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.featured-badge {
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--c-ink);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
}

.featured-title {
  margin: 0;
  font-size: clamp(17px, 2.4vw, 22px);
  font-weight: 800;
}

.featured-note {
  margin: 12px 0 0;
  font-size: 12px;
  color: var(--c-text-3);
}

.video-wrapper {
  width: 100%;
  margin: 0 auto;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: #000;
}
.video-wrapper iframe { width: 100%; height: 100%; border: none; }

.unit-groups {
  max-width: 1000px;
  margin: 0 auto;
}

.unit-loading {
  text-align: center;
  color: var(--c-text-3);
  padding: 32px 0;
}

.group-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 22px 0 12px;
  font-size: 20px;
  font-weight: 800;
}

.group-title::before {
  content: '';
  width: 4px;
  height: 20px;
  border-radius: 4px;
  background: var(--c-accent);
}

.group-count {
  padding: 1px 10px;
  border-radius: 999px;
  background: var(--c-surface-2);
  color: var(--c-text-2);
  font-size: 13px;
  font-weight: 700;
}

.sub-group {
  margin-left: 14px;
}

.sub-group-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 16px 0 10px;
  font-size: 16px;
  font-weight: 700;
  color: var(--c-text-2);
}

.sub-group-logo {
  height: 22px;
  width: auto;
  object-fit: contain;
}

.unit-list {
  gap: 10px;
  --bs-list-group-border-width: 0;
}

.unit-list .list-group-item {
  border: 1px solid var(--c-border) !important;
  border-radius: var(--radius-md) !important;
  background: var(--c-surface);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.unit-list .list-group-item:hover {
  border-color: var(--c-border-strong) !important;
  box-shadow: var(--shadow-md);
}

.unit-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.unit-img {
  flex-shrink: 0;
  width: 120px;
  height: 68px;
  border-radius: var(--radius-sm, 8px);
  background: var(--c-surface-2);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: var(--c-text-3);
  font-size: 22px;
}

.unit-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.unit-title-col {
  flex-grow: 1;
  min-width: 0;
  word-break: break-word;
}

.unit-title {
  font-weight: 600;
  color: var(--c-text);
}

.unit-actions {
  flex-shrink: 0;
}

.unit-date {
  display: flex;
  align-items: center;
  gap: 6px;
}

.note-tip {
  position: relative;
  display: inline-flex;
  align-items: center;
  color: var(--c-text-3);
  cursor: pointer;
  outline: none;
}

.note-tip:hover,
.note-tip:focus-visible,
.note-tip.is-open {
  color: var(--c-accent-ink, var(--c-accent));
}

.note-bubble {
  position: absolute;
  left: 50%;
  bottom: calc(100% + 8px);
  transform: translateX(-50%);
  z-index: 20;
  width: max-content;
  max-width: min(280px, 70vw);
  padding: 8px 12px;
  border-radius: 8px;
  background: var(--c-text, #222);
  color: var(--c-surface, #fff);
  font-size: 13px;
  line-height: 1.5;
  white-space: pre-line;
  word-break: break-word;
  box-shadow: var(--shadow-md);
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transition: opacity 0.15s ease;
}

.note-bubble::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: var(--c-text, #222);
}

.note-tip.is-open .note-bubble,
.note-tip:focus-visible .note-bubble {
  opacity: 1;
  visibility: visible;
}

@media (hover: hover) {
  .note-tip:hover .note-bubble {
    opacity: 1;
    visibility: visible;
  }
}

.unit-actions .btn {
  white-space: nowrap;
}

@media (max-width: 575.98px) {
  .sub-group {
    margin-left: 0;
  }

  .unit-row {
    gap: 12px;
  }

  .unit-img {
    width: 88px;
    height: 50px;
  }
}
</style>
