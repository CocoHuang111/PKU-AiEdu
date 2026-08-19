# 评估指标的处理思路

本文回答一个问题：`evaluation_criterion.md` 里的每一条三级指标，**由谁来算**。

配套文件：

- `evaluation_criterion.md` — 指标定义（人工维护的需求文档）
- `ai_engine/pedagogy/evaluation_rubric.yaml` — 指标的机器可读版本（代码实际读的）
- `ai_engine/pedagogy/feature_lexicon.yaml` — 本地统计用的词表与阈值

> **实施状态（2026-08-19）**：第六节的六个阶段已全部落地。
> 本地客观特征从 5 项扩到 44 项，视觉指标从自由文本改为结构化标签聚合。
> 验证：`make check-features`（不调大模型，70 项断言）。
> 下面第二节的「现状」列已按实现后的情况更新，第三、四节保留了设计推理
> 与**实现后仍然存在的局限**——那些局限不会因为代码写完就消失。

---

## 一、结论：方案可行，且当前代码已经是这个架构

「本地先算客观量 → 把客观量和原始模态一起喂给大模型 → 大模型输出二级/一级评分与报告」
这条路是对的，而且 `ai_engine/evaluation/` 已经按这个思路实现了：

```
视频 → media.extract_audio / extract_keyframes
     → providers/asr.py            转写（带时间戳）
     → text_features.py            文本客观特征（本地，纯 Python）
     → audio_features.py           声学客观特征（本地，librosa）
     → vision.py                   关键帧描述（VLM）
     → judge.py                    按维度逐个调 LLM 打二级指标分 → 加权汇总
     → pipeline.generate_report    生成文字报告
```

三级指标已经作为「观测点」注入提示词了，见 `prompts/eval_judge.j2` 第 7–13 行，
它遍历的 `ind.criteria` 就是 rubric 里的三级指标。客观特征以表格形式注入，
并明确告诉模型「这是事实，不要质疑」（第 24 行、33 行）。

所以要做的不是重建流程，而是**把该本地算的算干净**。目前的问题是：
有一批本来可以精确计算的指标，现在被含糊地丢给了大模型。下面逐条对照。

### 划分原则

判断一条指标该放哪一层，看它是否依赖语义理解：

| 层 | 判据 | 谁来做 |
| --- | --- | --- |
| **本地-确定** | 有明确定义的计算式，同一输入必得同一结果 | Python / librosa / ffmpeg |
| **本地-代理** | 能算出一个相关量，但「好不好」要人（模型）解读 | 代码算数值，LLM 解读 |
| **VLM-转录** | 需要看画面，但输出的是**观测事实**而非评价 | VLM 输出结构化标签，本地聚合成比例 |
| **LLM-判断** | 必须理解学科内容和教学意图 | LLM |

第三层是最容易被忽略、但收益最大的一层。**VLM 应该当「观测员」而不是「评委」**：
让它对每一帧回答「教师视线在看学生 / 看屏幕 / 看讲稿」，本地再统计
「看讲稿帧占比 = 35%」，把这个比例交给 Judge。而不是让 VLM 或 Judge
凭 12 段自由文本描述直接感觉「看稿行为多不多」。

目前 `eval_vision.j2` 输出的是 120 字以内的自由文本（见该文件第 10 行），
无法聚合成任何比例型指标 —— 这是当前最主要的结构性缺口，详见第四节。

---

## 二、逐指标对照表

「现状」列：✅ 有客观数据支撑 · ⚠️ 有数据但口径或证据有限 · ❌ 仍是纯语义判断

### 教学态度

