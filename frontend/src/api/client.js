import axios from 'axios'
import { ElMessage } from 'element-plus'
import { clearAuth } from '../authStore'

const client = axios.create({
  baseURL: '/',
  timeout: 600000,
  withCredentials: true,
})

client.interceptors.response.use(
  (resp) => resp.data,
  (err) => {
    const status = err.response?.status
    const msg = err.response?.data?.detail || err.message || '请求失败'
    if (status !== 401) {
      ElMessage.error(typeof msg === 'string' ? msg : JSON.stringify(msg))
    }
    if (status === 401) {
      clearAuth()
      if (!location.hash.startsWith('#/login')) {
        const redirect = location.hash.replace(/^#/, '') || '/qa'
        location.hash = `#/login?redirect=${encodeURIComponent(redirect)}`
      }
    }
    return Promise.reject(err)
  }
)

export default client

export const authApi = {
  config: () => client.get('/api/auth/config'),
  register: (data) => client.post('/api/auth/register', data),
  login: (data) => client.post('/api/auth/login', data),
  logout: () => client.post('/api/auth/logout'),
  me: () => client.get('/api/auth/me'),
  updateMe: (data) => client.patch('/api/auth/me', data),
  changePassword: (data) => client.post('/api/auth/change-password', data),
  uploadAvatar: (file) => {
    const form = new FormData()
    form.append('file', file)
    return client.post('/api/auth/me/avatar', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  pkuStart: () => client.get('/api/auth/pku/start'),
}

export const adminApi = {
  overview: () => client.get('/api/admin/overview'),
  users: (params) => client.get('/api/admin/users', { params }),
  getUser: (id) => client.get(`/api/admin/users/${id}`),
  disableUser: (id) => client.post(`/api/admin/users/${id}/disable`),
  enableUser: (id) => client.post(`/api/admin/users/${id}/enable`),
  setRole: (id, role) => client.post(`/api/admin/users/${id}/role`, { role }),
  resetPassword: (id, password) =>
    client.post(`/api/admin/users/${id}/reset-password`, { password }),
  tasks: (params) => client.get('/api/admin/tasks', { params }),
  cancelTask: (kind, id) => client.post(`/api/admin/tasks/${kind}/${id}/cancel`),
  cleanupTask: (kind, id) => client.delete(`/api/admin/tasks/${kind}/${id}`),
  audit: (params) => client.get('/api/admin/audit', { params }),
}

// ---------------------------------------------------------------- 视频评估
export const evaluationApi = {
  uploadMaterials(files, onProgress) {
    const opts = files || {}
    const form = new FormData()
    if (opts.video) form.append('file', opts.video)
    if (opts.syllabus) form.append('syllabus', opts.syllabus)
    if (opts.courseware) form.append('courseware', opts.courseware)
    if (opts.transcript) form.append('transcript', opts.transcript)
    if (opts.transcriptText?.trim()) form.append('transcript_text', opts.transcriptText.trim())
    if (opts.reference?.trim()) form.append('reference', opts.reference.trim())
    return client.post('/api/evaluation/upload_video', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        if (onProgress && e.total) onProgress(Math.round((e.loaded / e.total) * 100))
      },
    })
  },
  uploadVideo(file, onProgress, extras) {
    const opts = typeof extras === 'string' ? { reference: extras } : extras || {}
    return this.uploadMaterials(
      {
        video: file,
        syllabus: opts.syllabus,
        courseware: opts.courseware,
        transcript: opts.transcript,
        transcriptText: opts.transcriptText,
        reference: opts.reference,
      },
      onProgress
    )
  },
  listTasks: (params) => client.get('/api/evaluation/tasks', { params }),
  getTask: (id) => client.get(`/api/evaluation/task/${id}`),
  cancelTask: (id) => client.post(`/api/evaluation/task/${id}/cancel`),
  deleteTask: (id) => client.delete(`/api/evaluation/task/${id}`),
  evaluateTranscript: (text, durationSec, reference) =>
    client.post('/api/evaluation/transcript', {
      text,
      duration_sec: durationSec,
      reference: reference?.trim() || undefined,
    }),
  getRubric: () => client.get('/api/evaluation/rubric'),
  exportUrl: (id, format) => `/api/evaluation/task/${id}/export?format=${format}`,
  chartUrl: (id, name) => `/api/evaluation/task/${id}/chart/${name}`,
  fileUrl: (id, kind) => `/api/evaluation/task/${id}/file/${kind}`,
}

// ---------------------------------------------------------------- 大纲优化
export const syllabusApi = {
  optimizeText: (text, promptMode) =>
    client.post('/api/syllabus/optimize', {
      text,
      prompt_mode: promptMode || undefined,
    }),
  optimizeFile(file, promptMode) {
    const form = new FormData()
    form.append('file', file)
    const mode = promptMode ? `?prompt_mode=${encodeURIComponent(promptMode)}` : ''
    return client.post(`/api/syllabus/optimize_file${mode}`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  listTasks: () => client.get('/api/syllabus/tasks'),
  getTask: (id) => client.get(`/api/syllabus/task/${id}`),
  cancelTask: (id) => client.post(`/api/syllabus/task/${id}/cancel`),
  deleteTask: (id) => client.delete(`/api/syllabus/task/${id}`),
  history: () => client.get('/api/syllabus/history'),
  getRecord: (id) => client.get(`/api/syllabus/record/${id}`),
  downloadUrl: (id) => `/api/syllabus/download/${id}`,
  exportUrl: (id, format) => `/api/syllabus/export/${id}?format=${format}`,
}

// ---------------------------------------------------------------- 问答
export const qaApi = {
  corpora: () => client.get('/api/qa/corpora'),
  sessions: () => client.get('/api/qa/sessions'),
  getSession: (id) => client.get(`/api/qa/session/${id}`),
  patchSession: (id, data) => client.patch(`/api/qa/session/${id}`, data),
  deleteSession: (id) => client.delete(`/api/qa/session/${id}`),
}

export const healthApi = {
  check: () => client.get('/api/health'),
}
