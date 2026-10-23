import { zipSync } from 'fflate'
import {
  ALL_FORMATS,
  AppendOnlyStreamTarget,
  BlobSource,
  BufferTarget,
  Conversion,
  FlacOutputFormat,
  Input,
  Mp3OutputFormat,
  Mp4OutputFormat,
  Output,
  VideoSampleSink,
  WavOutputFormat,
  WebMOutputFormat,
} from 'mediabunny'
import { StreamingPartWriter } from './resumableUpload'

const DENSE_INTERVAL_SEC = 3
const KEYFRAME_COUNT = 12
const MAX_DURATION_SEC = 4 * 60 * 60
const MAX_DENSE_FRAMES = 5000

class BrowserEvidenceError extends Error {
  constructor(message) {
    super(message)
    this.name = 'BrowserEvidenceError'
  }
}

function ensureNotAborted(signal) {
  if (signal?.aborted) throw new DOMException('操作已取消', 'AbortError')
}

function audioOutput(codec, { streaming = false } = {}) {
  if (codec === 'aac' || codec === 'alac') {
    return {
      format: new Mp4OutputFormat(
        streaming ? { fastStart: 'fragmented', minimumFragmentDuration: 2 } : { fastStart: false }
      ),
      extension: 'm4a',
      mime: 'audio/mp4',
    }
  }
  if (codec === 'opus' || codec === 'vorbis') {
    return {
      format: new WebMOutputFormat(),
      extension: 'webm',
      mime: 'audio/webm',
    }
  }
  if (codec === 'mp3') {
    return { format: new Mp3OutputFormat(), extension: 'mp3', mime: 'audio/mpeg' }
  }
  if (codec === 'flac') {
    return { format: new FlacOutputFormat(), extension: 'flac', mime: 'audio/flac' }
  }
  if (codec?.startsWith('pcm-')) {
    if (streaming) throw new BrowserEvidenceError('PCM/WAV 音轨暂不支持边提取边上传')
    return { format: new WavOutputFormat({ large: true }), extension: 'wav', mime: 'audio/wav' }
  }
  throw new BrowserEvidenceError(`暂不支持无损拆分 ${codec || '未知'} 音频`)
}

function outputDescription(codec, sourceName) {
  const spec = audioOutput(codec, { streaming: true })
  const stem = sourceName.replace(/\.[^.]+$/, '') || 'classroom'
  return {
    codec,
    filename: `${stem}.audio.${spec.extension}`,
    mime: spec.mime,
  }
}

function createCanvas(width, height) {
  if (typeof OffscreenCanvas !== 'undefined') return new OffscreenCanvas(width, height)
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  return canvas
}

async function canvasJpeg(canvas, quality) {
  if (typeof canvas.convertToBlob === 'function') {
    return canvas.convertToBlob({ type: 'image/jpeg', quality })
  }
  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new BrowserEvidenceError('图片编码失败'))),
      'image/jpeg',
      quality
    )
  })
}

async function sampleJpeg(sample, width, height, quality) {
  const canvas = createCanvas(width, height)
  const context = canvas.getContext('2d', { alpha: false })
  if (!context) throw new BrowserEvidenceError('浏览器无法创建画面处理画布')
  context.fillStyle = '#000'
  context.fillRect(0, 0, width, height)
  sample.draw(context, 0, 0, width, height)
  return canvasJpeg(canvas, quality)
}

function denseTimestamps(duration) {
  const count = Math.min(Math.ceil(duration / DENSE_INTERVAL_SEC), MAX_DENSE_FRAMES)
  return Array.from({ length: count }, (_, index) => index * DENSE_INTERVAL_SEC)
}

function keyframeTimestamps(duration) {
  return Array.from({ length: KEYFRAME_COUNT }, (_, index) => {
    const ratio = 0.05 + (0.9 * index) / Math.max(KEYFRAME_COUNT - 1, 1)
    return duration * ratio
  })
}

