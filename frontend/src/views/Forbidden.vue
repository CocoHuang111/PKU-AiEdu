<template>
  <div class="page">
    <h1>没有管理员权限</h1>
    <p>这个页面只给后台管理员使用。如果你认为这是误判，请联系已有管理员。</p>
    <el-button type="primary" @click="$router.replace('/qa')">回到问答</el-button>
  </div>
</template>

<style scoped>
.page {
  max-width: 520px;
  margin: 80px auto;
  padding: 32px;
  background: #fff;
  border: 1px solid #e8eaed;
  border-radius: 10px;
}
h1 {
  margin: 0 0 12px;
  font-size: 22px;
}
p {
  color: #606266;
  line-height: 1.6;
}
</style>
