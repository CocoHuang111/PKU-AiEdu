import axios from 'axios'
import { ElMessage } from 'element-plus'

const client = axios.create({ baseURL: '/', timeout: 600000 })

client.interceptors.response.use(
  (resp) => resp.data,
  (err) => {
    const msg = err.response?.data?.detail || err.message || '请求失败'
    ElMessage.error(typeof msg === 'string' ? msg : JSON.stringify(msg))
    return Promise.reject(err)
  }
)

export default client

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
  listTasks: () => client.get('/api/evaluation/tasks'),
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
