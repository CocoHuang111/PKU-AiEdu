<template>
  <div class="syllabus">
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-inner">
        <div class="drawer-head">
          <span class="drawer-title">历史任务</span>
          <button class="icon-btn" type="button" title="收起" @click="sidebarOpen = false">
            <el-icon :size="18"><DArrowLeft /></el-icon>
          </button>
        </div>
        <div class="drawer-tools">
          <el-input
            v-model="taskQuery"
            placeholder="搜索历史任务"
            :prefix-icon="Search"
            clearable
          />
          <button class="new-eval-btn" type="button" @click="newOptimization">
            <el-icon :size="16"><Plus /></el-icon>
            新建优化
          </button>
          <div class="filter-row">
            <button
              v-for="f in TASK_FILTERS"
              :key="f.key"
              type="button"
              class="filter-btn"
              :class="{ on: taskFilter === f.key }"
              @click="taskFilter = f.key"
            >
              {{ f.label }}
            </button>
          </div>
        </div>
        <div class="task-list">
          <div v-if="!tasks.length" class="empty-hint">暂无优化记录</div>
          <div v-else-if="!visibleGroups.length" class="empty-hint">没有匹配的任务</div>
          <section v-for="group in visibleGroups" :key="group.key" class="task-group">
            <div class="group-label">{{ group.label }}</div>
            <div
              v-for="t in group.items"
              :key="t.id"
              class="task"
              :class="{ active: t.id === activeId, running: isRunning(t) }"
              @click="selectTask(t.id)"
            >
              <el-icon class="task-icon" :size="18"><Document /></el-icon>
              <div class="task-body">
                <div class="task-name">{{ t.filename }}</div>
                <div class="task-notification-tags" @click.stop>
                  <el-tag size="small" :type="t.status === 'processing' ? 'warning' : 'info'">{{ statusText(t.status) }}</el-tag>
                  <el-tag size="small" :type="emailEnabled(t) ? 'success' : 'info'">{{ t.notification_status === 'sent' ? '邮件已发送' : t.notification_status === 'failed' ? '邮件发送失败' : emailEnabled(t) ? '邮件通知已开启' : '邮件通知未开启' }}</el-tag>
                  <el-switch v-if="isRunning(t)" :model-value="emailEnabled(t)" :loading="mailUpdatingIds.includes(t.id)" size="small" aria-label="邮件通知" @change="toggleTaskMail(t, $event)" />
                </div>
                <div v-if="isRunning(t)" class="task-run">
                  <span>{{ t.status === 'queued' ? '排队中' : `优化中 ${t.progress}%` }}</span>
                  <el-progress v-if="t.status !== 'queued'" :percentage="t.progress" :stroke-width="4" :show-text="false" />
                  <div class="task-meta">{{ t.step_label }}{{ stepDetail(t) }}</div>
                </div>
                <div v-else class="task-status-row">
                  <span class="task-status" :class="t.status">{{ statusText(t.status) }}</span>
                  <span class="task-time">{{ formatTime(t.created_at) }}</span>
                </div>
                <div v-if="t.error" class="task-error">{{ t.error }}</div>
              </div>
              <el-button
                v-if="isRunning(t)"
                text
                type="danger"
                size="small"
                class="task-stop"
                :loading="cancellingId === t.id"
                @click.stop="cancelTask(t.id)"
              >
                停止
              </el-button>
              <button
                class="del-btn"
                type="button"
                title="删除"
                @click.stop="removeTask(t)"
              >
                <el-icon :size="16"><Delete /></el-icon>
              </button>
            </div>
          </section>
        </div>
      </div>
    </aside>

    <div class="stage">
      <header v-if="!sidebarOpen" class="stage-top">
        <div class="top-left">
          <button class="icon-btn" type="button" title="历史任务" @click="sidebarOpen = true">
            <el-icon :size="20"><Tickets /></el-icon>
          </button>
          <button class="icon-btn" type="button" title="新建优化" @click="newOptimization">
            <el-icon :size="20"><Plus /></el-icon>
          </button>
        </div>
      </header>

      <div class="stage-body">
        <div class="workspace">
          <header class="page-head">
            <div>
              <h1>教学大纲优化</h1>
              <p>上传大纲文档，生成融合AI辅助教学的优化版本</p>
            </div>
          </header>

          <section class="compose">
            <div class="mode-row">
              <span class="mode-label">优化模式</span>
              <div class="mode-group" role="group" aria-label="优化模式">
                <button type="button" :class="{ active: promptMode === 'markdown' }"
                  :aria-pressed="promptMode === 'markdown'" @click="promptMode = 'markdown'">原文微调</button>
                <button type="button" :class="{ active: promptMode === 'markdown_schema' }"
                  :aria-pressed="promptMode === 'markdown_schema'" @click="promptMode = 'markdown_schema'">重构框架</button>
              </div>
            </div>

            <div class="file-slot">
              <div v-if="sourceFile && !reviewing" class="ready-card">
                <div class="slot-head">
                  教学大纲
                  <span class="req-tag">必填</span>
                  <div v-if="!reviewing" class="head-actions">
                    <button type="button" class="text-act" @click="pickFile">
                      <el-icon :size="14"><RefreshRight /></el-icon>
                      更换
                    </button>
                    <button type="button" class="text-act" @click="clearFile">
                      <el-icon :size="14"><Delete /></el-icon>
                      删除
                    </button>
                  </div>
                </div>
                <div class="aux-file">
                  <div class="type-badge" :class="fileKind(sourceFile).tone">
                    {{ fileKind(sourceFile).label }}
                  </div>
                  <div class="aux-copy">
                    <div class="fname">{{ sourceFile.name }}</div>
                    <div v-if="sourceFile.size" class="fmeta">{{ formatSize(sourceFile.size) }}</div>
                    <div class="ok">
                      <el-icon :size="14"><CircleCheckFilled /></el-icon>
                      已选择
                    </div>
                  </div>
                </div>
              </div>
              <div v-else-if="reviewing" class="ready-card">
                <div class="slot-head">
                  教学大纲
                  <span class="req-tag">必填</span>
                  <div v-if="activeTask && isRunning(activeTask)" class="head-actions">
                    <button
                      type="button"
                      class="text-act"
                      :disabled="cancellingId === activeTask.id"
                      @click="cancelTask(activeTask.id)"
                    >
                      停止
                    </button>
                  </div>
                </div>
                <div v-if="activeTask?.filename" class="aux-file">
                  <div class="type-badge" :class="fileKind({ name: activeTask.filename }).tone">
                    {{ fileKind({ name: activeTask.filename }).label }}
                  </div>
                  <div class="aux-copy">
                    <div class="fname">{{ activeTask.filename }}</div>
                  </div>
                </div>
                <div v-else class="empty-slot">未上传</div>
                <div v-if="activeTask" class="file-progress">
                  <el-progress
                    :percentage="activeTask.progress"
                    :stroke-width="6"
                    :show-text="false"
                    :status="progressStatus(activeTask.status)"
                  />
                  <div class="file-progress-caption" :class="{ error: !!activeTask.error }">
                    {{ progressCaption }}
                  </div>
                </div>
              </div>
              <el-upload
                v-else
                drag
                class="file-drop"
                :auto-upload="false"
                :show-file-list="false"
                :disabled="submitting"
                accept=".pdf,.docx,.doc,.txt,.md"
                :on-change="onFileChange"
              >
                <div class="slot-head">
                  教学大纲
                  <span class="req-tag">必填</span>
                </div>
                <el-icon class="drop-icon" :size="36"><Document /></el-icon>
                <div class="upload-text">
                  拖入大纲文件，或<span class="pick">点击选择</span>
                </div>
                <div class="upload-hint">支持 PDF、Word、Markdown、纯文本，单个文件不超过 50 MB</div>
              </el-upload>
            </div>

            <div v-if="!reviewing" class="compose-actions">
              <el-button @click="clearCompose" :disabled="!sourceFile">
                清空
              </el-button>
              <el-button
                type="primary"
                :loading="submitting"
                :disabled="!canStart || !!busyTask"
                @click="startOptimize"
              >
                开始优化
              </el-button>
            </div>
            <input
              ref="filePicker"
              type="file"
              accept=".pdf,.docx,.doc,.txt,.md"
              hidden
              @change="onFilePicked"
            />
          </section>

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
                        <el-dropdown-item command="markdown">Markdown (.md)</el-dropdown-item>
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  CircleCheckFilled,
  DArrowLeft,
  Delete,
  Document,
  Plus,
  RefreshRight,
  Search,
  Tickets,
} from '@element-plus/icons-vue'
import DOMPurify from 'dompurify'
import { marked } from 'marked'
import { syllabusApi } from '../api/client'
import { useRoute, useRouter } from 'vue-router'
import { showEvalQueuedFollowup } from '../evalFollowupStore'

