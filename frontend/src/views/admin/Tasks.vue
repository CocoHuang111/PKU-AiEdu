<template>
  <div class="page">
    <h1>任务管理</h1>
    <div class="toolbar">
      <el-select v-model="kind" style="width: 140px" @change="load">
        <el-option label="视频评估" value="eval" />
        <el-option label="大纲优化" value="syllabus" />
      </el-select>
      <el-select v-model="status" clearable placeholder="状态" style="width: 140px" @change="load">
        <el-option v-for="s in statuses" :key="s" :label="s" :value="s" />
      </el-select>
    </div>
    <el-table :data="items" v-loading="loading">
      <el-table-column prop="filename" label="文件" />
      <el-table-column prop="status" label="状态" width="110" />
      <el-table-column prop="current_step" label="当前步骤" width="140" />
      <el-table-column prop="error" label="错误摘要" />
      <el-table-column prop="user_id" label="用户" width="280" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'queued' || row.status === 'processing'"
            text
            type="primary"
            @click="cancel(row)"
          >
            取消
          </el-button>
          <el-button
            v-if="row.status === 'failed' || row.status === 'cancelled'"
            text
            type="danger"
            @click="cleanup(row)"
          >
            清理
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="pager"
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      v-model:current-page="page"
      @current-change="load"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { adminApi } from '../../api/client'

const statuses = ['queued', 'processing', 'completed', 'failed', 'cancelled']
const kind = ref('eval')
const status = ref('')
const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const data = await adminApi.tasks({
      kind: kind.value,
      status: status.value || undefined,
      page: page.value,
      page_size: pageSize,
    })
    items.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function cancel(row) {
  await adminApi.cancelTask(kind.value, row.id)
  ElMessage.success('已请求取消')
  load()
}

async function cleanup(row) {
  await adminApi.cleanupTask(kind.value, row.id)
  ElMessage.success('已清理')
  load()
}

onMounted(load)
</script>

<style scoped>
.page { max-width: 1200px; margin: 0 auto; }
.toolbar { display: flex; gap: 8px; margin: 12px 0 16px; }
.pager { margin-top: 16px; }
</style>
