<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import ZonedDateTime from '@/components/ZonedDateTime.vue'
import PageHeader from '@/components/PageHeader.vue'
import Modal from '@/components/Modal.vue'
import { useApi } from '@/composables/fetch'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

// 增加路由
// const router = useRouter()


// 引入 Pinia 状态
const auth = useAuthStore()
const { token, isLoggedIn } = storeToRefs(auth)  // 保持响应式
const { verifyToken, startPolling, stopPolling } = auth             // 非 ref 的函数可直接解构
const authChecked = ref(false)

// 调用api
const { apiFetch } = useApi()

// 默认弹框关闭
const showModal = ref(false)
const selectedItem = ref(null)        // 原始数据，用于页面展示
const tempItem = ref({})              // 临时副本，仅用于弹框编辑
const showDetailModal = ref(false)
const detailItem = ref(null)

const unitTypeOptions = [
  { value: 'regular', label: '常规' },
  { value: 'yueyaoqu', label: '乐曜曲' },
  { value: 'birthday', label: '生日公演' },
  { value: 'election', label: '作品展演' },
  { value: 'mvp', label: 'MVP公演' },
  { value: 'graduation', label: '毕业公演' },
  { value: 'encore', label: '安可/奖励' },
  { value: 'todaymvp', label: '今日之星' },
  { value: 'b50', label: '金曲大赏' },
  { value: 'special', label: '特殊' }
]

const unitTypeValueSet = new Set(unitTypeOptions.map(option => option.value))

const unitSongOptionsByStageCode = {
  'MX': ['Ice Queen', 'Battle Cry', '占卜师', '深海之声', '双生花', '最后的曙光'],
  'HJ-B': ['初眠（Ring）', '下一站是你', 'Let it down（深海之森）', 'Scream Out（火柴梗）', '爱未央', 'Miss D（迷失地）'],
  'XII': ['她和她', '完美超载', 'Love Letter', '初吻练习曲', '自以为', '人间规则'],
  'HJ-C': ['爱的加速器', '最好的朋友', '关不掉', '皆渡（莲）', '粉红狙击手', '0.2s'],
  'ITL': ['残骸（ForEver）', 'Like it（随机碰撞）', '呓语（Lullaby）', 'Over & Over', '距离（Hesitate）', '新纪元（Nova Terra）', '换下制服之前', '女孩', '回响（Calling when I\'m gone）', '看春春欲晚'],
  '48Hz': ['返校日（Class H）', '今日晴', 'Brave Heart', '要你说爱我', 'Up To You（真相背后）', 'Black Rain'],
}

const getUnitSongOptions = (stageCode) => {
  const code = String(stageCode || '').trim()
  return unitSongOptionsByStageCode[code] || []
}

const createEmptyUnit = () => ({
  name: '',
  pos: '',
  type: 'regular'
})

const normalizeUnitList = (rawUnit) => {
  let source = rawUnit

  if (!source) return []

  if (typeof source === 'string') {
    try {
      source = JSON.parse(source)
    } catch {
      return []
    }
  }

  if (!Array.isArray(source)) return []

  return source.map((item) => ({
    name: String(item?.name || ''),
    pos: item?.pos === undefined || item?.pos === null ? '' : String(item.pos),
    type: unitTypeValueSet.has(item?.type) ? item.type : 'regular'
  }))
}

const addUnitItem = () => {
  if (!Array.isArray(tempItem.value.unit)) {
    tempItem.value.unit = []
  }
  tempItem.value.unit.push(createEmptyUnit())
}

const removeUnitItem = (index) => {
  tempItem.value.unit.splice(index, 1)
}

const draggedUnitIndex = ref(null)
const dragOverUnitIndex = ref(null)

const handleUnitDragStart = (index) => {
  draggedUnitIndex.value = index
}

const handleUnitDragOver = (index) => {
  if (draggedUnitIndex.value === null || draggedUnitIndex.value === index) return
  dragOverUnitIndex.value = index
}

const handleUnitDrop = (index) => {
  const fromIndex = draggedUnitIndex.value
  if (fromIndex === null || fromIndex === index) return
  if (!Array.isArray(tempItem.value.unit)) return

  const units = tempItem.value.unit
  const [movedItem] = units.splice(fromIndex, 1)
  if (!movedItem) return

  units.splice(index, 0, movedItem)
  draggedUnitIndex.value = index
  dragOverUnitIndex.value = null
}

const handleUnitDragEnd = () => {
  draggedUnitIndex.value = null
  dragOverUnitIndex.value = null
}

const moveUnitItemUp = (index) => {
  if (!Array.isArray(tempItem.value.unit)) return
  if (index <= 0) return

  const units = tempItem.value.unit
  const [current] = units.splice(index, 1)
  units.splice(index - 1, 0, current)
}

const moveUnitItemDown = (index) => {
  if (!Array.isArray(tempItem.value.unit)) return

  const units = tempItem.value.unit
  if (index < 0 || index >= units.length - 1) return

  const [current] = units.splice(index, 1)
  units.splice(index + 1, 0, current)
}

const getUnitTypeLabel = (type) => {
  const found = unitTypeOptions.find(option => option.value === type)
  return found ? found.label : '常规'
}

const isPositiveInteger = (value) => /^[1-9]\d*$/.test(String(value).trim())

// 详情弹框中每条 Unit 的结构化展示：歌名 / 站位 / 类型
const getUnitDetail = (unitItem) => {
  const name = unitItem?.name || '-'
  const type = unitItem?.type
  const typeLabel = getUnitTypeLabel(type)
  const pos = String(unitItem?.pos ?? '').trim()
  const showPos = type === 'regular' || type === 'yueyaoqu' || type === 'b50'
  const isSpecial = type === 'special'

  let posLabel = ''
  let posKind = 'pos'

  if (showPos || (isSpecial && (isPositiveInteger(pos) || pos === '0'))) {
    if (pos === '0') {
      posLabel = 'Solo'
      posKind = 'solo'
    } else {
      posLabel = `${pos || '-'} 号位`
    }
  } else if (pos === '1') {
    posLabel = ''
  } else if (isSpecial) {
    posLabel = pos
  } else {
    posLabel = pos ? `助演 ${pos}` : '助演'
    posKind = 'support'
  }

  return { name, type, typeLabel, posLabel, posKind }
}