| 三级指标 | 处理层 | 具体做法 | 现状 |
| --- | --- | --- | --- |
| 非正常停顿留白少 | 本地-确定 | RMS 静音检测，连续静音 > `long_pause_sec`(2.5s) 计一次；输出 `long_pause_count`、`long_pause_per_10min` | ✅ `audio_features.py` |
| 语气稳定 | 本地-代理 | `loudness_std`（响度波动）+ `pitch_std`（基频标准差）。数值稳不稳定是事实，「从容/紧张」的归因交 LLM | ✅ |
| 语调积极且富于变化 | 本地-代理 | `pitch_variation = pitch_std / pitch_median`（归一化的语调起伏度），配合 `emphasis_per_min`（响度峰值密度） | ✅ |
| 课程结构完整 | LLM-判断 | 需判断有无开场引入、主体、总结收束。本地辅助：`transition_count` 与后段/前段语速比 | ⚠️ 无开场/收束的时间位置特征 |
| 纪律提醒、点名提问适时 | 本地-代理 | `discipline_markers` 已从 `interaction_markers` 拆出，单独计 `discipline_count` | ⚠️ 只有总数，无时间轴分布 |
| 课件/板书设计详细完整 | VLM-转录 | 每帧标 `board_present` / `board_content` → `board_present_ratio`、`board_diagram_ratio` | ✅ `vision.py` |
| 看稿、读屏行为少 | VLM-转录 | 每帧标 `gaze` 五分类 → `gaze_script_ratio`、`gaze_screen_ratio` | ✅ |
| 手势动作自然、表情自然、目光专注 | VLM-转录 | 每帧标 `gesture` / `posture` → `gesture_active_ratio`、`walking_ratio` | ⚠️ 表情未标注（关键帧分辨率不足） |

### 教学内容

这个维度**大部分是语义判断，本地只能提供线索**。

| 三级指标 | 处理层 | 具体做法 | 现状 |
| --- | --- | --- | --- |
| 本节课内容完整闭环 | LLM-判断 | 根据转写判断本节课是否形成知识闭环（引入—展开—收束），不对照整门课大纲。外部清单仅作选填辅助 | ✅ |
| 逻辑层次清晰，概念-原理-案例链条完整 | LLM-判断 | 本地辅助：`transition_count`（过渡衔接词次数） | ⚠️ 仅辅助 |
| 详略结合，重点难点讲解充分 | LLM-判断 | 本地辅助：分段语速与后段/前段语速比 | ⚠️ 缺术语时间轴驻留特征 |
| 引入实际案例、社会情境等 | 本地-代理 | `case_markers` 词表 → `case_count`。充分性交 LLM | ✅ |
| 引用最新研究成果、行业动态或最新数据 | 本地-代理 | `recency_markers` + 正则抽年份 → `recency_count`、`year_ref_count` | ✅ |
| 高阶/推理问题比例合理 | 本地-代理 | 布鲁姆词表给提问句分类 → `higher_order_question_ratio`，未命中的不计入分母 | ✅ |
| 无知识性错误 | LLM-判断 | 权重降到 0.6，且提示词要求「只报有明确把握的错误、逐条引原文、注意 ASR 同音字误识」 | ⚠️ 本质不可靠，已限权 |

### 教学方法

| 三级指标 | 处理层 | 具体做法 | 现状 |
| --- | --- | --- | --- |
| 提问后保留有效思考等待时间 | **本地-确定** | 提问句落在片段末尾时，取该段 `end` 到下一段 `start` 的间隔 → `wait_time_mean/median`、`wait_time_effective_ratio`（≥3s） | ✅ `timeline_features.py` |
| 提问次数 | 本地-确定 | 句尾问号 + `question_markers` 词表；输出 `question_count`、`question_per_10min` | ✅ |
| 启发技巧使用 | 本地-代理 | `inspire_markers` 词表 → `inspire_count` | ✅ |
| 开放性问题占比合理 | 本地-确定 | `open_question_markers` 命中的提问句 / 全部提问句 → `open_question_ratio`；另有 `question_gini` 看分布是否均匀 | ✅ |
| 追问充分 | 本地-代理 | 设计过提问簇检测，但没有说话人分离就分不清「追问」与「连续自问自答」 | ❌ 待第四节 (3) |
| 板书/课件布局清晰 | VLM-转录 | 每帧标 `board_content` → `board_diagram_ratio` | ⚠️ 未标「重点是否突出」 |
| 板书/课件可读性高 | VLM-转录 | 每帧标 `board_readable` → `board_readable_high/low_ratio` | ✅ |
| 板书/课件停留充分 | **本地-确定** | 密集抽帧（默认 3s）+ 灰度帧差 → 切换时刻 → `dwell_median_sec`、`dwell_short_ratio` | ✅ `slide_features.py` |
| 课件切换与讲授同步 | 本地-代理 | 切换时刻 ±10s 内是否有过渡话语 → `slide_sync_ratio` | ✅ |
| 多媒体切换使用熟练 | 本地-代理 | `blank_frame_ratio`（黑屏白屏帧占比）作为操作卡顿的代理量 | ⚠️ 代理较弱 |

