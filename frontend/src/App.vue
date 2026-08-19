<template>
  <router-view />
</template>

<style>
/* ── 北大红主题：覆盖 Element Plus 的 CSS 变量 ───────────────────────── */
:root {
  --pku-red: #a61b1b;
  --pku-red-dark: #7b1113;
  --pku-red-darker: #891616;

  --el-color-primary: #a61b1b;
  --el-color-primary-dark-2: #891616;
  --el-color-primary-light-3: #bf6161;
  --el-color-primary-light-5: #d28d8d;
  --el-color-primary-light-7: #e0b5b5;
  --el-color-primary-light-8: #eac9c9;
  --el-color-primary-light-9: #f5e6e6;

  --el-border-radius-base: 6px;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  height: 100%;
  margin: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #f5f7fa;
  color: #303133;
}

.el-button--primary:hover,
.el-button--primary:focus {
  background-color: #891616 !important;
  border-color: #891616 !important;
}
.el-button--primary:active {
  background-color: #7b1010 !important;
  border-color: #7b1010 !important;
}

.el-tag {
  --el-tag-bg-color: #f5e6e6;
  --el-tag-border-color: #e0b5b5;
  --el-tag-text-color: #a61b1b;
}

/* 全局滚动条 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-thumb {
  background: #d0d3d9;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #b8bcc4;
}
::-webkit-scrollbar-track {
  background: transparent;
}
</style>