const route = useRoute()
const router = useRouter()
const mailUpdatingIds = ref([])
function emailEnabled(task) {
  return ['pending', 'waiting_service', 'needs_email', 'sent'].includes(task.notification_status)
}
async function toggleTaskMail(task, enabled) {
  if (mailUpdatingIds.value.includes(task.id)) return
  mailUpdatingIds.value.push(task.id)
  try {
    if (enabled && !(await syllabusApi.followUp(task.id)).has_email) {
      ElMessage.info('请先完善个人资料中的邮箱')
      await router.push({ path: '/profile', query: { reportMailTask: task.id, reportMailKind: 'syllabus' } })
      return
    }
    const response = enabled ? await syllabusApi.requestEmail(task.id) : await syllabusApi.cancelEmail(task.id)
    task.notification_status = response.status
    await loadTasks()
  } catch { /* 公共拦截器显示错误 */ }
  finally { mailUpdatingIds.value = mailUpdatingIds.value.filter(id => id !== task.id) }
}

const POLL_INTERVAL = 2500
const TASK_FILTERS = [
  { key: 'all', label: '全部' },
  { key: 'running', label: '进行中' },
  { key: 'completed', label: '已完成' },
  { key: 'failed', label: '失败' },
]

const promptMode = ref('markdown')
const sourceFile = ref(null)
const filePicker = ref(null)
const submitting = ref(false)
const cancellingId = ref(null)
const tasks = ref([])
const activeId = ref(null)
const result = ref(null)
const sidebarOpen = ref(true)
const taskQuery = ref('')
const taskFilter = ref('all')
let pollTimer = null

