<script setup>
import { ref, onMounted, computed } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import { useApi } from '@/composables/fetch'


const timelineItems = ref([])
const isLoading = ref(true)

// ===== 年表类型切换：重要 / 全部 =====
const scopeOptions = [
  { key: 'imp', label: '重要大事年表' },
  { key: 'all', label: '全部大事年表' }
]
const activeScope = ref('imp') // 默认显示重要

// ===== 年份筛选（只要这几个）=====
const yearOptions = ['all', '2026', '2025', '2024', '2023']
const activeYear = ref('all')

const getYear = (rawDate) => (rawDate && rawDate.length >= 4 ? rawDate.slice(0, 4) : '未知')

// 转换日期格式
const formatCNDateFromYYYYMMDD = (dateStr) => {
  if (!dateStr || dateStr.length !== 8) return ''

  const y = dateStr.slice(0, 4)
  const m = parseInt(dateStr.slice(4, 6), 10)
  const d = parseInt(dateStr.slice(6, 8), 10)

  return `${y}年${m}月${d}日`
}

// 详情换行规整
const normalizeDetail = (text) => {
  if (!text) return ''
  return String(text).replace(/\\r\\n/g, '\n').replace(/\\n/g, '\n')
}

// ===== 组合筛选：年份 + (重要/全部) =====
const filteredTimelineItems = computed(() => {
  let arr = timelineItems.value

  // ① scope：重要才按 is_imp 过滤
  if (activeScope.value === 'imp') {
    arr = arr.filter(it => it.is_imp === true)
  }

  // ② 年份
  if (activeYear.value !== 'all') {
    arr = arr.filter(it => getYear(it.rawDate) === activeYear.value)
  }

  return arr
})

// 调用api
const { apiFetch } = useApi()

// ===== 出道天数（按北京时间日期计算，出道当天计为第 1 天）=====
const DEBUT_DATE = Date.UTC(2023, 4, 2)
const getBeijingTodayUTC = () => {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit'
  }).formatToParts(new Date())
  const get = (type) => Number(parts.find(p => p.type === type).value)
  return Date.UTC(get('year'), get('month') - 1, get('day'))
}
const debutDays = Math.floor((getBeijingTodayUTC() - DEBUT_DATE) / 86400000) + 1

// ===== 已完成公演场次：is_end 为 true 的条目中 session 最大值 =====
const stageCount = ref(null)
const loadStageCount = async () => {
  try {
    const { ok, data } = await apiFetch('/stages')
    if (!ok || !Array.isArray(data)) return
    stageCount.value = data
      .filter(item => item.is_end === true)
      .reduce((max, item) => Math.max(max, parseInt(item.session, 10) || 0), 0)
  } catch (e) {
    console.error('公演场次加载失败', e)
  }
}

const loadEvents = async () => {
  isLoading.value = true
  try {
    const { ok, data } = await apiFetch('/events')
    if (!ok) {
      alert('❌ 活动数据加载失败')
      return
    }

    // ✅注意：这里不能再 filter is_imp，否则“全部”模式永远没有非重要事件
    timelineItems.value = (data ?? [])
      .map(item => ({
        id: item.id,
        rawDate: item.date, // YYYYMMDD
        date: formatCNDateFromYYYYMMDD(item.date),
        title: item.title,
        img: item.img ? `/${item.img}` : '', // 重要模式要用到图片
        tag: 'SNH48',
        detail: item.detail,
        is_imp: item.is_imp === true
      }))
      .sort((a, b) => a.rawDate.localeCompare(b.rawDate))
  } catch (e) {
    console.error('加载失败', e)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadEvents()
  loadStageCount()
})
</script>

