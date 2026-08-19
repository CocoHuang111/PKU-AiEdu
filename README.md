# 北大问教 2.0

面向高校教师的智能教学支持系统。三个功能：

| 功能 | 输入 | 输出 |
| --- | --- | --- |
| ① 教学视频质量评估 | 教学视频 | 五维雷达图 + 24 项二级指标明细 + 诊断报告 |
| ② 教学大纲优化 | PDF / Word / Markdown 大纲 | 结构化 XML 大纲 + 改动留痕 |
| ③ 教学智能问答 | 自然语言提问 | 基于多语料库检索的带引用回答 |

技术栈：Vue 3 + Vite + Element Plus 前端，FastAPI 后端，Chroma 向量库。
**大模型（LLM / VLM / Embedding）默认走通义千问云端 API**；语音识别（ASR）固定本地 faster-whisper，不随 mode 切换。

> **本文档持续维护**。整体框架、运行命令、待解决问题、每次改动的思路都记录在这里，
> 是了解项目状态的唯一入口。约定见 `.cursor/rules/maintain-readme.mdc`。

---

## 一、环境要求

| 依赖 | 版本 | 说明 |
| --- | --- | --- |
| Python | **3.11** | 必须。3.13+ 在 arm64 上没有 ctranslate2 / chromadb 的 wheel |
| Node.js | ≥ 18 | 前端构建 |
| ffmpeg | 任意近期版本 | 抽音频与关键帧，`brew install ffmpeg` |
| Docker | **不需要** | 全部本地进程运行 |

大模型通道（**默认云端**）：

