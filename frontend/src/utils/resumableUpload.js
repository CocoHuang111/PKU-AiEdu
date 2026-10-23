import { evaluationApi } from '../api/client'

export const DEFAULT_CHUNK_BYTES = 8 * 1024 * 1024
const MAX_RETRIES = 3
const RESUME_STORAGE_KEY = 'askedu.resumable-uploads.v1'

function ensureNotAborted(signal) {
  if (signal?.aborted) throw new DOMException('操作已取消', 'AbortError')
}

function sleep(milliseconds, signal) {
  return new Promise((resolve, reject) => {
    ensureNotAborted(signal)
    const timer = setTimeout(resolve, milliseconds)
    signal?.addEventListener(
      'abort',
      () => {
        clearTimeout(timer)
        reject(new DOMException('操作已取消', 'AbortError'))
      },
      { once: true }
    )
  })
}

export async function sha256(blob) {
  const bytes = blob instanceof Uint8Array ? blob : await blob.arrayBuffer()
  const digest = await crypto.subtle.digest('SHA-256', bytes)
  return Array.from(new Uint8Array(digest), (value) => value.toString(16).padStart(2, '0')).join('')
}

export async function fileFingerprint(file) {
  const sampleBytes = Math.min(1024 * 1024, file.size)
  const first = new Uint8Array(await file.slice(0, sampleBytes).arrayBuffer())
  const lastStart = Math.max(0, file.size - sampleBytes)
  const last = new Uint8Array(await file.slice(lastStart).arrayBuffer())
  const metadata = new TextEncoder().encode(`${file.name}\n${file.size}\n${file.lastModified || 0}\n`)
  const joined = new Uint8Array(metadata.length + first.length + last.length)
  joined.set(metadata)
  joined.set(first, metadata.length)
  joined.set(last, metadata.length + first.length)
  return sha256(joined)
}

function readResumeRecords() {
  try {
    const value = JSON.parse(localStorage.getItem(RESUME_STORAGE_KEY) || '{}')
    return value && typeof value === 'object' ? value : {}
  } catch {
    return {}
  }
}

export function rememberedTaskId(fingerprint) {
  return readResumeRecords()[fingerprint]?.taskId || null
}

export function rememberTask(fingerprint, taskId, filename) {
  try {
    const records = readResumeRecords()
    records[fingerprint] = { taskId, filename, updatedAt: Date.now() }
    localStorage.setItem(RESUME_STORAGE_KEY, JSON.stringify(records))
  } catch {
    /* 私密窗口禁用存储时，当前页面内的重试仍然有效。 */
  }
}

export function forgetTask(fingerprint) {
  try {
    const records = readResumeRecords()
    delete records[fingerprint]
    localStorage.setItem(RESUME_STORAGE_KEY, JSON.stringify(records))
  } catch {
    /* 无本地存储权限时无需清理。 */
  }
}

async function withRetry(action, signal) {
  let lastError
  for (let attempt = 0; attempt < MAX_RETRIES; attempt += 1) {
    ensureNotAborted(signal)
    try {
      return await action(attempt)
    } catch (error) {
      if (error?.name === 'AbortError' || error?.code === 'ERR_CANCELED') throw error
      lastError = error
      if (attempt + 1 < MAX_RETRIES) await sleep(500 * 2 ** attempt, signal)
    }
  }
  throw lastError
}

async function uploadOnePart({ taskId, kind, index, blob, sessionId, signal, onProgress }) {
  const digest = await sha256(blob)
  return withRetry(
    () =>
      evaluationApi.uploadPart(taskId, kind, index, blob, {
        sessionId,
        sha256: digest,
        signal,
        onProgress,
      }),
    signal
  )
}

export async function measureUploadSpeed({ signal, bytes = 1024 * 1024 } = {}) {
  ensureNotAborted(signal)
  const warmup = new Blob([crypto.getRandomValues(new Uint8Array(64 * 1024))])
  await evaluationApi.probeUpload(warmup, signal)
  const blocks = []
  let remaining = bytes
  while (remaining > 0) {
    const size = Math.min(64 * 1024, remaining)
    blocks.push(crypto.getRandomValues(new Uint8Array(size)))
    remaining -= size
  }
  const payload = new Blob(blocks)
  const started = performance.now()
  await evaluationApi.probeUpload(payload, signal)
  const elapsedSec = Math.max((performance.now() - started) / 1000, 0.05)
  return {
    bytesPerSec: payload.size / elapsedSec,
    megabitsPerSec: (payload.size * 8) / elapsedSec / 1_000_000,
    elapsedSec,
  }
}

export function chooseUploadStrategy(file, network, evidence) {
  const uploadBytesPerSec = Math.max(Number(network?.bytesPerSec || 0), 1)
  const originalSeconds = file.size / uploadBytesPerSec
  if (!evidence) {
    return {
      mode: 'original',
      originalSeconds,
      fastSeconds: null,
      reason: '当前浏览器无法稳定生成快速材料',
    }
  }
  const fastUploadSeconds = evidence.estimatedBytes / uploadBytesPerSec
  // 提取与上传能重叠进行，整体按较慢的一侧估算，再给收尾留少量余量。
  const fastSeconds = Math.max(evidence.estimatedProcessSec, fastUploadSeconds) * 1.08
  const savedRatio = 1 - fastSeconds / Math.max(originalSeconds, 1)
  const mode = originalSeconds >= 90 && savedRatio >= 0.2 ? 'fast' : 'original'
  return {
    mode,
    originalSeconds,
    fastSeconds,
    savedRatio,
    estimatedEvidenceBytes: evidence.estimatedBytes,
    reason:
      mode === 'fast'
        ? `预计比原视频上传节省 ${Math.max(0, Math.round(savedRatio * 100))}% 时间`
        : '原视频较小或当前网络足够快，预处理收益有限',
  }
}