const activeTask = computed(() => tasks.value.find((t) => t.id === activeId.value) || null)
const busyTask = computed(() => activeTask.value && isRunning(activeTask.value))
const reviewing = computed(() => Boolean(activeId.value && !submitting.value))
const canStart = computed(() => Boolean(sourceFile.value))

const isMarkdownOutput = computed(() => {
  if (!result.value) return true
  if (result.value.output_format) return result.value.output_format === 'markdown'
  const content = (result.value.xml || '').trimStart()
  return content.startsWith('#') || !content.startsWith('<')
})

const loadingHint = computed(() => {
  if (promptMode.value === 'markdown_schema') {
    return '重构框架生成较久，可离开页面，进度会自动刷新'
  }
  return '可离开页面，进度会自动刷新'
})

const progressCaption = computed(() => {
  const t = activeTask.value
  if (!t) return ''
  if (t.error) return t.error
  if (isRunning(t)) {
    const step = `${t.step_label || ''}${stepDetail(t)}`.trim()
    return step || loadingHint.value
  }
  if (t.status === 'completed') return '优化已完成'
  if (t.status === 'cancelled') return '已停止'
  return statusText(t.status)
})

const filteredTasks = computed(() => {
  const q = taskQuery.value.trim().toLowerCase()
  return tasks.value.filter((t) => {
    if (taskFilter.value === 'running' && !isRunning(t)) return false
    if (taskFilter.value === 'completed' && t.status !== 'completed') return false
    if (taskFilter.value === 'failed' && t.status !== 'failed' && t.status !== 'cancelled') {
      return false
    }
    const hay = `${t.filename || ''} ${t.summary?.course_name || ''}`.toLowerCase()
    if (q && !hay.includes(q)) return false
    return true
  })
})

const visibleGroups = computed(() => {
  const now = new Date()
  const start = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime() / 1000
  const running = []
  const today = []
  const earlier = []
  for (const t of filteredTasks.value) {
    if (isRunning(t)) running.push(t)
    else if ((t.created_at || 0) >= start) today.push(t)
    else earlier.push(t)
  }
  return [
    { key: 'running', label: '进行中', items: running },
    { key: 'today', label: '今天', items: today },
    { key: 'earlier', label: '更早', items: earlier },
  ].filter((g) => g.items.length)
})

function isRunning(t) {
  return t.status === 'processing' || t.status === 'queued'
}

