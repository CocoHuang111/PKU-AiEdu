<template>
  <el-container class="shell">
    <el-aside width="220px" class="side">
      <div class="brand">
        北大问教
        <span>PKU-AskEdu 2.0</span>
      </div>
      <el-menu :default-active="$route.path" router class="menu">
        <el-menu-item index="/evaluation">🎬&nbsp; 教学视频评估</el-menu-item>
        <el-menu-item index="/syllabus">📘&nbsp; 教学大纲优化</el-menu-item>
        <el-menu-item index="/qa">🎓&nbsp; 教学智能问答</el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <span class="title">{{ $route.meta.title || '智能教学支持系统' }}</span>
        <span class="status">
          <el-tag v-if="health" size="small" :type="health.mode === 'cloud' ? '' : 'warning'">
            {{ health.mode === 'cloud' ? '云端 LLM' : '本地 LLM' }} · {{ health.llm_model }}
          </el-tag>
          <el-tag v-if="health" size="small" type="info">ASR 本地</el-tag>
          <el-tag v-else size="small" type="info">后端未连接</el-tag>
        </span>
      </el-header>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { healthApi } from '../api/client'

const health = ref(null)

onMounted(async () => {
  try {
    health.value = await healthApi.check()
  } catch {
    health.value = null
  }
})
</script>

<style scoped>
.shell {
  height: 100vh;
}

.side {
  background: #7b1113;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.brand {
  padding: 22px 20px 18px;
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 1px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}
.brand span {
  display: block;
  font-size: 11px;
  font-weight: 400;
  letter-spacing: 0.5px;
  color: rgba(255, 255, 255, 0.55);
  margin-top: 4px;
}

.menu {
  background: transparent;
  border-right: none;
  padding-top: 8px;
}
.menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.82);
  font-size: 14px;
  height: 48px;
}
.menu :deep(.el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.menu :deep(.el-menu-item.is-active) {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  font-weight: 600;
}

.header {
  height: 56px;
  background: #fff;
  border-bottom: 1px solid #e6e8eb;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.main {
  padding: 16px;
  background: #f5f7fa;
  overflow-y: auto;
}
</style>
