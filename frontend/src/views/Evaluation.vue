<template>
  <div class="eval">
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-inner">
        <div class="drawer-head">
          <span class="drawer-title">历史任务</span>
          <button class="icon-btn" type="button" title="收起" @click="sidebarOpen = false">
            <el-icon :size="18"><DArrowLeft /></el-icon>
          </button>
        </div>
        <div class="drawer-tools">
          <el-input
            v-model="taskQuery"
            placeholder="搜索历史任务"
            :prefix-icon="Search"
            clearable
          />
          <button class="new-eval-btn" type="button" @click="newEvaluation">
            <el-icon :size="16"><Plus /></el-icon>
            新建评估
          </button>
          <div class="filter-row">
            <button
              v-for="f in TASK_FILTERS"
              :key="f.key"
              type="button"
              class="filter-btn"
              :class="{ on: taskFilter === f.key }"
              @click="taskFilter = f.key"
            >
              {{ f.label }}
            </button>
          </div>
        </div>
        <div class="task-list">
          <div v-if="!tasks.length" class="empty-hint">暂无评估记录</div>
          <div v-else-if="!visibleGroups.length" class="empty-hint">没有匹配的任务</div>
          <section v-for="group in visibleGroups" :key="group.key" class="task-group">
            <div class="group-label">{{ group.label }}</div>
            <div
              v-for="t in group.items"
              :key="t.id"
              class="task"
              :class="{ active: t.id === activeId, running: isRunning(t) }"
              @click="selectTask(t.id)"
            >
              <el-icon class="task-icon" :size="18"><VideoCamera /></el-icon>
              <div class="task-body">
                <div class="task-name">{{ t.filename }}</div>
                <div v-if="isRunning(t)" class="task-run">
                  <span>评估中 {{ t.progress }}%</span>
                  <el-progress :percentage="t.progress" :stroke-width="4" :show-text="false" />
                  <div class="task-meta">{{ t.step_label }}{{ stepDetail(t) }}</div>
                </div>
                <div v-else class="task-status-row">
                  <span class="task-status" :class="t.status">{{ statusText(t.status) }}</span>
                  <span class="task-time">{{ formatTime(t.created_at) }}</span>
                </div>
                <div v-if="t.summary && t.status === 'completed'" class="task-meta">
                  {{ t.summary.score }} 分 · {{ t.summary.grade }}
                </div>
                <div v-if="t.error" class="task-error">{{ t.error }}</div>
              </div>
              <el-button
                v-if="isRunning(t)"
                text
                type="danger"
                size="small"
                class="task-stop"
                :loading="cancellingId === t.id"
                @click.stop="cancelTask(t.id)"
              >
                停止
              </el-button>
              <button
                class="del-btn"
                type="button"
                title="删除"
                @click.stop="removeTask(t)"
              >
                <el-icon :size="16"><Delete /></el-icon>
              </button>
            </div>
          </section>
        </div>
      </div>
    </aside>

    <div class="stage">
      <header v-if="!sidebarOpen" class="stage-top">
        <div class="top-left">
          <button class="icon-btn" type="button" title="历史任务" @click="sidebarOpen = true">
            <el-icon :size="20"><Tickets /></el-icon>
          </button>
          <button class="icon-btn" type="button" title="新建评估" @click="newEvaluation">
            <el-icon :size="20"><Plus /></el-icon>
          </button>
        </div>
      </header>

      <div class="stage-body">
        <div v-if="!result" class="workspace">
          <header class="page-head">
            <div>
              <h1>教学视频评估</h1>
              <p>上传课堂视频与辅助材料，获得多模态教学诊断</p>
            </div>
          </header>

          <section v-if="statusBanner" class="status-banner" :class="statusBanner.tone">
            <el-icon class="done-icon" :class="{ 'is-loading': statusBanner.tone === 'run' }" :size="36">
              <CircleCheckFilled v-if="statusBanner.tone === 'done'" />
              <CircleCloseFilled v-else-if="statusBanner.tone === 'fail'" />
              <Loading v-else />
            </el-icon>
            <div class="done-copy">
              <div class="done-title">{{ statusBanner.title }}</div>
              <div class="done-file">{{ activeTask?.filename }}</div>
              <div class="done-sub">{{ statusBanner.sub }}</div>
              <el-progress
                v-if="statusBanner.progress != null"
                :percentage="statusBanner.progress"
                :stroke-width="8"
                class="status-bar"
              />
            </div>
            <div class="done-actions">
              <el-button
                v-if="statusBanner.tone === 'run'"
                type="primary"
                :loading="cancellingId === activeTask?.id"
                @click="cancelTask(activeTask.id)"
              >
                停止
              </el-button>
              <el-button v-else type="primary" @click="newEvaluation">重新评估</el-button>
              <el-button v-if="statusBanner.tone === 'done'" type="primary" @click="viewResult">
                查看评估结果
              </el-button>
            </div>
          </section>

          <section class="compose">
            <div class="video-slot">
              <div v-if="videoFile" class="ready-card video-ready">
                <div class="slot-head">
                  课堂视频
                  <span class="req-tag">必填</span>
                  <div class="head-actions">
                    <button v-if="videoUrl" type="button" class="text-act" @click="previewOpen = true">
                      <el-icon :size="14"><View /></el-icon>
                      预览
                    </button>
                    <template v-if="!reviewing">
                      <button type="button" class="text-act" @click="pickVideo">
                        <el-icon :size="14"><RefreshRight /></el-icon>
                        更换
                      </button>
                      <button type="button" class="text-act" @click="clearVideo">
                        <el-icon :size="14"><Delete /></el-icon>
                        删除
                      </button>
                    </template>
                  </div>
                </div>
                <div class="video-body">
                  <div class="thumb">
                    <img v-if="videoPoster" :src="videoPoster" alt="" />
                    <span v-if="videoDuration" class="dur">{{ videoDuration }}</span>
                  </div>
                  <div class="video-info">
                    <div class="fname">{{ videoFile.name }}</div>
                    <div v-if="videoMetaLine" class="fmeta">{{ videoMetaLine }}</div>
                    <div class="ok">
                      <el-icon :size="14"><CircleCheckFilled /></el-icon>
                      上传完成
                    </div>
                    <div class="bar-row">
                      <div class="bar"><i :style="{ width: (uploading ? uploadPercent : 100) + '%' }"></i></div>
                      <span>{{ uploading ? uploadPercent : 100 }}%</span>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else-if="reviewing" class="ready-card empty-view">
                <div class="slot-head">
                  课堂视频
                  <span class="req-tag">必填</span>
                </div>
                <div class="empty-slot">未上传</div>
              </div>
              <el-upload
                v-else
                drag
                class="video-drop"
                :auto-upload="false"
                :show-file-list="false"
                accept=".mp4,.avi,.mov,.mkv,.flv,.wmv,.webm,.m4v"
                :on-change="onVideoChange"
              >
                <div class="slot-head">
                  课堂视频
                  <span class="req-tag">必填</span>
                </div>
                <el-icon class="drop-icon" :size="36"><VideoCameraFilled /></el-icon>
                <div class="upload-text">
                  拖入视频文件，或<span class="pick">点击选择</span>
                </div>
                <div class="upload-hint">支持 MP4、MOV、MKV 等格式，建议上传 5–90 分钟的视频</div>
              </el-upload>
            </div>

            <div class="aux-row">
              <div v-if="coursewareFile" class="aux-slot filled">
                <div class="slot-head">
                  教学课件
                  <span class="opt-tag">选填</span>
                </div>
                <div class="aux-file">
                  <div class="type-badge" :class="fileKind(coursewareFile).tone">
                    {{ fileKind(coursewareFile).label }}
                  </div>
                  <div class="aux-copy">
                    <div class="fname">{{ coursewareFile.name }}</div>
                      <div v-if="coursewareFile.size" class="fmeta">{{ formatSize(coursewareFile.size) }}</div>
                    <div class="ok">
                      <el-icon :size="14"><CircleCheckFilled /></el-icon>
                      上传完成
                    </div>
                  </div>
                </div>
                <div v-if="!reviewing" class="aux-actions">
                  <button type="button" class="text-act" @click="pickCourseware">
                    <el-icon :size="14"><RefreshRight /></el-icon>
                    更换
                  </button>
                  <button type="button" class="text-act" @click="coursewareFile = null">
                    <el-icon :size="14"><Delete /></el-icon>
                    删除
                  </button>
                </div>
              </div>
              <div v-else-if="reviewing" class="aux-slot empty-view">
                <div class="slot-head">
                  教学课件
                  <span class="opt-tag">选填</span>
                </div>
                <div class="empty-slot">未上传</div>
              </div>
              <el-upload
                v-else
                drag
                class="aux-drop"
                :auto-upload="false"
                :show-file-list="false"
                accept=".pdf,.pptx,.ppt"
                :on-change="onCoursewareChange"
              >
                <div class="slot-head">
                  教学课件
                  <span class="opt-tag">选填</span>
                </div>
                <svg class="aux-icon" viewBox="0 0 1024 1024" aria-hidden="true">
                  <path
                    fill="currentColor"
                    d="M96 128h287.872l128.384 128H928a32 32 0 0 1 32 32v576a32 32 0 0 1-32 32H96a32 32 0 0 1-32-32V160a32 32 0 0 1 32-32z"
                  />
                  <path class="chip" d="M160 192h197.504L485.76 320H864v64H460.76L332.5 256H160z" />
                </svg>
                <div class="upload-text">
                  拖入课件文件，或<span class="pick">点击选择</span>
                </div>
                <div class="upload-hint">支持 PDF / PPT / PPTX 格式</div>
              </el-upload>

              <div v-if="syllabusFile" class="aux-slot filled">
                <div class="slot-head">
                  课程大纲
                  <span class="opt-tag">选填</span>
                </div>
                <div class="aux-file">
                  <div class="type-badge" :class="fileKind(syllabusFile).tone">
                    {{ fileKind(syllabusFile).label }}
                  </div>
                  <div class="aux-copy">
                    <div class="fname">{{ syllabusFile.name }}</div>
                      <div v-if="syllabusFile.size" class="fmeta">{{ formatSize(syllabusFile.size) }}</div>
                    <div class="ok">
                      <el-icon :size="14"><CircleCheckFilled /></el-icon>
                      上传完成
                    </div>
                  </div>
                </div>
                <div v-if="!reviewing" class="aux-actions">
                  <button type="button" class="text-act" @click="pickSyllabus">
                    <el-icon :size="14"><RefreshRight /></el-icon>
                    更换
                  </button>
                  <button type="button" class="text-act" @click="syllabusFile = null">
                    <el-icon :size="14"><Delete /></el-icon>
                    删除
                  </button>
                </div>
              </div>
              <div v-else-if="reviewing" class="aux-slot empty-view">
                <div class="slot-head">
                  课程大纲
                  <span class="opt-tag">选填</span>
                </div>
                <div class="empty-slot">未上传</div>
              </div>
              <el-upload
                v-else
                drag
                class="aux-drop"
                :auto-upload="false"
                :show-file-list="false"
                accept=".pdf,.docx,.doc,.txt,.md,.html"
                :on-change="onSyllabusChange"
              >
                <div class="slot-head">
                  课程大纲
                  <span class="opt-tag">选填</span>
                </div>
                <svg class="aux-icon" viewBox="0 0 1024 1024" aria-hidden="true">
                  <path
                    fill="currentColor"
                    d="M160 64h480l256 256v608a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32z"
                  />
                  <path class="chip" d="M640 154.496 805.504 320H640z" />
                  <path class="chip" d="M320 320h160v64H320z" />
                  <path class="chip" d="M320 512h384v64H320z" />
                  <path class="chip" d="M320 704h384v64H320z" />
                </svg>
                <div class="upload-text">
                  拖入大纲文件，或<span class="pick">点击选择</span>
                </div>
                <div class="upload-hint">支持 PDF / Word / Markdown 格式</div>
              </el-upload>

              <div v-if="scriptFile" class="aux-slot filled">
                <div class="slot-head">
                  课堂讲稿
                  <span class="opt-tag">选填</span>
                </div>
                <div class="aux-file">
                  <div class="type-badge" :class="fileKind(scriptFile).tone">
                    {{ fileKind(scriptFile).label }}
                  </div>
                  <div class="aux-copy">
                    <div class="fname">{{ scriptFile.name }}</div>
                      <div v-if="scriptFile.size" class="fmeta">{{ formatSize(scriptFile.size) }}</div>
                    <div class="ok">
                      <el-icon :size="14"><CircleCheckFilled /></el-icon>
                      上传完成
                    </div>
                  </div>
                </div>
                <div v-if="!reviewing" class="aux-actions">
                  <button type="button" class="text-act" @click="pickScript">
                    <el-icon :size="14"><RefreshRight /></el-icon>
                    更换
                  </button>
                  <button type="button" class="text-act" @click="scriptFile = null">
                    <el-icon :size="14"><Delete /></el-icon>
                    删除
                  </button>
                </div>
              </div>
              <div v-else-if="reviewing" class="aux-slot empty-view">
                <div class="slot-head">
                  课堂讲稿
                  <span class="opt-tag">选填</span>
                </div>
                <div class="empty-slot">未上传</div>
              </div>
              <el-upload
                v-else
                drag
                class="aux-drop"
                :auto-upload="false"
                :show-file-list="false"
                accept=".pdf,.docx,.doc,.txt,.md,.html"
                :on-change="onScriptChange"
              >
                <div class="slot-head">
                  课堂讲稿
                  <span class="opt-tag">选填</span>
                </div>
                <svg class="aux-icon" viewBox="0 0 1024 1024" aria-hidden="true">
                  <path
                    fill="currentColor"
                    d="M160 64h704a32 32 0 0 1 32 32v832a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32z"
                  />
                  <path
                    fill="currentColor"
                    d="M96 192h128q32 0 32 32t-32 32H96q-32 0-32-32t32-32m0 192h128q32 0 32 32t-32 32H96q-32 0-32-32t32-32m0 192h128q32 0 32 32t-32 32H96q-32 0-32-32t32-32m0 192h128q32 0 32 32t-32 32H96q-32 0-32-32t32-32"
                  />
                  <path class="chip" d="M672 128h64v768h-64z" />
                </svg>
                <div class="upload-text">
                  拖入讲稿文件，或<span class="pick">点击选择</span>
                </div>
                <div class="upload-hint">支持 PDF / Word / TXT / Markdown 格式</div>
              </el-upload>
            </div>

            <div v-if="videoFile && !reviewing" class="eta-banner">
              <el-icon :size="16"><InfoFilled /></el-icon>
              系统将结合视频、课件、大纲与讲稿进行多模态分析，预计耗时 8–15 分钟。
            </div>

            <div v-if="!reviewing" class="compose-actions">
              <span class="foot-count">已选择 {{ materialCount }} / 4 项材料</span>
              <el-button :disabled="materialCount === 0" @click="clearMaterials">清空</el-button>
              <el-button type="primary" :loading="uploading" :disabled="!canStart" @click="startUpload">
                开始视频评估
              </el-button>
            </div>

            <input
              ref="videoPicker"
              type="file"
              accept=".mp4,.avi,.mov,.mkv,.flv,.wmv,.webm,.m4v"
              hidden
              @change="onVideoPicked"
            />
            <input
              ref="coursewarePicker"
              type="file"
              accept=".pdf,.pptx,.ppt"
              hidden
              @change="onCoursewarePicked"
            />
            <input
              ref="syllabusPicker"
              type="file"
              accept=".pdf,.docx,.doc,.txt,.md,.html"
              hidden
              @change="onSyllabusPicked"
            />
            <input
              ref="scriptPicker"
              type="file"
              accept=".pdf,.docx,.doc,.txt,.md,.html"
              hidden
              @change="onScriptPicked"
            />
            <el-dialog v-model="previewOpen" title="预览视频" width="720px" destroy-on-close>
              <video v-if="videoUrl" :src="videoUrl" controls class="preview-video"></video>
            </el-dialog>
          </section>
        </div>

        <div v-else class="result">
          <header class="report-head">
            <div>
              <h1>{{ reportTitle }}</h1>
              <p v-if="reportTime">生成于 {{ reportTime }}</p>
            </div>
            <div class="report-actions">
              <el-button @click="newEvaluation">
                <el-icon class="btn-ico"><RefreshRight /></el-icon>
                重新评估
              </el-button>
              <el-dropdown trigger="click" @command="onExport">
                <el-button class="export-btn">
                  导出报告
                  <el-icon class="btn-ico"><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="md" :disabled="!result.report">
                      诊断报告 Markdown
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </header>

          <nav class="report-tabs">
            <button
              v-for="tab in reportTabs"
              :key="tab.key"
              type="button"
              class="report-tab"
              :class="{ on: reportTab === tab.key }"
              @click="reportTab = tab.key"
            >
              {{ tab.label }}
            </button>
          </nav>

          <div v-show="reportTab === 'overview'" class="overview">
            <div class="overview-top">
              <div class="radar-card">
                <div class="radar-wrap">
                  <div ref="radarEl" class="radar"></div>
                  <div class="radar-center">
                    <div class="radar-score">{{ result.overall.score }}</div>
                    <div class="radar-lab">综合总分</div>
                    <div class="radar-grade">{{ result.overall.grade }} {{ result.overall.grade_label }}</div>
                  </div>
                </div>
                <div class="meta-row">
                  <span
                    v-for="(c, i) in overviewChips"
                    :key="i"
                    class="meta-chip"
                    :class="c.tone"
                  >
                    <el-icon v-if="c.check" :size="12"><CircleCheckFilled /></el-icon>
                    {{ c.text }}
                  </span>
                </div>
              </div>
              <div class="dim-card">
                <el-table :data="result.dimensions" size="small" class="dim-table">
                  <el-table-column prop="label" label="维度" width="100" />
                  <el-table-column label="得分" width="72" align="center">
                    <template #default="{ row }">
                      <span v-if="row.assessed">{{ row.score }}</span>
                      <span v-else class="na">—</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="等级" width="96" align="center">
                    <template #default="{ row }">
                      <span v-if="row.assessed" class="grade-pill" :class="row.grade">
                        {{ row.grade }} {{ row.grade_label || '' }}
                      </span>
                      <span v-else class="na">未评估</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="折算说明" min-width="180">
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
              </div>
            </div>

            <section class="digest-panel">
              <header class="digest-banner">
                <div class="digest-banner-left">
                  <h2>教学诊断摘要</h2>
                  <span class="digest-tag">基于五维评估</span>
                </div>
                <button type="button" class="digest-more" @click="reportTab = 'report'">
                  查看完整诊断报告
                  <el-icon :size="14"><ArrowRight /></el-icon>
                </button>
              </header>
              <div class="digest-cols">
                <div class="digest-block good">
                  <div class="digest-label">
                    <el-icon :size="18"><CircleCheckFilled /></el-icon>
                    <span>突出优点</span>
                    <em>{{ reportDigest.strengths.length }} 项</em>
                  </div>
                  <ul v-if="reportDigest.strengths.length">
                    <li v-for="(t, i) in reportDigest.strengths" :key="'s' + i">{{ t }}</li>
                  </ul>
                  <p v-else class="empty-hint">暂无</p>
                </div>
                <div class="digest-block warn">
                  <div class="digest-label">
                    <el-icon :size="18"><WarningFilled /></el-icon>
                    <span>主要问题</span>
                    <em>{{ reportDigest.issues.length }} 项</em>
                  </div>
                  <ul v-if="reportDigest.issues.length">
                    <li v-for="(t, i) in reportDigest.issues" :key="'i' + i">{{ t }}</li>
                  </ul>
                  <p v-else class="empty-hint">暂无</p>
                </div>
                <div class="digest-block bad">
                  <div class="digest-label">
                    <el-icon :size="18"><Aim /></el-icon>
                    <span>改进建议</span>
                    <em>{{ reportDigest.suggestions.length }} 项</em>
                  </div>
                  <ol v-if="reportDigest.suggestions.length">
                    <li v-for="(t, i) in reportDigest.suggestions" :key="'g' + i">
                      <i>{{ i + 1 }}</i>
                      <span>{{ t }}</span>
                    </li>
                  </ol>
                  <p v-else class="empty-hint">暂无</p>
                </div>
              </div>
            </section>
          </div>

          <section v-if="reportTab === 'indicators'" class="block">
            <el-collapse v-model="openDims">
              <el-collapse-item v-for="d in result.dimensions" :key="d.key" :name="d.key">
                <template #title>
                  <span class="dim-title">
                    {{ d.label }}
                    <span v-if="d.assessed" class="grade-pill" :class="d.grade">{{ d.score }} 分</span>
                    <span v-else class="grade-pill">未评估</span>
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

          <section v-else-if="reportTab === 'features'" class="block">
            <p class="feature-legend">
              色条是当前值在刻度上的位置；占比类按 0–100% 铺。浅色框是 rubric
              登记的理想区间，落入为绿、略偏为黄、明显偏离为红。
            </p>
            <div class="feature-cols">
              <div v-for="g in featureGroups" :key="g.key">
                <div class="feature-head">{{ g.label }}</div>
                <div class="feature-origin">{{ g.origin }}</div>
                <div
                  v-for="f in g.rows"
                  :key="f.key"
                  class="feature-item"
                  :class="f.meter.tone"
                >
                  <div class="feature-line">
                    <span>{{ f.label }}</span>
                    <b>{{ f.value }}{{ f.unit }}</b>
                  </div>
                  <div class="feature-meter" :title="f.meter.title">
                    <div class="feature-track">
                      <i class="feature-fill" :style="{ width: f.meter.pct + '%' }" />
                      <i
                        v-if="f.meter.idealBand"
                        class="feature-ideal"
                        :style="{
                          left: f.meter.idealBand.left + '%',
                          width: f.meter.idealBand.width + '%',
                        }"
                      />
                    </div>
                    <span v-if="f.meter.idealHint" class="feature-hint">{{ f.meter.idealHint }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section v-else-if="reportTab === 'courseware'" class="block">
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

          <section v-else-if="reportTab === 'frames'" class="block">
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

          <section v-else-if="reportTab === 'report'" class="block">
            <div class="markdown" v-html="reportHtml"></div>
          </section>

          <section v-else-if="reportTab === 'transcript'" class="block">
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
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from 'echarts'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import {
  Aim,
  ArrowDown,
  ArrowRight,
  CircleCheckFilled,
  CircleCloseFilled,
  DArrowLeft,
  Delete,
  InfoFilled,
  Loading,
  Plus,
  RefreshRight,
  Search,
  Tickets,
  VideoCamera,
  VideoCameraFilled,
  View,
  WarningFilled,
} from '@element-plus/icons-vue'
import { evaluationApi } from '../api/client'

const MODALITY_LABEL = { audio: '音频', text: '文本', vision: '图像' }
const MODALITY_TYPE = { audio: 'warning', text: 'success', vision: 'info' }
const CONF_LABEL = { high: '高', medium: '中', low: '低' }
const POLL_INTERVAL = 2500
const TASK_FILTERS = [
  { key: 'all', label: '全部' },
  { key: 'running', label: '进行中' },
  { key: 'completed', label: '已完成' },
  { key: 'failed', label: '失败' },
]

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

// 与 evaluation_rubric.yaml 的 ideal 对齐；旧任务结果没有 ideal 字段时用这里兜底
const FEATURE_IDEAL = {
  speech_rate: [200, 280],
  speech_rate_cv: [0, 20],
  speech_rate_late_ratio: [0.9, 1.15],
  filler_density: [0, 1.5],
}
const FEATURE_UNIT_CEILING = {
  '字/分钟': 360,
  '次/百字': 4,
  次: 16,
  人: 30,
  帧: 36,
  页: 36,
  秒: 16,
  Hz: 280,
  dB: 40,
}

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
const reportTab = ref('overview')

const uploading = ref(false)
const uploadPercent = ref(0)
const videoFile = ref(null)
const syllabusFile = ref(null)
const coursewareFile = ref(null)
const scriptFile = ref(null)
const videoPicker = ref(null)
const coursewarePicker = ref(null)
const syllabusPicker = ref(null)
const scriptPicker = ref(null)
const videoUrl = ref('')
const videoPoster = ref('')
const videoDuration = ref('')
const videoWidth = ref(0)
const videoHeight = ref(0)
const previewOpen = ref(false)
const cancellingId = ref(null)
const sidebarOpen = ref(true)
const taskQuery = ref('')
const taskFilter = ref('all')

const canStart = computed(() => Boolean(videoFile.value))
const materialCount = computed(() => {
  let n = 0
  if (videoFile.value) n += 1
  if (coursewareFile.value) n += 1
  if (syllabusFile.value) n += 1
  if (scriptFile.value) n += 1
  return n
})
const activeTask = computed(() => tasks.value.find((t) => t.id === activeId.value) || null)
const reviewing = computed(() => Boolean(activeId.value && !uploading.value))
const statusBanner = computed(() => {
  const t = activeTask.value
  if (!t || uploading.value) return null
  if (t.status === 'completed') {
    return { tone: 'done', title: '评估已完成', sub: '完整评估报告已生成，可前往结果页查看' }
  }
  if (t.status === 'failed') {
    return { tone: 'fail', title: '解析失败', sub: t.error || '评估过程中出错' }
  }
  if (t.status === 'cancelled') {
    return { tone: 'fail', title: '解析失败', sub: '任务已停止' }
  }
  if (t.status === 'processing' || t.status === 'queued') {
    const step = `${t.step_label || ''}${stepDetail(t)}`.trim()
    return {
      tone: 'run',
      title: '解析中',
      sub: step || '正在处理上传材料',
      progress: t.progress ?? 0,
    }
  }
  return null
})
const videoMetaLine = computed(() => {
  if (!videoFile.value) return ''
  const bits = []
  if (videoFile.value.size) bits.push(formatSize(videoFile.value.size))
  const ext = extOf(videoFile.value).toUpperCase()
  if (ext) bits.push(ext)
  if (videoWidth.value && videoHeight.value) bits.push(`${videoWidth.value} × ${videoHeight.value}`)
  return bits.join(' · ')
})

const radarEl = ref(null)
let radarChart = null
let pollTimer = null

const frameUrls = computed(() => result.value?.keyframes?.map((f) => f.url) || [])
const coursewareUrls = computed(() => result.value?.courseware_slides?.map((f) => f.url) || [])
const featureGroups = computed(() => {
  const groups = result.value?.objective_features || {}
  return FEATURE_GROUPS.map((g) => ({
    ...g,
    rows: (groups[g.key] || []).map((f) => ({ ...f, meter: featureMeter(f) })),
  })).filter((g) => g.rows.length)
})

function featureIdeal(f) {
  if (Array.isArray(f.ideal) && f.ideal.length === 2) {
    const lo = Number(f.ideal[0])
    const hi = Number(f.ideal[1])
    if (Number.isFinite(lo) && Number.isFinite(hi)) return [lo, hi]
  }
  return FEATURE_IDEAL[f.key] || null
}

function trimNum(n) {
  if (!Number.isFinite(n)) return String(n)
  if (Number.isInteger(n)) return String(n)
  return String(Math.round(n * 100) / 100)
}

function featureMeter(f) {
  const raw = Number(f.value)
  const n = Number.isFinite(raw) ? raw : 0
  const ideal = featureIdeal(f)
  const unit = f.unit || ''
  const key = f.key || ''
  let min = 0
  let max = 1
  if (unit === '%') {
    min = 0
    max = 100
  } else if (key === 'asr_confidence') {
    min = Math.min(-3, n)
    max = 0
  } else if (unit === 'dB' && n < 0) {
    min = Math.min(-60, n)
    max = 0
  } else if (unit === 'dB') {
    min = 0
    max = Math.max(40, n * 1.15)
  } else if (unit === '' && n >= 0 && n <= 1 && !ideal) {
    min = 0
    max = 1
  } else {
    const ceil = FEATURE_UNIT_CEILING[unit] ?? 10
    max = Math.max(ceil, Math.abs(n) * 1.15, 0.01)
    if (ideal) max = Math.max(max, Math.abs(ideal[1]) * 1.35, Math.abs(ideal[0]))
    min = Math.min(0, n, ideal ? ideal[0] : 0)
  }
  const span = max - min || 1
  const toPct = (x) => Math.min(100, Math.max(0, ((x - min) / span) * 100))
  const pct = Number.isFinite(raw) && raw !== 0 ? Math.max(toPct(n), 1.2) : toPct(n)
  let tone = 'neutral'
  if (ideal && Number.isFinite(raw)) {
    if (raw >= ideal[0] && raw <= ideal[1]) tone = 'good'
    else {
      const band = Math.max(ideal[1] - ideal[0], 1e-6)
      const dist = raw < ideal[0] ? ideal[0] - raw : raw - ideal[1]
      tone = dist / band <= 0.4 ? 'mid' : 'bad'
    }
  }
  let idealBand = null
  let idealHint = ''
  if (ideal) {
    const a = toPct(ideal[0])
    const b = toPct(ideal[1])
    idealBand = { left: Math.min(a, b), width: Math.max(Math.abs(b - a), 3) }
    idealHint = `理想 ${trimNum(ideal[0])}–${trimNum(ideal[1])}${unit}`
  }
  const title = ideal
    ? `当前 ${f.value}${unit}，刻度 ${trimNum(min)}–${trimNum(max)}${unit}，${idealHint}`
    : `当前 ${f.value}${unit}`
  return { pct, tone, idealBand, idealHint, title }
}

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

const reportTitle = computed(() => {
  const name = (activeTask.value?.filename || '课堂').replace(/\.[^.]+$/, '')
  return `${name} · 教学评估报告`
})
const reportTime = computed(() => formatDateTime(activeTask.value?.created_at))

const reportTabs = computed(() => {
  const r = result.value
  if (!r) return []
  const tabs = [{ key: 'overview', label: '综合总览' }]
  if (r.report) tabs.push({ key: 'report', label: '诊断报告' })
  tabs.push({ key: 'indicators', label: '二级指标' })
  if (featureGroups.value.length) tabs.push({ key: 'features', label: '客观特征' })
  if (r.courseware_slides?.length) tabs.push({ key: 'courseware', label: '课件观测' })
  if (r.keyframes?.length) tabs.push({ key: 'frames', label: '关键帧' })
  if (r.transcript?.full_text) tabs.push({ key: 'transcript', label: '转写文稿' })
  return tabs
})

const overviewChips = computed(() => {
  const r = result.value
  if (!r) return []
  const chips = [
    { text: `课堂时长 ${r.overall.duration_minutes} 分钟`, tone: 'time' },
    { text: r.source === 'video' ? '视频评估' : '讲稿评估', tone: 'source' },
    {
      text: `模态 ${(r.overall.modalities || []).map((m) => MODALITY_LABEL[m]).join('/')}`,
      tone: 'mod',
    },
  ]
  if (r.transcript_source === 'script') chips.push({ text: '已使用讲稿', tone: 'used', check: true })
  if (r.has_syllabus) chips.push({ text: '已对照课程大纲', tone: 'used', check: true })
  if (r.has_courseware) chips.push({ text: '已对照上传课件', tone: 'used', check: true })
  return chips
})

const reportDigest = computed(() => {
  const digest = { strengths: [], issues: [], suggestions: [] }
  const llm = result.value?.digest
  if (llm && (llm.strengths?.length || llm.issues?.length || llm.suggestions?.length)) {
    digest.strengths = (llm.strengths || []).slice(0, 2)
    digest.issues = (llm.issues || []).slice(0, 2)
    digest.suggestions = (llm.suggestions || []).slice(0, 2)
    return digest
  }
  const md = result.value?.report || ''
  for (const chunk of md.split(/^##\s+/m)) {
    const nl = chunk.indexOf('\n')
    const title = (nl >= 0 ? chunk.slice(0, nl) : chunk).trim()
    const body = nl >= 0 ? chunk.slice(nl).trim() : ''
    if (/突出优点/.test(title)) digest.strengths = extractMdItems(body).map((t) => briefLine(t))
    else if (/主要问题/.test(title)) digest.issues = extractMdItems(body).map((t) => briefLine(t))
    else if (/改进建议/.test(title)) digest.suggestions = extractMdItems(body).map((t) => briefLine(t))
  }
  if (!digest.strengths.length) {
    digest.strengths = (result.value?.dimensions || [])
      .flatMap((d) => d.indicators || [])
      .filter((i) => i.assessed)
      .sort((a, b) => (b.score || 0) - (a.score || 0))
      .slice(0, 2)
      .map((i) => `${i.label} ${i.score} 分`)
  }
  if (!digest.issues.length) {
    digest.issues = (result.value?.dimensions || [])
      .filter((d) => d.assessed && d.primary_issue)
      .slice(0, 2)
      .map((d) => briefLine(`${d.label}：${d.primary_issue}`))
  }
  if (!digest.suggestions.length) {
    digest.suggestions = (result.value?.dimensions || [])
      .flatMap((d) => d.indicators || [])
      .filter((i) => i.assessed && i.suggestion && i.suggestion !== '保持')
      .slice(0, 2)
      .map((i) => briefLine(i.suggestion))
  }
  digest.strengths = digest.strengths.filter(Boolean).slice(0, 2)
  digest.issues = digest.issues.filter(Boolean).slice(0, 2)
  digest.suggestions = digest.suggestions.filter(Boolean).slice(0, 2)
  return digest
})

function extractMdItems(body) {
  const tidy = (s) =>
    s
      .replace(/^(?:\d+[\.、．)]|[-*])\s*/, '')
      .replace(/^(?:首先|其次|再次|最后|此外)[，,]\s*/, '')
      .replace(/\*\*/g, '')
      .replace(/\n+/g, ' ')
      .trim()
  const useful = (s) => s && !/^[.…\-—\s]+$/.test(s)
  const items = body
    .split(/\n(?=(?:\d+[\.、．)]|[-*])\s*)/)
    .map(tidy)
    .filter(useful)
  if (items.length > 1) return items.slice(0, 2)
  const paras = body
    .split(/\n\n+|(?=(?:首先|其次|再次|最后)[，,])/)
    .map(tidy)
    .filter(useful)
  return (items.length ? items : paras).slice(0, 2)
}

