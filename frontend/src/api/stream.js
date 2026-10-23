/**
 * SSE 流式问答。用 fetch 而非 axios —— axios 在浏览器端拿不到增量的响应体。
 *
 * onEvent 会收到后端推来的各类事件：
 *   { type: 'plan',      data: {...} }  检索规划（关键词、选中的语料库）
 *   { type: 'citations', data: [...] }  引用来源
 *   { type: 'chunk',     data: '文字' } 答案增量
 *   { type: 'done',      answer, citations, plan }
 *   { type: 'session',   session_id }
 *   { type: 'error',     data: '错误信息' }
 */
import { clearAuth } from '../authStore'

export async function askStream(
  { question, mode, sessionId, corpora, evalTaskIds, attachmentIds },
  onEvent,
  signal
) {
  const resp = await fetch('/api/qa/ask/stream', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question,
      mode: mode || 'ask',
      session_id: sessionId || null,
      corpora: Array.isArray(corpora) ? corpora : null,
      eval_task_ids: Array.isArray(evalTaskIds) ? evalTaskIds : null,
      attachment_ids: Array.isArray(attachmentIds) ? attachmentIds : null,
    }),
    signal,
  })

  if (resp.status === 401) {
    clearAuth()
    if (!location.hash.startsWith('#/login')) {
      location.hash = '#/login'
    }
    throw new Error('登录已失效，请重新登录')
  }

  if (!resp.ok) {
    const text = await resp.text().catch(() => '')
    throw new Error(`请求失败 ${resp.status}: ${text.slice(0, 200)}`)
  }

  const reader = resp.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const parts = buffer.split('\n\n')
    buffer = parts.pop() || ''

    for (const part of parts) {
      const line = part.split('\n').find((l) => l.startsWith('data:'))
      if (!line) continue
      try {
        onEvent(JSON.parse(line.slice(5).trim()))
      } catch {
        // 半包或脏数据，跳过
      }
    }
  }
}
