<template>
  <div class="page" v-loading="loading">
    <h1>概览</h1>
    <div class="cards">
      <el-card v-for="item in cards" :key="item.label" shadow="never">
        <div class="num">{{ item.value }}</div>
        <div class="label">{{ item.label }}</div>
      </el-card>
    </div>
    <h2>最近失败的评估任务</h2>
    <el-table :data="data.recent_errors || []" empty-text="暂无">
      <el-table-column prop="filename" label="文件" />
      <el-table-column prop="error" label="错误摘要" />
      <el-table-column prop="user_id" label="用户" width="280" />
    </el-table>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { adminApi } from '../../api/client'

const loading = ref(false)
const data = ref({
  users: {},
  eval_tasks: {},
  syllabus_tasks: {},
  storage_bytes: 0,
  recent_errors: [],
})

const cards = computed(() => {
  const users = data.value.users || {}
  const evals = data.value.eval_tasks || {}
  return [
    { label: '用户总数', value: users.total || 0 },
    { label: '近 7 日新增', value: users.new_7d || 0 },
    { label: '24 小时登录', value: users.recent_login_24h || 0 },
    { label: '近期 Session', value: users.active_sessions_24h || 0 },
    { label: '评估排队', value: evals.queued || 0 },
    { label: '评估运行', value: evals.processing || 0 },
    { label: '评估成功', value: evals.completed || 0 },
    { label: '评估失败', value: evals.failed || 0 },
    { label: '存储占用 (MB)', value: Math.round((data.value.storage_bytes || 0) / 1024 / 1024) },
  ]
})

onMounted(async () => {
  loading.value = true
  try {
    data.value = await adminApi.overview()
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page { max-width: 1100px; margin: 0 auto; }
h1 { margin: 0 0 16px; }
h2 { margin: 28px 0 12px; font-size: 16px; }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.num { font-size: 28px; font-weight: 700; color: #7b1113; }
.label { color: #909399; margin-top: 4px; }
</style>
