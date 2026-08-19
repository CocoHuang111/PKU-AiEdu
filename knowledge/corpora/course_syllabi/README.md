# 课程大纲参考语料库

收录国内外**公开、高质量**课程 syllabus **原版**（HTML / PDF），供大纲优化与智能问答检索参照。

```bash
make ingest
# 或
python -m knowledge.ingest --corpus course_syllabi
```

**说明**：本 README 仅作目录与编辑点评，**不入库**（ingest 自动跳过 `readme.md`）。
正文以各子目录下的 `.html` / `.pdf` 为准。

---

## 目录结构

```
course_syllabi/
├── MIT-OCW/       # MIT OpenCourseWare（CC BY-NC-SA）
├── Stanford/      # Stanford 课程 archive
├── Yale-OYC/      # Open Yale Courses
├── CMU/           # CMU CS archive
├── Harvard/       # Harvard CS50
└── README.md      # 本文件（目录 + 参考价值，不入库）
```

---

## 收录目录（11 门）

### MIT OpenCourseWare

#### 1. 6.006 Introduction to Algorithms（算法导论）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `MIT-OCW/6.006-算法导论-Spring2020.html` |
| **学期** | Spring 2020 |
| **学科** | 计算机 · 算法与数据结构 |
| **原始 URL** | https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/syllabus/ |
| **许可** | Creative Commons BY-NC-SA |
| **归档日期** | 2026-08-06 |

**参考价值**

- **先修门控**（Problem Set 0）写法可借鉴
- **Quiz 分散 + Final 高权重** 的测评结构
- 明确列出**算法范式**与**数据结构**清单，便于 OBE 对齐

---

#### 2. 6.042J Mathematics for Computer Science（计算机科学数学）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `MIT-OCW/6.042J-计算机科学数学-Spring2015.html` |
| **学期** | Spring 2015 |
| **学科** | 计算机 / 数学 · 离散数学 |
| **原始 URL** | https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/syllabus/ |
| **许可** | Creative Commons BY-NC-SA |
| **归档日期** | 2026-08-06 |

**参考价值**

- **Flipped + 团队课堂** 的完整政策表述（参与 vs 正确率）
- Online feedback 5% **参与即满分** 设计
- 详细 **learning outcomes** 十条清单
- 最低分剔除与 midterm/final **crib sheet** 规则

---

#### 3. 18.06 Linear Algebra（线性代数 · Strang）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `MIT-OCW/18.06-线性代数-Spring2010.html` |
| **学期** | Spring 2010 |
| **学科** | 数学 · 线性代数 |
| **原始 URL** | https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/syllabus/ |
| **许可** | Creative Commons BY-NC-SA |
| **归档日期** | 2026-08-06 |

**参考价值**

- **目标—内容—测评** 高度对齐的数学课范例
- 明确「可讨论 / 须独立写」的学术诚信表述
- 10 条主线便于章节级 mapping

---

#### 4. 21A.00 Introduction to Anthropology（人类学导论）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `MIT-OCW/21A.00-人类学导论-Spring2022.html` |
| **学期** | Spring 2022 |
| **学科** | 人文 · 人类学 |
| **原始 URL** | https://ocw.mit.edu/courses/21a-00-introduction-to-anthropology-spring-2022/pages/syllabus/ |
| **许可** | Creative Commons BY-NC-SA |
| **归档日期** | 2026-08-06 |

**参考价值**

- **研讨课**参与规则与设备政策范例
- 多种 writing genre（commentary + research）的权重设计
- 「Ritual design」等**创造性作业**与 OBE 对齐

---

#### 5. 7.91J Foundations of Computational and Systems Biology（计算与系统生物学）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `MIT-OCW/7.91J-计算与系统生物学-Spring2014.html` |
| **学期** | Spring 2014 |
| **学科** | 交叉 · 计算生物学 |
| **原始 URL** | https://ocw.mit.edu/courses/7-91j-foundations-of-computational-and-systems-biology-spring-2014/pages/syllabus/ |
| **许可** | Creative Commons BY-NC-SA |
| **归档日期** | 2026-08-06 |

**参考价值**

- **同一课程多课号、多评分方案** 的写法
- Problem Set + Exam + Project + Peer Review 组合
- 明确 Python 与跨学科先修矩阵

---

### Stanford

#### 6. CS106A Programming Methodology（编程方法学 · Python）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `Stanford/CS106A-编程方法学-Python.html` |
| **学期** | Summer 2025（archive） |
| **学科** | 计算机 · 编程入门 |
| **原始 URL** | https://stanford.edu/class/archive/cs/cs106a/cs106a.1258/syllabus |
| **许可** | © Stanford University；公开网页仅供教育参考 |
| **归档日期** | 2026-08-06 |

