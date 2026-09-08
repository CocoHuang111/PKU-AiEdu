# 北大问教 2.0

面向高校教师的智能教学支持系统。三个功能：

| 功能 | 输入 | 输出 |
| --- | --- | --- |
| ① 教学视频质量评估 | 教学视频 | 五维雷达图 + 25 项二级指标明细 + 诊断报告 |
| ② 教学大纲优化 | PDF / Word / Markdown 大纲 | Markdown 大纲（原文微调 / 重构框架）+ AI 助教助学融入课程设计 |
| ③ 教学智能问答 | 自然语言提问 | 基于多语料库检索的带引用回答 |

技术栈：Vue 3 + Vite + Element Plus 前端，FastAPI 后端，PostgreSQL 业务库，Chroma 向量库。
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
| PostgreSQL | **16** | 用户、Session、任务、文件元数据和审计日志 |
| Docker | 仅数据库可选 | `make db-up` 只启动 PostgreSQL 16；本机已有 Postgres 17 也可，创建 `pku2` 用户和库即可 |

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

# 4. 业务数据库
make db-up          # 或使用本机 PostgreSQL 16，并设置 DATABASE_URL
make db-migrate
python -m scripts.create_admin --username admin --display-name 管理员

# 5. 自检
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

浏览器打开 http://localhost:5174 先登录（`#/login`），通过后进入教学智能问答（`#/qa`）。

Ubuntu 服务器内测部署见 [`DEPLOYMENT.md`](DEPLOYMENT.md)：用固定公网 IP 走 HTTPS，
不必先买域名。生产部署使用 `compose.production.yml`，会建立全新的 PostgreSQL 和
Chroma 数据，不需要复制本机的历史任务、上传文件或旧向量索引。

`AUTH_MODE=local` 时用工号密码注册/登录；管理员只能用 `python -m scripts.create_admin` 或已有管理员提升，注册接口拿不到 `admin`。
`AUTH_MODE=pku_sso` 时本地注册和登录关闭，登录页只显示北京大学统一身份认证。本地账号不会自动合并到北大账号。

切换认证模式前先备份数据库。切换本身不迁移、不合并、不删除账号。

### 数据库、备份与认证切换

```bash
# 启动 / 初始化（本机已有 Postgres 时不必开 Docker）
make db-up
make db-migrate

# 备份（容器内 postgres）
docker compose exec -T postgres pg_dump -U pku2 pku2 > backup.sql

# 恢复
docker compose exec -T postgres psql -U pku2 -d pku2 < backup.sql

# 切换到北大统一身份认证：只改服务端环境变量，不要自动清库
# 在 .env 中设置：
#   AUTH_MODE=pku_sso
#   ADMIN_IDENTITIES=pku_sso:官方稳定subject
# 然后重启后端。本地注册/登录入口关闭；原本地账号保留为历史数据。
```

旧 `data/app.db` 不会被修改或删除。如果要把旧业务记录挂到某个新用户下：

```bash
python -m scripts.import_sqlite --db data/app.db --user-id <UUID>
python -m scripts.import_sqlite --db data/app.db --user-id <UUID> --execute
```

---

## 四、命令速查

| 命令 | 作用 |
| --- | --- |
| `make check` | 环境自检：Python / ffmpeg / 依赖 / API Key / 向量库 |
| `make check-features` | 客观特征自检：词表、分段汇总、等待时间、VLM 标签解析、rubric 对齐（**不调大模型，不花额度**） |
| `python scripts/draw_feat_overview.py` | 重画客观特征总览四张卡的示意图 SVG（默认写到 `design-mockups/objective-feature-four-groups/`） |
| `python scripts/draw_pace_page.py` | 重画授课内容页语速折线 / 提问结构 PNG（默认写到 `design-mockups/pace-page/`；`--from-task` 可读评估结果 JSON） |
| `python scripts/draw_audio_page.py` | 重画声学特征页波形 / 响度 / 基频 / 等待样本 PNG（默认写到 `design-mockups/audio-page/`；`--from-task` 可读评估结果 JSON） |
| `make check-syllabus` | 大纲优化单元测试：XML/Markdown 校验、分章生成、导出（**不调大模型**） |
| `make install` | 安装基础依赖 |
| `make install-local` | 安装可选依赖：本地 embedding / rerank、说话人分离 |
| `make backend` | 启动 FastAPI（8010），带 `--reload` |
| `make frontend` | 启动 Vite（5174） |
| `make db-up` | 准备 PostgreSQL：本机 5432 已在监听则直接复用并确保有 `pku2` 库；否则才 `docker compose up` |
| `make db-down` | 只停 Docker 容器。本机 Homebrew Postgres 不受影响 |
| `make db-migrate` | `alembic upgrade head` |
| `make db-downgrade` | `alembic downgrade -1` |
| `make create-admin` | 创建或提升本地管理员（会提示输入密码） |
| `make test-auth` | 认证、隔离、管理员、mock SSO、Alembic 测试 |
| `python -m scripts.import_sqlite --user-id <UUID>` | 可选：预览把旧 `data/app.db` 记录挂到指定用户（加 `--execute` 才写入） |
| `python -m scripts.purge_user_data --user-id <UUID>` | 预览清理某用户；加 `--execute` 才删除 |
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
| `make check-expert-rules` | 专家评分长表、冻结规则和 Judge 可观察性测试（**不调大模型**） |
| `make expert-rules-ingest` | 四份专家评分表 → `dataset/expert_rules/expert_reviews_long.csv` |
| `make expert-rules-extract` | 评语 → 原子观点（会调大模型，支持续跑） |
| `make expert-rules-distill` | 分数条件统计 → 待人工审核的结构化规则 |
| `python -m scripts.test_gb` | GB 训练约定：离散化、2022 划分、玩具拟合 |
| `python -m scripts.train_gb_obj_reg` | 客观特征+五维 → 回归 |
| `python -m scripts.train_gb_llm_reg` | 只用五维 → 回归 |
| `python -m scripts.train_gb_obj_cls5` | 客观特征+五维 → 5 分类 |
| `python -m scripts.train_gb_llm_cls8` | 只用五维 → 8 分类 |
| `python -m scripts.train_gb_obj_only` | 只用客观特征 → 回归 |
| `python -m scripts.train_gb_ind_reg` | 只用二级指标 → 回归 |
| `python -m scripts.train_gb_obj_cls5` | 客观特征+五维 → 5 分类 |
| `python -m scripts.train_gb_obj_only_cls5` | 只用客观特征 → 5 分类 |
| `python -m scripts.train_gb_ind_cls5` | 只用二级指标 → 5 分类 |
| `make train-gb` | 原来四个（同一 `gb_split.json`）再 `compare_gb` |
| `make train-gb-2018` | 2018 `fixed_prompt` / `effect_inferred` 各训四种 GB（共用年内划分） |
| `make train-gb-2018-v4` | 从快照恢复 2018 v4 后训六种 GB（含客观/二级） |
| `make train-gb-2018-v7-v9` | 2018 v7.1 / v9 各训六种 GB，同一年内划分对照 |
| `make train-gb-all-v7-v9` | 四年拼表后 v7.1 / v9 各训六种 GB（2022 留出 14 人） |
| `make train-gb-v9-regression-experiments` | v9 四种小样本回归实验；独立输出，不改线上模型 |
| `make train-gb-live` | 四年 v7.1 全量客观特征+五维 5 分类 → `models/live/gb_obj_cls5.pkl`（线上总分） |
| `make judge-overall-2018` | 2018 测试集：LLM 读取五维与客观特征盲评总分，再与专家/GB 对照 |
| `python -m scripts.build_eval_dataset inventory --root … --xlsx … --out …` | 扫描教师文件夹 + 打分表 → inventory / manifest |
| `python -m scripts.build_eval_dataset extract --manifest … --resume` | ASR + 课件 + VLM + Judge（慢；可断点续跑） |
| `python -m scripts.build_eval_dataset reflect --dir …` | 对照专家评语写 lesson（改过 prompt 后不要加 `--resume`） |
| `python -m scripts.build_eval_dataset distill --dir …` | 把本年 lesson 压成 5–8 条口径 |
| `python -m scripts.build_eval_dataset rejudge --dir … --prompt-version vN [--output-cache cache_name] [--resume]` | 只重打分，不重跑转写；可把新版评分写入独立缓存 |
| `python -m scripts.build_eval_dataset merge --dir … [--scores-cache cache_name] [--output-dir …]` | 从指定评分缓存写出 training_detail / training_gb / alignment |
| `python -m scripts.build_eval_dataset combine --dirs dataset/20XX_spring … --out dataset` | 拼成 training_*_all.csv（加 batch 列） |
| `PKU_MODE=local <任意命令>` | 强制走本地 Ollama，无需 API Key |
| `git status` | 本地仓库；**无远程**。视频、xlsx、`.env`、模型、cache 已 ignore |
| `lsof -ti :8010 \| xargs kill -9` | 端口被占用时强杀 |

---

## 五、整体框架

### 分层

```
frontend/          Vue 3 单页应用，只管展示与交互
      │  HTTP / SSE（Vite 代理 /api → 8010）
backend/app/       FastAPI：路由、参数校验、PostgreSQL 持久化、异步任务调度
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
├── evaluation_criterion.md  # 评估指标的需求定义（人工维护，五维 41 条三级指标）
├── evaluation_design.md     # 每条三级指标由谁来算：本地 / VLM / LLM 的划分与缺口
├── ai_engine/
│   ├── config.py            #   读 config.yaml，按 mode 解析出各能力的配置
│   ├── providers/           #   base.py 定接口，llm/embedding/asr.py 给实现
│   ├── pedagogy/
│   │   ├── evaluation_rubric.yaml   # 五维 25 项指标 + 客观特征标签（改这里就能调）
│   │   ├── feature_lexicon.yaml     # 文本特征统计词表与判分阈值
│   │   ├── syllabus_schema.xml      # 大纲级 XML 结构（与 markdown_schema 对齐）
│   │   ├── syllabus_markdown_schema.md # 大纲 Markdown 固定框架
│   │   └── prompts/*.j2             # Jinja2 提示词
│   ├── evaluation/          #   media / judge / pipeline / train
│   │                        #   特征提取按来源分文件：
│   │                        #     text_features     转写文本统计 + 分段汇总
│   │                        #     audio_features    librosa 声学特征
│   │                        #     timeline_features 提问等待时间、ASR 置信度
│   │                        #     transcript_punc   Whisper 后用 LLM 补中文标点
│   │                        #     slide_features    课件切换（先框投影/板书，再格子帧差）
│   │                        #     materials         教师上传的大纲/课件/讲稿解析
│   │                        #     vision            VLM 结构化标注 + 聚合
│   │                        #     diarization       说话人分离（可选，默认关）
│   │                        #     pace_charts       授课内容页 matplotlib PNG（语速折线 / 提问条）
│   │                        #     audio_charts      声学特征页 matplotlib PNG（波形 / 响度 / 基频 / 等待）
│   │                        #     gb.py / gb_fit.py  GB 校准；线上总分用 models/live/gb_obj_cls5.pkl
│   ├── syllabus/optimizer.py
│   │             export.py      # XML / Markdown → Markdown / docx / pdf（大纲与评估报告共用）
│   ├── qa/pipeline.py
│   └── rag/                 #   loaders / splitter / store / retriever
├── backend/app/
│   ├── main.py              #   应用装配、CORS、health
│   ├── api/                 #   auth.py / admin.py / evaluation.py / syllabus.py / qa.py
│   ├── models/              #   SQLAlchemy 模型
│   ├── auth/                #   Local / PKU SSO provider 与 Session
│   ├── core/db.py           #   PostgreSQL 业务仓储
│   ├── core/auth.py         #   get_current_user / require_admin
│   ├── core/security.py     #   Argon2id、Session 哈希
│   └── workers/             #   tasks.py 评估任务；syllabus_tasks.py 大纲优化
├── frontend/src/
│   ├── api/client.js        #   axios 封装 + Cookie + 统一错误提示
│   ├── api/stream.js        #   SSE 流式读取（credentials: include）
│   ├── authStore.js         #   当前用户（权威来源是 /api/auth/me）
│   ├── qaStore.js           #   问答会话与 SSE 状态（切页后仍继续）
│   └── views/               #   Login / Layout / QA / Evaluation / Syllabus / Profile / admin
├── alembic/                 #   数据库迁移
├── docker-compose.yml       #   仅 PostgreSQL 16
├── knowledge/corpora/       # 知识语料（放你的文档）
├── data/                    # 上传、关键帧、Chroma；旧 SQLite 不删不迁
├── test/                    # 联调样例：大纲 PDF/Word 可入库；微格视频与打分表不入库
├── dataset/                 # 评估训练批次（manifest / csv / 蒸馏要点；cache / cache_* 不入库）
└── scripts/                 # check_env / check_features / check-syllabus
                             # / smoke_test / qa_test / test_parsing
                             # / build_eval_dataset / test_eval_dataset / test_gb
                             # / train_gb_* / compare_gb / draw_feat_overview / draw_pace_page
                             # / create_admin / import_sqlite / purge_user_data / test_auth_system
```

### 数据流

```
功能①  视频（必填）+ 课件 / 大纲 / 讲稿（选填）
            │    ffmpeg 抽音轨 + 视觉双轨抽帧
            │    稀疏轨：均匀 12 帧 → 送 VLM（每帧一次调用）
            │    密集轨：每 3 秒灰度缩略帧 → 有 VLM 时先框投影/板书再只比对框内
            │    若上传课件：渲染页面 → 另走 VLM 逐页标注（板书/课件设计以此为准）
            → 有讲稿则直接当转写；否则 faster-whisper 转写（自动繁转简，再用 LLM 补中文标点）
            → 客观特征按来源分 7 组：
                 text       转写文本统计 + 分段汇总
                 audio      librosa 声学特征
                 timeline   提问等待时间、ASR 置信度
                 slides     课件切换、停留时长、讲授同步
                 vision     课堂关键帧 VLM 标签聚合成比例
                 courseware 上传课件的页面标注（选填）
                 speakers   说话人分离（可选，默认关闭）
            → LLM-as-Judge 按维度逐项打二级分，再由模型按课型综合出一级分
            → 五维雷达仍走 Judge（v7.1 prompt）；总分由四年 v7.1 客观特征+五维 5 分类 GB 校准
            → 生成报告 → 摘要回流进向量库

功能②  文档 → PyMuPDF/pypdf 多后端解析
            → 固定框架：章节索引 → 原文切片 → 全局骨架 → 分批章节优化 → source_id 合并校验
              （灵活框架仍为单轮生成；中间结果异常时固定框架可降级为单轮）
            → lxml 结构/深度/业务校验，不合法则带报错回喂模型自修（最多 2 次）
            → 可导出 Markdown / Word / PDF（export.py）

功能③  提问 → LLM 生成检索关键词
            → 勾选的历史评估报告直接带入；公开库仍向量检索
            → LLM 结合指定报告与检索结果生成带 [n] 角标的回答（SSE 流式）
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
「本地帧差检测；有 VLM 时先框投影/板书」），弱代理量必须写清它弱在哪 —— 比如 ASR 置信度
混杂了录音质量与口音，课件切换次数来自画面局部跳变、仍非精确页数。不标局限，模型会把
所有数字当成同等硬度的事实。

**课程大纲与课件都是选填，有和无走两条评分口径**。
有大纲时，「内容完整性」对照大纲中与本节课相关的安排来评；没有大纲时，
根据转写判断这节课自身是否形成知识闭环。有课件时，板书/课件的布局与可读性
以上传文件为准，课堂关键帧只用来看教态和学生状态；没有课件时，这些项改看
抽取的关键帧。课堂节奏（停留、切换同步）始终看视频帧差，不看课件文件。

**每个一级维度单独调一次 LLM**，而不是一次性打完 25 项。提示词更聚焦、输出更短，
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
| ASR（语音识别） | faster-whisper（**固定本地，非大模型**）；中文转写后默认用 LLM 补标点 | 同左 |

显式切换方式（不推荐日常使用本地）：

```bash
# .env 中 PKU_MODE=cloud   ← 默认，大模型走通义千问
PKU_MODE=local make backend  # 仅当需要 Ollama 时
```

> 换 embedding 模型后向量维度会变，需要 `make ingest-reset` 重建向量库。

---

## 七、三个功能怎么用

未登录会跳到 `#/login`。本地模式注册字段：工号、密码、确认密码、姓名、可选邀请码。
登录后「我的」里工号只读（即登录账号），可改姓名、职称、院系、邮箱、手机、课程、简介和头像。
问答 / 评估 / 大纲的历史只看当前用户的；管理员走独立的 `#/admin`。

### ① 教学视频质量评估

默认左侧展开历史任务（可搜索、按全部/进行中/已完成/失败筛选，按进行中/今天/更早分组）。
右侧是「教学视频评估」工作区（固定宽度居中，收起历史列表后不拉宽）：上方课堂视频（必填，通栏拖入），下方课件 / 大纲 / 讲稿三个选填入口同样支持拖入或点击选择，底栏显示已选材料数并开始评估。
点历史任务（进行中 / 已完成 / 失败）会在右侧回看当时上传的视频和材料，并显示「解析中」进度、「评估已完成」或「解析失败」。
已完成任务点「查看评估结果」才进入报告（综合总览 + 现有明细标签页）；点「重新评估」或「新建评估」回到上传。
收起侧栏后左上角只留历史 / 新建图标。
任务异步执行，前端每 2.5 秒轮询进度。
历史任务右侧垃圾桶可删除；进行中的任务删除前会先停止。
处理中或排队中的任务可点「停止」中途取消诊断（在 ASR、视觉分析、打分等
步骤的进度回调处协作式退出，短步骤如抽音频期间可能需稍等片刻）。

**视频必填**（mp4 / mov / mkv 等）。抽音轨、关键帧和课件切换。
课件、大纲、讲稿选填。

**课件选填**（pdf / pptx / ppt）。有则以上传课件评版式与可读性；
没有则根据课堂关键帧判断。PPT/PPTX 优先用 LibreOffice 转成 PDF 再渲染页面，
转不成时 PPTX 会退回纯文本（版式只能弱判）。扩展名是 `.pptx` 但文件截断时，
会改用同目录同名的 `.ppt`。解析彻底失败则按无课件口径继续，不把整堂课判死。

**大纲选填**（pdf / Word / txt / md）。有则对照大纲安排评本节课内容完整性；
没有则根据讲稿或转写看这节课是否形成知识闭环。

**讲稿选填**（pdf / Word / txt / md 文件）。后端当作转写文本：
有讲稿就跳过语音识别，直接用这份文本打分；没有讲稿才从视频跑 ASR。