### 教学素质

| 三级指标 | 处理层 | 具体做法 | 现状 |
| --- | --- | --- | --- |
| 口齿清晰 | 本地-代理 | `ASRSegment` 已保留 `avg_logprob`，按时长加权 → `asr_confidence`、`asr_low_confidence_ratio` | ⚠️ 弱代理，见第三节 (3) |
| 语速整体稳定 | **本地-确定** | 分段语速的变异系数 `speech_rate_cv` | ✅ |
| 重点内容语速调整、语调变化 | 本地-代理 | `speech_rate_cv` + `pitch_variation`。「是否发生在重点处」需 LLM 对齐内容 | ⚠️ |
| 时间分配合理 | 本地-代理 | `speech_rate_late_ratio`（后 1/3 段 / 前 1/3 段语速）检测前松后紧 | ✅ |
| 冗余词频率低 | 本地-确定 | `filler_markers` → `filler_density`（次/百字） | ✅ |
| 用词准确无歧义 | LLM-判断 | 纯语义 | ❌ 本质如此 |
| 过渡自然 | 本地-代理 | `transition_count` 辅助 + LLM 判断 | ✅ |
| 眼神交流充分 | VLM-转录 | `gaze_students_ratio`（与「看稿读屏」共用同一组标签） | ✅ |
| 肢体表达自然 | VLM-转录 | `gesture_active_ratio`、`walking_ratio` | ✅ |

### 教学效果

**这个维度仍然最弱**，除非开启说话人分离，见第四节 (3)。

| 三级指标 | 处理层 | 具体做法 | 现状 |
| --- | --- | --- | --- |
| 课堂整体噪音小 | 本地-确定 | 有声帧能量 / 静音帧能量 → `snr_estimate` | ✅ `audio_features.py` |
| 学生回答语气坚定 | 本地-代理 | 需要说话人分离才能定位学生片段并测其响度/基频 | ⚠️ 仅开启 pyannote 后可评 |
| 学生提问/发言次数 | 本地-代理 | 开启分离 → `student_turn_count`、`student_speech_ratio`；否则退回 `student_speech_count` 词表粗估 | ⚠️ 默认口径偏高（已标注） |
| 学生回答正确率高、逻辑清晰 | LLM-判断 | 依赖能否定位学生发言片段 | ⚠️ 同上 |

### 汇总

指标文档共 38 条三级指标：

| 处理层 | 条数 | ✅ | ⚠️ | ❌ |
| --- | --- | --- | --- | --- |
| 本地-确定 | 8 | 8 | 0 | 0 |
| 本地-代理 | 16 | 9 | 6 | 1 |
| VLM-转录 | 7 | 5 | 2 | 0 |
| LLM-判断 | 7 | 1 | 3 | 3 |
| **合计** | **38** | **23** | **11** | **4** |

对比实施前（✅ 12 / ⚠️ 17 / ❌ 9）：

- **本地-确定 8 条全部落地**。此前完全没做的提问等待时间、课件停留时长补齐了，
  语速稳定性的分段汇总也接上了。这 8 条不再经过大模型的主观判断。
- **VLM 7 条从「全部只有自由文本」变成 5 条有比例型数值**。剩下 2 条是标注
  粒度问题：「表情自然」需要人脸特写，关键帧分辨率不够；「重点是否突出」
  需要理解板书语义，超出了「观测员」的职责。