function briefLine(text) {
  let t = String(text || '')
    .replace(/\*\*/g, '')
    .replace(/\s+/g, ' ')
    .replace(/^[.…]+/, '')
    .replace(/^(?:首先|其次|再次|最后|此外)[，,]\s*/, '')
    .trim()
  if (!t) return ''
  const titled = t.match(/^(.{2,16}?)[：:——]\s*(.+)$/)
  if (titled) t = titled[1]
  else {
    const stopped = t.match(/^(.+?[。！？；;])/)
    if (stopped && stopped[1].length >= 6) t = stopped[1]
  }
  t = t.replace(/[。！？；;：:]+$/, '')
  if (t.length > 28) return `${t.slice(0, 28)}…`
  return t
}

function formatDateTime(ts) {
  if (!ts) return ''
  const d = new Date(ts * 1000)
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`
}

function openIndicatorTab(key) {
  reportTab.value = 'indicators'
  openDims.value = [key]
}

function onExport(cmd) {
  if (cmd !== 'md' || !result.value?.report) return
  const blob = new Blob([result.value.report], { type: 'text/markdown;charset=utf-8' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `${reportTitle.value}.md`
  a.click()
  URL.revokeObjectURL(a.href)
}

const filteredTasks = computed(() => {
  const q = taskQuery.value.trim().toLowerCase()
  return tasks.value.filter((t) => {
    if (taskFilter.value === 'running' && !isRunning(t)) return false
    if (taskFilter.value === 'completed' && t.status !== 'completed') return false
    if (taskFilter.value === 'failed' && t.status !== 'failed' && t.status !== 'cancelled') return false
    if (q && !(t.filename || '').toLowerCase().includes(q)) return false
    return true
  })
})

const visibleGroups = computed(() => {
  const now = new Date()
  const start = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime() / 1000
  const running = []
  const today = []
  const earlier = []
  for (const t of filteredTasks.value) {
    if (isRunning(t)) running.push(t)
    else if ((t.created_at || 0) >= start) today.push(t)
    else earlier.push(t)
  }
  return [
    { key: 'running', label: '进行中', items: running },
    { key: 'today', label: '今天', items: today },
    { key: 'earlier', label: '更早', items: earlier },
  ].filter((g) => g.items.length)
})

// ---------------------------------------------------------------- 任务列表

function isRunning(t) {
  return t.status === 'processing' || t.status === 'queued'
}

function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts * 1000).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
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
  reportTab.value = 'overview'
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
  if (activeId.value && before !== 'completed' && after?.status === 'completed') {
    result.value = null
  }
  if (activeId.value && before !== 'cancelled' && after?.status === 'cancelled') {
    result.value = null
  }
}

async function selectTask(id) {
  activeId.value = id
  result.value = null
  const listed = tasks.value.find((t) => t.id === id)
  if (listed) applyTaskMaterials(listed)
  try {
    const task = await evaluationApi.getTask(id)
    applyTaskMaterials(task)
  } catch {
    /* 拦截器已提示 */
  }
}

function applyTaskMaterials(task) {
  clearMaterials()
  const m = task?.materials || {}
  if (m.video?.name) {
    videoFile.value = { name: m.video.name, size: m.video.size || 0 }
    bindRemoteVideo(task.id)
  }
  if (m.courseware?.name) {
    coursewareFile.value = { name: m.courseware.name, size: m.courseware.size || 0 }
  }
  if (m.syllabus?.name) {
    syllabusFile.value = { name: m.syllabus.name, size: m.syllabus.size || 0 }
  }
  if (m.script?.name) {
    scriptFile.value = { name: m.script.name, size: m.script.size || 0 }
  }
}

function bindRemoteVideo(taskId) {
  revokeVideoUrl()
  const url = `/api/evaluation/task/${taskId}/file/video`
  videoUrl.value = url
  const video = document.createElement('video')
  video.preload = 'metadata'
  video.muted = true
  video.src = url
  video.onloadedmetadata = () => {
    videoDuration.value = formatDuration(video.duration)
    videoWidth.value = video.videoWidth
    videoHeight.value = video.videoHeight
    video.currentTime = Math.min(1, video.duration * 0.1 || 0)
  }
  video.onseeked = () => {
    try {
      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth || 320
      canvas.height = video.videoHeight || 180
      canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height)
      videoPoster.value = canvas.toDataURL('image/jpeg', 0.7)
    } catch {
      /* 远程视频无法截帧时只显示文件名 */
    }
  }
}

async function viewResult() {
  if (!activeId.value) return
  try {
    const task = await evaluationApi.getTask(activeId.value)
    if (task.status === 'completed' && task.result) {
      result.value = task.result
      reportTab.value = 'overview'
      openDims.value = task.result.dimensions[0] ? [task.result.dimensions[0].key] : []
      await ensureRadar()
    } else {
      ElMessage.warning('评估尚未完成')
    }
  } catch {
    /* 拦截器已提示 */
  }
}

// ---------------------------------------------------------------- 上传

async function removeTask(t) {
  const running = isRunning(t)
  try {
    await ElMessageBox.confirm(
      running ? '该任务正在评估，删除后将停止并无法恢复。确定删除？' : '确定删除这个评估任务？',
      '提示',
      { type: 'warning' }
    )
  } catch {
    return
  }
  try {
    if (running) {
      try {
        await evaluationApi.cancelTask(t.id)
      } catch {
        /* 任务可能已结束 */
      }
    }
    await evaluationApi.deleteTask(t.id)
    ElMessage.success('已删除')
    if (activeId.value === t.id) newEvaluation()
    await loadTasks()
  } catch {
    /* 拦截器已提示 */
  }
}

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
  setVideo(file.raw)
}
function onCoursewareChange(file) {
  if (file?.raw) coursewareFile.value = file.raw
}
function onSyllabusChange(file) {
  if (file?.raw) syllabusFile.value = file.raw
}
function onScriptChange(file) {
  if (file?.raw) scriptFile.value = file.raw
}

function pickFrom(input) {
  input?.click()
}
function pickVideo() {
  pickFrom(videoPicker.value)
}
function pickCourseware() {
  pickFrom(coursewarePicker.value)
}
function pickSyllabus() {
  pickFrom(syllabusPicker.value)
}
function pickScript() {
  pickFrom(scriptPicker.value)
}

function takeFile(ev) {
  const file = ev.target.files?.[0] || null
  ev.target.value = ''
  return file
}
function onVideoPicked(ev) {
  const file = takeFile(ev)
  if (file) setVideo(file)
}
function onCoursewarePicked(ev) {
  const file = takeFile(ev)
  if (file) coursewareFile.value = file
}
function onSyllabusPicked(ev) {
  const file = takeFile(ev)
  if (file) syllabusFile.value = file
}
function onScriptPicked(ev) {
  const file = takeFile(ev)
  if (file) scriptFile.value = file
}

function extOf(file) {
  const name = file?.name || ''
  const i = name.lastIndexOf('.')
  return i >= 0 ? name.slice(i + 1).toLowerCase() : ''
}

function fileKind(file) {
  const ext = extOf(file)
  if (ext === 'ppt' || ext === 'pptx') return { label: 'PPT', tone: 'ppt' }
  if (ext === 'pdf') return { label: 'PDF', tone: 'pdf' }
  if (ext === 'doc' || ext === 'docx') return { label: 'DOC', tone: 'doc' }
  if (ext === 'txt' || ext === 'md') return { label: ext.toUpperCase(), tone: 'txt' }
  return { label: (ext || 'FILE').toUpperCase(), tone: 'file' }
}

function formatSize(bytes) {
  if (bytes >= 1024 ** 3) return `${(bytes / 1024 ** 3).toFixed(2)} GB`
  if (bytes >= 1024 ** 2) return `${(bytes / 1024 ** 2).toFixed(1)} MB`
  if (bytes >= 1024) return `${Math.round(bytes / 1024)} KB`
  return `${bytes} B`
}

function formatDuration(sec) {
  if (!Number.isFinite(sec) || sec < 0) return ''
  const m = Math.floor(sec / 60)
  const s = Math.floor(sec % 60)
  return `${m}:${String(s).padStart(2, '0')}`
}

function revokeVideoUrl() {
  if (videoUrl.value && videoUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(videoUrl.value)
  }
  videoUrl.value = ''
  videoPoster.value = ''
  videoDuration.value = ''
  videoWidth.value = 0
  videoHeight.value = 0
}

function setVideo(file) {
  videoFile.value = file
  revokeVideoUrl()
  if (!file) return
  const url = URL.createObjectURL(file)
  videoUrl.value = url
  const video = document.createElement('video')
  video.preload = 'metadata'
  video.muted = true
  video.src = url
  video.onloadedmetadata = () => {
    videoDuration.value = formatDuration(video.duration)
    videoWidth.value = video.videoWidth
    videoHeight.value = video.videoHeight
    video.currentTime = Math.min(1, video.duration * 0.1 || 0)
  }
  video.onseeked = () => {
    try {
      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth || 320
      canvas.height = video.videoHeight || 180
      canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height)
      videoPoster.value = canvas.toDataURL('image/jpeg', 0.7)
    } catch {
      /* 跨域或解码失败时没有封面，仍显示时长 */
    }
  }
}

function clearVideo() {
  videoFile.value = null
  previewOpen.value = false
  revokeVideoUrl()
}

function clearMaterials() {
  clearVideo()
  syllabusFile.value = null
  coursewareFile.value = null
  scriptFile.value = null
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
      },
      (p) => (uploadPercent.value = p)
    )
    ElMessage.success('上传成功，已加入评估队列')
    activeId.value = resp.task_id
    await loadTasks()
    const created = tasks.value.find((t) => t.id === resp.task_id)
    if (created) applyTaskMaterials(created)
  } catch {
    /* 拦截器已提示 */
  } finally {
    uploading.value = false
  }
}

// ---------------------------------------------------------------- 雷达图
// 总览用 v-show，刚切进来或结果页刚挂上时盒子宽度常为 0。ECharts 在 0 宽上
// init 会留下空白画布，所以要等量到尺寸再画，尺寸变化再 resize。

let radarRo = null

function renderRadar() {
  const el = radarEl.value
  if (!el || !result.value || reportTab.value !== 'overview') return
  if (el.clientWidth < 8 || el.clientHeight < 8) return
  // 未评估的维度不画进雷达图，否则会塌成一个 0 分尖角，视觉上极具误导性
  const dims = (result.value.dimensions || []).filter((d) => d.assessed)
  if (!radarChart || radarChart.getDom() !== el) {
    radarChart?.dispose()
    radarChart = echarts.init(el)
  }
  if (dims.length < 3) {
    radarChart.clear()
    return
  }
  radarChart.setOption(
    {
      tooltip: {},
      radar: {
        indicator: dims.map((d) => ({ name: d.label, max: 100 })),
        radius: '68%',
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
    },
    true
  )
  radarChart.resize()
}

function bindRadarObserver() {
  if (radarRo || !radarEl.value) return
  radarRo = new ResizeObserver(() => {
    if (reportTab.value !== 'overview' || !result.value) return
    if (!radarChart) renderRadar()
    else radarChart.resize()
  })
  radarRo.observe(radarEl.value)
}

async function ensureRadar() {
  await nextTick()
  bindRadarObserver()
  renderRadar()
  if (!radarChart) requestAnimationFrame(renderRadar)
}

function onResize() {
  radarChart?.resize()
}

watch(result, (r) => {
  if (!r) {
    radarChart?.dispose()
    radarChart = null
    return
  }
  if (reportTab.value === 'overview') ensureRadar()
})

watch(reportTab, (tab) => {
  if (tab === 'overview' && result.value) {
    radarChart?.dispose()
    radarChart = null
    ensureRadar()
  }
})

onMounted(() => {
  loadTasks()
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  clearTimeout(pollTimer)
  window.removeEventListener('resize', onResize)
  radarRo?.disconnect()
  radarRo = null
  radarChart?.dispose()
  revokeVideoUrl()
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
  width: 300px;
  border-right-color: #ececec;
}
.sidebar-inner {
  width: 300px;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.drawer-head {
  height: 56px;
  padding: 0 8px 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #303133;
  flex-shrink: 0;
}
.drawer-title {
  font-size: 18px;
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
.drawer-tools {
  padding: 0 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-shrink: 0;
}
.new-eval-btn {
  height: 36px;
  border: 1px solid #a61b1b;
  background: #fff;
  color: #a61b1b;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
}
.new-eval-btn:hover {
  background: #fdf4f4;
}
.filter-row {
  display: flex;
  gap: 4px;
}
.filter-btn {
  flex: 1;
  height: 28px;
  border: none;
  background: transparent;
  color: #8a8a8a;
  font-size: 13px;
  cursor: pointer;
  border-radius: 6px;
}
.filter-btn.on,
.filter-btn:hover {
  color: #a61b1b;
  background: #f5e6e6;
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

.workspace {
  width: 100%;
  max-width: 992px;
  margin: 0 auto;
  padding: 32px 56px 48px;
  box-sizing: border-box;
}

.page-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ececec;
  margin-bottom: 20px;
}
.page-head h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1f1f1f;
}
.page-head p {
  margin: 8px 0 0;
  font-size: 14px;
  color: #8a8a8a;
}

.status-banner,
.done-banner {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
  box-sizing: border-box;
  padding: 16px 20px;
  margin-bottom: 24px;
  background: #f3faf3;
  border-radius: 10px;
}
.status-banner.fail {
  background: #fef2f2;
}
.status-banner.run {
  background: #f7f7f8;
}
.done-icon {
  color: #2e8b57;
  flex-shrink: 0;
}
.status-banner.fail .done-icon {
  color: #c45656;
}
.status-banner.run .done-icon {
  color: #a61b1b;
}
.status-bar {
  margin-top: 10px;
  max-width: 360px;
}
.empty-slot {
  color: #c0c4cc;
  font-size: 13px;
  text-align: center;
  padding: 24px 0 16px;
}
.done-copy {
  min-width: 0;
  flex: 1;
}
.done-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f1f1f;
}
.done-file {
  margin-top: 2px;
  font-size: 13px;
  color: #303133;
}
.done-sub {
  margin-top: 2px;
  font-size: 12px;
  color: #8a8a8a;
}
.done-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.compose {
  padding-top: 4px;
}
.video-slot {
  margin-top: 8px;
}
.ready-card {
  border: 1px solid #e6e6e6;
  border-radius: 10px;
  background: #fff;
  padding: 14px 16px 16px;
}
.video-ready .slot-head {
  margin-bottom: 14px;
}
.head-actions {
  margin-left: auto;
  display: flex;
  gap: 14px;
}
.text-act {
  border: none;
  background: transparent;
  color: #606266;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  padding: 0;
}
.text-act:hover {
  color: #a61b1b;
}
.video-body {
  display: flex;
  gap: 16px;
  align-items: stretch;
}
.thumb {
  position: relative;
  width: 176px;
  height: 100px;
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  background: #1f1f1f;
}
.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.dur {
  position: absolute;
  right: 6px;
  bottom: 6px;
  background: rgba(0, 0, 0, 0.72);
  color: #fff;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 8px;
}
.video-info {
  min-width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.fname {
  font-size: 15px;
  font-weight: 600;
  color: #1f1f1f;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.fmeta {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}
.ok {
  margin-top: 6px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #2e8b57;
  font-size: 13px;
}
.bar-row {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.bar {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
}
.bar i {
  display: block;
  height: 100%;
  background: #a61b1b;
  border-radius: 8px;
}
.bar-row span {
  font-size: 12px;
  color: #909399;
  width: 40px;
  text-align: right;
}
.aux-slot.filled {
  align-items: stretch;
  text-align: left;
  justify-content: space-between;
}
.aux-file {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  width: 100%;
  margin-top: 8px;
}
.type-badge {
  width: 44px;
  height: 52px;
  border-radius: 6px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
}
.type-badge.ppt {
  background: #d24726;
}
.type-badge.pdf {
  background: #c0392b;
}
.type-badge.doc {
  background: #2b579a;
}
.type-badge.txt,
.type-badge.file {
  background: #6b7280;
}
.aux-copy {
  min-width: 0;
  flex: 1;
}
.aux-actions {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 14px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}
.eta-banner {
  margin-top: 16px;
  padding: 12px 14px;
  background: #f5f6f7;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #606266;
}
.eta-banner .el-icon {
  color: #409eff;
  flex-shrink: 0;
}
.preview-video {
  width: 100%;
  max-height: 70vh;
  background: #000;
}
.video-drop :deep(.el-upload),
.video-drop :deep(.el-upload-dragger) {
  width: 100%;
}
.video-drop :deep(.el-upload-dragger) {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 14px 20px 28px;
  border: 1px dashed #d8d8d8;
  border-radius: 10px;
  background: #fff;
}
.video-drop :deep(.el-upload-dragger:hover) {
  border-color: #a61b1b;
}
.video-drop .slot-head {
  align-self: flex-start;
  margin-bottom: 18px;
}
.aux-drop .slot-head {
  align-self: flex-start;
  margin-bottom: 18px;
}
.aux-drop :deep(.el-upload),
.aux-drop :deep(.el-upload-dragger) {
  width: 100%;
}
.aux-drop :deep(.el-upload-dragger) {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 14px 16px 28px;
  border: 1px dashed #d8d8d8;
  border-radius: 10px;
  background: #fff;
}
.aux-drop :deep(.el-upload-dragger:hover) {
  border-color: #a61b1b;
}
.drop-icon,
.aux-icon {
  color: #a61b1b;
  background: none;
  border: none;
  box-shadow: none;
}
svg.aux-icon {
  width: 36px;
  height: 36px;
  display: block;
  flex-shrink: 0;
  margin: 4px 0 8px;
}
svg.aux-icon .chip {
  fill: #fff;
}
.upload-text .pick {
  color: #a61b1b;
  text-decoration: underline;
  text-underline-offset: 2px;
}
.aux-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
  margin-top: 16px;
}
.aux-slot {
  min-width: 0;
  padding: 14px 16px 16px;
  border: 1px solid #e6e6e6;
  border-radius: 10px;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  text-align: left;
  gap: 10px;
}
.aux-slot .slot-head {
  align-self: flex-start;
  text-align: left;
  width: 100%;
}
.aux-upload,
.aux-upload :deep(.el-upload) {
  width: 100%;
}
.slot-head {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
}
.req-tag,
.opt-tag {
  margin-left: 8px;
  font-size: 11px;
  font-weight: 600;
  padding: 1px 8px;
  border-radius: 10px;
  line-height: 18px;
}
.req-tag {
  color: #a61b1b;
  background: #fff;
  border: 1px solid #a61b1b;
}
.opt-tag {
  color: #909399;
  background: #fff;
  border: 1px solid #dcdcdc;
}
.slot-hint {
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
}
.compose-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}
.foot-count {
  font-size: 13px;
  color: #8a8a8a;
}
@media (max-width: 960px) {
  .aux-row {
    grid-template-columns: 1fr;
  }
}

.block {
  padding: 28px 32px 32px;
  border-bottom: 1px solid #ececec;
}
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

.task-list {
  flex: 1;
  overflow-y: auto;
  padding: 4px 8px 16px;
}

/* 上传 */
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
.task-group + .task-group {
  margin-top: 8px;
}
.group-label {
  font-size: 12px;
  font-weight: 600;
  color: #8a8a8a;
  letter-spacing: 0.08em;
  padding: 8px 8px 4px;
}
.task {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 8px;
  border-top: 1px solid #ececec;
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
.task-icon {
  flex-shrink: 0;
  margin-top: 2px;
  color: #8a8a8a;
}
.task.active .task-icon,
.task.running .task-icon {
  color: #a61b1b;
}
.task-body {
  min-width: 0;
  flex: 1;
}
.task-name {
  font-size: 13px;
  color: #303133;
  letter-spacing: 0.02em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.task-stop {
  flex-shrink: 0;
}
.del-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  border-radius: 6px;
  color: #909399;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.del-btn:hover {
  background: #fff;
  color: #c45656;
}
.task-status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: 4px;
}
.task-status {
  font-size: 12px;
  color: #8a8a8a;
}
.task-status.completed {
  color: #2e8b57;
}
.task-status.failed,
.task-status.cancelled {
  color: #f56c6c;
}
.task-time {
  font-size: 11px;
  color: #a8abb2;
}
.task-run {
  margin-top: 6px;
  font-size: 12px;
  color: #a61b1b;
}
.task-meta {
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

.result {
  min-height: 100%;
  max-width: 1180px;
  margin: 0 auto;
  padding: 24px 32px 48px;
}

.report-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}
.report-head h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #1f1f1f;
}
.report-head p {
  margin: 6px 0 0;
  font-size: 13px;
  color: #8a8a8a;
}
.report-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}
.btn-ico {
  margin-right: 4px;
  vertical-align: middle;
}
.export-btn {
  color: #a61b1b;
  border-color: #a61b1b;
  background: #fff;
}
.export-btn:hover {
  color: #891616;
  border-color: #891616;
  background: #fdf4f4;
}

.report-tabs {
  display: flex;
  gap: 4px;
  margin-top: 18px;
  border-bottom: 1px solid #ececec;
}
.report-tab {
  height: 40px;
  padding: 0 14px;
  border: none;
  background: transparent;
  color: #606266;
  font-size: 14px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
}
.report-tab.on {
  color: #a61b1b;
  font-weight: 600;
  border-bottom-color: #a61b1b;
}

.overview-top {
  display: grid;
  grid-template-columns: 42fr 58fr;
  gap: 20px;
  margin-top: 20px;
  align-items: center;
}
.digest-panel {
  margin-top: 36px;
  border: 1px solid #f3d0d0;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
}
.radar-card,
.dim-card,
.panel {
  min-width: 0;
  background: #fff;
}
.radar-card,
.dim-card {
  padding: 0;
}
.panel {
  border: 1px solid #eeeeee;
  border-radius: 10px;
  padding: 16px;
}
.radar-wrap {
  position: relative;
}
.radar-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  padding-bottom: 8px;
}
.radar-score {
  font-size: 40px;
  font-weight: 800;
  color: #a61b1b;
  line-height: 1;
}
.radar-lab {
  margin-top: 4px;
  font-size: 12px;
  color: #8a8a8a;
}
.radar-grade {
  margin-top: 2px;
  font-size: 13px;
  font-weight: 600;
  color: #a61b1b;
}
.meta-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: -20px;
}
.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  width: fit-content;
  max-width: 100%;
  padding: 2px 8px;
  border: 1px solid transparent;
  border-radius: 999px;
  font-size: 12px;
  line-height: 20px;
  white-space: nowrap;
  background: #f5f5f5;
  color: #606266;
}
.meta-chip.time {
  background: #fff6e8;
  border-color: #eed9b3;
  color: #b87a12;
}
.meta-chip.source {
  background: #fdecec;
  border-color: #f3d0d0;
  color: #a61b1b;
}
.meta-chip.mod,
.meta-chip.used {
  background: #eaf6ee;
  border-color: #c8e6d2;
  color: #2e8b57;
}
.dim-table {
  width: 100%;
}
.grade-pill {
  display: inline-block;
  padding: 1px 8px;
  border-radius: 10px;
  font-size: 12px;
  line-height: 18px;
  background: #f5f5f5;
  color: #8a8a8a;
}
.grade-pill.A {
  background: #fdecec;
  color: #a61b1b;
}
.grade-pill.B {
  background: #fff4e8;
  color: #d48806;
}
.grade-pill.C {
  background: #fdf6ec;
  color: #e6a23c;
}
.grade-pill.D {
  background: #fef0f0;
  color: #f56c6c;
}
.mod-text {
  font-size: 12px;
  color: #8a8a8a;
}
.digest-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 18px;
  background: #a61b1b;
  color: #fff;
}
.digest-banner-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}
.digest-banner h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.02em;
}
.digest-tag {
  flex-shrink: 0;
  padding: 1px 8px;
  border: 1px solid rgba(255, 255, 255, 0.85);
  border-radius: 999px;
  font-size: 11px;
  line-height: 18px;
  color: #fff;
}
.digest-more {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  border: none;
  background: none;
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  padding: 0;
  white-space: nowrap;
}
.digest-cols {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  align-items: stretch;
}
.digest-block {
  min-width: 0;
  padding: 18px 20px 20px;
  border-right: 1px solid #f0e0e0;
}
.digest-block:last-child {
  border-right: none;
}
.digest-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: #1f1f1f;
  font-size: 15px;
  font-weight: 700;
}
.digest-label em {
  margin-left: auto;
  font-style: normal;
  font-size: 11px;
  font-weight: 600;
  line-height: 18px;
  padding: 0 7px;
  border-radius: 999px;
}
.digest-block.good .digest-label :deep(svg) {
  color: #2e8b57;
}
.digest-block.warn .digest-label :deep(svg) {
  color: #d48806;
}
.digest-block.bad .digest-label :deep(svg) {
  color: #a61b1b;
}
.digest-block.good em {
  background: #eaf6ee;
  color: #2e8b57;
}
.digest-block.warn em {
  background: #fff6e8;
  color: #d48806;
}
.digest-block.bad em {
  background: #fdecec;
  color: #a61b1b;
}
.digest-block ul,
.digest-block ol {
  width: 100%;
  margin: 0;
  padding: 0;
  list-style: none;
  color: #303133;
  font-size: 13px;
  line-height: 1.7;
}
.digest-block ul li,
.digest-block ol li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  overflow: visible;
  word-break: break-word;
}
.digest-block ul li::before {
  content: '';
  flex-shrink: 0;
  width: 6px;
  height: 6px;
  margin-top: 7px;
  border-radius: 50%;
}
.digest-block.good ul li::before {
  background: #2e8b57;
}
.digest-block.warn ul li::before {
  background: #d48806;
}
.digest-block ol li i {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  margin-top: 1px;
  border-radius: 50%;
  background: #a61b1b;
  color: #fff;
  font-size: 11px;
  font-style: normal;
  font-weight: 600;
  line-height: 1;
}
.digest-block li + li {
  margin-top: 10px;
}

@media (max-width: 1100px) {
  .overview-top,
  .digest-cols {
    grid-template-columns: 1fr;
  }
  .digest-block {
    border-right: none;
    border-bottom: 1px solid #f0e0e0;
  }
  .digest-block:last-child {
    border-bottom: none;
  }
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
  height: 360px;
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
.feature-legend {
  margin: 0 0 16px;
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
}
.feature-cols {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
  padding: 8px 0;
  border-bottom: 1px dashed #f0f0f0;
}
.feature-line {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  font-size: 13px;
  color: #606266;
}
.feature-line b {
  color: #303133;
  font-weight: 600;
  white-space: nowrap;
}
.feature-meter {
  margin-top: 6px;
}
.feature-track {
  position: relative;
  height: 8px;
  background: #f2f3f5;
  border-radius: 99px;
  overflow: hidden;
}
.feature-fill {
  position: relative;
  z-index: 1;
  display: block;
  height: 100%;
  border-radius: 99px;
  background: #c45656;
  max-width: 100%;
}
.feature-item.good .feature-fill {
  background: #2e8b57;
}
.feature-item.mid .feature-fill {
  background: #d48806;
}
.feature-item.bad .feature-fill {
  background: #a61b1b;
}
.feature-ideal {
  position: absolute;
  z-index: 2;
  top: 0;
  height: 100%;
  border: 1.5px solid rgba(46, 139, 87, 0.7);
  border-radius: 99px;
  box-sizing: border-box;
  pointer-events: none;
}
.feature-hint {
  display: block;
  margin-top: 4px;
  font-size: 11px;
  color: #b0b3b8;
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
