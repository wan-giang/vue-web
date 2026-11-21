<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '@/composables/fetch'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'


// 引入 Pinia 状态
const auth = useAuthStore()
const { isLoggedIn } = storeToRefs(auth)  // 保持响应式
const { logout, verifyToken, startPolling, stopPolling } = auth            // 非 ref 的函数可直接解构

// 调用api
const { apiFetch } = useApi()
const router = useRouter()

const username = ref('')
const password = ref('')
const message = ref('')
const authChecked = ref(false)

// 轮询监控登录
onMounted(async () => {
  await verifyToken()
  authChecked.value = true
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})


// 登录
const login = async () => {
  message.value = ''

  if (!username.value || !password.value) {
    message.value = '请输入用户名和密码'
    return
  }

  const { ok, data } = await apiFetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  })

  if (ok) {
    isLoggedIn.value = true
    message.value = '✅ 登录成功！'
  } else {
    message.value = data.message || '❌ 登录失败'
  }
}

// 退出登录
const handleLogout = () => {
  logout()
  message.value = '👋 已成功退出登录'
}

</script>

<template>
  <div class="page login-page">


      <div class="login-card surface">
        <span class="login-icon"><i class="fa-solid fa-user-shield"></i></span>

        <template v-if="!authChecked">
          <h2 class="login-title">加载中...</h2>
        </template>

        <template v-else-if="isLoggedIn">
          <h2 class="login-title">已登录</h2>
          <p class="login-sub">欢迎回来，管理员。</p>
          <button class="btn btn-primary w-100 mt-3" @click="router.push('/admin-logs')">查看操作日志</button>
          <button class="btn btn-outline-danger w-100 mt-2" @click="handleLogout">退出登录</button>
        </template>

        <template v-else>
          <h2 class="login-title">网站管理员登录</h2>
          <p class="login-sub">仅限本站管理员使用</p>
          <form class="text-start" @submit.prevent="login">
            <input v-model="username" type="text" placeholder="用户名" autocomplete="username" class="form-control mb-2" />
            <input v-model="password" type="password" placeholder="密码" autocomplete="current-password" class="form-control mb-3" />
            <button type="submit" class="btn btn-primary w-100">登录</button>
          </form>
        </template>

        <p v-if="message" class="login-message" :class="isLoggedIn ? 'ok' : 'err'">{{ message }}</p>
      </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: calc(100vh - var(--header-h) - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 48px;
}

.login-card {
  width: min(380px, 100%);
  padding: 36px 28px 28px;
  text-align: center;
  box-shadow: var(--shadow-lg);
}

.login-icon {
  display: inline-grid;
  place-items: center;
  width: 56px;
  height: 56px;
  border-radius: 18px;
  background: var(--c-ink);
  color: var(--c-accent);
  font-size: 22px;
  margin-bottom: 16px;
}

.login-title {
  margin: 0;
  font-size: 22px;
  font-weight: 800;
}

.login-sub {
  margin: 6px 0 22px;
  color: var(--c-text-3);
  font-size: 14px;
}

.login-message {
  margin: 16px 0 0;
  padding: 8px 12px;
  border-radius: 10px;
  font-size: 14px;
}

.login-message.ok {
  background: #dcfce7;
  color: #15803d;
}

.login-message.err {
  background: #ffe4e6;
  color: #be123c;
}
</style>