**模态缺失的处理**：如果关掉视觉分析（或 VLM 不可用），依赖 `vision` 模态的
二级指标会被标记为「未评估」，在明细表里灰显，也不进雷达图。
但**课件切换检测不依赖逐帧 VLM 标注**：默认会先花 1～2 次调用框出投影/板书，
再在框内做本地帧差；关掉 VLM 或框不到时退回整幅格子，所以「板书停留充分」
「切换与讲授同步」在 `vlm_enabled: false` 时仍然可评。上传了课件时，课件页标注会点亮 `vision` 模态，
即使关键帧分析失败，「板书设计」仍可能可评。

**诊断摘要**：总览三列（优点 / 问题 / 建议）优先用模型写的「〇、诊断摘要」——
每类恰好 2 条短句，后端解析进 `digest` 后从报告正文删掉。诊断报告页和导出都不带这一节。
旧任务没有 `digest` 时，仍从报告原文剪句兜底；展示时同样会藏掉该节。
报告模板是 `eval_report.j2`，v7.1 / v9 打分后都走这一份，没有分叉副本。

**导出报告**：结果页右上角红底白字「导出报告」，可选 Markdown / Word / PDF。
走 `GET /api/evaluation/task/{id}/export?format=markdown|docx|pdf`，
转换复用大纲的 `export_syllabus`（Markdown 源）。Word / PDF 需本机 `pandoc` 或 LibreOffice。
导出文件开头补标题、生成日期、综合得分、课堂时长、评估方式和对照材料，不改库里的报告正文。

**客观特征怎么看**：标签是四个大组——
**授课内容**（文本）、**声学特征**（声学+时序）、**课堂视觉**、**工具调度**（课件+切换）。
进客观特征页默认落在授课内容。说话人分离默认关，有数据时才多一个标签。

**客观特征明细**：点大组标签进入该组。
**授课内容**只含文本特征，按稿子做成大号数字、语速折线、提问结构条和指标明细表。
语速折线和提问结构条由后端 `GET /api/evaluation/task/{id}/chart/{speech_rate|question_structure}`
用 matplotlib 现画 PNG（比页面里手写 SVG 更接近折线/条形稿）；示意数据可用
`python scripts/draw_pace_page.py` 重画。表里的「建议 ≥ 15 次」等参考范围只给展示，
不进 Judge；语速三项仍用 rubric 的 `ideal` 判状态。
没有参考范围的项不进表：无提问段落用环形图，其余用图标+数字卡。有参考范围的项仍用指标 / 当前值 / 参考范围 / 状态 / 说明五列表。
**声学特征**页与授课内容同一套排版：顶部四个数字（响度、信噪比、平均等待、ASR 高置信占比），
左右两栏图（音轨波形+响度/基频，提问等待样本+分布条），下面指标 / 当前值 / 参考范围 / 状态 / 说明五列表。
没有参考范围的项（长停顿次数、等待样本数）放在右侧 ASR 置信度分布下面，用图标数字卡。
图表走 `GET /api/evaluation/task/{id}/chart/{audio_wave|loudness_series|pitch_series|wait_samples|slide_freq}`，
matplotlib 现画。新任务会把 `wave_envelope` / `loudness_curve` / `pitch_curve` / `long_pause_times`
和 `wait_samples` 写进 `raw_features`（不进 rubric、不进 Judge）；旧任务没有曲线时按均值生成示意，
没有逐次等待则图上写「暂无」。表上的响度 -26～-16 dB、等待 3–6 秒等区间只给展示。
**课堂视觉**顶部四个黑色数字（看学生、有手势、板书或投影、抬头率高），下面左分布条、右三条结论（左侧对号、无标题无分割线），不再套卡片。
分布条用现有视觉特征：视线四分类互斥；教学行为是有手势 / 讲台前或走动 / 有人举手；课堂媒介是板书或投影 / 含图表 / 可读性高。
后两组可以重叠，条宽按合计归一化，图例仍写原始占比。结论由占比规则写成，不进 Judge。
明细表与声学页相同：指标 / 当前值 / 参考范围 / 状态 / 说明。看学生 ≥50%、看讲稿 ≤25% 等区间只给展示；
帧数、走动、举手、可见学生人数没有区间，标成事实观察。
**工具调度**分有无上传课件两套。有课件：四个数字（已分析页数、版式清晰、页面切换、讲授同步），左栏版式/密度/图表/可读性分布条，右栏切换时间轴和四项切换数字。
无课件：说明行写成「已获得 n / 13 项，7项课件页面质量指标因未上传材料已跳过」；四个数字改成切换次数、频率、停留中位数、讲授同步；全宽时间轴加节奏批注；下面是分段切换频次图、停留时长环图和一条结论。
时间轴和频次图用 `slide_change_times`；停留环图优先 `dwell_samples`（新评估写入 `raw_features.slides`，不进 Judge），旧任务按切换时刻反推。短停留仍按词典 20 秒，不是稿子里的 30 秒。
明细仍是五列表。切换次数、已分析页数是事实观察；每 10 分钟 3–5 次等区间只给展示。
其余大组（有数据时的说话人）仍按来源分段，每项除数字外有一条比例条：占比类按 0–100% 铺；
次数 / 语速等按单位刻度铺。rubric 里写了 `ideal` 的项会画出浅绿色理想区间，
落入为绿、略偏为黄、明显偏离为红。来源就是可信度：`text` / `audio` /
`timeline` / `slides` 是算出来的，`vision` / `courseware` 是 VLM 看出来再聚合的。
带括号说明的标签是弱代理量，比如「学生发言线索次数（词表粗估，偏高）」。

**关键帧下面的彩色标签**是 VLM 的逐帧结构化观测（视线、手势、可读性、抬头率），
绿色为正向、红色为负向。这些标签聚合后就是上面 `vision` 组的比例数字。
若上传了课件，结果页会多一组「上传课件页面观测」。

脚本联调仍可用 `POST /api/evaluation/transcript` 只喂转写，不走页面入口。

用专家打分表按年构造训练批次（inventory / extract / reflect / distill / rejudge / merge）
见 **八、构造评估训练批次**。不要把蒸馏口径粘进 `eval_judge.j2`。

### ② 教学大纲优化

默认左侧展开历史任务（可搜索、按全部/进行中/已完成/失败筛选，按进行中/今天/更早分组），
交互与教学评估一致。右侧上传区也按评估页来：虚线拖入框、选中后显示文件卡片，再点「开始优化」。
页面只提供**原文微调 / 重构框架**两种 Markdown 模式（不再露出 XML）。
提交后**立即返回任务 ID**，进度条每 2.5 秒轮询；处理中可点**停止**（协作式取消）。
点历史任务可回看进度或打开对应结果。
收起侧栏后左上角只留历史 / 新建图标。
历史任务右侧垃圾桶可删除；进行中的任务删除前会先停止。

完成后输出 Markdown，页面上原文与结果左右对照，可复制或下载；
校验通过后可**导出 Word / PDF**。旧的 XML 任务仍可打开并按原格式下载。

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

# 删除任务（进行中请先停止，或由页面删除时自动停止）
curl -X DELETE "http://127.0.0.1:8010/api/syllabus/task/{task_id}"
```

**页面上的两种优化模式**（均为 Markdown）：

| 模式 | API `prompt_mode` | Prompt 文件 | 说明 |
| --- | --- | --- | --- |
| **原文微调**（页面默认） | `markdown` | `syllabus_optimize_markdown.j2` | 在原文上增删：目录、段落/列表体例、题记引语等个人表述都保留；禁止套通用模板、禁止一律改成要点列表；AI 助教/助学写入原课程设计栏目；不超过原文 2 倍 |
| **重构框架** | `markdown_schema` | `syllabus_optimize_markdown_schema.j2` | 映射到 `syllabus_markdown_schema.md`；各章教学形式、考核政策与「AI 辅助教学」节必写；大纲级，不超过原文 2 倍 |

XML 两种模式（`adaptive` / `schema`）仍可通过 API 调用，页面不再提供入口；日常优化只走上面两个 Markdown 入口。
API 未传 `prompt_mode` 时仍由 `config.yaml` → `syllabus.prompt_template` 决定（当前默认仍是 XML 的 `syllabus_optimize.j2`）。
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

默认左侧展开历史会话（可搜索；列表分成「置顶」「最近」，
格式与教学评估的历史任务一致）。回答上方会显示这次用了哪些关键词、查了哪些语料库，下方可展开引用来源。
输入框左侧「+」打开检索范围。公开语料库**默认全选**；取消勾选则不检索该库。
「历史评估报告」**默认不选**。点它会弹出任务列表，可滚动勾选、全选或清除；确定后才纳入检索。
勾选后提问会把这些任务的诊断报告**整份放进提示词**（总分、五维、正文；单独 12000 字额度），
再检索沙龙/大纲等作补充。检索关键字里不会出现「历史评估」，因为报告不是靠关键字搜进来的。
这份列表跟评估页左侧任务同步：评估成功完成会写入向量库，删除任务会清掉对应块；
切回问答页或再打开弹窗会刷新。失败、取消、进行中的任务不会出现。
回答提示词会把指定报告标成该教师自己的课堂诊断：问自己的课时应依据报告分析，
不得说「无法观摩课堂」。检索条上会显示「历史评估报告 ·已带入 N 份」。

提问后可以切到教学评估或大纲优化，也可以再开一个新对话继续问：生成在后台继续，
历史列表会标「思考中」，多个会话可以同时思考。当前打开的会话若正在生成，发送按钮才会禁用。
问句在发出时就落库，整段答完再写入；刷新后会回到上次会话，若仍在生成则轮询直到完成。

---

## 八、构造评估训练批次

按**自然年**一批。当年用冻结的 Judge prompt 打分；专家评语只在打完分之后
`reflect` / `distill`，**不进该课分数**。蒸馏出的短口径用 `--lessons` 注入
**下一年**的 extract，不要粘进 `eval_judge.j2`（线上评估默认不带历史口径）。
全部年份跑完、prompt 冻结后再统一 `rejudge` + `merge` 出训练表。单年约 20 条，
不够单独训稳 GB。

打分表含联系方式。原始 xlsx / 视频只留本机（`.gitignore` 已排除）；仓库里的
csv **不含**邮箱电话。

### 目录约定

```
test/20XX春微格作业-N人/     # 2018/2019：一人一文件夹 + 打分表 xlsx（不入库）
test/2022微格/               # 2022：备课/试讲两个平铺目录 + 三位专家合并表
test/2024春微格作业-74人/    # 2024：备课/试讲平铺；文件名是「姓名」或「姓名-学号」
dataset/20XX_spring/
  inventory.csv              # 扫描全表：含 skip 原因
  manifest.csv               # 训练候选：有姓名匹配且有视频
  lessons/{姓名}.json        # reflect 逐课产出
  lessons_distilled.md       # distill 压成 5–8 条（人工确认后再挂明年）
  cache/{姓名}/              # 不入库（默认评分缓存）
    evidence.json            # 转写 + 客观特征 + 课件文本（体积小）
    scores.json              # 当年 prompt 的五维分
  cache_*/{姓名}/            # 不入库（rejudge --output-cache 的独立版本）
  v4/                        # 2018：从快照恢复的 v4 merge（含二级指标）
  training_gb.csv            # merge：客观特征 + 五维 LLM 分 + 专家百分制（无评语）
  training_detail.csv        # merge：上面这些 + 评语和二级指标
  alignment.csv              # merge：专家分 vs LLM 总分残差
  fixed_prompt/              # 2018：v5-rules17 独立 merge（教学效果多半缺失）
  effect_inferred/           # 2018：v6 独立 merge（五维齐全）
  gb_split.json              # 2018 年内 80/20，两套 prompt 共用（勿覆盖四年划分）
dataset/lessons_frozen.md    # 四年 distill 人工合并的 8 条；最终 rejudge 只用这一份
dataset/training_gb_all.csv  # combine：四年拼表，训 GB 用这一份
dataset/gb_split.json        # 从 2022 划出的预测集 id（四年对照共用）
dataset/gb_predictions.csv   # 四个模型在预测集上的 0–5 对照
dataset/training_detail_all.csv
dataset/alignment_all.csv
```

纳入 manifest：能对上打分表「姓名」，**且**有教学视频。
`no_video` / `no_score` 写入 inventory，不进 extract。Finder 复制出的
`某文件夹 (2)` 会跳过。2018 表是「评语」单列；2019 是「整体优点 / 需要改进」；
2022 是「突出优点 / 需要改进」，且同一人三行（每位专家一行），扫描时压成
一人一行并拼 comment。2024 是一人一行「汇总评语-ZX」，另把「备注」接上；
分数用「平均分」，不要用旁边那列「分数」（那是某一位专家）。xlsx 若第一行
是标题，会自动找含「姓名」的那一行当表头。CSV **不含**邮件、职工号。

2022 / 2024 都不是一人一夹：视频在试讲目录、课件在备课目录。2022 文件名
`编号-姓名-院系`（青教赛有前缀）；2024 是 `姓名.mp4` / `姓名-学号.pdf`
（英文名可能比打分表少一个词，按前缀对齐）。目录里堆满编号文件时自动按
姓名把两边拼成一条，不要把整夹当成一个人。

### 从专家评分表学习 Judge 规则

新的规则学习不再把逐课 `reflect` 压成 8 句口号，而是先保留原始的
“分数—评语”对应关系，再判断某个问题在低分中是主缺陷，还是在高分中只是
改进建议。代码、Prompt、运行产物和生产规则分开放置：

```
scripts/eval_dataset/expert_rules.py       # 清洗、统计、冻结逻辑
scripts/build_expert_rules.py              # 命令行入口
ai_engine/pedagogy/prompts/expert_*.j2     # 原子抽取 / 条件规则 Prompt
dataset/expert_rules/                      # 长表、逐条缓存、候选规则、审计报告
ai_engine/pedagogy/expert_rules.yaml       # 仅存人工批准、供线上 Judge 使用的规则
```

执行顺序：

```bash
# 1. 只读四份 xlsx，生成长表和来源哈希；不调大模型
make expert-rules-ingest

# 2. 每条有效评语拆成原子观点；中断后可续跑
make expert-rules-extract

# 3. 生成 rule_candidates.csv、rules_candidate.yaml 和 rule_audit.md
make expert-rules-distill

# 4. 人工把确认的规则改成 approved: true，再冻结进生产 Judge
python -m scripts.build_expert_rules freeze
```

2024 原表实际是每位教师 5 个个人分数。006–009 的备注全部与各自分数配对；
005 只有存在个人备注时才配对。“汇总评语-ZX”只与平均分配对，绝不冒充 005
个人意见。2018/2019 的汇总文字也只与平均分配对。

Judge Prompt 固定包含“不可观察不等于表现差”：因 PPT 画外音、单人微格等形式
看不到学生或教师时，相应二级指标返回 `assessed=false, score=null`，缺失不扣分，
一级维度只根据其余可观察项计算。生产规则从 `expert_rules.yaml` 按维度加载；
候选文件不会自动进入线上评分。

### 每年做什么（复制执行）

先 `conda activate pku2`。`extract` 一条 15–20 分钟课大约要实时的 3～5 倍 ASR，
再加 VLM / Judge，11 人往往要数小时。断了加 `--resume`：已有 `evidence.json`
的人会跳过。

**不要**对本年使用本年刚蒸馏出的 `--lessons` 再打一遍（评语泄漏，对齐虚高）。
**不要**把候选规则手工粘进 `eval_judge.j2`；审核后用 `freeze` 写入独立规则文件。

```bash
# 0. 校验扫描逻辑（不调大模型）
python -m scripts.test_eval_dataset

# 1. 扫描 → dataset/<批次>/{inventory,manifest}.csv
python -m scripts.build_eval_dataset inventory \
  --root "test/2019春微格作业-42人" \
  --xlsx "test/2019春微格作业-42人/微格教学评审意见汇总表-总表（排序）-2019春.xlsx" \
  --out dataset/2019_spring

# 2. 抽证据 + 打分。下一年才带上一年的口径；prompt-version 逐年 +1
python -m scripts.build_eval_dataset extract \
  --manifest dataset/2019_spring/manifest.csv \
  --resume --prompt-version v1 \
  --lessons dataset/2018_spring/lessons_distilled.md

# 3. 对照评语写 lesson，再压成清单（人工看过 md 再给下一年用）
#    改过 eval_reflect.j2 后不要加 --resume，否则沿用旧 json
python -m scripts.build_eval_dataset reflect --dir dataset/2019_spring
python -m scripts.build_eval_dataset distill --dir dataset/2019_spring

# 4. 全部年份结束后：同一版 prompt 只重打分，再出训练表
python -m scripts.build_eval_dataset rejudge --dir dataset/2019_spring \
  --prompt-version vN \
  --lessons dataset/2018_spring/lessons_distilled.md
python -m scripts.build_eval_dataset merge --dir dataset/2019_spring
```

`extract` 默认删掉抽音和关键帧，**转写留在 cache**。原始视频确认不再重抽后
可删 `test/20XX…`（约十几 GB）；不影响以后对本年 `rejudge` / `merge`。
`dataset/20XX_spring/`（含 `lessons_distilled.md` 和 cache）必须留着。

课件：PDF 直接渲染；PPT/PPTX 经 LibreOffice 转 PDF。截断的假 pptx 会改用
同目录 `.ppt`。解析失败按无课件继续，不把整堂课判死。

`reflect` 的 lesson 必须是「下次没有专家评语」仍能执行的祈使句（主缺陷 /
建议项 / 哪一维不该被单项打穿）。含「专家」「对齐专家」「听感」的句子会
写入 `rejected_lesson` 后清空，不进 distill。

### 各年进度

| 批次 | inventory | extract | reflect / distill | 说明 |
| --- | --- | --- | --- | --- |
| `dataset/2018_spring` | 22 人进 manifest | **v4 已齐**；已 merge | 已写出 `lessons_distilled.md` | 冻结口径 `dataset/lessons_frozen.md` |
| `dataset/2019_spring` | 42 人扫描、**11** 人有视频 | **v4 已齐**；已 merge | 已写出 `lessons_distilled.md` | 王长松 `expert_avg=0` 为无效标签，训 GB 自动剔除 |
| `dataset/2022_spring` | 68 人进 manifest | **v4 已齐**；已 merge | 已写出 `lessons_distilled.md` | 备课 17 课件 + 1 教案 |
| `dataset/2024_spring` | 74 人扫描、**3** 人有视频 | **v4 已齐**；已 merge | 已写出 `lessons_distilled.md` | 试讲目前 3 个 mp4 |

```bash
# 2024：先扫平铺目录。没有视频的人记 no_video，不进 extract
python -m scripts.build_eval_dataset inventory \
  --root "test/2024春微格作业-74人" \
  --xlsx "test/2024春微格作业-74人/24春微格试讲评分表.xlsx" \
  --out dataset/2024_spring

python -m scripts.build_eval_dataset extract \
  --manifest dataset/2024_spring/manifest.csv \
  --resume --prompt-version v3 \
  --lessons dataset/2022_spring/lessons_distilled.md
