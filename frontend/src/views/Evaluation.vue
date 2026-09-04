<template>
  <div class="eval">
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-inner">
        <div class="drawer-head">
          <span class="drawer-title">历史评估</span>
          <div class="drawer-actions">
            <button class="icon-btn" type="button" title="新建评估" @click="newEvaluation">
              <el-icon :size="18"><Plus /></el-icon>
            </button>
            <button class="icon-btn" type="button" title="收起" @click="sidebarOpen = false">
              <el-icon :size="18"><Close /></el-icon>
            </button>
          </div>
        </div>
        <div class="task-list">
          <div v-if="!tasks.length" class="empty-hint">暂无评估记录</div>
          <div
            v-for="t in tasks"
            :key="t.id"
            class="task"
            :class="{ active: t.id === activeId }"
            @click="selectTask(t.id)"
          >
            <div class="task-top">
              <el-tag :type="statusType(t.status)" size="small">{{ statusText(t.status) }}</el-tag>
              <span class="task-name">{{ t.filename }}</span>
              <el-button
                v-if="t.status === 'processing' || t.status === 'queued'"
                text
                type="danger"
                size="small"
                class="task-stop"
                :loading="cancellingId === t.id"
                @click.stop="cancelTask(t.id)"
              >
                停止
              </el-button>
            </div>
            <el-progress
              v-if="t.status === 'processing' || t.status === 'queued'"
              :percentage="t.progress"
              :stroke-width="4"
              :show-text="false"
              style="margin: 6px 0 4px"
            />
            <div class="task-meta">
              <span>{{ t.step_label }}{{ stepDetail(t) }}</span>
              <span v-if="t.summary">{{ t.summary.score }} 分 · {{ t.summary.grade }}</span>
            </div>
            <div v-if="t.error" class="task-error">{{ t.error }}</div>
          </div>
        </div>
      </div>
    </aside>

    <div class="stage">
      <header class="stage-top">
        <div class="top-left">
          <template v-if="!sidebarOpen">
            <button
              class="icon-btn"
              type="button"
              title="历史评估"
              @click="sidebarOpen = true"
            >
              <el-icon :size="20"><Tickets /></el-icon>
            </button>
            <button class="icon-btn" type="button" title="新建评估" @click="newEvaluation">
              <el-icon :size="20"><Plus /></el-icon>
            </button>
          </template>
        </div>
        <div class="top-title">{{ pageTitle }}</div>
      </header>

      <div class="stage-body">
        <div v-if="!result" class="compose">
          <section class="block">
            <div class="block-title">上传评估材料</div>
            <p class="compose-lead">
              必须上传教学视频。课件、大纲、讲稿选填。有讲稿则直接当作转写，
              不再跑语音识别；没有讲稿才从视频做语音转写。
            </p>
            <div class="welcome-dims">
              <span v-for="d in DIM_LABELS" :key="d">{{ d }}</span>
            </div>
            <div class="slots">
              <div class="slot">
                <div class="slot-title">
                  视频
                  <span class="slot-flag">必填</span>
                </div>
                <el-upload
                  drag
                  :auto-upload="false"
                  :show-file-list="false"
                  accept=".mp4,.avi,.mov,.mkv,.flv,.wmv,.webm,.m4v"
                  :on-change="onVideoChange"
                >
                  <div class="upload-inner">
                    <div class="upload-text">{{ videoFile ? videoFile.name : '拖入教学视频或点击选择' }}</div>
                    <div class="upload-hint">mp4 / mov / mkv 等</div>
                  </div>
                </el-upload>
                <div v-if="videoFile" class="mat-file">
                  {{ videoFile.name }}
                  <el-button text size="small" @click="videoFile = null">清除</el-button>
                </div>
                <div class="slot-hint">抽取音轨、关键帧与课件切换，再按五维打分</div>
              </div>

              <div class="slot">
                <div class="slot-title">
                  课件
                  <span class="slot-flag optional">选填</span>
                </div>
                <el-upload
                  drag
                  :auto-upload="false"
                  :show-file-list="false"
                  accept=".pdf,.pptx,.ppt"
                  :on-change="onCoursewareChange"
                >
                  <div class="upload-inner">
                    <div class="upload-text">{{ coursewareFile ? coursewareFile.name : '拖入课件或点击选择' }}</div>
                    <div class="upload-hint">pdf / pptx / ppt</div>
                  </div>
                </el-upload>
                <div v-if="coursewareFile" class="mat-file">
                  {{ coursewareFile.name }}
                  <el-button text size="small" @click="coursewareFile = null">清除</el-button>
                </div>
                <div class="slot-hint">有则评版式与可读性；没有则根据课堂关键帧判断</div>
              </div>

              <div class="slot">
                <div class="slot-title">
                  大纲
                  <span class="slot-flag optional">选填</span>
                </div>
                <el-upload
                  drag
                  :auto-upload="false"
                  :show-file-list="false"
                  accept=".pdf,.docx,.doc,.txt,.md,.html"
                  :on-change="onSyllabusChange"
                >
                  <div class="upload-inner">
                    <div class="upload-text">{{ syllabusFile ? syllabusFile.name : '拖入课程大纲或点击选择' }}</div>
                    <div class="upload-hint">pdf / Word / txt / md</div>
                  </div>
                </el-upload>
                <div v-if="syllabusFile" class="mat-file">
                  {{ syllabusFile.name }}
                  <el-button text size="small" @click="syllabusFile = null">清除</el-button>
                </div>
                <div class="slot-hint">有则对照安排评完整性；没有则看讲稿或转写是否闭环</div>
              </div>

              <div class="slot">
                <div class="slot-title">
                  讲稿
                  <span class="slot-flag optional">选填</span>
                </div>
                <el-upload
                  drag
                  :auto-upload="false"
                  :show-file-list="false"
                  accept=".pdf,.docx,.doc,.txt,.md,.html"
                  :on-change="onScriptChange"
                >
                  <div class="upload-inner">
                    <div class="upload-text">{{ scriptFile ? scriptFile.name : '拖入讲稿或点击选择' }}</div>
                    <div class="upload-hint">pdf / Word / txt / md，后端当作转写</div>
                  </div>
                </el-upload>
                <div v-if="scriptFile" class="mat-file">
                  {{ scriptFile.name }}
                  <el-button text size="small" @click="scriptFile = null">清除</el-button>
                </div>
                <el-input
                  v-model="scriptText"
                  type="textarea"
                  :rows="4"
                  placeholder="也可直接粘贴讲稿文本…"
                  class="script-input"
                />
                <div class="slot-hint">有讲稿则跳过语音识别，直接用这份文本打分</div>
              </div>
            </div>
            <el-progress
              v-if="uploading"
              :percentage="uploadPercent"
              :stroke-width="6"
              style="margin-top: 16px"
            />
            <el-button
              type="primary"
              class="full-btn"
              :loading="uploading"
              :disabled="!canStart"
              @click="startUpload"
            >
              开始评估
            </el-button>
          </section>
        </div>

        <div v-else class="result">
          <section class="block score-block">
            <div class="score-value">{{ result.overall.score }}</div>
            <div class="score-grade">{{ result.overall.grade }} 级 · {{ result.overall.grade_label }}</div>
            <div class="score-meta">
              课堂时长 {{ result.overall.duration_minutes }} 分钟 ·
              {{ result.source === 'video' ? '视频评估' : '讲稿评估' }} ·
              模态 {{ (result.overall.modalities || []).map((m) => MODALITY_LABEL[m]).join('/') }}
              <el-tag v-if="result.transcript_source === 'script'" size="small" type="success" effect="plain" class="src-tag">已使用讲稿</el-tag>
              <el-tag v-if="result.has_syllabus" size="small" type="success" effect="plain" class="src-tag">已对照课程大纲</el-tag>
              <el-tag v-if="result.has_courseware" size="small" type="success" effect="plain" class="src-tag">已对照上传课件</el-tag>
              <el-tag
                v-if="result.overall.score_source === 'gb_llm_cls5'"
                size="small"
                type="warning"
                effect="plain"
                class="src-tag"
              >
                五维5分类 GB
              </el-tag>
            </div>
            <div
              v-if="result.overall.score_source === 'gb_llm_cls5' && result.overall.equal_weight_score != null"
              class="score-note"
            >
              总分由 v9 五维 5 分类 GB 校准；Judge 等权平均 {{ result.overall.equal_weight_score }}
            </div>
            <div v-if="result.overall.skipped_indicators" class="score-warn">
              {{ result.overall.skipped_indicators }} 个二级指标因缺少对应模态数据未参与评分
            </div>
          </section>

          <section class="block">
            <div class="block-title">五维得分</div>
            <div ref="radarEl" class="radar"></div>
            <el-table :data="result.dimensions" size="small">
              <el-table-column prop="label" label="维度" width="110" />
              <el-table-column label="得分" width="80" align="center">
                <template #default="{ row }">
                  <span v-if="row.assessed">{{ row.score }}</span>
                  <span v-else class="na">—</span>
                </template>
              </el-table-column>
              <el-table-column label="等级" width="80" align="center">
                <template #default="{ row }">
                  <el-tag v-if="row.assessed" :type="gradeType(row.grade)" size="small">
                    {{ row.grade }}
                  </el-tag>
                  <span v-else class="na">未评估</span>
                </template>
              </el-table-column>
              <el-table-column label="说明" min-width="240">
                <template #default="{ row }">
                  <div v-if="row.assessed && row.dimension_rationale" class="dim-rationale">
                    {{ row.dimension_rationale }}
                  </div>
                  <div v-else>{{ row.description }}</div>
                  <el-tag
                    v-if="row.score_source === 'weighted_fallback'"
                    size="small"
                    type="info"
                    effect="plain"
                    class="src-tag"
                  >
                    等权兜底{{ row.weighted_score != null ? ' ' + row.weighted_score : '' }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </section>

          <section class="block">
            <div class="block-title">二级指标明细</div>
            <el-collapse v-model="openDims">
              <el-collapse-item v-for="d in result.dimensions" :key="d.key" :name="d.key">
                <template #title>
                  <span class="dim-title">
                    {{ d.label }}
                    <el-tag v-if="d.assessed" :type="gradeType(d.grade)" size="small">
                      {{ d.score }} 分
                    </el-tag>
                    <el-tag v-else type="info" size="small">未评估</el-tag>
                    <el-tag v-if="d.skipped_count" type="info" size="small" effect="plain">
                      {{ d.skipped_count }} 项跳过
                    </el-tag>
                    <el-tag
                      v-if="d.score_source === 'weighted_fallback'"
                      type="info"
                      size="small"
                      effect="plain"
                    >
                      等权兜底
                    </el-tag>
                  </span>
                </template>
                <el-table :data="d.indicators" size="small" :row-class-name="rowClass">
                  <el-table-column prop="label" label="二级指标" width="120" />
                  <el-table-column label="模态" width="130">
                    <template #default="{ row }">
                      <el-tag
                        v-for="m in row.modalities"
                        :key="m"
                        size="small"
                        :type="MODALITY_TYPE[m]"
                        effect="plain"
                        class="modality-tag"
                      >
                        {{ MODALITY_LABEL[m] }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="得分" width="70" align="center">
                    <template #default="{ row }">
                      <span v-if="row.assessed">{{ row.score }}</span>
                      <span v-else class="na">—</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="置信" width="70" align="center">
                    <template #default="{ row }">
                      <span v-if="row.assessed" :class="'conf-' + row.confidence">
                        {{ CONF_LABEL[row.confidence] }}
                      </span>
                      <span v-else class="na">—</span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="evidence" label="评分依据" min-width="240" />
                  <el-table-column prop="suggestion" label="改进建议" min-width="200" />
                </el-table>
              </el-collapse-item>
            </el-collapse>
          </section>

          <section v-if="featureGroups.length" class="block">
            <div class="block-title">客观特征（事实层）</div>
            <div class="feature-cols">
              <div v-for="g in featureGroups" :key="g.key">
                <div class="feature-head">{{ g.label }}</div>
                <div class="feature-origin">{{ g.origin }}</div>
                <div v-for="f in g.rows" :key="f.key" class="feature-item">
                  <span>{{ f.label }}</span>
                  <b>{{ f.value }}{{ f.unit }}</b>
                </div>
              </div>
            </div>
          </section>

          <section v-if="result.courseware_slides?.length" class="block">
            <div class="block-title">上传课件页面观测（{{ result.courseware_slides.length }} 页）</div>
            <div class="frames">
              <div v-for="f in result.courseware_slides" :key="'cw-' + f.index" class="frame">
                <el-image :src="f.url" fit="cover" class="frame-img" :preview-src-list="coursewareUrls" :initial-index="f.index" />
                <div class="frame-time">第 {{ f.page }} 页</div>
                <div v-if="coursewareTags(f).length" class="frame-tags">
                  <el-tag v-for="t in coursewareTags(f)" :key="t.key" size="small" effect="plain" :type="t.type">
                    {{ t.text }}
                  </el-tag>
                </div>
                <div class="frame-desc">{{ f.labels?.note || f.description }}</div>
              </div>
            </div>
          </section>

          <section v-if="result.keyframes?.length" class="block">
            <div class="block-title">关键帧视觉观测（{{ result.keyframes.length }} 帧）</div>
            <div class="frames">
              <div v-for="f in result.keyframes" :key="f.index" class="frame">
                <el-image :src="f.url" fit="cover" class="frame-img" :preview-src-list="frameUrls" :initial-index="f.index" />
                <div class="frame-time">{{ f.timestamp }}</div>
                <div v-if="frameTags(f).length" class="frame-tags">
                  <el-tag v-for="t in frameTags(f)" :key="t.key" size="small" effect="plain" :type="t.type">
                    {{ t.text }}
                  </el-tag>
                </div>
                <div class="frame-desc">{{ f.labels?.note || f.description }}</div>
              </div>
            </div>
          </section>

          <section class="block">
            <div class="block-title">教学诊断报告</div>
            <div class="markdown" v-html="reportHtml"></div>
          </section>

          <section v-if="result.transcript?.full_text" class="block">
            <div class="block-head">
              <div class="block-title">语音转写文稿</div>
              <span class="transcript-meta">
                {{ result.transcript.language }} ·
                {{ Math.round(result.transcript.duration_sec / 60) }} 分钟 ·
                {{ result.transcript.full_text.length }} 字
              </span>
            </div>
            <el-collapse v-if="result.transcript.segments?.length">
              <el-collapse-item
                v-for="s in result.transcript.segments"
                :key="s.index"
                :title="`第 ${s.index + 1} 段 · ${s.time_range} · 语速 ${s.features.speech_rate} 字/分`"
                :name="s.index"
              >
                <div class="segment-text">{{ s.text }}</div>
              </el-collapse-item>
            </el-collapse>
            <div v-else class="segment-text">{{ result.transcript.full_text }}</div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { Close, Plus, Tickets } from '@element-plus/icons-vue'
import { evaluationApi } from '../api/client'

const DIM_LABELS = ['教学态度', '教学内容', '教学方法', '教学效果', '教学素质']
const MODALITY_LABEL = { audio: '音频', text: '文本', vision: '图像' }
const MODALITY_TYPE = { audio: 'warning', text: 'success', vision: 'info' }
const CONF_LABEL = { high: '高', medium: '中', low: '低' }
const POLL_INTERVAL = 2500

// 分组即证据来源。把来源标出来，是为了让人一眼看出哪些数字是算的、哪些是模型看的
const FEATURE_GROUPS = [
  { key: 'text', label: '文本特征', origin: '转写文本统计' },
  { key: 'audio', label: '声学特征', origin: 'librosa 音轨分析' },
  { key: 'timeline', label: '时序特征', origin: 'ASR 时间戳与解码指标' },
  { key: 'vision', label: '视觉观测统计', origin: 'VLM 逐帧标注后聚合' },
  { key: 'courseware', label: '上传课件观测', origin: '教师上传课件，VLM 逐页标注' },
  { key: 'slides', label: '课件时序特征', origin: '本地帧差检测，不经大模型' },
  { key: 'speakers', label: '说话人分离', origin: 'pyannote 分离统计' },
]

// 每帧最想一眼看到的四个标签
const FRAME_TAG_FIELDS = [
  { key: 'gaze', map: { students: '看学生', screen: '看屏幕', script: '看讲稿', audience_away: '背对学生' } },
  { key: 'gesture', map: { pointing: '指向板书', illustrative: '讲解手势', writing: '书写中', none: '无手势' } },
  { key: 'board_readable', map: { high: '可读性高', medium: '可读性中', low: '可读性低' } },
  { key: 'heads_up', map: { high: '抬头率高', medium: '抬头率中', low: '抬头率低' } },
]
const FRAME_TAG_TYPE = {
  看学生: 'success',
  讲解手势: 'success',
  指向板书: 'success',
  可读性高: 'success',
  抬头率高: 'success',
  看讲稿: 'danger',
  背对学生: 'danger',
  可读性低: 'danger',
  抬头率低: 'danger',
  无手势: 'warning',
}

const tasks = ref([])
const activeId = ref(null)
const result = ref(null)
const openDims = ref([])

const uploading = ref(false)
const uploadPercent = ref(0)
const videoFile = ref(null)
const syllabusFile = ref(null)
const coursewareFile = ref(null)
const scriptFile = ref(null)
const scriptText = ref('')
const cancellingId = ref(null)
const sidebarOpen = ref(true)

const canStart = computed(() => Boolean(videoFile.value))

const radarEl = ref(null)
let radarChart = null
let pollTimer = null

const frameUrls = computed(() => result.value?.keyframes?.map((f) => f.url) || [])
const coursewareUrls = computed(() => result.value?.courseware_slides?.map((f) => f.url) || [])
const featureGroups = computed(() => {
  const groups = result.value?.objective_features || {}
  return FEATURE_GROUPS.map((g) => ({ ...g, rows: groups[g.key] || [] })).filter(
    (g) => g.rows.length
  )
})

function coursewareTags(slide) {
  const labels = slide.labels || {}
  const map = {
    layout: { clear: '版式清楚', cluttered: '版式拥挤', mixed: '版式一般' },
    density: { sparse: '留白充足', moderate: '密度适中', text_heavy: '文字过密' },
    readable: { high: '可读性高', medium: '可读性中', low: '可读性低' },
  }
  const typeMap = {
    版式清楚: 'success',
    留白充足: 'success',
    可读性高: 'success',
    版式拥挤: 'danger',
    文字过密: 'danger',
    可读性低: 'danger',
  }
  return ['layout', 'density', 'readable']
    .map((key) => ({ key, text: map[key][labels[key]] }))
    .filter((t) => t.text)
    .map((t) => ({ ...t, type: typeMap[t.text] || 'info' }))
}

function frameTags(frame) {
  const labels = frame.labels || {}
  return FRAME_TAG_FIELDS.map(({ key, map }) => ({ key, text: map[labels[key]] }))
    .filter((t) => t.text)
    .map((t) => ({ ...t, type: FRAME_TAG_TYPE[t.text] || 'info' }))
}
const reportHtml = computed(() =>
  result.value?.report ? DOMPurify.sanitize(marked.parse(result.value.report)) : ''
)
const pageTitle = computed(() => {
  if (!activeId.value) return result.value ? '评估结果' : '新建评估'
  return tasks.value.find((t) => t.id === activeId.value)?.filename || '评估结果'
})

// ---------------------------------------------------------------- 任务列表

function statusType(s) {
  return { completed: 'success', processing: 'warning', failed: 'danger', cancelled: 'info' }[s] || 'info'
}
function statusText(s) {
  return { completed: '已完成', processing: '处理中', failed: '失败', queued: '排队中', cancelled: '已停止' }[s] || s
}
function gradeType(g) {
  return { A: 'success', B: '', C: 'warning', D: 'danger' }[g] || 'info'
}
function rowClass({ row }) {
  return row.assessed ? '' : 'row-skipped'
}

function stepDetail(t) {
  const d = t.step_detail || {}
  if (t.current_step === 'asr' && d.total_sec) {
    return `（${Math.round(d.done_sec / 60)}/${Math.round(d.total_sec / 60)} 分钟）`
  }
  if (t.current_step === 'vlm_describe' && d.total) return `（${d.done || 0}/${d.total}）`
  if (t.current_step === 'llm_judge' && d.dimension) return `（${d.dimension}）`
  return ''
}

function newEvaluation() {
  activeId.value = null
  result.value = null
  clearMaterials()
}

async function loadTasks() {
  try {
    tasks.value = await evaluationApi.listTasks()
    schedulePoll()
  } catch {
    /* 拦截器已提示 */
  }
}

function schedulePoll() {
  clearTimeout(pollTimer)
  const busy = tasks.value.some((t) => t.status === 'processing' || t.status === 'queued')
  if (busy) pollTimer = setTimeout(refreshRunning, POLL_INTERVAL)
}

async function refreshRunning() {
  const before = tasks.value.find((t) => t.id === activeId.value)?.status
  await loadTasks()
  const after = tasks.value.find((t) => t.id === activeId.value)
  // 当前选中的任务刚跑完，自动把结果拉出来
  if (activeId.value && before !== 'completed' && after?.status === 'completed') {
    selectTask(activeId.value)
  }
  if (activeId.value && before !== 'cancelled' && after?.status === 'cancelled') {
    result.value = null
  }
}

async function selectTask(id) {
  activeId.value = id
  try {
    const task = await evaluationApi.getTask(id)
    if (task.status === 'completed' && task.result) {
      result.value = task.result
      openDims.value = task.result.dimensions.map((d) => d.key)
      await nextTick()
      renderRadar()
    } else {
      result.value = null
      if (task.status === 'failed') {
        ElMessage.error(task.error || '任务失败')
      }
    }
  } catch {
    /* 拦截器已提示 */
  }
}

// ---------------------------------------------------------------- 上传

async function cancelTask(id) {
  cancellingId.value = id
  try {
    await evaluationApi.cancelTask(id)
    ElMessage.success('已请求停止诊断')
    await loadTasks()
    if (activeId.value === id) {
      result.value = null
    }
  } catch {
    /* 拦截器已提示 */
  } finally {
    cancellingId.value = null
  }
}

function onVideoChange(file) {
  videoFile.value = file.raw
}

function onSyllabusChange(file) {
  syllabusFile.value = file.raw
}

function onCoursewareChange(file) {
  coursewareFile.value = file.raw
}

function onScriptChange(file) {
  scriptFile.value = file.raw
}

function clearMaterials() {
  videoFile.value = null
  syllabusFile.value = null
  coursewareFile.value = null
  scriptFile.value = null
  scriptText.value = ''
}

async function startUpload() {
  if (!canStart.value) return
  uploading.value = true
  uploadPercent.value = 0
  try {
    const resp = await evaluationApi.uploadMaterials(
      {
        video: videoFile.value,
        syllabus: syllabusFile.value,
        courseware: coursewareFile.value,
        transcript: scriptFile.value,
        transcriptText: scriptText.value,
      },
      (p) => (uploadPercent.value = p)
    )
    ElMessage.success('上传成功，已加入评估队列')
    activeId.value = resp.task_id
    clearMaterials()
    await loadTasks()
  } catch {
    /* 拦截器已提示 */
  } finally {
    uploading.value = false
  }
}

// ---------------------------------------------------------------- 雷达图

function renderRadar() {
  if (!radarEl.value || !result.value) return
  radarChart ??= echarts.init(radarEl.value)
  // 未评估的维度不画进雷达图，否则会塌成一个 0 分尖角，视觉上极具误导性
  const dims = result.value.dimensions.filter((d) => d.assessed)
  if (dims.length < 3) {
    radarChart.clear()
    return
  }
  radarChart.setOption({
    tooltip: {},
    radar: {
      indicator: dims.map((d) => ({ name: d.label, max: 100 })),
      radius: '66%',
      axisName: { color: '#606266', fontSize: 13 },
      splitArea: { areaStyle: { color: ['#fff', '#fafafa'] } },
    },
    series: [
      {
        type: 'radar',
        areaStyle: { opacity: 0.25 },
        lineStyle: { color: '#a61b1b', width: 2 },
        itemStyle: { color: '#a61b1b' },
        data: [{ value: dims.map((d) => d.score), name: '本节课' }],
      },
    ],
  })
  radarChart.resize()
}

function onResize() {
  radarChart?.resize()
}

onMounted(() => {
  loadTasks()
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  clearTimeout(pollTimer)
  window.removeEventListener('resize', onResize)
  radarChart?.dispose()
})
</script>

<style scoped>
.eval {
  height: calc(100vh - 56px);
  display: flex;
  background: #fff;
  overflow: hidden;
}

.sidebar {
  width: 0;
  flex-shrink: 0;
  overflow: hidden;
  background: #f7f7f8;
  border-right: 1px solid transparent;
  transition: width 0.2s ease, border-color 0.2s ease;
}
.sidebar.open {
  width: 280px;
  border-right-color: #ececec;
}
.sidebar-inner {
  width: 280px;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.drawer-head {
  height: 64px;
  padding: 0 8px 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #303133;
  flex-shrink: 0;
  border-bottom: 1px solid #f0e0e0;
}
.drawer-title {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.02em;
  line-height: 1.2;
  color: #7b1113;
  position: relative;
  padding-left: 10px;
}
.drawer-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 4px;
  bottom: 4px;
  width: 3px;
  border-radius: 2px;
  background: #a61b1b;
}
.drawer-actions {
  display: flex;
  align-items: center;
}

.stage {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.stage-top {
  height: 52px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
}
.top-left {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-shrink: 0;
}
.top-title {
  min-width: 0;
  flex: 1;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.icon-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: 8px;
  color: #4b4b4b;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.icon-btn:hover {
  background: #f3f3f3;
}

.stage-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.block {
  padding: 28px 32px 32px;
  border-bottom: 1px solid #ececec;
}
.compose .block:last-child,
.result .block:last-child {
  border-bottom: none;
}
.block-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 14px;
}
.block-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}
.block-head .block-title {
  margin-bottom: 0;
}
.full-btn {
  width: 100%;
  margin-top: 12px;
}

.task-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px 8px 16px;
}