- **云端（默认）**：通义千问 API Key，在 [阿里云百炼](https://bailian.console.aliyun.com/) 申请。
  `.env` 中 `PKU_MODE=cloud`（`.env.example` 已预设）。
- **本地（可选，需显式开启）**：[Ollama](https://ollama.com)，设置 `PKU_MODE=local`，
  需要 `ollama pull qwen2.5:3b bge-m3`，视觉分析还需要 `ollama pull qwen2.5vl:7b`（约 6GB）。

语音识别（ASR）始终本地 faster-whisper，**不是大模型**，无云端切换选项。

---

## 二、安装

```bash
# 1. Python 环境（必须 3.11）
conda create -n pku2 python=3.11 -y
conda activate pku2
make install

# 2. 系统依赖
brew install ffmpeg

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 DASHSCOPE_API_KEY

# 4. 自检
make check
```

`make check` 会逐项告诉你 Python 版本、ffmpeg、各依赖包、API Key 连通性、
向量库状态是否就绪，缺什么给什么命令。

---

## 三、启动

```bash
# 建向量库（首次必做，之后往语料目录加文档时再跑）
make ingest

# 两个终端分别启动
make backend     # http://localhost:8010/docs
make frontend    # http://localhost:5174
```

浏览器打开 http://localhost:5174 即可。

---

## 四、命令速查

| 命令 | 作用 |
| --- | --- |
| `make check` | 环境自检：Python / ffmpeg / 依赖 / API Key / 向量库 |
| `make check-features` | 客观特征自检：词表、分段汇总、等待时间、VLM 标签解析、rubric 对齐（**不调大模型，不花额度**） |
| `make check-syllabus` | 大纲优化单元测试：XML/Markdown 校验、分章生成、导出（**不调大模型**） |
| `make install` | 安装基础依赖 |
| `make install-local` | 安装可选依赖：本地 embedding / rerank、说话人分离 |
| `make backend` | 启动 FastAPI（8010），带 `--reload` |
| `make frontend` | 启动 Vite（5174） |
| `make ingest` | 增量构建向量库 |
| `make ingest-reset` | 清空后重建向量库（换 embedding 模型后必须） |
| `make salon` | 沙龙 mp4 → ASR(small) 转写 + LLM 提取教学知识 → Markdown |
| `make salon-transcribe` | 只做沙龙 ASR 转写（结果在 `.work/`） |
| `make salon-structure` | 只做沙龙 LLM 结构化（需已有转写） |
| `python -m knowledge.ingest --corpus pku_salon` | 只重建沙龙语料库 |
| `make clean` | 清理 `__pycache__` |
| `make smoke` | 纯文本跑通「打分 → 报告」链路（会调大模型） |
| `python -m scripts.smoke_test --reference` | 同上，附带课程大纲文本，对照大纲评完整性 |
| `python -m scripts.qa_test "问题"` | 跑通「关键词 → 检索 → 生成」链路 |
| `python -m scripts.test_parsing` | 校验对大模型跑偏输出的容错解析 |
| `python -m scripts.test_eval_dataset` | 微格数据集 inventory 匹配（**不调大模型**） |
| `python -m scripts.build_eval_dataset inventory ...` | 扫描教师文件夹 + 打分表，写 inventory/manifest |
| `PKU_MODE=local <任意命令>` | 强制走本地 Ollama，无需 API Key |
| `git status` | 本地仓库；**无远程**。视频、xlsx、`.env`、模型、cache 已 ignore |
| `lsof -ti :8010 \| xargs kill -9` | 端口被占用时强杀 |

---

## 五、整体框架

### 分层

```
frontend/          Vue 3 单页应用，只管展示与交互
      │  HTTP / SSE（Vite 代理 /api → 8010）
backend/app/       FastAPI：路由、参数校验、SQLite 持久化、异步任务调度
      │  直接函数调用
ai_engine/         AI 能力层，不依赖任何 Web 框架，可独立在脚本里跑
      │
      ├── providers/   能力抽象：LLM / VLM / Embedding / Rerank / ASR
      ├── pedagogy/    教育学底座：指标体系、XML schema、提示词模板
      ├── evaluation/  功能① 流水线
      ├── syllabus/    功能② 大纲优化
      ├── qa/          功能③ 问答
      └── rag/         文档解析、分块、Chroma 读写、检索
```

**依赖方向是单向的**：`backend` 依赖 `ai_engine`，反过来不行。所以三个功能
都能脱离 Web 服务单独在命令行里调试（`scripts/` 下的几个脚本就是这么用的）。

### 目录

```
├── config.yaml              # 统一配置：模型、语料库、评估参数
├── .env                     # API Key（不入库；从 .env.example 复制）
├── .env.example             # 环境变量模板，不含真实 Key
├── evaluation_criterion.md  # 评估指标的需求定义（人工维护，五维 38 条三级指标）
├── evaluation_design.md     # 每条三级指标由谁来算：本地 / VLM / LLM 的划分与缺口
├── ai_engine/
│   ├── config.py            #   读 config.yaml，按 mode 解析出各能力的配置
│   ├── providers/           #   base.py 定接口，llm/embedding/asr.py 给实现
│   ├── pedagogy/
│   │   ├── evaluation_rubric.yaml   # 五维 24 项指标 + 客观特征标签（改这里就能调）
│   │   ├── feature_lexicon.yaml     # 文本特征统计词表与判分阈值
│   │   ├── syllabus_schema.xml      # 大纲级 XML 结构（与 markdown_schema 对齐）
│   │   ├── syllabus_markdown_schema.md # 大纲 Markdown 固定框架
│   │   └── prompts/*.j2             # Jinja2 提示词
│   ├── evaluation/          #   media / judge / pipeline
│   │                        #   特征提取按来源分文件：
│   │                        #     text_features     转写文本统计 + 分段汇总
│   │                        #     audio_features    librosa 声学特征
│   │                        #     timeline_features 提问等待时间、ASR 置信度
│   │                        #     slide_features    课件切换（本地帧差，无 API）
│   │                        #     materials         教师上传的大纲/课件解析
│   │                        #     vision            VLM 结构化标注 + 聚合
│   │                        #     diarization       说话人分离（可选，默认关）
│   ├── syllabus/optimizer.py
│   │             export.py      # XML → Markdown / docx / pdf
│   ├── qa/pipeline.py
│   └── rag/                 #   loaders / splitter / store / retriever
├── backend/app/
│   ├── main.py              #   应用装配、CORS、health
│   ├── api/                 #   evaluation.py / syllabus.py / qa.py
│   ├── core/db.py           #   SQLite：评估任务 / 大纲任务 / 问答 / 大纲记录
│   └── workers/             #   tasks.py 视频评估；syllabus_tasks.py 大纲优化
├── frontend/src/
│   ├── api/client.js        #   axios 封装 + 统一错误提示
│   ├── api/stream.js        #   SSE 流式读取（fetch，axios 拿不到增量）
│   └── views/               #   Layout / Evaluation / Syllabus / QA
├── knowledge/corpora/       # 知识语料（放你的文档）
├── data/                    # 上传、关键帧、Chroma、SQLite（已 gitignore）
├── test/                    # 联调样例：大纲 PDF/Word 可入库；微格视频与打分表不入库
├── dataset/                 # 评估训练批次（manifest / csv / 蒸馏要点；cache 不入库）
└── scripts/                 # check_env / check_features / check-syllabus
                             # / smoke_test / qa_test / test_parsing
                             # / build_eval_dataset / test_eval_dataset
```

### 数据流

```
功能①  视频（可选：课程大纲、课件）→ ffmpeg 抽音轨 + 视觉双轨抽帧
            │    稀疏轨：均匀 12 帧 → 送 VLM（每帧一次调用）
            │    密集轨：每 3 秒灰度缩略帧 → 只做本地帧差（零 API 成本）
            │    若上传课件：渲染页面 → 另走 VLM 逐页标注（板书/课件设计以此为准）
            → faster-whisper 转写（自动繁转简）
            → 客观特征按来源分 7 组：
                 text       转写文本统计 + 分段汇总
                 audio      librosa 声学特征
                 timeline   提问等待时间、ASR 置信度
                 slides     课件切换、停留时长、讲授同步
                 vision     课堂关键帧 VLM 标签聚合成比例
                 courseware 上传课件的页面标注（选填）
                 speakers   说话人分离（可选，默认关闭）
            → LLM-as-Judge 按维度逐项打二级分，再由模型按课型综合出一级分
            → 五维合成总分 → 生成报告 → 摘要回流进向量库

功能②  文档 → PyMuPDF/pypdf 多后端解析
            → 固定框架：章节索引 → 原文切片 → 全局骨架 → 分批章节优化 → source_id 合并校验
              （灵活框架仍为单轮生成；中间结果异常时固定框架可降级为单轮）
            → lxml 结构/深度/业务校验，不合法则带报错回喂模型自修（最多 2 次）
            → 可导出 Markdown / Word / PDF（export.py）

功能③  提问 → LLM 生成检索关键词并选语料库
            → Chroma 多路检索、合并去重
            → LLM 结合检索结果生成带 [n] 角标的回答（SSE 流式）
```

### 几个关键设计决策

**事实层与判断层分离**。语速、提问次数、停顿次数、响度、基频这些能精确计算的量
由代码算好，作为证据喂给大模型；模型只负责在事实基础上做判断。避免让大模型
凭感觉估计本来可量化的指标。

**VLM 是观测员，不是评委**。VLM 每帧只输出固定字段的标签（视线看学生/屏幕/讲稿、
板书可读性高/中/低……），由本地聚合成「看讲稿帧占比 35%」这类比例，再交 Judge 打分。
若让 VLM 输出自由文本描述，视觉指标只能靠 Judge 读一遍留印象，本可量化的
「看稿读屏行为少」会退化成印象分。

**证据必须带来源和局限**。喂给 Judge 的每组特征都标明出处（「由 librosa 从音轨提取」
「本地帧差检测，不经过大模型」），弱代理量必须写清它弱在哪 —— 比如 ASR 置信度
混杂了录音质量与口音，课件切换次数在固定机位下只是上界。不标局限，模型会把
所有数字当成同等硬度的事实。

**课程大纲与课件都是选填，有和无走两条评分口径**。
有大纲时，「内容完整性」对照大纲中与本节课相关的安排来评；没有大纲时，
根据转写判断这节课自身是否形成知识闭环。有课件时，板书/课件的布局与可读性
以上传文件为准，课堂关键帧只用来看教态和学生状态；没有课件时，这些项改看
抽取的关键帧。课堂节奏（停留、切换同步）始终看视频帧差，不看课件文件。

**每个一级维度单独调一次 LLM**，而不是一次性打完 24 项。提示词更聚焦、输出更短，
JSON 解析失败率显著更低，也便于单维度重试。同一轮输出里，模型先打二级分，再给出
`dimension_score`：按这节课的课型（微格、纯讲授、有无学生出镜等）灵活折算一级分，
而不是对二级分做固定加权。一级分必须落在已评二级分的 min/max 附近（允许 ±5），
越界或缺字段时回退到 yaml 里的二级权重加权平均。

**模态感知打分**。完全依赖缺失模态的二级指标标记为「未评估」并排除在一级折算之外，
而不是硬给低分。否则关掉视觉分析会让「板书设计」拖垮整个维度。

**Provider 抽象层**。业务代码只依赖 `ai_engine/providers` 的接口，不关心背后是
云端还是本地。接新模型厂商 = 加一个子类 + 工厂里加一个分支。

**配置优先于代码**。指标体系、词表、XML 结构、语料库列表都在 YAML/XML 里，
调整这些不需要改代码，改完重启后端即可。

---

## 六、切换云端 / 本地大模型

**默认已是云端**，一般只需在 `.env` 填好 `DASHSCOPE_API_KEY`，无需改 mode。

| 能力 | 默认（cloud） | local（需显式开启） |
| --- | --- | --- |
| LLM | qwen3.7-plus（通义 API） | qwen2.5:3b（Ollama） |
| VLM（关键帧 / 课件页） | qwen3-vl-plus | qwen2.5vl:7b |
| Embedding | text-embedding-v3 | bge-m3 |
| ASR（语音识别） | faster-whisper（**固定本地，非大模型**） | 同左 |

显式切换方式（不推荐日常使用本地）：

```bash
# .env 中 PKU_MODE=cloud   ← 默认，大模型走通义千问
PKU_MODE=local make backend  # 仅当需要 Ollama 时
```

> 换 embedding 模型后向量维度会变，需要 `make ingest-reset` 重建向量库。

---

## 七、三个功能怎么用

### ① 教学视频质量评估

在页面左侧拖入视频，需要的话再选课程大纲和课件，点「开始评估」。
任务异步执行，前端每 2.5 秒轮询进度。
处理中或排队中的任务可点「停止」中途取消诊断（在 ASR、视觉分析、打分等
步骤的进度回调处协作式退出，短步骤如抽音频期间可能需稍等片刻）。

**课程大纲选填**（pdf / Word / txt / md）。有则对照大纲安排评本节课内容完整性；
没有则根据转写看这节课是否形成知识闭环。

**课件选填**（pdf / pptx / ppt）。有则以上传课件评版式与可读性；
没有则根据课堂关键帧判断。PPT/PPTX 优先用 LibreOffice 转成 PDF 再渲染页面，
转不成时 PPTX 会退回纯文本（版式只能弱判）。

**模态缺失的处理**：如果关掉视觉分析（或 VLM 不可用），依赖 `vision` 模态的
二级指标会被标记为「未评估」，在明细表里灰显，也不进雷达图。
但**课件切换检测走本地帧差，不依赖 VLM**，所以「板书停留充分」「切换与讲授同步」
在 `vlm_enabled: false` 时仍然可评。上传了课件时，课件页标注会点亮 `vision` 模态，
即使关键帧分析失败，「板书设计」仍可能可评。

**客观特征怎么看**：结果页的「客观特征（事实层）」按来源分 7 组，每组下面标了
出处（如「本地帧差检测，不经大模型」）。来源就是可信度：`text` / `audio` /
`timeline` / `slides` 是算出来的，`vision` / `courseware` 是 VLM 看出来再聚合的。
带括号说明的标签是弱代理量，比如「学生发言线索次数（词表粗估，偏高）」。

**关键帧下面的彩色标签**是 VLM 的逐帧结构化观测（视线、手势、可读性、抬头率），
绿色为正向、红色为负向。这些标签聚合后就是上面 `vision` 组的比例数字。
若上传了课件，结果页会多一组「上传课件页面观测」。

**想先不传视频跑通链路**：用左下角的「转写文本快速评估」，粘贴一段课堂文本，
跳过 ASR 与视觉直接验证打分链路，几十秒出结果（同样可粘贴课程大纲）。

**用专家打分表构造训练批次**（目前 2018 春微格已扫完 inventory，**尚未**批量 ASR）。
同一年内冻结 Judge prompt；评语只用于打完分之后的 `reflect` / `distill`，不进该课打分。
新经验只喂给后面的年份。训 GB 前用最终 prompt `rejudge`（只重打分，不重跑转写）。
本批约 22 条，只够打通流水线，不够单独训稳 GB。打分表含联系方式，**不要**把原始 xlsx
或带邮箱电话的文件推进公开远程；本仓库写出的 csv 不含邮箱/电话。

```bash
# 1. 扫描（已对 2018 跑过，产出 dataset/2018_spring/inventory.csv 与 manifest.csv）
python -m scripts.build_eval_dataset inventory \
  --root "test/2018春微格作业-32人" \
  --xlsx "test/2018春微格作业-32人/微格教学评审汇总-2018--汇总意见.xlsx" \
  --out dataset/2018_spring

# 2. 抽证据 + 当前 prompt 打分（ASR 很慢；先 --limit 2 冒烟）
python -m scripts.build_eval_dataset extract \
  --manifest dataset/2018_spring/manifest.csv --resume --limit 2 --prompt-version v0

# 3. 对照评语逐课写 lesson，再压成 5–8 条（人工看过再挂下一年度 Judge）
python -m scripts.build_eval_dataset reflect --dir dataset/2018_spring
python -m scripts.build_eval_dataset distill --dir dataset/2018_spring

# 4. 全部年份跑完、冻结最终 prompt 后，只重打分再 merge
python -m scripts.build_eval_dataset rejudge --dir dataset/2018_spring \
  --prompt-version vN --lessons dataset/2018_spring/lessons_distilled.md
python -m scripts.build_eval_dataset merge --dir dataset/2018_spring
```

纳入规则：文件夹名能匹配打分表姓名 **且** 有教学视频。无视频（`no_video`）或无专家分
（`no_score`）写入 inventory 但不进 manifest。默认仍扫描「未通过」子目录。
`extract` 永存 `cache/{id}/evidence.json`（转写与特征，体积小），默认删掉抽音和关键帧；
原始视频留在 `test/`。终端是 TTY 时，`asr` / `vlm_describe` / `llm_judge` 在同一行刷新进度条
（分钟数或帧数）；重定向到文件时按 10% 打一行，避免刷屏。`training_gb.csv` 不含评语文本。
`eval_judge.j2` 可注入已确认的短口径清单（`--lessons`），默认不自动改提示词文件。

校验匹配逻辑：`python -m scripts.test_eval_dataset`。

### ② 教学大纲优化

上传 PDF / Word / Markdown，或直接粘贴文本。提交后**立即返回任务 ID**，页面显示进度条并每 2.5 秒轮询；处理中可点**停止**（协作式取消）。完成后输出 XML 或 Markdown（取决于模式），页面上原文与结果左右对照，可复制或下载；校验通过后可**导出 Word / PDF**（XML 模式还可导出 Markdown；Markdown 模式可直接下载 `.md`）。

任务 API（与视频评估类似）：

```bash
# 上传文件 → 返回 task_id（固定 Markdown 框架）
curl -F "file=@test/syllabus-RL2025-Fall.pdf" \
  "http://127.0.0.1:8010/api/syllabus/optimize_file?prompt_mode=markdown_schema"

# 灵活 Markdown（保留原大纲结构）
curl -F "file=@test/syllabus-RL2025-Fall.pdf" \
  "http://127.0.0.1:8010/api/syllabus/optimize_file?prompt_mode=markdown"

# 查询进度
curl "http://127.0.0.1:8010/api/syllabus/task/{task_id}"

# 停止任务
curl -X POST "http://127.0.0.1:8010/api/syllabus/task/{task_id}/cancel"
```

**四种优化模式**（页面上可切换，用于对比效果）：

| 模式 | API `prompt_mode` | Prompt 文件 | 说明 |
| --- | --- | --- | --- |
| **灵活结构 · XML**（默认） | `adaptive` | `syllabus_optimize.j2` | 保留原大纲章节逻辑，XML 标签随原稿变化（根节点 `<course_syllabus>`） |
| **固定框架 · XML** | `schema` | `syllabus_optimize_schema.j2` | 映射到 `syllabus_schema.xml` **大纲级**结构（根节点 `<syllabus>`，章节用 `<points>`） |
| **灵活结构 · Markdown** | `markdown` | `syllabus_optimize_markdown.j2` | 保留原大纲结构，输出**大纲级** Markdown；篇幅不超过原文 2 倍 |
| **固定框架 · Markdown** | `markdown_schema` | `syllabus_optimize_markdown_schema.j2` | 映射到 `syllabus_markdown_schema.md`（大纲级框架），篇幅不超过原文 2 倍 |

默认模式由 `config.yaml` → `syllabus.prompt_template` 控制；API 可传 `prompt_mode` 覆盖。
送入 LLM 的原文上限由 `syllabus.max_input_chars` 控制（默认 80000 字）。
Markdown 模式输出字数上限为 `syllabus.markdown_max_length_ratio`（默认 2.0）× 原文字数。
固定框架 **XML** 与 **Markdown** 均已对齐为**大纲级**：章节用要点列表（XML 为 `<points><point>`），
不写 topic/activity 教案字段；篇幅不超过原文 2 倍（XML prompt 注入 `max_output_chars`）。

固定框架 XML 遵循“原文忠实性优先”，生成前会自动规范化 assessment/activity 的 type 同义词；
校验检查章节要点、学时/权重配平与基本结构，不再要求 80 字 explanation。

固定框架默认使用**单轮生成**（一次 LLM 调用，较快、不易超时）。若需更高章节忠实度，
可在 `config.yaml` → `syllabus` 改回分阶段模式：

- `llm_timeout: 600`：大纲优化专用 LLM 读超时（秒），固定框架生成长 XML 时需 5–10 分钟；
- `generation_strategy: single|staged`：单轮（默认）或分章流水线（慢，长大纲易超时）；
- `chapter_batch_size: 1`：staged 模式下每次优化的章节数；
- `max_staged_chapters: 30`：staged 模式下章节数上限；
- `staged_fallback_to_single: true`：staged 失败时退回单轮。

分阶段模式先让模型抽取章节索引，Python 按定位文本切片后再逐章优化；单轮模式则
一次性生成整份 XML。`origin/source_id` 属于内部元数据，导出 Markdown、Word、PDF
时不会显示。

### ③ 教学智能问答

回答上方会显示这次用了哪些关键词、查了哪些语料库，下方可展开引用来源。
检索效果不好时，看这两处就能判断是关键词生成的问题还是语料覆盖的问题。

---

## 八、加自己的知识语料

```bash
# 1. 把文档丢进对应目录（支持子目录）
knowledge/corpora/edu_theory/      # 教育学基础理论
knowledge/corpora/pku_salon/       # 北大教学沙龙
knowledge/corpora/course_syllabi/  # 课程大纲参考

# 2. 重建
make ingest
```

支持 pdf / docx / md / txt / html。`edu_theory/` 已按主题分子目录，ingest 会递归入库：

| 子目录 | 主题 |
| --- | --- |
| `01-学习科学/` | 学习机制与经典理论 |
| `02-课程与教学设计/` | 布鲁姆、OBE、UDL、AI redesign、Human-Effort/PROCESS 模板 |
| `03-课堂互动与教学法/` | 主动学习、提问、大班课、AI 脚手架与 roleplay |
| `04-评价与反馈/` | 形成性评价、Authentic assessment |
| `05-高等教育实践/` | Chickering 七项良好实践 |
| `06-生成式AI与大学教学/` | 政策、AIMES、备课工作流、SARPS、Co-Intelligence、实践案例 |
| `07-AI素养与能力框架/` | AI literacy、UNESCO 能力框架 |
| `08-AI教学整合模型/` | TPACK、SAMR、人机共同调节 |
| `09-AI时代的评价与诚信/` | 评价重构、AIAS、学术诚信、Better-than-AI rubric |
| `10-公平无障碍与数据治理/` | UDL×AI、学习分析伦理 |

**每篇语料均含「文献性质 / 核心出处 / 参考文献与可追溯来源」**，期刊论文标注 DOI，
网页类标注访问日期，以保证可核查性。新增语料后执行 `make ingest` 增量入库。

`course_syllabi/` 已收录 11 门公开 syllabus **原版 HTML**（MIT OCW、Stanford、Yale OYC、
CMU、Harvard CS50），按院校分子目录；目录与各课「参考价值」见
`knowledge/corpora/course_syllabi/README.md`。

仓库里现有的「种子-*.md」只是用来验证链路，放入真实资料后可以删掉。

**新增一个语料库**：在 `config.yaml` 的 `corpora` 下加一项，再建同名目录即可，
前端的勾选框和检索路由会自动带上。

### 教学沙龙：从 mp4 自动生成语料

```bash
# 1. 把录像放进 raw_video/，文件名前 8 位为日期 YYYYMMDD
#    例：20240315_大班课互动.mp4

# 2. 转写 + 提取教学知识（ASR 用 small，结构化默认走云端 LLM）
make salon
# 或分步：make salon-transcribe → make salon-structure

# 3. 写入向量库
python -m knowledge.ingest --corpus pku_salon
```

| 路径 | 说明 |
| --- | --- |
| `pku_salon/raw_video/` | 原始 mp4（**不入库**） |
| `pku_salon/.work/` | 转写中间产物 audio / transcript.json（**不入库**） |
| `pku_salon/YYYYMMDD-*.md` | 正式语料，问答检索用 |

配置在 `config.yaml` 的 `salon:` 段（`asr_model: small` 等）。不保留主讲人信息，
LLM 只提取与教学实践相关的要点，过滤寒暄和行政内容。

---

## 九、调整评估指标

指标体系有三份文件，职责不同，**改之前先分清要改哪一份**：

| 文件 | 是什么 | 谁读 |
| --- | --- | --- |
| `evaluation_criterion.md` | 需求源头：五维 38 条三级指标的人工定义 | 人 |
| `evaluation_design.md` | 每条三级指标由谁来算（本地 / VLM / LLM）、实现要点与**实现后仍存在的局限** | 人 |
| `ai_engine/pedagogy/evaluation_rubric.yaml` | 上面两份的机器可读版本 + 客观特征的标签 | 代码 |
| `ai_engine/pedagogy/feature_lexicon.yaml` | 本地统计用的词表与判分阈值 | 代码 |

改了 `evaluation_criterion.md` 就要同步 rubric，否则两份文档会各自演化。
`evaluation_design.md` 第五节记录了原先的四处不一致（已全部修正），以及
三级观测点已按指标文档对齐、不再自行扩写。

运行时配置全部在 `ai_engine/pedagogy/evaluation_rubric.yaml` 里，改完重启后端生效：

- 增删一级维度、二级指标
- 调整权重：二级 `weight` 只在模型没给出有效一级分时做加权平均兜底；
  五个一级维度的 `weight` 仍用于合成总分。`accuracy`（知识准确性）权重已降到 0.6，
  兜底时避免通用模型误报事实错误把整维打穿。正常路径的一级分由 Judge 按课型综合，
  不受这组固定权重约束
- 改每个指标的观测点描述（直接影响大模型的打分依据）
- 标注每个指标依赖哪些模态（`audio` / `text` / `vision`）
- `requires_reference: true` 可声明某指标必须有外部参照才评分（目前没有指标启用）
- `objective_features` 分 7 组（`text` / `audio` / `timeline` / `vision` /
  `slides` / `courseware` / `speakers`），给每个客观特征配中文标签、单位和理想区间。
  **代码里新算了特征但没在这里登记，它就不会进证据表也不会显示在前端** ——
  `make check-features` 会检查这一点

文本特征的统计词表和判分阈值在 `feature_lexicon.yaml`，都可以按你的学科习惯调整：

| 配置块 | 内容 |
| --- | --- |
| `question_markers` / `open_question_markers` | 什么话算「提问」、什么算「开放性问题」 |
| `bloom_higher_markers` / `bloom_lower_markers` | 认知层级分类，算高阶问题占比。两表都没命中的提问计为「未分类」，不进比例的分母 |
| `case_markers` / `recency_markers` | 案例引入、前沿性表述 |
| `discipline_markers` | 纪律提醒与点名（已从 `interaction_markers` 拆出，两边不重复计数） |
| `inspire_markers` / `transition_markers` / `filler_markers` | 启发话语、过渡衔接、口头禅 |
| `audio_thresholds` | 长停顿秒数、理想语速区间、信噪比门槛 |
| `timeline_thresholds` | 有效等待时间（默认 3 秒）、等待时间截断上限、ASR 低置信门槛 |
| `slide_thresholds` | 页面停留下限（默认 20 秒）、切换同步的时间窗（默认 ±10 秒） |

改完跑一次 `make check-features` 确认没把结构改坏（不花 API 额度）。

提示词模板在 `ai_engine/pedagogy/prompts/`，是 Jinja2 文件。改 `eval_vision.j2`
时注意：VLM 的输出字段必须和 `vision.py` 的 `LABEL_SCHEMA` 对得上，
否则解析后全部归为 `unclear`。

### 视觉与说话人的开关

`config.yaml` → `evaluation`：

| 配置项 | 默认 | 说明 |
| --- | --- | --- |
| `vlm_enabled` | `true` | 关掉则跳过 VLM 逐帧标注 |
| `keyframe_count` | `12` | 稀疏轨：送 VLM 的帧数，**每帧一次 API 调用** |
| `slide_detection_enabled` | `true` | 关掉则跳过课件切换检测 |
| `slide_sample_interval_sec` | `3.0` | 密集轨抽帧间隔，只做本地帧差，零 API 成本 |
| `slide_change_threshold` | `0.08` | 相邻帧平均灰度差超此值判为切换（0~1）。调大 = 少报切换 |
| `courseware_max_pages` | `16` | 教师上传的课件最多渲染多少页送 VLM，超出则均匀抽样 |
| `diarization_enabled` | `false` | 说话人分离，见下 |

**说话人分离默认关闭**，开启需要三步：

```bash
make install-local                      # 装 pyannote.audio
# 在 https://huggingface.co/pyannote/speaker-diarization-3.1 接受使用条款
# 在 .env 里填 HF_TOKEN=hf_xxx
# 在 config.yaml 里把 evaluation.diarization_enabled 改成 true
```

代价是 CPU 上 45 分钟音频约需 10–20 分钟，会明显拉长流水线。收益是「学生发言
次数」从词表粗估（**系统性偏高**，因为教师说「我觉得」比学生更多）变成真实的
发言轮次与时长占比，「教学效果」维度才有可信依据。任何一步没配好都只会在
进度里记一条 warning，不会让评估失败。

---

## 十、排错

| 现象 | 原因与处理 |
| --- | --- |
| `No module named 'ctranslate2'` / 装 faster-whisper 失败 | Python 版本太新。必须用 3.11：`conda create -n pku2 python=3.11` |
| `缺少 API Key：请在 .env 中设置 DASHSCOPE_API_KEY` | `cp .env.example .env` 后填 key；确认 `.env` 中 `PKU_MODE=cloud` |
| `未找到 ffmpeg` | `brew install ffmpeg` |
| `Ollama 调用失败` | 确认 `ollama serve` 在跑，且已 `ollama pull qwen2.5:3b` |
| 上传视频后卡在「语音识别」很久 | 首次运行要下载 whisper 权重；且 CPU 转写约为实时的 1/3～1/5。先用几分钟的短视频试 |
| 转写结果是繁体 | 已内置 zhconv 自动转简体。若没转，确认装了 `zhconv` |
| 评估结果里很多指标显示「未评估」 | 对应模态没数据。视觉指标需要 VLM 可用（云端要 key，本地要 `ollama pull qwen2.5vl:7b`） |
| 关键帧下面没有彩色标签，只有一句话 | VLM 没按 JSON 格式回，标签全部归为 `unclear`。本地模型（qwen2.5vl:7b）比云端更容易跑偏，可换云端或看 `frame.description` 里的报错 |
| 客观特征里没有「课件时序特征」这一组 | `slide_detection_enabled` 被关了，或 ffmpeg 解码失败（进度详情里有 warning）。密集抽帧要求视频有可解码的视频流，纯音频文件会失败 |
| 课件切换次数明显偏多 | 固定机位下教师走动也会造成画面差异，切换数是**上界**。把 `slide_change_threshold` 从 0.08 往上调（如 0.15）会更保守 |
| 选了视频但没有开始评估 | 上传入口改为先选文件再点「开始评估」，以便同时附上大纲/课件。选完视频后要点按钮 |
| PPT/PPTX 课件没有页面图像 | 本机没有 LibreOffice，无法把幻灯片转成 PDF。请另存为 PDF 再传，或 `brew install --cask libreoffice` |
| 上传大纲后任务直接失败 | 扫描版 PDF 抽不出文字。请改传 Word，或先做 OCR |
| 客观特征里没有「上传课件观测」这一组 | 没传课件，或 VLM 对课件页全部标注失败（进度详情里有 warning） |
| 说话人分离报「需要 HuggingFace token」 | `.env` 里没填 `HF_TOKEN`，或没在模型页面接受使用条款。两者都要做 |
| 说话人分离报「未安装 pyannote.audio」 | `make install-local` |
| 新加的客观特征前端看不到 | 忘了在 `evaluation_rubric.yaml` 的 `objective_features` 里登记标签。跑 `make check-features` 会指出缺哪个 key |
| `make check-features` 报「无未登记的特征 key」失败 | 同上，按提示把 key 加到 rubric 对应分组里 |
| 问答检索不到内容 / 语料库计数为 0 | 没建库。`make ingest`，并确认语料目录里确实有文档 |
| `dimension mismatch` 之类的 Chroma 报错 | 换过 embedding 模型。`make ingest-reset` 重建 |
| 前端起来了但数据全空 | 后端没启动或端口不是 8010。检查 `make backend`，代理配置在 `frontend/vite.config.js` |
| 端口被占用 | `lsof -ti :8010 \| xargs kill -9` |
| 扫描版 PDF 解析为空 | 目前不带 OCR。先用其他工具转成文字版 |
| 中文 PDF「原始大纲」乱码 | 已用 PyMuPDF 多后端解析；仍失败则改传 docx 或粘贴文本 |
| 大纲 PDF 导出失败 | 需安装 `pandoc` 或 LibreOffice：`brew install pandoc` 或 `brew install --cask libreoffice` |
| 旧版 `.doc` 无法解析 | macOS 会尝试用 textutil；失败的话在 Word 里另存为 .docx |
| 大纲校验失败但未自动修复 | 自修采用**黑名单制**：除 `source_id 覆盖或顺序错误` 等少数项外，默认会自修（最多 2 次）。看进度是否出现「自动修复」及 `repair_attempts` 标签 |
| 大纲校验「章节学时合计与总学时不一致」 | 重启后端后应触发自修；若 2 次仍失败，可能是原文学时数据不完整，模型无法可靠配平 |
| 大纲固定框架 XML 报 `activity type 不在允许枚举中` | 模型用了「案例教学」「研讨」等；校验前会自动映射为标准 type，无法识别则写「其他」。**重启后端**后重试 |
| 大纲固定框架 XML 报 `assessment/item type 不在允许枚举中` | 模型用了「期末考试」「平时成绩」等同义词；已自动映射为标准 type。**重启后端**后重试；仍失败可看报错里的「当前为 …」对照允许列表 |
| 大纲上传 Word/PDF 后报 `KeyError: 'source_text'` | 异步 worker 未读到 `source_path`（已在 2026-08-18 修复）。**重启后端**后再试；仍失败则确认 `data/` 下上传文件存在 |
| 运行大纲校验测试时报 `No module named 'lxml'` | 使用了系统 Python。先执行 `conda activate pku2`，再运行 `make check-syllabus` |

---

## 十一、待解决的问题

**当前聚焦**：功能② 大纲优化——固定框架的结构、内容深度和业务校验已完成第一轮；
**下一步优先**做分章生成、原文覆盖率检查和导出版式。功能③智能问答继续迭代。
功能①视频评估已按 `evaluation_criterion.md` 完成指标落点梳理并实施完
`evaluation_design.md` 第六节的六个阶段（客观特征从 5 项扩到 44 项，视觉指标
从自由文本改为结构化标签聚合）。剩余缺口见文末「暂缓项」。

解决一项就从对应分类里删掉，并在第十二章变更记录里写清楚怎么解的。

---

### 功能③ 教学智能问答

#### A. 语料与建库

| 问题 | 影响 | 优化方向 |
| --- | --- | --- |
| **沙龙语料需从 mp4 生成** | 脚本已就绪（`make salon`），但需用户放入真实录像；种子 md 可删 | 视频放 `raw_video/` → `make salon` → `ingest --corpus pku_salon` |
| **建库需手动触发** | 新增/更新文档后容易忘记 ingest，检索结果过时 | 加 `ingest --watch` 或上传文档后自动增量入库 |
| **噪声文档进库** | `course_syllabi/` 里的 `README.md` 会被切块检索，干扰问答 | ingest 时排除 README/说明类文件，或按 glob 白名单入库 |
| **换 embedding 需全量重建** | 切换云端/本地 embedding 后维度不一致，Chroma 报错 | 已在 store 里做了维度冲突提示；文档化「换模型必跑 `make ingest-reset`」流程 |

#### B. 检索链路

| 问题 | 影响 | 优化方向 |
| --- | --- | --- |
| **无重排序** | `config.yaml` 里 rerank 为 `none`，只靠向量 cosine 分数，精排能力弱 | 云端接 DashScope/Cohere rerank，或本地 `CrossEncoderRerank` |
| **纯向量检索** | 专有名词、课程代码、人名等字面匹配弱的场景召回差 | 加 BM25 或关键词检索，与向量做 hybrid merge |
| **分块策略未调优** | 固定 500 字 + 80 overlap，沙龙记录/理论长段落可能被拦腰切断 | 按语料类型配置 chunk_size；或按 Markdown 标题层级切 |
| **去重键过粗** | 用文本前 120 字去重，不同段落开头相似时会误合并 | 改用 chunk id / 来源+偏移；或 MMR 多样性采样 |
| **召回量无全局上限** | ~~多 query 合并后条数膨胀~~ | **已设 `max_hits=12`**；仍受 6000 字上下文上限约束 |
| **无相似度阈值** | ~~低分片段仍喂给模型~~ | **已设 `score_threshold=0.5`**；零命中时不引用、走 LLM 通用知识 |
| **上下文上限偏小** | `max_context_chars=6000`，多库多 facets 问题信息不够 | 提高到 8k–12k，或做 Map-Reduce 式分库摘要再合成 |

#### C. 检索规划（Query Planner）

| 问题 | 影响 | 优化方向 |
| --- | --- | --- |
| **规划失败静默降级** | LLM 输出非 JSON 时走 fallback（原问题 + 全库），界面只显示 `planner=fallback`，用户不知规划失败 | fallback 时在 UI 显式提示；记录日志便于调 prompt |
| **小模型格式不稳定** | 本地 qwen2.5:3b 偶发不按 JSON 输出，规划命中率低于云端 | 默认云端做规划；或加 JSON mode / 更小更专的规划 prompt |
| **多轮指代能力有限** | 只带最近 6 轮历史，复杂追问（「刚才第三点展开说说」）容易丢上下文 | 加摘要记忆或单独做指代消解一步 |
| **语料库勾选** | 用户勾选仅限定检索范围；queries 仍由 LLM 生成 | 勾选时可选跳过规划、直接用原问题检索 |
| **闲聊与系统问答未分流** | `need_retrieval=false` 时仍走同一套 answer prompt，没有专门的系统说明模板 | 规划为 false 时走轻量 system FAQ，避免空检索仍拼长 prompt |

> **2026-08-06 已做**：取消 LLM 语料库路由；非手动勾选时始终全库检索，由相似度阈值决定是否引用。

#### D. 回答生成与可信度

| 问题 | 影响 | 优化方向 |
| --- | --- | --- |
| **引用未校验** | 模型生成的 `[1][2]` 角标可能与检索片段不对应，存在「看起来有引用、实际张冠李戴」 | 生成后做 citation grounding 校验，或约束「每句引用必须含片段关键词」 |
| **弱检索仍强作答** | ~~零命中与弱命中混淆~~ | **已分档**：≥0.5 才引用；零命中禁止 `[n]`，明示通用建议 |
| **无质量反馈闭环** | 无法标记幻觉、无用引用、答非所问 | 前端加 👍/👎 或「引用有误」，落库供后续调 prompt / 调 chunk |

#### E. 前端与产品体验

| 问题 | 影响 | 优化方向 |
| --- | --- | --- |
| **会话管理简陋** | 只有列表 + 删除，无搜索、重命名、导出 Markdown | 补会话标题编辑、全文导出 |
| **引用展示过短** | snippet 固定 200 字，难以判断是否值得点开 | 可展开全文；高亮与回答句子的匹配片段 |
| **无「换检索再答」** | 关键词或语料库选错时只能重新提问 | 加「编辑关键词 / 换库重试」按钮，复用同一会话 |
| **无鉴权** | 所有会话、语料库状态对局域网内任何人可见 | 最简登录 + 会话按用户隔离（与全局暂缓项联动） |

---

### 功能② 教学大纲优化

> **当前聚焦（2026-08-15 更新）**
>
> | 问题 | 现象 | 优化方向 |
> | --- | --- | --- |
> | **灵活模式 XML 仍不规范** | 固定框架已加自定义结构、枚举、深度和配平校验；灵活模式因标签随原稿变化，目前仍只做 well-formed 校验 | 为灵活模式定义最小公共约束；分步生成降低单次出错率 |
> | **导出 MD/Word/PDF 不美观** | `export.py` 仅做 XML 树→标题映射，无版式；Word 字体/间距简陋；PDF 依赖 pandoc 默认样式；与教师 familiar 的大纲版式差距大 | 按大纲类型做 Word 模板；Markdown 层级与表格还原；HTML 中间层 + 样式；关键节点（考核表、章节）专用渲染 |
> | **章节内仍可能语义漏项** | 固定框架已按原文切片分批优化，并用 `source_id` 保证章节数量和顺序；但目前不能证明章节内每个知识点都被模型保留 | 为原文知识点分配细粒度 source ID；做关键词/语义覆盖检查；按需接入 Teaching with AI 语料 |

#### A. 文档解析

| 问题 | 影响 | 优化方向 |
| --- | --- | --- |
| **扫描版 PDF 无 OCR** | 图片型 PDF 解析为空，直接报错 | 接 PaddleOCR / Tesseract，或引导用户先 OCR |
| **`.doc` 跨平台差** | 仅 macOS `textutil` 兜底，Linux/Windows 易失败 | 统一推荐 docx；或接 LibreOffice headless 转换 |
| **超长文档截断** | `max_input_chars=80000`，极长大纲尾部仍可能被截掉 | 分章解析后逐章优化再合并；或先结构化提取目录再分段送模 |
| **复杂版式丢失** | 多栏 PDF、合并单元格 Word 表格，纯文本抽取顺序混乱 | 按大纲常见模板做专用 parser（章节标题正则 + 表格还原） |

#### B. 生成策略

| 问题 | 影响 | 优化方向 |
| --- | --- | --- |
| **分阶段请求耗时增加** | 分阶段需多次 LLM 调用，同步 HTTP 请求内易超过前端 10 分钟超时；已改回默认单轮 | 需要时再开 `generation_strategy: staged`；或改异步任务并展示进度 |
| **无人工反馈回路** | 用户看完结果无法说「第 3 章学时改一下」 | 支持选中章节/regenerate + 自然语言修订指令 |
| **未利用参考语料库** | `course_syllabi` 已建向量库，但 optimizer 未做 RAG | 同类课程检索 2–3 份参考大纲，作为 few-shot 或约束 |
| **新增内容仍需人工复核** | 固定框架已禁止无依据补全，并用 `origin` 与 `<needs_confirmation>` 区分来源；但来源标记仍由模型自述 | 程序比对原文覆盖率和新增事实；前端按来源高亮 |

#### C. 校验与质量

| 问题 | 影响 | 优化方向 |
| --- | --- | --- |
| **灵活模式仅语法校验** | 固定框架已有自定义规则；灵活模式的动态标签仍只能保证 well-formed | 为两种模式提取共同的课程事实与业务规则，再做统一校验 |
| **细粒度内容覆盖率未程序检查** | `source_id` 已保证整章不漏和顺序不乱，但不能证明章内每个知识点都被保留 | 抽取 topic/知识点 source ID，合并后逐项检查并提示缺失 |
| **修复次数有限** | XML 语法错误最多 auto-repair 2 次，复杂错误仍失败 | 分块生成降低单次 XML 长度；或 syntax repair 与 content repair 分开 |
| **改动说明不可信** | `<improvements>` 由模型自述，可能与实际 diff 不一致 | 程序对比原文与 XML 生成结构化 diff，improvements 由规则+模型补充 |

#### D. 前端与交付

| 问题 | 影响 | 优化方向 |
| --- | --- | --- |
| **同步阻塞请求** | 大纲优化已改为异步任务 + 进度轮询，与视频评估一致 | 可选 WebSocket；长时间任务支持邮件/通知 |
| **无可读预览** | 非技术用户看不懂 XML 标签 | 按 schema 渲染为表单/大纲树形视图；或默认展示 Markdown 预览 |
| **对比无 diff 高亮** | 左右对照需人工找改动 | 章节级 diff 高亮；improvements 与 diff 联动跳转 |
| **历史无版本对比** | 只能打开单条记录，无法看两次优化差异 | 同一课程多次优化做 version diff |

---

### 暂缓项（视频评估 / 全局）

以下不影响当前问答、大纲优化迭代，需要时再排期。

下表的视频评估各项已在 `evaluation_design.md` 里逐条展开（含做法、成本与实施顺序），
这里只留索引。

| 分类 | 问题 | 备注 |
| --- | --- | --- |
| 视频评估 | 一级维度分由 LLM 按课型折算，同一视频两次跑可能差几分 | 越界会回退加权平均；要可复现可看 `weighted_score` 字段 |
| 视频评估 | 说话人分离已接入但**未在真实课堂验证过**（缺 HF token，默认关闭） | 剩余 4 条 ❌ 指标里唯一有解的一条，验证后「教学效果」维度才可信 |
| 视频评估 | 课件切换次数是**上界**：固定机位下教师走动也算差异 | 解法是让 VLM 在第一帧框出投影区域，密集轨只比对该区域 |
| 视频评估 | 「详略结合」缺客观依据 | 可加术语时间轴驻留特征（某术语首次到末次出现跨多少分钟、占多少字） |
| 视频评估 | 提问等待时间的有效样本常只有个位数（受 ASR 片段边界限制） | 开 `word_timestamps=True` 可解，代价是转写慢 20–30% |
| 视频评估 | 「表情自然」「板书重点是否突出」未纳入 VLM 标注 | 前者受关键帧分辨率限制，后者需理解板书语义 |
| 视频评估 | ASR 置信度是弱代理：混杂录音质量与口音，**换 whisper 模型后历史数据不可比** | 已在提示词里标明局限，无更好的本地替代 |
| 视频评估 | CPU 转写慢、长视频证据截断 | 暂缓，不阻塞问答/大纲 |
| 视频评估 | 评估报告回流未去重 | 同上 |
| 全局 | 无鉴权 | 问答会话、大纲历史、评估任务均受影响 |
| 全局 | Evaluation 页 bundle 过大 | 与当前聚焦无关 |

---

## 十二、变更记录

倒序排列，最新在最上面。每条写清楚**为什么这么改**。

### 2026-08-19 · 开始本地 git

**问题**：项目一直没有版本库，改动只靠 README 变更记录；再拖下去微格视频、
模型权重和 `.env` 更容易被误加进去。
**思路**：只做本地仓库、不配远程。ignore 微格目录（视频 + 含联系方式的 xlsx）、
所有音视频/表格后缀、`.env`、`models/`、`dataset/**/cache/`、沙龙 `raw_video/`。
补一份不含 Key 的 `.env.example`。原先待解决问题里「example 带真实 Key」随之关掉。
**影响**：`.gitignore`、`.env.example`、`data/.gitkeep`、`models/.gitkeep`。
`git init` 后第一次提交是 2.0 基线，不推送。

### 2026-08-19 · extract 日志改成进度条

**问题**：ASR 每个片段、VLM 每帧都 `print` 一行，`extract` 一条 20 分钟课会刷出
上百行 ` [15%] asr done_sec=...`，终端里看不清当前卡在哪一步。
**思路**：长步骤（`asr` / `vlm_describe` / `llm_judge`）TTY 上用 `\r` 刷新一条
`[████░░░░] 40%  8/20 分钟`；步骤切换或 warning 再换行。管道/日志文件里按 10%
节流，避免把重定向文件写成几万行。
**影响**：`scripts/eval_dataset/progress.py`；`build_eval_dataset` 的 extract/rejudge
和 `smoke_test` 共用。沙龙转写 `process_salon.py` 同步成同款条。前端轮询进度不变。

### 2026-08-19 · 微格评估数据集构造 CLI

**问题**：有 2018 春微格视频、大纲/课件和专家均分+评语，但没有可复用的扫描和
批量评估脚本；评语也没有进入任何对齐流程。
**思路**：`build_eval_dataset` 按年批次工作。inventory 用文件夹名匹配打分表、
按后缀判定材料；extract 把 ASR/VLM 证据与 Judge 分数分开存盘，用完即删中间媒体。
评语在 reflect/distill 里蒸馏成短口径，只喂给后续年份，不进该课打分、不当 GB 特征。
最终用同一 prompt 版本 rejudge 再 merge。2018 本批约 22 条，不够单独训 GB。
**影响**：`scripts/build_eval_dataset.py`、`scripts/eval_dataset/`、`pipeline.py`
拆出 `collect_video_evidence` / `score_from_evidence`、`eval_reflect.j2` /
`eval_distill.j2`、Judge 可注入 `expert_lessons`。已写出
`dataset/2018_spring/{inventory,manifest}.csv`。extract 需本机长时间跑 ASR，未在此次执行。

### 2026-08-19 · 撤回教学效果的氛围校准

**问题**：上一轮为抬高「教学效果」一级分，加了氛围独立高分、一级分贴氛围、
报告不把互动少当主要问题、以及兜底权重倾斜。这等于改了该维的评价标准，
和指标文档里四项并列、以及「发言次数 / 回答语气」的观测点不再一致。
**思路**：整轮撤回。教学效果仍只靠 Judge 按课型综合二级分（min/max ±5），
二级权重恢复等权；不在代码里按氛围抬分。
**影响**：`judge.py`、`eval_judge.j2`、`eval_report.j2`、`evaluation_rubric.yaml`、
`Evaluation.vue`、`test_parsing.py`。重启后端生效。

### 2026-08-19 · 教学效果：氛围好、互动少也可以得高分

**问题**：高校讲授课和微格录像口头互动本来就少。「学生参与度」「互动质量」
按发言次数如实偏低后，模型仍习惯把四项平均，教学效果整维普遍偏低；报告
还把「互动少」写成主要问题。安静有序的课被当成失败课。
**思路**：二级分口径不变（次数少就是少）。氛围独立评分：安静有序可以 80+，
禁止用发言次数反推氛围差。一级分加硬规则——氛围比次数类平均分高 10 分以上时，
整维不得低于氛围分 −5；提示词要求模型主动贴近氛围，代码在模型仍取平均时抬上去。
报告侧：一级分已达良好时，把增加提问写成建议而不是主要缺陷。兜底权重改为
氛围 2.0、参与/互动 0.6。
**影响**：已整轮撤回，见上一条。勿按本条改代码。

### 2026-08-19 · 云端默认模型改为 Qwen3.7 / Qwen3-VL

**问题**：评估 Judge、报告、问答、大纲优化仍走 `qwen-plus`，视觉走 `qwen-vl-max`，
与百炼上当前主力模型不一致，JSON 打分和关键帧理解都偏旧。
**思路**：不拆评估专用模型配置，全局 LLM 与 VLM 一起换。文本能力（Judge、报告、
问答、大纲、沙龙结构化）统一 `qwen3.7-plus`；关键帧和课件页统一 `qwen3-vl-plus`。
Embedding / ASR 不变。换模型后新旧评估分数不可直接对比。
**影响**：`config.yaml` 的 `llm.cloud.model`、`vlm.cloud.model`；README 云端/本地对照表。
重启后端生效。若百炼返回模型不存在，到控制台核对模型 ID 是否已开通。

### 2026-08-19 · 一级维度分改为 LLM 按课型折算

**问题**：五维一级分原先是二级指标的固定加权平均。微格课几乎没有学生出镜时，
「学生参与」类低分会把教学效果整维拖垮，和教研员看课的综合判断不一致。
**思路**：同一轮 Judge 先打二级分，再输出 `dimension_score` / `dimension_rationale`。
模型按课型决定哪些二级更关键，但分数必须落在已评二级分的 min/max ±5 以内，
防止为了好看而另打一套。缺字段或越界时回退加权平均，前端标「等权兜底」。
**影响**：`eval_judge.j2`、`judge.py`、`eval_report.j2`、`Evaluation.vue`、
`test_parsing.py`、`evaluation_rubric.yaml` 注释。结果新增 `score_source`、
`weighted_score`、`dimension_rationale`。五维合成总分仍用一级维度 weight。

### 2026-08-19 · 大纲校验脚本从 test/ 挪到 scripts/

**问题**：`test/` 里混着联调样例（大纲 PDF、微格视频）和 Python 测试脚本，
打开目录时分不清哪些是数据、哪些是要跑的代码。

**思路**：`test/` 只放样例。有用的 `test_syllabus_validation.py` 挪到 `scripts/`，
与 `check_features` / `test_parsing` 同类；补 `make check-syllabus`。

**影响**：`scripts/test_syllabus_validation.py`、Makefile、README 命令与排错表。

### 2026-08-19 · 评估支持选填课程大纲和课件，评分口径随有无材料切换

**问题**：教师无法把真正的课程大纲和课件交给模型。之前只有一个粘贴框，
而且提示词写死「不要用整门课大纲覆盖面打分」，有大纲也用不上；板书/课件
设计只能看教室录像截帧，机位和对焦经常让可读性被误判。

**思路**：上传页增加两个选填入口。有大纲就对照大纲中与本节相关的安排评
内容完整性，没有大纲才退回「转写是否闭环」。有课件就把课件文件当作版式
与可读性的权威证据（VLM 逐页标注），关键帧只评教态和学生状态；没有课件
才根据抽取帧判断。课堂节奏（停留、切换同步）始终看视频帧差。PPT/PPTX
优先经 LibreOffice 转 PDF 再渲染，转不成时 PPTX 退回纯文本。

**影响**：`materials.py`、`eval_courseware.j2`、`eval_judge.j2`、`pipeline.py`、
`vision.py`、上传 API 与 `eval_tasks` 新列、Evaluation 页。`make check-features`
增加大纲/课件分支断言。

### 2026-08-19 · 「内容完整性」改为按本节课闭环评分，不再强制大纲参照

**问题**：缺知识点清单时「内容完整性」被标为未评估。实际要看的不是整门课
大纲覆盖了多少，而是**这节课自己有没有讲完、有没有收束**。这件事转写里就能看，
不该因为没贴大纲就空着。

**思路**：去掉 `completeness.requires_reference`。三级观测点改为
「本节课内容完整闭环」。Judge 提示词写明：根据转写判断引入—展开—收束，
不要用整门课覆盖面打分；外部清单有则当辅助，没有也照常评。

**影响**：`evaluation_criterion.md`、`evaluation_rubric.yaml`、`eval_judge.j2`、
前端上传提示、API 字段说明。`requires_reference` 机制仍留在 `judge.py`，
目前没有任何指标启用。

### 2026-08-19 · 修复 Markdown 模式三项测试失败

**问题**：`MarkdownModeTests` 有 3 个失败，测试与实现各有一处对不上。
真正的实现 bug 是 `_strip_markdown_wrapper`：本意是砍掉模型在标题前的废话，
却用「第一个不在开头的 `# ` / `## `」当切点。文档合法地以 `# 课程名` 开头、
后面有 `## 章节` 时，一级标题被切掉，课程名变成了第二节标题。
另外两处是测试本身：11 字无标题文本会先命中「内容过短」，到不了标题检查；
原文 260 字时输出上限落到代码里的 800 字下限，测不到「不超过原文 2 倍」。

**思路**：剥离函数改为「已经以标题开头就不再切；只有标题前有废话时才从第一个
标题起算」。标题测试补一条足够长的无标题正文；篇幅测试把原文加长到 2 倍超过
800，走真正的倍率路径。

**影响**：`optimizer.py` 的 `_strip_markdown_wrapper`；`test_syllabus_validation.py`。
25 项大纲校验测试全部通过。

### 2026-08-19 · rubric 三级观测点改回以 evaluation_criterion.md 为准

**问题**：rubric 在指标文档之外自行扩写了若干三级观测点（「课堂秩序良好」
「章节之间有明确的承接关系」「显性呈现思考路径」等）。两份文档各自演化，
Judge 实际按扩写打分，需求源头却看不到这些条目。

**思路**：指标文档是需求源头。扩写即使合理，也必须先写进
`evaluation_criterion.md` 再进 rubric，不能只改机器可读的那份。
删掉所有文档里没有的观测点，留下的条目改回原文措辞。
`思维引导` 和 `教学资源融合` 在文档里只有二级、没有三级，不编造观测点，
按二级名称本身评分。

**影响**：`evaluation_rubric.yaml` 的 `criteria` 全部对齐指标文档；
若干二级指标的 `modalities` 随剩余观测点收窄（如课堂管理不再依赖 vision）。
`make check-features` 新增集合比对：rubric 每条 criterion 必须能在指标文档的
条目列表里找到。

### 2026-08-19 · 实施 evaluation_design.md 六阶段，客观特征 5 项 → 44 项

**问题**：设计文档指出了两类系统性问题，这次全部动手改。一是**本可精确计算的指标
被丢给 LLM 凭印象打分**：提问等待时间、课件停留时长完全没做，语速稳定性只差一步
汇总。二是**VLM 输出自由文本**，7 条视觉指标拿到的是 12 段散文，聚合不出任何比例，
视觉维度整体是印象分。另有三条更根本的：「知识点覆盖完整」没有参照物、
「无知识性错误」与其他指标同权、「学生发言次数」的词表口径系统性偏高。

**思路**：核心是**把「缺证据」和「有证据」明确分开，而不是让模型在缺证据时假装有**。

- **VLM 从评委改回观测员**。`eval_vision.j2` 改为输出 9 个固定字段的 JSON，
  `vision.py` 的 `LABEL_SCHEMA` 校验取值后聚合成 15 项比例型特征。三个防假数据的
  设计：`unclear` 留在分母并单独上报占比（悄悄剔除看不清的帧会让「看学生占比」
  虚高）；表外取值（模型偶尔直接答中文）归为 `unclear` 而不是静默进分母；
  单帧失败不影响其余帧。
- **视觉拆成两条轨**，因为成本结构完全不同：稀疏轨 12 帧送 VLM（每帧一次 API 调用），
  密集轨每 3 秒抽 160×90 灰度帧只做本地帧差（一次 ffmpeg 调用走管道进 numpy，
  不落盘，零 API 成本）。密集轨也点亮 `vision` 模态，所以关掉 VLM 时
  「板书停留」「切换同步」仍可评。
- **缺参照物就标未评估**。`completeness` 加 `requires_reference: true`，
  `judge.py` 的跳过机制从「只按模态缺失触发」扩展成「按原因触发」。
  宁可显示未评估，也不给一个看起来有依据的假分数。
- **弱代理量必须自己承认弱**。ASR 置信度混杂录音质量与口音、课件切换次数在固定
  机位下只是上界、学生发言次数是词表粗估 —— 这三条都写进了提示词和前端标签。
  不标局限，模型会把所有数字当成同等硬度的事实。
- **`accuracy` 权重 1.0 → 0.6**。实测该项被打 0 分时「教学内容」得 73.2 分，
  同权则会掉到 68.3 分。通用模型的学科事实核查既会漏报也会误报，
  一次误判不该拉动整个维度。同时提示词要求逐条引用原文，并提醒
  「转写可能有同音字误识，不要把 ASR 错误当成教师讲错」。

**影响**：

- `build_evidence()` 签名改了：`(transcript, duration, features: dict[str, dict],
  vision_notes, reference)`。`features` 的键与 rubric 的 `objective_features` 分组
  一一对应，加一组特征 = rubric 加一段 + 往 `features` 塞一个键。
- `objective_features` / `raw_features` 从 2 组扩到 6 组（text / audio / timeline /
  vision / slides / speakers），前端按组渲染并标注来源。
- 新增 `timeline_features.py`、`slide_features.py`、`diarization.py`。
  `ASRSegment` 多了 `avg_logprob` / `no_speech_prob` 两个字段。
- `keyframes[].labels` 新增结构化标签，`description` 保留为渲染后的中文串，
  前端改动是加法而非替换。
- `eval_tasks` 表加 `reference` 列。`CREATE TABLE IF NOT EXISTS` 不会给已存在的表
  补列，所以 `init_db()` 里加了 `ALTER TABLE` 迁移，幂等可重复执行。
- rubric 对齐了三处：「语**速**积极」笔误改「语调」（否则 Judge 会拿语速数据评语调）、
  「教学资源整合」统一为「融合」、「高阶问题比例」从「学科前沿融入」移到
  「重点难点设计」（认知层级属内容深度，与学科前沿是两件事）。
- 说话人分离**默认关闭**：需要 HF token + 接受模型条款，CPU 上 45 分钟音频要
  10–20 分钟。任何一步没配好只记 warning 不中断评估。
- 新增 `make check-features`：70 项断言，不调大模型不花额度。它还会校验
  「代码算出的每个 key 都在 rubric 里登记了标签」，防止新增特征忘记登记后
  静默不进证据表。
- 密集抽帧改成**流式** yield（`iter_gray_frames`），单趟扫描只保留上一帧。
  一次性返回整段视频的帧数组会让内存随时长和抽帧间隔线性增长；流式后内存
  占用是常数（实测把间隔调到 0.1 秒，峰值增量约 1 MB）。

**验证**：`make check-features` 70 项全过 —— 其中课件切换检测用 ffmpeg 现造一段
「黑 6 秒→白 6 秒→灰 6 秒」的视频，切换时刻已知，断言切换位置、停留时长、
同步率、阈值方向、非视频文件的报错路径。另外用假 LLM 跑通 `evaluate_transcript`
全链路，确认缺参照时 `completeness` 被跳过、有参照时可评、降权效果符合预期；
在旧 schema 的 SQLite 上验证迁移与幂等；用 TestClient 验证 multipart 上传的
`reference` 落库并透传给 worker（空白输入归一为「未提供」）；前端 `vite build` 通过。

**遗留**：说话人分离没有真实课堂数据验证过（缺 HF token）。
「思维引导」「教学资源融合」在指标文档里没有三级观测点，目前按二级名称评分。

### 2026-08-19 · 新增 evaluation_design.md，逐条厘清指标由谁来算

**问题**：`evaluation_criterion.md` 定义了 38 条三级指标，但「哪些本地算、哪些交
大模型」一直是隐性知识。逐条核对代码后发现两类系统性问题：一是本可精确计算的
指标被丢给了 LLM 凭印象打分（提问等待时间、课件停留时长完全没做，语速稳定性只差
一步汇总）；二是 `eval_vision.j2` 要求 VLM「120 字以内一段话写完」，7 条视觉指标
拿到的是 12 段自由文本，聚合不出任何比例型数值，等于视觉维度整体是印象分。

**思路**：把指标分四层落点 —— 本地-确定（有计算式）、本地-代理（能算相关量但
需模型解读）、VLM-转录（VLM 只输出观测标签，本地聚合成比例）、LLM-判断（必须
理解学科内容）。关键是新增「VLM-转录」这一层：**让 VLM 当观测员而不是评委**，
每帧输出 `gaze/gesture/board_*` 等固定字段，本地统计出「看讲稿帧占比 35%」这类
数值再交 Judge，视觉指标才有事实基础。同时保留 `unclear` 标签并上报其帧数，
避免模型在看不清时硬选一个标签制造假数据。

同时记录了三个不能靠「补个函数」解决的方法论缺口：说话人分离缺失导致教学效果
维度失真（现用「我觉得」等词判定学生发言，而教师说这话的频率更高，方向上就错了）；
「知识点覆盖完整」缺外部参照，模型只能先臆想一份应覆盖清单再对着打钩；
「无知识性错误」与其他指标同权，通用模型的学科事实核查能力撑不起这个权重。

**影响**：仅新增文档与 README 索引，未改代码。README 第九章补充三份指标文件的
职责划分，「暂缓项」的视频评估条目按设计文档重写为索引。后续改动按设计文档
第六节的六个阶段推进，前两阶段不引入新依赖也不改输出结构。

### 2026-08-18 · LLM 自修改为黑名单制（默认尝试修复）

**问题**：白名单 `HARD_VALIDATION_MARKERS` 导致每新增一种校验错误都要手工加入，
否则跳过自修（如学时配平、type 枚举等）。
**思路**：删除白名单，改为 `SKIP_LLM_REPAIR_MARKERS` 黑名单；除明确列出的错误外，
校验失败一律走 LLM 自修（最多 2 次）。当前黑名单仅含分阶段 source_id 覆盖错误。
**影响**：`optimizer.py`、`test_syllabus_validation.py`、README。

### 2026-08-18 · 固定框架 XML 对齐 Markdown 大纲级结构

**问题**：XML 固定框架仍是教案级（topic/explanation/activity/每章 AI），与 Markdown 大纲级框架
不一致，且易生成过长内容。
**思路**：重写 `syllabus_schema.xml`：章节改为 `<points><point>` + 可选 `<teaching_format>`；
目标去掉 evidence；考核/improvements 从简；AI 移至可选根级 `<ai_integration>`；
同步更新 `syllabus_optimize_schema.j2`、分阶段 prompt、`validate_schema_xml` 与测试。
**影响**：`syllabus_schema.xml`、`syllabus_optimize_schema.j2`、`syllabus_optimize_global.j2`、
`syllabus_optimize_chapters.j2`、`optimizer.py`、`syllabus_repair.j2`、`export.py`、
`test_syllabus_validation.py`、README。

### 2026-08-18 · 教学活动 activity type 同义词自动规范化并兜底「其他」

**问题**：固定框架 XML 常因 activity@type 写成「案例教学」「研讨」等导致校验失败；
用户反馈 enum 类错误未有效自修（整篇 XML 修复慢、易超时，且此前 activity 未做规范化）。
**思路**：扩展 activity 别名/关键词匹配；校验前 `_normalize_schema_enums` 统一规范
activity 与 assessment 的 type；无法识别时兜底为「其他」；允许枚举新增「其他」。
**影响**：`optimizer.py`、`syllabus_optimize_schema.j2`、`syllabus_schema.xml`、
`test_syllabus_validation.py`、README。

### 2026-08-18 · 固定框架 XML 考核 type 同义词自动规范化

**问题**：模型常输出「期末考试」「平时成绩」「论文」等考核 type，不在枚举内导致
`/syllabus/assessment/item[n] 的 type 不在允许枚举中`；且该类错误此前不会触发 LLM 自修。
**思路**：扩展 `_resolve_assessment_type` 别名与关键词匹配；校验前
`_normalize_schema_assessment_types` 自动写回标准 type；prompt/schema 补充允许枚举；
`type 不在` 纳入可自修标记。
**影响**：`optimizer.py`、`syllabus_optimize_schema.j2`、`syllabus_schema.xml`、
`test_syllabus_validation.py`、README。

### 2026-08-18 · Markdown 固定框架改为大纲级，限制输出不超过原文 2 倍

**问题**：固定 Markdown 框架沿用了 XML 深度结构（每章知识主题、活动设计、150–300 字阐述），
5 页 Word 可膨胀到 40+ 页，不符合「大纲」定位。
**思路**：重写 `syllabus_markdown_schema.md` 为要点式大纲框架；prompt 明确「不是教案」、
注入原文字数与 `max_output_chars`（默认 2×）；灵活 Markdown prompt 同步加篇幅约束；
`config.yaml` 新增 `markdown_max_length_ratio`；超标时校验仍通过但前端黄色提示。
**影响**：`syllabus_markdown_schema.md`、`syllabus_optimize_markdown_schema.j2`、
`syllabus_optimize_markdown.j2`、`optimizer.py`、`config.yaml`、`Syllabus.vue`、README。

### 2026-08-18 · 修复上传 Word/PDF 时大纲任务 KeyError: source_text

**问题**：异步 worker 读取任务时 `_syllabus_task_row` 未返回 `source_path`，
文件上传任务被误判为粘贴文本分支，访问 `task["source_text"]` 触发 KeyError。
**思路**：`get_syllabus_task(..., include_source=True)` 供 worker 使用；分支判断
改为 `.get()`，并在两者皆空时给出明确错误。
**影响**：`backend/app/core/db.py`、`backend/app/workers/syllabus_tasks.py`、README。

### 2026-08-18 · 大纲优化新增 Markdown 直出模式

**问题**：部分教师希望直接拿到可编辑的 `.md` 文件，而不是先产出 XML 再导出；
固定框架与灵活结构两种策略在 Markdown 场景下也需要分别对比。
**思路**：新增 `syllabus_optimize_markdown.j2`（灵活）与
`syllabus_optimize_markdown_schema.j2`（固定框架，注入 `syllabus_markdown_schema.md`）；
`optimizer.py` 识别 Markdown 模板后跳过 XML 校验/修复，做轻量 Markdown 结构校验；
前端增加两个模式选项，结果区渲染 Markdown 预览；导出链路识别 Markdown 源文件。
**影响**：`optimizer.py`、`export.py`、`Syllabus.vue`、`config.yaml`、
`syllabus_markdown_schema.md`、两个新 prompt、README、`test_syllabus_validation.py`。

### 2026-08-18 · 大纲优化改为异步任务，支持进度条与中途停止

**问题**：固定框架单轮生成需 5–10 分钟，同步 HTTP 请求易超时且页面无进度反馈。
**思路**：复用视频评估模式：`POST optimize_file` 立即返回 `task_id`，后台
`BackgroundTasks` 跑 single 生成；前端轮询 `/api/syllabus/task/{id}` 展示进度条，
`POST .../cancel` 协作式停止；SQLite 新增 `syllabus_tasks` 表。
**影响**：`backend/app/api/syllabus.py`、`workers/syllabus_tasks.py`、`core/db.py`、
`optimizer.py`（progress 回调）、`Syllabus.vue`、`client.js`、README。

### 2026-08-18 · 大纲优化 LLM 超时延长至 600 秒

**问题**：固定框架改回单轮后，模型生成整份深度 XML 常超过全局 LLM 300s 读超时，
浏览器与后端均报 `LLM 网络错误: The read operation timed out` 并返回 500。
**思路**：`syllabus.llm_timeout` 单独配置为 600s；`llm.chat` 支持按次覆盖
`timeout`；连接超时仍保持 30s，仅延长读等待。
**影响**：`config.yaml`、`ai_engine/providers/llm.py`、`optimizer.py`、
`Syllabus.vue`、README。

### 2026-08-18 · 固定框架改回默认单轮生成，避免多次调用超时

**问题**：分阶段流水线对每章单独调用模型，9 章大纲需 10+ 次请求，总耗时常超过
前端 axios 600s 与云端 LLM 300s 限制，页面频繁显示超时。
**思路**：`generation_strategy` 默认改为 `single`，一次生成整份 XML；分阶段代码保留，
需更高章节忠实度时在 `config.yaml` 手动开启 `staged`。
**影响**：`config.yaml`、`optimizer.py`、`Syllabus.vue`、README 配置说明。

### 2026-08-15 · 自动转义 LLM 输出中未转义的 &，修复 xmlParseEntityRef

**问题**：模型在正文里输出 `A & B` 等未转义字符，lxml 报
`xmlParseEntityRef: no name`；此前 `_should_skip_llm_repair` 又把该错误误判为
「可跳过 repair 的业务规则」，导致返回 `valid=false` 且页面只能看到残缺 XML。
**思路**：在 `_strip_wrapper` 与最终校验前用 `_sanitize_llm_xml` 补全 `&amp;`；
统一经 `_parse_xml_root` 解析；将 `xmlParse*` 纳入必须 repair 的硬错误；前端
按错误类型区分「语法错误」与「校验未通过」。
**影响**：`optimizer.py`、`Syllabus.vue`、`test_syllabus_validation.py`。

### 2026-08-15 · 放宽固定框架业务校验，避免误报 valid=false

**问题**：分阶段生成已能返回 200，但 LLM 常输出「约1.5 周」等非纯数字学时、
周次与学时混用导致活动学时配平误报，以及「课程项目」等考核 type 不在枚举内；
随后整篇 repair 再次 300s 超时，页面长期显示 `valid=false`。
**思路**：新增 `_parse_hours_text` 解析带单位表述；章节含「周」时跳过活动/总学时配平；
考核 type 增加别名映射；仅结构/深度类错误才走 LLM repair，业务规则类直接返回。
**影响**：`optimizer.py`、`test_syllabus_validation.py`。

### 2026-08-15 · 移除教学活动学时配平校验（周次与学时不可比）

**问题**：RL 等课程大纲章节 `hours` 为 1/1.5（周次），而 `<activity hours>` 为
2–4（课堂学时），原配平规则 10 项全部误报，页面显示「校验未通过」。
**思路**：删除「教学活动学时合计须等于本章 hours」硬校验（Prompt 仍保留为建议）；
章节合计与总学时不配平时，若量级差异明显（合计 < 总学时一半）则视为周次/学时混用并跳过。
**影响**：`optimizer.py`、`test_syllabus_validation.py`。

### 2026-08-15 · 修复固定框架漏章与校验修复超时导致 500

**问题**：`schema` 模式分批生成时模型常漏掉某个 `source_id`（如 S4），触发
`StagedGenerationError` 直接 500；有时分阶段已完成但 schema 校验失败后，整篇修复
prompt 过大，300s 超时再次 500。`adaptive` 模式不受影响故表现为仅固定框架失败。
**思路**：改为默认逐章生成（`chapter_batch_size: 1`）；漏章/覆盖错误时带
source_id 清单重试，XML 语法错误才走 repair；最终校验修复若超时则返回
`valid=false` 的 200 而非 500，并保留已生成 XML 供页面展示。
**影响**：`optimizer.py`、`config.yaml`、`syllabus_optimize_chapters.j2`、
`Syllabus.vue` 等待提示文案。

### 2026-08-15 · 修复固定框架章节定位失败导致单轮超时

**问题**：分阶段生成时，模型返回的 `start_marker` 常在原文前缀之后追加不存在的内容，精确
`find()` 失败；随后自动退回单轮生成，单次 prompt 更大且在 120s 超时内失败并返回 500。
**思路**：章节定位改为“精确匹配 → 空白归一 → 最长前缀匹配”；匹配长度用于推进 cursor。
分章 XML 解析失败时在批内自动修复（最多 2 次），不再退回更重的单轮生成。
同时将云端 LLM 超时由 120s 提到 300s，并将 `chapter_batch_size` 调为 2。
**影响**：`ai_engine/syllabus/optimizer.py`、`config.yaml`、
`syllabus_optimize_chapters.j2`；新增定位相关单元测试。

### 2026-08-15 · 固定框架改为按原文切片的分阶段生成

**问题**：即使 Prompt 和 XML 增加了忠实性与深度约束，把最长 8 万字原文一次性交给模型
重写整份大纲，仍容易因注意力稀释而漏章、改标题或把章节压缩成摘要。

**思路**：先让模型只返回可在原文中精确搜索的章节索引，再由 Python 按定位文本切出原始
章节正文；全局课程信息与章节内容分别生成，章节按配置分批优化后使用 `source_id` 依原顺序
合并。合并后及自动修复后都检查 source ID 覆盖；若章节索引或中间 XML 不可靠，默认安全
降级到原单轮流程。导出时隐藏 `origin/source_id`，避免内部追踪信息进入教师文档。

**影响**：新增章节抽取、全局骨架、分章优化三个 Prompt；`optimizer.py` 新增分阶段流水线和
降级元数据；`config.yaml` 新增 `generation_strategy`、`chapter_batch_size`、
`max_staged_chapters`、`staged_fallback_to_single`；测试覆盖原文切片、顺序合并和降级。
固定框架会增加 LLM 调用次数和同步请求耗时，灵活结构模式不受影响。

### 2026-08-15 · 固定框架改为“忠实展开 + 深度校验”

**问题**：原 XML 用大量可重复的短叶子节点承载章节内容，模型容易生成很多一两句话的
`point/activity`；Prompt 同时要求强制补全和广泛加入 AI，导致内容浅、分点碎且偏离原稿。
生成结果又只检查 XML 能否解析，漏节点、非法枚举、学时不配平仍会被当作有效结果。

**思路**：章节改用 `overview → topic → explanation` 承载连续论述，教学活动拆成目的、过程和
学生产出；Prompt 明确“忠实性优先”、限制主题与活动粒度、禁止无依据补全，并把 AI 改为
适切时才加入。新增 `origin` 来源标记、`additional_sections` 原栏目保留和
`needs_confirmation` 待确认清单。固定框架生成后执行结构、内容深度、枚举及数值配平校验，
失败时把框架和错误一并交给模型定向修复。

**影响**：更新 `syllabus_schema.xml`、固定框架 Prompt、修复 Prompt 和
`ai_engine/syllabus/optimizer.py`；新增 `test/test_syllabus_validation.py`。旧的固定框架 XML
不满足新结构，重新优化后才能通过校验；灵活结构模式仍只做 XML 语法校验。

### 2026-08-06 · 记录大纲优化三项联调问题（待下次迭代）

**背景**：完成 PDF 解析、双 Prompt 模式、MD/Word/PDF 导出后的首次实测。
**现象**：① XML 输出结构/字段仍不规范；② 导出文档版式简陋；③ 优化后内容深度不足（AI 策略等偏泛）。
**处理**：暂未改代码，已写入 README 功能②「当前聚焦」表，下次优先排期。

### 2026-08-06 · 大纲优化双 Prompt 模式（灵活结构 vs 固定框架）

**问题**：需在「保留原大纲结构」与「统一 XML 模板」两种策略间对比优化效果。
**思路**：保留 `syllabus_optimize.j2`（灵活）；新增 `syllabus_optimize_schema.j2` 注入
`syllabus_schema.xml`；`config.yaml` 的 `prompt_template` + API/前端 `prompt_mode` 切换。
**影响**：`syllabus_optimize_schema.j2`、`optimizer.py`、`Syllabus.vue`、`schemas.py`。

### 2026-08-06 · 大纲优化支持导出 Markdown / Word / PDF

**问题**：优化结果只有 XML，教师难以直接使用；且新 prompt 允许灵活 XML 结构，固定 schema 渲染不再适用。
**思路**：新增 `ai_engine/syllabus/export.py` 通用 XML 树遍历 → Markdown（零依赖）/ docx（python-docx）；
PDF 优先 pandoc，备选 LibreOffice 转 docx；API `GET /api/syllabus/export/{id}?format=`；前端「导出」下拉菜单。
**影响**：`export.py`、`syllabus.py` API、`Syllabus.vue`；PDF 需本机 `pandoc` 或 LibreOffice。

### 2026-08-06 · 大纲优化输入上限 3 万 → 8 万字

**问题**：PyMuPDF 正确解析中文 PDF 后，30k 字上限仍导致尾部章节（考核、参考文献）被截断送模。
**思路**：`syllabus.max_input_chars` 提至 80000，与沙龙 `max_transcript_chars` 对齐；
云端 qwen-plus 上下文足够容纳。
**影响**：`config.yaml`；仍超长时前端会显示「原文超长已截断」。

### 2026-08-06 · 中文 PDF 解析改用 PyMuPDF 多后端

**问题**：部分中文大纲 PDF 用 `pypdf` 抽取时汉字被映射成 Malayalam/Bengali 等无关字符，
界面「原始大纲」全乱码，但 PDF 阅读器内复制正常。
**思路**：`loaders._load_pdf` 依次尝试 PyMuPDF、pdftotext（若已装 poppler）、pypdf，
按 CJK 字符数与 exotic 脚本字符数评分选最优；仍像乱码则明确报错并引导 docx/粘贴。
**影响**：`ai_engine/rag/loaders.py`、`requirements.txt` 新增 `pymupdf`；大纲优化与 ingest 共用。

### 2026-08-06 · 问答检索改为全库 + 相似度阈值

**问题**：LLM 自动选库不稳定，低分片段仍进上下文导致引用不靠谱；零命中与弱命中未区分。
**思路**：去掉语料库 LLM 路由（非手动勾选时始终查全部库）；`score_threshold=0.5`、
`max_hits=12` 过滤弱相关块且不降级；零命中时 `qa_answer.j2` 禁止引用编号、
仅用模型通用知识并明示「语料未命中」；`top_k` 提至 15 以保障阈值过滤前有足够候选。
**影响**：`config.yaml`、`qa/pipeline.py`、`retriever.py`、`qa_keywords.j2`、
`qa_answer.j2`、`QA.vue` 提示文案。

### 2026-08-06 · course_syllabi 改为原版 HTML 并重建目录 README

**问题**：首批 AI 整理 Markdown 摘要非原文，与「参照真实 syllabus」目标冲突，且会与原版重复入库。
**思路**：curl 归档 11 门课公开 syllabus 网页为 `.html`；删除全部摘要 `.md`；
重写 `course_syllabi/README.md`——含完整目录、来源 URL/许可/归档日期，以及各课「参考价值」（仅 README，不入库）。
**影响**：`knowledge/corpora/course_syllabi/` 11 个 `.html` + README；需 `make ingest --corpus course_syllabi` 重建向量库。

### 2026-08-06 · course_syllabi 明确摘要性质与来源标注

**问题**：首批 syllabus 以 Markdown 摘要入库，文首来源说明不足，易被误认为官方 PDF 原文。
**思路**：11 篇统一增补「文献性质 / 原文形态 / 整理方式 / 与原文差异」；
`course_syllabi/README.md` 写明「首选原版 PDF/HTML、当前批次仅为网页摘要」的收录原则。
**影响**：仅语料元数据与 README，无代码变更。

### 2026-08-06 · course_syllabi 收录公开高质量教学大纲

**问题**：`course_syllabi` 除 README 外为空，大纲优化 QA 缺少可检索的参照 syllabus。
**思路**：从 MIT OCW、Stanford archive、Open Yale Courses、CMU 15-122 archive、
Harvard CS50 等**公开、公认高质量**来源整理 11 门课；统一 Markdown 模板（元数据、
评分/周次、参考价值、URL+归档日期）；按院校分子目录。
**影响**：`knowledge/corpora/course_syllabi/` 新增 11 篇 + 更新子目录 README；
需 `make ingest --corpus course_syllabi` 更新向量库。

### 2026-08-06 · edu_theory 补充 AI 教学应用方法语料

**问题**：已有政策/理论/评价文档，但「如何在课堂与作业中**具体用 AI**」的可检索方法不足
（备课工作流、roleplay、PROCESS 模板、主动学习脚手架、编程 debug 案例等）。
**思路**：新增 8 篇面向**教学应用**的 Markdown：Mollick 四原则、Bowen & Watson 备课与
PROCESS/Better-than-AI、Chan SARPS、课堂 roleplay 与 peer instruction 变体、编程实践案例；
与既有 policy/redesign 文档交叉引用，统一参考文献格式。
**影响**：`edu_theory` 新增 8 篇（合计 36 篇）；需 `make ingest` 更新向量库。

### 2026-08-06 · edu_theory 补充 AI 政策、理论与实践案例语料

**问题**：`edu_theory` 在 AI 专题仅 2 篇斯坦福导向文档，缺少中国/国际高校政策、
AI literacy、TPACK、评价重构、学术诚信与完整实践案例；与 `pku_salon` 中 2023–2025
大量 AI 讨论形成检索落差。
**思路**：按审计清单新增四个 AI 专题子目录（07–10），并在 02/04/06 延伸交叉文档；
统一沿用既有 Markdown 模板（文献性质、核实日期、DOI/URL 参考文献）；政策类据
教育部/清华/北大/MIT 等公开来源，理论类据 UNESCO/OECD/同行评审论文，案例为可复用
示范模板并标注非正式 syllabus。
**影响**：`knowledge/corpora/edu_theory/` 新增 15 篇 Markdown（合计 28 篇）；
需 `make ingest` 更新向量库。

### 2026-08-02 · 视频评估支持中途停止

**问题**：长视频诊断（尤其 ASR）一旦启动无法取消，只能等跑完或关页面，后台仍
继续占用 CPU/API。
**思路**：新增 `cancelled` 任务状态与 `POST /api/evaluation/task/{id}/cancel`；
worker 在 `progress()` 回调里轮询 SQLite 取消标志并抛出 `EvaluationCancelled`；
前端任务列表对排队/处理中任务显示「停止」按钮。
**影响**：`db.py`、`tasks.py`、`evaluation.py`（API）、`Evaluation.vue`、`client.js`。

### 2026-08-02 · 大模型默认锁定云端 API

**问题**：用户易把 ASR（本地 Whisper）误认为「在用本地大模型」；缺少 API Key 时
错误提示还建议改 local，与「默认云端」目标不一致。
**思路**：`config.yaml` / `.env.example` 明确 `PKU_MODE=cloud` 为默认；
`check_env` 与前端状态栏区分「云端 LLM」与「ASR 本地」；移除缺 Key 时改 local 的提示。
**影响**：`config.yaml`、`config.py`、`.env.example`、`llm.py`、`check_env.py`、
`main.py` health 字段、`Layout.vue`、README。

### 2026-08-02 · edu_theory 语料补全来源标注

**问题**：新增 12 篇 edu_theory 语料仅有简略「参考来源」，缺少 DOI/URL、
文献性质说明和访问日期，问答引用时难以核查真实性。
**思路**：为每篇统一增加文首元数据（文献性质、核心出处、核实日期）和
「参考文献与可追溯来源」节；期刊补 DOI，网页补访问日期；沙龙经验等非论文
内容单独标注；同步更新种子文档与 README 语料说明。
**影响**：`knowledge/corpora/edu_theory/` 下 13 篇 Markdown；需 `make ingest` 更新向量库。

### 2026-08-02 · 扩充 edu_theory 大学教育学语料

**问题**：`edu_theory` 仅有「种子-教学设计基础.md」一条演示文档，问答功能检索
教育学理论时覆盖不足，无法支撑课程设计、评价、AI 政策等常见问题。
**思路**：按六个主题建子目录，写入 12 篇结构化 Markdown（建构主义、认知负荷、
How Learning Works、布鲁姆/OBE/UDL、主动学习、提问策略、大班课、形成性评价、
Chickering 七原则、斯坦福 AIMES 与 AI 课程政策模板等），内容面向大学阶段并
标注参考来源；新增后需 `make ingest` 增量入库。
**影响**：仅 `knowledge/corpora/edu_theory/` 语料与 README 说明，无代码变更。

### 2026-08-02 · 沙龙视频自动转语料脚本

**需求**：用户把沙龙 mp4 放在 `pku_salon/raw_video/`，文件名前 8 位为日期；
不需校准主讲人，核心是提取教学知识；ASR 用 `small`。
**思路**：两步流水线——① ffmpeg + faster-whisper(small) 转写，产物存 `.work/`；
② 云端 LLM 按 `salon_structure.j2` 提取教学要点，输出 `YYYYMMDD-*.md`。
ingest 排除 `raw_video/`、`.work/`、`种子-*`、`README.md`。
**影响**：新增 `knowledge/process_salon.py`、`config.yaml` 的 `salon:` 段、
Makefile 的 `salon*` 目标；`loaders.py` 增加跳过规则。

### 2026-08-02 · 待解决问题按问答/大纲分类重组

**背景**：视频评估暂缓，后续迭代聚焦功能③智能问答与功能②大纲优化。
**思路**：第十一章不再用单一优先级大表混排三类功能的问题，而是按
「语料与建库 / 检索链路 / 规划与生成 / 前端体验」等子类分别罗列，
每条写清影响与优化方向，便于排期。视频评估与全局项移入「暂缓项」。
**影响**：仅文档，无代码变更。

### 2026-08-02 · 打分改为模态感知

**问题**：本地没装 VLM 时，「板书设计」「多媒体应用」「教学仪态」这三个纯视觉指标
被模型硬打了 23 分，把「教学方法」整个维度从合理水平拖到 23.3。
**思路**：缺失模态应当表达为「无数据」而不是「低分」。`judge_all` 新增 `available`
模态集合参数，完全依赖缺失模态的二级指标不再送给模型打分，直接标记 `assessed=false`，
排除在加权平均之外；整个维度都无法评估时维度分也置空，不计入总分。
**影响**：`judge.py` 新增 `available` 参数与 `_skipped_indicator`；结果结构新增
`assessed` / `skipped_count` / `overall.modalities` / `overall.skipped_indicators`
字段；报告模板与 `_fallback_report` 需过滤未评估项；前端需处理 `score=null`，
雷达图只画已评估维度（否则会塌成 0 分尖角，视觉上极具误导）。
**验证**：同一段测试视频，教学方法 23.3 → 45.0，3 个视觉指标正确标为跳过。

### 2026-08-02 · Whisper 中文转写统一转简体

**问题**：faster-whisper 转中文常输出繁体（「為什麼」「想一想」），导致
`feature_lexicon.yaml` 里的简体词表全部匹配不上，提问次数、启发次数假性归零，
进而让依赖这些证据的指标打分失真。
**思路**：在 ASR provider 出口处统一转简体，比在每个下游消费点各自处理更可靠。
用 zhconv（纯 Python、体积小），只在检测到语言是 zh 时转换。
**影响**：`providers/asr.py` 加 `_to_simplified`；`requirements.txt` 加 zhconv；
`check_env.py` 加检测项。
**验证**：同一段音频，提问次数 0 → 2，互动话语 1 → 5，启发性话语 0 → 1。

### 2026-08-02 · Judge 的 JSON 解析容错

**问题**：qwen2.5:3b 没按约定返回 `{"indicators": [...]}`，而是直接吐了一个裸数组，
`parsed.get()` 抛 `AttributeError`，整个评估任务失败。
**思路**：小参数量模型不遵守输出格式是常态，不能假设它守约。加一层归一化，
把裸数组、换了键名、扁平映射、夹带寒暄等形态都接住；重试提示里附上正确格式示例。
**影响**：`judge.py` 新增 `_as_indicator_list`；`qa/pipeline.py` 的 `_parse_json`
同样加了非 dict 的防御（走 fallback 而不是崩溃）。
**验证**：`scripts/test_parsing.py` 覆盖 7 种跑偏形态，全部通过。

### 2026-08-02 · 修复维度名被等级名覆盖

**问题**：五维得分显示成「合格 / 良好」而不是「教学态度 / 教学内容」。
**原因**：`grade_of()` 返回 `{"grade", "label"}`，用 `**` 展开进维度字典时，
`label` 键把维度自己的名字覆盖掉了。
**思路**：改用 `grade_label` 键名，从根上消除冲突，而不是靠调整展开顺序。
**影响**：`loader.py`、`pipeline.py`、`eval_report.j2`、`Evaluation.vue`
及 smoke_test 中所有 `overall.label` 的引用同步改名。

### 2026-08-02 · 大纲优化的错误信息去重

**问题**：API 返回「大纲优化失败：大纲优化失败：缺少 API Key…」，前缀重复两次。
**原因**：optimizer 和 API 层各套了一次前缀。
**思路**：optimizer 抛出的 `RuntimeError` 已经是面向用户的完整说明，API 层
单独 catch 它并原样透传，只对其他异常加前缀。

### 2026-08-02 · XML 脚手架属性改为代码清理

**问题**：schema 模板里 `repeatable="true"` 是给模型看的结构标注，但模型会照抄进输出。
**思路**：提示词已经写了「输出时请去掉」，但模型时灵时不灵。这种确定性的清理
不该指望提示词，改在 `prettify()` 里遍历节点直接删掉属性。

### 2026-08-02 · 项目初始化

从零搭建完整骨架并跑通三条链路。技术选型：前端 Vue 3 + Vite + Element Plus
（复用旧版 UI 资产，避免 Next.js 在纯 SPA 场景下的过度设计）；后端 FastAPI；
向量库 Chroma；LLM/VLM/Embedding 云端本地双通道；ASR 固定本地 faster-whisper
（云端 DashScope ASR 要求音频有公网 URL，本地文件不便接入）。

联调验证：用 macOS TTS 合成 50 秒中文讲课视频跑通完整流水线；
种子语料验证问答检索；粗糙的机器学习大纲验证 XML 生成与校验。