function statusText(status) {
  return (
    { completed: '已完成', processing: '优化中', failed: '失败', queued: '排队中', cancelled: '已停止' }[
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

function applyResult(payload) {
  if (!payload) {
    result.value = null
    return
  }
  result.value = {
    ...payload,
    validation_error: payload.validation_error || '',
  }
}

function schedulePoll() {
  clearTimeout(pollTimer)
  const busy = tasks.value.some(isRunning)
  if (busy) pollTimer = setTimeout(refreshRunning, POLL_INTERVAL)
}

async function loadTasks() {
  try {
    tasks.value = await syllabusApi.listTasks()
    schedulePoll()
  } catch {
    /* 拦截器已提示 */
  }
}

async function refreshRunning() {
  const before = tasks.value.find((t) => t.id === activeId.value)?.status
  await loadTasks()
  const after = tasks.value.find((t) => t.id === activeId.value)
  if (activeId.value && before !== 'completed' && after?.status === 'completed') {
    await selectTask(activeId.value)
    ElMessage.success('优化完成')
  } else if (activeId.value && before !== 'failed' && after?.status === 'failed') {
    applyResult(null)
    ElMessage.error(after.error || '优化失败')
  } else if (activeId.value && before !== 'cancelled' && after?.status === 'cancelled') {
    applyResult(null)
    ElMessage.info('已停止优化')
  }
}

async function selectTask(id) {
  activeId.value = id
  sourceFile.value = null
  applyResult(null)
  try {
    const task = await syllabusApi.getTask(id)
    const idx = tasks.value.findIndex((t) => t.id === id)
    if (idx >= 0) {
      tasks.value[idx] = {
        ...tasks.value[idx],
        ...task,
        summary: tasks.value[idx].summary || {
          course_name: task.result?.course_name,
          valid: task.result?.valid,
        },
      }
    }
    if (task.status === 'completed' && task.result) {
      applyResult(task.result)
    }
  } catch {
    /* 拦截器已提示 */
  }
}

function newOptimization() {
  activeId.value = null
  result.value = null
  clearCompose()
}

function clearCompose() {
  sourceFile.value = null
}

function clearFile() {
  sourceFile.value = null
}

function pickFile() {
  filePicker.value?.click()
}

function onFileChange(file) {
  if (file?.raw) setSourceFile(file.raw)
}

function setSourceFile(file) {
  if (file.size > 50 * 1024 * 1024) {
    ElMessage.warning('大纲超过大小限制（50 MB）')
    return
  }
  sourceFile.value = file
}

function onFilePicked(ev) {
  const file = ev.target.files?.[0] || null
  ev.target.value = ''
  if (file) setSourceFile(file)
}

async function startTask(payload) {
  activeId.value = payload.task_id
  result.value = null
  await loadTasks()
  await selectTask(payload.task_id)
}

async function cancelTask(id) {
  cancellingId.value = id
  try {
    await syllabusApi.cancelTask(id)
    ElMessage.success('已请求停止')
    await loadTasks()
    if (activeId.value === id) {
      result.value = null
    }
  } catch {
    /* 拦截器已提示 */
  } finally {
    cancellingId.value = null
  }
}

async function removeTask(t) {
  const running = isRunning(t)
  try {
    await ElMessageBox.confirm(
      running ? '该任务正在优化，删除后将停止并无法恢复。确定删除？' : '确定删除这个优化任务？',
      '提示',
      { type: 'warning' }
    )
  } catch {
    return
  }
  try {
    if (running) {
      try {
        await syllabusApi.cancelTask(t.id)
      } catch {
        /* 任务可能已结束 */
      }
    }
    await syllabusApi.deleteTask(t.id)
    ElMessage.success('已删除')
    if (activeId.value === t.id) newOptimization()
    await loadTasks()
  } catch {
    /* 拦截器已提示 */
  }
}

function modeLabel(mode) {
  if (
    mode === 'syllabus_optimize_markdown_schema.j2' ||
    mode === 'markdown_schema'
  ) {
    return '重构框架'
  }
  if (
    mode === 'syllabus_optimize_markdown.j2' ||
    mode === 'markdown' ||
    mode === 'markdown_adaptive'
  ) {
    return '原文微调'
  }
  if (mode === 'syllabus_optimize_schema.j2' || mode === 'schema') {
    return '重构框架 · XML'
  }
  return mode?.includes('xml') || mode === 'adaptive' ? '原文微调 · XML' : '原文微调'
}

function fileKind(file) {
  const name = file?.name || ''
  const i = name.lastIndexOf('.')
  const ext = i >= 0 ? name.slice(i + 1).toLowerCase() : ''
  if (ext === 'pdf') return { label: 'PDF', tone: 'pdf' }
  if (ext === 'doc' || ext === 'docx') return { label: 'DOC', tone: 'doc' }
  if (ext === 'txt' || ext === 'md') return { label: ext.toUpperCase(), tone: 'txt' }
  return { label: (ext || 'FILE').toUpperCase(), tone: 'file' }
}

function formatSize(bytes) {
  if (bytes >= 1024 ** 3) return `${(bytes / 1024 ** 3).toFixed(2)} GB`
  if (bytes >= 1024 ** 2) return `${(bytes / 1024 ** 2).toFixed(1)} MB`
  if (bytes >= 1024) return `${Math.round(bytes / 1024)} KB`
  return `${bytes} B`
}

function renderMd(text) {
  return DOMPurify.sanitize(marked.parse(text || ''))
}

function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts * 1000).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
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

async function startOptimize() {
  if (!canStart.value || busyTask.value) return
  submitting.value = true
  try {
    const payload = await syllabusApi.optimizeFile(sourceFile.value, promptMode.value)
    await startTask(payload)
    void showEvalQueuedFollowup(payload.task_id, { kind: 'syllabus', desktop: false })
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

onMounted(async () => {
  await loadTasks()
  if (typeof route.query.task === 'string' && /^[0-9a-f-]{36}$/i.test(route.query.task)) {
    await selectTask(route.query.task)
    if (route.query.submitted === '1') void showEvalQueuedFollowup(route.query.task, { kind: 'syllabus', desktop: false })
  }
})
onUnmounted(() => clearTimeout(pollTimer))
</script>

<style scoped>
.task-notification-tags { display: flex; align-items: center; flex-wrap: wrap; gap: 5px; margin: 6px 0; }
.syllabus {
  height: calc(100vh - 56px);
  display: flex;
  background: #fff;
  overflow: hidden;
}

.sidebar {
  width: 0;
  flex-shrink: 0;
  overflow: hidden;
  background: #f7f7f8;
  border-right: 1px solid transparent;
  transition: width 0.2s ease, border-color 0.2s ease;
}
.sidebar.open {
  width: 300px;
  border-right-color: #ececec;
}
.sidebar-inner {
  width: 300px;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.drawer-head {
  height: 56px;
  padding: 0 8px 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #303133;
  flex-shrink: 0;
}
.drawer-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.02em;
  line-height: 1.2;
  color: #7b1113;
  position: relative;
  padding-left: 10px;
}
.drawer-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 4px;
  bottom: 4px;
  width: 3px;
  border-radius: 2px;
  background: #a61b1b;
}
.drawer-tools {
  padding: 0 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-shrink: 0;
}
.new-eval-btn {
  height: 36px;
  border: 1px solid #a61b1b;
  background: #fff;
  color: #a61b1b;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
}
.new-eval-btn:hover {
  background: #fdf4f4;
}
.filter-row {
  display: flex;
  gap: 4px;
}
.filter-btn {
  flex: 1;
  height: 28px;
  border: none;
  background: transparent;
  color: #8a8a8a;
  font-size: 13px;
  cursor: pointer;
  border-radius: 6px;
}
.filter-btn.on,
.filter-btn:hover {
  color: #a61b1b;
  background: #f5e6e6;
}

.stage {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.stage-top {
  height: 52px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
}
.top-left {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-shrink: 0;
}
.icon-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: 8px;
  color: #4b4b4b;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.icon-btn:hover {
  background: #f3f3f3;
}

.stage-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.workspace {
  width: 100%;
  max-width: 992px;
  margin: 0 auto;
  padding: 32px 56px 48px;
  box-sizing: border-box;
}

.page-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ececec;
  margin-bottom: 20px;
}
.page-head h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1f1f1f;
}
.page-head p {
  margin: 8px 0 0;
  font-size: 14px;
  color: #8a8a8a;
}

.task-list {
  flex: 1;
  overflow-y: auto;
  padding: 4px 8px 16px;
}

.empty-hint {
  color: #909399;
  font-size: 13px;
  text-align: center;
  padding: 24px 0;
}
.task-group + .task-group {
  margin-top: 8px;
}
.group-label {
  font-size: 12px;
  font-weight: 600;
  color: #8a8a8a;
  letter-spacing: 0.08em;
  padding: 8px 8px 4px;
}
.task {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 8px;
  border-top: 1px solid #ececec;
  cursor: pointer;
}
.task:hover {
  background: #ececed;
}
.task.active {
  background: #f5e6e6;
}
.task.active .task-name {
  color: #7b1113;
}
.task-icon {
  flex-shrink: 0;
  margin-top: 2px;
  color: #8a8a8a;
}
.task.active .task-icon,
.task.running .task-icon {
  color: #a61b1b;
}
.task-body {
  min-width: 0;
  flex: 1;
}
.task-name {
  font-size: 13px;
  color: #303133;
  letter-spacing: 0.02em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.task-stop {
  flex-shrink: 0;
}
.del-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  border-radius: 6px;
  color: #909399;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.del-btn:hover {
  background: #fff;
  color: #c45656;
}
.task-status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: 4px;
}
.task-status {
  font-size: 12px;
  color: #8a8a8a;
}
.task-status.completed {
  color: #2e8b57;
}
.task-status.failed,
.task-status.cancelled {
  color: #f56c6c;
}
.task-time {
  font-size: 11px;
  color: #a8abb2;
}
.task-run {
  margin-top: 6px;
  font-size: 12px;
  color: #a61b1b;
}
.task-meta {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
.task-error {
  font-size: 12px;
  color: #f56c6c;
  margin-top: 4px;
  word-break: break-all;
}

.card {
  margin-bottom: 16px;
  border: 1px solid #e8eaed;
}
.card-title {
  font-size: 14px;
  font-weight: 600;
}

.compose {
  padding-top: 4px;
  margin-bottom: 24px;
}
.mode-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 18px;
}
.mode-label {
  font-size: 16px;
  color: #303133;
  font-weight: 600;
}
.mode-group {
  display: inline-flex;
  gap: 4px;
  padding: 3px;
  border-radius: 8px;
  background: #f3f4f6;
}
.mode-group button {
  padding: 7px 18px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #606266;
  cursor: pointer;
  font-size: 13px;
  white-space: nowrap;
}
.mode-group button.active {
  background: #fff;
  color: #a61b1b;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  font-weight: 600;
}