/* 上传 */
.upload-inner {
  padding: 18px 8px;
}
.upload-icon {
  font-size: 30px;
}
.upload-text {
  margin-top: 8px;
  font-size: 14px;
  color: #303133;
}
.upload-hint {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

/* 任务 */
.empty-hint {
  color: #909399;
  font-size: 13px;
  text-align: center;
  padding: 24px 0;
}
.task {
  padding: 10px 8px 10px 12px;
  border-radius: 10px;
  cursor: pointer;
}
.task:hover {
  background: #ececed;
}
.task.active {
  background: #f5e6e6;
}
.task.active .task-name {
  color: #7b1113;
}
.task-top {
  display: flex;
  align-items: center;
  gap: 8px;
}
.task-name {
  flex: 1;
  min-width: 0;
  font-size: 13px;
  color: #303133;
  letter-spacing: 0.02em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.task-stop {
  flex-shrink: 0;
  margin-left: auto;
}
.task-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
.task-error {
  font-size: 12px;
  color: #f56c6c;
  margin-top: 4px;
  word-break: break-all;
}

/* 上传 */
.compose,
.result {
  min-height: 100%;
}
.compose-lead {
  margin: 0 0 14px;
  color: #606266;
  font-size: 14px;
  line-height: 1.7;
}
.compose .welcome-dims {
  justify-content: flex-start;
  margin: 0 0 18px;
}

.slots {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px 32px;
}
.slot {
  min-width: 0;
}
.slot-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}
.slot-flag {
  margin-left: 8px;
  font-size: 12px;
  font-weight: 400;
  color: #a61b1b;
}
.slot-flag.optional {
  color: #909399;
}
.slot-hint {
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
  margin-top: 8px;
}
.script-input {
  margin-top: 10px;
}
@media (max-width: 800px) {
  .slots {
    grid-template-columns: 1fr;
  }
}
.welcome-dims {
  margin-top: 22px;
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}
.welcome-dims span {
  padding: 5px 14px;
  background: #f5e6e6;
  color: #a61b1b;
  border-radius: 14px;
  font-size: 13px;
}

/* 总分 */
.score-block {
  text-align: center;
}
.score-value {
  font-size: 60px;
  font-weight: 800;
  color: #a61b1b;
  line-height: 1.1;
}
.score-grade {
  font-size: 20px;
  color: #303133;
  margin-top: 4px;
}
.score-meta {
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
}
.src-tag {
  margin-left: 6px;
  vertical-align: middle;
}
.score-warn {
  font-size: 12px;
  color: #e6a23c;
  margin-top: 6px;
}
.score-note {
  font-size: 12px;
  color: #909399;
  margin-top: 6px;
}
.na {
  color: #c0c4cc;
}
:deep(.row-skipped) {
  background: #fafafa;
  color: #a8abb2;
}

.radar {
  height: 340px;
  margin-bottom: 12px;
}

.dim-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
}
.dim-rationale {
  color: #606266;
  line-height: 1.5;
}
.modality-tag {
  margin-right: 4px;
}
.conf-high {
  color: #67c23a;
}
.conf-medium {
  color: #e6a23c;
}
.conf-low {
  color: #f56c6c;
}