<template>
  <div class="page text-center">

      <PageHeader
        kicker="Timeline"
        title="大事年表"
        description="除特别注明外，所有图片均来自 SNH48 公演直播截图，或由 SNH48 官方微博发布。"
      />

      <section class="stats">
        <div class="stat-card surface">
          <div class="stat-label"><i class="fa-regular fa-calendar me-1"></i>出道至今</div>
          <div class="stat-value">{{ debutDays }}<span class="stat-unit">天</span></div>
          <div class="stat-note">自 2023年5月2日 出道</div>
        </div>
        <div class="stat-card surface">
          <div class="stat-label"><i class="fa-solid fa-masks-theater me-1"></i>已完成公演</div>
          <div class="stat-value">
            <template v-if="stageCount !== null">{{ stageCount }}<span class="stat-unit">场</span></template>
            <span v-else class="spinner-border spinner-border-sm"></span>
          </div>
          <div class="stat-note">按已结束公演的最大场次计</div>
        </div>
      </section>

      <section class="timeline-section">

        <!-- ① 年表类型切换：重要 / 全部 -->
        <div class="scope-filter">
          <button
            v-for="s in scopeOptions"
            :key="s.key"
            type="button"
            class="scope-btn"
            :class="{ active: activeScope === s.key }"
            @click="activeScope = s.key"
          >
            {{ s.label }}
          </button>
        </div>

        <!-- ② 年份筛选条 -->
        <div class="year-filter">
          <button
            v-for="y in yearOptions"
            :key="y"
            type="button"
            class="year-btn"
            :class="{ active: activeYear === y }"
            @click="activeYear = y"
          >
            {{ y === 'all' ? '全部' : y }}
          </button>
        </div>

        <!-- ✅重要：保留原时间轴格式 -->
        <div v-if="activeScope === 'imp'" class="timeline">
          <div
            v-for="(it, idx) in filteredTimelineItems"
            :key="it.id ?? (it.rawDate + '_' + idx)"
            class="timeline-row"
            :class="{ reverse: idx % 2 === 1 }"
          >
            <!-- 左侧（或右侧）图片卡 -->
            <div class="timeline-media">
              <div class="photo-card">
                <img v-if="it.img" :src="it.img" :alt="it.title" />
              </div>
            </div>

            <!-- 中轴线与圆点 -->
            <div class="timeline-axis">
              <span class="axis-dot"></span>
            </div>

            <!-- 右侧（或左侧）信息条 -->
            <div class="timeline-info">
              <div class="info-bar">
                <div class="info-date">{{ it.date }}</div>
                <div class="info-sub">{{ it.title }}</div>
                <div class="info-detail">{{ normalizeDetail(it.detail) }}</div>
              </div>
            </div>
          </div>

          <div v-if="isLoading" class="empty-tip">正在加载…</div>
          <div v-else-if="filteredTimelineItems.length === 0" class="empty-tip">当前筛选无数据</div>
        </div>

        <!-- ✅全部：列表模式（不带图片） -->
        <div v-else class="event-list">
          <div
            v-for="it in filteredTimelineItems"
            :key="it.id ?? (it.rawDate + '_' + it.title)"
            class="event-item"
          >
            <div class="event-head">
              <div class="event-date">{{ it.date }}</div>
              <!-- <span v-if="it.is_imp" class="badge-imp">重要</span> -->
            </div>

            <div class="event-title">{{ it.title }}</div>

            <!-- <div v-if="normalizeDetail(it.detail)" class="event-detail">
              {{ normalizeDetail(it.detail) }}
            </div> -->
          </div>

          <div v-if="isLoading" class="empty-tip">正在加载…</div>
          <div v-else-if="filteredTimelineItems.length === 0" class="empty-tip">当前筛选无数据</div>
        </div>
      </section>
  </div>
</template>

<style scoped>
.stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  max-width: 720px;
  margin: 0 auto;
}