**参考价值**

- **Bucket grading**（+/✓+/✓/✓−/−）替代细粒度分数
- **Grace period + on-time bonus** 迟交政策组合
- Interactive grading 与 **mastery learning** 声明
- 软件工程原则（分解/封装/测试）写入 course description

---

### CMU

#### 7. 15-122 Principles of Imperative Computation（命令式编程原理）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `CMU/15-122-命令式编程原理-Summer2024.html` |
| **学期** | Summer 2024 |
| **学科** | 计算机 · 系统编程（C0/C） |
| **原始 URL** | https://www.cs.cmu.edu/~15122-archive/n24/syllabus.shtml |
| **许可** | CMU 课程网站公开材料 |
| **归档日期** | 2026-08-06 |

**参考价值**

- **Programming + Written** 双轨作业比例（30% + 15%）
- C0→C 渐进与 deliberate programming 叙事
- **Late day** 机制与 style regrade 流程
- Learning objectives 分「编程技能 / 算法」两栏

---

### Harvard

#### 8. CS50 Introduction to Computer Science（计算机科学导论）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `Harvard/CS50-计算机科学导论-Fall2024.html` |
| **学期** | Fall 2024 |
| **学科** | 计算机 · 通识入门 |
| **原始 URL** | https://cs50.harvard.edu/college/2024/fall/syllabus/ |
| **许可** | Harvard CS50 公开网页材料 |
| **归档日期** | 2026-08-06 |

**参考价值**

- **60/15/15/10**（作业 / checks / 项目 / 出席）大课经典权重
- **correctness / design / style** 加权公式（2:2:1）
- SAT/UNS 与 QRD 分布要求说明
- Checks **限制工具使用** 的诚信设计
- 10 周主题链 + final project 三阶段里程碑

---

### Open Yale Courses

#### 9. ECON 159 Game Theory（博弈论）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `Yale-OYC/ECON159-博弈论-Fall2007.html` |
| **学期** | Fall 2007 |
| **学科** | 经管 · 博弈论 |
| **原始 URL** | https://oyc.yale.edu/economics/econ-159 |
| **许可** | Open Yale Courses 公开访问条款 |
| **归档日期** | 2026-08-06 |

**参考价值**

- 人文社科/经管课 **problem set + 双 exam** 经典结构（30/30/40）
- 先修分层说明（required / recommended / exclusion）
- 27 讲主题链可直接映射 chapter plan

---

#### 10. HIST 119 The Civil War and Reconstruction Era（美国内战与重建）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `Yale-OYC/HIST119-美国内战与重建-Spring2008.html` |
| **学期** | Spring 2008 |
| **学科** | 历史 |
| **原始 URL** | https://oyc.yale.edu/history/hist-119 |
| **许可** | Open Yale Courses 公开访问条款 |
| **归档日期** | 2026-08-06 |

**参考价值**

- **双 paper + final** 人文课经典权重（30/30/30/10）
- 文档集 + 长篇背景阅读的层次分工
- 明确 paper 分属课程**前半/后半**板块

---

#### 11. PHIL 181 Philosophy and the Science of Human Nature（哲学与人类本性）

| 项 | 内容 |
| --- | --- |
| **本地文件** | `Yale-OYC/PHIL181-哲学与人类本性-Spring2011.html` |
| **学期** | Spring 2011 |
| **学科** | 哲学 / 认知科学 |
| **原始 URL** | https://oyc.yale.edu/philosophy/phil-181 |
| **许可** | Open Yale Courses 公开访问条款 |
| **归档日期** | 2026-08-06 |

**参考价值**

- **哲学 + 认知科学** 跨学科 syllabus 结构
- 高频 **directed exercises**（35%）+ 双 essay 权重差异化
- Final **题目预公布** 的测评设计
- 经典文本 + 实证论文 + 多媒体资源并列列举

---

## 新增语料规范

1. **优先保留原版**：PDF 直接入库；仅网页 syllabus 的用 `curl` 归档 HTML 至对应子目录
2. **命名**：`课号-课程名-学期.html`（或 `.pdf`）
3. **本 README 同步更新**：元数据、原始 URL、许可、归档日期、**参考价值**（编辑归纳，非原文）
4. **勿将二次摘要与原版并存入库**——避免 RAG 检索重复/冲突

## 许可汇总

| 来源 | 许可 |
| --- | --- |
| MIT OCW | Creative Commons BY-NC-SA |
| Open Yale Courses | OYC 公开访问条款 |
| Stanford / CMU / Harvard | 各院校课程网站公开材料；以原页为准 |
