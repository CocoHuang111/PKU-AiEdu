<template>
  <el-container class="shell" direction="vertical">
    <header class="nav">
      <div class="brand">北大问教</div>
      <div class="nav-right">
        <el-menu
          :default-active="$route.path"
          :ellipsis="false"
          router
          mode="horizontal"
          class="menu"
        >
          <el-menu-item index="/qa">智能问答</el-menu-item>
          <el-menu-item index="/evaluation">教学评估</el-menu-item>
          <el-menu-item index="/syllabus">大纲优化</el-menu-item>
          <el-menu-item index="/profile">我的</el-menu-item>
        </el-menu>
        <div class="who">
          <router-link v-if="isAdmin()" class="admin-link" to="/admin">后台</router-link>
          <el-button class="logout" text @click="onLogout">退出</el-button>
        </div>
      </div>
    </header>

      <el-main class="main" :class="{ flush: $route.path === '/qa' || $route.path === '/evaluation' || $route.path === '/syllabus' }">
        <router-view v-slot="{ Component }">
          <keep-alive include="QA">
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </el-main>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { authApi } from '../api/client'
import { clearAuth, isAdmin } from '../authStore'
import { resetQa } from '../qaStore'

const router = useRouter()

async function onLogout() {
  try {
    await authApi.logout()
  } catch {
    /* 本地清掉即可 */
  }
  clearAuth()
  resetQa()
  router.replace('/login')
}
</script>

<style scoped>
.shell {
  height: 100vh;
}

.nav {
  height: 56px;
  flex-shrink: 0;
  background: #7b1113;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.brand {
  flex-shrink: 0;
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 1px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 0;
}
.who {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: 8px;
  flex-shrink: 0;
}
.admin-link {
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
  text-decoration: none;
  margin-right: 8px;
}
.admin-link:hover {
  color: #fff;
}
.logout {
  color: rgba(255, 255, 255, 0.72) !important;
  padding: 0 8px;
}
.logout:hover {
  color: #fff !important;
}

.menu {
  flex: 0 0 auto;
  width: auto;
  background: transparent;
  border-bottom: none;
  height: 56px;
  --el-menu-bg-color: transparent;
  --el-menu-hover-bg-color: transparent;
  --el-menu-text-color: rgba(255, 255, 255, 0.78);
  --el-menu-hover-text-color: #fff;
  --el-menu-active-color: #fff;
}
.menu :deep(.el-menu-item) {
  height: 56px;
  line-height: 56px;
  font-size: 14px;
  border-bottom: 2px solid transparent !important;
  padding: 0 18px;
  overflow: visible;
}
.menu :deep(.el-menu-item:hover) {
  background: transparent;
}
.menu :deep(.el-menu-item.is-active) {
  background: transparent !important;
  font-weight: 600;
  border-bottom-color: #fff !important;
}

.main {
  padding: 16px;
  background: #f5f7fa;
  overflow-y: auto;
}
.main.flush {
  padding: 0;
  overflow: hidden;
  background: #fff;
}
</style>