.stat-card {
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.stat-label {
  font-size: 14px;
  font-weight: 700;
  color: var(--c-text-2);
}

.stat-value {
  font-size: clamp(32px, 6vw, 48px);
  font-weight: 800;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
  color: var(--c-text);
}

.stat-unit {
  margin-left: 4px;
  font-size: 16px;
  font-weight: 700;
  color: var(--c-text-2);
}

.stat-note {
  font-size: 12px;
  color: var(--c-text-3);
}

@media (max-width: 479.98px) {
  .stats {
    gap: 10px;
  }

  .stat-card {
    padding: 16px 10px;
  }
}

.timeline-section {
  width: 100%;
  max-width: 1000px;
  margin: 28px auto 0;
  text-align: left;
}

.timeline-title {
  font-size: 30px;
  font-weight: 700;
  margin: 6px 0 18px;
  text-align: center;
}

/* ===== 年表类型切换 ===== */
.scope-filter {
  display: flex;
  width: fit-content;
  max-width: 100%;
  gap: 4px;
  margin: 8px auto 14px;
  padding: 4px;
  border-radius: 999px;
  background: var(--c-surface-2);
  border: 1px solid var(--c-border);
}

.scope-btn {
  border: none;
  background: transparent;
  padding: 8px 18px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  font-size: 14px;
  color: var(--c-text-2);
  transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
}
.scope-btn.active {
  background: var(--c-surface);
  color: var(--c-text);
  box-shadow: var(--shadow-sm);
}

/* ===== 年份筛选条 ===== */
.year-filter {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 8px 0 16px;
  justify-content: center;
}
.year-btn {
  border: 1px solid var(--c-border-strong);
  background: var(--c-surface);
  padding: 6px 16px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  color: var(--c-text-2);
  font-variant-numeric: tabular-nums;
  transition: all 0.2s ease;
}
.year-btn:hover {
  color: var(--c-text);
  border-color: var(--c-text-3);
}
.year-btn.active {
  border-color: var(--c-ink);
  background: var(--c-ink);
  color: #fff;
}

.empty-tip {
  margin: 18px 0 6px;
  text-align: center;
  color: #888;
  font-size: 14px;
}

/* 容器 */
.timeline {
  position: relative;
  padding: 8px 0;
}

/* 一行：三列（媒体 / 中轴 / 信息） */
.timeline-row {
  display: grid;
  grid-template-columns: 1fr 56px 1fr;
  align-items: center;
  gap: 16px;
  padding: 18px 0;
}

/* 奇偶反转：让内容左右交错 */
.timeline-row.reverse .timeline-media {
  order: 3;
}
.timeline-row.reverse .timeline-info {
  order: 1;
}
.timeline-row.reverse .timeline-axis {
  order: 2;
}

.timeline-axis {
  position: relative;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.timeline-axis::before {
  content: "";
  position: absolute;
  top: -18px;
  bottom: -18px;
  width: 2px;
  background: #e5e5e5;
  left: 50%;
  transform: translateX(-50%);
}
.axis-dot {
  width: 14px;
  height: 14px;
  border-radius: 999px;
  background: white;
  border: 3px solid #f2b705;
  box-shadow: 0 0 0 4px rgba(240, 90, 119, 0.12);
  z-index: 2;
}

/* ====== 图片卡（模仿截图：圆角+描边） ====== */
.photo-card {
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid var(--c-border);
  box-shadow: var(--shadow-md);
  background: #111;
  max-width: 640px;
  width: 100%;
}

.photo-card img {
  width: 100%;
  height: auto;
  display: block;
}

/* 右上角斜角标（BEJ48） */
.corner-tag {
  position: absolute;
  top: 10px;
  right: -34px;
  transform: rotate(45deg);
  background: #f2b705;
  color: #fff;
  font-weight: 700;
  font-size: 12px;
  padding: 6px 40px;
  letter-spacing: 1px;
}

/* ====== 信息条（粉色渐变 + 左侧红色竖条/横线） ====== */
.timeline-info {
  display: flex;
  justify-content: flex-start;
}

.timeline-row.reverse .timeline-info {
  justify-content: flex-end;
}

.info-bar {
  width: min(640px, 100%);
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-left: 4px solid var(--c-accent);
  box-shadow: var(--shadow-sm);
  padding: 16px 20px;
  border-radius: var(--radius-md);
}
.timeline-row.reverse .info-bar {
  border-left: 1px solid var(--c-border);
  border-right: 4px solid var(--c-accent);
}
.info-date {
  font-size: 18px;
  font-weight: 800;
  color: var(--c-accent-strong);
  padding-bottom: 10px;
  border-bottom: 1px solid var(--c-border);
  margin-bottom: 10px;
}
.info-sub {
  font-size: 17px;
  color: var(--c-text);
  letter-spacing: 0.5px;
  font-weight: 600;
}
.info-detail {
  padding-top: 8px;
  font-size: 13px;
  color: var(--c-text-2);
  letter-spacing: 0.5px;
  white-space: pre-line;
  line-height: 1.65;
}

@media (max-width: 768px) {
  /* ① 单列（你已有） */
  .timeline-row {
    grid-template-columns: 1fr;
    gap: 14px;
    text-align: center; /* 关键：整体文本居中 */
  }

  .timeline-axis {
    display: none;
  }

  /* ② 图片卡整体居中 */
  .timeline-media {
    display: flex;
    justify-content: center;
  }

  /* ③ 信息条容器居中 */
  .timeline-info {
    display: flex;
    justify-content: center !important;
  }

  /* ④ 信息卡片自身居中 + 文本对齐 */
  .info-bar {
    margin: 0 auto;
    text-align: left; /* 如果你想正文仍然左对齐，可保留 */
  }

  /* ⑤ 取消 reverse 带来的左右逻辑影响 */
  .timeline-row.reverse .timeline-media,
  .timeline-row.reverse .timeline-info {
    order: initial;
  }

  .timeline-row.reverse .info-bar {
    border-right: 1px solid var(--c-border);
    border-left: 4px solid var(--c-accent);
  }
}

/* ====== 全部：列表样式（无图片） ====== */
.event-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 6px 0 10px;
}
.event-item {
  border: 1px solid var(--c-border);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  background: var(--c-surface);
  box-shadow: var(--shadow-sm);
  text-align: left;
}
.event-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.event-date {
  font-size: 14px;
  font-weight: 800;
  color: var(--c-accent-strong);
}
.badge-imp {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 999px;
  border: 1px solid rgba(240, 90, 119, 0.35);
  background: rgba(240, 90, 119, 0.12);
  color: #c23a53;
  font-weight: 800;
}
.event-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--c-text);
  line-height: 1.35;
  margin-bottom: 6px;
}
.event-detail {
  font-size: 14px;
  color: #555;
  letter-spacing: 0.2px;
  white-space: pre-line;
  line-height: 1.65;
}
</style>
