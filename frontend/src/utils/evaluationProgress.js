export function materialsReady(task) {
  return Boolean(task && ['queued', 'processing', 'completed', 'failed'].includes(task.status))
}

export function evaluationBanner(task, { localUploading = false, remote = false } = {}) {
  if (!task) return null
  if (task.status === 'completed') return { tone: 'done', title: '评估完成', sub: '完整评估报告已生成，可前往结果页查看' }
  if (task.status === 'upload_failed') return { tone: 'fail', title: '材料传输失败', sub: task.error || '材料传输过程中出错' }
  if (task.status === 'failed') return { tone: 'fail', title: '评估失败', sub: task.error || '评估过程中出错' }
  if (task.status === 'cancelled') return { tone: 'fail', title: '任务已停止', sub: '该任务未继续执行' }
  if (task.status === 'cancel_requested') return { tone: 'run', title: '正在停止', sub: '正在停止当前任务' }
  if (task.status === 'uploading' || (localUploading && !materialsReady(task))) {
    return { tone: 'run', title: '材料传输中', sub: remote || task.current_step === 'remote_downloading' ? '服务器正在下载视频并接收辅助材料' : '正在上传视频和辅助材料' }
  }
  if (task.status === 'queued') return { tone: 'run', title: '等待解析', sub: '材料已就绪，正在等待服务器开始解析' }
  if (task.status === 'processing') return {
    tone: 'run', title: task.current_step === 'report' ? '报告生成' : '解析中',
    sub: task.step_label || '正在处理材料', progress: task.progress ?? 0,
    progressNote: '评估阶段进度，不代表已耗时比例或剩余时间',
  }
  return null
}