```

```bash
# 2022：先扫平铺目录，再抽证（68 人，ASR 会跑很久；断了加 --resume）
python -m scripts.build_eval_dataset inventory \
  --root "test/2022微格" \
  --xlsx "test/2022微格/2022春微格教学评审结果统计表-三位专家合并版本.xlsx" \
  --out dataset/2022_spring

python -m scripts.build_eval_dataset extract \
  --manifest dataset/2022_spring/manifest.csv \
  --resume --prompt-version v2 \
  --lessons dataset/2019_spring/lessons_distilled.md
```

第一年 extract **不要** `--lessons`。2018 示例：

```bash
python -m scripts.build_eval_dataset extract \
  --manifest dataset/2018_spring/manifest.csv --resume --prompt-version v0
```

`merge` 产出 `training_gb.csv`（**不含评语**，给 GB）/ `training_detail.csv` /
`alignment.csv`（后两张含评语，给人看）。最终训 GB 用冻结 prompt rejudge
之后的那一版。四年口径已人工合并为 `dataset/lessons_frozen.md`（8 条）。

```bash
# 四年都已 v4 后：按年出表，再拼总表
for y in 2018_spring 2019_spring 2022_spring 2024_spring; do
  python -m scripts.build_eval_dataset merge --dir dataset/$y
done
python -m scripts.build_eval_dataset combine \
  --dirs dataset/2018_spring dataset/2019_spring dataset/2022_spring dataset/2024_spring \
  --out dataset
```

训 GB 用 `dataset/training_gb_all.csv`。不要用 `comment`、`expert_avg` 当特征。
2019 王长松均分是 0，属于无效标签，脚本会自动丢掉。

四个对照脚本**共用** `dataset/gb_split.json`：从 2022（68 人）划 20% 作预测集，
2018/2019/2024 以及 2022 剩下的人作训练集。第一次训练写出划分，之后只读不改。
想重划加 `--resplit`（四个脚本要一起加，否则会对不上）。

```bash
make check-gb
make train-gb
```

| 脚本 | 特征 | 任务 | 产出 |
| --- | --- | --- | --- |
| `scripts/train_gb_obj_reg.py` | 客观特征 + 五维 `llm_dim_*` | 回归 0–5 | `models/gb_obj_reg.pkl` |
| `scripts/train_gb_llm_reg.py` | 只有五维 | 回归 0–5 | `models/gb_llm_reg.pkl` |
| `scripts/train_gb_llm_cls5.py` | 只有五维 | 5 分类（step 0.4） | `models/gb_llm_cls5.pkl` |
| `scripts/train_gb_llm_cls8.py` | 只有五维 | 8 分类（step 0.25） | `models/gb_llm_cls8.pkl` |
| `scripts/train_gb_obj_only.py` | 只有 7 组客观特征 | 回归 0–5 | `models/gb_obj_only_reg.pkl` |
| `scripts/train_gb_ind_reg.py` | 只有 `ind_*` 二级分 | 回归 0–5 | `models/gb_ind_reg.pkl` |
| `scripts/train_gb_obj_cls5.py` | 客观特征 + 五维 `llm_dim_*` | 5 分类（step 0.4） | `models/gb_obj_cls5.pkl` |
| `scripts/train_gb_obj_only_cls5.py` | 只有 7 组客观特征 | 5 分类（step 0.4） | `models/gb_obj_only_cls5.pkl` |
| `scripts/train_gb_ind_cls5.py` | 只有 `ind_*` 二级分 | 5 分类（step 0.4） | `models/gb_ind_cls5.pkl` |

`compare_gb` 在同一批人上比 **0–5 分** MAE/RMSE。专家表是满分 4 分、2 分及格，
因此按 `原分÷4×100` 换百分制，再除以 20 得到等值 0–5：2→2.5、3→3.75、4→5。
分类用 2–4 原分划档，再把档中点按同一公式还原。回归直接拟合 0–5，输出截断到 [0, 5]。
对照实验的 pkl 仍 gitignore。线上总分模型例外：`models/live/gb_obj_cls5.pkl`
（四年 v7.1 全量、客观特征+五维 5 分类），`evaluate_session`（视频或讲稿）都读这一份。
换 v7.1 数据或超参后必须 `make train-gb-live`，否则会报「找不到线上 GB 模型」。

> 2026-09-02 注意：下面所有在旧换算 `（均分−2）÷2` 上得到的 MAE、模型和逐人预测
> 均为历史结果，不能再与 Judge 比较，也不能用于当前结论。修正标签后必须重新训练。

2018 两套新 prompt（22 人）**不覆盖**四年划分，另存
`dataset/2018_spring/gb_split.json`：年内 80/20（seed 42），预测集 5 人
（宋晨、王勋、厉行、王菁、杨文云），两套表用同一批人。

```bash
make train-gb-2018
make train-gb-2018-v4
make train-gb-2018-v7-v9
make train-gb-live
```

`make train-gb-2018-v7-v9` 会先按各自缓存重新 merge（补上二级指标列），再在
同一 `gb_split.json` 上训当前六种：五维回归、客观+五维回归、五维 5 分类、
客观+五维 5 分类、只客观 5 分类、只二级指标 5 分类。
逐版预测在 `dataset/2018_spring/{goal_effect_v7_1,v9}/gb_predictions.csv`，
对照总表在 `dataset/2018_spring/v7_1_vs_v9_gb.csv`。下面是修改六路定义前的历史
5 人留出结果（包含五维 8 分类、只客观回归和只二级回归，**不是当前命令的六路口径**）：

| | Judge | 客+五回归 | 五维回归 | 五维5类 | 五维8类 | 只客观 | 只二级 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v7.1 | 0.454 | **0.382** | 0.612 | 0.817 | 0.424 | 0.432 | 0.422 |
| v9 | 0.557 | 0.362 | 0.361 | **0.342** | 0.486 | 0.432 | 0.388 |

只客观两版数字相同，因为客观特征不随 prompt 变。v9 的五维 GB 明显好于 v7.1，
等权 Judge 反而变差（0.454→0.557）；v9 上五维 5 分类仍是六种里最好的，也是线上
正在用的那路。预测集只有 5 人，排序不能外推。

四年齐套（2018/2019/2022/2024 共 104 人，剔除王长松后 103；预测集是 2022 的 14 人）：

```bash
make train-gb-all-v7-v9
```

各年 `cache_v9` / `cache_goal_effect_v7_1` 已齐。脚本按年 merge 再拼总表
（`dataset/all_v9/`、`dataset/all_v7_1/`），划分用 `dataset/gb_split.json`
（若缺失则从 `eval_snapshots/v4/global/gb_split.json` 恢复）。对照总表
`dataset/all_v7_1_vs_v9_gb.csv`。当前六种方法正是：五维回归、客观+五维回归、
五维 5 分类、客观+五维 5 分类、只客观 5 分类、只二级指标 5 分类。本次 14 人留出
（0–5 分 MAE）：

| | Judge | 五维回归 | 客+五回归 | 五维5类 | 客+五5类 | 客观5类 | 二级5类 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v7.1 | 0.716 | 0.495 | 0.528 | 0.622 | **0.473** | **0.473** | **0.473** |
| v9 | 0.640 | 0.423 | 0.417 | 0.420 | **0.348** | 0.473 | 0.455 |

v9 的最佳方案是 **客观特征+五维 5 分类**，MAE 0.348、RMSE 0.414、准确率
0.429；它也优于 v7.1 的全部方案。只客观 5 分类两版完全相同（MAE 0.473），
符合客观特征不随 prompt 变化的预期。v9 在五维回归、客+五回归、五维 5 分类、
客+五 5 分类和二级 5 分类上均优于 v7.1，说明 v9 的评分信息整体更适合后续 GB。
预测集只有 14 人，结论仍需交叉验证。

线上总分用 **v7.1 prompt + 客观特征+五维 5 分类 GB**。`make train-gb-live` 会先在
2022 留出上对照，再把四年 v7.1 有效样本全部拟合到 `models/live/gb_obj_cls5.pkl`。
五维雷达仍走 Judge（`eval_judge.j2` 的 v7.1 口径，含 70 分软地板和教学效果预期效果兜底）；
总分是 5 档中点映回百分制（55 / 65 / 75 / 85 / 95）。结果里 `prompt_version` 为
`v7.1-goal-effect-fallback`。数据集 `rejudge` / `merge` 不走 GB，避免训练表被校准分污染。
v9 对照仍可用 `make train-gb-all-v7-v9`，不改线上模型。

#### v9 四种小样本回归实验

```bash
make train-gb-v9-regression-experiments
```

实验不覆盖原 GB 文件：模型写入 `models/all_v9_regression_experiments/`，结果写入
`dataset/all_v9/regression_experiments/`。固定测试集仍为同一批 2022 留出 14 人；
同时执行 10 次重复 5 折（50 折）和按批次留出验证。

| 方法 | 固定测试 MAE | 固定测试 RMSE | 重复5折 MAE | 重复5折 RMSE |
| --- | ---: | ---: | ---: | ---: |
| 五维 Ridge | 0.3853 | 0.4285 | 0.3389±0.0428 | 0.4226±0.0726 |
| 五维+聚合特征 Huber | 0.3778 | 0.4394 | 0.3582±0.0443 | 0.4379±0.0633 |
| 五维+单调聚合 GAM | **0.3681** | **0.4202** | **0.3366±0.0407** | **0.4190±0.0673** |
| 聚合主干+精选特征残差 GB | 0.3691 | 0.4349 | 0.3639±0.0581 | 0.4508±0.0696 |

单调模型在固定测试和重复 5 折都最好；五维 Ridge 次之且最简单。残差 GB 没有在
交叉验证中带来增益，暂不推荐上线。这里的 GAM 是项目内实现的单调分段加性模型，
不依赖额外第三方库。所有实验产物仅供离线比较，前端和线上模型路径均未修改。

默认 `dataset/2018_spring/cache/` 的 `scores.json` 已被 v5 覆盖，evidence 仍在。
`train-gb-2018-v4` 从 `eval_snapshots/v4/2018_spring/cache` 把 22 份 v4 分数拷到
`cache_v4/`，再 merge 到 `dataset/2018_spring/v4/`。当前 Judge 已是 v7.1 规则，
**不能**再 `--prompt-version v4` 重打还自称 v4。同一 `gb_split.json` 上六种方法
（0–5，n=5）：

| 方法 | MAE | 相对 Judge |
| --- | ---: | ---: |
| Judge 总分 | 0.53 | 基线 |
| 客观特征+五维 回归 | **0.38** | −0.15 |
| 五维 5 分类 | 0.44 | −0.09 |
| **只用二级指标 回归** | **0.44** | −0.09 |
| **只用客观特征 回归** | **0.47** | −0.06 |
| 五维 8 分类 | 0.80 | +0.27 |
| 五维 回归 | 0.84 | +0.31 |

两路新方法都略好于等权 Judge，但都没有超过「客观+五维」。二级指标更看逻辑/完整/
提问；客观特征更看手势、响度波动、换片。样本只有 5 人，不能据此换线上模型。

| 表 | prompt | 预测集 MAE（0–5） |
| --- | --- | --- |
| `fixed_prompt` | v5-rules17 | 历史旧尺度结果，需重训 |
| `effect_inferred` | v6-effect-inferred | 历史旧尺度结果，需重训 |

只靠五维的三种都打不过 Judge（Judge 总分本来就是五维等权平均）。客+五回归两次都
压过 Judge 约 0.21，主要靠音量波动 / 手势 / 换片等客观特征，但预测集只有 5 人：
宋晨（专家 1.12）被拉近，王勋（专家 4.12）被压到 ~1.8，MAE 优势很可能是单点。
v5 有 17/22 人缺「教学效果」，五维 GB 只能中位数填；v6 补齐后 5 分类略好，其余
没有变好。单年 22 条仍不够单独训稳。逐人对照见各自目录的 `gb_predictions.csv`。

另有一个不训练的 LLM 综合总分对照：评分时只读取 v6 五维诊断与客观特征，五人全部
落盘后才加载专家分和 GB 预测，避免标签泄漏。已有结果可用 `--resume` 复用：

```bash
make judge-overall-2018
```

产出位于 `dataset/2018_spring/effect_inferred/llm_overall/`：每人原始判断在 `cache/`，
逐人比较（含专家评语）在 `comparison.csv`，汇总在 `summary.json`。本次 5 人上 LLM 综合总分 MAE
**0.645**、RMSE **0.910**，优于等权 Judge（MAE 1.045）和四种 GB（最佳“客+五回归”
MAE 0.836），但样本极少，且宋晨仍被高估 1.675 分，不能据此直接替换线上总分。

---

## 九、加自己的知识语料

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

## 十、调整评估指标

指标体系有三份文件，职责不同，**改之前先分清要改哪一份**：

| 文件 | 是什么 | 谁读 |
| --- | --- | --- |
| `evaluation_criterion.md` | 需求源头：五维 41 条三级指标的人工定义 | 人 |
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

### 如何调整某项指标的关注重点

不要只改一个数字权重。先确定想改变的是“报告评什么”“什么算要害”“维度如何折算”
还是“最终总分关注什么”，再修改对应入口：

1. **调整报告必须评价的项目**：先在 `evaluation_criterion.md` 增删人工定义，再同步
   `evaluation_rubric.yaml` 的 `indicators`。二级指标的 `key` 会进入 JSON/CSV，发布后尽量
   不重命名；`criteria` 是 Judge 必须逐条对照的三级观察点，`modalities` 决定什么证据
   缺失时该项不可评。只改 Markdown 不会改变运行结果。
2. **调整“要害”与“改进建议”的边界**：修改 `expert_rules.yaml` 中相应规则的
   `minor_when`、`major_when`、`not_observable_when` 和 `scoring_action`。规则只能影响已有
   指标/维度的严重度和折算，不能自动创造一个新的报告指标；需要单独展示时仍要在 rubric
   新增二级指标。
3. **调整维度内部的关注重点**：修改 `eval_judge.j2` 的通用或维度专属指令。正常路径的
   `dimension_score` 由 LLM 按课型和语义综合，二级 `weight` 主要用于 LLM 一级分无效时的
   加权兜底，所以仅把 `weight: 1.0` 改成 `1.5` 不保证正常评分会更关注该项。
4. **调整最终总分的关注重点**：等权总分由一级维度 `weight` 控制；独立 LLM 综合总分则
   由 `eval_overall_judge.j2` 控制。若希望某种单项缺陷不得打穿、多个缺陷可累计，或某项
   成为决定性问题，需要在综合总分 Prompt 中明确写出，不能指望二级权重自动传递语义。

修改后先运行 `make check-features`。历史 `scores.json` 不会自动变化；需要用新的
`--prompt-version` 和 `--output-cache` 重新 `rejudge`，不要覆盖旧缓存，确认效果后再 merge。
例如：

```bash
python -m scripts.build_eval_dataset rejudge \
  --dir dataset/2018_spring \
  --prompt-version v7-goal-clarity \
  --output-cache cache_goal_v7 \
  --resume
