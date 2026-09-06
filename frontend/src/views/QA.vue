<template>
  <div class="qa">
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-inner">
        <div class="drawer-head">
          <span class="drawer-title">历史会话</span>
          <button class="icon-btn" type="button" title="收起" @click="sidebarOpen = false">
            <el-icon :size="18"><DArrowLeft /></el-icon>
          </button>
        </div>
        <div class="drawer-tools">
          <el-input
            v-model="sessionQuery"
            placeholder="搜索历史会话"
            :prefix-icon="Search"
            clearable
          />
          <button class="new-eval-btn" type="button" @click="newSession">
            <el-icon :size="16"><Plus /></el-icon>
            新对话
          </button>
        </div>
        <div class="task-list">
          <div v-if="!sessions.length" class="empty-hint">还没有会话</div>
          <div v-else-if="!visibleGroups.length" class="empty-hint">没有匹配的会话</div>
          <section v-for="group in visibleGroups" :key="group.key" class="task-group">
            <div class="group-label">{{ group.label }}</div>
            <div
              v-for="s in group.items"
              :key="s.id"
              class="task"
              :class="{ active: s.id === sessionId, pinned: s.pinned }"
              @click="openSession(s.id)"
            >
              <el-icon class="task-icon" :size="18"><ChatDotRound /></el-icon>
              <div class="task-body">
                <div class="task-name">{{ s.title }}</div>
                <div class="task-status-row">
                  <span class="task-time">{{ formatTime(s.updated_at) }}</span>
                </div>
              </div>
              <el-dropdown
                trigger="click"
                @command="(cmd) => onSessionCommand(s, cmd)"
                @click.stop
              >
                <button class="more-btn" type="button" title="更多" @click.stop>
                  <el-icon :size="16"><MoreFilled /></el-icon>
                </button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="rename">重命名</el-dropdown-item>
                    <el-dropdown-item command="pin">
                      {{ s.pinned ? '取消置顶' : '置顶' }}
                    </el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </section>
        </div>
      </div>
    </aside>

    <div class="stage">
      <header class="chat-top">
        <div class="top-left">
          <template v-if="!sidebarOpen">
            <button
              class="icon-btn"
              type="button"
              title="历史会话"
              @click="sidebarOpen = true"
            >
              <el-icon :size="20"><ChatLineRound /></el-icon>
            </button>
            <button class="icon-btn" type="button" title="新对话" @click="newSession">
              <el-icon :size="20"><Plus /></el-icon>
            </button>
          </template>
        </div>
        <div class="top-heading">
          <div class="top-title">{{ currentTitle }}</div>
          <el-dropdown
            v-if="sessionId"
            trigger="click"
            @command="(cmd) => onCurrentCommand(cmd)"
          >
            <button class="more-btn header-more" type="button" title="更多">
              <el-icon :size="16"><MoreFilled /></el-icon>
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="rename">重命名</el-dropdown-item>
                <el-dropdown-item command="pin">
                  {{ currentPinned ? '取消置顶' : '置顶' }}
                </el-dropdown-item>
                <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <section class="chat">
        <div ref="bodyEl" class="chat-body">
          <div v-if="!messages.length" class="chat-empty">
            <h1>有什么教学问题？</h1>
            <p>基于教育学理论、教学沙龙记录与你的历史评估报告来回答。</p>
            <div class="samples">
              <button
                v-for="q in SAMPLES"
                :key="q"
                type="button"
                class="sample"
                @click="useSample(q)"
              >
                {{ q }}
              </button>
            </div>
          </div>

          <div v-else class="thread">
            <div v-for="(m, i) in messages" :key="i" class="msg" :class="m.role">
              <div v-if="m.role === 'user'" class="bubble user">{{ m.content }}</div>
              <div v-else class="assistant">
                <div v-if="m.plan" class="plan">
                  <span class="plan-label">检索</span>
                  <el-tag v-for="q in m.plan.queries" :key="q" size="small" effect="plain">
                    {{ q }}
                  </el-tag>
                  <el-tag
                    v-for="c in m.plan.corpora"
                    :key="c"
                    size="small"
                    type="info"
                    effect="plain"
                  >
                    {{ corpusLabel(c) }}
                  </el-tag>
                </div>

                <div v-if="m.content" class="markdown" v-html="renderMd(m.content)"></div>
                <span v-if="m.streaming" class="stream-status">
                  <span v-if="m.thinking" class="thinking">思考中<span class="dots"></span></span>
                  <span class="cursor">▋</span>
                </span>

                <el-collapse v-if="m.citations?.length" class="citations">
                  <el-collapse-item :title="`来源（${m.citations.length}）`" name="c">
                    <div v-for="c in m.citations" :key="c.index" class="citation">
                      <div class="citation-head">
                        <el-tag size="small" effect="plain">[{{ c.index }}]</el-tag>
                        <span class="citation-corpus">{{ c.corpus_label }}</span>
                        <span class="citation-source">{{ c.source }}</span>
                        <span class="citation-score">相似度 {{ c.score }}</span>
                      </div>
                      <div class="citation-text">{{ c.snippet }}</div>
                    </div>
                  </el-collapse-item>
                </el-collapse>
              </div>
            </div>
          </div>
        </div>

        <footer class="composer-wrap">
          <div class="composer">
            <div class="composer-box">
              <el-popover placement="top-start" :width="280" trigger="click">
                <template #reference>
                  <button
                    class="plus-btn"
                    type="button"
                    :class="{ active: corporaNarrowed }"
                    title="检索范围"
                  >
                    <el-icon :size="18"><Plus /></el-icon>
                  </button>
                </template>
                <div class="corpus-menu">
                  <div class="corpus-menu-title">检索范围</div>
                  <el-checkbox-group v-model="selectedCorpora">
                    <el-checkbox
                      v-for="c in corpora"
                      :key="c.name"
                      :value="c.name"
                      :disabled="!c.count"
                    >
                      {{ c.label }}（{{ c.count }}）
                    </el-checkbox>
                  </el-checkbox-group>
                  <div class="corpus-hint">默认全选。取消勾选则不检索该库。</div>
                </div>
              </el-popover>
              <el-input
                v-model="input"
                type="textarea"
                :autosize="{ minRows: 1, maxRows: 6 }"
                resize="none"
                placeholder="问任何教学相关的问题"
                @keydown.enter.exact.prevent="send"
              />
              <el-button
                class="send-btn"
                type="primary"
                circle
                :loading="sending"
                :disabled="!input.trim()"
                @click="send"
              >
                <el-icon v-if="!sending" :size="16"><Promotion /></el-icon>
              </el-button>
            </div>
            <div class="composer-hint">Enter 发送，Shift+Enter 换行</div>
          </div>
        </footer>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { ChatDotRound, ChatLineRound, DArrowLeft, MoreFilled, Plus, Promotion, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { qaApi } from '../api/client'
import { askStream } from '../api/stream'

const SAMPLES = [
  '如何提高大班课的学生参与度？',
  '教学目标怎么写才算可测量？',
  '课堂提问后应该等待多久？',
  '板书和课件应该怎么分工？',
]

const sessions = ref([])
const sessionId = ref(null)
const messages = ref([])
const corpora = ref([])
const selectedCorpora = ref([])
const input = ref('')
const sending = ref(false)
const sidebarOpen = ref(true)
const sessionQuery = ref('')
const bodyEl = ref(null)

const currentTitle = computed(() => {
  if (!sessionId.value) return '新对话'
  return sessions.value.find((s) => s.id === sessionId.value)?.title || '对话'
})

const currentPinned = computed(() => {
  return !!sessions.value.find((s) => s.id === sessionId.value)?.pinned
})

const visibleGroups = computed(() => {
  const q = sessionQuery.value.trim().toLowerCase()
  const filtered = sessions.value.filter((s) => {
    if (q && !(s.title || '').toLowerCase().includes(q)) return false
    return true
  })
  const pinned = filtered.filter((s) => s.pinned)
  const recent = filtered.filter((s) => !s.pinned)
  return [
    { key: 'pinned', label: '置顶', items: pinned },
    { key: 'recent', label: '最近', items: recent },
  ].filter((g) => g.items.length)
})

const selectableNames = computed(() =>
  corpora.value.filter((c) => c.count).map((c) => c.name)
)
const corporaNarrowed = computed(() => {
  const all = selectableNames.value
  if (!all.length) return false
  return all.length !== selectedCorpora.value.length || all.some((n) => !selectedCorpora.value.includes(n))
})

function renderMd(text) {
  return DOMPurify.sanitize(marked.parse(text || ''))
}
function corpusLabel(name) {
  return corpora.value.find((c) => c.name === name)?.label || name
}
function formatTime(ts) {
  return new Date(ts * 1000).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

async function scrollDown() {
  await nextTick()
  if (bodyEl.value) bodyEl.value.scrollTop = bodyEl.value.scrollHeight
}

async function loadSessions() {
  try {
    sessions.value = await qaApi.sessions()
  } catch {
    /* 拦截器已提示 */
  }
}

async function loadCorpora() {
  try {
    corpora.value = await qaApi.corpora()
    selectedCorpora.value = corpora.value.filter((c) => c.count).map((c) => c.name)
  } catch {
    /* 拦截器已提示 */
  }
}

function newSession() {
  sessionId.value = null
  messages.value = []
}

async function openSession(id) {
  try {
    const s = await qaApi.getSession(id)
    sessionId.value = id
    messages.value = s.history.map((m) => ({ ...m, streaming: false }))
    scrollDown()
  } catch {
    /* 拦截器已提示 */
  }
}

async function removeSession(id) {
  try {
    await ElMessageBox.confirm('确定删除这个会话？', '提示', { type: 'warning' })
  } catch {
    return
  }
  await qaApi.deleteSession(id)
  if (sessionId.value === id) newSession()
  loadSessions()
}

async function renameSession(id) {
  const current = sessions.value.find((s) => s.id === id)?.title || ''
  let name
  try {
    const { value } = await ElMessageBox.prompt('请输入新的会话名称', '重命名', {
      confirmButtonText: '保存',
      cancelButtonText: '取消',
      inputValue: current,
      inputPattern: /\S/,
      inputErrorMessage: '名称不能为空',
    })
    name = (value || '').trim()
  } catch {
    return
  }
  if (!name) return
  await qaApi.patchSession(id, { title: name.slice(0, 80) })
  await loadSessions()
}

async function togglePin(id, pinned) {
  await qaApi.patchSession(id, { pinned })
  await loadSessions()
}

function onSessionCommand(s, cmd) {
  if (cmd === 'rename') renameSession(s.id)
  else if (cmd === 'pin') togglePin(s.id, !s.pinned)
  else if (cmd === 'delete') removeSession(s.id)
}

function onCurrentCommand(cmd) {
  const s = sessions.value.find((item) => item.id === sessionId.value)
  if (!s) return
  onSessionCommand(s, cmd)
}

function useSample(q) {
  input.value = q
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

function createLineRevealer(reply) {
  let committed = ''
  let pending = ''
  const queue = []
  let running = false

  function paint() {
    reply.content = committed + pending
    reply.thinking = !reply.content
    scrollDown()
  }

  async function run() {
    if (running) return
    running = true
    while (queue.length) {
      committed += queue.shift()
      paint()
      if (queue.length) await sleep(queue.length > 12 ? 16 : 40)
    }
    running = false
  }

  return {
    push(text) {
      pending += text
      const parts = pending.split('\n')
      pending = parts.pop() ?? ''
      if (parts.length) {
        for (const line of parts) queue.push(`${line}\n`)
        run()
      }
      paint()
    },
    async flush() {
      if (pending) {
        queue.push(pending)
        pending = ''
      }
      while (queue.length || running) {
        await run()
        if (!queue.length) break
        await sleep(8)
      }
      paint()
    },
  }
}

async function send() {
  const question = input.value.trim()
  if (!question || sending.value) return

  input.value = ''
  sending.value = true
  messages.value.push({ role: 'user', content: question })

  const reply = {
    role: 'assistant',
    content: '',
    citations: [],
    plan: null,
    streaming: true,
    thinking: true,
  }
  messages.value.push(reply)
  const reveal = createLineRevealer(reply)
  scrollDown()

  try {
    await askStream(
      { question, sessionId: sessionId.value, corpora: selectedCorpora.value },
      (event) => {
        if (event.type === 'plan') reply.plan = event.data
        else if (event.type === 'citations') reply.citations = event.data
        else if (event.type === 'chunk') reveal.push(event.data)
        else if (event.type === 'session') {
          sessionId.value = event.session_id
          loadSessions()
        } else if (event.type === 'error') {
          ElMessage.error(event.data)
        }
      }
    )
    await reveal.flush()
  } catch (e) {
    await reveal.flush()
    reply.content += `\n\n（请求失败：${e.message}）`
    ElMessage.error(e.message)
  } finally {
    reply.thinking = false
    reply.streaming = false
    sending.value = false
    scrollDown()
  }
}

onMounted(() => {
  loadSessions()
  loadCorpora()
})
</script>

<style scoped>
.qa {
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

.stage {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  position: relative;
}

.chat-top {
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
.top-heading {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 4px;
}
.top-heading :deep(.el-dropdown) {
  margin-left: auto;
  flex-shrink: 0;
}
.top-title {
  min-width: 0;
  flex: 1;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: left;
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

.chat {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.chat-body {
  flex: 1;
  overflow-y: auto;
}

.chat-empty {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px 80px;
  text-align: center;
}
.chat-empty h1 {
  margin: 0;
  font-size: 32px;
  font-weight: 600;
  color: #1f1f1f;
  letter-spacing: 0.5px;
}
.chat-empty p {
  margin: 12px 0 0;
  color: #8a8a8a;
  font-size: 14px;
  max-width: 420px;
  line-height: 1.7;
}
.samples {
  margin-top: 28px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  max-width: 560px;
  width: 100%;
}
.sample {
  text-align: left;
  padding: 14px 16px;
  border: 1px solid #e8e8e8;
  background: #fff;
  border-radius: 14px;
  font-size: 13px;
  color: #303133;
  cursor: pointer;
  line-height: 1.5;
}
.sample:hover {
  background: #f7f7f7;
  border-color: #dcdcdc;
}

.thread {
  max-width: 768px;
  margin: 0 auto;
  padding: 8px 20px 24px;
  width: 100%;
}

.msg {
  display: flex;
  margin: 18px 0;
}
.msg.user {
  justify-content: flex-end;
}
.msg.assistant {
  justify-content: flex-start;
}

.bubble.user {
  max-width: 72%;
  padding: 10px 16px;
  border-radius: 18px;
  background: #f4f4f4;
  color: #1f1f1f;
  font-size: 15px;
  line-height: 1.7;
  white-space: pre-wrap;
}

.assistant {
  width: 100%;
  font-size: 15px;
  line-height: 1.8;
  color: #1f1f1f;
}

.plan {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 5px;
  margin-bottom: 10px;
}
.plan-label {
  font-size: 12px;
  color: #a8abb2;
}

.stream-status {
  display: inline-flex;
  align-items: baseline;
  gap: 4px;
  min-height: 1.8em;
}
.thinking {
  font-size: 14px;
  color: #a61b1b;
  letter-spacing: 0.04em;
}
.dots::after {
  display: inline-block;
  width: 1.4em;
  text-align: left;
  content: '';
  animation: thinking-dots 1.2s steps(4, end) infinite;
}
@keyframes thinking-dots {
  0% {
    content: '';
  }
  25% {
    content: '.';
  }
  50% {
    content: '..';
  }
  75% {
    content: '...';
  }
}

.cursor {
  animation: blink 1s step-end infinite;
  color: #a61b1b;
}
@keyframes blink {
  50% {
    opacity: 0;
  }
}

.citations {
  margin-top: 10px;
}
.citations :deep(.el-collapse-item__header) {
  font-size: 12px;
  color: #a61b1b;
  height: 32px;
  line-height: 32px;
  border-bottom: none;
}
.citations :deep(.el-collapse-item__arrow) {
  color: #a61b1b;
}
.citation {
  padding: 8px 0;
  border-bottom: 1px dashed #f0f0f0;
}
.citation-head {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  margin-bottom: 4px;
}
.citation-corpus {
  color: #a61b1b;
  font-weight: 600;
}
.citation-source {
  color: #909399;
}
.citation-score {
  margin-left: auto;
  color: #c0c4cc;
}
.citation-text {
  font-size: 12px;
  color: #606266;
  line-height: 1.7;
}

.markdown :deep(h2),
.markdown :deep(h3) {
  font-size: 15px;
  color: #1f1f1f;
  margin: 14px 0 6px;
}
.markdown :deep(p) {
  margin: 6px 0;
}
.markdown :deep(ul),
.markdown :deep(ol) {
  padding-left: 20px;
  margin: 6px 0;
}
.markdown :deep(li) {
  margin: 3px 0;
}
.markdown :deep(code) {
  background: #f5f5f5;
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 13px;
}
.markdown :deep(pre) {
  background: #f7f8fa;
  padding: 10px;
  border-radius: 8px;
  overflow-x: auto;
}

.composer-wrap {
  flex-shrink: 0;
  padding: 0 16px 16px;
}
.composer {
  max-width: 768px;
  margin: 0 auto;
}
.composer-box {
  position: relative;
  border: 1px solid #e4e4e4;
  border-radius: 26px;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  padding: 10px 52px 10px 48px;
}
.composer-box:focus-within {
  border-color: #d0d0d0;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
}
.composer-box :deep(.el-textarea__inner) {
  box-shadow: none;
  border: none;
  padding: 4px 0;
  background: transparent;
  font-size: 15px;
  line-height: 1.6;
}
.plus-btn {
  position: absolute;
  left: 8px;
  bottom: 8px;
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 50%;
  background: #f4f4f4;
  color: #4b4b4b;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.plus-btn:hover,
.plus-btn.active {
  background: #f5e6e6;
  color: #a61b1b;
}
.send-btn {
  position: absolute;
  right: 8px;
  bottom: 8px;
  width: 34px;
  height: 34px;
}
.composer-hint {
  text-align: center;
  font-size: 12px;
  color: #c0c4cc;
  margin-top: 8px;
}

.corpus-menu-title {
  font-size: 13px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}
.corpus-menu :deep(.el-checkbox-group) {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.corpus-hint {
  margin-top: 10px;
  font-size: 12px;
  color: #c0c4cc;
  line-height: 1.5;
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
.task.pinned .task-icon {
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
.task-status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: 4px;
}
.task-time {
  font-size: 11px;
  color: #a8abb2;
}
.task :deep(.el-dropdown) {
  flex-shrink: 0;
}
.more-btn {
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
.more-btn:hover {
  background: #fff;
  color: #303133;
}
.header-more:hover {
  background: #f3f3f3;
}

@media (max-width: 640px) {
  .samples {
    grid-template-columns: 1fr;
  }
  .chat-empty h1 {
    font-size: 24px;
  }
  .bubble.user {
    max-width: 88%;
  }
}
</style>
