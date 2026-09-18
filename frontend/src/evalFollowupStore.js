/**
 * 评估入队后的跟进弹窗放在页面组件外面：切到问答 / 大纲 / 我的，或浏览器切到后台，
 * 上传结束后仍能弹出。刷新后若尚未关掉弹窗，会按 sessionStorage 再打开一次。
 */
import { ref, watch } from 'vue'
import { evaluationApi } from './api/client'
import router from './router'

const STORAGE_KEY = 'pku-askedu-eval-queued-followup'

export const followupVisible = ref(false)
export const followupTask = ref(null)
export const followupInfo = ref(null)
export const mailStatus = ref('')
export const mailDeclined = ref(false)
export const mailSaving = ref(false)

function persistPending(taskId) {
  try {
    if (taskId) sessionStorage.setItem(STORAGE_KEY, taskId)
    else sessionStorage.removeItem(STORAGE_KEY)
  } catch {
    /* 私密窗口可能禁用存储 */
  }
}

function readPending() {
  try {
    return sessionStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

watch(followupVisible, (open) => {
  if (!open) persistPending('')
})

export function closeFollowup() {
  followupVisible.value = false
}

export function requestDesktopNotifyPermission() {
  if (typeof Notification === 'undefined') return
  if (Notification.permission !== 'default') return
  Notification.requestPermission().catch(() => {})
}

function onEvaluationRoute() {
  return router.currentRoute.value.path === '/evaluation'
}

function notifyDesktop(taskId) {
  if (typeof Notification === 'undefined') return
  if (Notification.permission !== 'granted') return
  if (document.visibilityState === 'visible' && onEvaluationRoute()) return
  try {
    const n = new Notification('视频已加入评估队列', {
      body: '上传已完成，评估将在后台继续。点此回到教学评估查看进度。',
      tag: `eval-queued-${taskId}`,
    })
    n.onclick = () => {
      window.focus()
      n.close()
      if (!onEvaluationRoute()) {
        router.push({ path: '/evaluation', query: { task: taskId, submitted: '1' } })
      }
    }
  } catch {
    /* 部分内嵌浏览器不支持 Notification 构造 */
  }
}

export async function showEvalQueuedFollowup(taskId, { desktop = true } = {}) {
  if (!taskId) return
  const sameOpen = followupVisible.value && followupTask.value === taskId
  followupTask.value = taskId
  persistPending(taskId)
  followupVisible.value = true
  if (!sameOpen) {
    followupInfo.value = null
    mailStatus.value = ''
    mailDeclined.value = false
  }
  if (desktop) notifyDesktop(taskId)
  try {
    const info = await evaluationApi.followUp(taskId)
    if (followupTask.value !== taskId) return
    followupInfo.value = info
    mailStatus.value = info.notification_status || ''
  } catch {
    /* 任务已成功提交，后续提示失败不影响解析 */
  }
}

export function restorePendingFollowup() {
  const id = readPending()
  if (id) void showEvalQueuedFollowup(id, { desktop: false })
}

export async function enableReportMail() {
  if (!followupTask.value) return
  mailSaving.value = true
  mailDeclined.value = false
  try {
    const info = await evaluationApi.followUp(followupTask.value)
    if (!info.has_email) {
      const taskId = followupTask.value
      closeFollowup()
      await router.push({ path: '/profile', query: { reportMailTask: taskId } })
      return
    }
    const response = await evaluationApi.requestEmail(followupTask.value)
    mailStatus.value = response.status
  } catch {
    /* 错误由公共拦截器提示 */
  } finally {
    mailSaving.value = false
  }
}

export function goToFeature(path) {
  closeFollowup()
  router.push(path)
}

export function stayOnEvaluation() {
  const taskId = followupTask.value
  closeFollowup()
  if (!onEvaluationRoute()) {
    router.push({ path: '/evaluation', query: taskId ? { task: taskId } : {} })
  }
}