```

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
| `slide_sample_interval_sec` | `3.0` | 密集轨抽帧间隔，帧差本身为零 API 成本 |
| `slide_change_threshold` | `0.08` | 框内（或整幅）变化最大的那一格超过此值才算候选。调大 = 少报。候选还需下一采样定住才计入 |
| `slide_roi_enabled` | `true` | 先用 VLM 框出投影/板书再比对框内；关掉或框不到则退回整幅格子 |
| `slide_roi_max_frames` | `2` | 最多看几张关键帧来框（首帧 + 中间帧）。找到投影和板书就停 |
| `courseware_max_pages` | `16` | 教师上传的课件最多渲染多少页送 VLM，超出则均匀抽样 |
| `diarization_enabled` | `false` | 说话人分离，见下 |

`config.yaml` → `asr`：

| 配置项 | 默认 | 说明 |
| --- | --- | --- |
| `punctuate` | `true` | 转写后用 LLM **只补中文标点**，不改字。失败则规则断句。上传讲稿当转写时不走这一步 |

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

## 十一、排错

| 现象 | 原因与处理 |
| --- | --- |
| `No module named 'ctranslate2'` / 装 faster-whisper 失败 | Python 版本太新。必须用 3.11：`conda create -n pku2 python=3.11` |
| `缺少 API Key：请在 .env 中设置 DASHSCOPE_API_KEY` | `cp .env.example .env` 后填 key；确认 `.env` 中 `PKU_MODE=cloud` |
| `未找到 ffmpeg` | `brew install ffmpeg` |
| `Ollama 调用失败` | 确认 `ollama serve` 在跑，且已 `ollama pull qwen2.5:3b` |
| 上传视频后卡在「语音识别」很久 | 首次运行要下载 whisper 权重；且 CPU 转写约为实时的 1/3～1/5。先用几分钟的短视频试 |
| 转写结果是繁体 | 已内置 zhconv 自动转简体。若没转，确认装了 `zhconv` |
| 中文转写几乎没有句号问号 | 默认会在 ASR 后用 LLM 补标点。确认 `asr.punctuate: true`，且云端 Key / 本地 Ollama 可用；失败会走规则断句，仍可能较粗。上传讲稿则跳过 ASR 与补标点 |
| 评估结果里很多指标显示「未评估」 | 对应模态没数据。视觉指标需要 VLM 可用（云端要 key，本地要 `ollama pull qwen2.5vl:7b`） |
| 关键帧下面没有彩色标签，只有一句话 | VLM 没按 JSON 格式回，标签全部归为 `unclear`。本地模型（qwen2.5vl:7b）比云端更容易跑偏，可换云端或看 `frame.description` 里的报错 |
| 客观特征里没有「课件时序特征」这一组 | `slide_detection_enabled` 被关了，或 ffmpeg 解码失败（进度详情里有 warning）。密集抽帧要求视频有可解码的视频流，纯音频文件会失败 |
| 课件切换次数经常为 0 | 旧口径用整帧平均，角落投影会被摊薄。现已先框区域再比对。仍为 0 时可能是投影极暗、VLM 没框到且格子也看不出，或 `slide_detection_enabled` 被关 |
| 课件切换次数明显偏多 | 人刚好停住、镜头晃一下仍可能多记。把 `slide_change_threshold` 从 0.08 往上调（如 0.15）会更保守 |
| 选了视频但没有开始评估 | 上传入口改为先选文件再点「开始评估」，以便同时附上大纲/课件。选完视频后要点按钮 |
| PPT/PPTX 课件没有页面图像 | 本机没有 LibreOffice，无法把幻灯片转成 PDF。请另存为 PDF 再传，或 `brew install --cask libreoffice` |
| `MuPDF error: cannot create appearance stream for Screen annotations` | LibreOffice 把 PPT 里的嵌入媒体转成 PDF Screen 注释，PyMuPDF 画不出来。已跳过注释渲染并关掉这段 stderr，页面图像不受影响 |
| 课件报 `Package not found` / `不是 zip` | 扩展名是 `.pptx` 但文件截断，或其实是旧版 `.ppt`。会改用同目录下完整的 `.ppt`；仍失败则跳过课件、按无课件口径继续评 |
| 2019 inventory 只有约 11 人进 manifest | 42 个教师文件夹里约 30 个是空的（另有一整套 Finder ` (2)` 空副本已跳过）。缺视频记 `no_video`，有打分也不进 extract |
| 2019 王长松 `expert_avg=0` | 0 不是有效专家评分。即使换算后为 0，四个 `train_gb_*` 脚本仍会自动丢掉这一行 |
| `No module named 'sklearn'` / `pandas` | 线上总分和训 GB 都要。`pip install pandas scikit-learn`（已写入 `requirements.txt`，`make install` 会装） |
| `找不到线上 GB 模型` | 还没训线上模型。`make train-gb-live`（读 `dataset/all_v7_1/training_gb.csv`） |
| 2022 备课目录只有十几个文件 | 试讲 68 个视频齐，课件/教案只交了约 18 份。缺课件按无课件继续评，不判死 |
| 2022 楚健春平均分数对不上表内唯一一行 | 合并表里他只有刘树华一行（3.5），「平均分数」却是 3.033。标签用平均分数，并标 `incomplete_experts` |
| 2024 inventory 只有 3 人进 manifest | `2024春微格试讲-74位/` 目前只有张亿、王欢、黄炜三个 mp4，其余 71 人只有备课 PDF，记 `no_video`。补视频后重新 inventory 再 `--resume` extract |
| 2024 表里「分数」和「平均分」不一致 | 「分数」是专家账号 005 的单人分。标签用「平均分」 |
| `reflect` 大量 `empty`、lesson 被拒 | 旧 prompt 会写出「对齐专家」「结合听感」。不要加 `--resume`，直接重跑 `reflect`；含禁词的句子会进 `rejected_lesson` 被清空 |
| 上传大纲后任务直接失败 | 扫描版 PDF 抽不出文字。请改传 Word，或先做 OCR |
| 客观特征里没有「上传课件观测」这一组 | 没传课件，或 VLM 对课件页全部标注失败（进度详情里有 warning） |
| 说话人分离报「需要 HuggingFace token」 | `.env` 里没填 `HF_TOKEN`，或没在模型页面接受使用条款。两者都要做 |
| 说话人分离报「未安装 pyannote.audio」 | `make install-local` |
| 授课内容页语速图 / 提问条裂开或接口 500 | 没装 matplotlib，或 conda 环境不是 `pku2`。`conda activate pku2 && pip install matplotlib`（已写入 `requirements.txt`） |
| 声学特征页等待图写「暂无逐次等待样本」 | 旧任务没存 `wait_samples`。重新评估后才有棒棒糖图；等待质量条会退回「≥3秒 vs 偏短」两段 |
| 声学特征页波形/响度不像真实音轨 | 旧任务没有包络和曲线，页面按响度均值生成示意。新评估会写入 `wave_envelope` / `loudness_curve` / `pitch_curve` |
| 新加的客观特征前端看不到 | 忘了在 `evaluation_rubric.yaml` 的 `objective_features` 里登记标签。跑 `make check-features` 会指出缺哪个 key |
| `make check-features` 报「无未登记的特征 key」失败 | 同上，按提示把 key 加到 rubric 对应分组里 |
| 问答检索不到内容 / 语料库计数为 0 | 没建库。`make ingest`，并确认语料目录里确实有文档 |
| 问答里「历史评估报告」是空的 / 勾不了某次课 | 只有评估**成功完成**才会入库。进行中、失败、取消的不会出现。从评估页删掉任务会同步删向量。点「+」里的「历史评估报告」打开弹窗；切回问答页会刷新列表 |
| `dimension mismatch` 之类的 Chroma 报错 | 换过 embedding 模型。`make ingest-reset` 重建 |
| 打开页面立刻跳到登录 | 正常。先 `make db-up && make db-migrate`，再注册或用 `create_admin` 创建的账号登录 |
| 登录后历史是空的 | 新 PostgreSQL 默认是空库。旧 SQLite 不会自动导入 |
| 接口 401 /「请先登录」 | Session Cookie 失效或被撤销。重新登录；下载和图表走同源 Cookie，不必再拼 token |
| 注册报「工号已被使用」 | 工号规范化后全局唯一。换工号，或直接登录 |
| 后端启动报数据库连接失败 | PostgreSQL 没起来，或 `DATABASE_URL` 不对。`make db-up` 后重试 |
| `make db-up` 报 Docker daemon | 正常。这台机器用的是 Homebrew Postgres，不需要 Docker。直接再跑一次 `make db-up`（已改为自动复用本机 5432） |
| `/admin` 进不去 | 当前账号不是 `role=admin` 且 `status=active`。用 `python -m scripts.create_admin` |
| 前端起来了但数据全空 | 后端没启动或端口不是 8010。检查 `make backend`，代理配置在 `frontend/vite.config.js` |
| 端口被占用 | `lsof -ti :8010 \| xargs kill -9` |
| 扫描版 PDF 解析为空 | 目前不带 OCR。先用其他工具转成文字版 |
| 中文 PDF「原始大纲」乱码 | 已用 PyMuPDF 多后端解析；仍失败则改传 docx |
| 大纲 / 评估报告 PDF、Word 导出失败 | 需安装 `pandoc` 或 LibreOffice：`brew install pandoc` 或 `brew install --cask libreoffice` |
| 旧版 `.doc` 无法解析 | macOS 会尝试用 textutil；失败的话在 Word 里另存为 .docx |
| 大纲校验失败但未自动修复 | 自修采用**黑名单制**：除 `source_id 覆盖或顺序错误` 等少数项外，默认会自修（最多 2 次）。看进度是否出现「自动修复」及 `repair_attempts` 标签 |
| 大纲校验「章节学时合计与总学时不一致」 | 重启后端后应触发自修；若 2 次仍失败，可能是原文学时数据不完整，模型无法可靠配平 |
| 大纲固定框架 XML 报 `activity type 不在允许枚举中` | 模型用了「案例教学」「研讨」等；校验前会自动映射为标准 type，无法识别则写「其他」。**重启后端**后重试 |
| 大纲固定框架 XML 报 `assessment/item type 不在允许枚举中` | 模型用了「期末考试」「平时成绩」等同义词；已自动映射为标准 type。**重启后端**后重试；仍失败可看报错里的「当前为 …」对照允许列表 |
| 大纲上传 Word/PDF 后报 `KeyError: 'source_text'` | 异步 worker 未读到 `source_path`（已在 2026-08-18 修复）。**重启后端**后再试；仍失败则确认 `data/` 下上传文件存在 |
| 运行大纲校验测试时报 `No module named 'lxml'` | 使用了系统 Python。先执行 `conda activate pku2`，再运行 `make check-syllabus` |

---

## 十二、待解决的问题

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
| **尚未接北大统一身份认证** | 已有 provider 接口、回调路由和 mock 测试；没有官方文档前不写伪生产代码 | 拿到官方协议后再只改 `PKUSSOAuthProvider` |

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
| **无可读预览** | 页面已默认出 Markdown 预览；旧 XML 任务仍是标签原文 | 旧 XML 记录可做树形/表单预览，或提示导出 Markdown |
| **对比无 diff 高亮** | 左右对照需人工找改动 | 章节级 diff 高亮；improvements 与 diff 联动跳转 |
| **历史无版本对比** | 只能打开单条记录，无法看两次优化差异 | 同一课程多次优化做 version diff |
| **异步改造前的旧记录不在侧栏** | 2026-08-18 之前只写入 `syllabus_records`、没有对应 `syllabus_tasks` 的记录，新侧栏看不到 | 需要时把无 task 的 record 合成已完成条目；`GET /api/syllabus/history` 仍可查 |

---

### 暂缓项（视频评估 / 全局）

以下不影响当前问答、大纲优化迭代，需要时再排期。

下表的视频评估各项已在 `evaluation_design.md` 里逐条展开（含做法、成本与实施顺序），
这里只留索引。

| 分类 | 问题 | 备注 |
| --- | --- | --- |
| 视频评估 | 线上总分已接四年 v7.1 客+五 5 分类 GB；2022 留出仅 14 人 | 全量拟合不能当泛化；换年或加样本后应 `make train-gb-live` 重训 |
| 视频评估 | 2018 两套旧 prompt 上只有客+五回归压过 Judge，预测集仅 5 人 | 历史对照，不再接线上 |
| 视频评估 | 2018 v4 上「只客观 / 只二级」略好于 Judge，仍不如客+五回归 | 同一 5 人测试集；默认 cache 的 v4 分已被 v5 覆盖，训练用的是快照恢复 |
| 视频评估 | 一级维度分由 LLM 按课型折算，同一视频两次跑可能差几分 | 越界会回退加权平均；要可复现可看 `weighted_score` 字段 |
| 视频评估 | 说话人分离已接入但**未在真实课堂验证过**（缺 HF token，默认关闭） | 剩余 4 条 ❌ 指标里唯一有解的一条，验证后「教学效果」维度才可信 |
| 视频评估 | 课件切换仍非精确页数：框偏了、人走进框内停住、投影极暗时会漏报/多记 | 已先用 VLM 框投影/板书再只比对框内；框不到退回整幅格子 |
| 视频评估 | 「详略结合」缺客观依据 | 可加术语时间轴驻留特征（某术语首次到末次出现跨多少分钟、占多少字） |
| 视频评估 | 提问等待时间的有效样本常只有个位数（受 ASR 片段边界限制） | 开 `word_timestamps=True` 可解，代价是转写慢 20–30% |
| 视频评估 | 「表情自然」「板书重点是否突出」未纳入 VLM 标注 | 前者受关键帧分辨率限制，后者需理解板书语义 |
| 视频评估 | ASR 置信度是弱代理：混杂录音质量与口音，**换 whisper 模型后历史数据不可比** | 已在提示词里标明局限，无更好的本地替代 |
| 视频评估 | CPU 转写慢、长视频证据截断 | 暂缓，不阻塞问答/大纲 |
| 全局 | 北大 SSO 只完成适配层和 mock，未接真实官方协议 | 接入时只改 `backend/app/auth/pku_sso.py` 与环境变量 |
| 全局 | Evaluation 页 bundle 过大 | 与当前聚焦无关 |

---

## 十三、变更记录

倒序排列，最新在最上面。每条写清楚**为什么这么改**。

### 2026-09-08 · 内测用公网 IP 上 HTTPS，不迁历史数据

**问题**：内测没有域名，又不能把 `APP_ENV=production` 的 Secure Cookie 配在裸 HTTP 上。
**思路**：Caddy 2.11 用 Let's Encrypt `shortlived` 给固定公网 IP 签证书；Docker 在服务器上建空库和空向量索引，不拷本机任务。评估默认并发 1，避免 2 核机器被多个 Whisper 打满。
**影响**：`DEPLOYMENT.md`、`compose.production.yml`、`deploy/Caddyfile`、`EVALUATION_MAX_CONCURRENCY`。

### 2026-09-08 · 顶栏「我的」旁不再显示姓名

**问题**：标签页右侧再写一遍姓名，和「我的」重复，也占位置。
**思路**：顶栏只保留入口和退出；姓名在资料页看。管理员仍显示「后台」。
**影响**：`Layout.vue`。

### 2026-09-08 · 注册「显示名称」改成「姓名」

**问题**：注册写「显示名称」，资料页写「姓名」，同一字段两套叫法。
**思路**：注册标签和缺填提示改成姓名，与「我的」对齐。接口仍是 `display_name`。
**影响**：`Login.vue`。

### 2026-09-08 · 登录账号改回「工号」

**问题**：登录/注册写的是「用户名」，「我的」里又有一个可改的工号，教师会当成两个东西；工号保存接口其实已经丢掉这个字段。
**思路**：本地登录标识对教师就是工号。登录和注册标签改成工号；资料页工号只读，显示登录账号。新注册把 `staff_id` 写成同一值，避免后台出现两套工号。
**影响**：`Login.vue`、`Profile.vue`、`Users.vue`、`auth.py`、`local.py`、`security.py`、`create_admin.py`。已有账号仍用原来的登录名，只是页面改叫工号。

### 2026-09-08 · 勾选的评估报告单独进 prompt，不跟检索抢字数

**问题**：勾选后虽会取出报告，但和沙龙检索挤在 6000 字里，第三份起会被截掉；规划模型也不知道报告已经带入，还在关键字里猜「评估报告」。
**思路**：指定报告用 `pinned_eval_max_chars=12000` 单独额度，整份诊断（总分、五维、正文）放进「教师指定的课堂评估报告」；公开库仍用 6000 字检索作补充。规划提示词写明报告已带入，不必再为库名生成检索词。
**影响**：`config.yaml`、`retriever.py`、`qa_answer.j2`、`qa_keywords.j2`。需重启后端。勾几份就带几份，太多时按额度从前往后截。

### 2026-09-08 · 勾选的历史评估改为直接带入提示词

**问题**：勾选只缩小 `eval_reports` 的向量检索范围。报告正文和「参与度」等问法相似度常低于 0.5，沙龙语料反而进了上下文，回答变成通用策略，检索条里「历史评估报告」也看不出是否用上。
**思路**：勾选的任务从数据库取出总分、五维和诊断报告，作为【指定评估】固定放进 prompt 最前面；公开语料仍按相似度检索作补充。不再用报告块去过 0.5 阈值。
**影响**：`qa.py`、`pipeline.py`、`qa_answer.j2`、`QA.vue`。需重启后端。来源里会标「指定带入」。

### 2026-09-08 · 多个问答会话可以同时思考

**问题**：后端每个提问已经是独立后台任务，前端却用全局 `sending` 锁发送按钮。一个对话在生成时，新开对话也问不了，看起来像不支持并行。
**思路**：按会话记生成任务。发送按钮只看「当前打开的会话是否在思考」；切走后 SSE 仍写回那个会话的消息列表，侧栏各自标「思考中」。
**影响**：`qaStore.js`。刷新后仍靠轮询收尾；同一会话不能连发两条。

### 2026-09-08 · 问答提示词标明历史评估是自己的课

**问题**：勾选了历史评估报告，模型仍说「无法直接观摩您的课堂」。提示词没说明这些块是该教师自己的诊断报告，模型当成没有听过课的通用助教。
**思路**：`qa_answer.j2` 写明「历史评估报告 / 教学视频评估报告」是本系统对该教师课堂录像的诊断，问自己的课必须依据报告分析，禁止那句客套。规划提示词在「我的课 / 课堂质量」类问题上加一条能对上报告的检索短语。
**影响**：改的是 Jinja 模板，下次提问即可；报告没检索到时仍走通用建议。

### 2026-09-08 · 去掉检索说明和顶栏英文副标题

**问题**：检索范围弹层里的操作说明占地方；顶栏「北大问教」旁的 `PKU-AskEdu 2.0` 对教师也没有用。
**思路**：说明文案删掉，任务入口本身已写「点击选择任务」。顶栏只留中文品牌名。
**影响**：`QA.vue`、`Layout.vue`。登录页英文副标题未改。

### 2026-09-08 · 历史评估改弹窗勾选，默认不检索

**问题**：嵌在「+」菜单里的任务列表太挤，而且默认把全部历史评估勾上，一提问就会把几次课混在一起。
**思路**：公开语料库仍默认全选；历史评估报告单独一行，点开弹窗再选。弹窗里滚动列表，有全选和清除，点确定才写入检索范围。
**影响**：`QA.vue`、`qaStore.js`。没选任务时不查 `eval_reports`。

### 2026-09-08 · 问答可勾选某一次历史评估

**问题**：评估完成后报告会进 `eval_reports`，问答却只能整库混搜，不能指定「就问这一堂课」。
用户也不清楚这份语料和评估页任务列表是不是同一批数据。
**思路**：完成评估仍按 `task_id` 写入（先删后写，避免同一任务留下旧块）；删除任务继续清向量。
问答「+」里点「历史评估报告」打开任务弹窗，请求带 `eval_task_ids`。
检索用 Chroma `user_id` + `task_id ∈ …` 过滤，别人的任务 ID 会被丢掉。
**影响**：`retriever.py` / `qa.py` / `QAForm` / `QA.vue`。切回问答页会刷新列表。
失败、取消、进行中的任务不入库，也不会出现在勾选里。

### 2026-09-08 · 侧面走动不再算成看屏幕

**问题**：教师左右走动时的侧面中间态，VLM 常标成 `gaze=screen`。这其实是面向教室的互动站位，却把「看屏幕」占比抬高，教态被说成读屏。
**思路**：观测提示词写明：横移、侧身、脸朝教室或镜头 → 看学生；只有头明确转向投影才算看屏幕；后背正对教室才算背对。解析时再兜一层：走动中且未指向屏幕的 `screen` 改记为 `students`。指向屏幕的走动仍算看屏幕。
**影响**：`eval_vision.j2`、`vision.py`、`eval_judge.j2`。已完成的评估要重跑，旧关键帧标签不会改。

### 2026-09-08 · Whisper 转写后用 LLM 补中文标点

**问题**：faster-whisper 转英文常带 `. ?`，转中文几乎不断句。切句、问句统计和「片段末尾提问后的等待时间」都对不齐。Atmos 也是 Whisper，标点靠转写后的 LLM 补。
**思路**：ASR 仍用本地 Whisper；中文墙字再送给现成 LLM，只补 `。，、？！`，不改字。按片段编号批量回写，时间戳不动。行数对不上或改写了汉字则丢弃，改走规则断句，评估不中断。上传讲稿不走 ASR，也就不补。
**影响**：`transcript_punc.py`；`asr.punctuate` 默认为 true。每堂课多几次短 LLM 调用。沙龙转写同样补。已完成的评估要重跑才有标点。

### 2026-09-07 · 课件切换先框投影/板书，再只看框内变化

**问题**：整幅格子能抓住角落投影，但教师走动、旁边黑板、灯光仍会进格子；用户希望
先框出投影/板书，再判断那一块变化够不够明显。
**思路**：评估时额外用 1～2 张关键帧（首帧，必要时加中间帧）让 VLM 给出投影和
板书的 0～1 框。密集轨只在框内做格子帧差；投影和板书分开框，避免把中间的人算进去。
框不到、VLM 关掉或几乎整幅都是录屏时，退回原来的整幅格子。
**影响**：新增 `eval_screen_roi.j2`、`locate_content_rois`；每条视频大约多 1～2 次
VLM 调用。`slide_roi_enabled` 可关。Judge / 前端会标明是否用了框。已完成的评估
要重跑才会变。

### 2026-09-07 · 课件切换改成格子帧差，避免角落投影记成 0 次

**问题**：切换次数不是 LLM 看的，而是整幅 160×90 灰度帧的平均像素差。非纯 PPT
录像里投影只占画面一角，翻页贡献被墙和人摊薄，经常低于 0.08，整节课记成 0 次；
Judge 再把「几乎不换页」当事实写进报告。
**思路**：改看 8×5 格子里变化最大的那一格；候选还要等下一采样该格定住才计入
（翻页后画面会停，走动则下一拍仍在变）。不增加 API，也不用先框屏幕。
**影响**：`slide_features.py`；`eval_judge.j2` / 前端不再把次数写成「上界」。
`make check-features` 增加角落小色块能检出、移动色块不记翻页两条。旧评估和线上
GB 用的是整帧平均口径，新跑的 `slide_change_count` 与历史不可比；若要 GB 对齐需
重提特征再训。

### 2026-09-07 · 智能问答切页后继续生成

**问题**：问答是页内 SSE，切到教学评估 / 大纲优化会拆掉组件；会话又要等整段答完才入库。
思考中的问题和半成品答案都会丢，看起来像不支持后台运行。
**思路**：提问当下落一条 pending 会话；LLM 生成跟 SSE 连接脱钩，客户端走了也跑完再写入。
前端把对话状态放到 `qaStore`，并用 `keep-alive` 保住问答页。回来接着看；刷新则打开上次会话，
若仍 pending 就轮询。侧栏对生成中的会话显示「思考中」。
**影响**：`qa.py`、`db.py`、`qaStore.js`、`QA.vue`、`Layout.vue`。评估 / 大纲任务本来就是 worker 后台跑，行为不变。

### 2026-09-07 · 结果页标签拉齐左右

**问题**：综合总览、诊断报告等标签挤在左边，底边和内容区左右不齐。
**思路**：标签均分整行宽度，文字居中，第一项贴左、最后一项贴右。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 客观特征去掉总览标签

**问题**：四个大组已经各自成页，总览 2×2 卡和标签重复，进客观特征还要再点一次。
**思路**：删掉「总览」标签和四张卡。进客观特征默认打开授课内容。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 线上评估改回 v7.1 prompt + 客+五 5 分类 GB

**问题**：前端视频评估走的是 v9 打分口径和四年 v9 训出的 GB。现在要对齐 v7.1：Judge 用 70 分软地板和教学效果预期效果兜底，总分用同一套客观特征+五维 5 分类，但必须在 v7.1 分数上训。
**思路**：`eval_judge.j2` 去掉 v9 的严重度绑分与 90 分示范性证据门槛；生产规则恢复 70 分软地板。`LIVE_PROMPT_VERSION` 改成 `v7.1-goal-effect-fallback`。`make train-gb-live` 改读 `dataset/all_v7_1/training_gb.csv`，重写 `models/live/gb_obj_cls5.pkl`。v9 对照表和 `cache_v9` 保留，不接线上。
**影响**：新评估任务的五维和总分都会变；已完成的旧任务结果不变。缺模型时先跑 `make train-gb-live`。

### 2026-09-07 · 无课件说明并进标题行

**问题**：灰色提示框单独占一行，和上面「已获得 n / 13 项」说的是同一件事。
**思路**：跳过说明接到获得项数后面，去掉灰框。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 有课件时时间轴加大、质量条缩短

**问题**：有课件那一版左边质量条占太宽，时间轴偏小；轴下四个数字挤成一行，不好扫。
**思路**：中栏改成左窄右宽。质量条最多到列宽的 88%。有课件的时间轴加高。轴下四个指标带图标，排成一行。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 工具调度页按有无课件分两套

**问题**：点进「工具调度」仍是课件 / 切换两段比例条，对不上有课件和无课件两张稿。
**思路**：有课件时左边四条质量分布、右边切换时间轴。没课件时提示 7 项已跳过，改成全宽时间轴、分段频次图和停留环图。数字用黑色，明细跟声学页同一套五列表。新评估把 `dwell_samples` 写入 `raw_features.slides`，不进 Judge。
**影响**：`Evaluation.vue`、`slide_features.py`、`tools_charts.py`、图表 API。

### 2026-09-07 · 课堂视觉拉开区块间距

**问题**：四个数字下面的分割线几乎贴着状态分布和结论；指标明细又没有分割线，和上面连在一起。
**思路**：分割线到分布 / 结论留 28px。指标明细上方同样留空并加一条分割线。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 课堂视觉结论改成对号列表

**问题**：「观测结论」标题和三条之间的分割线让右栏像另开了一节，和左边分布条不对齐。
**思路**：去掉标题和分割线。每条左侧放对号图标，直接跟分布条顶对齐。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 课堂视觉去掉标题卡片，明细改成五列表

**问题**：页内再写一遍「课堂视觉」、数字用红色还加竖线，分布和统计又套卡片，和授课内容 / 声学页不一致；横表也不好看明细。
**思路**：标题留给标签栏。四个数字改黑色、去掉竖线。分布和结论不再画框。代表帧统计改成与声学页相同的指标 / 当前值 / 参考范围 / 状态 / 说明；展示用区间不进 Judge，没有区间的标事实观察。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 诊断摘要不再放进诊断报告

**问题**：总览已经有三列摘要卡，诊断报告开头又把「〇、诊断摘要」复述一遍，像两份同一内容。
**思路**：模型仍在同一轮写出摘要短句，解析进 `digest` 后从报告正文剔除。新任务入库就不带这一节；旧任务在报告页和导出时同样去掉。
**影响**：`eval_report.j2`、`pipeline.py`、`evaluation.py` 导出、`Evaluation.vue`。

### 2026-09-07 · 课堂视觉页按稿子重排

**问题**：点进「课堂视觉」仍是通用比例条，对不上稿子里的大号占比、状态分布、观测结论和代表帧表。
**思路**：单独排这一页。四个数字用看学生 / 有手势 / 板书或投影 / 抬头率高。三条分布用现有视觉特征，不另造指标；视线互斥，行为与媒介可重叠。结论按占比规则写，不进 Judge。表默认 8 项，其余展开。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 长停顿与等待样本卡放大靠拢

**问题**：音高图右侧两张观察卡偏小，又被两列均分拉开，看起来空、散。
**思路**：只放大声学页这一对：图标 72px、数字 36px。两卡左右并排、居中，间距 30px；显式 `flex-direction: row`，避免被格子的纵向 flex 竖排。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 提问等待图压到波形同高

**问题**：等待图 PNG 比波形高，网格行被它撑开，左右第一行图对不齐。
**思路**：这一行的高度只由左侧波形决定；等待图绝对定位铺满格子。画幅高度从 1.85 降到 1.45，少留上下空白。
**影响**：`Evaluation.vue`、`audio_charts.py`。

### 2026-09-07 · 声学页左右四行对齐

**问题**：提问等待、分布条、两项观察卡都堆在右栏，和左侧波形 / 响度 / 音高对不齐；平均、中位数还占等待图上方一行。
**思路**：改成四行网格。标题行把平均、中位数放在「提问等待」右侧。等待图与波形同行同高，分布条与响度同行，长停顿 / 等待样本与音高同行。等待 PNG 画幅改成和波形一样。
**影响**：`Evaluation.vue`、`audio_charts.py`。

### 2026-09-07 · 音高图纵轴按峰值撑开

**问题**：音高变化把 Y 轴钉在 80–280 Hz，女声或重音峰值会被裁掉，看起来像线顶到框上。
**思路**：默认仍是 80–280。曲线超出时按最高点上留约 8% 再取整刻度，最低点同理向下扩。
**影响**：`audio_charts.py`。

### 2026-09-07 · 长停顿与等待样本挪到 ASR 分布下

**问题**：没有参考范围的两项还在表格下面，右侧 ASR 分布条底下空着。
**思路**：长停顿次数、等待样本数改放到提问等待栏、ASR 置信度分布下面，表下不再重复。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 响度与音高改成上下排

**问题**：响度、基频并排各占半栏，线挤、刻度看不清。
**思路**：两张图改成和波形同宽、上下各占一行。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 声学页图表拉开间距、补全边距

**问题**：响度/基频挤在波形下面各占半栏，刻度被裁；等待图强制画到 12 秒，样本都在 0 附近时上半空白很大，和左侧也不齐。
**思路**：响度、基频改成与波形同宽竖排。三张音轨图加高一点，长停顿标签画进图内。等待纵轴按数据收，至少留到 7 秒好看见 3–6 秒绿带。分布条贴紧图下。
**影响**：`audio_charts.py`、`Evaluation.vue`。

### 2026-09-07 · 声学特征页排版对齐授课内容

**问题**：声学页刚按独立稿做成标题、筛选标签、绿带红点表，和授课内容页（字幕、左右图、五列表、图标卡）不像一套。
**思路**：去掉页内大标题和可判定/观察项切换。图改成与语速/提问条同一套左右栏。表改回指标 / 当前值 / 参考范围 / 状态 / 说明；没有区间的项仍用图标卡。波形和等待图保留。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 声学特征页改成稿子里的图+表

**问题**：点进「声学特征」仍是声学比例条和时序表上下两截，对不上「声学与时序」稿（大号响度/信噪比/等待、波形与基频、等待样本、带区间位置的明细）。
**思路**：该页单独排版。波形、响度、基频、等待样本用 matplotlib 按任务结果现画 PNG。新评估把音轨包络、响度/基频曲线、长停顿时刻和逐次等待写进 `raw_features`，不进 Judge。旧任务没有曲线时按均值示意，没有 `wait_samples` 则等待图留空。可判定项用绿带和红点标位置；长停顿次数、等待样本数只作观察项。展示用参考区间不进 Judge。
**影响**：`Evaluation.vue`、`audio_features.py`、`timeline_features.py`、`ai_engine/evaluation/audio_charts.py`、`GET /api/evaluation/task/{id}/chart/{name}`、`scripts/draw_audio_page.py`。

### 2026-09-07 · 大纲优化页文案改为原文微调 / 重构框架

**问题**：标题说明仍写「结构化的优化版本」，模式名「灵活结构 / 固定框架」也不贴现在的两种做法。
**思路**：说明改为强调融合 AI 辅助教学；页面与结果标签改成「原文微调」「重构框架」。API `prompt_mode` 不变。
**影响**：`Syllabus.vue`。

### 2026-09-07 · 大纲结果的下载与导出合成一个菜单

**问题**：Markdown 结果同时有「下载 Markdown」和「导出」（Word/PDF），两个入口功能重叠。
**思路**：只留「导出」，三项为 Markdown / Word / PDF，都走 `/export`。复制按钮保留。
**影响**：`Syllabus.vue`。

### 2026-09-07 · 大纲优化进度并进文件卡片

**问题**：优化进行中文件卡和「优化进度」卡上下各一块，文件名重复，中间还隔着按钮区。
**思路**：回看或进行中的任务只保留文件卡：文件名下面一条进度条，条下用一行说明当前步骤、完成或失败原因。停止放进卡片标题栏。独立进度卡删掉。
**影响**：`Syllabus.vue`。

### 2026-09-07 · 灵活结构补 Markdown 标题以免校验失败

**问题**：灵活结构要求跟原文体例后，模型常按 Word/PDF 抽出的「课程概述」纯文本输出，没有 `#` 标题，前端报「Markdown 缺少标题结构」且无法导出。
**思路**：提示词写明节名必须译成 `#` / `##` / `###`（这是 Markdown 编码，不是改目录）；生成后若仍无标题，给首行补 `#`，必要时再 LLM 最小修复。正文段落/列表规则不变。
**影响**：`syllabus_optimize_markdown.j2`、`optimizer.py`、`test_syllabus_validation.py`。重启后端后重新优化。