async function collectFrames(videoTrack, duration, signal, onProgress) {
  const sink = new VideoSampleSink(videoTrack, { hardwareAcceleration: 'prefer-hardware' })
  const archiveFiles = {}
  const denseFrames = []
  const keyframes = []
  const denseTimes = denseTimestamps(duration)
  let index = 0

  for await (const sample of sink.samplesAtTimestamps(denseTimes)) {
    ensureNotAborted(signal)
    const expectedTime = denseTimes[index]
    if (!sample) throw new BrowserEvidenceError(`无法读取 ${expectedTime.toFixed(1)} 秒画面`)
    try {
      const blob = await sampleJpeg(sample, 160, 90, 0.58)
      const name = `dense/${String(index).padStart(5, '0')}.jpg`
      archiveFiles[name] = new Uint8Array(await blob.arrayBuffer())
      denseFrames.push({ name, time_sec: Number(expectedTime.toFixed(3)) })
    } finally {
      sample.close()
    }
    index += 1
    onProgress?.({ percent: 30 + Math.round((index / denseTimes.length) * 55), stage: '抽取画面证据' })
  }

  const keyTimes = keyframeTimestamps(duration)
  index = 0
  for await (const sample of sink.samplesAtTimestamps(keyTimes)) {
    ensureNotAborted(signal)
    const expectedTime = keyTimes[index]
    if (!sample) throw new BrowserEvidenceError(`无法读取 ${expectedTime.toFixed(1)} 秒关键画面`)
    try {
      const scale = Math.min(1, 1280 / Math.max(sample.displayWidth, 1))
      const width = Math.max(2, Math.round(sample.displayWidth * scale))
      const height = Math.max(2, Math.round(sample.displayHeight * scale))
      const blob = await sampleJpeg(sample, width, height, 0.82)
      const name = `key/${String(index).padStart(2, '0')}.jpg`
      archiveFiles[name] = new Uint8Array(await blob.arrayBuffer())
      keyframes.push({ name, time_sec: Number(expectedTime.toFixed(3)) })
    } finally {
      sample.close()
    }
    index += 1
    onProgress?.({ percent: 85 + Math.round((index / keyTimes.length) * 12), stage: '抽取关键画面' })
  }

  ensureNotAborted(signal)
  onProgress?.({ percent: 98, stage: '整理证据包' })
  const zipped = zipSync(archiveFiles, { level: 0 })
  return {
    archive: new File([zipped], 'browser-evidence.zip', { type: 'application/zip' }),
    denseFrames,
    keyframes,
  }
}

async function extractAudio(input, audioTrack, codec, sourceName, signal, onProgress) {
  const spec = audioOutput(codec)
  const target = new BufferTarget()
  const output = new Output({ format: spec.format, target })
  const conversion = await Conversion.init({
    input,
    output,
    tracks: 'primary',
    video: { discard: true },
    copy: { mode: 'forced', shiftTolerance: 0 },
    tags: {},
  })
  if (!conversion.isValid || !conversion.utilizedTracks.includes(audioTrack)) {
    throw new BrowserEvidenceError('该音轨无法无损拆分')
  }
  const cancel = () => void conversion.cancel()
  signal?.addEventListener('abort', cancel, { once: true })
  conversion.onProgress = (progress) => {
    onProgress?.({ percent: Math.round(progress * 28), stage: '无损拆分原始音频' })
  }
  try {
    await conversion.execute()
  } finally {
    signal?.removeEventListener('abort', cancel)
  }
  ensureNotAborted(signal)
  if (!target.buffer) throw new BrowserEvidenceError('没有生成音频文件')
  const stem = sourceName.replace(/\.[^.]+$/, '') || 'classroom'
  return new File([target.buffer], `${stem}.audio.${spec.extension}`, { type: spec.mime })
}