.file-slot {
  margin-top: 8px;
}
.ready-card {
  border: 1px solid #e6e6e6;
  border-radius: 10px;
  background: #fff;
  padding: 14px 16px 16px;
}
.slot-head {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
}
.req-tag {
  margin-left: 8px;
  font-size: 11px;
  font-weight: 600;
  padding: 1px 8px;
  border-radius: 10px;
  line-height: 18px;
  color: #a61b1b;
  background: #fff;
  border: 1px solid #a61b1b;
}
.head-actions {
  margin-left: auto;
  display: flex;
  gap: 14px;
}
.text-act {
  border: none;
  background: transparent;
  color: #606266;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  padding: 0;
}
.text-act:hover {
  color: #a61b1b;
}
.aux-file {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  width: 100%;
  margin-top: 14px;
}
.type-badge {
  width: 44px;
  height: 52px;
  border-radius: 6px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
}
.type-badge.pdf {
  background: #c0392b;
}
.type-badge.doc {
  background: #2b579a;
}
.type-badge.txt,
.type-badge.file {
  background: #6b7280;
}
.aux-copy {
  min-width: 0;
  flex: 1;
}
.fname {
  font-size: 15px;
  font-weight: 600;
  color: #1f1f1f;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.fmeta {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}
.ok {
  margin-top: 6px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #2e8b57;
  font-size: 13px;
}
.empty-slot {
  color: #c0c4cc;
  font-size: 13px;
  text-align: center;
  padding: 24px 0 16px;
}

.file-drop :deep(.el-upload),
.file-drop :deep(.el-upload-dragger) {
  width: 100%;
}
.file-drop :deep(.el-upload-dragger) {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 14px 20px 28px;
  border: 1px dashed #d8d8d8;
  border-radius: 10px;
  background: #fff;
}
.file-drop :deep(.el-upload-dragger:hover) {
  border-color: #a61b1b;
}
.file-drop .slot-head {
  align-self: flex-start;
  margin-bottom: 18px;
}
.drop-icon {
  color: #a61b1b;
}
.upload-text {
  margin-top: 8px;
  font-size: 14px;
  color: #303133;
}
.upload-text .pick {
  color: #a61b1b;
  text-decoration: underline;
  text-underline-offset: 2px;
}
.upload-hint {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.compose-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.file-progress {
  margin-top: 14px;
}
.file-progress-caption {
  margin-top: 6px;
  font-size: 12px;
  line-height: 1.4;
  color: #909399;
}
.file-progress-caption.error {
  color: #f56c6c;
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
</style>