- **剩下 4 条 ❌ 有两类**：3 条是本质上的语义判断（用词准确无歧义等），本地
  无从下手；1 条是「追问充分」，卡在说话人分离上，开启 pyannote 后可解。

客观特征从 5 项（实施前 text 8 + audio 8，其中多项未被计算）扩到 **44 项已登记特征**，
分 6 组标注来源。`make check-features` 会校验「代码算出的 key 都在 rubric 里有标签」，
防止新增特征忘记登记后静默不进证据表。

---

## 三、本地指标的实现要点

以下五项均已落地。保留每项的**实现后仍存在的局限**——这些不会因为代码写完就消失，
是解读分数时必须知道的前提。

### (1) 提问等待时间 · `timeline_features.py`

对应经典的 wait-time 研究（Rowe）：等待 3 秒以上，学生回答的长度和质量显著提升。
所以除均值外单独报 `wait_time_effective_ratio`（≥3 秒的提问占比）。

实现：遍历 `asr_result.segments`，**只取问句正好落在片段末尾的样本**，
取该段 `end` 到下一段 `start` 的间隔。

三处必须知道的处理：

- Whisper 片段是 5–30 秒的块。问句落在片段中间时，段间间隔测的不是提问后的
  停顿，算进来只会污染统计，所以直接排除，并把 `wait_time_sample_count`
  一起报给 Judge。提示词里写明「样本数低于 5 时 confidence 不得高于 medium」。
- 间隔超过 `wait_time_cap_sec`（默认 30 秒）的按 30 秒截断。这种长间隔更可能是
  ASR 漏转写或学生答话没被拾音，不是教师主动留白，不截断会把均值整体拉高。
- `asr.vad_filter: true` 虽然过滤静音段，但片段时间戳仍在原始时间轴上，
  间隔照样能测，不受影响。

**仍存在的局限**：样本量取决于教师的提问是否恰好在片段边界，一堂课往往只有
个位数有效样本。想要更准需要 `word_timestamps=True` 拿词级时间戳，
代价是转写变慢约 20–30%，暂未开启。

### (2) 课件切换检测 · `slide_features.py`

对应「板书/课件停留充分」「课件切换与讲授同步」「多媒体切换使用熟练」三条。

实现：`media.iter_gray_frames()` 用一次 ffmpeg 调用，按 `fps=1/interval` 抽
160×90 灰度帧，**走管道流式 yield，不落盘也不在内存里堆帧**。
`_scan_frames()` 单趟扫过帧流，只保留上一帧，同时得到总帧数、切换位置、纯色帧数 ——
所以内存占用与视频长度、抽帧间隔都无关（实测把间隔调到 0.1 秒，峰值内存增量
约 1 MB）。相邻帧平均灰度绝对差归一化到 0~1，超 `slide_change_threshold`
判为一次切换。零 API 调用。

产出 `slide_change_count`、`dwell_median_sec`、`dwell_short_ratio`（停留 < 20 秒
的页面占比）、`slide_sync_ratio`、`blank_frame_ratio`。

**仍存在的局限**（已写进提示词，避免 Judge 当成精确值）：

- 固定机位下「教师走动」也会造成画面差异，所以**切换次数是上界而非精确值**。
  要更准需要先框定屏幕区域再比对，而屏幕位置本身得先识别 —— 可以让 VLM
  在第一帧定位一次屏幕矩形后续复用，目前没做。
- `slide_sync_ratio` 只说明切换与话语节奏对得上，**不代表讲的内容与页面内容一致**，
  后者是语义判断。
- 没有转写时该项**缺省而不是填 0**，否则「缺测」会被读成「实测为 0」。

### (3) ASR 置信度作为口齿清晰的代理

`ASRSegment` 现在保留了 `avg_logprob` 与 `no_speech_prob`，按片段时长加权平均
得到 `asr_confidence`（等权平均会让一句「嗯」和一段三十秒讲授占同样分量）。

**这是本次新增特征里最弱的一个**：它混杂了录音质量、口音、专业术语生僻度，
不是纯粹的「口齿清晰度」，而且**不同 whisper 模型规模之间数值不可比**
（换 `asr.model` 后历史数据就失去可比性）。提示词里已明确写成「弱代理」，
否则 Judge 会当硬指标用。