export async function prepareBrowserEvidence(file, { signal, onProgress } = {}) {
  ensureNotAborted(signal)
  onProgress?.({ percent: 0, stage: '检查浏览器兼容性' })
  const input = new Input({ formats: ALL_FORMATS, source: new BlobSource(file) })
  try {
    const [audioTrack, videoTrack, duration] = await Promise.all([
      input.getPrimaryAudioTrack(),
      input.getPrimaryVideoTrack(),
      input.computeDuration(),
    ])
    if (!audioTrack) throw new BrowserEvidenceError('视频中没有音轨')
    if (!videoTrack) throw new BrowserEvidenceError('视频中没有画面轨道')
    if (!(await videoTrack.canDecode())) throw new BrowserEvidenceError('当前浏览器无法解码该视频')
    if (!Number.isFinite(duration) || duration <= 0 || duration > MAX_DURATION_SEC) {
      throw new BrowserEvidenceError('视频时长无效或超过4小时')
    }

    const codec = await audioTrack.getCodec()
    const audio = await extractAudio(input, audioTrack, codec, file.name, signal, onProgress)
    onProgress?.({ percent: 30, stage: '开始抽取画面证据' })
    const frames = await collectFrames(videoTrack, duration, signal, onProgress)
    const manifest = {
      version: 1,
      original_filename: file.name,
      original_size: file.size,
      duration_sec: Number(duration.toFixed(3)),
      interval_sec: DENSE_INTERVAL_SEC,
      audio_codec: codec,
      audio_size: audio.size,
      dense_frames: frames.denseFrames,
      keyframes: frames.keyframes,
    }
    onProgress?.({ percent: 100, stage: '浏览器预处理完成' })
    return { audio, archive: frames.archive, manifest }
  } catch (error) {
    if (error?.name === 'AbortError' || error?.name === 'ConversionCanceledError') {
      throw new DOMException('操作已取消', 'AbortError')
    }
    if (error instanceof BrowserEvidenceError) throw error
    throw new BrowserEvidenceError(error?.message || '浏览器预处理失败')
  } finally {
    input.dispose()
  }
}

export async function benchmarkBrowserEvidence(file, { signal, onProgress } = {}) {
  ensureNotAborted(signal)
  const input = new Input({ formats: ALL_FORMATS, source: new BlobSource(file) })
  try {
    onProgress?.({ stage: '检测视频与音轨' })
    const [audioTrack, videoTrack, duration] = await Promise.all([
      input.getPrimaryAudioTrack(),
      input.getPrimaryVideoTrack(),
      input.computeDuration(),
    ])
    if (!audioTrack) throw new BrowserEvidenceError('视频中没有音轨')
    if (!videoTrack) throw new BrowserEvidenceError('视频中没有画面轨道')
    if (!(await videoTrack.canDecode())) throw new BrowserEvidenceError('当前浏览器无法解码该视频')
    if (!Number.isFinite(duration) || duration <= 0 || duration > MAX_DURATION_SEC) {
      throw new BrowserEvidenceError('视频时长无效或超过4小时')
    }
    const codec = await audioTrack.getCodec()
    const audio = outputDescription(codec, file.name)
    const readBytes = Math.min(file.size, 16 * 1024 * 1024)
    const readStarted = performance.now()
    await file.slice(0, readBytes).arrayBuffer()
    const readSec = Math.max((performance.now() - readStarted) / 1000, 0.02)
    const readBytesPerSec = readBytes / readSec

    onProgress?.({ stage: '测量浏览器画面处理速度' })
    const sink = new VideoSampleSink(videoTrack, { hardwareAcceleration: 'prefer-hardware' })
    const frameStarted = performance.now()
    let jpegBytes = 0
    let sampled = 0
    let decoded = 0
    const benchmarkWindowSec = Math.min(duration, 2)
    for await (const sample of sink.samples(0, benchmarkWindowSec)) {
      ensureNotAborted(signal)
      try {
        if (decoded % 12 === 0 && sampled < 6) {
          const blob = await sampleJpeg(sample, 160, 90, 0.58)
          jpegBytes += blob.size
          sampled += 1
        }
      } finally {
        sample.close()
      }
      decoded += 1
    }
    if (!decoded || !sampled) throw new BrowserEvidenceError('无法读取测速画面')
    const frameSec = Math.max((performance.now() - frameStarted) / 1000, 0.02)
    const denseCount = denseTimestamps(duration).length
    const audioBitrate = (await audioTrack.getAverageBitrate()) || 128_000
    const estimatedAudioBytes = Math.ceil((audioBitrate * duration) / 8 * 1.08)
    const estimatedFrameBytes = Math.ceil(
      (jpegBytes / Math.max(sampled, 1)) * denseCount + KEYFRAME_COUNT * 140 * 1024
    )
    const scanSec = file.size / Math.max(readBytesPerSec, 1)
    const frameProcessSec = (frameSec / Math.max(benchmarkWindowSec, 0.1)) * duration
    return {
      durationSec: duration,
      codec,
      audio,
      denseCount,
      estimatedBytes: estimatedAudioBytes + estimatedFrameBytes,
      estimatedAudioBytes,
      estimatedFrameBytes,
      estimatedProcessSec: Math.max(1, scanSec + frameProcessSec),
      benchmark: { readBytesPerSec, frameSeconds: frameSec, sampledFrames: sampled },
    }
  } catch (error) {
    if (error?.name === 'AbortError') throw error
    if (error instanceof BrowserEvidenceError) throw error
    throw new BrowserEvidenceError(error?.message || '浏览器处理测速失败')
  } finally {
    input.dispose()
  }
}

