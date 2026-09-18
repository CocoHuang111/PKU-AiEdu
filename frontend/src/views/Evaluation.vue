<template>
  <div class="eval">
    <el-dialog v-model="followupVisible" title="视频已提交，可离开此页面" width="min(540px, 92vw)">
      <p>视频已进入评估流程。{{ estimateText }}</p>
      <p class="upload-hint">预计时间仅供参考，视频时长及服务器负载会影响实际耗时。关闭页面不会停止处理，进度可在历史任务中查看。</p>
      <p>是否在报告完成后发送邮件通知？</p>
      <p v-if="mailStatus === 'waiting_service'" class="upload-hint">通知申请已保存；邮件服务尚未配置，暂不能发送。报告仍可在系统内查看。</p>
      <p v-else-if="mailStatus === 'pending'">已开启完成邮件通知。</p>
      <p v-else-if="mailStatus === 'sent'">报告通知已发送。</p>
      <el-button v-if="!['pending', 'sent', 'waiting_service'].includes(mailStatus)" :loading="mailSaving" @click="enableReportMail">是，完成后通知我</el-button>
      <el-button v-if="!['pending', 'sent', 'waiting_service'].includes(mailStatus)" @click="mailDeclined = true">{{ mailDeclined ? '已选择暂不需要' : '暂不需要' }}</el-button>
      <p>等待期间，是否先试试其他教学功能？</p>
      <el-button type="primary" @click="goToFeature('/qa')">前往智能问答</el-button>
      <el-button @click="goToFeature('/syllabus')">前往大纲优化</el-button>
      <template #footer><el-button @click="followupVisible = false">留在评估页面</el-button></template>
    </el-dialog>
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
                  <span>{{ taskRunningText(t) }} {{ taskProgress(t) }}%</span>
                  <el-progress :percentage="taskProgress(t)" :stroke-width="4" :show-text="false" />
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
                    <template v-if="!reviewing && !uploading">
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
                      <el-icon v-if="!preparingEvidence" :size="14"><CircleCheckFilled /></el-icon>
                      <el-icon v-else class="is-loading" :size="14"><Loading /></el-icon>
                      {{ videoStageText }}
                    </div>
                    <div class="bar-row">
                      <div class="bar"><i :style="{ width: videoProgress + '%' }"></i></div>
                      <span>{{ videoProgress }}%</span>
                    </div>
                  </div>
                </div>
                <div v-if="!reviewing" class="upload-mode-picker">
                  <button
                    type="button"
                    :class="{ active: uploadMode === 'fast' }"
                    :disabled="uploading"
                    @click="chooseUploadMode('fast')"
                  >
                    <strong>快速上传 <em v-if="recommendedUploadMode === 'fast'">推荐</em></strong>
                    <span>本机无损拆音频并抽取画面，上传量更小</span>
                  </button>
                  <button
                    type="button"
                    :class="{ active: uploadMode === 'original' }"
                    :disabled="uploading"
                    @click="chooseUploadMode('original')"
                  >
                    <strong>原视频上传 <em v-if="recommendedUploadMode === 'original'">推荐</em></strong>
                    <span>兼容性最好，网络较快或小文件时更合适</span>
                  </button>
                </div>
                <div v-if="evidenceSummary" class="evidence-summary">{{ evidenceSummary }}</div>
              </div>
              <div v-else-if="reviewing" class="ready-card empty-view">
                <div class="slot-head">
                  课堂视频
                  <span class="req-tag">必填</span>
                </div>
                <div class="empty-slot">未上传</div>
              </div>
              <div v-else class="video-source-card">
                <div class="slot-head">
                  课堂视频
                  <span class="req-tag">必填</span>
                </div>
                <div class="video-source-tabs">
                  <button
                    type="button"
                    :class="{ active: videoSource === 'file' }"
                    :disabled="uploading"
                    @click="chooseVideoSource('file')"
                  >
                    本地视频
                  </button>
                  <button
                    type="button"
                    :class="{ active: videoSource === 'link' }"
                    :disabled="uploading"
                    @click="chooseVideoSource('link')"
                  >
                    北大网盘链接
                  </button>
                </div>
                <el-upload
                  v-if="videoSource === 'file'"
                  drag
                  class="video-drop"
                  :auto-upload="false"
                  :show-file-list="false"
                  accept=".mp4,.avi,.mov,.mkv,.flv,.wmv,.webm,.m4v"
                  :on-change="onVideoChange"
                >
                  <el-icon class="drop-icon" :size="36"><VideoCameraFilled /></el-icon>
                  <div class="upload-text">
                    拖入视频文件，或<span class="pick">点击选择</span>
                  </div>
                  <div class="upload-hint">支持 MP4、MOV、MKV 等格式，建议上传 5–90 分钟的视频</div>
                </el-upload>
                <div v-else class="video-link-panel">
                  <el-icon class="link-icon" :size="34"><Link /></el-icon>
                  <div class="link-copy">粘贴北大网盘公开分享链接或视频下载地址</div>
                  <el-input
                    v-model="remoteVideoLink"
                    :disabled="uploading"
                    clearable
                    size="large"
                    placeholder="北大网盘公开分享链接或视频直链"
                    @keyup.enter="readRemoteShare()"
                  />
                  <el-button :loading="remoteShareLoading" :disabled="uploading || !validRemoteVideoLink"
                    @click="readRemoteShare()">读取链接</el-button>
                  <div class="upload-hint">
                    网盘导入目前仅支持北大网盘无需登录、无需访问密码的公开分享，且文件须允许下载。其他网盘请下载后本地上传。
                  </div>
                  <div v-if="remoteShare" class="remote-file-picker">
                    <div class="upload-hint">{{ remoteShare.provider_name }} · {{ remoteShare.notice }}</div>
                    <div v-if="remoteShare.configuration_message" class="link-error">{{ remoteShare.configuration_message }}</div>
                    <el-button v-if="remoteSharePath.length" text :disabled="uploading || remoteShareLoading"
                      @click="readRemoteShare(remoteSharePath.slice(0, -1))">返回上一级</el-button>
                    <div v-for="entry in remoteShare.files" :key="entry.id">
                      <el-button v-if="entry.is_dir" text :disabled="uploading || remoteShareLoading"
                        @click="readRemoteShare([...remoteSharePath, entry.id])">📁 {{ entry.name }}</el-button>
                      <el-radio v-else v-model="remoteShareFileId" :value="entry.id" :disabled="uploading || remoteShareLoading">
                        {{ entry.name }}{{ entry.size != null ? `（${formatSize(entry.size)}）` : '' }}
                      </el-radio>
                    </div>
                    <div v-if="remoteShare.provider !== 'direct' && !remoteShare.files.length" class="upload-hint">此目录没有可导入的视频或子目录</div>
                  </div>
                  <div v-if="remoteUrlError" class="link-error">{{ remoteUrlError }}</div>
                  <div v-if="isRemoteImport" class="remote-progress">
                    <div class="bar-row">
                      <div class="bar"><i :style="{ width: remoteImportProgress + '%' }"></i></div>
                      <span>{{ remoteImportProgress }}%</span>
                    </div>
                    <div class="remote-progress-text">
                      {{ activeTask?.step_label || '服务器正在读取链接' }}{{ activeTask ? stepDetail(activeTask) : '' }}
                    </div>
                  </div>
                </div>
              </div>
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

            <div v-if="(videoFile || validRemoteVideoLink) && !reviewing" class="eta-banner">
              <el-icon :size="16"><InfoFilled /></el-icon>
              {{ videoSource === 'link'
                ? '视频将由服务器直接下载，不占用本机上传带宽；链接失效或需要登录时将导入失败。'
                : uploadMode === 'fast'
                ? '快速上传不会压缩声音；如果当前浏览器不兼容，将自动回退为原视频上传。'
                : '系统将上传完整视频，网络较快或文件较小时更合适。' }}
            </div>

            <div v-if="!reviewing" class="compose-actions">
              <span class="foot-count">已选择 {{ materialCount }} / 4 项材料</span>
              <el-button :disabled="materialCount === 0 || uploading" @click="clearMaterials">清空</el-button>
              <el-button
                v-if="uploading"
                type="danger"
                plain
                :loading="Boolean(uploadTaskId && cancellingId === uploadTaskId)"
                @click="uploadTaskId ? cancelTask(uploadTaskId) : cancelLocalUpload()"
              >
                {{ uploadTaskId ? '停止任务' : '停止处理' }}
              </el-button>
              <el-button v-else type="primary" :disabled="!canStart" @click="startUpload">
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
                <el-button type="primary" class="export-btn">
                  导出报告
                  <el-icon class="btn-ico"><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="markdown" :disabled="!result.report">
                      Markdown (.md)
                    </el-dropdown-item>
                    <el-dropdown-item command="docx" :disabled="!result.report">
                      Word (.docx)
                    </el-dropdown-item>
                    <el-dropdown-item command="pdf" :disabled="!result.report">
                      PDF (.pdf)
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

          <section v-else-if="reportTab === 'features'" class="block feature-page">
            <nav class="feat-tabs">
              <button
                v-for="b in FEATURE_BUCKETS"
                :key="b.key"
                type="button"
                class="feat-tab"
                :class="{ on: featureSubTab === b.key, off: !bucketCount(b.key) }"
                @click="featureSubTab = b.key"
              >
                {{ b.label }}
                <em>{{ bucketCount(b.key) }}</em>
              </button>
              <button
                v-if="featureGroupMap.speakers?.rows.length"
                type="button"
                class="feat-tab"
                :class="{ on: featureSubTab === 'speakers' }"
                @click="featureSubTab = 'speakers'"
              >
                说话人
                <em>{{ featureGroupMap.speakers.rows.length }}</em>
              </button>
              <div class="feat-meta">
                <span>已获得 {{ featureGot }} / {{ featureExpected }} 项特征</span>
                <span v-if="!featureGroupMap.speakers?.rows.length">说话人分离未启用</span>
              </div>
            </nav>

            <div v-if="featureSubTab === 'content'" class="pace-page">
              <section class="pace-block">
                <header class="pace-head">
                  <p>基于语音转写与语义结构分析，已获得 {{ featureGroupMap.text?.rows.length || 0 }} / {{ featureGroupMap.text?.expected || 19 }} 项</p>
                </header>
                <div class="pace-heroes">
                  <div v-for="h in pacePage.textHeroes" :key="h.label" class="pace-hero">
                    <b>{{ h.value }}</b>
                    <span>
                      {{ h.label }}
                      <em v-if="h.tag" :class="'tone-' + h.tone">{{ h.tag }}</em>
                    </span>
                  </div>
                </div>
                <div class="pace-charts">
                  <figure>
                    <figcaption>课堂语速变化</figcaption>
                    <div class="pace-chart-frame">
                      <img
                        v-if="activeId"
                        :src="evaluationApi.chartUrl(activeId, 'speech_rate')"
                        alt="课堂语速变化"
                      />
                      <p v-else class="pace-hint">完成评估后显示语速折线</p>
                    </div>
                  </figure>
                  <figure>
                    <figcaption>提问结构</figcaption>
                    <div class="pace-chart-frame pace-chart-frame-fit">
                      <img
                        v-if="activeId"
                        :src="evaluationApi.chartUrl(activeId, 'question_structure')"
                        alt="提问结构"
                      />
                    </div>
                  </figure>
                </div>
                <div class="pace-detail">
                  <header class="pace-detail-head">
                    <h3>指标明细 <em>共 {{ pacePage.textCount }} 项</em></h3>
                    <div class="pace-detail-leg">
                      <span><i class="dot ok" />符合参考</span>
                      <span><i class="dot warn" />需要关注</span>
                      <span><i class="dot fact" />事实观察</span>
                    </div>
                  </header>

                  <section v-if="pacePage.textRows.length" class="pace-judge">
                    <table class="pace-table">
                      <thead>
                        <tr>
                          <th>指标</th>
                          <th>当前值</th>
                          <th>参考范围</th>
                          <th>状态</th>
                          <th>说明</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="r in pacePage.textRows" :key="r.key">
                          <td>{{ r.label }}</td>
                          <td>{{ r.value }}</td>
                          <td>{{ r.range }}</td>
                          <td><em :class="'tone-' + r.tone">{{ r.status }}</em></td>
                          <td>{{ r.note }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </section>

                  <section v-if="pacePage.textDonut || pacePage.textFacts.length" class="pace-obs">
                    <div class="pace-obs-body">
                      <div v-if="pacePage.textDonut" class="pace-donut-card">
                        <div class="pace-donut-wrap">
                          <svg viewBox="0 0 120 120" aria-hidden="true">
                            <circle cx="60" cy="60" r="42" pathLength="100" class="pace-donut-bg" />
                            <circle
                              cx="60"
                              cy="60"
                              r="42"
                              pathLength="100"
                              class="pace-donut-arc"
                              :stroke-dasharray="`${pacePage.textDonut.pct} ${100 - pacePage.textDonut.pct}`"
                            />
                          </svg>
                          <div class="pace-donut-label">
                            <b>{{ pacePage.textDonut.pctLabel }}</b>
                            <span>{{ pacePage.textDonut.label }}</span>
                          </div>
                        </div>
                        <p>课堂时长占比</p>
                      </div>
                      <div class="pace-obs-grid">
                        <div v-for="h in pacePage.textFacts" :key="h.key" class="pace-obs-item">
                          <span class="pace-obs-ico" v-html="paceObsIcon(h.key)" />
                          <div>
                            <b>{{ h.value }}</b>
                            <span>{{ h.label }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </section>
                </div>
              </section>
            </div>

            <div v-else-if="featureSubTab === 'audio'" class="pace-page">
              <section v-if="audioPage.got" class="pace-block">
                <header class="pace-head">
                  <p>
                    融合音轨声学分析、提问等待与转写时序质量，已获得
                    {{ audioPage.got }} / {{ audioPage.expected }} 项
                  </p>
                </header>
                <div class="pace-heroes">
                  <div v-for="h in audioPage.heroes" :key="h.label" class="pace-hero">
                    <b>{{ h.value }}</b>
                    <span>
                      {{ h.label }}
                      <em v-if="h.tag" :class="'tone-' + h.tone">{{ h.tag }}</em>
                    </span>
                  </div>
                </div>
                <div class="audio-charts">
                  <div class="audio-cap">音轨与声学变化</div>
                  <div class="audio-cap audio-cap-wait">
                    <b>提问等待</b>
                    <span v-if="audioPage.waitMean">平均 {{ audioPage.waitMean }}</span>
                    <span v-if="audioPage.waitMedian">中位数 {{ audioPage.waitMedian }}</span>
                  </div>
                  <div class="audio-cell audio-wave">
                    <img
                      v-if="activeId"
                      :src="evaluationApi.chartUrl(activeId, 'audio_wave')"
                      alt="音轨波形"
                    />
                  </div>
                  <div class="audio-cell audio-wait">
                    <img
                      v-if="activeId"
                      :src="evaluationApi.chartUrl(activeId, 'wait_samples')"
                      alt="提问等待样本"
                    />
                  </div>
                  <div class="audio-cell audio-line">
                    <span>响度变化</span>
                    <img
                      v-if="activeId"
                      :src="evaluationApi.chartUrl(activeId, 'loudness_series')"
                      alt="响度变化"
                    />
                  </div>
                  <div class="audio-cell audio-dist">
                    <div v-if="audioPage.waitQuality.length" class="audio-stack">
                      <span>等待质量分布</span>
                      <div class="audio-bar">
                        <i
                          v-for="s in audioPage.waitQuality"
                          :key="s.key"
                          :style="{ width: s.pct + '%', background: s.color }"
                        />
                      </div>
                      <ul>
                        <li v-for="s in audioPage.waitQuality" :key="s.key">
                          <i :style="{ background: s.color }" />
                          {{ s.label }}
                          <b>{{ s.pct }}%</b>
                        </li>
                      </ul>
                    </div>
                    <div v-if="audioPage.asrStack.length" class="audio-stack">
                      <span>ASR置信度分布</span>
                      <div class="audio-bar">
                        <i
                          v-for="s in audioPage.asrStack"
                          :key="s.key"
                          :style="{ width: s.pct + '%', background: s.color }"
                        />
                      </div>
                      <ul>
                        <li v-for="s in audioPage.asrStack" :key="s.key">
                          <i :style="{ background: s.color }" />
                          {{ s.label }}
                          <b>{{ s.pct }}%</b>
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="audio-cell audio-line">
                    <span>音高变化</span>
                    <img
                      v-if="activeId"
                      :src="evaluationApi.chartUrl(activeId, 'pitch_series')"
                      alt="音高变化"
                    />
                  </div>
                  <div class="audio-cell audio-facts">
                    <div v-for="h in audioPage.facts" :key="h.key" class="pace-obs-item">
                      <span class="pace-obs-ico" v-html="paceObsIcon(h.key)" />
                      <div>
                        <b>{{ h.value }}</b>
                        <span>{{ h.label }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="pace-detail">
                  <header class="pace-detail-head">
                    <h3>指标明细 <em>共 {{ audioPage.got }} 项</em></h3>
                    <div class="pace-detail-leg">
                      <span><i class="dot ok" />符合参考</span>
                      <span><i class="dot warn" />需要关注</span>
                      <span><i class="dot fact" />事实观察</span>
                    </div>
                  </header>

                  <section v-if="audioPage.judgeRows.length" class="pace-judge">
                    <table class="pace-table">
                      <thead>
                        <tr>
                          <th>指标</th>
                          <th>当前值</th>
                          <th>参考范围</th>
                          <th>状态</th>
                          <th>说明</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="r in audioPage.judgeRows" :key="r.key">
                          <td>{{ r.label }}</td>
                          <td>{{ r.value }}</td>
                          <td>{{ r.range }}</td>
                          <td><em :class="'tone-' + r.tone">{{ r.status }}</em></td>
                          <td>{{ r.note }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </section>
                </div>
              </section>
              <div v-else class="empty-hint">该组暂无特征</div>
            </div>

            <div v-else-if="featureSubTab === 'vision'" class="pace-page vision-page">
              <section v-if="visionPage.got" class="pace-block">
                <header class="pace-head">
                  <p>
                    基于课堂关键帧结构化观测，已获得
                    {{ visionPage.got }} / {{ visionPage.expected }} 项，已分析
                    {{ visionPage.frames }} 帧
                  </p>
                </header>
                <div class="pace-heroes">
                  <div v-for="h in visionPage.heroes" :key="h.label" class="pace-hero">
                    <b>{{ h.value }}</b>
                    <span>{{ h.label }}</span>
                  </div>
                </div>
                <div class="vision-mid">
                  <div class="vision-col">
                    <h3>课堂视觉状态分布</h3>
                    <div v-for="row in visionPage.stacks" :key="row.key" class="vision-stack-row">
                      <span>{{ row.label }}</span>
                      <div>
                        <div class="vision-bar">
                          <i
                            v-for="s in row.parts"
                            :key="s.key"
                            :style="{ width: s.width + '%', background: s.color }"
                            :title="s.label + ' ' + s.pct + '%'"
                          />
                        </div>
                        <ul>
                          <li v-for="s in row.parts" :key="s.key">
                            <i :style="{ background: s.color }" />
                            {{ s.label }} {{ trimNum(s.pct) }}%
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  <div class="vision-col">
                    <div
                      v-for="(c, i) in visionPage.conclusions"
                      :key="c.title"
                      class="vision-find"
                    >
                      <el-icon :size="20"><CircleCheckFilled /></el-icon>
                      <div>
                        <h4 :class="{ on: i === 0 }">{{ c.title }}</h4>
                        <p>{{ c.text }}</p>
                      </div>
                    </div>
                    <p v-if="!visionPage.conclusions.length" class="pace-hint">暂无足够数据生成结论</p>
                  </div>
                </div>
                <div class="pace-detail">
                  <header class="pace-detail-head">
                    <h3>指标明细 <em>共 {{ visionPage.rows.length }} 项</em></h3>
                    <div class="pace-detail-leg">
                      <span><i class="dot ok" />符合参考</span>
                      <span><i class="dot warn" />需要关注</span>
                      <span><i class="dot fact" />事实观察</span>
                    </div>
                  </header>
                  <section v-if="visionPage.rows.length" class="pace-judge">
                    <table class="pace-table">
                      <thead>
                        <tr>
                          <th>指标</th>
                          <th>当前值</th>
                          <th>参考范围</th>
                          <th>状态</th>
                          <th>说明</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="r in visionPage.rows" :key="r.key">
                          <td>{{ r.label }}</td>
                          <td>{{ r.value }}</td>
                          <td>{{ r.range }}</td>
                          <td><em :class="'tone-' + r.tone">{{ r.status }}</em></td>
                          <td>{{ r.note }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </section>
                </div>
              </section>
              <div v-else class="empty-hint">该组暂无特征</div>
            </div>

            <div v-else-if="featureSubTab === 'tools'" class="pace-page tools-page">
              <section v-if="toolsPage.got" class="pace-block">
                <header class="pace-head tools-head">
                  <p>{{ toolsPage.lead }}</p>
                  <em v-if="toolsPage.hasCw" class="tools-badge">已上传课件 · {{ toolsPage.pages }}页</em>
                </header>
                <div class="pace-heroes">
                  <div v-for="h in toolsPage.heroes" :key="h.label" class="pace-hero">
                    <b>{{ h.value }}</b>
                    <span>{{ h.label }}</span>
                  </div>
                </div>

                <template v-if="toolsPage.hasCw">
                  <div class="tools-mid">
                    <div class="tools-col tools-quality">
                      <h3>课件质量分布</h3>
                      <div v-for="row in toolsPage.stacks" :key="row.key" class="vision-stack-row">
                        <span>{{ row.label }}</span>
                        <div>
                          <div class="vision-bar">
                            <i
                              v-for="s in row.parts"
                              :key="s.key"
                              :style="{ width: s.width + '%', background: s.color }"
                              :title="s.label + ' ' + s.pct + '%'"
                            />
                          </div>
                          <ul>
                            <li v-for="s in row.parts" :key="s.key">
                              <i :style="{ background: s.color }" />
                              {{ s.label }} {{ trimNum(s.pct) }}%
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                    <div class="tools-col">
                      <h3>页面切换时间轴</h3>
                      <div class="tools-axis tools-axis-lg" v-if="toolsPage.timeline">
                        <svg :viewBox="`0 0 ${toolsPage.timeline.W} ${toolsPage.timeline.H}`" preserveAspectRatio="none">
                          <rect
                            :x="toolsPage.timeline.pad"
                            :y="toolsPage.timeline.trackY"
                            :width="toolsPage.timeline.inner"
                            :height="toolsPage.timeline.trackH"
                            rx="6"
                            fill="#f2f2f2"
                          />
                          <line
                            v-for="(t, i) in toolsPage.timeline.ticks"
                            :key="i"
                            :x1="t.x"
                            :x2="t.x"
                            :y1="toolsPage.timeline.tickY1"
                            :y2="toolsPage.timeline.tickY2"
                            stroke="#a61b1b"
                            stroke-width="1.8"
                          />
                          <text
                            v-for="lab in toolsPage.timeline.labels"
                            :key="lab.text"
                            :x="lab.x"
                            :y="toolsPage.timeline.labelY"
                            text-anchor="middle"
                            fill="#8a8a8a"
                            font-size="11"
                          >
                            {{ lab.text }}
                          </text>
                        </svg>
                        <p class="tools-axis-leg"><i />切换时刻</p>
                      </div>
                      <p v-else class="pace-hint">暂无切换时刻</p>
                      <div class="tools-minis">
                        <div v-for="m in toolsPage.minis" :key="m.key" class="pace-obs-item">
                          <span class="pace-obs-ico" v-html="paceObsIcon(m.key)" />
                          <div>
                            <b>{{ m.value }}</b>
                            <span>{{ m.label }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </template>

                <template v-else>
                  <div class="tools-axis-block">
                    <h3>页面切换时间轴</h3>
                    <div class="tools-axis" v-if="toolsPage.timeline">
                      <svg :viewBox="`0 0 ${toolsPage.timeline.W} ${toolsPage.timeline.H}`" preserveAspectRatio="none">
                        <rect
                          :x="toolsPage.timeline.pad"
                          :y="toolsPage.timeline.trackY"
                          :width="toolsPage.timeline.inner"
                          :height="toolsPage.timeline.trackH"
                          rx="5"
                          fill="#f2f2f2"
                        />
                        <line
                          v-for="(t, i) in toolsPage.timeline.ticks"
                          :key="i"
                          :x1="t.x"
                          :x2="t.x"
                          :y1="toolsPage.timeline.tickY1"
                          :y2="toolsPage.timeline.tickY2"
                          stroke="#a61b1b"
                          stroke-width="1.6"
                        />
                        <text
                          v-for="lab in toolsPage.timeline.labels"
                          :key="lab.text"
                          :x="lab.x"
                          :y="toolsPage.timeline.labelY"
                          text-anchor="middle"
                          fill="#8a8a8a"
                          font-size="11"
                        >
                          {{ lab.text }}
                        </text>
                      </svg>
                    </div>
                    <div v-if="toolsPage.axisNotes.length" class="tools-pills">
                      <span v-for="n in toolsPage.axisNotes" :key="n">{{ n }}</span>
                    </div>
                  </div>
                  <div class="tools-mid tools-mid-wide">
                    <div class="tools-col">
                      <h3>分段切换频率</h3>
                      <img
                        v-if="activeId"
                        class="tools-freq"
                        :src="evaluationApi.chartUrl(activeId, 'slide_freq')"
                        alt="分段切换频率"
                      />
                    </div>
                    <div class="tools-col tools-dwell">
                      <h3>页面停留时长分布</h3>
                      <div class="tools-dwell-body">
                        <div v-if="toolsPage.donut" class="tools-donut-wrap">
                          <div class="tools-donut" :style="{ background: toolsPage.donut.bg }" />
                          <div class="tools-donut-label">
                            <b>{{ toolsPage.donut.median }}</b>
                            <span>中位数</span>
                          </div>
                        </div>
                        <ul v-if="toolsPage.donut">
                          <li v-for="s in toolsPage.donut.parts" :key="s.key">
                            <i :style="{ background: s.color }" />
                            {{ s.label }} {{ trimNum(s.pct) }}%
                          </li>
                        </ul>
                        <div v-if="toolsPage.dwellNote" class="vision-find">
                          <el-icon :size="20"><CircleCheckFilled /></el-icon>
                          <div>
                            <h4>{{ toolsPage.dwellNote.title }}</h4>
                            <p>{{ toolsPage.dwellNote.text }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </template>

                <div class="pace-detail">
                  <header class="pace-detail-head">
                    <h3>指标明细 <em>共 {{ toolsPage.rows.length }} 项</em></h3>
                    <div class="pace-detail-leg">
                      <span><i class="dot ok" />符合参考</span>
                      <span><i class="dot warn" />需要关注</span>
                      <span><i class="dot fact" />事实观察</span>
                    </div>
                  </header>
                  <section v-if="toolsPage.rows.length" class="pace-judge">
                    <table class="pace-table">
                      <thead>
                        <tr>
                          <th>指标</th>
                          <th>当前值</th>
                          <th>参考范围</th>
                          <th>状态</th>
                          <th>说明</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="r in toolsPage.rows" :key="r.key">
                          <td>{{ r.label }}</td>
                          <td>{{ r.value }}</td>
                          <td>{{ r.range }}</td>
                          <td><em :class="'tone-' + r.tone">{{ r.status }}</em></td>
                          <td>{{ r.note }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </section>
                </div>
              </section>
              <div v-else class="empty-hint">该组暂无特征</div>
            </div>

            <div v-else class="feature-detail">
              <p class="feature-legend">
                {{ activeBucketLegend }}。色条是当前值在刻度上的位置；
                占比类按 0–100% 铺。浅色框是 rubric 登记的理想区间。
              </p>
              <div v-if="activeBucketSections.length" class="feature-cols single">
                <div v-for="sec in activeBucketSections" :key="sec.key">
                  <div class="feature-head">{{ sec.label }}</div>
                  <div
                    v-for="f in sec.rows"
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
              <div v-else class="empty-hint">该组暂无特征</div>
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
import { useRouter, useRoute } from 'vue-router'
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
  Link,
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

const router = useRouter()
const route = useRoute()
const followupVisible = ref(false)
const followupTask = ref(null)
const followupInfo = ref(null)
const mailStatus = ref('')
const mailDeclined = ref(false)
const mailSaving = ref(false)
const estimateText = computed(() => {
  if (followupInfo.value?.status === 'completed') return '评估已完成，可以查看报告。'
  const estimate = followupInfo.value?.estimate
  if (!estimate) return '预计时间暂不可用，请稍后查看任务进度。'
  return `${estimate.preliminary ? '初步估算' : '根据近期解析耗时估算'}，预计约 ${estimate.min_minutes}–${estimate.max_minutes} 分钟完成（含等待）。`
})

async function showFollowup(taskId) {
  followupTask.value = taskId
  followupInfo.value = null
  mailStatus.value = ''
  mailDeclined.value = false
  followupVisible.value = true
  try {
    const info = await evaluationApi.followUp(taskId)
    if (followupTask.value !== taskId) return
    followupInfo.value = info
    mailStatus.value = info.notification_status || ''
  } catch { /* 任务已成功提交，后续提示失败不影响解析 */ }
}

async function enableReportMail() {
  if (!followupTask.value) return
  mailSaving.value = true
  mailDeclined.value = false
  try {
    const info = await evaluationApi.followUp(followupTask.value)
    if (!info.has_email) {
      followupVisible.value = false
      await router.push({ path: '/profile', query: { reportMailTask: followupTask.value } })
      return
    }
    const response = await evaluationApi.requestEmail(followupTask.value)
    mailStatus.value = response.status
  } catch { /* 错误由公共拦截器提示 */ }
  finally { mailSaving.value = false }
}

function goToFeature(path) {
  followupVisible.value = false
  router.push(path)
}

// 分组即证据来源。把来源标出来，是为了让人一眼看出哪些数字是算的、哪些是模型看的
const FEATURE_GROUPS = [
  { key: 'text', label: '文本特征', short: '文本', expected: 19, origin: '转写文本统计' },
  { key: 'audio', label: '声学特征', short: '声学', expected: 10, origin: 'librosa 音轨分析' },
  { key: 'timeline', label: '时序特征', short: '时序', expected: 6, origin: 'ASR 时间戳与解码指标' },
  { key: 'vision', label: '视觉观测统计', short: '视觉', expected: 15, origin: 'VLM 逐帧标注后聚合' },
  { key: 'courseware', label: '上传课件观测', short: '课件', expected: 7, origin: '教师上传课件，VLM 逐页标注' },
  { key: 'slides', label: '课件时序特征', short: '切换', expected: 6, origin: '本地帧差检测，不经大模型' },
  { key: 'speakers', label: '说话人分离', short: '说话人', expected: 6, origin: 'pyannote 分离统计' },
]
const FEATURE_BUCKETS = [
  { key: 'content', label: '授课内容', sources: ['text'] },
  { key: 'audio', label: '声学特征', sources: ['audio', 'timeline'] },
  { key: 'vision', label: '课堂视觉', sources: ['vision'] },
  { key: 'tools', label: '工具调度', sources: ['courseware', 'slides'] },
]

// 与 evaluation_rubric.yaml 的 ideal 对齐；旧任务结果没有 ideal 字段时用这里兜底
const FEATURE_IDEAL = {
  speech_rate: [200, 280],
  speech_rate_cv: [0, 20],
  speech_rate_late_ratio: [0.9, 1.15],
  filler_density: [0, 1.5],
}
// 仅供授课内容 / 时序表明细展示，不进 Judge。有 rubric.ideal 的用 ideal。
const PACE_GUIDE = {
  speech_rate: { range: '200 - 280 字/分钟' },
  speech_rate_cv: { range: '10% - 20%' },
  speech_rate_late_ratio: { range: '0.90 - 1.20' },
  question_count: { range: '建议 ≥ 15 次', min: 15 },
  question_per_10min: { range: '建议 3 – 5 次', band: [3, 5] },
  open_question_ratio: { range: '建议 ≥ 40%', min: 40 },
  higher_order_question_ratio: { range: '建议 ≥ 30%', min: 30 },
  question_gini: { range: '建议 0.20 – 0.50', band: [0.2, 0.5] },
  wait_time_mean: { range: '建议 ≥ 3 秒', min: 3 },
  wait_time_effective_ratio: { range: '建议 ≥ 50%', min: 50 },
  asr_low_confidence_ratio: { range: '建议 ≤ 10%', max: 10 },
}
// 声学页展示用参考区间，不进 Judge
const AUDIO_GUIDE = {
  loudness_db: { range: '-26 ~ -16 dB', band: [-26, -16], ok: '良好' },
  loudness_std: { range: '建议 ≤ 8 dB', max: 8, ok: '稳定' },
  pitch_median: { range: '150 ~ 220 Hz', band: [150, 220], ok: '适中' },
  pitch_std: { range: '建议 20 – 60 Hz', band: [20, 60], ok: '适中' },
  pitch_variation: { range: '建议 0.10 – 0.35', band: [0.1, 0.35], ok: '适中' },
  emphasis_per_min: { range: '建议 8 – 20 次', band: [8, 20], ok: '适中' },
  long_pause_per_10min: { range: '建议 ≤ 6 次', max: 6, ok: '良好' },
  silence_ratio: { range: '建议 ≤ 25%', max: 25, ok: '良好' },
  snr_estimate: { range: '建议 ≥ 15 dB', min: 15, ok: '良好' },
  wait_time_mean: { range: '3 ~ 6 秒', band: [3, 6], ok: '适中' },
  wait_time_median: { range: '3 ~ 6 秒', band: [3, 6], ok: '适中' },
  wait_time_effective_ratio: { range: '建议 ≥ 50%', min: 50, ok: '良好' },
  asr_confidence: { range: '建议 ≥ −0.40', min: -0.4, ok: '良好' },
  asr_low_confidence_ratio: { range: '建议 ≤ 10%', max: 10, ok: '良好' },
}
const AUDIO_ORDER = [
  'loudness_db',
  'snr_estimate',
  'loudness_std',
  'silence_ratio',
  'pitch_median',
  'pitch_std',
  'pitch_variation',
  'emphasis_per_min',
  'long_pause_per_10min',
  'wait_time_mean',
  'wait_time_median',
  'wait_time_effective_ratio',
  'asr_confidence',
  'asr_low_confidence_ratio',
]
const VISION_LABELS = {
  frames_analyzed: '已分析帧数',
  gaze_students_ratio: '视线看学生',
  gaze_script_ratio: '视线看讲稿',
  gaze_screen_ratio: '视线看屏幕',
  gaze_unclear_ratio: '视线无法判断',
  gesture_active_ratio: '手势活跃',
  walking_ratio: '讲台前或走动',
  board_present_ratio: '板书或投影',
  board_diagram_ratio: '含图表',
  board_readable_high_ratio: '可读性高',
  board_readable_low_ratio: '可读性低',
  heads_up_high_ratio: '学生抬头率高',
  heads_up_unclear_ratio: '抬头率无法判断',
  hands_raised_frame_ratio: '有人举手',
  students_visible_median: '可见学生中位数',
}
const VISION_GUIDE = {
  gaze_students_ratio: { range: '建议 ≥ 50%', min: 50, ok: '良好' },
  gaze_script_ratio: { range: '建议 ≤ 25%', max: 25, ok: '良好' },
  gaze_screen_ratio: { range: '建议 ≤ 25%', max: 25, ok: '良好' },
  gaze_unclear_ratio: { range: '建议 ≤ 15%', max: 15, ok: '良好' },
  gesture_active_ratio: { range: '建议 ≥ 40%', min: 40, ok: '良好' },
  board_present_ratio: { range: '建议 ≥ 60%', min: 60, ok: '良好' },
  board_diagram_ratio: { range: '建议 ≥ 20%', min: 20, ok: '良好' },
  board_readable_high_ratio: { range: '建议 ≥ 50%', min: 50, ok: '良好' },
  board_readable_low_ratio: { range: '建议 ≤ 20%', max: 20, ok: '良好' },
  heads_up_high_ratio: { range: '建议 ≥ 50%', min: 50, ok: '良好' },
  heads_up_unclear_ratio: { range: '建议 ≤ 30%', max: 30, ok: '良好' },
}
const VISION_ORDER = [
  'gaze_students_ratio',
  'gaze_script_ratio',
  'gaze_screen_ratio',
  'gaze_unclear_ratio',
  'gesture_active_ratio',
  'walking_ratio',
  'board_present_ratio',
  'board_diagram_ratio',
  'board_readable_high_ratio',
  'board_readable_low_ratio',
  'heads_up_high_ratio',
  'heads_up_unclear_ratio',
  'hands_raised_frame_ratio',
  'students_visible_median',
  'frames_analyzed',
]
const TOOLS_LABELS = {
  courseware_pages_analyzed: '已分析页数',
  cw_layout_clear_ratio: '版式清晰',
  cw_layout_cluttered_ratio: '版式拥挤',
  cw_density_heavy_ratio: '文字过密',
  cw_diagram_ratio: '含图表',
  cw_readable_high_ratio: '可读性高',
  cw_readable_low_ratio: '可读性低',
  slide_change_count: '页面切换',
  slide_change_per_10min: '每10分钟切换',
  dwell_median_sec: '停留中位数',
  dwell_short_ratio: '短停留比例',
  slide_sync_ratio: '讲授同步',
  blank_frame_ratio: '空白画面',
}
const TOOLS_GUIDE = {
  cw_layout_clear_ratio: { range: '建议 ≥ 60%', min: 60, ok: '良好' },
  cw_layout_cluttered_ratio: { range: '建议 ≤ 30%', max: 30, ok: '良好' },
  cw_density_heavy_ratio: { range: '建议 ≤ 25%', max: 25, ok: '良好' },
  cw_diagram_ratio: { range: '建议 ≥ 25%', min: 25, ok: '良好' },
  cw_readable_high_ratio: { range: '建议 ≥ 60%', min: 60, ok: '良好' },
  cw_readable_low_ratio: { range: '建议 ≤ 20%', max: 20, ok: '良好' },
  slide_change_per_10min: { range: '建议 3 – 5 次', band: [3, 5], ok: '正常' },
  dwell_median_sec: { range: '建议 20 – 70 秒', band: [20, 70], ok: '适中' },
  dwell_short_ratio: { range: '建议 ≤ 15%', max: 15, ok: '良好' },
  slide_sync_ratio: { range: '建议 ≥ 60%', min: 60, ok: '良好' },
  blank_frame_ratio: { range: '建议 ≤ 8%', max: 8, ok: '良好' },
}
const TOOLS_ORDER = [
  'courseware_pages_analyzed',
  'cw_layout_clear_ratio',
  'cw_layout_cluttered_ratio',
  'cw_density_heavy_ratio',
  'cw_diagram_ratio',
  'cw_readable_high_ratio',
  'cw_readable_low_ratio',
  'slide_change_count',
  'slide_change_per_10min',
  'dwell_median_sec',
  'dwell_short_ratio',
  'slide_sync_ratio',
  'blank_frame_ratio',
]
const PACE_LABELS = {
  speech_rate: '平均语速',
  speech_rate_cv: '语速变异系数',
  speech_rate_late_ratio: '后段/前段语速比',
  question_count: '提问次数',
  question_per_10min: '每 10 分钟提问',
  open_question_ratio: '开放性问题比例',
  higher_order_question_ratio: '高阶问题比例',
  question_gini: '提问集中度',
  wait_time_mean: '平均等待时间',
  wait_time_effective_ratio: '有效等待比例',
  asr_confidence: '转写置信度',
  asr_low_confidence_ratio: '低置信转写比例',
  classified_question_count: '可分类提问',
  question_free_segment_ratio: '无提问段落',
  interaction_count: '互动话语',
  discipline_count: '纪律提醒',
  inspire_count: '启发性话语',
  case_count: '案例引入',
  recency_count: '前沿表述',
  year_ref_count: '年份引用',
  filler_density: '口头禅密度',
  transition_count: '过渡衔接',
  student_speech_count: '学生发言线索',
  wait_time_median: '等待中位数',
  wait_time_sample_count: '等待样本数',
  loudness_db: '平均响度',
  loudness_std: '响度波动',
  snr_estimate: '信噪比',
  pitch_median: '基频中位数',
  pitch_std: '基频标准差',
  pitch_variation: '语调起伏度',
  emphasis_per_min: '每分钟重音',
  long_pause_count: '长停顿次数',
  long_pause_per_10min: '每10分钟长停顿',
  silence_ratio: '静音占比',
}
const PACE_TEXT_ORDER = [
  'speech_rate',
  'speech_rate_cv',
  'speech_rate_late_ratio',
  'question_count',
  'question_per_10min',
  'open_question_ratio',
  'higher_order_question_ratio',
  'question_gini',
]
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
const featureSubTab = ref('content')

const uploading = ref(false)
const uploadPercent = ref(0)
const uploadMode = ref('original')
const videoSource = ref('link')
const remoteVideoLink = ref('')
const remoteSharePassword = ref('')
const remoteShare = ref(null)
const remoteSharePath = ref([])
const remoteShareFileId = ref('')
const remoteShareLoading = ref(false)
let remoteShareRequest = 0

watch([remoteVideoLink, remoteSharePassword], () => {
  remoteShareRequest += 1
  remoteShare.value = null
  remoteSharePath.value = []
  remoteShareFileId.value = ''
  remoteShareLoading.value = false
}, { flush: 'sync' })

async function readRemoteShare(path = []) {
  if (!validRemoteVideoLink.value || uploading.value) return
  const request = ++remoteShareRequest
  remoteShareLoading.value = true
  remoteShare.value = null
  remoteShareFileId.value = ''
  try {
    const result = await evaluationApi.inspectRemoteSource({
      url: remoteVideoLink.value.trim(), password: remoteSharePassword.value.trim(), path,
    })
    if (request !== remoteShareRequest) return
    remoteShare.value = result
    remoteSharePath.value = path
    const videos = result.files.filter((f) => f.is_video)
    if (videos.length === 1) remoteShareFileId.value = videos[0].id
  } catch {
    // The API client displays the provider-specific, sanitized error.
  } finally {
    if (request === remoteShareRequest) remoteShareLoading.value = false
  }
}
const preparingEvidence = ref(false)
const evidencePercent = ref(0)
const evidenceStage = ref('')
const evidenceSummary = ref('')
const uploadRecommendation = ref(null)
const recommendationAnalyzing = ref(false)
const uploadModeManuallyChosen = ref(false)
const uploadTaskId = ref(null)
const uploadContext = ref(null)
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
const videoDurationSec = ref(0)
const videoWidth = ref(0)
const videoHeight = ref(0)
const previewOpen = ref(false)
const cancellingId = ref(null)
const sidebarOpen = ref(true)
const taskQuery = ref('')
const taskFilter = ref('all')
let uploadController = null
let taskListRequest = 0
let recommendationRequest = 0
let recommendationPromise = null

const validRemoteVideoLink = computed(() => {
  if (videoSource.value !== 'link') return ''
  const text = remoteVideoLink.value.trim()
  const links = text.match(/https?:\/\/[^\s<>"，。；）]+/gi) || []
  const value = links.length === 1 ? (links[0] === text ? links[0] : links[0].replace(/[)\]]+$/, '')) : ''
  if (!value) return ''
  try {
    const parsed = new URL(value)
    return ['http:', 'https:'].includes(parsed.protocol) && parsed.hostname ? value : ''
  } catch {
    return ''
  }
})
const remoteUrlError = computed(() => {
  if (videoSource.value !== 'link' || !remoteVideoLink.value.trim() || validRemoteVideoLink.value) return ''
  return '请一次填写一个完整的 HTTP/HTTPS 链接'
})
const canStart = computed(() => Boolean(videoFile.value || (validRemoteVideoLink.value && !remoteShareLoading.value &&
  remoteShare.value?.download_ready !== false && (remoteShare.value?.provider === 'direct' || remoteShareFileId.value))))
const recommendedUploadMode = computed(() => uploadRecommendation.value?.strategy?.mode || null)
const materialCount = computed(() => {
  let n = 0
  if (videoFile.value || validRemoteVideoLink.value) n += 1
  if (coursewareFile.value) n += 1
  if (syllabusFile.value) n += 1
  if (scriptFile.value) n += 1
  return n
})
const activeTask = computed(() => tasks.value.find((t) => t.id === activeId.value) || null)
const isActiveUpload = computed(
  () => Boolean(uploading.value && uploadTaskId.value && activeId.value === uploadTaskId.value)
)
const isRemoteImport = computed(
  () => Boolean(isActiveUpload.value && uploadContext.value?.videoUrl)
)
const remoteImportProgress = computed(() => {
  if (!isRemoteImport.value) return 0
  return activeTask.value?.progress || 0
})
const reviewing = computed(() => Boolean(activeId.value && !isActiveUpload.value))
const videoProgress = computed(() => {
  if (preparingEvidence.value) return evidencePercent.value
  if (isActiveUpload.value && uploadMode.value === 'fast' && evidenceSummary.value) {
    return 70 + Math.round(uploadPercent.value * 0.3)
  }
  if (isActiveUpload.value) return uploadPercent.value
  return reviewing.value ? 100 : 0
})
const videoStageText = computed(() => {
  if (preparingEvidence.value) return evidenceStage.value || '浏览器预处理中'
  if (isActiveUpload.value) return '正在上传材料'
  if (reviewing.value) return '上传完成'
  return uploadMode.value === 'fast' ? '已选择，等待快速处理' : '已选择，等待上传'
})
const statusBanner = computed(() => {
  const t = activeTask.value
  if (!t || isActiveUpload.value) return null
  if (t.status === 'completed') {
    return { tone: 'done', title: '评估已完成', sub: '完整评估报告已生成，可前往结果页查看' }
  }
  if (t.status === 'upload_failed') {
    return { tone: 'fail', title: '上传失败', sub: t.error || '材料上传过程中出错' }
  }
  if (t.status === 'failed') {
    return { tone: 'fail', title: '评估失败', sub: t.error || '评估过程中出错' }
  }
  if (t.status === 'cancelled') {
    return { tone: 'fail', title: '任务已停止', sub: '该任务未继续执行' }
  }
  if (t.status === 'uploading') {
    return { tone: 'run', title: '上传中', sub: '视频和辅助材料正在上传', progress: t.progress ?? 0 }
  }
  if (t.status === 'processing' || t.status === 'queued' || t.status === 'cancel_requested') {
    const step = `${t.step_label || ''}${stepDetail(t)}`.trim()
    return {
      tone: 'run',
      title: t.status === 'cancel_requested' ? '正在停止' : '解析中',
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
const featureGroupMap = computed(() => {
  const groups = result.value?.objective_features || {}
  const map = {}
  for (const g of FEATURE_GROUPS) {
    map[g.key] = {
      ...g,
      rows: (groups[g.key] || []).map((f) => ({ ...f, meter: featureMeter(f) })),
    }
  }
  return map
})
const featureGot = computed(() =>
  FEATURE_GROUPS.reduce((n, g) => n + (featureGroupMap.value[g.key]?.rows.length || 0), 0)
)
const featureExpected = FEATURE_GROUPS.reduce((n, g) => n + g.expected, 0)

function featRow(group, key) {
  return featureGroupMap.value[group]?.rows.find((r) => r.key === key) || null
}
function featNum(group, key) {
  const n = Number(featRow(group, key)?.value)
  return Number.isFinite(n) ? n : null
}
function featText(group, key, fallback = '—') {
  const row = featRow(group, key)
  if (!row) return fallback
  return `${row.value}${row.unit || ''}`
}
function bucketCount(key) {
  const bucket = FEATURE_BUCKETS.find((b) => b.key === key)
  if (!bucket) return featureGroupMap.value[key]?.rows.length || 0
  return bucket.sources.reduce((n, src) => n + (featureGroupMap.value[src]?.rows.length || 0), 0)
}

function lessonSeconds() {
  const minutes = Number(result.value?.overall?.duration_minutes)
  if (Number.isFinite(minutes) && minutes > 0) return minutes * 60
  const segs = result.value?.transcript?.segments || []
  const last = segs[segs.length - 1]
  const end = Number(last?.end_sec)
  return Number.isFinite(end) && end > 0 ? end : 1
}

const activeBucketSections = computed(() => {
  if (featureSubTab.value === 'speakers') {
    const g = featureGroupMap.value.speakers
    return g?.rows.length ? [{ key: g.key, label: `${g.label} · ${g.origin}`, rows: g.rows }] : []
  }
  const bucket = FEATURE_BUCKETS.find((b) => b.key === featureSubTab.value)
  if (!bucket) return []
  return bucket.sources
    .map((src) => {
      const g = featureGroupMap.value[src]
      return g?.rows.length ? { key: g.key, label: `${g.label} · ${g.origin}`, rows: g.rows } : null
    })
    .filter(Boolean)
})

const activeBucketLegend = computed(() => {
  if (featureSubTab.value === 'speakers') {
    return featureGroupMap.value.speakers?.origin || '说话人分离'
  }
  const bucket = FEATURE_BUCKETS.find((b) => b.key === featureSubTab.value)
  if (!bucket) return ''
  return bucket.sources
    .map((src) => featureGroupMap.value[src]?.origin)
    .filter(Boolean)
    .join('；')
})

function paceStatus(row, guide) {
  const n = Number(row?.value)
  const ideal = featureIdeal(row)
  if (ideal && Number.isFinite(n)) {
    if (n >= ideal[0] && n <= ideal[1]) {
      if (row.key === 'speech_rate') return { text: '适中', tone: 'ok' }
      if (row.key === 'speech_rate_cv') return { text: '稳定', tone: 'ok' }
      return { text: '良好', tone: 'ok' }
    }
    const band = Math.max(ideal[1] - ideal[0], 1e-6)
    const dist = n < ideal[0] ? ideal[0] - n : n - ideal[1]
    if (row.key === 'speech_rate') {
      return n > ideal[1] ? { text: '偏快', tone: 'warn' } : { text: '偏慢', tone: 'warn' }
    }
    return dist / band <= 0.4 ? { text: '关注', tone: 'warn' } : { text: '偏离', tone: 'bad' }
  }
  if (!Number.isFinite(n) || !guide) return { text: '—', tone: 'ok' }
  const okText = guide.ok || '适中'
  if (guide.min != null) {
    return n >= guide.min ? { text: okText, tone: 'ok' } : { text: '关注', tone: 'warn' }
  }
  if (guide.max != null) {
    return n <= guide.max ? { text: guide.ok || '良好', tone: 'ok' } : { text: '关注', tone: 'warn' }
  }
  if (guide.band) {
    return n >= guide.band[0] && n <= guide.band[1]
      ? { text: okText, tone: 'ok' }
      : { text: '关注', tone: 'warn' }
  }
  return { text: '—', tone: 'ok' }
}

function paceNote(row, status) {
  const key = row.key
  if (key === 'speech_rate') {
    if (status.text === '适中') return '语速在推荐区间内，利于学生理解与跟随'
    if (status.text === '偏快') return '语速偏快，学生可能来不及消化'
    return '语速偏慢，课堂推进可能偏缓'
  }
  if (key === 'speech_rate_cv') {
    return status.tone === 'ok' ? '语速波动适中，节奏稳定' : '分段语速起伏较大'
  }
  if (key === 'speech_rate_late_ratio') {
    return status.tone === 'ok' ? '后段语速与前段基本持平' : '前后段语速差距较大'
  }
  if (key === 'question_count' || key === 'question_per_10min') {
    return status.tone === 'ok' ? '提问总量适中' : '提问偏少，可增加互动'
  }
  if (key === 'open_question_ratio') {
    return status.tone === 'ok' ? '开放性问题比例良好' : '开放性问题偏少'
  }
  if (key === 'higher_order_question_ratio') {
    return status.tone === 'ok' ? '高阶问题比例良好' : '高阶问题仍可增加'
  }
  if (key === 'question_gini') {
    return status.tone === 'ok' ? '提问分布比较均匀' : '提问分布略集中，建议分散到更多教学环节'
  }
  if (key === 'wait_time_mean' || key === 'wait_time_effective_ratio') {
    return status.tone === 'ok' ? '提问后给学生留了思考时间' : '等待时间偏短'
  }
  if (key === 'asr_low_confidence_ratio') {
    return status.tone === 'ok' ? '转写整体可靠' : '低置信转写偏多，数字要谨慎看'
  }
  if (key === 'loudness_db') {
    return status.tone === 'ok' ? '音量适中，听感清楚' : '响度偏离常见授课区间'
  }
  if (key === 'snr_estimate') {
    return status.tone === 'ok' ? '课堂底噪较低' : '背景噪音偏大'
  }
  if (key === 'silence_ratio') {
    return status.tone === 'ok' ? '静音比例正常' : '静音偏多，可能有长时间停顿'
  }
  if (key === 'loudness_std') {
    return status.tone === 'ok' ? '响度波动不大' : '音量起伏偏大'
  }
  if (key === 'pitch_median' || key === 'pitch_std' || key === 'pitch_variation') {
    return status.tone === 'ok' ? '语调变化在常见范围' : '基频起伏需要关注'
  }
  if (key === 'emphasis_per_min') {
    return status.tone === 'ok' ? '重音节奏适中' : '强调密度偏离常见范围'
  }
  if (key === 'long_pause_per_10min') {
    return status.tone === 'ok' ? '非正常长停顿不多' : '长停顿偏多'
  }
  if (key === 'wait_time_median') {
    return status.tone === 'ok' ? '等待中位数落在推荐区间' : '等待中位数偏离 3–6 秒'
  }
  if (key === 'asr_confidence') {
    return status.tone === 'ok' ? '转写解码较有把握' : '平均对数概率偏低'
  }
  return row.label
}

function paceRangeText(row) {
  const guide = PACE_GUIDE[row.key] || {}
  if (guide.range) return guide.range
  const ideal = featureIdeal(row)
  if (ideal) return `${trimNum(ideal[0])} – ${trimNum(ideal[1])}${row.unit || ''}`
  return ''
}

function paceTableRows(group, preferred) {
  const rows = featureGroupMap.value[group]?.rows || []
  const seen = new Set()
  const ordered = []
  for (const key of preferred || []) {
    const row = rows.find((r) => r.key === key)
    if (row) {
      ordered.push(row)
      seen.add(key)
    }
  }
  for (const row of rows) {
    if (!seen.has(row.key)) ordered.push(row)
  }
  return ordered
    .map((row) => {
      const range = paceRangeText(row)
      if (!range) return null
      const guide = PACE_GUIDE[row.key] || {}
      const status = paceStatus(row, guide)
      return {
        key: row.key,
        label: PACE_LABELS[row.key] || row.label,
        value: `${row.value}${row.unit || ''}`,
        range,
        status: status.text,
        tone: status.tone,
        note: paceNote(row, status),
      }
    })
    .filter(Boolean)
}

function paceExtraItems(group, excludeKeys) {
  const exclude = new Set(excludeKeys || [])
  return (featureGroupMap.value[group]?.rows || [])
    .filter((row) => !exclude.has(row.key) && !paceRangeText(row))
    .map((row) => ({
      key: row.key,
      label: PACE_LABELS[row.key] || row.label,
      value: `${row.value}${row.unit || ''}`,
      raw: Number(row.value),
    }))
}

function audioRangeText(row) {
  const guide = AUDIO_GUIDE[row.key] || {}
  if (guide.range) return guide.range
  const ideal = featureIdeal(row)
  if (ideal) return `${trimNum(ideal[0])} – ${trimNum(ideal[1])}${row.unit || ''}`
  return ''
}

function audioAllRows() {
  return [
    ...(featureGroupMap.value.audio?.rows || []),
    ...(featureGroupMap.value.timeline?.rows || []),
  ]
}

function audioTableRows() {
  const rows = audioAllRows()
  const seen = new Set()
  const ordered = []
  for (const key of AUDIO_ORDER) {
    const row = rows.find((r) => r.key === key)
    if (row) {
      ordered.push(row)
      seen.add(key)
    }
  }
  for (const row of rows) {
    if (!seen.has(row.key)) ordered.push(row)
  }
  return ordered
    .map((row) => {
      const range = audioRangeText(row)
      if (!range) return null
      const guide = AUDIO_GUIDE[row.key] || {}
      const status = paceStatus(row, guide)
      return {
        key: row.key,
        label: PACE_LABELS[row.key] || row.label,
        value: `${row.value}${row.unit || ''}`,
        range,
        status: status.text,
        tone: status.tone,
        note: paceNote(row, status),
      }
    })
    .filter(Boolean)
}

function audioFactItems() {
  return audioAllRows()
    .filter((row) => !audioRangeText(row))
    .map((row) => ({
      key: row.key,
      label: PACE_LABELS[row.key] || row.label,
      value: `${row.value}${row.unit || ''}`,
    }))
}

function waitQuality(samples, effectiveRatio) {
  const list = (samples || []).map(Number).filter((n) => Number.isFinite(n))
  if (list.length) {
    const short = list.filter((g) => g < 3).length
    const good = list.filter((g) => g >= 3 && g <= 6).length
    const long = list.filter((g) => g > 6).length
    const total = list.length
    return [
      { key: 'good', label: '有效等待 (3-6秒)', pct: Math.round((1000 * good) / total) / 10, color: '#67c23a' },
      { key: 'short', label: '偏短 (<3秒)', pct: Math.round((1000 * short) / total) / 10, color: '#e6a23c' },
      { key: 'long', label: '偏长 (>6秒)', pct: Math.round((1000 * long) / total) / 10, color: '#c0c4cc' },
    ].filter((s) => s.pct > 0)
  }
  if (effectiveRatio == null) return []
  const good = Math.min(100, Math.max(0, effectiveRatio))
    return [
      { key: 'good', label: '有效等待 (≥3秒)', pct: good, color: '#67c23a' },
      { key: 'short', label: '偏短 (<3秒)', pct: Math.round(10 * (100 - good)) / 10, color: '#e6a23c' },
    ].filter((s) => s.pct > 0)
}

function paceObsIcon(key) {
  const d = PACE_OBS_PATHS[key] || PACE_OBS_PATHS.default
  return `<svg viewBox="0 0 24 24" fill="none" stroke="#a61b1b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`
}

const PACE_OBS_PATHS = {
  classified_question_count:
    '<path d="M4 5h13a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H9l-4 3v-3H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/><path d="M7 9h9M7 12.5h6"/>',
  transition_count:
    '<path d="M7 7h10M7 12h10M7 17h10"/><path d="M5 5.5L3 7.5 5 9.5M19 14.5l2 2-2 2"/>',
  case_count:
    '<path d="M5 8h14v11a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"/><path d="M9 8V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V8"/><path d="M8 13h8M8 16.5h5"/>',
  interaction_count:
    '<path d="M4 6h10a2 2 0 0 1 2 2v5l-3.5-2H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2z"/><path d="M10 13.5h8.5a2 2 0 0 1 2 2v4.5l-3.2-1.8H10a2 2 0 0 1-2-2v-0.7"/>',
  discipline_count:
    '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 8.5-3 8.5h18S18 15 18 8"/><path d="M10 20.5a2.2 2.2 0 0 0 4 0"/>',
  recency_count:
    '<path d="M12 3.2l2.2 6.3H21l-5.4 3.8 2.1 6.4L12 16.7 6.3 19.7l2.1-6.4L3 9.5h6.8z"/>',
  student_speech_count:
    '<circle cx="9" cy="7.5" r="3.4"/><path d="M3.5 20v-1.4A4.6 4.6 0 0 1 8.1 14h1.8a4.6 4.6 0 0 1 4.6 4.6V20"/><circle cx="17" cy="8.5" r="2.6"/><path d="M21.5 20v-1.2A3.8 3.8 0 0 0 17.7 15h-.4"/>',
  inspire_count:
    '<path d="M9 17.5h6M10 21h4"/><path d="M12 2.8a6.6 6.6 0 0 0-4.1 11.7V16h8.2v-1.5A6.6 6.6 0 0 0 12 2.8z"/><path d="M10.5 9.2h3"/>',
  year_ref_count:
    '<rect x="3.5" y="5" width="17" height="16" rx="2"/><path d="M3.5 10h17M8 3.2v4.2M16 3.2v4.2"/><path d="M8 14h.01M12 14h.01M16 14h.01M8 17.5h.01M12 17.5h.01"/>',
  wait_time_median:
    '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.2v5.1l3.2 1.9"/>',
  wait_time_sample_count:
    '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.2v5.1l3.2 1.9"/>',
  long_pause_count:
    '<rect x="7" y="5" width="3.2" height="14" rx="0.8"/><rect x="13.8" y="5" width="3.2" height="14" rx="0.8"/>',
  slide_change_per_10min:
    '<rect x="3.5" y="6" width="11" height="14" rx="1.4"/><rect x="8.5" y="3.5" width="11" height="14" rx="1.4"/><path d="M15.5 10.5h5M18 8v5"/>',
  dwell_median_sec:
    '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.2v5.1l3.2 1.9"/>',
  dwell_short_ratio:
    '<circle cx="12" cy="12" r="8.5"/><path d="M10 8.2l6.2 3.8L10 15.8z"/>',
  blank_frame_ratio:
    '<rect x="4" y="6" width="16" height="12" rx="1.6"/><path d="M8 12h8"/>',
  asr_confidence:
    '<path d="M3 12h2.2l2-7 3.6 14 2.4-7H21"/><path d="M4 16.5h3M17 16.5h3"/>',
  default:
    '<circle cx="12" cy="12" r="8.5"/><path d="M8 12h8"/>',
}

const pacePage = computed(() => {
  const rate = featNum('text', 'speech_rate')
  const rateStatus = paceStatus(featRow('text', 'speech_rate') || { key: 'speech_rate', value: rate }, PACE_GUIDE.speech_rate)
  const textRows = paceTableRows('text', PACE_TEXT_ORDER)
  const textExtras = paceExtraItems('text')
  const donutRow = textExtras.find((h) => h.key === 'question_free_segment_ratio')
  const pct = Number.isFinite(donutRow?.raw) ? Math.min(100, Math.max(0, donutRow.raw)) : 0
  return {
    textHeroes: [
      {
        value: rate == null ? '—' : `${trimNum(rate)} 字/分钟`,
        label: '语速',
        tag: rate == null ? '' : rateStatus.text,
        tone: rateStatus.tone,
      },
      { value: featText('text', 'question_count'), label: '提问' },
      { value: featText('text', 'open_question_ratio'), label: '开放性问题' },
      { value: featText('text', 'higher_order_question_ratio'), label: '高阶问题' },
    ],
    timeHeroes: [
      { value: featText('timeline', 'wait_time_mean'), label: '平均等待' },
      { value: featText('timeline', 'wait_time_effective_ratio'), label: '有效等待' },
      { value: featText('timeline', 'asr_confidence'), label: '转写置信' },
      { value: featText('timeline', 'asr_low_confidence_ratio'), label: '低置信转写' },
    ].filter((h) => h.value !== '—'),
    textRows,
    textFacts: textExtras.filter((h) => h.key !== 'question_free_segment_ratio'),
    textDonut: donutRow
      ? { pct, pctLabel: `${trimNum(pct)}%`, label: donutRow.label }
      : null,
    textCount: textRows.length + textExtras.length,
    timeRows: paceTableRows('timeline'),
    timeFacts: paceExtraItems('timeline'),
  }
})

const audioPage = computed(() => {
  const audioCount = featureGroupMap.value.audio?.rows.length || 0
  const timeCount = featureGroupMap.value.timeline?.rows.length || 0
  const expected =
    (featureGroupMap.value.audio?.expected || 10) + (featureGroupMap.value.timeline?.expected || 6)
  const snr = featNum('audio', 'snr_estimate')
  const silence = featNum('audio', 'silence_ratio')
  const loud = featNum('audio', 'loudness_db')
  const voiceOk = snr != null && snr >= 15 && (silence == null || silence <= 25)
  const low = featNum('timeline', 'asr_low_confidence_ratio')
  const asrPct = low == null ? null : Math.min(100, Math.max(0, 100 - low))
  const samples = result.value?.raw_features?.timeline?.wait_samples
  const judgeRows = audioTableRows()
  const facts = audioFactItems()
  const waitMean = featRow('timeline', 'wait_time_mean')
  const waitMedian = featRow('timeline', 'wait_time_median')
  return {
    got: audioCount + timeCount,
    expected,
    audioCount,
    timeCount,
    judgeRows,
    facts,
    waitQuality: waitQuality(samples, featNum('timeline', 'wait_time_effective_ratio')),
    asrStack:
      low == null
        ? []
        : [
            { key: 'high', label: '高置信 (≥90%)', pct: Math.round(10 * asrPct) / 10, color: '#a61b1b' },
            { key: 'low', label: '低置信 (<90%)', pct: Math.round(10 * low) / 10, color: '#c0c4cc' },
          ].filter((s) => s.pct > 0),
    waitMean: waitMean ? `${waitMean.value}${waitMean.unit || ''}` : '',
    waitMedian: waitMedian ? `${waitMedian.value}${waitMedian.unit || ''}` : '',
    heroes: [
      {
        value: loud == null ? '—' : `${trimNum(loud)} dB`,
        label: '平均响度',
        tag: voiceOk ? '清晰稳定' : '',
        tone: 'ok',
      },
      { value: featText('audio', 'snr_estimate'), label: '信噪比' },
      { value: featText('timeline', 'wait_time_mean'), label: '平均等待' },
      {
        value: asrPct == null ? featText('timeline', 'asr_confidence') : `${trimNum(asrPct)} %`,
        label: 'ASR置信度',
      },
    ],
  }
})

function visionPct(key) {
  return featNum('vision', key)
}

function visionStack(parts) {
  const items = parts
    .map((s) => ({ ...s, pct: Math.max(0, visionPct(s.key) ?? 0) }))
    .filter((s) => s.pct > 0)
  const sum = items.reduce((n, s) => n + s.pct, 0)
  const scale = sum > 100 ? 100 / sum : 1
  return items.map((s) => ({ ...s, width: Math.round(10 * s.pct * scale) / 10 }))
}

function visionNote(row, status) {
  const key = row.key
  const ok = status.tone === 'ok'
  if (key === 'gaze_students_ratio') return ok ? '多数时间面向学生' : '面向学生的时间偏少'
  if (key === 'gaze_script_ratio') return ok ? '看讲稿不多' : '看讲稿偏多，可能打断目光交流'
  if (key === 'gaze_screen_ratio') return ok ? '看屏幕或背对学生不多' : '视线较多落在屏幕或背对学生'
  if (key === 'gaze_unclear_ratio') return ok ? '视线标注较清楚' : '无法判断的帧偏多，这项要谨慎看'
  if (key === 'gesture_active_ratio') return ok ? '手势使用较充分' : '手势出现偏少'
  if (key === 'board_present_ratio') return ok ? '板书或投影使用充分' : '板书或投影出现的帧不多'
  if (key === 'board_diagram_ratio') return ok ? '有一定图示内容' : '图表内容偏少'
  if (key === 'board_readable_high_ratio') return ok ? '板书投影多数可读' : '高可读帧偏少'
  if (key === 'board_readable_low_ratio') return ok ? '低可读帧不多' : '低可读帧偏多'
  if (key === 'heads_up_high_ratio') return ok ? '学生抬头率整体较好' : '抬头率高的帧不多'
  if (key === 'heads_up_unclear_ratio') return ok ? '抬头情况大多能看清' : '较多帧看不清学生抬头'
  return row.label
}

function visionFactNote(key) {
  if (key === 'frames_analyzed') return '成功标注的关键帧数量'
  if (key === 'walking_ratio') return '讲台前或走动的帧占比，只作观察'
  if (key === 'hands_raised_frame_ratio') return '画面中出现举手的帧占比，只作观察'
  if (key === 'students_visible_median') return '画面中可见学生人数的中位数'
  return '无展示用参考区间，只作观察'
}

function visionTableRows() {
  const rows = featureGroupMap.value.vision?.rows || []
  const seen = new Set()
  const ordered = []
  for (const key of VISION_ORDER) {
    const row = rows.find((r) => r.key === key)
    if (row) {
      ordered.push(row)
      seen.add(key)
    }
  }
  for (const row of rows) {
    if (!seen.has(row.key)) ordered.push(row)
  }
  return ordered.map((row) => {
    const guide = VISION_GUIDE[row.key]
    const label = VISION_LABELS[row.key] || row.label
    const value = `${row.value}${row.unit || ''}`
    if (!guide) {
      return {
        key: row.key,
        label,
        value,
        range: '—',
        status: '事实观察',
        tone: 'fact',
        note: visionFactNote(row.key),
      }
    }
    const status = paceStatus(row, guide)
    return {
      key: row.key,
      label,
      value,
      range: guide.range,
      status: status.text,
      tone: status.tone,
      note: visionNote(row, status),
    }
  })
}

function visionConclusions() {
  const gaze = visionPct('gaze_students_ratio')
  const script = visionPct('gaze_script_ratio') || 0
  const screen = visionPct('gaze_screen_ratio') || 0
  const gesture = visionPct('gesture_active_ratio')
  const heads = visionPct('heads_up_high_ratio')
  const unclear = visionPct('heads_up_unclear_ratio') || 0
  const board = visionPct('board_present_ratio')
  const out = []
  if (gaze != null) {
    if (gaze >= 50) {
      out.push({
        title: '多数时间面向学生',
        text: '教师视线主要面向学生，关注度较高，有利于课堂互动与理解。',
      })
    } else if (script >= gaze && script >= screen) {
      out.push({
        title: '看讲稿偏多',
        text: '教师较多时间看讲稿，面向学生的交流可能被打断。',
      })
    } else if (screen > gaze) {
      out.push({
        title: '看屏幕或背对学生偏多',
        text: '视线较多落在屏幕或背对学生，课堂目光交流偏弱。',
      })
    } else {
      out.push({
        title: '面向学生时间有限',
        text: '看学生帧占比不高，课堂目光交流偏弱。',
      })
    }
  }
  if (gesture != null) {
    if (gesture >= 50) {
      out.push({
        title: '手势表达较充分',
        text: '手势使用频率较高，能够辅助强调重点，增强表达效果。',
      })
    } else if (gesture >= 25) {
      out.push({
        title: '有一定手势辅助',
        text: '部分帧出现手势，讲解辅助有限。',
      })
    } else {
      out.push({
        title: '手势使用偏少',
        text: '多数帧未见明显手势，讲解主要依赖言语。',
      })
    }
  }
  if (heads != null) {
    if (heads >= 50) {
      out.push({
        title: '学生抬头状态整体良好',
        text: '学生抬头率较高，表明学生参与度较好，课堂注意力集中。',
      })
    } else if (unclear >= 40) {
      out.push({
        title: '学生抬头率难以判断',
        text: '较多帧无法看清学生抬头情况，这项只作参考。',
      })
    } else {
      out.push({
        title: '学生抬头率偏低',
        text: '抬头率高的帧不多，学生参与或镜头覆盖需要关注。',
      })
    }
  } else if (board != null) {
    out.push({
      title: board >= 70 ? '板书或投影使用充分' : '板书或投影出现有限',
      text:
        board >= 70
          ? '多数帧能看到板书或投影，视觉媒介使用充分。'
          : '板书或投影出现的帧不多，课堂视觉媒介偏少。',
    })
  }
  return out.slice(0, 3)
}

const visionPage = computed(() => {
  const got = featureGroupMap.value.vision?.rows.length || 0
  const expected = featureGroupMap.value.vision?.expected || 15
  const frames = visionPct('frames_analyzed')
  const pctText = (key) => {
    const n = visionPct(key)
    return n == null ? '—' : `${trimNum(n)}%`
  }
  const stacks = [
    {
      key: 'gaze',
      label: '教师视线',
      parts: visionStack([
        { key: 'gaze_students_ratio', label: '看学生', color: '#a61b1b' },
        { key: 'gaze_script_ratio', label: '看讲稿', color: '#e6a23c' },
        { key: 'gaze_screen_ratio', label: '看屏幕', color: '#67c23a' },
        { key: 'gaze_unclear_ratio', label: '无法判断', color: '#c0c4cc' },
      ]),
    },
    {
      key: 'act',
      label: '教学行为',
      parts: visionStack([
        { key: 'gesture_active_ratio', label: '有手势', color: '#a61b1b' },
        { key: 'walking_ratio', label: '讲台前或走动', color: '#e6a23c' },
        { key: 'hands_raised_frame_ratio', label: '有人举手', color: '#67c23a' },
      ]),
    },
    {
      key: 'media',
      label: '课堂媒介',
      parts: visionStack([
        { key: 'board_present_ratio', label: '板书或投影', color: '#a61b1b' },
        { key: 'board_diagram_ratio', label: '含图表', color: '#e6a23c' },
        { key: 'board_readable_high_ratio', label: '可读性高', color: '#67c23a' },
      ]),
    },
  ].filter((row) => row.parts.length)
  return {
    got,
    expected,
    frames: frames == null ? '—' : trimNum(frames),
    heroes: [
      { value: pctText('gaze_students_ratio'), label: '视线面向学生' },
      { value: pctText('gesture_active_ratio'), label: '有手势' },
      { value: pctText('board_present_ratio'), label: '板书或投影' },
      { value: pctText('heads_up_high_ratio'), label: '抬头率高' },
    ],
    stacks,
    conclusions: visionConclusions(),
    rows: visionTableRows(),
  }
})

function clockSec(sec) {
  const n = Math.max(0, Math.floor(Number(sec) || 0))
  const m = Math.floor(n / 60)
  const s = n % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

function toolsNum(group, key) {
  return featNum(group, key)
}

function toolsStack(parts) {
  const items = parts
    .map((s) => ({ ...s, pct: Math.max(0, Number(s.pct) || 0) }))
    .filter((s) => s.pct > 0)
  const sum = items.reduce((n, s) => n + s.pct, 0)
  const scale = sum > 100 ? 100 / sum : 1
  return items.map((s) => ({ ...s, width: Math.round(10 * s.pct * scale) / 10 }))
}

function cwPageRatio(field, wanted) {
  const pages = result.value?.courseware_slides || []
  const vals = pages.map((p) => p.labels?.[field]).filter(Boolean)
  if (!vals.length) return 0
  return Math.round((1000 * vals.filter((v) => wanted.includes(v)).length) / vals.length) / 10
}

function toolsChangeTimes() {
  const raw = result.value?.raw_features?.slides?.slide_change_times
  if (!Array.isArray(raw)) return []
  return raw.map(Number).filter((n) => Number.isFinite(n) && n >= 0).sort((a, b) => a - b)
}

function toolsDwells() {
  const raw = result.value?.raw_features?.slides?.dwell_samples
  if (Array.isArray(raw) && raw.length) {
    return raw.map(Number).filter((n) => Number.isFinite(n) && n > 0)
  }
  const times = toolsChangeTimes()
  const dur = lessonSeconds()
  if (!times.length || dur <= 0) return []
  const bounds = [0, ...times.filter((t) => t < dur), dur]
  const out = []
  for (let i = 0; i < bounds.length - 1; i += 1) {
    const d = bounds[i + 1] - bounds[i]
    if (d > 0) out.push(d)
  }
  return out
}

function toolsTimeline(tall = false) {
  const times = toolsChangeTimes()
  const dur = Math.max(lessonSeconds(), times[times.length - 1] || 0, 1)
  if (!times.length && !featNum('slides', 'slide_change_count')) return null
  const W = 640
  const H = tall ? 88 : 58
  const pad = 12
  const inner = W - pad * 2
  const trackY = tall ? 30 : 18
  const trackH = tall ? 18 : 10
  const tickY1 = tall ? 18 : 12
  const tickY2 = trackY + trackH + (tall ? 8 : 6)
  const labelY = H - 8
  const ticks = (times.length ? times : []).map((t) => ({
    x: pad + (Math.min(dur, Math.max(0, t)) / dur) * inner,
  }))
  if (!ticks.length) {
    const n = Math.min(featNum('slides', 'slide_change_count') || 0, 24)
    for (let i = 1; i <= n; i += 1) {
      ticks.push({ x: pad + (i / (n + 1)) * inner })
    }
  }
  return {
    W,
    H,
    pad,
    inner,
    trackY,
    trackH,
    tickY1,
    tickY2,
    labelY,
    ticks,
    labels: [
      { x: pad, text: clockSec(0) },
      { x: pad + inner / 2, text: clockSec(dur / 2) },
      { x: pad + inner, text: clockSec(dur) },
    ],
  }
}

function toolsAxisNotes() {
  const times = toolsChangeTimes()
  const dur = Math.max(lessonSeconds(), 1)
  const notes = []
  if (times.length >= 3) {
    const bin = 90
    let best = 0
    let bestStart = 0
    for (let t = 0; t < dur; t += 30) {
      const n = times.filter((x) => x >= t && x < t + bin).length
      if (n > best) {
        best = n
        bestStart = t
      }
    }
    if (best >= 3) {
      notes.push(`${clockSec(bestStart)}–${clockSec(bestStart + bin)} 切换较密集`)
    }
  }
  const dwells = toolsDwells()
  if (dwells.length) {
    const maxD = Math.max(...dwells)
    if (maxD >= 90) {
      const times2 = toolsChangeTimes()
      const bounds = [0, ...times2.filter((t) => t < dur), dur]
      let start = 0
      for (let i = 0; i < bounds.length - 1; i += 1) {
        if (bounds[i + 1] - bounds[i] === maxD) {
          start = bounds[i]
          break
        }
      }
      notes.push(`${clockSec(start)} 长停留`)
    }
  }
  if (times.length >= 4) {
    const bins = []
    for (let t = 0; t < dur; t += 300) {
      bins.push(times.filter((x) => x >= t && x < t + 300).length)
    }
    const mean = bins.reduce((a, b) => a + b, 0) / bins.length
    const sd = Math.sqrt(bins.reduce((s, v) => s + (v - mean) ** 2, 0) / bins.length)
    if (mean > 0 && sd / mean <= 0.55) notes.push('整体节奏较均匀')
  }
  return notes.slice(0, 3)
}

function toolsDonut() {
  const dwells = toolsDwells()
  const median = featNum('slides', 'dwell_median_sec')
  if (!dwells.length && median == null) return null
  let short = 0
  let mid = 0
  let long = 0
  if (dwells.length) {
    short = dwells.filter((d) => d < 20).length
    mid = dwells.filter((d) => d >= 20 && d <= 90).length
    long = dwells.filter((d) => d > 90).length
  } else {
    const s = featNum('slides', 'dwell_short_ratio') || 0
    short = s
    mid = Math.max(0, 100 - s)
    long = 0
  }
  const total = short + mid + long || 1
  const parts = [
    { key: 'short', label: '短停留 < 20秒', pct: Math.round((1000 * short) / total) / 10, color: '#e6a23c' },
    { key: 'mid', label: '常规停留 20-90秒', pct: Math.round((1000 * mid) / total) / 10, color: '#a61b1b' },
    { key: 'long', label: '长停留 > 90秒', pct: Math.round((1000 * long) / total) / 10, color: '#c0c4cc' },
  ].filter((s) => s.pct > 0)
  let acc = 0
  const stops = parts.map((s) => {
    const from = acc
    acc += s.pct
    return `${s.color} ${from}% ${acc}%`
  })
  return {
    parts,
    bg: `conic-gradient(${stops.join(', ')})`,
    median: median == null ? '—' : `${trimNum(median)} 秒`,
  }
}

function toolsDwellNote(donut) {
  if (!donut?.parts.length) return null
  const short = donut.parts.find((p) => p.key === 'short')?.pct || 0
  const long = donut.parts.find((p) => p.key === 'long')?.pct || 0
  if (short <= 20 && long <= 40) {
    return { title: '长短停留搭配基本合理', text: long > 25 ? '个别段落讲解偏长。' : '页面停留整体在常见范围。' }
  }
  if (short > 20) {
    return { title: '短停留偏多', text: '不少页面停留不足 20 秒，学生可能来不及看清。' }
  }
  return { title: '长停留偏多', text: '部分页面停留偏长，节奏可以再紧凑一些。' }
}

function toolsNote(row, status) {
  const ok = status.tone === 'ok'
  const key = row.key
  if (key === 'cw_layout_clear_ratio') return ok ? '多数页面版式清楚' : '版式清楚的页面偏少'
  if (key === 'cw_layout_cluttered_ratio') return ok ? '拥挤页面不多' : '版式拥挤的页面偏多'
  if (key === 'cw_density_heavy_ratio') return ok ? '文字过密的页面不多' : '文字过密页偏多，信息负担较重'
  if (key === 'cw_diagram_ratio') return ok ? '有一定图表辅助' : '图表页偏少'
  if (key === 'cw_readable_high_ratio') return ok ? '多数页面可读性高' : '高可读页面偏少'
  if (key === 'cw_readable_low_ratio') return ok ? '低可读页面不多' : '低可读页面偏多'
  if (key === 'slide_change_per_10min') return ok ? '切换频率在建议范围' : '切换偏快或偏慢'
  if (key === 'dwell_median_sec') return ok ? '页面停留中位数适中' : '停留中位数偏离常见区间'
  if (key === 'dwell_short_ratio') return ok ? '短停留不多' : '短停留偏多'
  if (key === 'slide_sync_ratio') return ok ? '切换处多有过渡话语' : '切换与讲授衔接偏弱'
  if (key === 'blank_frame_ratio') return ok ? '空白画面很少' : '空白画面偏多'
  return row.label
}

function toolsFactNote(key) {
  if (key === 'courseware_pages_analyzed') return '成功标注的上传课件页数'
  if (key === 'slide_change_count') {
    const src = result.value?.raw_features?.slides?.slide_roi_source
    if (src === 'vlm') return '已先框出投影/板书，再在该区域内检测切换；仍非精确页数'
    return '画面局部跳变识别到的切换次数，走动造成的持续变化会滤掉，仍非精确页数'
  }
  return '无展示用参考区间，只作观察'
}

function toolsTableRows() {
  const rows = [
    ...(featureGroupMap.value.courseware?.rows || []),
    ...(featureGroupMap.value.slides?.rows || []),
  ]
  const seen = new Set()
  const ordered = []
  for (const key of TOOLS_ORDER) {
    const row = rows.find((r) => r.key === key)
    if (row) {
      ordered.push(row)
      seen.add(key)
    }
  }
  for (const row of rows) {
    if (!seen.has(row.key)) ordered.push(row)
  }
  return ordered.map((row) => {
    const guide = TOOLS_GUIDE[row.key]
    const label = TOOLS_LABELS[row.key] || row.label
    const value = `${row.value}${row.unit || ''}`
    if (!guide) {
      return {
        key: row.key,
        label,
        value,
        range: '—',
        status: '事实观察',
        tone: 'fact',
        note: toolsFactNote(row.key),
      }
    }
    const status = paceStatus(row, guide)
    return {
      key: row.key,
      label,
      value,
      range: guide.range,
      status: status.text,
      tone: status.tone,
      note: toolsNote(row, status),
    }
  })
}

const toolsPage = computed(() => {
  const cwCount = featureGroupMap.value.courseware?.rows.length || 0
  const slideCount = featureGroupMap.value.slides?.rows.length || 0
  const cwExpected = featureGroupMap.value.courseware?.expected || 7
  const slideExpected = featureGroupMap.value.slides?.expected || 6
  const hasCw = cwCount > 0 || (result.value?.courseware_slides || []).length > 0
  const pages = toolsNum('courseware', 'courseware_pages_analyzed')
  const donut = toolsDonut()
  const stacks = hasCw
    ? [
        {
          key: 'layout',
          label: '版式',
          parts: toolsStack([
            { key: 'clear', label: '清晰', pct: toolsNum('courseware', 'cw_layout_clear_ratio'), color: '#67c23a' },
            { key: 'clutter', label: '拥挤', pct: toolsNum('courseware', 'cw_layout_cluttered_ratio'), color: '#c0c4cc' },
          ]),
        },
        {
          key: 'density',
          label: '信息密度',
          parts: toolsStack([
            { key: 'mod', label: '适中', pct: cwPageRatio('density', ['moderate']), color: '#67c23a' },
            { key: 'heavy', label: '过高', pct: toolsNum('courseware', 'cw_density_heavy_ratio') ?? cwPageRatio('density', ['text_heavy']), color: '#e6a23c' },
            { key: 'sparse', label: '过低', pct: cwPageRatio('density', ['sparse']), color: '#c0c4cc' },
          ]),
        },
        {
          key: 'chart',
          label: '图表使用',
          parts: toolsStack([
            { key: 'diag', label: '含图表', pct: toolsNum('courseware', 'cw_diagram_ratio'), color: '#67c23a' },
            {
              key: 'text',
              label: '纯文字',
              pct:
                toolsNum('courseware', 'cw_diagram_ratio') == null
                  ? cwPageRatio('content', ['text_heavy', 'none'])
                  : Math.max(0, Math.round(10 * (100 - (toolsNum('courseware', 'cw_diagram_ratio') || 0))) / 10),
              color: '#c0c4cc',
            },
          ]),
        },
        {
          key: 'read',
          label: '可读性',
          parts: toolsStack([
            { key: 'high', label: '高', pct: toolsNum('courseware', 'cw_readable_high_ratio'), color: '#67c23a' },
            { key: 'low', label: '低', pct: toolsNum('courseware', 'cw_readable_low_ratio'), color: '#c0c4cc' },
          ]),
        },
      ].filter((row) => row.parts.length)
    : []
  const val = (group, key, fallback = '—') => {
    const n = toolsNum(group, key)
    if (n == null) return fallback
    const unit = featRow(group, key)?.unit || ''
    if (unit === '%') return `${trimNum(n)}%`
    return unit ? `${trimNum(n)} ${unit}` : trimNum(n)
  }
  return {
    got: cwCount + slideCount,
    expected: cwExpected + slideExpected,
    cwExpected,
    hasCw,
    pages: pages == null ? (result.value?.courseware_slides || []).length || '—' : trimNum(pages),
    lead: hasCw
      ? `融合上传课件页面观测与视频切换时序，已获得 ${cwCount + slideCount} / ${cwExpected + slideExpected} 项`
      : `基于视频画面变化分析切换节奏，已获得 ${slideCount} / ${cwExpected + slideExpected} 项，${cwExpected}项课件页面质量指标因未上传材料已跳过`,
    heroes: hasCw
      ? [
          { value: val('courseware', 'courseware_pages_analyzed'), label: '已分析' },
          { value: val('courseware', 'cw_layout_clear_ratio'), label: '版式清晰' },
          { value: val('slides', 'slide_change_count'), label: '页面切换' },
          { value: val('slides', 'slide_sync_ratio'), label: '讲授同步' },
        ]
      : [
          { value: val('slides', 'slide_change_count'), label: '页面切换' },
          { value: val('slides', 'slide_change_per_10min'), label: '切换频率' },
          { value: val('slides', 'dwell_median_sec'), label: '停留中位数' },
          { value: val('slides', 'slide_sync_ratio'), label: '讲授同步' },
        ],
    stacks,
    timeline: toolsTimeline(hasCw),
    minis: [
      { key: 'slide_change_per_10min', value: val('slides', 'slide_change_per_10min'), label: '每 10 分钟' },
      { key: 'dwell_median_sec', value: val('slides', 'dwell_median_sec'), label: '停留中位数' },
      { key: 'dwell_short_ratio', value: val('slides', 'dwell_short_ratio'), label: '短停留' },
      { key: 'blank_frame_ratio', value: val('slides', 'blank_frame_ratio'), label: '空白画面' },
    ],
    axisNotes: toolsAxisNotes(),
    donut,
    dwellNote: toolsDwellNote(donut),
    rows: toolsTableRows(),
  }
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
function stripReportDigest(md) {
  if (!md) return ''
  const match = md.match(/^##\s*(?:[〇零0]、\s*)?诊断摘要\s*$/m)
  if (!match || match.index == null) return md
  const start = match.index
  const afterHeading = start + match[0].length
  const rest = md.slice(afterHeading)
  const next = rest.search(/^##\s/m)
  const before = md.slice(0, start).trimEnd()
  const after = next >= 0 ? rest.slice(next).trimStart() : ''
  return [before, after].filter(Boolean).join('\n\n')
}

const reportHtml = computed(() => {
  const md = stripReportDigest(result.value?.report || '')
  return md ? DOMPurify.sanitize(marked.parse(md)) : ''
})

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
  if (!result.value?.report) {
    ElMessage.warning('暂无诊断报告')
    return
  }
  if (!activeId.value) {
    ElMessage.warning('请从已完成任务导出')
    return
  }
  const a = document.createElement('a')
  a.href = evaluationApi.exportUrl(activeId.value, cmd)
  a.rel = 'noopener'
  a.click()
}

const filteredTasks = computed(() => {
  const q = taskQuery.value.trim().toLowerCase()
  return tasks.value.filter((t) => {
    if (taskFilter.value === 'running' && !isRunning(t)) return false
    if (taskFilter.value === 'completed' && t.status !== 'completed') return false
    if (taskFilter.value === 'failed' && !['failed', 'upload_failed', 'cancelled'].includes(t.status)) return false
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
  return ['uploading', 'queued', 'processing', 'cancel_requested'].includes(t.status)
}

function taskProgress(t) {
  if (t.id === uploadTaskId.value && uploadContext.value?.videoUrl) return t.progress || 0
  if (t.id === uploadTaskId.value && uploading.value) return uploadPercent.value
  return t.progress || 0
}

function taskRunningText(t) {
  if (t.status === 'uploading') return '上传中'
  if (t.status === 'cancel_requested') return '正在停止'
  return '评估中'
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
  return {
    uploading: '上传中',
    upload_failed: '上传失败',
    completed: '已完成',
    processing: '处理中',
    failed: '失败',
    queued: '排队中',
    cancel_requested: '正在停止',
    cancelled: '已停止',
  }[s] || s
}
function gradeType(g) {
  return { A: 'success', B: '', C: 'warning', D: 'danger' }[g] || 'info'
}
function rowClass({ row }) {
  return row.assessed ? '' : 'row-skipped'
}

function stepDetail(t) {
  const d = t.step_detail || {}
  if (t.current_step === 'remote_downloading') {
    if (d.phase === 'connecting') return '（正在连接）'
    if (d.phase === 'validating') return '（正在校验视频）'
    if (d.downloaded_bytes) {
      const done = formatSize(d.downloaded_bytes)
      return d.total_bytes ? `（${done} / ${formatSize(d.total_bytes)}）` : `（已下载 ${done}）`
    }
  }
  if (t.current_step === 'asr' && d.phase === 'punctuate') {
    return d.total ? `（整理转写 ${d.done || 0}/${d.total} 段）` : '（整理转写）'
  }
  if (t.current_step === 'asr' && d.total_sec) {
    return `（${Math.round(d.done_sec / 60)}/${Math.round(d.total_sec / 60)} 分钟）`
  }
  if (t.current_step === 'objective_features' && d.total_sec) {
    const phase = { loudness: '响度与停顿', pitch: '语调分析', cached: '已恢复检查点', starting: '准备声学分析' }[d.phase] || '声学分析'
    return `（${phase} ${Math.round(d.done_sec / 60)}/${Math.round(d.total_sec / 60)} 分钟）`
  }
  if (t.current_step === 'slide_detection' && d.phase === 'roi') return '（定位投影）'
  if (t.current_step === 'vlm_describe' && d.total) return `（${d.done || 0}/${d.total}）`
  if (t.current_step === 'llm_judge' && d.dimension) return `（${d.dimension}）`
  return ''
}

function newEvaluation() {
  activeId.value = null
  result.value = null
  reportTab.value = 'overview'
  featureSubTab.value = 'content'
  clearMaterials()
}

async function loadTasks() {
  const requestId = ++taskListRequest
  try {
    const incoming = await evaluationApi.listTasks()
    if (requestId !== taskListRequest) return
    if (activeId.value && !incoming.some((task) => task.id === activeId.value)) {
      const selected = tasks.value.find((task) => task.id === activeId.value)
      if (selected) incoming.unshift(selected)
    }
    if (uploadTaskId.value && !incoming.some((t) => t.id === uploadTaskId.value)) {
      const local = tasks.value.find((t) => t.id === uploadTaskId.value)
      if (local) incoming.unshift(local)
    }
    tasks.value = incoming
    schedulePoll()
  } catch {
    /* 拦截器已提示 */
  }
}

function schedulePoll() {
  clearTimeout(pollTimer)
  const busy = tasks.value.some((t) => isRunning(t))
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
  if (id === uploadTaskId.value && uploadContext.value) {
    restoreUploadContext()
    return
  }
  const listed = tasks.value.find((t) => t.id === id)
  if (listed) applyTaskMaterials(listed)
  try {
    const task = await evaluationApi.getTask(id)
    if (!tasks.value.some((entry) => entry.id === id)) tasks.value.unshift(task)
    else tasks.value = tasks.value.map((entry) => entry.id === id ? task : entry)
    applyTaskMaterials(task)
  } catch {
    /* 拦截器已提示 */
  }
}

function restoreUploadContext() {
  const ctx = uploadContext.value
  if (!ctx) return
  if (ctx.videoUrl) {
    clearVideo()
    videoSource.value = 'link'
    remoteVideoLink.value = ctx.videoUrl
    remoteSharePassword.value = ctx.sharePassword || ''
    remoteShare.value = ctx.shareListing || null
    remoteSharePath.value = [...(ctx.sharePath || [])]
    remoteShareFileId.value = ctx.shareFileId || ''
  } else {
    setVideo(ctx.video)
  }
  syllabusFile.value = ctx.syllabus
  coursewareFile.value = ctx.courseware
  scriptFile.value = ctx.transcript
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
  const url = evaluationApi.fileUrl(taskId, 'video')
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
      featureSubTab.value = 'content'
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
      running ? '该任务尚未结束，现在只能先停止。确定请求停止？' : '确定删除这个评估任务？',
      '提示',
      { type: 'warning' }
    )
  } catch {
    return
  }
  if (running) {
    await cancelTask(t.id)
    return
  }
  try {
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
    if (id === uploadTaskId.value) uploadController?.abort()
    const response = await evaluationApi.cancelTask(id)
    ElMessage.success(response.status === 'cancel_requested' ? '正在安全停止评估' : '任务已停止')
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

function filenameFromRemoteUrl(value) {
  try {
    const name = decodeURIComponent(new URL(value).pathname.split('/').pop() || '')
    if (/\.(mp4|avi|mov|mkv|flv|wmv|webm|m4v)$/i.test(name)) return name.slice(0, 180)
  } catch {
    /* canStart 已经校验 URL */
  }
  return '链接视频.mp4'
}

function shouldSuggestFastUpload(file, durationSec) {
  return (
    Number(file?.size || 0) >= 300 * 1024 * 1024 &&
    Number(durationSec || 0) >= 15 * 60 &&
    typeof VideoDecoder !== 'undefined'
  )
}

function formatEtaSeconds(seconds) {
  if (!Number.isFinite(seconds)) return '未知'
  if (seconds < 60) return `${Math.max(1, Math.round(seconds))} 秒`
  return `${Math.max(1, Math.round(seconds / 60))} 分钟`
}

function chooseUploadMode(mode) {
  uploadMode.value = mode
  uploadModeManuallyChosen.value = true
}

async function refreshUploadRecommendation(file) {
  const request = ++recommendationRequest
  recommendationAnalyzing.value = true
  evidenceSummary.value = '正在实测网络和浏览器处理速度…'
  const work = (async () => {
    try {
      const [{ measureUploadSpeed, chooseUploadStrategy }, { benchmarkBrowserEvidence }] =
        await Promise.all([import('../utils/resumableUpload'), import('../utils/videoEvidence')])
      const network = await measureUploadSpeed()
      let descriptor = null
      try {
        descriptor = await benchmarkBrowserEvidence(file, {
          onProgress: ({ stage }) => {
            if (request === recommendationRequest) evidenceSummary.value = `${stage}…`
          },
        })
      } catch {
        descriptor = null
      }
      const strategy = chooseUploadStrategy(file, network, descriptor)
      if (request !== recommendationRequest || videoFile.value !== file) return null
      uploadRecommendation.value = { file, network, descriptor, strategy }
      if (!uploadModeManuallyChosen.value) uploadMode.value = strategy.mode
      const speed = network.megabitsPerSec.toFixed(network.megabitsPerSec >= 10 ? 0 : 1)
      const originalEta = formatEtaSeconds(strategy.originalSeconds)
      const fastEta = strategy.fastSeconds ? formatEtaSeconds(strategy.fastSeconds) : '不可用'
      evidenceSummary.value = `实测上行 ${speed} Mbps；原视频约 ${originalEta}，快速上传约 ${fastEta}。${strategy.reason}`
      return uploadRecommendation.value
    } catch (error) {
      if (request !== recommendationRequest || videoFile.value !== file) return null
      uploadRecommendation.value = null
      if (!uploadModeManuallyChosen.value) {
        uploadMode.value = shouldSuggestFastUpload(file, videoDurationSec.value) ? 'fast' : 'original'
      }
      evidenceSummary.value = '测速暂不可用，将按文件大小选择并保留原视频回退。'
      return null
    } finally {
      if (request === recommendationRequest) recommendationAnalyzing.value = false
    }
  })()
  recommendationPromise = work
  return work
}

function revokeVideoUrl() {
  if (videoUrl.value && videoUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(videoUrl.value)
  }
  videoUrl.value = ''
  videoPoster.value = ''
  videoDuration.value = ''
  videoDurationSec.value = 0
  videoWidth.value = 0
  videoHeight.value = 0
}

function setVideo(file) {
  videoSource.value = 'file'
  remoteVideoLink.value = ''
  videoFile.value = file
  uploadMode.value = 'original'
  uploadModeManuallyChosen.value = false
  uploadRecommendation.value = null
  recommendationRequest += 1
  evidenceSummary.value = ''
  evidencePercent.value = 0
  evidenceStage.value = ''
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
    videoDurationSec.value = Number(video.duration) || 0
    videoWidth.value = video.videoWidth
    videoHeight.value = video.videoHeight
    if (shouldSuggestFastUpload(file, videoDurationSec.value)) uploadMode.value = 'fast'
    refreshUploadRecommendation(file)
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
  recommendationRequest += 1
  recommendationPromise = null
  uploadRecommendation.value = null
  recommendationAnalyzing.value = false
  videoFile.value = null
  previewOpen.value = false
  revokeVideoUrl()
}

function chooseVideoSource(source) {
  if (uploading.value || source === videoSource.value) return
  if (source === 'link') clearVideo()
  else remoteVideoLink.value = ''
  videoSource.value = source
}

function clearMaterials() {
  clearVideo()
  remoteVideoLink.value = ''
  videoSource.value = 'link'
  syllabusFile.value = null
  coursewareFile.value = null
  scriptFile.value = null
}

async function startUpload() {
  if (!canStart.value) return
  const startedFromId = activeId.value
  const context = {
    video: videoFile.value,
    videoUrl: validRemoteVideoLink.value ? remoteVideoLink.value.trim() : null,
    sharePassword: remoteSharePassword.value.trim(),
    sharePath: [...remoteSharePath.value],
    shareFileId: remoteShareFileId.value,
    shareFilename: remoteShare.value?.files.find((f) => f.id === remoteShareFileId.value)?.name,
    shareListing: remoteShare.value,
    syllabus: syllabusFile.value,
    courseware: coursewareFile.value,
    transcript: scriptFile.value,
  }
  uploading.value = true
  uploadPercent.value = 0
  uploadContext.value = context
  uploadController = new AbortController()
  try {
    if (context.video && recommendationPromise) {
      await recommendationPromise
    }
    let fingerprint = null
    let created = null
    let resumeTools = null
    if (context.video) {
      resumeTools = await import('../utils/resumableUpload')
      fingerprint = await resumeTools.fileFingerprint(context.video)
      context.fingerprint = fingerprint
      const rememberedId = resumeTools.rememberedTaskId(fingerprint)
      if (rememberedId) {
        try {
          const remembered = await evaluationApi.getTask(rememberedId)
          if (
            ['uploading', 'upload_failed'].includes(remembered.status) &&
            remembered.filename === context.video.name
          ) {
            created = remembered
          } else {
            resumeTools.forgetTask(fingerprint)
          }
        } catch {
          resumeTools.forgetTask(fingerprint)
        }
      }
    }
    if (!created) {
      created = await evaluationApi.createTask(
        context.video?.name || context.shareFilename || filenameFromRemoteUrl(context.videoUrl)
      )
      if (fingerprint) resumeTools.rememberTask(fingerprint, created.id, context.video.name)
    }
    uploadTaskId.value = created.id
    if (activeId.value === startedFromId) activeId.value = created.id
    tasks.value = [created, ...tasks.value.filter((t) => t.id !== created.id)]
    schedulePoll()
    if (context.video) {
      await evaluationApi.uploadAuxMaterials(created.id, context, uploadController.signal)
      const { uploadOriginalVideo, createOrResumeSession } = await import('../utils/resumableUpload')
      const originalUpload = () =>
        uploadOriginalVideo({
          taskId: created.id,
          file: context.video,
          fingerprint,
          signal: uploadController.signal,
          onProgress: ({ percent, stage }) => {
            uploadPercent.value = percent
            evidenceStage.value = stage
          },
        })
      const descriptor = uploadRecommendation.value?.file === context.video
        ? uploadRecommendation.value.descriptor
        : null
      if (uploadMode.value === 'fast' && descriptor) {
        preparingEvidence.value = true
        evidencePercent.value = 0
        evidenceStage.value = '初始化边提取边上传'
        try {
          const session = await createOrResumeSession(created.id, context.video, {
            mode: 'evidence',
            fingerprint,
            audioFilename: descriptor.audio.filename,
            audioMime: descriptor.audio.mime,
          })
          const { streamBrowserEvidence } = await import('../utils/videoEvidence')
          const streamed = await streamBrowserEvidence(context.video, {
            taskId: created.id,
            session,
            descriptor,
            signal: uploadController.signal,
            onProgress: ({ percent, stage }) => {
              evidencePercent.value = percent
              uploadPercent.value = percent
              evidenceStage.value = stage
            },
          })
          await evaluationApi.completeUploadSession(created.id, {
            session_id: session.session_id,
            audio_parts: streamed.audioParts,
            frame_parts: streamed.frameParts,
            manifest: streamed.manifest,
          })
          const saved = Math.max(
            0,
            100 - (streamed.evidenceBytes / Math.max(context.video.size, 1)) * 100
          )
          evidenceSummary.value = `实际上传 ${formatSize(streamed.evidenceBytes)}，比原视频减少 ${saved.toFixed(1)}%`
        } catch (error) {
          if (error?.name === 'AbortError' || error?.code === 'ERR_CANCELED') throw error
          await evaluationApi.resetUploadSession(created.id)
          uploadMode.value = 'original'
          preparingEvidence.value = false
          evidenceSummary.value = '浏览器快速处理不兼容，已自动切换为原视频断点续传。'
          ElMessage.warning(`快速处理不可用，已回退原视频分片上传：${error?.message || '未知错误'}`)
          await originalUpload()
        } finally {
          preparingEvidence.value = false
        }
      } else {
        await originalUpload()
      }
    } else {
      await evaluationApi.uploadTaskMaterials(
        created.id,
        context,
        (p) => (uploadPercent.value = p),
        uploadController.signal
      )
    }
    const submitted = await evaluationApi.submitTask(created.id)
    if (fingerprint) resumeTools.forgetTask(fingerprint)
    tasks.value = [submitted, ...tasks.value.filter((t) => t.id !== created.id)]
    ElMessage.success('上传成功，已加入评估队列')
    void showFollowup(created.id)
    await loadTasks()
    if (activeId.value === created.id) {
      const latest = tasks.value.find((t) => t.id === created.id) || submitted
      applyTaskMaterials(latest)
    }
  } catch (err) {
    if (err?.code !== 'ERR_CANCELED') await loadTasks()
  } finally {
    preparingEvidence.value = false
    uploading.value = false
    uploadTaskId.value = null
    uploadContext.value = null
    uploadController = null
  }
}

function cancelLocalUpload() {
  uploadController?.abort()
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

onMounted(async () => {
  await loadTasks()
  if (typeof route.query.task === 'string' && /^[0-9a-f-]{36}$/i.test(route.query.task)) {
    await selectTask(route.query.task)
    if (activeTask.value?.status === 'completed') await viewResult()
    if (route.query.submitted === '1') void showFollowup(route.query.task)
  }
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
.upload-mode-picker {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid #f0f0f0;
}
.upload-mode-picker button {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 11px 13px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  background: #fff;
  color: #606266;
  text-align: left;
  cursor: pointer;
}
.upload-mode-picker button:hover,
.upload-mode-picker button.active {
  border-color: #a61b1b;
  background: #fff8f8;
}
.upload-mode-picker button:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}
.upload-mode-picker strong {
  color: #303133;
  font-size: 13px;
}
.upload-mode-picker strong em {
  display: inline-block;
  margin-left: 4px;
  padding: 1px 5px;
  border-radius: 999px;
  background: #a61b1b;
  color: #fff;
  font-size: 10px;
  font-style: normal;
  font-weight: 600;
}
.upload-mode-picker span,
.evidence-summary {
  color: #909399;
  font-size: 12px;
  line-height: 1.5;
}
.evidence-summary {
  margin-top: 9px;
  color: #2e8b57;
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
.video-source-card {
  padding: 14px 16px 16px;
  border: 1px solid #e6e6e6;
  border-radius: 10px;
  background: #fff;
}
.video-source-tabs {
  display: inline-flex;
  gap: 4px;
  margin: 14px 0;
  padding: 3px;
  border-radius: 8px;
  background: #f3f4f6;
}
.video-source-tabs button {
  padding: 7px 18px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #606266;
  cursor: pointer;
  font-size: 13px;
}
.video-source-tabs button.active {
  background: #fff;
  color: #a61b1b;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  font-weight: 600;
}
.video-source-tabs button:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}
.video-link-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 18px 20px 20px;
  border: 1px dashed #d8d8d8;
  border-radius: 10px;
}
.link-icon {
  color: #a61b1b;
}
.link-copy {
  margin: 9px 0 12px;
  color: #303133;
  font-size: 14px;
}
.video-link-panel .el-input {
  width: min(680px, 100%);
  margin-bottom: 8px;
}
.remote-file-picker {
  width: min(680px, 100%);
  margin-top: 8px;
  max-height: 260px;
  overflow-y: auto;
}
.remote-file-picker :deep(.el-radio) {
  height: auto;
  min-height: 32px;
  width: calc(100% - 8px);
}
.remote-file-picker :deep(.el-radio__label) {
  white-space: normal;
  overflow-wrap: anywhere;
  line-height: 1.5;
}
.video-link-panel .upload-hint,
.link-error,
.remote-progress {
  width: min(680px, 100%);
}
.video-link-panel .upload-hint {
  line-height: 1.6;
}
.link-error {
  margin-top: 6px;
  color: #c45656;
  font-size: 12px;
}
.remote-progress {
  margin-top: 4px;
}
.remote-progress-text {
  margin-top: 5px;
  color: #606266;
  font-size: 12px;
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
  .upload-mode-picker {
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
.task-status.upload_failed,
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
  color: #fff;
  border-color: #a61b1b;
  background: #a61b1b;
}
.export-btn:hover,
.export-btn:focus {
  color: #fff;
  border-color: #891616;
  background: #891616;
}

.report-tabs {
  display: flex;
  margin-top: 18px;
  border-bottom: 1px solid #ececec;
}
.report-tab {
  flex: 1 1 0;
  height: 40px;
  padding: 0 8px;
  border: none;
  background: transparent;
  color: #606266;
  font-size: 14px;
  text-align: center;
  white-space: nowrap;
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
.feature-page {
  padding-top: 20px;
}
.pace-page {
  display: flex;
  flex-direction: column;
  gap: 28px;
}
.pace-block h3 {
  margin: 22px 0 10px;
  font-size: 15px;
  font-weight: 600;
  color: #1f1f1f;
}
.pace-head h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #1f1f1f;
}
.pace-head p {
  margin: 6px 0 0;
  font-size: 13px;
  color: #8a8a8a;
}
.pace-heroes {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-top: 12px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}
.pace-hero b {
  display: block;
  font-size: 30px;
  font-weight: 800;
  color: #1f1f1f;
  line-height: 1.2;
}
.pace-hero span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  font-size: 13px;
  color: #8a8a8a;
}
.pace-extras {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 18px 12px;
  margin-top: 36px;
}
.pace-hero.compact b {
  font-size: 26px;
  font-weight: 700;
}
.pace-hero.compact span {
  margin-top: 4px;
  font-size: 13px;
  line-height: 1.35;
}
.pace-hero em,
.pace-table em {
  font-style: normal;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 999px;
}
.pace-hero em.tone-ok,
.pace-table em.tone-ok {
  background: #eaf6ee;
  color: #2e8b57;
}
.pace-hero em.tone-warn,
.pace-table em.tone-warn {
  background: #fff6e8;
  color: #d48806;
}
.pace-table em.tone-bad {
  background: #fdecec;
  color: #c45656;
}
.pace-table em.tone-fact {
  background: #f4f4f5;
  color: #909399;
}
.pace-charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  column-gap: 20px;
  row-gap: 8px;
  margin-top: 20px;
  align-items: stretch;
}
.pace-charts figure {
  display: contents;
}
.pace-charts figure:first-child > * {
  grid-column: 1;
}
.pace-charts figure:last-child > * {
  grid-column: 2;
}
.pace-charts figcaption {
  grid-row: 1;
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  line-height: 22px;
  color: #1f1f1f;
}
.pace-chart-frame {
  grid-row: 2;
  min-width: 0;
}
.pace-charts figure:first-child .pace-chart-frame {
  align-self: start;
}
.pace-chart-frame img {
  display: block;
  width: 100%;
  height: auto;
  background: #fff;
}
.pace-chart-frame-fit {
  position: relative;
  height: 0;
  min-height: 100%;
  align-self: stretch;
}
.pace-chart-frame-fit img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
}
.pace-block .pace-charts + .pace-detail,
.pace-block .audio-charts + .pace-detail {
  margin-top: 0;
  padding-top: 14px;
  border-top: 1px solid #f0f0f0;
}
.vision-page .pace-detail,
.tools-page .pace-detail {
  margin-top: 28px;
  padding-top: 28px;
  border-top: 1px solid #f0f0f0;
}
.pace-detail-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}
.pace-detail-head h3 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f1f1f;
}
.pace-detail-head h3 em {
  margin-left: 8px;
  padding: 2px 8px;
  font-style: normal;
  font-size: 12px;
  font-weight: 600;
  color: #a61b1b;
  background: #f8e8e8;
  border-radius: 999px;
  vertical-align: middle;
}
.pace-detail-leg {
  display: flex;
  gap: 14px;
  font-size: 12px;
  color: #8a8a8a;
}
.pace-detail-leg .dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 5px;
  border-radius: 50%;
  vertical-align: middle;
}
.pace-detail-leg .dot.ok {
  background: #2e8b57;
}
.pace-detail-leg .dot.warn {
  background: #d48806;
}
.pace-detail-leg .dot.fact {
  background: #fff;
  border: 1.5px solid #c0c4cc;
  box-sizing: border-box;
}
.audio-charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto auto auto;
  column-gap: 28px;
  row-gap: 16px;
  margin-top: 20px;
  align-items: stretch;
}
.audio-cap {
  font-size: 15px;
  font-weight: 600;
  line-height: 22px;
  color: #1f1f1f;
}
.audio-cap-wait {
  display: flex;
  align-items: baseline;
  gap: 12px;
}
.audio-cap-wait b {
  font-weight: 600;
}
.audio-cap-wait span {
  font-size: 12px;
  font-weight: 500;
  color: #8a8a8a;
}
.audio-cell {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}
.audio-cell img {
  display: block;
  width: 100%;
  height: auto;
  background: #fff;
}
.audio-wait {
  position: relative;
  min-height: 0;
}
.audio-wait img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: fill;
}
.audio-line span,
.audio-stack > span {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #1f1f1f;
}
.audio-line img {
  flex: 1 1 auto;
  min-height: 0;
}
.audio-dist {
  justify-content: space-evenly;
  gap: 12px;
}
.audio-facts {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
  gap: 45px;
}
.audio-facts .pace-obs-item {
  margin: 0;
  min-height: 0;
  height: auto;
  gap: 12px;
}
.audio-facts .pace-obs-ico {
  flex-basis: 72px;
  width: 72px;
  height: 72px;
}
.audio-facts .pace-obs-ico :deep(svg),
.audio-facts .pace-obs-ico svg {
  width: 38px;
  height: 38px;
}
.audio-facts .pace-obs-item b {
  font-size: 36px;
}
.audio-facts .pace-obs-item span {
  font-size: 16px;
}
.audio-stack {
  margin: 0;
}
.audio-bar {
  display: flex;
  height: 10px;
  overflow: hidden;
  border-radius: 99px;
  background: #f2f2f2;
}
.audio-bar i {
  display: block;
  height: 100%;
}
.audio-stack ul {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 14px;
  margin: 6px 0 0;
  padding: 0;
  list-style: none;
  font-size: 12px;
  color: #606266;
}
.audio-stack li {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.audio-stack li i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.audio-stack li b {
  font-weight: 600;
  color: #303133;
}
.vision-mid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 40px;
  margin-top: 28px;
  min-width: 0;
}
.vision-col {
  min-width: 0;
}
.vision-col > h3 {
  margin: 0 0 16px;
  font-size: 15px;
  font-weight: 600;
  color: #1f1f1f;
}
.vision-stack-row {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 14px;
  align-items: start;
  margin-bottom: 16px;
}
.vision-stack-row > span {
  padding-top: 2px;
  font-size: 13px;
  font-weight: 600;
  color: #303133;
  line-height: 1.4;
}
.vision-bar {
  display: flex;
  height: 12px;
  overflow: hidden;
  border-radius: 99px;
  background: #f2f2f2;
}
.vision-bar i {
  display: block;
  height: 100%;
}
.vision-stack-row ul {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 14px;
  margin: 8px 0 0;
  padding: 0;
  list-style: none;
  font-size: 12px;
  color: #606266;
}
.vision-stack-row li {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.vision-stack-row li i {
  width: 8px;
  height: 8px;
  border-radius: 2px;
}
.vision-find {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}
.vision-find + .vision-find {
  margin-top: 18px;
}
.vision-find .el-icon {
  flex: 0 0 auto;
  margin-top: 1px;
  color: #a61b1b;
}
.vision-find h4 {
  margin: 0 0 6px;
  font-size: 15px;
  font-weight: 600;
  color: #1f1f1f;
}
.vision-find h4.on {
  color: #a61b1b;
}
.vision-find p {
  margin: 0;
  font-size: 13px;
  line-height: 1.7;
  color: #8a8a8a;
}
.tools-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.tools-head p {
  margin: 0;
}
.tools-badge {
  flex: 0 0 auto;
  padding: 4px 10px;
  border-radius: 999px;
  font-style: normal;
  font-size: 12px;
  font-weight: 600;
  color: #2e8b57;
  background: #eaf6ee;
}
.tools-mid {
  display: grid;
  grid-template-columns: minmax(0, 0.72fr) minmax(0, 1.28fr);
  gap: 36px;
  margin-top: 28px;
  min-width: 0;
}
.tools-mid-wide {
  grid-template-columns: 1fr 1fr;
}
.tools-quality .vision-bar {
  max-width: 88%;
}
.tools-col,
.tools-axis-block {
  min-width: 0;
}
.tools-col > h3,
.tools-axis-block > h3 {
  margin: 0 0 16px;
  font-size: 15px;
  font-weight: 600;
  color: #1f1f1f;
}
.tools-axis {
  width: 100%;
}
.tools-axis svg {
  display: block;
  width: 100%;
  height: 58px;
}
.tools-axis-lg svg {
  height: 96px;
}
.tools-axis-leg {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 8px 0 0;
  font-size: 12px;
  color: #8a8a8a;
}
.tools-axis-leg i {
  width: 10px;
  height: 2px;
  background: #a61b1b;
}
.tools-minis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px 14px;
  margin-top: 20px;
}
.tools-minis .pace-obs-item {
  margin: 0;
  gap: 10px;
}
.tools-minis .pace-obs-ico {
  flex-basis: 40px;
  width: 40px;
  height: 40px;
}
.tools-minis .pace-obs-ico :deep(svg),
.tools-minis .pace-obs-ico svg {
  width: 20px;
  height: 20px;
}
.tools-minis .pace-obs-item b {
  font-size: 16px;
}
.tools-minis .pace-obs-item span {
  font-size: 12px;
}
.tools-axis-block {
  margin-top: 28px;
}
.tools-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}
.tools-pills span {
  padding: 4px 10px;
  border: 1px solid #eee;
  border-radius: 999px;
  font-size: 12px;
  color: #606266;
  background: #fff;
}
.tools-freq {
  display: block;
  width: 100%;
  height: auto;
  background: #fff;
}
.tools-dwell-body {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 12px 20px;
  align-items: center;
}
.tools-dwell-body .vision-find {
  grid-column: 1 / -1;
}
.tools-dwell-body ul {
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 12px;
  color: #606266;
}
.tools-dwell-body li {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
}
.tools-dwell-body li i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.tools-donut-wrap {
  position: relative;
  width: 140px;
  height: 140px;
}
.tools-donut {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  -webkit-mask: radial-gradient(farthest-side, transparent 58%, #000 59%);
  mask: radial-gradient(farthest-side, transparent 58%, #000 59%);
}
.tools-donut-label {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
.tools-donut-label b {
  font-size: 18px;
  font-weight: 800;
  color: #1f1f1f;
  line-height: 1.2;
}
.tools-donut-label span {
  margin-top: 4px;
  font-size: 12px;
  color: #8a8a8a;
}
.pace-obs {
  margin-top: 22px;
}
.pace-obs-body {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 12px 40px;
  align-items: center;
}
.pace-donut-card {
  text-align: center;
}
.pace-donut-wrap {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto;
}
.pace-donut-wrap svg {
  width: 100%;
  height: 100%;
}
.pace-donut-bg {
  fill: none;
  stroke: #f0f0f0;
  stroke-width: 12;
}
.pace-donut-arc {
  fill: none;
  stroke: #a61b1b;
  stroke-width: 12;
  transform: rotate(-90deg);
  transform-origin: 60px 60px;
}
.pace-donut-label {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
.pace-donut-label b {
  font-size: 32px;
  font-weight: 800;
  color: #1f1f1f;
  line-height: 1.1;
}
.pace-donut-label span {
  margin-top: 6px;
  font-size: 15px;
  color: #8a8a8a;
}
.pace-donut-card > p {
  margin: 8px 0 0;
  font-size: 14px;
  color: #8a8a8a;
}
.pace-obs-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px 0;
}
.pace-obs-grid.time {
  margin-top: 16px;
}
.pace-obs-item {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}
.pace-obs-ico {
  flex: 0 0 52px;
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #f8eaea;
  color: #a61b1b;
}
.pace-obs-ico :deep(svg),
.pace-obs-ico svg {
  width: 28px;
  height: 28px;
  display: block;
}
.pace-obs-item b {
  display: block;
  font-size: 26px;
  font-weight: 700;
  color: #1f1f1f;
  line-height: 1.15;
}
.pace-obs-item span {
  font-size: 14px;
  color: #8a8a8a;
}
@media (max-width: 960px) {
  .pace-obs-body,
  .pace-obs-grid {
    grid-template-columns: 1fr 1fr;
  }
}
.pace-hint {
  margin: 8px 0 0;
  font-size: 12px;
  color: #8a8a8a;
}
.pace-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.pace-table th,
.pace-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #f2f2f2;
  color: #303133;
  vertical-align: top;
}
.pace-table th {
  color: #8a8a8a;
  font-weight: 600;
  background: #fafafa;
}
.pace-table td:last-child {
  color: #606266;
  line-height: 1.5;
}
@media (max-width: 960px) {
  .pace-heroes,
  .pace-charts {
    grid-template-columns: 1fr 1fr;
  }
  .audio-charts,
  .vision-mid,
  .tools-mid {
    grid-template-columns: 1fr;
  }
  .pace-extras {
    grid-template-columns: repeat(3, 1fr);
  }
}
.feat-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
  font-size: 12px;
  color: #8a8a8a;
  white-space: nowrap;
}
.feat-tabs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin: 0 0 20px;
}
.feat-tab {
  height: 32px;
  padding: 0 12px;
  border: 1px solid #ececec;
  border-radius: 6px;
  background: #fff;
  color: #303133;
  font-size: 13px;
  cursor: pointer;
}
.feat-tab em {
  margin-left: 4px;
  font-style: normal;
  color: #8a8a8a;
}
.feat-tab small {
  margin-left: 4px;
  color: #b0b3b8;
  font-size: 11px;
}
.feat-tab.on {
  background: #a61b1b;
  border-color: #a61b1b;
  color: #fff;
}
.feat-tab.on em,
.feat-tab.on small {
  color: rgba(255, 255, 255, 0.85);
}
.feat-tab.off:not(.on) {
  color: #909399;
}
.feat-read {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-top: 16px;
  padding: 16px 18px;
  border: 1px solid #eeeeee;
  border-radius: 10px;
}
.feat-read h3 {
  margin: 0;
  flex-shrink: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f1f1f;
}
.feat-read ul {
  display: flex;
  flex-wrap: wrap;
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
}
.feat-read li {
  position: relative;
  padding: 0 16px 0 16px;
  border-right: 1px solid #eee;
  font-size: 13px;
  color: #303133;
  line-height: 1.5;
}
.feat-read li:last-child {
  border-right: none;
}
.feat-read li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 6px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #2e8b57;
}
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
.feature-cols.single {
  grid-template-columns: minmax(280px, 640px);
}
.feature-cols.single > div + div {
  margin-top: 22px;
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
