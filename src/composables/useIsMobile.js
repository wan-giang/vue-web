import { ref } from 'vue'

// 与旧版侧边栏逻辑保持一致：窄屏或横屏手机都视为移动端
const query = () => window.innerWidth < 768 || window.innerHeight < 500

const isMobile = ref(query())
let listening = false

export function useIsMobile() {
  if (!listening) {
    window.addEventListener('resize', () => {
      isMobile.value = query()
    })
    listening = true
  }

  return { isMobile }
}
