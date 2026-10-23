"""问答模式注册表。

模式只定义任务工作流、默认证据范围和输出契约；语料库仍是证据来源，
用户在前端手动选择的语料库会覆盖模式默认值。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class QAMode:
    name: str
    label: str
    description: str
    placeholder: str
    retrieval_strategy: str
    default_corpora: tuple[str, ...]
    planner_instruction: str
    answer_instruction: str
    starter_questions: tuple[str, ...]

    def public_dict(self) -> dict:
        data = asdict(self)
        data.pop("planner_instruction")
        data.pop("answer_instruction")
        return data


MODES: tuple[QAMode, ...] = (
    QAMode(
        name="ask",
        label="通用问答",
        description="解释教学问题，并给出有依据的可执行建议",
        placeholder="问任何教学相关的问题",
        retrieval_strategy="chunk",
        default_corpora=(
            "edu_theory",
            "pku_salon",
            "course_cases",
            "discipline_pedagogy",
            "teaching_cases",
            "AIMES",
        ),
        planner_instruction=(
            "覆盖问题中的核心教学概念、适用情境与可能的实践策略；保持查询简洁。"
        ),
        answer_instruction=(
            "直接回答问题，先给结论，再解释依据并给出可执行建议；不要机械套用固定模板。"
        ),
        starter_questions=(
            "如何提高大班课的学生参与度？",
            "教学目标怎么写才算可测量？",
            "课堂提问后应该等待多久？",
            "板书和课件应该怎么分工？",
        ),
    ),
    QAMode(
        name="syllabus_design",
        label="大纲设计",
        description="匹配内容相近课程，设计目标、内容、进度与评价体系",
        placeholder="描述拟开课程、学生层次、学时和希望解决的大纲问题",
        retrieval_strategy="course_match",
        default_corpora=(
            "teaching_cases",
            "course_cases",
            "discipline_pedagogy",
            "edu_theory",
        ),
        planner_instruction=(
            "优先生成可用于匹配相似课程的中英文查询：包括学科主题、关键概念、课程层次，"
            "并补充学习目标、课程组织或考核方式等设计维度。"
        ),
        answer_instruction=(
            "围绕课程大纲层级作答。依次给出需求与必要假设、相似课程及匹配理由、可迁移做法、"
            "课程目标、内容与进度、教学形式、考核方式，以及目标-活动-评价的一致性。"
            "清楚区分来源事实与本次设计建议；有来源网址时提示用户追溯原文。"
        ),
        starter_questions=(
            "为一门本科人工智能导论设计课程大纲",
            "帮我匹配与数字人文内容相近的国外课程",
            "如何让课程目标、周计划和考核方式保持一致？",
            "参考相似课程重新设计这门课的评价结构",
        ),
    ),
    QAMode(
        name="teaching_design",
        label="教学设计",
        description="按问题粒度设计教学策略、活动、课次或单元方案",
        placeholder="描述教学主题、学生情况和当前难点；需要完整流程时再提供课时",
        retrieval_strategy="case_match",
        default_corpora=(
            "teaching_cases",
            "pku_salon",
            "discipline_pedagogy",
            "edu_theory",
            "AIMES",
        ),
        planner_instruction=(
            "围绕具体知识主题、学习难点、学生特征、教学活动与形成性评价生成查询；"
            "若问题涉及生成式 AI，再加入 AI 教学策略或课程政策侧面的查询。"
        ),
        answer_instruction=(
            "先判断教师问题的粒度，直接解决当前问题，不要把所有回答机械展开成完整教案。回答按"
            "以下顺序组织：1.学习目标；2.学情假设与难点；3.案例匹配；4.解决方案；5.形成性评价"
            "设计；6.实施风险。各部分的详细程度应与问题粒度匹配；若教师只问一种方法、一个活动或"
            "某个教学难点，就围绕该问题简洁填写这些部分，不额外扩写完整课时流程。只有教师明确"
            "要求完整课次或单元方案时，才在解决方案中展开教学阶段、师生活动和课后衔接。不要默认"
            "90分钟或任何固定时长。"
            "教师给出总课时时，按该时长安排；未给出时，优先使用阶段比例、时间范围或可伸缩方案，"
            "只有时长会实质改变方案且无法合理作答时才提示教师补充。若上方资料中存在与当前问题"
            "直接相关、匹配度较高的“完整教学案例”，可在解决方案前用一个简短小节列出相关案例，"
            "每个案例只说明它与当前问题的关联和最值得迁移的做法，并标注来源编号；案例数量和篇幅"
            "服从相关性，不为凑格式罗列弱相关案例。若案例都只是主题相近、情境或做法并不相似，"
            "省略案例小节，直接回答。北大教学沙龙、教育理论和学科教学资料只能作为补充依据，不得"
            "称为教学案例。案例部分原则上不超过回答篇幅的四分之一，主体篇幅必须用于结合当前课程"
            "形成具体、可执行的解决方案。形成性评价设计要说明如何在教学过程中判断学生是否达到"
            "学习目标；实施风险要指出最可能影响落地的条件及应对办法。明确区分案例原有做法与本次"
            "适配建议。"
        ),
        starter_questions=(
            "这节课内容很多，怎样确定应该重点讲什么？",
            "怎样讲清一个学生普遍觉得抽象的概念？",
            "为一次3小时研讨课设计能检查真实理解的活动",
            "允许学生使用生成式AI时，作业怎样设计更合适？",
        ),
    ),
    QAMode(
        name="learning_diagnosis",
        label="学情诊断",
        description="根据作业、课堂表现或评估报告识别问题并提出干预方案",
        placeholder="描述诊断问题，也可以上传作业、成绩表或选择历史评估报告",
        retrieval_strategy="evidence_first",
        default_corpora=(
            "edu_theory",
            "discipline_pedagogy",
            "pku_salon",
        ),
        planner_instruction=(
            "从知识掌握、错误类型、认知过程、学习投入和教学支持等角度生成查询；"
            "不要把尚未提供的数据写成事实。"
        ),
        answer_instruction=(
            "先界定数据范围和诊断限制，再按证据列出主要问题、可能原因及置信程度，"
            "区分可直接观察的现象与推断；随后给出学生分组、针对性干预和下一轮验证方式。"
            "若没有学生作业、表现数据或指定评估报告，先说明当前只能形成诊断框架，"
            "并列出完成诊断所需的最少材料。"
        ),
        starter_questions=(
            "根据这批作业中的错误诊断学生的主要困难",
            "分析我选择的课堂评估报告并制定改进计划",
            "如何区分概念没理解和练习不足？",
            "为不同学习水平的学生设计分层干预方案",
        ),
    ),
)

MODE_MAP = {mode.name: mode for mode in MODES}
DEFAULT_MODE = "ask"


def get_mode(name: str | None) -> QAMode:
    return MODE_MAP.get(name or DEFAULT_MODE, MODE_MAP[DEFAULT_MODE])


def public_modes() -> list[dict]:
    return [mode.public_dict() for mode in MODES]