export async function createOrResumeSession(taskId, file, options = {}) {
  const fingerprint = options.fingerprint || (await fileFingerprint(file))
  return evaluationApi.createUploadSession(taskId, {
    mode: options.mode || 'original',
    fingerprint,
    original_filename: file.name,
    original_size: file.size,
    audio_filename: options.audioFilename,
    audio_mime: options.audioMime,
  })
}

export async function uploadOriginalVideo({ taskId, file, fingerprint, signal, onProgress }) {
  const session = await createOrResumeSession(taskId, file, { mode: 'original', fingerprint })
  if (session.complete) return session.task
  const chunkSize = session.chunk_size || DEFAULT_CHUNK_BYTES
  const partCount = Math.ceil(file.size / chunkSize)
  const confirmed = new Map((session.received?.video || []).map((item) => [item.index, item.size]))
  let committed = Array.from(confirmed.values()).reduce((sum, size) => sum + size, 0)
  const activeProgress = new Map()
  const report = (loaded, stage) => {
    const visible = Math.min(file.size, loaded)
    onProgress?.({
      percent: Math.round((visible / Math.max(file.size, 1)) * 100),
      stage,
      loaded: visible,
      total: file.size,
    })
  }
  report(committed, '断点续传检查完成')

  let cursor = 0
  const workers = Array.from({ length: Math.min(3, partCount) }, async () => {
    while (true) {
      const index = cursor
      cursor += 1
      if (index >= partCount) return
      ensureNotAborted(signal)
      if (confirmed.has(index)) continue
      const start = index * chunkSize
      const blob = file.slice(start, Math.min(file.size, start + chunkSize))
      await uploadOnePart({
        taskId,
        kind: 'video',
        index,
        blob,
        sessionId: session.session_id,
        signal,
        onProgress: (loaded) => {
          activeProgress.set(index, loaded)
          const activeBytes = Array.from(activeProgress.values()).reduce((sum, size) => sum + size, 0)
          report(committed + activeBytes, '分片上传原视频')
        },
      })
      activeProgress.delete(index)
      committed += blob.size
      report(committed, '分片上传原视频')
    }
  })
  await Promise.all(workers)
  return evaluationApi.completeUploadSession(taskId, { session_id: session.session_id })
}

export class StreamingPartWriter {
  constructor({ taskId, kind, session, signal, onProgress, concurrency = 2 }) {
    this.taskId = taskId
    this.kind = kind
    this.session = session
    this.signal = signal
    this.onProgress = onProgress
    this.concurrency = concurrency
    this.chunkSize = session.chunk_size || DEFAULT_CHUNK_BYTES
    this.confirmed = new Set((session.received?.[kind] || []).map((item) => item.index))
    this.buffer = new Uint8Array(this.chunkSize)
    this.buffered = 0
    this.index = 0
    this.generatedBytes = 0
    this.uploadedBytes = (session.received?.[kind] || []).reduce((sum, item) => sum + item.size, 0)
    this.pending = new Set()
  }

  async _queue(bytes) {
    const index = this.index
    this.index += 1
    if (this.confirmed.has(index)) {
      this.onProgress?.({ generatedBytes: this.generatedBytes, uploadedBytes: this.uploadedBytes, index })
      return
    }
    const blob = new Blob([bytes])
    const promise = uploadOnePart({
      taskId: this.taskId,
      kind: this.kind,
      index,
      blob,
      sessionId: this.session.session_id,
      signal: this.signal,
    }).then(() => {
      this.uploadedBytes += blob.size
      this.onProgress?.({ generatedBytes: this.generatedBytes, uploadedBytes: this.uploadedBytes, index })
    })
    this.pending.add(promise)
    promise.then(
      () => this.pending.delete(promise),
      () => this.pending.delete(promise)
    )
    if (this.pending.size >= this.concurrency) await Promise.race(this.pending)
  }

  async write(chunk) {
    ensureNotAborted(this.signal)
    const bytes = chunk instanceof Uint8Array ? chunk : new Uint8Array(chunk)
    let offset = 0
    this.generatedBytes += bytes.byteLength
    while (offset < bytes.byteLength) {
      const length = Math.min(this.chunkSize - this.buffered, bytes.byteLength - offset)
      this.buffer.set(bytes.subarray(offset, offset + length), this.buffered)
      this.buffered += length
      offset += length
      if (this.buffered === this.chunkSize) {
        const full = this.buffer
        this.buffer = new Uint8Array(this.chunkSize)
        this.buffered = 0
        await this._queue(full)
      }
    }
    this.onProgress?.({ generatedBytes: this.generatedBytes, uploadedBytes: this.uploadedBytes })
  }

  async close() {
    if (this.buffered) await this._queue(this.buffer.slice(0, this.buffered))
    await Promise.all(this.pending)
    return { partCount: this.index, generatedBytes: this.generatedBytes, uploadedBytes: this.uploadedBytes }
  }

  async writePart(bytes) {
    ensureNotAborted(this.signal)
    const value = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes)
    this.generatedBytes += value.byteLength
    await this._queue(value)
  }

  writableStream() {
    return new WritableStream({
      write: (chunk) => this.write(chunk),
      close: () => undefined,
      abort: (reason) => {
        throw reason
      },
    })
  }
}

export async function uploadFrameArchive(writer, archiveBytes) {
  await writer.writePart(archiveBytes)
  return writer.index
}