async function streamAudio(input, audioTrack, codec, writer, signal, onProgress) {
  const spec = audioOutput(codec, { streaming: true })
  const target = new AppendOnlyStreamTarget(writer.writableStream())
  const output = new Output({ format: spec.format, target })
  const conversion = await Conversion.init({
    input,
    output,
    tracks: 'primary',
    video: { discard: true },
    copy: { mode: 'forced', shiftTolerance: 0 },
    tags: {},
  })
  if (!conversion.isValid || !conversion.utilizedTracks.includes(audioTrack)) {
    throw new BrowserEvidenceError('该音轨无法流式无损拆分')
  }
  const cancel = () => void conversion.cancel()
  signal?.addEventListener('abort', cancel, { once: true })
  conversion.onProgress = (progress) => {
    onProgress?.({ percent: Math.round(progress * 58), stage: '边拆分音频边上传' })
  }
  try {
    await conversion.execute()
    return await writer.close()
  } finally {
    signal?.removeEventListener('abort', cancel)
  }
}

async function collectFramesStreaming(videoTrack, duration, writer, signal, onProgress) {
  const sink = new VideoSampleSink(videoTrack, { hardwareAcceleration: 'prefer-hardware' })
  const denseFrames = []
  const keyframes = []
  const batch = {}
  let batchCount = 0

  const flush = async () => {
    if (!batchCount) return
    const zipped = zipSync(batch, { level: 0 })
    await writer.writePart(zipped)
    for (const key of Object.keys(batch)) delete batch[key]
    batchCount = 0
  }
  const append = async (name, blob) => {
    batch[name] = new Uint8Array(await blob.arrayBuffer())
    batchCount += 1
    if (batchCount >= 40) await flush()
  }

  const denseTimes = denseTimestamps(duration)
  let index = 0
  for await (const sample of sink.samplesAtTimestamps(denseTimes)) {
    ensureNotAborted(signal)
    const expectedTime = denseTimes[index]
    if (!sample) throw new BrowserEvidenceError(`无法读取 ${expectedTime.toFixed(1)} 秒画面`)
    try {
      const name = `dense/${String(index).padStart(5, '0')}.jpg`
      await append(name, await sampleJpeg(sample, 160, 90, 0.58))
      denseFrames.push({ name, time_sec: Number(expectedTime.toFixed(3)) })
    } finally {
      sample.close()
    }
    index += 1
    onProgress?.({
      percent: 58 + Math.round((index / denseTimes.length) * 34),
      stage: '边抽取画面边上传',
    })
  }

  const keyTimes = keyframeTimestamps(duration)
  index = 0
  for await (const sample of sink.samplesAtTimestamps(keyTimes)) {
    ensureNotAborted(signal)
    const expectedTime = keyTimes[index]
    if (!sample) throw new BrowserEvidenceError(`无法读取 ${expectedTime.toFixed(1)} 秒关键画面`)
    try {
      const scale = Math.min(1, 1280 / Math.max(sample.displayWidth, 1))
      const width = Math.max(2, Math.round(sample.displayWidth * scale))
      const height = Math.max(2, Math.round(sample.displayHeight * scale))
      const name = `key/${String(index).padStart(2, '0')}.jpg`
      await append(name, await sampleJpeg(sample, width, height, 0.82))
      keyframes.push({ name, time_sec: Number(expectedTime.toFixed(3)) })
    } finally {
      sample.close()
    }
    index += 1
    onProgress?.({ percent: 92 + Math.round((index / keyTimes.length) * 7), stage: '上传关键画面' })
  }
  await flush()
  const completed = await writer.close()
  return { denseFrames, keyframes, ...completed }
}