### 2026-09-07 · 灵活结构改为原文修订稿，保留体例与个人表述

**问题**：灵活结构虽要求跟原目录，仍强制「知识内容用要点列表、每点 1 句」，模型会把课程概述里的引语、连贯段落改成标准条目，个人特点被抹掉。
**思路**：灵活入口改成「同一份文档的有限增删」：目录同源、格式跟随原文（段落就段落、列表就列表），题记/引语/寄语必须保留；AI 与目标澄清按该节原有文体嵌入。固定框架仍用标准栏目，不改。
**影响**：`syllabus_optimize_markdown.j2`、`test_syllabus_validation.py`。重启后端后重新优化才会生效。

### 2026-09-07 · Markdown 大纲优化必须融入 AI 且灵活结构跟原目录

**问题**：页面默认走 Markdown 灵活结构，提示词把 AI 辅助教学写成「原文未提则省略」，优化结果几乎不改课程设计；「灵活」也只写了保留章节，模型仍常套成通用栏目模板。
**思路**：两份 Markdown 入口改为必写教师端助教、学生端助学、考核规范，并嵌进教学目标 / 教学安排 / 考核，而不是可删附录。灵活结构把「输出目录 = 原文目录」提到最高优先级，禁止改写成「课程信息 / 第 N 章」。固定框架模板同步把各章教学形式、AI 政策与「AI 辅助教学」节改为必写。
**影响**：`syllabus_optimize_markdown.j2`、`syllabus_optimize_markdown_schema.j2`、`syllabus_markdown_schema.md`、`test_syllabus_validation.py`。重启后端后重新优化才会生效；旧任务仍是旧报告。

### 2026-09-07 · SQLite 导入改为整条拷贝

**问题**：可选导入只 `create_task`，历史评估会变成空的排队任务，结果和大纲任务都丢了。
**思路**：按原 ID 写入状态、进度、结果 JSON 和大纲任务/记录，并挂到指定用户。仍不改 `data/app.db`。
**影响**：`scripts/import_sqlite.py`。本机已把旧记录导入管理员账号。

### 2026-09-07 · db-up 不再强依赖 Docker

**问题**：开发机 Homebrew PostgreSQL 已经在 5432 监听，`make db-up` 却去拉 `postgres:16`，Docker 没开就失败。
**思路**：先探测本机 5432；已经就绪就创建/复用 `pku2` 库，只有端口空闲时才启动 compose。
**影响**：`scripts/ensure_postgres.sh`、`Makefile` 的 `db-up`。

### 2026-09-07 · PostgreSQL 多用户与可切换认证

**问题**：未提交的 SQLite + Bearer 登录只够单机内测，密码和 Session 原文落库，也没有管理员后台、文件隔离和私有向量过滤。后面要接北大统一身份认证，但不能把本地账号自动合并过去。
**思路**：业务状态迁到 PostgreSQL，用户与登录身份分开。两种认证都签发同一套 HttpOnly Session Cookie，数据库只存令牌哈希。本地注册只能得到普通用户；管理员走安全命令或 SSO 白名单。Chroma 的 `eval_reports` 写入和查询都带 `user_id`。原 `data/app.db` 不改不删，导入必须显式指定归属用户。
**影响**：新增 Alembic、`docker-compose.yml`、`/admin`、认证 provider；`db.py` 改为 SQLAlchemy；前端改为 Cookie + `/api/auth/me`。北大 SSO 真实协议仍未接入。

### 2026-09-07 · 指标明细分成可判定与观察性

**问题**：没有参考范围的十项挤成小号数字，看不出「这是事实不是评分」；有区间的项也只靠文字，位置对不上区间。
**思路**：有参考范围的项仍用五列表。没有区间的项不进表，左侧环形图画无提问段落占比，右侧图标数字卡。表上的建议区间仍只给展示，不进 Judge。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 授课内容页去掉文本特征标题

**问题**：上面标签已经是「授课内容」，页内再写「文本特征」重复；提问条偏粗，表下十个数字也贴表格太近。
**思路**：去掉该标题，只留已获得项数。语速折线画矮一档；提问条图不再按自身高度撑开格子，而是在折线图框里 contain 居中。图与指标明细贴紧并加分割线。
**影响**：`Evaluation.vue`、`pace_charts.py`。

### 2026-09-07 · 指标明细只保留有参考范围的行

**问题**：口头禅次数、案例引入、年份引用等没有对照区间，硬塞进表里「参考范围 / 状态 / 说明」三列都是空的，表被拉得很长。
**思路**：只有 PACE_GUIDE 或 rubric `ideal` 的项留在表里。其余用顶部语速/提问那种数字+标签，字号略小、一行五个。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 授课内容与声学特征重新分组

**问题**：时序特征（等待、转写置信）挂在「授课节奏」里，和语速/提问稿不是一类；标签也容易理解成整堂课的快慢，而不是讲了什么。
**思路**：标签改成「授课内容」，只留文本特征。时序并进「声学特征」，总览卡 KPI 跟着走：内容卡看提问结构，声学卡看信噪比/静音和等待。
**影响**：`Evaluation.vue`。

### 2026-09-07 · 最简注册登录，历史数据归到种子账号

**问题**：局域网里谁都能看问答、评估、大纲；「我的」只存在本机 `localStorage`，换设备就丢。后面还要接北大统一身份认证，所以先做最小可用的账号，不要做成以后拆不掉的体系。
**思路**：用工号+密码注册/登录，令牌放 SQLite。业务表加 `user_id`，列表和读写都按当前用户过滤。启动时若没有工号 `2400017801`，写入黄珂凡这个种子账号，并把还没有主人的旧记录挂过去。资料改存服务端；注册只要姓名/工号/院系/邮箱/手机/密码，课程、简介、头像登录后再改。鉴权集中在 `auth.py`，以后换 IAAA 只动这一层。
**影响**：`backend/app/api/auth.py`、`core/auth.py`、`core/security.py`、`core/db.py`、三个业务 API、前端 `Login.vue` / `authStore.js` / 路由守卫。旧的 `profileStore.js` 删除。

### 2026-09-07 · 授课节奏明细改成稿子里的图+表

**问题**：点进「授课节奏」仍是和其他组一样的比例条，对不上文本特征稿（大号语速/提问、语速折线、提问结构条、指标明细表）。页面里手写 SVG 折线也不如出图干净。
**思路**：该页单独排版。语速折线和提问条用 matplotlib 按任务结果现画 PNG；没有音轨采样，点来自分段转写。表上的提问次数、开放性问题等参考范围只给展示，不进 Judge。
**影响**：`Evaluation.vue`、`ai_engine/evaluation/pace_charts.py`、`GET /api/evaluation/task/{id}/chart/{name}`、`scripts/draw_pace_page.py`；需 `matplotlib`。

### 2026-09-07 · 客观特征总览改成四个大组

**问题**：七组来源标签和总览卡的名字对不上，教师要自己把文本/时序、课件/切换拼在一起；卡内图也偏示意。
**思路**：标签改成总览 + 授课节奏 / 声学特征 / 课堂视觉 / 工具调度。卡按稿子做成一整块 2×2：大号主指标、轴上折线/波形/占比条/时间轴、底下一排 KPI。波形没有采样，用声学数字生成；切换时刻写入 `slide_change_times` 供新任务画点。说话人未划进四组，有数据才单独露标签。
**影响**：`Evaluation.vue`、`slide_features.py`、`scripts/draw_feat_overview.py`、`check_features.py`。

### 2026-09-06 · 大纲页去掉粘贴文本