### (4) 分段特征的汇总 · `summarize_segments()`

`segment_transcript()` 早就算出了每段特征，只是没汇总。现在产出：

- `speech_rate_cv` — 分段语速变异系数 → 「语速整体稳定」
- `speech_rate_late_ratio` — 后 1/3 段 / 前 1/3 段的平均语速 → 「前松后紧」
  （取三分之一而非首尾单段，单段容易被一次口误或一段噪声带偏）
- `question_gini` — 提问分布的基尼系数，归一化到 [0,1]，0 = 均匀
- `question_free_segment_ratio` — 无提问段落占比

段数少于 2 时不做汇总（返回空），避免拿一个段算出「变异系数 0」这种假稳定。

### (5) 词表扩充 · `feature_lexicon.yaml`

新增四组，`_count_markers` 逻辑通用，无需改代码：

- `case_markers` — 案例引入 → `case_count`
- `recency_markers` — 前沿表述 → `recency_count`（配合正则抽 `20\d{2}` 年份）
- `bloom_higher_markers` / `bloom_lower_markers` — 认知层级分类
- `discipline_markers` — 纪律提醒与点名，**已从 `interaction_markers` 里拆出**

**词表法的固有局限**：只看字面。「案例」出现在「这个案例不好」里也会计数，
布鲁姆分类里两表都没命中的提问计为「未分类」并**排除在比例的分母外**
（`classified_question_count` 一起上报），避免比例虚高。这些数字是「线索的强度」，
不是「事实的精确度」。

---

## 四、方法论上的硬缺口

这几条不是「补个函数」能解决的，需要单独决策。

### (1) VLM 输出必须结构化

原先 `eval_vision.j2` 要求「控制在 120 字以内，一段话写完」。自由文本的后果：
12 帧描述作为 12 条 bullet 塞进 Judge 提示词，Judge 只能读一遍留个印象，
**7 条视觉三级指标全都退化成了印象打分**。

现在 VLM 每帧输出固定字段的 JSON，`LABEL_SCHEMA` 定义了每个字段的合法取值：

```json
{
  "gaze": "students | screen | script | audience_away | unclear",
  "gesture": "none | pointing | illustrative | writing | unclear",
  "posture": "standing_front | walking | behind_podium | seated | unclear",
  "board_present": "blackboard | slide | both | none | unclear",
  "board_content": "text_heavy | diagram | mixed | none | unclear",
  "board_readable": "high | medium | low | none | unclear",
  "students_visible": 24,
  "heads_up": "high | medium | low | unclear",
  "hands_raised": "yes | no | unclear",
  "note": "一句话补充"
}
```

`aggregate_vision_features()` 把它们聚合成 `gaze_script_ratio`、
`board_readable_high_ratio`、`heads_up_high_ratio` 等 15 项比例型特征，
和文本/声学特征一起进证据表。VLM 从「评委」变回「观测员」。

三个防假数据的设计：

- **`unclear` 留在分母里**，并单独上报 `gaze_unclear_ratio`、
  `heads_up_unclear_ratio`。悄悄剔除看不清的帧会让「看学生占比」虚高，
  Judge 也无从知道这个数字建立在几帧证据上。提示词里写明
  「无法判断帧占比偏高时 confidence 应设为 low」。
- **表外取值归为 `unclear`**。模型偶尔会直接答中文（如 `"gaze": "看学生"`），
  不做校验的话这个臆造标签会静默进入分母，把比例算错。
- **单帧失败不影响其余帧**，失败帧 `ok=False` 并排除在聚合之外。

**仍存在的局限**：「表情自然」没有纳入标注 —— 关键帧是整个教室的全景，
分辨率不足以判断面部表情，硬让 VLM 标只会得到编造的标签。
「板书重点是否突出」也没标，那需要理解板书语义，超出「观测员」的职责。

### (2) 关键帧 12 张对时间敏感指标太稀疏 → 双轨

