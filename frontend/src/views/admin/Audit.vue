<template>
  <div class="page">
    <h1>审计日志</h1>
    <div class="toolbar">
      <el-input v-model="action" placeholder="操作类型" clearable @keyup.enter="load" />
      <el-input v-model="resourceType" placeholder="资源类型" clearable @keyup.enter="load" />
      <el-button type="primary" @click="load">筛选</el-button>
    </div>
    <el-table :data="items" v-loading="loading">
      <el-table-column prop="action" label="操作" width="160" />
      <el-table-column prop="resource_type" label="资源" width="140" />
      <el-table-column prop="resource_id" label="资源 ID" />
      <el-table-column prop="actor_user_id" label="操作者" />
      <el-table-column prop="ip_address" label="IP" width="140" />
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
import { adminApi } from '../../api/client'

const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const action = ref('')
const resourceType = ref('')

async function load() {
  loading.value = true
  try {
    const data = await adminApi.audit({
      action: action.value || undefined,
      resource_type: resourceType.value || undefined,
      page: page.value,
      page_size: pageSize,
    })
    items.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.page { max-width: 1200px; margin: 0 auto; }
.toolbar { display: flex; gap: 8px; margin: 12px 0 16px; width: 560px; }
.pager { margin-top: 16px; }
</style>
