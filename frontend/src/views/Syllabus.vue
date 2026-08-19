<template>
  <div class="layout">
    <!-- 输入区 -->
    <el-card shadow="never" class="card">
      <template #header>
        <span class="card-title">上传教学大纲 — 解析并生成结构化的优化大纲</span>
      </template>

      <div class="mode-row">
        <span class="mode-label">优化模式</span>
        <el-radio-group v-model="promptMode" size="small" class="mode-group">
          <el-radio-button value="adaptive">灵活结构 · XML</el-radio-button>
          <el-radio-button value="schema">固定框架 · XML</el-radio-button>
          <el-radio-button value="markdown">灵活结构 · Markdown</el-radio-button>
          <el-radio-button value="markdown_schema">固定框架 · Markdown</el-radio-button>
        </el-radio-group>
      </div>

      <el-tabs v-model="tab">
        <el-tab-pane label="上传文档" name="file">
          <el-upload
            drag
            :auto-upload="false"
            :show-file-list="false"
            :disabled="!!busyTask || submitting"
            accept=".pdf,.docx,.doc,.txt,.md"
            :on-change="handleFile"
          >
            <div class="upload-inner">
              <div class="upload-icon">📘</div>
              <div class="upload-text">拖入大纲文档或点击选择</div>
              <div class="upload-hint">支持 PDF / Word(docx, doc) / Markdown / 纯文本</div>
            </div>
          </el-upload>
        </el-tab-pane>

        <el-tab-pane label="粘贴文本" name="text">
          <el-input
            v-model="text"
            type="textarea"
            :rows="10"
            placeholder="把大纲内容粘贴到这里…"
          />
          <el-button
            type="primary"
            :loading="submitting"
            :disabled="text.trim().length < 10 || !!busyTask"
            style="margin-top: 12px"
            @click="runText"
          >
            开始优化
          </el-button>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 进行中的任务 -->
    <el-card v-if="activeTask" shadow="never" class="card task-card">
      <template #header>
        <div class="result-header">
          <span class="card-title">优化进度</span>
          <el-button
            v-if="activeTask.status === 'processing' || activeTask.status === 'queued'"
            type="danger"
            size="small"
            plain
            :loading="cancelling"
            @click="cancelActiveTask"
          >
            停止
          </el-button>
        </div>
      </template>
      <div class="task-filename">{{ activeTask.filename }}</div>
      <div class="task-status-row">
        <el-tag :type="statusType(activeTask.status)" size="small">
          {{ statusText(activeTask.status) }}
        </el-tag>
        <span class="task-step">{{ activeTask.step_label }}{{ stepDetail(activeTask) }}</span>
      </div>
      <el-progress
        :percentage="activeTask.progress"
        :stroke-width="10"
        :status="progressStatus(activeTask.status)"
        style="margin-top: 12px"
      />
      <div v-if="activeTask.error" class="task-error">{{ activeTask.error }}</div>
      <div v-else-if="activeTask.status === 'processing' || activeTask.status === 'queued'" class="task-hint">
        {{ loadingHint }}
      </div>
    </el-card>

    <!-- 结果区 -->
    <el-card v-if="result" shadow="never" class="card">
      <template #header>
        <div class="result-header">
          <span class="card-title">{{ result.course_name }}</span>
          <div class="result-actions">
            <el-tag v-if="result.valid" type="success" size="small">
              {{ isMarkdownOutput ? 'Markdown 校验通过' : 'XML 校验通过' }}
            </el-tag>
            <el-tag v-else type="danger" size="small">
              {{ isMarkdownOutput ? 'Markdown 校验失败' : 'XML 校验失败' }}
            </el-tag>
            <el-tag v-if="result.repair_attempts" type="warning" size="small">
              自动修复 {{ result.repair_attempts }} 次
            </el-tag>
            <el-tag v-if="result.truncated" type="warning" size="small">原文超长已截断</el-tag>
            <el-tag
              v-if="isMarkdownOutput && result.output_char_count"
              type="info"
              size="small"
            >
              {{ result.output_char_count }} / {{ result.max_output_chars || '—' }} 字
            </el-tag>
            <el-tag v-if="result.prompt_mode" type="info" size="small">
              {{ modeLabel(result.prompt_mode) }}
            </el-tag>
            <el-button size="small" @click="copyOutput">
              复制{{ isMarkdownOutput ? ' Markdown' : ' XML' }}
            </el-button>
            <el-button size="small" @click="downloadOutput">
              下载{{ isMarkdownOutput ? ' Markdown' : ' XML' }}
            </el-button>
            <el-dropdown
              trigger="click"
              :disabled="!result.valid || !result.id"
              @command="exportAs"
            >
              <el-button size="small" type="primary" :disabled="!result.valid || !result.id">
                导出 ▾
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-if="!isMarkdownOutput" command="markdown">
                    Markdown (.md)
                  </el-dropdown-item>
                  <el-dropdown-item command="docx">Word (.docx)</el-dropdown-item>
                  <el-dropdown-item command="pdf">PDF (.pdf)</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </template>

      <el-alert
        v-if="!result.valid"
        type="error"
        :closable="false"
        :title="validationAlertTitle(result.validation_error)"
        style="margin-bottom: 12px"
      />
      <el-alert
        v-else-if="result.validation_error"
        type="warning"
        :closable="false"
        :title="result.validation_error"
        style="margin-bottom: 12px"
      />

      <div class="compare">
        <div class="pane">
          <div class="pane-head">原始大纲</div>
          <pre class="pane-body original">{{ result.original_text }}</pre>
        </div>
        <div class="pane">
          <div class="pane-head">优化后大纲（{{ isMarkdownOutput ? 'Markdown' : 'XML' }}）</div>
          <pre v-if="!isMarkdownOutput" class="pane-body xml" v-html="highlight(result.xml)"></pre>
          <div v-else class="pane-body markdown" v-html="renderMd(result.xml)"></div>
        </div>
      </div>
    </el-card>

    <!-- 历史 -->
    <el-card shadow="never" class="card">
      <template #header>
        <div class="result-header">
          <span class="card-title">历史记录</span>
          <el-button text size="small" @click="loadHistory">刷新</el-button>
        </div>
      </template>
      <div v-if="!history.length" class="empty-hint">暂无记录</div>
      <el-table v-else :data="history" size="small" border @row-click="openRecord">
        <el-table-column prop="course_name" label="课程名称" />
        <el-table-column prop="filename" label="来源文件" width="220" />
        <el-table-column label="校验" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.valid ? 'success' : 'danger'" size="small">
              {{ row.valid ? '通过' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="时间" width="160">
          <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import DOMPurify from 'dompurify'
import { marked } from 'marked'
import { syllabusApi } from '../api/client'

const POLL_INTERVAL = 2500

const tab = ref('file')
const text = ref('')
const promptMode = ref('adaptive')
const submitting = ref(false)
const cancelling = ref(false)
const activeTask = ref(null)
const result = ref(null)
const history = ref([])
let pollTimer = null

const busyTask = computed(
  () =>
    activeTask.value &&
    (activeTask.value.status === 'processing' || activeTask.value.status === 'queued')
)

const isMarkdownOutput = computed(() => {
  if (!result.value) return promptMode.value.startsWith('markdown')
  if (result.value.output_format) return result.value.output_format === 'markdown'
  const content = (result.value.xml || '').trimStart()
  return content.startsWith('#') || !content.startsWith('<')
})

const loadingHint = computed(() => {
  if (promptMode.value === 'schema') {
    return '固定框架单轮生成较长 XML，可能需要 5–10 分钟；可离开页面，进度会自动刷新。'
  }
  if (promptMode.value === 'markdown_schema') {
    return '固定框架 Markdown 生成内容较长，可能需要 3–8 分钟；可离开页面，进度会自动刷新。'
  }
  if (promptMode.value === 'markdown') {
    return 'Markdown 模式通常 30 秒到 3 分钟；可离开页面，进度会自动刷新。'
  }
  return '通常 30 秒到 2 分钟；可离开页面，进度会自动刷新。'
})

function statusType(status) {
  return (
    { completed: 'success', processing: 'warning', failed: 'danger', cancelled: 'info' }[
      status
    ] || 'info'
  )
}

function statusText(status) {
  return (
    { completed: '已完成', processing: '处理中', failed: '失败', queued: '排队中', cancelled: '已停止' }[
      status
    ] || status
  )
}

function progressStatus(status) {
  if (status === 'completed') return 'success'
  if (status === 'failed') return 'exception'
  return undefined
}

function stepDetail(task) {
  const detail = task?.step_detail || {}
  if (task?.current_step === 'repairing' && detail.attempt) {
    return `（第 ${detail.attempt} 次）`
  }
  if (task?.current_step === 'parsing' && detail.filename) {
    return `（${detail.filename}）`
  }
  return ''
}

function schedulePoll() {
  clearTimeout(pollTimer)
  const busy =
    activeTask.value &&
    (activeTask.value.status === 'processing' || activeTask.value.status === 'queued')
  if (busy) pollTimer = setTimeout(refreshActiveTask, POLL_INTERVAL)
}

async function refreshActiveTask() {
  if (!activeTask.value?.id) return
  const before = activeTask.value.status
  try {
    const task = await syllabusApi.getTask(activeTask.value.id)
    activeTask.value = task
    if (before !== 'completed' && task.status === 'completed' && task.result) {
      result.value = {
        ...task.result,
        validation_error: task.result.validation_error || '',
      }
      ElMessage.success('优化完成')
      loadHistory()
    } else if (task.status === 'failed') {
      ElMessage.error(task.error || '优化失败')
    } else if (task.status === 'cancelled') {
      ElMessage.info('已停止优化')
    }
  } catch {
    /* 拦截器已提示 */
  } finally {
    schedulePoll()
  }
}

async function startTask(payload) {
  activeTask.value = {
    id: payload.task_id,
    filename: payload.filename,
    status: payload.status || 'queued',
    progress: 0,
    current_step: 'queued',
    step_label: '排队中',
    step_detail: {},
  }
  result.value = null
  schedulePoll()
  await refreshActiveTask()
}

async function cancelActiveTask() {
  if (!activeTask.value?.id) return
  cancelling.value = true
  try {
    await syllabusApi.cancelTask(activeTask.value.id)
    ElMessage.success('已请求停止')
    await refreshActiveTask()
  } catch {
    /* 拦截器已提示 */
  } finally {
    cancelling.value = false
  }
}

function modeLabel(mode) {
  if (
    mode === 'syllabus_optimize_schema.j2' ||
    mode === 'schema' ||
    mode === 'syllabus_optimize_markdown_schema.j2' ||
    mode === 'markdown_schema'
  ) {
    return mode.includes('markdown') || mode === 'markdown_schema'
      ? '固定框架 · Markdown'
      : '固定框架 · XML'
  }
  if (
    mode === 'syllabus_optimize_markdown.j2' ||
    mode === 'markdown' ||
    mode === 'markdown_adaptive'
  ) {
    return '灵活结构 · Markdown'
  }
  return '灵活结构 · XML'
}

function renderMd(text) {
  return DOMPurify.sanitize(marked.parse(text || ''))
}

function formatTime(ts) {
  return new Date(ts * 1000).toLocaleString('zh-CN')
}

function validationAlertTitle(error) {
  if (!error) return '校验未通过'
  if (/xmlParse|XML 语法|XML 无法解析|invalid element/i.test(error)) {
    return error.startsWith('XML') ? error : `XML 语法错误：${error}`
  }
  return `校验未通过：${error}`
}

/** 极轻量的 XML 高亮：标签、属性名、属性值分别着色 */
function highlight(xml) {
  const escaped = xml
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
  return escaped
    .replace(/(&lt;\/?)([\w-]+)/g, '$1<span class="tag">$2</span>')
    .replace(/([\w-]+)=(&quot;|")([^"&]*)\2/g, '<span class="attr">$1</span>=<span class="val">"$3"</span>')
}

async function handleFile(file) {
  submitting.value = true
  try {
    const payload = await syllabusApi.optimizeFile(file.raw, promptMode.value)
    await startTask(payload)
  } catch {
    /* 拦截器已提示 */
  } finally {
    submitting.value = false
  }
}

async function runText() {
  submitting.value = true
  try {
    const payload = await syllabusApi.optimizeText(text.value, promptMode.value)
    await startTask(payload)
  } catch {
    /* 拦截器已提示 */
  } finally {
    submitting.value = false
  }
}

async function copyOutput() {
  await navigator.clipboard.writeText(result.value.xml)
  ElMessage.success('已复制到剪贴板')
}

function downloadOutput() {
  if (result.value?.id) {
    const a = document.createElement('a')
    a.href = syllabusApi.downloadUrl(result.value.id)
    a.click()
    return
  }
  const markdown = isMarkdownOutput.value
  const blob = new Blob([result.value.xml], {
    type: markdown ? 'text/markdown;charset=utf-8' : 'application/xml;charset=utf-8',
  })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${result.value.course_name || 'syllabus'}.${markdown ? 'md' : 'xml'}`
  a.click()
  URL.revokeObjectURL(url)
}

function exportAs(format) {
  if (!result.value?.id) {
    ElMessage.warning('请先完成优化后再导出')
    return
  }
  if (!result.value.valid) {
    ElMessage.warning(`${isMarkdownOutput.value ? 'Markdown' : 'XML'} 校验未通过，无法导出`)
    return
  }
  const a = document.createElement('a')
  a.href = syllabusApi.exportUrl(result.value.id, format)
  a.rel = 'noopener'
  a.click()
  ElMessage.success(`正在下载 ${format.toUpperCase()}…`)
}

async function loadHistory() {
  try {
    history.value = await syllabusApi.history()
  } catch {
    /* 拦截器已提示 */
  }
}

async function openRecord(row) {
  try {
    const record = await syllabusApi.getRecord(row.id)
    result.value = {
      ...record,
      valid: !!record.valid,
      repair_attempts: 0,
      truncated: false,
      validation_error: '',
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch {
    /* 拦截器已提示 */
  }
}

onMounted(loadHistory)
onUnmounted(() => clearTimeout(pollTimer))
</script>

<style scoped>
.card {
  margin-bottom: 16px;
  border: 1px solid #e8eaed;
}
.card-title {
  font-size: 14px;
  font-weight: 600;
}

.mode-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 14px;
}
.mode-label {
  font-size: 13px;
  color: #606266;
  font-weight: 500;
}

.mode-group {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
}

.upload-inner {
  padding: 26px 8px;
}
.upload-icon {
  font-size: 34px;
}
.upload-text {
  margin-top: 8px;
  font-size: 14px;
  color: #303133;
}
.upload-hint {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.task-card {
  border-color: #e6a23c33;
}
.task-filename {
  font-size: 13px;
  color: #303133;
  font-weight: 500;
}
.task-status-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
  flex-wrap: wrap;
}
.task-step {
  font-size: 13px;
  color: #606266;
}
.task-hint {
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
}
.task-error {
  margin-top: 10px;
  font-size: 12px;
  color: #f56c6c;
}

.loading-tip {
  margin-top: 12px;
  padding: 10px 14px;
  background: #fdf6ec;
  border-radius: 5px;
  font-size: 13px;
  color: #e6a23c;
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}
.result-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.compare {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
@media (max-width: 1100px) {
  .compare {
    grid-template-columns: 1fr;
  }
}
.pane {
  border: 1px solid #ebeef5;
  border-radius: 5px;
  overflow: hidden;
}
.pane-head {
  padding: 8px 12px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
  font-size: 13px;
  font-weight: 600;
  color: #606266;
}
.pane-body {
  margin: 0;
  padding: 14px;
  max-height: 620px;
  overflow: auto;
  font-size: 12.5px;
  line-height: 1.75;
  white-space: pre-wrap;
  word-break: break-word;
}
.pane-body.original {
  color: #606266;
  font-family: -apple-system, 'PingFang SC', sans-serif;
}
.pane-body.xml {
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  background: #fcfcfd;
  color: #303133;
}
.pane-body.xml :deep(.tag) {
  color: #a61b1b;
  font-weight: 600;
}
.pane-body.xml :deep(.attr) {
  color: #2f6f9f;
}
.pane-body.xml :deep(.val) {
  color: #67804a;
}

.pane-body.markdown {
  font-family: -apple-system, 'PingFang SC', sans-serif;
  background: #fcfcfd;
  color: #303133;
  white-space: normal;
}
.pane-body.markdown :deep(h1),
.pane-body.markdown :deep(h2),
.pane-body.markdown :deep(h3),
.pane-body.markdown :deep(h4) {
  margin: 1em 0 0.5em;
  line-height: 1.4;
}
.pane-body.markdown :deep(h1:first-child),
.pane-body.markdown :deep(h2:first-child) {
  margin-top: 0;
}
.pane-body.markdown :deep(p),
.pane-body.markdown :deep(li) {
  margin: 0.4em 0;
}
.pane-body.markdown :deep(ul),
.pane-body.markdown :deep(ol) {
  padding-left: 1.4em;
}
.pane-body.markdown :deep(blockquote) {
  margin: 0.6em 0;
  padding-left: 12px;
  border-left: 3px solid #dcdfe6;
  color: #606266;
}

.empty-hint {
  color: #909399;
  font-size: 13px;
  text-align: center;
  padding: 16px 0;
}
</style>