**问题**：上传对齐评估页之后，粘贴框还在文件入口下面，教师实际只传文档，多一个入口容易分心。
**思路**：页面只保留文件上传；粘贴接口仍在后端，需要时可用 curl。
**影响**：`Syllabus.vue`。

### 2026-09-06 · 评估导出补上标题和日期

**问题**：导出的 Markdown / Word / PDF 直接从「一、总体评价」起笔，打开文件看不出是哪堂课、哪天评的、分数多少。
**思路**：导出时在正文前拼一页头（标题、生成日期、综合得分、时长、评估方式、对照材料），三种格式共用；页面展示和库里的 `report` 不动。
**影响**：`evaluation.py` 的 `_build_export_markdown`。

### 2026-09-06 · 大纲页去掉 XML 入口，上传对齐评估页

**问题**：四个模式里两个 XML 对教师没有用，还占选择；上传是旧式卡片+选完即提交，和评估页的拖入/就绪/再开始不一致。
**思路**：页面只留灵活结构、固定框架两个 Markdown 选项。上传改成评估页同款虚线拖入框和文件卡片，选完后点「开始优化」才提交；粘贴文本降为选填。XML 仍走 API，不删后端。
**影响**：`Syllabus.vue`。

### 2026-09-06 · 评估报告可导出 Markdown / Word / PDF

**问题**：结果页「导出报告」只有本地下 Markdown，按钮还是白底红字，和页内主操作不一致；教师也要 Word / PDF。
**思路**：按钮改成红底白字。下拉增加三种格式，走 `GET /api/evaluation/task/{id}/export`，转换直接调用已有的 `export_syllabus`，不另写转换链路。
**影响**：`evaluation.py`、`client.js`、`Evaluation.vue`。Word / PDF 与大纲导出一样依赖 `pandoc` 或 LibreOffice。

### 2026-09-06 · 大纲历史条目去掉摘要行

**问题**：对齐评估页时照搬了「分数 · 等级」那一行，大纲任务显示成课程名/校验结果，像内容介绍，占地方也没必要。
**思路**：已完成条目只留文件名、状态和时间；进行中仍显示步骤进度。
**影响**：`Syllabus.vue`。

### 2026-09-06 · 大纲优化历史任务对齐评估页

**问题**：大纲优化的历史是页面底部表格，和评估/问答的左侧任务列表不像一套产品；进行中的任务也不在历史里，只能看已落库的记录。
**思路**：左侧改成与评估页相同的推开式历史任务（搜索、状态筛选、进行中/今天/更早分组、分割线条目）。数据源从 `syllabus_records` 改为 `syllabus_tasks`，点条目回看进度或结果。补上 `DELETE /api/syllabus/task/{id}`，进行中先停止再删。
**影响**：`Syllabus.vue`、`Layout.vue`（大纲页铺满）、`client.js`、`syllabus.py`、`db.py`。

### 2026-09-06 · 评估完成卡片通栏

**问题**：完成态类名 `ok` 撞上「上传完成」的 `display: inline-flex`，卡片缩成内容宽。
**思路**：完成态改成 `done`，并显式 `width: 100%`，与失败卡同宽。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 评估历史任务可删除

**问题**：问答会话能删，评估历史只能停、不能清掉失败或旧任务。
**思路**：列表条目加垃圾桶图标，确认后调已有 `DELETE /api/evaluation/task/{id}`；进行中的先停止再删。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 客观特征标签与已获得项数同行

**问题**：总览卡上方还有一行灰色说明；「已获得 n 项」单独占右上，和标签错行。
**思路**：去掉说明；项数和「说话人未启用」收到标签行右侧。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 客观特征页去掉「事实层」标题

**问题**：页内再写一遍「客观特征（事实层）」，和上面标签重复。
**思路**：只留来源说明和已获得项数。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 客观特征页改成总览折叠卡

**问题**：七组特征平铺，语速、视线、切换要自己翻表才能形成印象。
**思路**：先总览四张卡（讲授节奏、声音与转写、课堂视觉、课件切换），点标签或
「查看该组特征」再进原来的七组比例条。数据解读用区间和阈值拼短句，不另调模型。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 五维表相对雷达与标签垂直居中

**问题**：表格顶对齐，雷达加标签更高时，表贴在上沿，左右不齐。
**思路**：上排改为 `align-items: center`，表在雷达图+标签的上下边界之间居中。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 总览雷达图略放大

**问题**：雷达画布 300px、半径 58%，五维图偏小，中间总分四周空。
**思路**：高度收到 360px，半径 68%，让图更满。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 总览收紧雷达标签、拉开摘要

**问题**：雷达图底和元信息标签空一截；诊断摘要又贴着上面的表。
**思路**：标签上边距收到 −20px；摘要上边距放到 36px。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 诊断摘要改成红头三列卡片

**问题**：摘要还是普通白卡片，和总览稿里的红底标题栏、分列计数对不上。
**思路**：顶栏校红，左侧标题加「基于五维评估」描边标签，右侧白字进完整报告；
三列用竖线隔开，优点/问题用彩点，建议用红圈序号，并标出条数。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 诊断摘要改由 LLM 直接写两点

**问题**：总览摘要是从长报告里剪句，再短也像缩写，而且和模型本意可能对不齐。
**思路**：`eval_report.j2` 增加「〇、诊断摘要」，每类恰好 2 条、每条不超过 22 字。
后端解析进 `digest`；总览优先用它。v7.1 / v9 没有单独的报告模板，打分后都用这一份。
**影响**：`eval_report.j2`、`pipeline.py`、`Evaluation.vue`。旧任务需重新评估才会出现模型摘要。

### 2026-09-06 · 诊断摘要改成短标题

**问题**：摘要取报告首句并留到 80 字，三列里仍像缩过的正文。
**思路**：有「标题：展开」时只留冒号前；否则取第一分句。每列最多 2 条、每条约 28 字。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 总览去掉指标卡、摘要改三列

**问题**：综合总览下排左边再铺一层二级指标，和上面的五维表、独立「二级指标」页重复；摘要竖着堆，宽了也读不快。
**思路**：总览只留雷达、五维表和诊断摘要；优点 / 问题 / 建议并排三列，明细去二级指标页。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 总览雷达图有时空白

**问题**：点开报告只看到中间总分，五维雷达偶尔不画；切到别的标签再回来，或拉一下窗口又出现。
**思路**：总览是 `v-show`，刚挂上时容器宽度常为 0，ECharts 在空盒子上 init 会留下空白画布。
等量到尺寸再画，并用 ResizeObserver 在格子撑开后补画 / resize。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 诊断报告标签放到第二位

**问题**：诊断报告夹在关键帧和转写中间，总览看完要连点好几下才到正文。
**思路**：有报告时紧挨「综合总览」，后面仍是二级指标、客观特征等。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 诊断摘要被 map 下标截成单字

**问题**：摘要里只剩「教…」「优化…」，卡片再宽也看不成句。
**思路**：`extractMdItems(...).map(briefLine)` 会把下标 0/1/2 当成截断长度。改成
`(t) => briefLine(t)`，并按首句截到约 80 字。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 总览下排与上排对齐

**问题**：二级指标和诊断摘要各占一半，摘要比上面的五维表窄，指标栏又偏宽。
**思路**：下排改成与上排相同的 42 / 58，指标对雷达、摘要对表格。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 总览标签改成红黄绿

**问题**：灰 / 靛蓝和校红不一套，扫一眼分不清。
**思路**：时长黄、评估方式红、模态与已用材料绿。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 总览标签去掉 GB / Judge / 未评估

**问题**：雷达下把校准方法和未评估项也做成标签，教师用不上，颜色还和材料标签抢视线。
**思路**：只留时长、评估方式、模态，以及讲稿 / 大纲 / 课件是否用上。前三项用灰 / 校红 / 靛蓝，材料三项统一绿。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 总览雷达与五维表去掉卡片框

**问题**：雷达图和维度表各套一层灰边卡片，和下面的摘要块叠在一起显得碎。
**思路**：只去掉这两块外框和内边距，下面的二级指标 / 诊断摘要卡片保留。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 雷达图下标签居中并收紧间距

**问题**：标签左对齐，和雷达图之间空出一截。
**思路**：整行居中；上边距收到 −8px，贴着雷达图底。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 雷达图下标签按字长着色

**问题**：元信息被塞进三列等宽灰卡片，「视频评估」和「已对照上传课件」一样大，看起来空、也分不清种类。
**思路**：改成按文字缩的胶囊标签；时长、来源、模态、讲稿/大纲/课件、GB、Judge、未评估各用一色。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 客观特征加上比例条

**问题**：客观特征页只有「标签 + 数字」，占比高低、语速是否落在理想区间要靠心算。
**思路**：每项下面加一条比例条。`%` 按 0–100 铺；其余按单位刻度。rubric 的
`ideal` 画成浅绿色框，落入/偏离用绿黄红区分。旧任务结果没有 `ideal` 字段时，
前端用与 yaml 对齐的兜底表。
**影响**：`Evaluation.vue`；`pipeline.py` 的特征行多带 `ideal`。

### 2026-09-06 · 点历史任务回看上传材料与状态

**问题**：只有新上传时右侧才有文件卡片；点进行中、失败或已完成任务时工作区是空的。
**思路**：任务接口带上材料文件名；点进任务后右侧还原视频 / 课件 / 大纲 / 讲稿，
并按状态显示「解析中」进度条、「评估已完成」或「解析失败」。
**影响**：`Evaluation.vue`、`db.py`（`materials`）、`GET /api/evaluation/task/{id}/file/{kind}`。

### 2026-09-06 · 诊断摘要恢复成可读短句

**问题**：摘要列表用了 `-webkit-box` 限行，格子里被挤成「教…」「语…」，看不出原句。
**思路**：列表按正常换行；每条取完整首句（约 42 字），丢掉只有省略号的碎片。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 总览诊断摘要改为短句

**问题**：摘要把报告里整段优点/问题和二级指标依据原样贴上去，看起来比「诊断报告」还长。
**思路**：摘要只留每条第一句并截到约 36 字；缺报告时用指标名、主问题短句兜底。展开细节去诊断报告页。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 评估报告页按总览稿改版

**问题**：报告是一长列分块，和总览设计稿对不上，二级指标、课件、转写也堆在同一页。
**思路**：改成标题栏 + 标签页。综合总览放雷达、元信息、五维表、指标摘要和诊断摘要；
二级指标、客观特征、课件观测、关键帧、诊断报告、转写仍用现有数据，有内容才出入口。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 三个选填入口降低高度

**问题**：课件 / 大纲 / 讲稿虚线框固定 220px 高，比内容高出一截。
**思路**：去掉固定最小高度，下边距与视频框相同（28px），避免再被压得过扁。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 课件文件夹图标补白线

**问题**：课件换成实心文件夹后没有内部线条，和大纲、讲稿的实心+留白不统一。
**思路**：按原来 Folder 的折页凹槽加一道白线，不再加内容条。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 三个选填入口改为拖入选择

**问题**：只有视频能拖入，课件 / 大纲 / 讲稿还是「选择文件」按钮；课件和大纲图标也相同。
**思路**：三个选填入口改成和视频一样的虚线拖入区。课件换成文件夹图标。「清空」恢复白底灰框，避免和主操作抢视觉。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 按原 Document / Notebook 线稿重画实心图标

**问题**：自绘实心块加细白线，和最初那套文件 / 笔记本图标对不上，也难看。
**思路**：沿用 Element Plus `Document`、`Notebook` 的折角、三道横线和侧页签坐标，外轮廓改实心，内部细节留白。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 课件大纲讲稿改用实心图标

**问题**：Element Plus 的文件夹 / 文档图标是描边路径，换成 `FolderOpened` 等之后看起来仍是空心。
**思路**：这三个入口不用组件库描边图标，改成实心剪影 SVG，和视频的 `VideoCameraFilled` 一致。
**影响**：`Evaluation.vue`。

### 2026-09-06 · 评估页右侧按钮与图标改实心红

**问题**：右侧「重新评估」「选择文件」「清空」是白底红框，上传区图标也是空心描边，看起来像未完成稿。
**思路**：这些按钮改成红底白字；视频 / 课件 / 大纲 / 讲稿改用实心图标，不再套底框。
**影响**：`Evaluation.vue`。

### 2026-09-04 · 评估工作区固定宽度居中

**问题**：右侧上传区随侧栏开合拉满整栏，左右贴边，历史关掉后表单还会再变宽。
**思路**：工作区设最大宽度并水平居中，加大左右留白；侧栏开关只改两侧空白，中间表单宽度不变。
**影响**：`Evaluation.vue`。

### 2026-09-04 · 问答历史去掉筛选标签

**问题**：全部 / 置顶 / 最近三个标签和下面的分组标题重复，侧栏显得挤。
**思路**：只保留搜索和「新对话」，列表仍按置顶、最近分组。
**影响**：`QA.vue`。

### 2026-09-04 · 问答历史列表对齐评估页

**问题**：问答侧栏和评估的历史任务列表不像一套产品：没有搜索、筛选，条目也不是分割线列表。
**思路**：问答改成同一套结构——搜索、「新对话」、全部 / 置顶 / 最近。分组只保留「置顶」和「最近」。
**影响**：`QA.vue`。

### 2026-09-04 · 选中材料后显示完成态卡片

**问题**：文件选中后只改一行文件名，看不出体积、时长，也无法预览或单独更换。
**思路**：选中后换成设计稿的完成态——视频有封面、时长、分辨率和进度条，三个选填
入口显示类型标、大小、上传完成，以及更换/删除。有视频时出现 8–15 分钟耗时说明。
**影响**：`Evaluation.vue`。

### 2026-09-04 · 评估上传区对齐设计稿

**问题**：讲稿还留着粘贴框，「发起新的评估」和底部分割线占地方；三个选填入口
按钮样式和位置跟稿不一致。
**思路**：讲稿只保留选文件。去掉小节标题。清空/开始上移到材料下方，已选数量
放到按钮左侧，不要底部分割线。视频虚线通栏，「点击选择」用北大红；三个选填
入口实线卡片、通栏描边红按钮。
**影响**：`Evaluation.vue`。

### 2026-09-04 · 评估页按工作区稿改版

**问题**：四个入口同等大小，历史列表不好搜、不好按状态筛；评估一结束就跳进长报告，
和「先确认完成、再看结果」的工作流不一致。
**思路**：左侧改成历史任务（搜索、筛选、时间分组、分割线条目）。右侧标题区下面，
视频通栏必填，课件/大纲/讲稿三列选填，底栏计数后开始。只有任务完成后才出现
「教学评估已完成」条，点查看才进结果页。
**影响**：`Evaluation.vue`。

### 2026-09-04 · 问答和评估默认打开历史列表

**问题**：历史侧栏默认收起，进页后看不到会话/任务，多点一次才能对照着聊或选记录。
**思路**：智能问答和教学评估进入时侧栏就是展开的，仍可点收起。交互还是推开式，不是浮层。
**影响**：`QA.vue`、`Evaluation.vue`。

### 2026-09-04 · 评估视频必填、讲稿选填

**问题**：四个入口刚改成「视频或讲稿其一」，课堂评估却必须以录像为准，
讲稿只能补充转写，不能单独提交。
**思路**：视频改回必填；讲稿与课件、大纲一样选填。有讲稿仍跳过 ASR。
**影响**：`Evaluation.vue`、`POST /api/evaluation/upload_video`。

### 2026-09-04 · 评估改为视频 / 课件 / 大纲 / 讲稿四个入口

**问题**：转写快评是第二条独立提交通道，和视频上传抢入口；讲稿其实就是转写，
却不能和课件、大纲一起走同一条任务。
**思路**：去掉「转写文本快速评估」。右侧四个并列入口，至少视频或讲稿其一。
讲稿（文件或粘贴）在后端对应转写：有则跳过 ASR；无视频时只评讲稿和文档。
**影响**：`Evaluation.vue`、`upload_video` 视频改为选填并接收 `transcript` /
`transcript_text`；`evaluate_session`；`eval_tasks` 新列 `transcript` /
`transcript_path`。重启后端才会补列。

### 2026-09-04 · 评估历史可展开，右侧去卡片铺满

**问题**：评估页左栏常驻占位，右侧结果还套在卡片里，和智能问答的「点图标再展开、内容铺满」不一致。
**思路**：历史列表改成与问答相同的推开式侧栏——收起时只留左上角历史 / 新建图标，展开后这两个图标隐藏，面板里有新建和收起。右侧取消 `el-card`，改成分割线分块，内容铺满整栏。
**影响**：`Evaluation.vue`；用法说明同步。

### 2026-09-04 · 评估页改为左历史、右上传

**问题**：上传、任务、转写快评都挤在左栏，历史记录不好扫，右侧空欢迎页占地方。
**思路**：左侧只留历史评估列表（新建 / 刷新）；右侧默认是视频、大纲、课件上传和转写快评。
点已完成任务看结果，点「新建」回到上传。
**影响**：`Evaluation.vue`；用法说明同步。

### 2026-09-04 · v9 四种小样本回归实验

**目的**：验证比原始 GB 回归更适合 103 条小样本的方案，并显式表达“一个维度偏弱”
与“多个维度偏弱”的差异。
**实现**：新增五维 Ridge、五维加聚合特征 Huber、单调分段加性模型，以及聚合主干
加限幅残差 GB。沿用 89/14 固定划分，并补充 10 次重复 5 折和按批次留出验证。
**结果**：单调模型固定测试 MAE 0.3681、重复 5 折 MAE 0.3366±0.0407，两项均为
四种新回归中最好；残差 GB 在重复 5 折上退化到 0.3639，暂不采用。
**隔离**：新模型在 `models/all_v9_regression_experiments/`，结果在
`dataset/all_v9/regression_experiments/`；未删除原模型，未改前端或线上模型路径。

### 2026-09-04 · 四年 v7.1 / v9 六种 GB 对照

**问题**：上一轮只在 2018 的 5 人留出上比六种 GB，样本太少，而且其他年份其实
已经有 `cache_v9` / `cache_goal_effect_v7_1`，没有用上。
**思路**：四年都按对应缓存 merge，拼成 `dataset/all_v9` 与 `dataset/all_v7_1`
（batch 用年份名），沿用 2022 留出 14 人的 `gb_split.json`。缺划分文件时从
v4 全局快照恢复，不重划。
**结果**：有效 103 人（王长松无效标签剔除）。按新指定六种方法重训后，v9 的
客观特征+五维 5 分类最好：MAE 0.348、RMSE 0.414、Acc 0.429；v7.1 最好 MAE
0.473。v9 在除纯客观特征外的五条路上都优于 v7.1；纯客观特征两版同为 0.473，
符合预期。v9 Judge MAE 0.640，v7.1 Judge MAE 0.716。未改线上模型。
**影响**：新增 `obj_cls5`、`obj_only_cls5`、`ind_cls5` 三个变体及三个命令入口；
`scripts/train_gb_all_v7_v9.py` 的六路定义改为本轮指定口径；更新
`dataset/all_v7_1/`、`dataset/all_v9/`、`dataset/all_v7_1_vs_v9_gb.csv` 和两版
`models/all_*` 模型。网络失败缓存已补跑，旧失败文件保留为
`scores.invalid_before_six_models.json`。

