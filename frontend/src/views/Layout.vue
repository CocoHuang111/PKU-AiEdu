<template>
  <el-container class="shell" direction="vertical">
    <el-dialog
      v-model="followupVisible"
      title="视频已加入评估队列"
      width="min(540px, 92vw)"
      append-to-body
      align-center
      @closed="closeFollowup"
    >
      <p>上传已完成，视频已进入评估流程。{{ estimateText }}</p>
      <p class="eval-followup-hint">预计时间仅供参考，视频时长及服务器负载会影响实际耗时。关闭标签页不会停止已入队的解析，进度可在历史任务中查看。</p>
      <p>是否在报告完成后发送邮件通知？</p>
      <p v-if="mailStatus === 'waiting_service'" class="eval-followup-hint">通知申请已保存；邮件服务尚未配置，暂不能发送。报告仍可在系统内查看。</p>
      <p v-else-if="mailStatus === 'pending'">已开启完成邮件通知。</p>
      <p v-else-if="mailStatus === 'sent'">报告通知已发送。</p>
      <el-button v-if="!['pending', 'sent', 'waiting_service'].includes(mailStatus)" :loading="mailSaving" @click="enableReportMail">是，完成后通知我</el-button>
      <el-button v-if="!['pending', 'sent', 'waiting_service'].includes(mailStatus)" @click="mailDeclined = true">{{ mailDeclined ? '已选择暂不需要' : '暂不需要' }}</el-button>
      <p>等待期间，是否先试试其他教学功能？</p>
      <el-button type="primary" @click="goToFeature('/qa')">前往智能问答</el-button>
      <el-button @click="goToFeature('/syllabus')">前往大纲优化</el-button>
      <template #footer>
        <el-button type="primary" @click="stayOnEvaluation">查看评估进度</el-button>
      </template>
    </el-dialog>
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
          <keep-alive include="QA,Evaluation">
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </el-main>
  </el-container>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api/client'
import { clearAuth, isAdmin } from '../authStore'
import { resetQa } from '../qaStore'
import {
  closeFollowup,
  enableReportMail,
  estimateText,
  followupVisible,
  goToFeature,
  mailDeclined,
  mailSaving,
  mailStatus,
  restorePendingFollowup,
  stayOnEvaluation,
} from '../evalFollowupStore'

const router = useRouter()

onMounted(() => {
  restorePendingFollowup()
})

async function onLogout() {
  closeFollowup()
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

<style>
.eval-followup-hint {
  color: #909399;
  font-size: 13px;
  line-height: 1.6;
}
</style>