const validateUnits = (units) => {
  if (!Array.isArray(units)) return true

  for (let i = 0; i < units.length; i += 1) {
    const item = units[i] || {}
    const lineNumber = i + 1
    const name = String(item.name || '').trim()
    const pos = String(item.pos ?? '').trim()
    const type = item.type

    if (!name) {
      alert(`❗ Unit 第 ${lineNumber} 条：name 为必填项`)
      return false
    }

    // if (!isPositiveInteger(pos)) {
    //   alert(`❗ Unit 第 ${lineNumber} 条：pos 必须是正整数`)
    //   return false
    // }

    if (!unitTypeValueSet.has(type)) {
      alert(`❗ Unit 第 ${lineNumber} 条：type 只能选择给定选项`)
      return false
    }
  }

  return true
}

const normalizeUnitsForPayload = (units) => {
  if (!Array.isArray(units)) return []

  return units.map(item => ({
    name: String(item.name || '').trim(),
    pos: String(item.pos).trim(),
    type: item.type
  }))
}

function formatDateForInput(datetimeStr) {
  // 原始格式: "2025-06-15 13:45:00+08:00"
  // 去掉秒和时区部分
  return datetimeStr.replace(' ', 'T').slice(0, 16)
}
function toISOWithTimezoneOffset(date) {
  const pad = (num) => String(num).padStart(2, '0')

  const yyyy = date.getFullYear()
  const mm = pad(date.getMonth() + 1)
  const dd = pad(date.getDate())
  const hh = pad(date.getHours())
  const min = pad(date.getMinutes())
  const ss = pad(date.getSeconds())

  // 假设固定使用北京时间 +08:00
  return `${yyyy}-${mm}-${dd}T${hh}:${min}:${ss}+08:00`
}
const openModal = (item = null) => {
  if (item) {
    // 编辑：深拷贝已有项
    selectedItem.value = item
    tempItem.value = JSON.parse(JSON.stringify(item))
    tempItem.value.unit = normalizeUnitList(tempItem.value.unit)
    if (tempItem.value.date) {
      tempItem.value.date = formatDateForInput(tempItem.value.date)
    }
  } else {
    // 新建：初始化默认值
    selectedItem.value = null
    tempItem.value = {
      session: '0',
      date: '',
      type: '',
      stage_code: '',
      title: '',
      url: '',
      cut_url: '',
      time: '',
      is_stage: false,
      is_end: false,
      unit: [],
    }
  }
  showModal.value = true
}

const openDetailModal = (item) => {
  detailItem.value = {
    ...item,
    unit: normalizeUnitList(item.unit)
  }
  showDetailModal.value = true
}

const closeDetailModal = () => {
  showDetailModal.value = false
}

