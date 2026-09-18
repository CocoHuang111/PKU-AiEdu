import { test } from 'node:test'
import assert from 'node:assert/strict'
import { evaluationBanner, materialsReady } from './evaluationProgress.js'

test('transfer and queue do not show evaluation percentages', () => {
  for (const status of ['uploading', 'queued']) {
    const banner = evaluationBanner({ status, progress: 80 })
    assert.equal(banner.progress, undefined)
  }
  assert.equal(evaluationBanner({ status: 'queued' }).title, '等待解析')
  assert.match(evaluationBanner({ status: 'uploading', current_step: 'remote_downloading' }).sub, /下载/)
})
test('processing and report distinguish stage progress from remaining time', () => {
  assert.equal(evaluationBanner({ status: 'processing', current_step: 'asr', progress: 45 }).title, '解析中')
  const banner = evaluationBanner({ status: 'processing', current_step: 'report', progress: 92 })
  assert.equal(banner.title, '报告生成')
  assert.equal(banner.progress, 92)
  assert.match(banner.progressNote, /不代表.*剩余时间/)
})
test('ready state follows server submission not exiting local upload', () => {
  for (const status of ['uploading', 'upload_failed', 'cancelled']) assert.equal(materialsReady({ status }), false)
  for (const status of ['queued', 'processing', 'completed', 'failed']) assert.equal(materialsReady({ status }), true)
  assert.equal(materialsReady(null), false)
  assert.equal(evaluationBanner({ status: 'failed', error: '错误' }).sub, '错误')
})
