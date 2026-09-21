/**
 * 问答状态放在页面组件外面：切到评估 / 大纲、或换另一个会话时，SSE 继续跑。
 * 后端会在提问当下落库；刷新后若仍在生成，则轮询直到完成。
 * 多个会话可以同时生成，发送按钮只锁当前正在思考的那一个。
 */
import { computed, nextTick, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { qaApi, evaluationApi } from './api/client'
import { askStream } from './api/stream'

const SESSION_KEY = 'pku-askedu-qa-session'
const POLL_MS = 1500

export const sessions = ref([])
export const sessionId = ref(null)
export const messages = ref([])
export const corpora = ref([])
export const selectedCorpora = ref([])
export const evalReports = ref([])
export const selectedEvalTaskIds = ref([])
export const input = ref('')
export const sidebarOpen = ref(true)
export const sessionQuery = ref('')

let ownerId = null
let scrollHook = null
let pollTimer = null
const jobs = ref([])
const pollingId = ref(null)

export const sending = computed(() => {
  if (sessionId.value) {
    if (jobs.value.some((j) => j.sending && j.sessionId === sessionId.value)) return true
    return pollingId.value === sessionId.value
  }
  return jobs.value.some((j) => j.sending && !j.sessionId && j.messages === messages.value)
})

export function setQaScroll(fn) {
  scrollHook = fn
}

export function resetQa() {
  stopPoll()
  ownerId = null
  jobs.value = []
  pollingId.value = null
  sessions.value = []
  sessionId.value = null
  messages.value = []
  corpora.value = []
  selectedCorpora.value = []
  evalReports.value = []
  selectedEvalTaskIds.value = []
  input.value = ''
  sessionQuery.value = ''
  try {
    sessionStorage.removeItem(SESSION_KEY)
  } catch {
    /* ignore */
  }
}

function persistSessionId(id) {
  try {
    if (id) sessionStorage.setItem(SESSION_KEY, id)
    else sessionStorage.removeItem(SESSION_KEY)
  } catch {
    /* ignore */
  }
}

function readSavedSessionId() {
  try {
    return sessionStorage.getItem(SESSION_KEY)
  } catch {
    return null
  }
}

function ensureQaOwner(userId) {
  if (ownerId === userId) return
  if (ownerId !== null) resetQa()
  ownerId = userId
}

async function scrollDown() {
  await nextTick()
  scrollHook?.()
}

function hydrateMessages(history) {
  return (history || []).map((m) => {
    const pending = !!m.pending
    return {
      ...m,
      streaming: pending,
      thinking: pending && !m.content,
    }
  })
}

function stopPoll() {
  clearTimeout(pollTimer)
  pollTimer = null
}

function markListPending(id, pending) {
  const item = sessions.value.find((s) => s.id === id)
  if (item) item.pending = pending
}

export const currentTitle = computed(() => {
  if (!sessionId.value) return '新对话'
  return sessions.value.find((s) => s.id === sessionId.value)?.title || '对话'
})

export const currentPinned = computed(() => {
  return !!sessions.value.find((s) => s.id === sessionId.value)?.pinned
})

export const visibleGroups = computed(() => {
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

export const selectableNames = computed(() =>
  corpora.value.filter((c) => c.count && c.name !== 'eval_reports').map((c) => c.name)
)

export const evalCorpus = computed(() => corpora.value.find((c) => c.name === 'eval_reports'))

export const staticCorpora = computed(() =>
  corpora.value.filter((c) => c.name !== 'eval_reports')
)

export const staticSelectedCorpora = computed({
  get() {
    return selectedCorpora.value.filter((n) => n !== 'eval_reports')
  },
  set(names) {
    const next = Array.isArray(names) ? names : []
    selectedCorpora.value = selectedEvalTaskIds.value.length
      ? [...next, 'eval_reports']
      : next
  },
})

export const corporaNarrowed = computed(() => {
  const all = selectableNames.value
  const staticSelected = selectedCorpora.value.filter((n) => n !== 'eval_reports')
  const staticNotAll =
    all.length > 0 &&
    (all.length !== staticSelected.length || all.some((n) => !staticSelected.includes(n)))
  const hasEval = selectedEvalTaskIds.value.length > 0
  return staticNotAll || hasEval
})

export function corpusLabel(name) {
  return corpora.value.find((c) => c.name === name)?.label || name
}

export async function loadSessions() {
  try {
    sessions.value = await qaApi.sessions()
    for (const job of jobs.value) {
      if (job.sending && job.sessionId) markListPending(job.sessionId, true)
    }
  } catch {
    /* 拦截器已提示 */
  }
}

export async function loadCorpora() {
  try {
    corpora.value = await qaApi.corpora()
    if (!selectedCorpora.value.length) {
      selectedCorpora.value = corpora.value
        .filter((c) => c.count && c.name !== 'eval_reports')
        .map((c) => c.name)
    }
  } catch {
    /* 拦截器已提示 */
  }
}

export async function loadEvalReports() {
  try {
    const tasks = await evaluationApi.listTasks({ status: 'completed', limit: 200 })
    const ids = new Set(tasks.map((t) => t.id))
    evalReports.value = tasks
    selectedEvalTaskIds.value = selectedEvalTaskIds.value.filter((id) => ids.has(id))
    syncEvalCorpusSelection()
  } catch {
    /* 拦截器已提示 */
  }
}

export function applyEvalTaskSelection(ids) {
  const allowed = new Set(evalReports.value.map((t) => t.id))
  selectedEvalTaskIds.value = ids.filter((id) => allowed.has(id))
  syncEvalCorpusSelection()
}

function syncEvalCorpusSelection() {
  const has = selectedEvalTaskIds.value.length > 0
  const selected = selectedCorpora.value.filter((n) => n !== 'eval_reports')
  selectedCorpora.value = has ? [...selected, 'eval_reports'] : selected
}

export function evalReportLabel(task) {
  const name = task.filename || '未命名视频'
  const score = task.summary?.score
  const scoreText = Number.isFinite(score) ? `${Math.round(score)}分` : ''
  return scoreText ? `${name}（${scoreText}）` : name
}

export function evalReportTime(task) {
  if (!task.created_at) return ''
  return new Date(task.created_at * 1000).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function newSession() {
  stopPoll()
  pollingId.value = null
  sessionId.value = null
  messages.value = []
  persistSessionId(null)
}

function jobForSession(id, msgs) {
  if (id) return jobs.value.find((j) => j.sessionId === id)
  return jobs.value.find((j) => !j.sessionId && j.messages === msgs)
}

export async function openSession(id) {
  const liveJob = jobForSession(id)
  if (liveJob) {
    sessionId.value = id
    messages.value = liveJob.messages
    persistSessionId(id)
    stopPoll()
    pollingId.value = null
    scrollDown()
    return
  }
  try {
    const s = await qaApi.getSession(id)
    sessionId.value = id
    messages.value = hydrateMessages(s.history)
    persistSessionId(id)
    scrollDown()
    const last = messages.value[messages.value.length - 1]
    if (last?.pending) {
      pollPending(id)
    } else {
      stopPoll()
      if (pollingId.value === id) pollingId.value = null
    }
  } catch {
    /* 拦截器已提示 */
  }
}

async function pollPending(id) {
  stopPoll()
  pollingId.value = id
  const tick = async () => {
    if (sessionId.value !== id) return
    if (jobForSession(id)) return
    try {
      const s = await qaApi.getSession(id)
      const hist = s.history || []
      const last = hist[hist.length - 1]
      messages.value = hydrateMessages(hist)
      if (!last?.pending) {
        if (pollingId.value === id) pollingId.value = null
        markListPending(id, false)
        await loadSessions()
        await scrollDown()
        return
      }
      await scrollDown()
    } catch {
      /* 下一轮再试 */
    }
    pollTimer = setTimeout(tick, POLL_MS)
  }
  pollTimer = setTimeout(tick, 400)
}

export async function removeSession(id) {
  try {
    await ElMessageBox.confirm('确定删除这个会话？', '提示', { type: 'warning' })
  } catch {
    return
  }
  await qaApi.deleteSession(id)
  jobs.value = jobs.value.filter((j) => j.sessionId !== id)
  if (pollingId.value === id) pollingId.value = null
  if (sessionId.value === id) newSession()
  loadSessions()
}

export async function renameSession(id) {
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

export async function togglePin(id, pinned) {
  await qaApi.patchSession(id, { pinned })
  await loadSessions()
}

export function onSessionCommand(s, cmd) {
  if (cmd === 'rename') renameSession(s.id)
  else if (cmd === 'pin') togglePin(s.id, !s.pinned)
  else if (cmd === 'delete') removeSession(s.id)
}

export function onCurrentCommand(cmd) {
  const s = sessions.value.find((item) => item.id === sessionId.value)
  if (!s) return
  onSessionCommand(s, cmd)
}

export function useSample(q) {
  input.value = q
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

function createLineRevealer(reply, job) {
  let committed = ''
  let pending = ''
  const queue = []
  let running = false

  function viewing() {
    return messages.value === job.messages
  }

  function paint() {
    reply.content = committed + pending
    reply.thinking = !reply.content
    if (viewing()) scrollDown()
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

export async function send() {
  const question = input.value.trim()
  if (!question || sending.value) return

  // The attached evaluation reports apply to this question only. Snapshot them
  // before resetting the composer so the next question returns to the default
  // state without changing the user's static knowledge-base selection.
  const corporaForRequest = [...selectedCorpora.value]
  const evalTaskIdsForRequest = corporaForRequest.includes('eval_reports')
    ? [...selectedEvalTaskIds.value]
    : null
  applyEvalTaskSelection([])
  selectedCorpora.value = [...selectableNames.value]

  stopPoll()
  pollingId.value = null
  input.value = ''
  const thread = messages.value
  thread.push({ role: 'user', content: question })

  const reply = {
    role: 'assistant',
    content: '',
    citations: [],
    plan: null,
    streaming: true,
    thinking: true,
    pending: true,
  }
  thread.push(reply)

  const job = {
    sessionId: sessionId.value,
    messages: thread,
    sending: true,
  }
  jobs.value = [...jobs.value, job]
  const reveal = createLineRevealer(reply, job)
  scrollDown()

  try {
    await askStream(
      {
        question,
        sessionId: job.sessionId,
        corpora: corporaForRequest,
        evalTaskIds: evalTaskIdsForRequest,
      },
      (event) => {
        if (event.type === 'plan') reply.plan = event.data
        else if (event.type === 'citations') reply.citations = event.data
        else if (event.type === 'chunk') reveal.push(event.data)
        else if (event.type === 'session') {
          job.sessionId = event.session_id
          jobs.value = [...jobs.value]
          if (messages.value === job.messages) {
            sessionId.value = event.session_id
            persistSessionId(event.session_id)
          }
          markListPending(event.session_id, true)
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
    reply.pending = false
    job.sending = false
    jobs.value = jobs.value.filter((j) => j !== job)
    if (job.sessionId) markListPending(job.sessionId, false)
    loadSessions()
    if (messages.value === job.messages) scrollDown()
  }
}

export async function initQa(userId) {
  ensureQaOwner(userId)
  if (!corpora.value.length) await loadCorpora()
  await loadEvalReports()
  await loadSessions()
  if (jobs.value.some((j) => j.sending) || messages.value.length) return
  const saved = readSavedSessionId()
  if (saved && sessions.value.some((s) => s.id === saved)) {
    await openSession(saved)
    return
  }
  const pending = sessions.value.find((s) => s.pending)
  if (pending) await openSession(pending.id)
}

export async function onQaActivated() {
  await loadCorpora()
  await loadEvalReports()
  await loadSessions()
  await scrollDown()
}