const handleConfirm = async () => {
  // 校验必填字段
  if (!tempItem.value.title 
    || !tempItem.value.date 
    || !tempItem.value.session
    || !tempItem.value.type
  ) {
    alert('❗ 请填写所有必填项')
    showModal.value = true
    return
  }

  if (!validateUnits(tempItem.value.unit)) {
    showModal.value = true
    return
  }

  const normalizedUnit = normalizeUnitsForPayload(tempItem.value.unit)
  const normalizedVenue = String(tempItem.value.time || '').trim()

  const payload = {
    session: tempItem.value.session,
    date: toISOWithTimezoneOffset(new Date(tempItem.value.date)),
    type: tempItem.value.type,
    stage_code: tempItem.value.stage_code,
    title: tempItem.value.title,
    url: tempItem.value.url,
    cut_url: tempItem.value.cut_url,
    time: normalizedVenue,
    is_stage: tempItem.value.is_stage,
    is_end: tempItem.value.is_end,
    unit: normalizedUnit
  }

  let result
  try {
    if (selectedItem.value) {
      // 编辑（PUT）
      result = await apiFetch(`/stages/${tempItem.value.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
    } else {
      // 新建（POST）
      result = await apiFetch('/stages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
    }

    const { ok, status, data } = result

    if (!ok) {
      if (status === 401) {
        alert('⚠️ 登录过期，请重新登录')
        router.push('/login')
      } else {
        alert(`❌ ${selectedItem.value ? '修改' : '添加'}失败：${data.message || '服务器错误'}`)
      }
      return
    }

    alert(`✅ ${selectedItem.value ? '修改' : '添加'}成功`)
    showModal.value = false
    loadStages()

  } catch (err) {
    // 捕获网络错误
    alert('❌ 网络连接失败，请检查网络或稍后重试')
    console.error(err)
    return
  }
}

// 刷新登录状态
window.addEventListener('storage', (event) => {
  if (event.key === 'token_zty') {
    const store = useAuthStore()
    store.isLoggedIn = !(event.newValue === null)
  }
})

const groupedStages = ref({ 'Team SII': [], '11': [], '新生': [], '其它': [] })
const expandedGroups = ref({ 'Team SII': false, '11': false, '新生': false, '其它': false })
const maxInitial = 3

const toggleExpanded = group => {
  expandedGroups.value[group] = !expandedGroups.value[group]
}

const loadStages = async () => {
  try {
    const { ok, status, data } = await apiFetch('/stages')
    if (!ok) {
      alert(`❌ 请求失败：${data.message || '未知错误'}`)
      return
    }

    const now = new Date()
    const temp = {
      '今日公演': [],
      '今日行程': [],
      '即将开始': [],
      'Team SII 公演': [],
      '1&1 Anyone 公演': [],
      '新生公演': [],
      '其它公演及活动': []
    }

    data.forEach(item => {
      const type = item.type?.trim()
      const date = new Date(item.date?.trim())
      const isStage = item.is_stage
      const isUpcoming = date > now

      // 判断是否为今日公演，直接按照0时计算
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const targetDate = new Date(date)
      targetDate.setHours(0, 0, 0, 0)
      const isCurrent = targetDate.getTime() <= today.getTime() && item.is_end === false
    
      if (isCurrent && isStage) {
        temp['今日公演'].push(item)
      } else if (isCurrent && !isStage) {
        temp['今日行程'].push(item)
      } else if (isUpcoming) {
        temp['即将开始'].push(item)
      } else if (type === 'Team SII') {
        temp['Team SII 公演'].push(item)
      } else if (type === '11') {
        temp['1&1 Anyone 公演'].push(item)
      } else if (type === '新生' || type === 'New Members') {
        temp['新生公演'].push(item)
      } else {
        temp['其它公演及活动'].push(item)
      }
    })

    for (const key in temp) {
      // 筛选出未开始的公演组别
      const isTodayGroup = key.includes('今日') || key === '即将开始'
      
      temp[key].sort((a, b) => {
        // const sessionDiff = parseInt(b.session) - parseInt(a.session)
        // if (sessionDiff !== 0) return sessionDiff

        // session 相同时，再按时间排序
        const dateA = new Date(a.date?.trim())
        const dateB = new Date(b.date?.trim())
        // 今日 → 时间升序，其它 → 时间降序
        return isTodayGroup
          ? dateA - dateB   // 升序（早的在前）
          : dateB - dateA   // 降序（晚的在前）
      })
    }

    groupedStages.value = temp
    filteredStages.value = { ...temp }
  } catch (e) {
    console.error('加载失败', e)
  }
}

// 判断时区
const isEast8 = ref(true)
const timezone = ref('')

onMounted(async () => {
  loadStages()  // 加载
  // getTimezoneOffset 返回的是分钟，东八区 = -480
  isEast8.value = new Date().getTimezoneOffset() === -480
  timezone.value = Intl.DateTimeFormat().resolvedOptions().timeZone
  await verifyToken()
  authChecked.value = true
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})

// 搜索
const searchQuery = ref("")
const searchSession = ref("")
const searchStageCode = ref("")
const searchStart = ref("")
const searchEnd = ref("")
const searchStartType = ref("text")
const searchEndType = ref("text")
const filteredStages = ref({})

const applyFilters = () => {
  const filtered = {}

  for (const group in groupedStages.value) {
    filtered[group] = groupedStages.value[group].filter(item => {
      const matchQuery =
        !searchQuery.value ||
        item.title.includes(searchQuery.value) ||
        item.type.includes(searchQuery.value)

      const matchSession =
        !searchSession.value ||
        item.session === String(searchSession.value)

      const matchStageCode =
        !searchStageCode.value ||
        item.stage_code === searchStageCode.value

      const date = new Date(item.date)
      const matchStart = !searchStart.value || date >= new Date(searchStart.value)
      const matchEnd = !searchEnd.value || date <= new Date(new Date(searchEnd.value).getTime() + 86400000)

      return matchQuery && matchSession && matchStageCode && matchStart && matchEnd
    })
  }

  filteredStages.value = filtered
}

const clearFilters = () => {
  searchQuery.value = ""
  searchSession.value = ""
  searchStageCode.value = ""
  searchStart.value = ""
  searchEnd.value = ""

  // ✅ 重置类型，恢复 placeholder 显示
  searchStartType.value = "text"
  searchEndType.value = "text"

  filteredStages.value = { ...groupedStages.value }
}

// 判断是否距离现在开始30分钟
const parseToDate = (v) => {
  if (!v) return null

  // 数字：可能是秒/毫秒时间戳
  if (typeof v === 'number') {
    return new Date(v < 1e12 ? v * 1000 : v)
  }

  // 字符串：兼容 "YYYY-MM-DD HH:mm:ss" / "YYYY-MM-DD HH:mm" / ISO
  if (typeof v === 'string') {
    const s = v.trim().replace(' ', 'T') // 让 "2025-12-31 19:00" 变成 ISO 友好格式
    const d = new Date(s)
    return isNaN(d.getTime()) ? null : d
  }

  // Date 对象
  if (v instanceof Date) return v

  return null
}

const splitTitle = (title) => {
  const normalizedTitle = String(title || '')
    .replace(/\\\\n/g, '\n')
    .replace(/\\n/g, '\n')
  const match = normalizedTitle.match(/（完整回放由B站up主“[^\"]*”提供）/)
  if (!match) {
    const main = normalizedTitle.trim()
    return { main, note: '', mainLines: main.split('\n'), noteLines: [] }
  }
  const note = match[0]
  const main = normalizedTitle.replace(note, '').trim()
  return {
    main,
    note,
    mainLines: main.split('\n'),
    noteLines: note.split('\n')
  }
}

const getTypeLabel = (type) => {
  const map = {
    'Team SII': 'Team SII',
    '11': '1&1 Anyone 公演队',
    'New Members': '新生公演队',
    'Team NII': 'Team NII',
    'Team HII': 'Team HII',
    'Team X': 'Team X',
    'Others': '其它（特殊公演或非公演）'
  }
  return map[type] || type || '-'
}

const getStageCodeLabel = (stageCode) => {
  const map = {
    MX: '命运的X号',
    'HJ-B': '幻镜-B版',
    XII: '代号XII 2.0',
    'HJ-C': '幻镜-C版',
    ITL: 'INTO THE LIGHT',
    11: '1&1 Anyone',
    '48Hz': '48Hz',
    SJHS: '三角函数',
    FX: 'Fire X',
    SP: '其它（特殊公演或非公演）'
  }
  return map[stageCode] || stageCode || '-'
}

const stageLogoMap = {
  'HJ-B': 'hj_lg.png',
  'HJ-C': 'hj_lg.png',
  MX: 'mx_lg.png',
  XII: 'xii_lg.png',
  ITL: 'itl_lg.png',
  '11': '11_lg.png',
  '48Hz': '48hz_lg.png'
}

const getStageLogo = (stageCode) => {
  const file = stageLogoMap[String(stageCode || '').trim()]
  return file ? `${import.meta.env.BASE_URL}lg/${file}` : ''
}

const getVenueLabel = (venue) => {
  const normalizedVenue = String(venue || '').trim()
  const map = {
    SNH: 'SNH48星梦剧院',
    BEJ: 'BEJ48壹空间',
    GNZ: 'GNZ48星梦剧院',
    CKG: 'CKG48星梦剧院',
    CGT: 'CGT48星梦剧院',
    HZ: '杭州星梦空间',
    NA: '其它剧场'
  }
  if (!normalizedVenue) {
    return 'SNH48星梦剧院'
  }
  return map[normalizedVenue] || normalizedVenue
}

const canShowLiveButton = (startDateLike) => {
  const start = parseToDate(startDateLike)
  if (!start) return false

  const now = new Date()

  // 提前 30 分钟的时间点
  const showFrom = new Date(start.getTime() - 30 * 60 * 1000)

  return now >= showFrom
}

</script>

<template>
  <div class="page">


      <PageHeader
        kicker="Stages & Events"
        title="公演及活动"
        description="本站收录的周童玥参加的公演及活动，包括即将进行、正在进行以及已经结束的 Team SII 公演、新生公演以及其它公演和活动。"
      />

      <details class="stage-guide surface">
        <summary>
          <span><i class="fa-regular fa-circle-question me-2"></i>按钮说明</span>
          <i class="fa-solid fa-chevron-down guide-chevron"></i>
        </summary>
        <ul class="guide-list">
          <li><span class="guide-tag tag-live">观看直播</span>SNH48 官方账号正在直播的公演或活动。</li>
          <li><span class="guide-tag tag-replay">完整视频回放</span>SNH48 官方账号发布的公演完整视频回放。若回放非官方发布，则会在标题注明。</li>
          <li><span class="guide-tag tag-cut">小周cut视频</span>公演中周童玥相关内容的剪辑回放。</li>
          <li><span class="guide-tag tag-off">灰色按钮</span>代表该场公演没有回放，或是没有制作剪辑。</li>
        </ul>
        <p class="guide-note">点击按钮可跳转至发布在 B 站的直播或视频页面。</p>
      </details>

      <div v-if="!isEast8" class="tz-warning">
        <i class="fa-solid fa-earth-asia"></i>
        <span><strong>注意：</strong>以下公演及活动所标出的时间，是您当前所在位置（{{ timezone }}）的时间，而非北京时间。</span>
      </div>

      <section class="filter-card surface">
        <div class="filter-head">
          <h2 class="filter-title"><i class="fa-solid fa-sliders me-2"></i>按条件筛选</h2>
          <p class="filter-hint">可按关键词、场次、公演名称、时间来筛选。寻找与周童玥相关的重要公演，可在关键词中输入 <strong>周童玥</strong>。</p>
        </div>

        <div class="filter-grid">
          <div class="filter-field filter-wide">
            <i class="fa-solid fa-magnifying-glass field-icon"></i>
            <input v-model="searchQuery" class="form-control form-control-sm with-icon" placeholder="关键词，如：生日公演" @keyup.enter="applyFilters" />
          </div>
          <div class="filter-field">
            <input v-model="searchSession" type="number" class="form-control form-control-sm" placeholder="场次，如：239" @keyup.enter="applyFilters" />
          </div>
          <div class="filter-field">
            <select v-model="searchStageCode" class="form-select form-select-sm">
              <option value="">全部公演</option>
              <option value="MX">命运的X号</option>
              <option value="HJ-B">幻镜-B版</option>
              <option value="XII">代号XII 2.0</option>
              <option value="HJ-C">幻镜-C版</option>
              <option value="ITL">INTO THE LIGHT</option>
              <option value="11">1&amp;1 Anyone</option>
              <option value="48Hz">48Hz</option>
              <option value="SJHS">三角函数</option>
              <option value="FX">Fire X</option>
              <option value="SP">其它（特殊公演或非公演）</option>
            </select>
          </div>

          <!-- 日期输入框：统一用 text + 切换成 date -->
          <div class="filter-field">
            <input
              v-model="searchStart"
              :type="searchStartType"
              class="form-control form-control-sm"
              placeholder="开始日期"
              @focus="searchStartType = 'date'"
              @blur="() => { if (!searchStart) searchStartType = 'text' }"
            />
          </div>
          <div class="filter-field">
            <input
              v-model="searchEnd"
              :type="searchEndType"
              class="form-control form-control-sm"
              placeholder="结束日期"
              @focus="searchEndType = 'date'"
              @blur="() => { if (!searchEnd) searchEndType = 'text' }"
            />
          </div>

          <div class="filter-actions">
            <button class="btn btn-primary btn-sm" @click="applyFilters">搜索</button>
            <button class="btn btn-outline-primary btn-sm" @click="clearFilters">重置</button>
          </div>
        </div>
      </section>

      <template v-if="authChecked && isLoggedIn">
        <button class="btn btn-success mb-3 d-block mx-auto" @click="() => openModal()">
          <i class="fa-solid fa-plus me-1"></i> 新建公演或活动记录
        </button>
      </template>

      <div class="stage-groups">
        <!-- 加载状态 -->
        <div v-if="!Object.keys(filteredStages).length" class="stage-loading">
          <span class="spinner-border spinner-border-sm me-2"></span>正在加载…
        </div>

        <!-- 数据已加载 -->
        <template v-for="(items, group) in filteredStages" :key="group">
          <h3 v-if="items.length" class="group-title">
            <span>{{ group }}</span>
            <span class="group-count">{{ items.length }}</span>
          </h3>
          <ul v-if="items.length" class="list-group stage-list mb-3">
            <li
              v-for="(item, index) in (expandedGroups[group] ? items : items.slice(0, maxInitial))"
              :key="item.id || item.session + item.date"
              class="list-group-item"
              >
              <div class="stage-row d-flex flex-column flex-md-row align-items-md-center gap-2 gap-md-3">
                <!-- 左侧：场次 + 日期 -->
                <div class="stage-meta text-center">
                  <div class="stage-session">
                    {{ item.session !== '0' ? `第 ${item.session} 场` : '不计入场次' }}
                  </div>
                  <ZonedDateTime :datetime="item.date" class="text-muted" />
                </div>

                <!-- 中间：标题 -->
                <div class="stage-title-col flex-grow-1 d-flex justify-content-center justify-content-md-start align-items-center text-center text-md-start">
                  <div>
                    <div class="stage-title">{{ splitTitle(item.title).mainLines[0] }}</div>
                    <div
                      v-for="(line, lineIndex) in splitTitle(item.title).mainLines.slice(1)"
                      :key="lineIndex"
                      class="text-muted small mt-1"
                    >
                      {{ line }}
                    </div>
                    <div v-if="splitTitle(item.title).note" class="text-muted small mt-1">
                      <template v-for="(line, lineIndex) in splitTitle(item.title).noteLines" :key="lineIndex">
                        <span>{{ line }}</span>
                        <br v-if="lineIndex < splitTitle(item.title).noteLines.length - 1" />
                      </template>
                    </div>
                  </div>
                </div>

                <!-- 右侧：两个按钮 -->
                <div class="stage-actions d-flex justify-content-center justify-content-md-end align-items-center gap-2">
                  <!-- 判断 group 是否为“今日公演”，且是否距离开场30分钟之内，然后提供直播入口 -->
                  <template v-if="group === '今日公演' && canShowLiveButton(item.date)">
                    <!-- SNH 或 time 为空 -->
                    <a
                      v-if="!item.time || item.time === 'SNH'"
                      href="https://live.bilibili.com/48"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- GNZ -->
                    <a
                      v-else-if="item.time === 'GNZ'"
                      href="https://live.bilibili.com/391199"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- BEJ -->
                    <a
                      v-else-if="item.time === 'BEJ'"
                      href="https://live.bilibili.com/383045"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- CKG -->
                    <a
                      v-else-if="item.time === 'CKG'"
                      href="https://live.bilibili.com/6015846"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- CGT -->
                    <a
                      v-else-if="item.time === 'CGT'"
                      href="https://live.bilibili.com/27848865"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- 默认情况 -->
                    <a
                      v-else
                      href="javascript:void(0)"
                      target="_blank"
                      class="btn btn-sm btn-success disabled"
                    >
                      暂无直播
                    </a>
                  </template>

                  <!-- 如果是“今日公演”，且距离开场超过30分钟，不提供直播入口 -->
                  <template v-else-if="group === '今日公演'">
                    <a href="javascript:void(0)" class="btn btn-sm btn-success disabled">
                      暂无直播
                    </a>
                  </template>

                  <!-- 判断 group 是否为“今日行程”，然后按钮变灰 -->
                  <template v-else-if="group === '今日行程'">
                    <a
                      href=""
                      target="_blank"
                      class="btn btn-sm btn-success disabled"
                    >
                      暂无直播
                    </a>
                  </template>
                  <!-- 即将开始：显示购票按钮 -->
                  <template v-else-if="group === '即将开始'">
                    <a
                      :href="item.url ? 'https://shop.48.cn/tickets/item/' + item.url : null"
                      target="_blank"
                      class="btn btn-sm btn-warning"
                      :class="item.url ? '' : 'disabled'"
                      :tabindex="!item.url ? -1 : null"
                      :aria-disabled="!item.url"
                    >
                      购买门票
                    </a>
                  </template>

                  <!-- 否则显示原有两个按钮 -->
                  <template v-else>
                    <button class="btn btn-sm btn-outline-dark" @click="() => openDetailModal(item)">
                      详情
                    </button>

                    <a
                      :href="item.url ? 'https://www.bilibili.com/video/' + item.url : null"
                      target="_blank"
                      class="btn btn-sm"
                      :class="item.url ? 'btn-primary' : 'btn-secondary disabled'"
                      :tabindex="!item.url ? -1 : null"
                      :aria-disabled="!item.url"
                    >
                      完整视频回放
                    </a>

                    <a
                      :href="item.cut_url ? 'https://www.bilibili.com/video/' + item.cut_url : null"
                      target="_blank"
                      class="btn btn-sm"
                      :class="item.cut_url ? 'btn-warning' : 'btn-secondary disabled'"
                      :tabindex="!item.cut_url ? -1 : null"
                      :aria-disabled="!item.cut_url"
                    >
                      小周cut视频
                    </a>
                  </template>

                  <!-- ✅ 登录后显示编辑按钮 -->
                  <template v-if="authChecked && isLoggedIn">
                    <button class="btn btn-sm btn-outline-dark" @click="() => openModal(item)">
                      编辑
                    </button>
                  </template>
                </div>
              </div>
            </li>
          </ul>
          <button
            v-if="items.length > maxInitial"
            class="btn btn-outline-primary btn-sm mb-2 d-block mx-auto"
            @click="toggleExpanded(group)"
          >
            {{ expandedGroups[group] ? '收起' : `展开全部 ${items.length} 条` }}
            <i class="fa-solid ms-1" :class="expandedGroups[group] ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
          </button>
        </template>
      </div>

      <Modal v-model="showModal" title="编辑项" @confirm="handleConfirm">
        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">时间 <span class="text-danger">*</span><br>（请输入北京时间）</label>
          <div class="col-sm-9">
            <input v-model="tempItem.date" type="datetime-local" class="form-control" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">场次 <span class="text-danger">*</span><br>（如果没有场次或不确定，请填写0）</label>
          <div class="col-sm-9">
            <input v-model="tempItem.session" type="number" class="form-control" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">标题 <span class="text-danger">*</span></label>
          <div class="col-sm-9">
            <input v-model="tempItem.title" type="text" class="form-control" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">队伍 <span class="text-danger">*</span></label>
          <div class="col-sm-9">
            <select v-model="tempItem.type" class="form-select">
              <option disabled value="">请选择队伍</option>
              <option value="Team SII">Team SII</option>
              <option value="11">1&1 Anyone 公演队</option>
              <option value="New Members">新生公演队</option>
              <option value="Team NII">Team NII</option>
              <option value="Team HII">Team HII</option>
              <option value="Team X">Team X</option>
              <option value="Others">其它（特殊公演或非公演）</option>
            </select>
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">公演类别 <span class="text-danger">*</span></label>
          <div class="col-sm-9">
            <select v-model="tempItem.stage_code" class="form-select">
              <option disabled value="">请选择公演类别</option>
              <option value="MX">命运的X号</option>
              <option value="HJ-B">幻镜-B版</option>
              <option value="XII">代号XII 2.0</option>
              <option value="HJ-C">幻镜-C版</option>
              <option value="ITL">INTO THE LIGHT</option>
              <option value="11">1&amp;1 Anyone</option>
              <option value="48Hz">48Hz</option>
              <option value="SJHS">三角函数</option>
              <option value="FX">Fire X</option>
              <option value="SP">其它（特殊公演或非公演）</option>
            </select>
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">演出地点</label>
          <div class="col-sm-9">
            <input
              v-model="tempItem.time"
              type="text"
              class="form-control"
              placeholder="SNH48剧场可留空；已支持剧场请填写代号（如 GNZ）"
              list="venue-options"
            />
            <datalist id="venue-options">
              <option value="SNH">SNH48星梦剧院</option>
              <option value="BEJ">BEJ48壹空间</option>
              <option value="GNZ">GNZ48星梦剧院</option>
              <option value="CKG">CKG48星梦剧院</option>
              <option value="CGT">CGT48星梦剧院</option>
              <option value="HZ">杭州星梦空间（无直播）</option>
              <option value="NA">其它剧场（无直播）</option>
            </datalist>
            <small class="text-muted d-block mt-1">可自行填写演出地点；自行填写的地点默认按无直播处理。</small>
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">是否已结束 <span class="text-danger">*</span></label>
          <div class="col-sm-9 text-start">
            <input v-model="tempItem.is_end" type="checkbox" class="form-check-input" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">是否为公演 <span class="text-danger">*</span></label>
          <div class="col-sm-9 text-start">
            <input v-model="tempItem.is_stage" type="checkbox" class="form-check-input" />
          </div>
        </div>

        <div class="form-group row mb-2">
          <label class="col-sm-3 col-form-label text-start">Unit</label>
          <div class="col-sm-9">
            <div
              v-for="(unitItem, unitIndex) in tempItem.unit"
              :key="`unit-${unitIndex}`"
              class="border rounded p-2 mb-2"
              :class="dragOverUnitIndex === unitIndex ? 'border-primary bg-light' : ''"
              @dragover.prevent="handleUnitDragOver(unitIndex)"
              @drop.prevent="handleUnitDrop(unitIndex)"
            >
              <div class="d-flex justify-content-between align-items-center mb-2">
                <small class="text-muted">第 {{ unitIndex + 1 }} 条</small>
                <span
                  class="text-muted small"
                  draggable="true"
                  style="cursor: grab; user-select: none;"
                  @dragstart="handleUnitDragStart(unitIndex)"
                  @dragend="handleUnitDragEnd"
                >
                  拖动排序
                </span>
              </div>

              <div class="row gx-2 gy-2 align-items-center mb-2 mx-0">
                <div class="col-md-5 px-1">
                  <label class="form-label mb-1">Unit歌曲名 <span class="text-danger">*</span></label>
                  <input
                    v-model="unitItem.name"
                    type="text"
                    class="form-control form-control-sm"
                    placeholder="可选默认曲目或自行填写"
                    list="unit-song-options"
                  />
                </div>
                <div class="col-md-3 px-1">
                  <label class="form-label mb-1">站位 <span class="text-danger">*</span></label>
                  <input v-model="unitItem.pos" type="text" class="form-control form-control-sm" placeholder="常规unit填站位数字，助演unit填被助演成员名" />
                </div>
                <div class="col-md-4 px-1">
                  <label class="form-label mb-1">类型 <span class="text-danger">*</span></label>
                  <select v-model="unitItem.type" class="form-select form-select-sm">
                    <option
                      v-for="option in unitTypeOptions"
                      :key="option.value"
                      :value="option.value"
                    >
                      {{ option.label }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="d-flex justify-content-end gap-2 flex-wrap">
                <button
                  type="button"
                  class="btn btn-outline-secondary btn-sm"
                  :disabled="unitIndex === 0"
                  @click="moveUnitItemUp(unitIndex)"
                >
                  上移
                </button>
                <button
                  type="button"
                  class="btn btn-outline-secondary btn-sm"
                  :disabled="unitIndex === tempItem.unit.length - 1"
                  @click="moveUnitItemDown(unitIndex)"
                >
                  下移
                </button>
                <button type="button" class="btn btn-outline-danger btn-sm" @click="removeUnitItem(unitIndex)">
                  删除该条
                </button>
              </div>
            </div>

            <datalist id="unit-song-options">
              <option
                v-for="song in getUnitSongOptions(tempItem.stage_code)"
                :key="song"
                :value="song"
              />
            </datalist>

            <div class="d-flex flex-column flex-md-row gap-2 justify-content-between align-items-start align-items-md-center mt-2">
              <small class="text-muted text-break">Unit歌曲名可从默认选项中选择，也可自行填写；类型只能选择给定项；支持拖动排序，也可用上移/下移按钮排序。</small>
              <button type="button" class="btn btn-outline-primary btn-sm" @click="addUnitItem">
                + 添加 Unit
              </button>
            </div>
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">完整视频回放<br>（请输入SNH48在b站官号发布的公演视频回放bv号）</label>
          <div class="col-sm-9">
            <input v-model="tempItem.url" type="text" class="form-control" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">小周cut视频<br>（请输入应援会在b站发布的小周cut视频bv号）</label>
          <div class="col-sm-9">
            <input v-model="tempItem.cut_url" type="text" class="form-control" />
          </div>
        </div>
        <!-- 你可以放任何 slot 内容，甚至是编辑表单 -->
      </Modal>

      <Modal v-model="showDetailModal" title="公演详情" cancel-text="关闭" :show-confirm="false">
        <div v-if="detailItem" class="detail">
          <!-- 头部：场次 + 标题 -->
          <header class="detail-hero" :class="{ 'has-logo': getStageLogo(detailItem.stage_code) }">
            <div class="detail-hero-text">
            <div class="detail-badges">
              <span class="detail-session">
                {{ detailItem.session !== '0' ? `第 ${detailItem.session} 场` : '不计入场次' }}
              </span>
              <span v-if="detailItem.stage_code" class="detail-chip">
                {{ getStageCodeLabel(detailItem.stage_code) }}
              </span>
            </div>
            <h4 class="detail-title">{{ splitTitle(detailItem.title).mainLines[0] || '-' }}</h4>
            <p
              v-for="(line, lineIndex) in splitTitle(detailItem.title).mainLines.slice(1)"
              :key="`detail-title-main-${lineIndex}`"
              class="detail-subtitle"
            >
              {{ line }}
            </p>
            <p v-if="splitTitle(detailItem.title).note" class="detail-note">
              <i class="fa-solid fa-circle-info me-1"></i>
              <template v-for="(line, lineIndex) in splitTitle(detailItem.title).noteLines" :key="`detail-title-note-${lineIndex}`">
                <span>{{ line }}</span>
                <br v-if="lineIndex < splitTitle(detailItem.title).noteLines.length - 1" />
              </template>
            </p>
            </div>
            <img
              v-if="getStageLogo(detailItem.stage_code)"
              :src="getStageLogo(detailItem.stage_code)"
              :alt="`${getStageCodeLabel(detailItem.stage_code)} logo`"
              class="detail-logo"
              decoding="async"
            />
          </header>

          <!-- 基本信息 -->
          <dl class="detail-info">
            <div class="info-item">
              <dt><i class="fa-regular fa-calendar"></i>时间</dt>
              <dd><ZonedDateTime :datetime="detailItem.date" format="YYYY-MM-DD HH:mm" /></dd>
            </div>
            <div class="info-item">
              <dt><i class="fa-solid fa-location-dot"></i>地点</dt>
              <dd>{{ getVenueLabel(detailItem.time) }}</dd>
            </div>
            <div class="info-item">
              <dt><i class="fa-solid fa-user-group"></i>队伍</dt>
              <dd>{{ getTypeLabel(detailItem.type) }}</dd>
            </div>
          </dl>

          <!-- Unit 列表 -->
          <section class="detail-section">
            <h5 class="section-title">
              <i class="fa-solid fa-music"></i>Unit 表演
              <span v-if="detailItem.unit.length" class="section-count">{{ detailItem.unit.length }}</span>
            </h5>
            <ol v-if="detailItem.unit.length" class="unit-list">
              <li
                v-for="(unitItem, unitIndex) in detailItem.unit.map(getUnitDetail)"
                :key="`detail-unit-${unitIndex}`"
                class="unit-row"
              >
                <span class="unit-index">{{ unitIndex + 1 }}</span>
                <span class="unit-name">{{ unitItem.name }}</span>
                <span class="unit-tags">
                  <span v-if="unitItem.posLabel" class="unit-tag" :class="`pos-${unitItem.posKind}`">
                    {{ unitItem.posLabel }}
                  </span>
                  <span class="unit-tag" :class="`type-${unitItem.type}`">{{ unitItem.typeLabel }}</span>
                </span>
              </li>
            </ol>
            <p v-else class="detail-empty">暂无 Unit 记录</p>
          </section>

          <!-- 视频 -->
          <section class="detail-section">
            <h5 class="section-title"><i class="fa-solid fa-circle-play"></i>视频</h5>
            <div class="video-links">
              <component
                :is="detailItem.url ? 'a' : 'div'"
                :href="detailItem.url ? 'https://www.bilibili.com/video/' + detailItem.url : undefined"
                target="_blank"
                rel="noopener"
                class="video-card video-replay"
                :class="{ 'is-disabled': !detailItem.url }"
              >
                <span class="video-icon"><i class="fa-solid fa-film"></i></span>
                <span class="video-text">
                  <strong>完整视频回放</strong>
                  <small>{{ detailItem.url || '暂无回放' }}</small>
                </span>
                <i v-if="detailItem.url" class="fa-solid fa-arrow-up-right-from-square video-arrow"></i>
              </component>

              <component
                :is="detailItem.cut_url ? 'a' : 'div'"
                :href="detailItem.cut_url ? 'https://www.bilibili.com/video/' + detailItem.cut_url : undefined"
                target="_blank"
                rel="noopener"
                class="video-card video-cut"
                :class="{ 'is-disabled': !detailItem.cut_url }"
              >
                <span class="video-icon"><i class="fa-solid fa-star"></i></span>
                <span class="video-text">
                  <strong>小周cut视频</strong>
                  <small>{{ detailItem.cut_url || '暂无cut' }}</small>
                </span>
                <i v-if="detailItem.cut_url" class="fa-solid fa-arrow-up-right-from-square video-arrow"></i>
              </component>
            </div>
          </section>
        </div>
      </Modal>
  </div>
</template>

<style scoped>
.stage-guide {
  max-width: 880px;
  margin: 0 auto 16px;
  padding: 0;
  overflow: hidden;
}

.stage-guide summary {
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
}

.stage-guide summary::-webkit-details-marker {
  display: none;
}

.guide-chevron {
  font-size: 12px;
  color: var(--c-text-3);
  transition: transform 0.2s ease;
}

.stage-guide[open] .guide-chevron {
  transform: rotate(180deg);
}

.guide-list {
  list-style: none;
  margin: 0;
  padding: 4px 20px 0;
  border-top: 1px solid var(--c-border);
}

.guide-list li {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 10px 0;
  color: var(--c-text-2);
  font-size: 14px;
}

.guide-tag {
  flex-shrink: 0;
  min-width: 96px;
  text-align: center;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}

.tag-live { background: #dcfce7; color: #15803d; }
.tag-replay { background: #ece9f7; color: var(--c-ink); }
.tag-cut { background: var(--c-accent-soft); color: var(--c-accent-ink); }
.tag-off { background: var(--c-surface-2); color: var(--c-text-3); }

.guide-note {
  margin: 0;
  padding: 4px 20px 16px;
  font-size: 13px;
  color: var(--c-text-3);
}

.tz-warning {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  max-width: 880px;
  margin: 0 auto 16px;
  padding: 12px 18px;
  border-radius: var(--radius-md);
  background: #fff7ed;
  border: 1px solid #fed7aa;
  color: #9a3412;
  font-size: 14px;
}

.tz-warning i {
  margin-top: 4px;
}

.filter-card {
  max-width: 880px;
  margin: 0 auto 8px;
  padding: 20px;
}

.filter-title {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
}

.filter-hint {
  margin: 6px 0 16px;
  font-size: 13px;
  color: var(--c-text-2);
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.filter-wide {
  grid-column: span 2;
}

.filter-field {
  position: relative;
}

.field-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 13px;
  color: var(--c-text-3);
  pointer-events: none;
}

.with-icon {
  padding-left: 34px;
}

.filter-actions {
  display: flex;
  gap: 8px;
  grid-column: span 2;
}

.filter-actions .btn {
  flex: 1;
}

.stage-groups {
  max-width: 1000px;
  margin: 0 auto;
}

.stage-loading {
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

.stage-list {
  gap: 10px;
  --bs-list-group-border-width: 0;
}

.stage-list .list-group-item {
  border: 1px solid var(--c-border) !important;
  border-radius: var(--radius-md) !important;
  background: var(--c-surface);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}

.stage-list .list-group-item:hover {
  border-color: var(--c-border-strong) !important;
  box-shadow: var(--shadow-md);
}

.stage-meta {
  min-width: 120px;
  padding-right: 4px;
  flex-shrink: 0;
  white-space: nowrap;
}

.stage-session {
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  color: var(--c-text);
}

.stage-meta :deep(*) {
  font-size: 13px;
}

.stage-title-col {
  min-width: 0;
  word-break: break-word;
}

.stage-actions .btn {
  white-space: nowrap;
}

.stage-actions {
  flex-shrink: 0;
  flex-wrap: nowrap;
}

@media (max-width: 767.98px) {
  .stage-actions {
    flex-wrap: wrap;
  }
}

.stage-title {
  font-weight: 600;
  color: var(--c-text);
}

/* ---------- 详情弹框 ---------- */
.detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-hero {
  position: relative;
  padding: 20px 22px;
  border-radius: var(--radius-md);
  background:
    radial-gradient(120% 140% at 100% 0%, rgba(242, 183, 5, 0.22), transparent 55%),
    linear-gradient(135deg, var(--c-accent-soft), var(--c-surface-2));
  border: 1px solid rgba(242, 183, 5, 0.25);
  overflow: hidden;
}

.detail-hero.has-logo {
  display: flex;
  align-items: center;
  gap: 16px;
}

.detail-hero-text {
  flex: 1 1 auto;
  min-width: 0;
}

.detail-logo {
  flex-shrink: 0;
  width: 150px;
  height: 100px;
  object-fit: contain;
  margin: -8px -6px -8px 0;
  filter: drop-shadow(0 4px 10px rgba(28, 25, 23, 0.12));
}

.detail-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.detail-session {
  padding: 3px 12px;
  border-radius: 999px;
  background: var(--c-ink);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.detail-chip {
  padding: 3px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.75);
  color: var(--c-accent-ink);
  border: 1px solid rgba(242, 183, 5, 0.35);
  font-size: 13px;
  font-weight: 700;
}

.detail-title {
  margin: 0;
  font-size: 20px;
  font-weight: 800;
  line-height: 1.4;
  color: var(--c-text);
  word-break: break-word;
}

.detail-subtitle {
  margin: 4px 0 0;
  font-size: 14px;
  color: var(--c-text-2);
}

.detail-note {
  margin: 10px 0 0;
  font-size: 12px;
  color: var(--c-text-2);
}

.detail-info {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin: 0;
}

.info-item {
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  background: var(--c-surface-2);
  min-width: 0;
}

.info-item dt {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
  font-size: 12px;
  font-weight: 600;
  color: var(--c-text-3);
}

.info-item dd {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--c-text);
  font-variant-numeric: tabular-nums;
  word-break: break-word;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 10px;
  font-size: 15px;
  font-weight: 800;
}

.section-title > i {
  color: var(--c-accent-strong);
}

.section-count {
  padding: 0 8px;
  border-radius: 999px;
  background: var(--c-surface-2);
  color: var(--c-text-2);
  font-size: 12px;
  font-weight: 700;
}

.unit-list {
  list-style: none;
  margin: 0;
  padding: 0;
  border: 1px solid var(--c-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.unit-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
}

.unit-row + .unit-row {
  border-top: 1px solid var(--c-border);
}

.unit-row:hover {
  background: var(--c-surface-2);
}

.unit-index {
  flex-shrink: 0;
  width: 26px;
  height: 26px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--c-accent-soft);
  color: var(--c-accent-ink);
  font-size: 12px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.unit-name {
  flex: 1 1 auto;
  min-width: 0;
  font-weight: 600;
  word-break: break-word;
}

.unit-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 6px;
  flex-shrink: 0;
  max-width: 55%;
}

.unit-tag {
  padding: 2px 9px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  background: var(--c-surface-2);
  color: var(--c-text-2);
}

.unit-tag.pos-pos { background: #ece9f7; color: var(--c-ink); }
.unit-tag.pos-solo { background: var(--c-ink); color: #fff; }
.unit-tag.pos-support { background: #e0f2fe; color: #0369a1; white-space: normal; }

.unit-tag.type-birthday { background: #fce7f3; color: #be185d; }
.unit-tag.type-graduation { background: #f3e8ff; color: #7e22ce; }
.unit-tag.type-mvp,
.unit-tag.type-todaymvp,
.unit-tag.type-b50 { background: var(--c-accent-soft); color: var(--c-accent-ink); }
.unit-tag.type-yueyaoqu,
.unit-tag.type-election { background: #dcfce7; color: #15803d; }
.unit-tag.type-encore { background: #ffedd5; color: #c2410c; }

.detail-empty {
  margin: 0;
  padding: 14px;
  border-radius: var(--radius-md);
  border: 1px dashed var(--c-border-strong);
  text-align: center;
  font-size: 14px;
  color: var(--c-text-3);
}

.video-links {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.video-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--c-border);
  background: var(--c-surface);
  color: var(--c-text);
  text-decoration: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

a.video-card:hover {
  border-color: var(--c-border-strong);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
  color: var(--c-text);
}

.video-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-size: 16px;
}

.video-replay .video-icon { background: var(--c-ink); color: #fff; }
.video-cut .video-icon { background: var(--c-accent); color: var(--c-ink); }

.video-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.video-text strong {
  font-size: 14px;
}

.video-text small {
  font-size: 12px;
  color: var(--c-text-3);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.video-arrow {
  font-size: 12px;
  color: var(--c-text-3);
}

.video-card.is-disabled {
  background: var(--c-surface-2);
  cursor: not-allowed;
}

.video-card.is-disabled .video-icon {
  background: var(--c-border-strong);
  color: #fff;
}

.video-card.is-disabled strong {
  color: var(--c-text-3);
}

@media (max-width: 576px) {
  .detail-hero {
    padding: 16px;
  }

  .detail-title {
    font-size: 18px;
  }

  .detail-logo {
    width: 96px;
    height: 64px;
    margin: 0;
  }

  .detail-info {
    grid-template-columns: 1fr 1fr;
  }

  .detail-info .info-item:first-child {
    grid-column: 1 / -1;
  }

  .video-links {
    grid-template-columns: 1fr;
  }

  .unit-row {
    flex-wrap: wrap;
    row-gap: 6px;
  }

  .unit-tags {
    max-width: none;
    width: 100%;
    justify-content: flex-start;
    padding-left: 38px;
  }
}

@media (min-width: 768px) {
  .stage-meta {
    border-right: 1px solid var(--c-border);
    padding-right: 16px;
  }
}

@media (max-width: 768px) {
  .filter-grid {
    grid-template-columns: 1fr 1fr;
  }

  .filter-wide,
  .filter-actions {
    grid-column: 1 / -1;
  }

  .guide-list li {
    flex-direction: column;
    gap: 6px;
  }

  .group-title {
    font-size: 18px;
  }
}
</style>
