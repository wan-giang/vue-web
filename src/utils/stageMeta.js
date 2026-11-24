// 公演代码 → 公演名 / logo，供 Stages.vue 与 Units.vue 共用
const stageCodeLabelMap = {
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

const stageLogoMap = {
  'HJ-B': 'hj_lg.png',
  'HJ-C': 'hj_lg.png',
  MX: 'mx_lg.png',
  XII: 'xii_lg.png',
  ITL: 'itl_lg.png',
  '11': '11_lg.png',
  '48Hz': '48hz_lg.png'
}

export const getStageCodeLabel = (stageCode) =>
  stageCodeLabelMap[stageCode] || stageCode || '-'

export const getStageLogo = (stageCode) => {
  const file = stageLogoMap[String(stageCode || '').trim()]
  return file ? `${import.meta.env.BASE_URL}lg/${file}` : ''
}

// public 目录下的图片路径（或完整 http 链接）→ 可用的 src
export const resolvePublicImg = (img) => {
  const value = String(img || '').trim()
  if (!value) return ''
  if (/^(https?:)?\/\//.test(value) || value.startsWith('data:')) return value
  return `${import.meta.env.BASE_URL}${value.replace(/^\/+/, '')}`
}

export const BILIBILI_VIDEO_BASE = 'https://www.bilibili.com/video/'
