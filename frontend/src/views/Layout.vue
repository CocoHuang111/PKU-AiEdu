<template>
  <el-container class="shell" direction="vertical">
    <header class="nav">
      <div class="brand">
        北大问教
        <span>PKU-AskEdu 2.0</span>
      </div>
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
    </header>

      <el-main class="main" :class="{ flush: $route.path === '/qa' || $route.path === '/evaluation' }">
        <router-view />
      </el-main>
  </el-container>
</template>

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
  display: flex;
  align-items: baseline;
  gap: 8px;
}
.brand span {
  font-size: 11px;
  font-weight: 400;
  letter-spacing: 0.5px;
  color: rgba(255, 255, 255, 0.55);
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