`keyframe_count: 12` 在 45 分钟课约每 3.75 分钟一帧。对「教态」「板书风格」
这类稳态特征够用，但对「停留充分」「切换同步」完全不够。

现在分成两条独立配置的轨：

| 轨 | 配置项 | 间隔 | 成本 | 用途 |
| --- | --- | --- | --- | --- |
| 稀疏轨 | `keyframe_count: 12` | ~3.75 分钟 | 每帧一次 VLM 调用 | 教态、板书风格、抬头率 |
| 密集轨 | `slide_sample_interval_sec: 3.0` | 3 秒 | 一次 ffmpeg 解码 + numpy | 切换时刻、停留时长 |

密集轨点亮 `vision` 模态，所以**即使 `vlm_enabled: false`，板书停留与切换同步
仍然可评**，不再整片标为未评估。

### (3) 说话人分离 · 默认关闭

`student_speech_markers` 用「我觉得」「我认为」判定学生发言，但**教师讲课时说
这些词的频率远高于学生**，这个统计系统性高估，方向上就不可信。
受影响的是「教学效果」四条里的三条，以及「追问充分」。

`diarization.py` 接了 `pyannote-audio`：主讲人 = 总时长占比最高的说话人，
其余归为学生。产出 `student_turn_count`、`student_speech_ratio`、
`turn_exchange_count`（师生轮次交替次数，这才是「有来有回」的直接证据）。

**默认关闭**（`evaluation.diarization_enabled: false`），因为：需要装
`requirements-local.txt`、需要 HF token 并在模型页接受条款、CPU 上 45 分钟音频
约 10–20 分钟。任何一步缺失都抛 `DiarizationError`，流水线记一条 warning 继续跑，
不会让整次评估失败。

关闭时的诚实处理：`student_speech_count` 的 rubric 标签直接写成
「学生发言线索次数（词表粗估，偏高）」，提示词里也写明
「该数字系统性偏高，只能当弱线索，不要据此断言学生参与充分」。

### (4) 「内容完整性」有大纲对照大纲，没有大纲评转写闭环

原先认为没有大纲就无法判断「应覆盖什么」，因此缺参照就标未评估。
后来改成只看转写闭环，并禁止按整门课覆盖面打分。现在口径随材料切换：

- **教师上传了课程大纲**：对照大纲中与本节课相关的安排来评完整性。
  若大纲覆盖整门课，先根据转写判断本节对应哪一部分，再对照该部分，
  不要把未安排在这节课的后续章节当成缺漏。
- **没有大纲**：根据转写判断本节课自身是否完整闭环（主题是否交代、
  核心是否讲完、有无收束）。

课件同理：有上传课件则以课件文件评版式与可读性；没有则根据课堂关键帧。
`requires_reference` 机制仍留在 `judge.py`，目前没有任何指标启用。

### (5) 「无知识性错误」已限权

通用大模型对具体学科的事实核查能力有限，既会漏报也会误报。两处一起改：

- rubric 里 `accuracy.weight` 从 1.0 降到 **0.6**。实测该项被打 0 分时，
  「教学内容」维度得 73.2 分；若维持同权则会掉到 68.3 分。
- 提示词追加约束：只报有明确把握的错误、逐条引用原文、
  **注意转写本身可能有同音字误识，不要把 ASR 错误当成教师讲错**、
  没把握时给 `confidence: low`。

---

## 五、rubric 与指标文档的差异（已对齐）

原先四处不一致，现已全部修正：

| 位置 | 指标文档 | 原 rubric | 处理 |
| --- | --- | --- | --- |
| 教学态度/教师教态 | 语调积极且富于变化 | 「语**速**积极且富有变化」 | ✅ 已改为「语调」。原文案会误导 Judge 拿语速数据评语调 |
| 教学方法/二级指标 | 教学资源**融合** | 教学资源**整合** | ✅ 已统一为「融合」 |
| 教学内容 | 高阶/推理问题比例合理 | 挂在「学科前沿融入」下 | ✅ 已移到同维度的「重点难点设计」。认知层级属于内容深度，与学科前沿是两件事；留在教学内容维度内以保持与指标文档的维度归属一致 |
| 教学素质/时间控制 | 时间分配合理 | 已含 | 无需改动 |