### 2026-09-04 · 2018 v7.1 / v9 六种 GB 对照

**问题**：v9 只训过五维 5 分类，v7.1 只训过原来四路，看不出换口径后「只客观 /
只二级 / 五维回归」相对 Judge 有没有跟上。旧 `training_gb.csv` 还缺 `ind_*`，
二级回归根本跑不了。
**思路**：按 `cache_goal_effect_v7_1` / `cache_v9` 重新 merge，补上二级分，再在
同一年内划分上训六种。对照脚本一次跑完两套，避免手改 Makefile 漏路。
**结果**：v7.1 仍是客+五回归最好（MAE 0.382，压过 Judge 0.454）；v9 六种都压过
自己的 Judge，最好是五维 5 分类 0.342。v9 等权 Judge 比 v7.1 差（0.557 vs 0.454），
但五维 GB 从 0.6–0.8 掉到 0.34–0.36，说明 v9 一级分更适合当 GB 特征。只客观两版
都是 0.432。样本仍是 5 人，不改线上模型。
**影响**：`scripts/train_gb_2018_v7_v9.py`，`make train-gb-2018-v7-v9`；v9 / v7.1
的 `training_gb.csv` 现含二级指标。线上仍用全量 v9 五维 5 分类。

### 2026-09-03 · 回答按行揭示，思考中带动画

**问题**：模型有时一整段才推过来，页面像突然贴上全文；检索规划阶段只有光标，看不出在想。
**思路**：完整行进队列再逐行刷到页面（当前未写完的一行仍即时显示）。规划/检索还没字时，
光标前显示动态「思考中...」。
**影响**：只改 `QA.vue`。流式协议不变。

### 2026-09-03 · 历史会话分成置顶 / 最近

**问题**：置顶和普通会话混在一列里，钉上去的条目不够显眼。
**思路**：侧栏改成「置顶」「最近」两级。有置顶才显示第一组；标题左侧加北大红竖条，
置顶组用红圆点，当前会话用浅红底。
**影响**：只改 `QA.vue`。

### 2026-09-03 · 会话支持重命名、置顶和「…」菜单

**问题**：历史条目只有悬停删除，没法改名或钉在上面；当前对话标题也没有同一套操作。
**思路**：每条历史和当前标题右侧加「…」菜单（重命名 / 置顶 / 删除）。置顶用 `qa_sessions.pinned`
列，列表先钉后按更新时间排。未落库的「新对话」不显示菜单。标题栏不加分割线，「…」一律右对齐。
**影响**：`db.py` 迁移 + `PATCH /api/qa/session/{id}`；`QA.vue`、`client.js`。后端需重启以补列。

### 2026-09-03 · 历史侧栏标题放大，会话名靠左

**问题**：「历史会话」在窄侧栏里偏小；当前对话名居中，侧栏打开后视觉锚点不稳。
**思路**：侧栏标题改为 28px。顶栏会话名改为左对齐、垂直居中。每条历史名称前加小聊天气泡，
并略增字距。
**影响**：只改 `QA.vue`。

### 2026-09-03 · 历史打开后收起顶栏按钮；检索默认全选

**问题**：侧栏已有新对话和收起，顶栏还留着同一组按钮。检索范围空着表示「全库」，
点开「+」却看不到勾选，和「默认全选」的直觉相反。
**思路**：侧栏打开时隐藏顶栏的历史/新对话按钮。语料列表加载后把有文档的库全部勾上；
取消勾选才排除。空列表发给后端表示不检索（`None` 仍是全库，给脚本用）。
**影响**：`QA.vue`、`stream.js`、`pipeline.py` 的 `_resolve_corpora`、`schemas.py`。

### 2026-09-03 · 问答历史改推开布局，检索范围放进「+」

**问题**：历史会话用遮罩盖住对话，打开后没法边看历史边聊；语料勾选常驻输入框上方，占地方。
**思路**：侧栏改为占位推开，对话区在剩余宽度里重新居中。输入框左侧加「+」，检索范围放进
弹出菜单，勾选后按钮高亮。点开历史条目不再自动收起侧栏。
**影响**：只改 `QA.vue`。

### 2026-09-03 · 问答页改成 ChatGPT 式布局

**问题**：历史会话常驻左侧，对话区像后台表单，和现在顶栏后的「主功能是聊天」不匹配。
**思路**：默认只留左上角会话/新对话图标；点会话图标才滑出历史列表。对话居中、用户气泡
靠右、底部圆角输入框。问答路由去掉 Layout 外边距，铺满主区。
**影响**：`QA.vue` 重排；`Layout.vue` 对 `/qa` 使用 `flush`。检索勾选和引用仍在，只是视觉降权。

### 2026-09-03 · 顶栏「我的」被收成省略号

**问题**：Tab 靠右后，Element Plus 横向菜单默认 `ellipsis=true`，宽度一紧就把最后一项收成「…」。
**思路**：关掉省略折叠（`:ellipsis="false"`），四个标签始终完整显示。
**影响**：只改 `Layout.vue`。

### 2026-09-03 · 顶栏去掉模型标签，Tab 靠右

**问题**：顶栏右侧的云端/本地 LLM 与 ASR 标签对教师没有操作意义，还把四个入口挤在中间。
**思路**：去掉 health 状态展示和对应请求；品牌留左，四个 Tab 顶到右边。
**影响**：只改 `Layout.vue`。后端 `/api/health` 仍给联调和自检用，前端不再打。

### 2026-09-03 · 导航改到顶部，文案缩短

**问题**：左侧目录占横向空间，四个入口还带 emoji，和「顶部标签页」的用法不一致。
**思路**：去掉侧栏和内页标题条，改成顶栏：品牌 + 四个文字标签（智能问答 / 教学评估 /
大纲优化 / 我的）+ 后端状态。路由不变，只改 `Layout.vue` 和页标题 meta。
**影响**：问答页高度仍按 `100vh - 顶栏 - 主区 padding` 计算，视觉上内容区变宽。

### 2026-09-03 · 默认进问答，侧栏增加个人信息

**问题**：打开系统先落到视频评估，日常入口更常是问答；侧栏也没有教师身份入口。
**思路**：根路径改为跳到 `/qa`；侧栏顺序改成问答、评估、大纲，并新增 `/profile`。
资料存在本机 `localStorage`（`pku-askedu-profile`），不接后端——系统还没有账号。
**影响**：`router/index.js`、`Layout.vue`、新增 `Profile.vue` / `profileStore.js`。
旧书签 `#/evaluation` 仍可用。

### 2026-09-03 · 线上总分改用 2018 v9 五维 5 分类 GB

**问题**：前端视频评估一直用当前 Judge 文件打五维，再等权平均出总分；GB 只在离线
对照里跑，没有接到产品链路。v9 已经是现行评分口径，继续挂 `live` 标签看不出用的
是哪一版。
**思路**：用 `dataset/2018_spring/v9/training_gb.csv` 的全部 22 人训五维 5 分类，
写成 `models/live/gb_llm_cls5.pkl`。线上 `evaluate_video` / 转写快评固定
`prompt_version=v9-calibrated`，五维仍由 Judge 打，总分改成 GB 档中点
（`label_to_score_100`）。等权平均留在 `equal_weight_score` 备查。数据集 rejudge
不加校准，避免 `llm_overall` 被 GB 污染后下一轮训练套套循环。
**对照**：同一 `gb_split.json` 的 5 人留出上，五维 5 分类 MAE **0.342** / Acc 0.400，
Judge 等权 MAE **0.557**。全量 22 人拟合 Acc=1.0、MAE 0.140，这是训练集内数字，
不能当泛化。宋晨从 Judge 3.80 收到 3.75（专家 3.06），王勋从 3.70 抬到 4.25
（专家 4.56），杨文云仍被高估（专家 3.70 / Judge 3.01 / GB 4.25）。
**影响**：`gb.py` 增加推理；`pipeline.py` 线上路径接 GB；前端总分旁标明来源；
`make train-gb-live`；`.gitignore` 放行 `models/live/gb_llm_cls5.pkl`。缺模型时
评估会失败，先跑训练命令。

### 2026-09-03 · 2018 v4 恢复缓存并增加两路 GB

**问题**：只比「五维 / 五维+客观」看不出客观特征和二级指标各自有没有校准价值；
同时 2018 默认 `cache/` 的 `scores.json` 已被 v5 覆盖，直接 rejudge v4 会用上
当前 v9 规则，不再是原来的 v4。
**思路**：从 `eval_snapshots/v4` 拷回 22 份分数到 `cache_v4/`，用现成 evidence
merge。特征选择收紧为前缀：`objective` 只要 7 组客观列，`indicators` 只要 `ind_*`
（不含 `_assessed`）。merge 的 `training_gb.csv` 带上二级分。同一
`gb_split.json` 上加训两路回归。
**影响**：`scripts/train_gb_{obj_only,ind_reg,2018_v4}.py`，`make train-gb-2018-v4`。
测试集 MAE：客+五 0.38，二级 0.44，客观 0.47，Judge 0.53。不要用当前代码重打 v4。

### 2026-09-03 · gitignore 补上独立评分缓存

**问题**：`.gitignore` 只排除 `dataset/**/cache/`，`rejudge --output-cache` 写到
`cache_fixed_prompt`、`cache_goal_v7`、`cache_v9` 等平级目录，`git add .` 会把可重建的
`scores.json` 和网络失败残片一并入库。
**思路**：目录名以 `cache_` 开头的一律忽略；改分制前的 `scale_backup_legacy_*` 与现表
重复，一并排除。merge 出的 csv、lessons、专家规则长表仍可见。
**影响**：`.gitignore` 增加 `dataset/**/cache_*/`、`dataset/scale_backup_legacy_*/`。
提交前不必再手动漏掉这些目录。

### 2026-09-03 · v9 取消70分软地板并增加五维诊断报告

**问题**：v7.1 的冻结规则普遍写有“单个改进项不可导致维度低于70分”，模型容易把它
误解为维度最低分保护；同时 `severity` 与一级分没有绑定，出现 `ordinary_issue` 却仍给
85–90分。报告又只选择全局最低的2–3项，导致已经识别出的教学态度、教学内容问题经常
不进入最终报告。
**处理**：17条冻结规则全部移除70分软地板，单个轻微问题通常影响2–5分，但多个独立且
证据充分的问题必须累计，一个严重问题或多个问题累计可使维度低于60分。Judge Prompt
绑定 `none=85–100 / improvement_only=75–89 / ordinary_issue=60–79 /
major_issue=0–59`，并规定90分以上至少需要两项示范性证据，不能用“未发现错误、材料存在、
结构完整”等直接推出优秀。报告输入显式展示每维 `primary_issue` 与 `severity`，新增“五维
诊断”部分：每维一个具体亮点、一个具体改进点；确无反面证据时固定写“当前证据未发现
显著问题”。主要问题按严重度、学习影响、证据和独特性选择，不再只取最低分。
**影响**：版本记为 `v9-calibrated`，2018 独立缓存为 `cache_v9`，运行
`make rejudge-2018-v9`；v7.1 与更早缓存不会被覆盖。未来重新 distill/freeze 也会自动清除
旧候选规则中的70分软地板。

### 2026-09-02 · v7.1 恢复教学效果的预期效果兜底

**问题**：从 v6 回到加入“教学目标与定位”的 v7 时，教学效果专用的“直接结果与预期
效果分开”提示块和导出元数据被一并撤回；通用可观察性规则还误写成“缺失本身产生0分
扣分”。结果2018 v7有12/22人的教学效果被保存为真实0分，污染五维总分和GB训练。
**处理**：直接学生结果不可观察时，四个二级指标继续保持 `null`，但一级教学效果必须
根据目标、内容、逻辑、表达、案例、节奏和总结等教学过程推断，标记 `score_basis=inferred`，
置信度不高于 medium。禁止因学生未出镜或无学生声音给0分、低分或空分。模型首次仍返回
0/空分时自动重试；两次都失败时，使用其余四个可观察一级维度的加权均值作低置信度技术
兜底，并明确不代表观察到学生真实掌握。
**影响**：当前口径版本记为 `v7.1-goal-effect-fallback`，独立缓存目录为
`cache_goal_effect_v7_1`；旧 `cache_goal_v7`、旧GB模型和旧对照表保留为历史结果，不覆盖。
运行 `make rejudge-2018-v7-effect` 后再独立 merge、重训。

### 2026-09-02 · 修正专家 4 分制到百分制的换算

**问题**：原代码把评分表中的 2 分误当成量表零点，使用 `(均分−2)÷2×100`，导致
“满分 4 分、2 分及格”的 2 分被换成 0 分；Judge 却仍按正常百分制评价，二者 MAE
不在同一尺度上。
**处理**：统一改为 `均分÷4×100`，即 2→50、3→75、4→100；0–5 对照相应改为
`均分÷4×5`，即 2→2.5、3→3.75、4→5。同步修正分类中点还原、百分制逆变换、专家规则
审计分和综合评分 Prompt 的及格锚点。新增迁移脚本，旧 CSV 首次修正前备份到
`dataset/scale_backup_legacy_20260902/`，历史 prompt 快照与历史模型预测不覆盖。
**影响**：旧 GB 模型、MAE、Judge 基线和逐人误差均须重算；直接使用 2–4 原分划出的
5/8/10 分类标签不变，但分类预测到百分制或 0–5 的还原值会变化。
2018 v7 已用修正后的标签重新合并到 `dataset/2018_spring/goal_v7/`，无需重跑视频分析或
五维 Judge。已沿用原来的17人训练、5人测试划分重训，命令为 `make train-gb-2018-v7`。
测试集新结果（0–5）为：Judge MAE 1.137；客观特征+五维回归 **0.385**；五维回归
0.826；五维5分类 1.022（Acc 0）；五维8分类 **0.499**（Acc 0.20）。样本只有5人，
该排序仅用于同一测试集上的探索性比较，不能据此确定最终线上模型。

### 2026-09-02 · 撤回 v8 五维报告双轴实验

**问题**：v8 增加的结构化亮点、问题角色、根因去重和最高/最低报告改写，在 5 人测试中
没有带来足够稳定的专家对齐效果，并引入目标、流利度、PPT 等新的误判。
**处理**：恢复到加入“教学目标与定位”后的 v7 代码状态；删除 v8 专用命令、对照脚本和
双轴字段，不改动 v7 的指标定义与关注重点调整指南。已经生成的 v8 缓存仅作为历史实验
保留，不会被当前代码读取或复用。

### 2026-08-31 · 新增“教学目标与定位”二级指标及调整指南

**问题**：专家规则已有“教学目标或本节定位不清”，但运行 rubric 没有对应二级指标，
因此它只能影响教学内容维度的主缺陷判断，不能在五维明细中单独展示；同时指标关注重点
分散在 rubric、规则和两层 Prompt 中，后续容易误以为只改 `weight` 就会生效。
**思路**：在教学内容下新增 `goal_clarity / 教学目标与定位`，从目标可识别、内容与目标
一致、完整课时回扣目标三个观察点评价；不强制口头宣读，缺开头/结尾的片段不因此扣分，
只有目标不可识别且内容发散时才可作为主缺陷。README 补充四层修改入口和重打分流程。
**影响**：指标体系从 24 个二级指标增至 25 个；旧缓存不变，新版需用独立缓存 rejudge。

### 2026-08-30 · 2018 测试集增加 LLM 综合总分盲评

**问题**：现有 Judge 只对五维等权平均，GB 在 2018 的 5 人预测集上又容易受小样本和
代理特征误导，尚未验证 LLM 能否结合五维语义诊断与客观证据重新判断总分。
**思路**：新增独立综合评分 Prompt。调用 LLM 时严格排除专家分、专家评语和 GB 预测；
五人结果全部落盘后再读对照表，防止标签泄漏。总分不是机械平均，并加入反证保护与
不可观察证据降置信度规则。
**影响**：新增 `scripts/judge_overall.py`、`eval_overall_judge.j2` 及无泄漏测试，命令为
`make judge-overall-2018`。本次 LLM MAE 0.645，优于等权 Judge 1.045 和最佳 GB 0.836；
优势主要来自厉行、王菁、杨文云接近专家，以及缓解王勋的 GB 极端低估，但宋晨仍显著
高估，因此结论仅作为五例探索结果。

### 2026-08-30 · 2018 两套 prompt 上训四种 GB

**问题**：`fixed_prompt`（v5-rules17）和 `effect_inferred`（v6）是新打的 2018 表，
四年拼表上的 GB 结论不能直接当成这两套 prompt 的结论；v5 还缺大量「教学效果」。
**思路**：不覆盖 `dataset/gb_split.json`。22 人做年内 80/20（seed 42），两套表共用
同一预测集，四种方法各训一遍。表里没有 `batch` 时按全体划分。
**影响**：`scripts/train_gb_2018_prompts.py`、`make train-gb-2018`。划分在
`dataset/2018_spring/gb_split.json`。客+五回归两次都压过 Judge 约 0.21，五维三种
都打不过；预测集只有 5 人，不能据此换线上总分。

### 2026-08-30 · rejudge 支持新旧评分并存

**问题**：`rejudge` 原先固定覆盖 `cache/{video_id}/scores.json`，不利于逐人比较旧 Prompt 与
新规则的结果；`merge` 也只能读取默认缓存并覆盖批次根目录下的三张 CSV。

**影响**：`rejudge` 新增 `--output-cache`，证据仍从默认 `cache` 读取，评分可写入例如
`cache_fixed_prompt/{video_id}/scores.json`。`merge` 新增 `--scores-cache` 和
`--output-dir`，可从新版评分缓存生成独立对照表。两项参数均有默认值，旧命令行为不变；
缓存目录必须位于批次目录内，拒绝绝对路径和 `..` 路径。

### 2026-08-30 · 专家“分数—评语”规则学习接入 Judge

**问题**：旧 `reflect / distill` 把每课差异压成少量短句，容易得到“校准尺度、勿打穿”
等未来没有专家意见时无法执行的经验；同时 Judge 强制给所有二级指标数值分，PPT 画外音、
单人微格或无学生镜头时，学生参与、互动和掌握等不可观察项仍可能被当成低表现。

**思路**：四份评分表先清洗成长表，再让 LLM 逐条拆出原子优缺点，按独立教师统计问题
被明确提及时的高/低分分布、评分人口径差和反例，最后生成带 `minor_when / major_when /
not_observable_when` 的结构化候选规则。2018/2019 的汇总文字只配平均分；2022 保留三位
专家的个人分数—评语；2024 原表实际是五位专家，006–009 的备注和各自分数配对，005
仅在有个人备注时配对，“汇总评语-ZX”只配平均分。共得到 715 条评分记录、638 条有效
评语、209 位教师。抽取命令逐条显示缓存、耗时和 ETA，并可用 `--resume` 续跑。