/* 客观特征 */
.feature-cols {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
}
.feature-head {
  font-size: 13px;
  font-weight: 600;
  color: #a61b1b;
  padding-bottom: 6px;
  border-bottom: 1px solid #f0e0e0;
}
.feature-origin {
  font-size: 11px;
  color: #b0b3b8;
  margin: 5px 0 6px;
}
.feature-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  font-size: 13px;
  color: #606266;
  border-bottom: 1px dashed #f0f0f0;
}
.feature-item b {
  color: #303133;
}

/* 关键帧 */
.frames {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 14px;
}
.frame {
  border: 1px solid #ebeef5;
  border-radius: 6px;
  overflow: hidden;
}
.frame-img {
  width: 100%;
  height: 130px;
  display: block;
}
.frame-time {
  padding: 6px 8px 0;
  font-size: 12px;
  font-weight: 600;
  color: #a61b1b;
}
.frame-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 6px 8px 0;
}
.frame-desc {
  padding: 4px 8px 8px;
  font-size: 12px;
  color: #606266;
  line-height: 1.6;
}

.mat-file {
  font-size: 12px;
  color: #606266;
  margin-top: 4px;
  word-break: break-all;
}

/* 报告 */
.markdown {
  font-size: 14px;
  line-height: 1.85;
  color: #303133;
}
.markdown :deep(h2) {
  font-size: 15px;
  color: #a61b1b;
  margin: 18px 0 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid #f0e0e0;
}
.markdown :deep(h2:first-child) {
  margin-top: 0;
}
.markdown :deep(ul),
.markdown :deep(ol) {
  padding-left: 22px;
}
.markdown :deep(li) {
  margin: 5px 0;
}
.markdown :deep(strong) {
  color: #a61b1b;
}

.transcript-meta {
  font-size: 12px;
  color: #909399;
}
.segment-text {
  font-size: 13px;
  line-height: 1.9;
  color: #606266;
  white-space: pre-wrap;
  background: #fafafa;
  padding: 12px;
  border-radius: 4px;
}
</style>