前三项都有 `make check-features` 的断言兜着，改回去会立刻失败。

**三级观测点已按 `evaluation_criterion.md` 对齐（2026-08-19）**：删掉 rubric 自行扩写的观测点，措辞改回指标文档原文。删掉的包括：

- 课堂秩序良好
- 章节之间有明确的承接关系
- 难点有拆解、有铺垫
- 显性呈现思考路径与方法论
- 教师对学生反馈有确认与纠正
- 学生抬头率高
- 师生问答形成有来有回的交流
- 氛围活跃但不失秩序

**两个二级指标在指标文档里没有对应的三级观测点**：`思维引导`、`教学资源融合`。
没有自行编造观测点，Judge 按二级名称本身评分。若以后要给它们三级指标，先写进
`evaluation_criterion.md`，再同步 rubric。

`make check-features` 会把 rubric 里每一条 criterion 与指标文档的条目做集合比对，
多出来立刻失败。

---

## 六、实施顺序（六阶段已全部完成）

| 阶段 | 内容 | 依赖 | 状态 |
| --- | --- | --- | --- |
| 1 | 分段特征汇总 + 词表扩充 + rubric 对齐 | 无新依赖 | ✅ |
| 2 | 提问等待时间 + ASR 置信度 | 无新依赖 | ✅ |
| 3 | VLM 输出结构化 | 改 prompt + 聚合 + 前端 | ✅ |
| 4 | 课件切换检测 + 密集抽帧轨 | numpy（已有） | ✅ |
| 5 | 知识点参照输入 | 前端加输入项 + DB 加列 | ✅ |
| 6 | pyannote 说话人分离 | 可选依赖 + HF token | ✅ 已接入，**默认关闭** |

### 落地清单

新增模块：

- `ai_engine/evaluation/timeline_features.py` — 提问等待时间、ASR 置信度
- `ai_engine/evaluation/slide_features.py` — 课件切换、停留时长、讲授同步
- `ai_engine/evaluation/diarization.py` — 说话人分离（可选）
- `ai_engine/evaluation/materials.py` — 课程大纲文本抽取、课件渲染为页面图像
- `scripts/check_features.py` — 本地特征自检，`make check-features`

结构性改动：

- `build_evidence()` 签名从 `(transcript, duration, text_features, audio_features,
  vision_notes)` 改为 `(transcript, duration, features: dict[str, dict],
  vision_notes, reference)`，`features` 的键与 rubric 的 `objective_features`
  分组一一对应。加一组特征 = rubric 加一段 + 往 `features` 塞一个键。
- `objective_features` / `raw_features` 从 2 组扩到 7 组，前端按组渲染并标注来源。
- `keyframes[].labels` 新增结构化标签，`description` 保留为渲染后的中文串
  （前端仍可直接展示，改动是加法而非替换）。
- `eval_tasks` 表新增 `reference` / `syllabus_path` / `courseware_path` 列，
  `init_db()` 里加了 `ALTER TABLE` 迁移
  （`CREATE TABLE IF NOT EXISTS` 不会给已存在的表补列），幂等可重复执行。

### 下一步可做的

按收益排序，都不在原六阶段内：

1. **说话人分离跑通一次真实课堂**，验证「学生发言」口径能不能落地。这是
   剩下 4 条 ❌ 里唯一有解的一条。
2. **屏幕区域定位**：让 VLM 在第一帧框出投影区域，密集轨只比对该区域，
   把「切换次数是上界」变成精确值。
3. **术语时间轴驻留特征**：某术语首次到末次出现跨多少分钟、占多少字，
   给「详略结合」提供客观依据。
4. **词级时间戳**（`word_timestamps=True`）：让提问等待时间不再受片段边界限制，
   代价是转写慢 20–30%。
5. **指标文档若增补三级观测点**（例如给「思维引导」「教学资源融合」补三级），
   先改 `evaluation_criterion.md`，再同步 rubric。`make check-features` 会拦住反向操作。