**Judge 口径**：最终 Prompt 固定写入“不可观察不等于表现差”。因视频形式缺少观察对象时，
二级指标返回 `observability=not_observable, assessed=false, score=null`，缺失不扣分、不填
中间分，一级维度只使用其余可观察项。Judge 输出增加 `primary_issue / severity /
applied_rule_ids`；生产侧按维度读取 `expert_rules.yaml`，候选规则默认不会上线。同一现象通过
唯一 `primary_dimension` 与 `must_not_penalize_dimensions` 防止跨维重复扣分。

**五维校验**：以 `evaluation_criterion.md` 为基本定义。人工审核后冻结 17 条规则：教学态度
4 条、教学内容 4 条、教学方法 7 条、教学素质 2 条。“感染力、激情或生动性”依据“语调
积极且富于变化”归入教学态度；画面、机位和拍摄质量不属于五维，保留为技术提示但不进入
正式评分。`freeze` 现在会拒绝复合标签、`recording_only`、`unknown`、非法排除维度和重复
rule ID，避免无效规则静默进入生产文件。

**影响**：新增 `scripts/build_expert_rules.py`、`scripts/eval_dataset/expert_rules.py`、
`expert_review_extract.j2`、`expert_rule_distill.j2`、`ai_engine/pedagogy/expert_rules.yaml` 与
`dataset/expert_rules/` 审计产物。Judge Prompt、rubric 或冻结规则改变后会生成新的
`judge_fingerprint`；即使 `prompt_version` 相同也不会误复用旧 `scores.json`。新增 7 项规则
与可观察性测试，原有特征、数据集和 GB 测试保持通过。下一步应先保留 v4 对照快照，再以
不注入旧 `lessons_frozen.md` 的新版本统一 rejudge，随后 merge/combine，对比新旧 Judge
MAE、排序相关和大误差案例后再重训 GB。

### 2026-08-29 · GB 改在 0–5 分上训练和比较

**问题**：专家打的是 2–4 均分，对照表却用 0–100，MAE 十六七看着和专家表对不上。
**历史思路（已于 2026-09-02 判定为错误口径）**：曾使用 `(均分−2)/2×5`
（2→0、4→5）。评分表中的 2 是及格线而非量表零点，当前已改为 `均分÷4×5`。
当时回归直接拟合 0–5 并截断；
分类仍按 2–4 分档，中点再映回 0–5。Judge 总分同样 ÷20。划分仍用已有 `gb_split.json`。
**影响**：本条记录中的旧 MAE 与模型均已失效，仅保留为问题追踪；须按 2026-09-02
的新口径重训后再填写结果。线上仍走 Judge。

### 2026-08-27 · 四个 GB 对照共用 2022 预测集

**问题**：前两版一个是全特征回归、一个是五维 5 分类，划分不同（留一年 vs 随机 8:2），
数字不能比。客观特征要不要、回归还是分类、5 类还是更细的档，需要同一批人上的结论。
**思路**：删掉 `ai_engine/evaluation/train.py`。改成四个脚本，划分锁在
`dataset/gb_split.json`：只从 2022 划 20% 作预测集（分层按 5 类，稀有档并进多数档），
其余年份全部进训练。分类预测用档中点还原成百分制，才能和回归、Judge 比 MAE。
8 类 step=0.25，比 5 类细、比论文 10 类少一些空档。
**影响**：`scripts/train_gb_{obj_reg,llm_reg,llm_cls5,llm_cls8}.py`，`make train-gb`。
预测宽表 `dataset/gb_predictions.csv`。第一次 2022 留出 14 人：Judge MAE 16.4；
五维 8 分类 18.9，全特征回归 19.1，五维回归 21.0，五维 5 分类 21.3（Acc 0.43）。
线上仍走 Judge。

### 2026-08-27 · GB v2：只学五维 LLM 分的分类器（保留 v1）

**问题**：v1 把约 70 维客观特征拿去回归百分制，留一年 MAE 16.7，没有打过 Judge 的 14.9。
论文和 1.0 都是「少量语义特征 + 分类 GB」：1.0 用五维手工特征做 5 分类，论文用离散化
降低噪声。客观特征缺测、跨年分布差，可能在帮倒忙。
**思路**：另训一版，特征只用五维 `llm_dim_*`，标签按 1.0 把专家均分切成 5 类
（`⌊(均分−2.0)/0.4⌋`）。v1 的 `gb_regressor.pkl` 不删、不覆盖，默认路径按任务分开。
分类预测还原成百分制 MAE，才能和 v1、Judge 放在同一把尺上。
**影响**：`make train-cls` → `models/gb_classifier_llm.pkl`（v1 的 `gb_regressor.pkl`
仍在）。`--n-classes 10` 可对照论文。第一次留一年：Acc 0.26 / MAE 20.8，Judge 离散化
Acc 0.38 / MAE 14.9。线上评估仍走 Judge。

### 2026-08-27 · 增加 GB 训练脚本（回归校准，默认不改线上打分）

**问题**：四年 v4 训练表已经拼好，但 2.0 还没有对应 1.0 `train.py` 的拟合入口。
直接复用 1.0 的五分类 GB 对不上现在的表：特征从 5 维变成约 70 维，标签是百分制，
Judge 已经给了五维分，GB 的任务变成校准而不是主评分器。
**思路**：邵果毅论文选 GB 是因为样本少、有噪声，不宜上深度网；浅树拟合残差。
2.0 默认 `GradientBoostingRegressor` 预测 `expert_total_100`，按年留一交叉验证，
并用 `llm_overall` 当基线。分类（论文 10 类 / 1.0 的 5 类）留作 `--task classify`
对照，因为没有论文里的「文本切 8 段」扩增，10 类在 n≈100 时尾部只有 1–2 人。
王长松均分为 0 由脚本剔除；说话人整列空则丢掉；课件等高缺失列加缺失指示。
**影响**：`ai_engine/evaluation/{gb,train}.py`，`make train` / `make check-gb`。
`pandas`、`scikit-learn` 写入 `requirements.txt`。pkl 仍 gitignore。第一次留一年
CV：GB MAE 16.7，Judge 总分基线 14.9；随机 8:2 则 GB 12.9 < Judge 15.3（同年样本
泄漏，不能当结论）。所以线上 `evaluate_video` 仍只走 Judge，等留一年稳定优于
基线再接入。

### 2026-08-27 · 四年 v4 训练表 merge + combine

**问题**：v4 rejudge 已齐，但还没有能训 GB 的拼表。`merge` 只认一个目录，
四年要手动 cat 还容易把评语表和特征表搞混。
**思路**：四年各跑一次 `merge`（不调模型）。新增 `combine` 加上 `batch` 列
拼成 `dataset/training_*_all.csv`。GB 只用 `training_gb_all.csv`（无评语）。
**历史影响**：104 行，全是 v4。`training_gb_all.csv` 79 列。2019 王长松均分为 0，
拟合前应剔除。本条记录中的旧百分制残差已因 2026-09-02 的换算修正而失效。

### 2026-08-27 · 四年 v4 rejudge 全部完成

**问题**：断电后 2022 只写成丛治辰，2024 还没开始，训练表不能拼。
**思路**：`--resume` 跳过已是 v4 的人，续跑 2022 剩余 67 人再打 2024 的 3 人。
**影响**：四年 `cache/*/scores.json` 均为 v4（22+11+68+3=104，失败 0）。
年序分仍在 `cache_by_year/`。下一步四年 `merge` 再拼 `training_gb_all.csv`。

### 2026-08-26 · rejudge 支持 --resume（断电后续跑 2022）

**问题**：四年 v4 rejudge 跑完 2018/2019 后刚开始 2022（只写成丛治辰）电脑没电。
原命令会把已是 v4 的人再打一遍。
**思路**：`--resume` 时若 `scores.json` 的 `prompt_version` 已是目标版本则跳过。
2018（22）和 2019（11）保留；2022 从剩余 67 人接着打，然后 2024 的 3 人。
**影响**：`build_eval_dataset rejudge` 增加 `--resume`。不要对未完成的年份省略该参数。

### 2026-08-26 · 四年统一 rejudge（v4 + 冻结口径）开始

**问题**：各年 `scores.json` 分别是 v0/v1/v2/v3，特征不可比，不能直接拼训练表。
**思路**：先把各年 `scores.json` 拷到 `cache_by_year/`，再用同一份
`dataset/lessons_frozen.md`、`--prompt-version v4` 只重打分，不重跑 ASR。
**影响**：rejudge 覆盖 `cache/*/scores.json`。跑完后再 `merge`。年序分仍在
`cache_by_year/`，`.gitignore` 已排除。

### 2026-08-26 · 四年 distill 合并成冻结 8 条

**问题**：2018/2019/2022/2024 各有一份最多 8 条的快照，不是累加栈，直接拼接
会重复且互相打架。2018/2024 主张「纯讲授互动少只作建议」；2019 有一条
「勿因无学生出镜宽容互动缺失」；2022 同时有「互动少仅作建议」和「提问设计
不足须作主缺陷打穿」。最终 rejudge 只能喂一份。
**思路**：按出现次数和能否解释分数分歧人工压成 8 条祈使句。互动冲突取多数：
无学生出镜或内容完整的纯讲授，互动少不打穿效果维；语速过快/念稿仍要扣，但
口误不打穿态度维。课型不符、缺导入总结、内容不完整、读屏、PPT 字多、课件
与讲述不一致/纯板书缺总结保留。不粘进 `eval_judge.j2`。
**影响**：写出 `dataset/lessons_frozen.md`。后续四年 `rejudge` 都用
`--prompt-version v4 --lessons dataset/lessons_frozen.md`。各年原 md 不动。

### 2026-08-26 · 2024 春 3 人 extract 完成（v3 + 2022 口径）

**问题**：有视频的 3 人需要按 2022 蒸馏口径打分，才能进入 reflect。
**思路**：`--prompt-version v3 --lessons dataset/2022_spring/lessons_distilled.md`，
不重跑前几年，也不用 2024 自己的评语回打本年。
**影响**：`dataset/2024_spring/cache/` 张亿、王欢、黄炜三人 `evidence.json` +
`scores.json` 齐（失败 0），三人都有备课 PDF。其余 71 人仍缺视频。
下一步可对这 3 人 `reflect`，或等试讲目录补齐后再 inventory / extract。

### 2026-08-26 · 开始 2024 春微格批次（姓名-学号平铺）

**问题**：2024 仍是备课/试讲分目录，但文件名改成 `姓名.mp4` / `姓名-学号.pdf`，
旧的「编号-姓名-院系」解析对不上。打分表一人一行，「平均分」和「分数」不是
同一列；评语在「汇总评语-ZX」，另有「备注」；表里有邮件和职工号，不能进 csv。
试讲目录目前几乎是空的。
**思路**：平铺扫描同时认 2022 编号格式和 2024 姓名-学号（英文名按前缀对上
打分表）。分数用「平均分」，「分数」只进 expert1。「汇总评语-ZX」+「备注」
拼进 comment。CSV 不写邮件/职工号。extract 用
`--prompt-version v3 --lessons dataset/2022_spring/lessons_distilled.md`。
**影响**：`inventory.py`、`test_eval_dataset.py`、`.gitignore` 增加
`test/2024春微格作业-74人/`。写出 `dataset/2024_spring/{inventory,manifest}.csv`：
74 人扫描、3 人有视频。缺视频的人要等材料补齐才能 extract。

### 2026-08-23 · 2022 春 68 人 extract 完成（v2 + 2019 口径）

**问题**：2022 有视频的 68 人需要按 2019 蒸馏口径打分，才能进入 reflect。
**思路**：`--prompt-version v2 --lessons dataset/2019_spring/lessons_distilled.md`，
不重跑 2018/2019，也不用 2022 自己的评语回打本年。
**影响**：`dataset/2022_spring/cache/` 68 人 `evidence.json` + `scores.json` 齐（失败 0）。
17 人有课件、1 人有教案。下一步是 `reflect` / `distill`，不必立刻 merge。

### 2026-08-23 · 开始 2022 春微格批次（平铺目录 + 三人行打分表）

**问题**：2022 材料不再是一人一夹。视频在「试讲」目录、课件在「备课」目录，
文件名是 `编号-姓名-院系`（青教赛带前缀）；打分表同一人三行、均分列叫
「平均分数」、评语叫「突出优点 / 需要改进」。旧扫描会把整个试讲夹当成一个人，
且若按第一人（楚健春只有一行）收集专家列，会把另外 67 人的第二、三位专家分丢掉。
**思路**：目录里堆满编号文件时按文件名拆姓名，把备课和试讲拼成一条。三人行
压成一人一行：分数用表上「平均分数」，三位专家的优点/改进全部写入 comment，
各位「总体评价」进 expert1/2/3。专家列按全表最大人数补齐，避免被缺行的人截断。
2022 extract 用 `--prompt-version v2 --lessons dataset/2019_spring/lessons_distilled.md`，
不把 2022 自己的口径打回本年。
**影响**：`inventory.py`、`test_eval_dataset.py`、`.gitignore` 增加 `test/2022微格/`。
写出 `dataset/2022_spring/{inventory,manifest}.csv`（68 人）。备课目前约 18 份。
楚健春标 `incomplete_experts`，分仍用 3.033。

### 2026-08-20 · 2019 春 11 人 extract 完成（v1 + 2018 口径）

**问题**：2019 有视频的 11 人需要按 2018 蒸馏口径打分，才能进入下一年 reflect。
**思路**：`--prompt-version v1 --lessons dataset/2018_spring/lessons_distilled.md`，
不重跑 2018。课件解析失败不判死整堂课。
**影响**：`dataset/2019_spring/cache/` 11 人 `evidence.json` + `scores.json` 齐（失败 0）。
胡岠无课件文件。下一步是 `reflect` / `distill`，不必立刻 merge。

### 2026-08-20 · 数据集构造操作收成 README 第八章

**问题**：inventory / extract / reflect / distill / rejudge / merge 的约定散落在
功能① 的段落和聊天记录里，2019 开跑时不知道 `--lessons` 怎么挂、能不能删原始视频、
要不要立刻 merge。
**思路**：从「三个功能怎么用」里抽出独立章节，按年流水线写可复制命令、目录约定、
禁止事项（不把口径粘进 `eval_judge.j2`、不用本年口径打本年）和 2018/2019 进度表。
命令速查补全对应入口。
**影响**：README 第七节只留跳转；新第八章；其后章节序号 +1。

### 2026-08-20 · 开始 2019 春微格批次（注入 2018 口径）

**问题**：2018 已蒸馏出 `lessons_distilled.md`，2019 要按同一套扫描/抽证流程跑，
并把口径注入 Judge。2019 打分表第一行是标题、表头在第二行，评语拆成「整体优点 /
需要改进」；目录被 Finder 复制出 42 个空的 ` (2)` 文件夹；约 30 个正本文件夹也没有视频。
**思路**：xlsx 找到含「姓名」的那一行当表头。没有「评语」列时把优点+改进拼成 comment。
跳过 ` (2)` 副本。2019 extract 用 `--prompt-version v1 --lessons dataset/2018_spring/lessons_distilled.md`，
不对 2018 自己 rejudge。
**影响**：`xlsx.py`、`inventory.py`、`.gitignore` 增加 `test/2019春微格作业-42人/`。
写出 `dataset/2019_spring/{inventory,manifest}.csv`：42 人扫描、11 人有视频进候选。
缺视频的人要等材料补齐才能 extract。

### 2026-08-20 · reflect/distill 改为「没专家时怎么打」

**问题**：第一轮 lesson 在教模型「有专家时如何对齐」，例如「需对齐专家主缺陷」
「熟悉度结合专家听感」。下次 Judge 没有评语、也没有听感，这些句子无法执行。
**思路**：不把客观特征表塞进 reflect（避免过拟合单课数字）。评语和模型摘要对照
仍做，但 lesson 必须是给未来评分员的祈使句：主缺陷是什么、什么只算建议、
哪一维不该被单项打穿。禁止「专家 / 模型 / 对齐 / 听感」。含这些词的输出
写入 `rejected_lesson` 后清空，distill 也不收。Judge 注入段改为「历史评审偏好」，
用于主缺陷和一级折算，不覆盖已打的二级分。
**影响**：`eval_reflect.j2`、`eval_distill.j2`、`eval_judge.j2`、
`scripts/build_eval_dataset.py`。已有 `lessons/*.json` 是旧口径，需**不加**
`--resume` 重跑 reflect，再 distill。

### 2026-08-20 · 课件解析容错：截断 PPTX 与 MuPDF Screen 注释

**问题**：2018 微格 extract 卡在两处。王菁的 `科维理-王菁.pptx` 以 PK 开头但没有
zip 中央目录（尾部是 `0xFF` 填充），LibreOffice 打不开，python-pptx 报
`Package not found`，整堂课失败；同目录其实有一份能转的 `.ppt`。门卫伟的
PPTX 能转 PDF，但页上有嵌入媒体变成的 Screen 注释，MuPDF 往 stderr 刷
`cannot create appearance stream`，看起来像崩了。
**思路**：选课件时跳过打不开的 pptx，改用旁边的 ppt。解析端也做同样回退，
这样旧 manifest 仍指向坏 pptx 时 extract 也能走通。渲染 PDF 时不画注释，
并关掉 MuPDF 这段 stderr。课件彻底失败改为 warning，按无课件口径继续，
不再把已抽的音一起判死。LibreOffice 使用独立 user profile，避免 GUI 占用
默认配置目录导致转换空返回。
**影响**：`materials.py`、`pipeline.py`、`inventory.py`。`make check-features`
覆盖损坏 pptx 改用同名 PDF；`make check-dataset` 断言王菁选中 `.ppt`。
`--resume` 会重试王菁（没有 evidence.json）。门卫伟若已写出 evidence 则不会重跑。

### 2026-08-19 · ffmpeg stderr 按容错 UTF-8 解码

**问题**：2018 厉行的 `.mov` 抽音频在 5% 报 `utf-8 codec can't decode byte 0xb9`。
不是 MOV 不能转——刘冲的 `.mov` 已成功。ffmpeg 会把容器里的 GBK/老 QuickTime
元数据打到 stderr，`subprocess.run(..., text=True)` 默认按 UTF-8 严格解码，
读输出时就崩，音轨其实还没抽完。
**思路**：抽音、抽帧、probe 一律 `encoding=utf-8, errors=replace`。非法字节换成
替换符，真正的 ffmpeg 失败仍看 returncode。
**影响**：`ai_engine/evaluation/media.py`。`--resume` 会重试厉行（没有
evidence.json）。

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