export async function streamBrowserEvidence(
  file,
  { taskId, session, descriptor, signal, onProgress } = {}
) {
  ensureNotAborted(signal)
  const audioInput = new Input({ formats: ALL_FORMATS, source: new BlobSource(file) })
  try {
    const audioTrack = await audioInput.getPrimaryAudioTrack()
    if (!audioTrack) throw new BrowserEvidenceError('视频中没有音轨')
    const audioWriter = new StreamingPartWriter({
      taskId,
      kind: 'audio',
      session,
      signal,
    })
    const audio = await streamAudio(
      audioInput,
      audioTrack,
      descriptor.codec,
      audioWriter,
      signal,
      onProgress
    )
    ensureNotAborted(signal)

    const frameInput = new Input({ formats: ALL_FORMATS, source: new BlobSource(file) })
    try {
      const videoTrack = await frameInput.getPrimaryVideoTrack()
      if (!videoTrack) throw new BrowserEvidenceError('视频中没有画面轨道')
      const frameWriter = new StreamingPartWriter({
        taskId,
        kind: 'frames',
        session,
        signal,
        concurrency: 2,
      })
      const frames = await collectFramesStreaming(
        videoTrack,
        descriptor.durationSec,
        frameWriter,
        signal,
        onProgress
      )
      const manifest = {
        version: 1,
        original_filename: file.name,
        original_size: file.size,
        duration_sec: Number(descriptor.durationSec.toFixed(3)),
        interval_sec: DENSE_INTERVAL_SEC,
        audio_codec: descriptor.codec,
        audio_size: audio.generatedBytes,
        dense_frames: frames.denseFrames,
        keyframes: frames.keyframes,
      }
      onProgress?.({ percent: 100, stage: '快速材料上传完成' })
      return {
        manifest,
        audioParts: audio.partCount,
        frameParts: frames.partCount,
        evidenceBytes: audio.generatedBytes + frames.generatedBytes,
      }
    } finally {
      frameInput.dispose()
    }
  } catch (error) {
    if (error?.name === 'AbortError' || error?.name === 'ConversionCanceledError') {
      throw new DOMException('操作已取消', 'AbortError')
    }
    if (error instanceof BrowserEvidenceError) throw error
    throw new BrowserEvidenceError(error?.message || '边提取边上传失败')
  } finally {
    audioInput.dispose()
  }
}
