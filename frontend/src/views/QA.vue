<template>
  <div class="qa">
    <!-- 会话侧栏 -->
    <aside class="sessions">
      <div class="sessions-head">
        <span>历史会话</span>
        <el-button size="small" type="primary" plain @click="newSession">+ 新建</el-button>
      </div>
      <div class="sessions-list">
        <div v-if="!sessions.length" class="empty-hint">暂无会话</div>
        <div
          v-for="s in sessions"
          :key="s.id"
          class="session"
          :class="{ active: s.id === sessionId }"
          @click="openSession(s.id)"
        >
          <div class="session-title">{{ s.title }}</div>
          <div class="session-time">{{ formatTime(s.updated_at) }}</div>
          <el-button
            class="session-del"
            text
            type="danger"
            size="small"
            @click.stop="removeSession(s.id)"
          >
            删除
          </el-button>
        </div>
      </div>
    </aside>

    <!-- 对话区 -->
    <section class="chat">
      <div ref="bodyEl" class="chat-body">
        <div v-if="!messages.length" class="chat-empty">
          <div class="chat-empty-icon">🎓</div>
          <h3>教学智能问答</h3>
          <p>基于教育学理论、教学沙龙记录与你的历史评估报告，回答教学相关问题。</p>
          <div class="samples">
            <el-tag
              v-for="q in SAMPLES"
              :key="q"
              class="sample"
              effect="plain"
              @click="input = q"
            >
              {{ q }}
            </el-tag>
          </div>
        </div>

        <div v-for="(m, i) in messages" :key="i" class="msg" :class="m.role">
          <div v-if="m.role === 'user'" class="bubble user">{{ m.content }}</div>
          <div v-else class="bubble assistant">
            <!-- 检索规划：调试检索质量的窗口 -->
            <div v-if="m.plan" class="plan">
              <span class="plan-label">检索关键词</span>
              <el-tag v-for="q in m.plan.queries" :key="q" size="small" effect="plain">
                {{ q }}
              </el-tag>
              <span class="plan-label">语料库</span>
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

            <div class="markdown" v-html="renderMd(m.content)"></div>
            <span v-if="m.streaming" class="cursor">▋</span>

            <el-collapse v-if="m.citations?.length" class="citations">
              <el-collapse-item :title="`引用来源（${m.citations.length}）`" name="c">
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

      <!-- 输入区 -->
      <footer class="chat-footer">
        <div class="corpus-bar">
          <span class="corpus-label">语料库</span>
          <el-checkbox-group v-model="selectedCorpora" size="small">
            <el-checkbox v-for="c in corpora" :key="c.name" :value="c.name" :disabled="!c.count">
              {{ c.label }}（{{ c.count }}）
            </el-checkbox>
          </el-checkbox-group>
          <span class="corpus-hint">不勾选则检索全部语料库（相似度≥50%才引用，最多12条）</span>
        </div>
        <div class="input-row">
          <el-input
            v-model="input"
            type="textarea"
            :rows="2"
            resize="none"
            placeholder="输入教学相关问题，Enter 发送，Shift+Enter 换行"
            @keydown.enter.exact.prevent="send"
          />
          <el-button type="primary" :loading="sending" :disabled="!input.trim()" @click="send">
            发送
          </el-button>
        </div>
      </footer>
    </section>
  </div>
</template>

<script setup>
import { nextTick, onMounted, ref } from 'vue'
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
const bodyEl = ref(null)

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
  }
  messages.value.push(reply)
  scrollDown()

  try {
    await askStream(
      { question, sessionId: sessionId.value, corpora: selectedCorpora.value },
      (event) => {
        if (event.type === 'plan') reply.plan = event.data
        else if (event.type === 'citations') reply.citations = event.data
        else if (event.type === 'chunk') {
          reply.content += event.data
          scrollDown()
        } else if (event.type === 'session') {
          sessionId.value = event.session_id
          loadSessions()
        } else if (event.type === 'error') {
          ElMessage.error(event.data)
        }
      }
    )
  } catch (e) {
    reply.content += `\n\n（请求失败：${e.message}）`
    ElMessage.error(e.message)
  } finally {
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
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 16px;
  height: calc(100vh - 88px);
}

/* 会话侧栏 */
.sessions {
  background: #fff;
  border: 1px solid #e8eaed;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.sessions-head {
  padding: 12px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 600;
}
.sessions-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}
.session {
  position: relative;
  padding: 9px 10px;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 4px;
  border-left: 3px solid transparent;
}
.session:hover {
  background: #f7f8fa;
}
.session:hover .session-del {
  display: block;
}
.session.active {
  background: #fce8e8;
  border-left-color: #a61b1b;
}
.session-title {
  font-size: 13px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.session-time {
  font-size: 11px;
  color: #a8abb2;
  margin-top: 2px;
}
.session-del {
  display: none;
  position: absolute;
  right: 4px;
  top: 6px;
}

/* 对话区 */
.chat {
  background: #fff;
  border: 1px solid #e8eaed;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
}

.chat-empty {
  text-align: center;
  padding: 70px 20px;
}
.chat-empty-icon {
  font-size: 42px;
}
.chat-empty h3 {
  margin: 14px 0 8px;
  color: #303133;
}
.chat-empty p {
  color: #909399;
  font-size: 14px;
  max-width: 460px;
  margin: 0 auto;
  line-height: 1.8;
}
.samples {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}
.sample {
  cursor: pointer;
}

.msg {
  display: flex;
  margin-bottom: 18px;
}
.msg.user {
  justify-content: flex-end;
}

.bubble {
  max-width: 82%;
  padding: 11px 15px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.8;
}
.bubble.user {
  background: linear-gradient(135deg, #8b1010, #a61b1b);
  color: #fff;
  white-space: pre-wrap;
}
.bubble.assistant {
  background: #fff;
  border: 1px solid #f0e0e0;
  color: #303133;
}

/* 检索规划 */
.plan {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 5px;
  padding-bottom: 9px;
  margin-bottom: 10px;
  border-bottom: 1px dashed #f0e0e0;
}
.plan-label {
  font-size: 12px;
  color: #a8abb2;
  margin-right: 2px;
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

/* 引用 */
.citations {
  margin-top: 10px;
}
.citations :deep(.el-collapse-item__header) {
  font-size: 12px;
  color: #c47a7a;
  height: 32px;
  line-height: 32px;
  border-bottom: none;
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

/* Markdown */
.markdown :deep(h2),
.markdown :deep(h3) {
  font-size: 14px;
  color: #a61b1b;
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
  border-radius: 5px;
  overflow-x: auto;
}

/* 输入区 */
.chat-footer {
  border-top: 1px solid #ebeef5;
  padding: 12px 16px;
  background: #fdfdfd;
}
.corpus-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}
.corpus-label {
  font-size: 12px;
  color: #909399;
}
.corpus-hint {
  font-size: 12px;
  color: #c0c4cc;
}
.input-row {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}
.input-row .el-button {
  height: 60px;
  padding: 0 24px;
}
</style>
