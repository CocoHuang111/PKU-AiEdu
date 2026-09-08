"""大纲优化的单元测试：XML/Markdown 校验、枚举归一化、分章生成、导出。

不调真实大模型。运行：

    python -m unittest scripts.test_syllabus_validation
    make check-syllabus
"""

from __future__ import annotations

import unittest
from decimal import Decimal
from unittest.mock import patch

from lxml import etree

from ai_engine.pedagogy.loader import read_schema_file
from ai_engine.syllabus.export import export_syllabus, xml_to_markdown
from ai_engine.syllabus.optimizer import (
    _generate_staged_schema_xml,
    _locate_chapter_start,
    _normalize_schema_assessment_types,
    _normalize_schema_enums,
    _parse_chapter_index,
    _parse_hours_text,
    _resolve_activity_type,
    _resolve_assessment_type,
    _sanitize_llm_xml,
    _should_skip_llm_repair,
    _strip_markdown_wrapper,
    _ensure_leading_atx,
    detect_output_format,
    extract_course_name_from_markdown,
    optimize_text,
    validate_markdown,
    validate_schema_xml,
)


VALID_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<syllabus>
  <course>
    <name>测试课程</name>
    <code>TEST001</code>
    <credits>2</credits>
    <total_hours>4</total_hours>
    <discipline>测试学科</discipline>
    <audience>本科二年级学生</audience>
    <prerequisites>待教师确认</prerequisites>
    <description>本课程介绍测试所需的核心概念与基本方法，帮助学生建立分析框架并完成案例实践。</description>
  </course>
  <objectives>
    <objective id="O1" level="应用" origin="clarified">
      <statement>学生能够运用课程中的核心原理分析并解决典型问题</statement>
    </objective>
  </objectives>
  <chapters>
    <chapter source_id="S1" index="1" origin="original">
      <title>第一章 核心原理</title>
      <hours>4</hours>
      <points>
        <point origin="original">界定核心概念及其相互关系</point>
        <point origin="clarified">说明原理适用的条件与分析边界</point>
      </points>
      <teaching_format>讲授、案例讨论</teaching_format>
    </chapter>
  </chapters>
  <assessment>
    <item id="A1" type="大作业" weight="100" origin="original">
      <description>通过综合案例报告评价目标达成情况</description>
      <ai_policy>待教师确认</ai_policy>
    </item>
  </assessment>
  <references/>
  <additional_sections/>
  <needs_confirmation>
    <item target="先修课程">请教师确认先修课程要求</item>
  </needs_confirmation>
  <improvements/>
</syllabus>
"""


class ValidateSchemaXmlTest(unittest.TestCase):
    def test_accepts_complete_schema_document(self) -> None:
        valid, error = validate_schema_xml(VALID_XML)
        self.assertTrue(valid, error)

    def test_repair_by_default_unless_blacklisted(self) -> None:
        self.assertFalse(
            _should_skip_llm_repair("章节学时合计 27，与总学时 48 不一致")
        )
        self.assertFalse(_should_skip_llm_repair("type 不在允许枚举中"))
        self.assertTrue(
            _should_skip_llm_repair("章节 source_id 覆盖或顺序错误：预期 ['S1']")
        )

    def test_rejects_empty_points_and_unbalanced_hours(self) -> None:
        xml = VALID_XML.replace(
            "<total_hours>4</total_hours>", "<total_hours>6</total_hours>"
        ).replace(
            "<point origin=\"clarified\">说明原理适用的条件与分析边界</point>",
            "<point origin=\"clarified\"></point>",
        )

        valid, error = validate_schema_xml(xml)

        self.assertFalse(valid)
        self.assertIn("不能为空或过短", error)
        self.assertIn("章节学时合计 4", error)
        self.assertFalse(_should_skip_llm_repair(error))

    def test_allows_unknown_numbers_to_wait_for_confirmation(self) -> None:
        xml = VALID_XML.replace(
            "<total_hours>4</total_hours>",
            "<total_hours>待教师确认</total_hours>",
        )
        xml = xml.replace("<hours>4</hours>", "<hours>待教师确认</hours>", 1)
        xml = xml.replace('weight="100"', 'weight="待教师确认"')

        valid, error = validate_schema_xml(xml)

        self.assertTrue(valid, error)

    def test_accepts_fuzzy_week_based_hours(self) -> None:
        xml = VALID_XML.replace("<hours>4</hours>", "<hours>约1.5 周</hours>", 1)
        xml = xml.replace('hours="4"', 'hours="2"', 1)

        valid, error = validate_schema_xml(xml)

        self.assertTrue(valid, error)
        self.assertEqual(_parse_hours_text("约1.5 周"), Decimal("1.5"))

    def test_skips_week_activity_balance_checks_for_outline_schema(self) -> None:
        xml = VALID_XML.replace("<hours>4</hours>", "<hours>1 周</hours>", 1)

        valid, error = validate_schema_xml(xml)

        self.assertTrue(valid, error)

    def test_accepts_common_assessment_aliases(self) -> None:
        xml = VALID_XML.replace('type="大作业"', 'type="课程项目"', 1)

        valid, error = validate_schema_xml(xml)

        self.assertTrue(valid, error)
        self.assertEqual(_resolve_assessment_type("课程项目"), "项目")

    def test_accepts_assessment_type_synonyms(self) -> None:
        xml = VALID_XML.replace(
            'type="大作业" weight="100"',
            'type="期末考试" weight="80"',
            1,
        ).replace(
            "<assessment>",
            '<assessment><item id="A0" type="平时成绩" weight="20" origin="original">'
            "<description>课堂参与与出勤</description>"
            "<ai_policy>待教师确认</ai_policy></item>",
            1,
        )

        normalized = _normalize_schema_enums(xml)

        self.assertIn('type="平时表现"', normalized)
        self.assertIn('type="期末"', normalized)
        valid, error = validate_schema_xml(normalized)
        self.assertTrue(valid, error)

    def test_resolve_activity_type_synonyms(self) -> None:
        self.assertEqual(_resolve_activity_type("案例教学"), "案例")
        self.assertEqual(_resolve_activity_type("翻转研讨"), "讨论")

    def test_unknown_activity_type_falls_back_to_other(self) -> None:
        self.assertEqual(_resolve_activity_type("神秘活动"), "其他")

    def test_normalizes_assessment_types_before_validation(self) -> None:
        xml = VALID_XML.replace('type="大作业"', 'type="论文"', 1)
        normalized = _normalize_schema_enums(xml)

        self.assertIn('type="大作业"', normalized)
        valid, error = validate_schema_xml(normalized)
        self.assertTrue(valid, error)

    def test_sanitize_bare_ampersands_before_validation(self) -> None:
        xml = VALID_XML.replace(
            "说明原理适用的条件与分析边界",
            "形成 model-free & model-based 的完整认知链条。",
        )

        valid, error = validate_schema_xml(xml)

        self.assertTrue(valid, error)
        self.assertIn("&amp;", _sanitize_llm_xml(xml))

    def test_export_hides_internal_source_metadata(self) -> None:
        markdown = xml_to_markdown(VALID_XML)

        self.assertNotIn("source_id", markdown)
        self.assertNotIn("origin=", markdown)


class FakeLlm:
    def __init__(self, outputs: list[str]) -> None:
        self.outputs = iter(outputs)
        self.prompts: list[str] = []

    def chat(self, messages) -> str:
        self.prompts.append(messages[-1].content)
        return next(self.outputs)


class StagedGenerationTest(unittest.TestCase):
    def test_locates_chapter_with_overlong_marker_prefix(self) -> None:
        original = (
            "前置说明\n"
            "1. 导论（1 周）：我们将重点介绍本课程的基本结构和主要内容，并讨论一些课程的时间安排。\n"
            "2. 强化学习中的基本要素（1 周）：介绍基本概念。"
        )
        marker = (
            "1. 导论（1 周）：我们将重点介绍本课程的基本结构和主要内容，"
            "并讨论一些课程的额外幻觉文本"
        )
        position, matched_len, match_mode = _locate_chapter_start(
            original,
            marker,
            "1. 导论（1 周）",
            0,
        )

        self.assertGreaterEqual(position, 0)
        self.assertIn("prefix", match_mode)
        self.assertGreater(matched_len, 12)

    def test_parse_chapter_index_accepts_prefix_marker(self) -> None:
        original = (
            "1. 导论（1 周）：我们将重点介绍本课程的基本结构和主要内容，并讨论一些课程的时间安排。\n"
            "2. 强化学习中的基本要素（1 周）：介绍基本概念。"
        )
        index_xml = """\
<chapter_index>
  <chapter source_id="S1" index="1">
    <title>1. 导论（1 周）</title>
    <start_marker>1. 导论（1 周）：我们将重点介绍本课程的基本结构和主要内容，并讨论一些课程的幻觉后缀</start_marker>
    <hours>1</hours>
  </chapter>
  <chapter source_id="S2" index="2">
    <title>2. 强化学习中的基本要素（1 周）</title>
    <start_marker>2. 强化学习中的基本要素（1 周）：介绍基本概念。</start_marker>
    <hours>1</hours>
  </chapter>
</chapter_index>
"""
        _, chapters = _parse_chapter_index(index_xml, original, max_chapters=10)

        self.assertEqual([chapter.source_id for chapter in chapters], ["S1", "S2"])
        self.assertIn("时间安排", chapters[0].source_content)

    def test_extracts_slices_and_assembles_chapters_in_source_order(self) -> None:
        original = (
            "课程名称：测试课程\n"
            "第一章 原理\n"
            "第一章的完整原始内容。\n"
            "第二章 应用\n"
            "第二章的完整原始内容。\n"
            "考核方式：课程报告。"
        )
        index_xml = """\
<chapter_index>
  <chapter source_id="S1" index="一">
    <title>第一章 原理</title>
    <start_marker>第一章 原理</start_marker>
    <hours>2</hours>
  </chapter>
  <chapter source_id="S2" index="二">
    <title>第二章 应用</title>
    <start_marker>第二章 应用</start_marker>
    <hours>2</hours>
  </chapter>
</chapter_index>
"""
        global_xml = """\
<syllabus>
  <course/>
  <objectives/>
  <chapters><chapter><title>不应保留</title></chapter></chapters>
  <assessment/>
  <references/>
  <additional_sections/>
  <needs_confirmation/>
  <improvements/>
</syllabus>
"""
        first_batch = """\
<chapters>
  <chapter source_id="S1" index="错误">
    <title>被模型改写的标题</title>
    <hours>99</hours>
    <points><point origin="original">第一章要点</point></points>
  </chapter>
</chapters>
"""
        second_batch = """\
<chapters>
  <chapter source_id="S2" index="错误">
    <title>另一个错误标题</title>
    <hours>99</hours>
    <points><point origin="original">第二章要点</point></points>
  </chapter>
</chapters>
"""
        llm = FakeLlm([index_xml, global_xml, first_batch, second_batch])

        xml, source_ids = _generate_staged_schema_xml(
            llm,
            original,
            read_schema_file("syllabus_schema.xml"),
            batch_size=1,
            max_chapters=10,
        )

        root = etree.fromstring(xml.encode("utf-8"))
        chapters = root.findall("chapters/chapter")
        self.assertEqual(source_ids, ["S1", "S2"])
        self.assertEqual(
            [chapter.findtext("title") for chapter in chapters],
            ["第一章 原理", "第二章 应用"],
        )
        self.assertEqual(
            [chapter.findtext("hours") for chapter in chapters],
            ["2", "2"],
        )
        self.assertIn("第一章的完整原始内容", llm.prompts[2])
        self.assertIn("第二章的完整原始内容", llm.prompts[3])

    def test_falls_back_to_single_generation_when_index_is_invalid(self) -> None:
        llm = FakeLlm(["<wrong_root/>", VALID_XML])

        with patch("ai_engine.syllabus.optimizer.settings") as mock_settings:
            mock_settings.section.return_value = {
                "max_input_chars": 80000,
                "prompt_template": "syllabus_optimize_schema.j2",
                "schema_file": "syllabus_schema.xml",
                "generation_strategy": "staged",
                "chapter_batch_size": 2,
                "max_staged_chapters": 30,
                "staged_fallback_to_single": True,
            }
            with patch("ai_engine.syllabus.optimizer.get_llm", return_value=llm):
                result = optimize_text(
                    "第一章 核心原理\n课程教学内容", prompt_mode="schema"
                )

        self.assertTrue(result["valid"], result["validation_error"])
        self.assertEqual(result["generation_strategy"], "single_fallback")
        self.assertIn("chapter_index", result["staged_fallback_reason"])


class MarkdownModeTests(unittest.TestCase):
    VALID_MD = """\
# 测试课程

## 课程信息

- **课程名称**：测试课程
- **学分**：2

## 教学目标

### 目标 1

- **层次**：理解
- **表述**：学生能够说明课程核心概念
- **达成证据**：课堂测验

## 教学内容

### 第 1 章 · 导论

- **学时**：2
- **章节概述**：介绍课程背景与基本概念，帮助学生建立整体认知框架。

#### 知识主题 1 · 核心概念

- **内容阐述**：说明课程涉及的基本术语及其相互关系，并给出简单示例。
- **核心概念**：概念 A、概念 B

## 优化说明

1. 将模糊目标改写为可测量表述 — 依据：原大纲「了解基本概念」
"""

    def test_validate_markdown_requires_heading(self) -> None:
        valid, error = validate_markdown(self.VALID_MD)
        self.assertTrue(valid, error)
        # 过短的输入在标题检查之前就会失败，不能拿它测「缺标题」
        valid, error = validate_markdown("只有正文没有标题结构")
        self.assertFalse(valid)
        self.assertIn("过短", error)
        no_heading = "这是一段没有任何 Markdown 标题的课堂大纲正文，" * 5
        self.assertGreaterEqual(len(no_heading), 80)
        valid, error = validate_markdown(no_heading)
        self.assertFalse(valid)
        self.assertIn("标题", error)
        promoted = _ensure_leading_atx(no_heading)
        self.assertTrue(promoted.startswith("# "), promoted[:40])
        valid, error = validate_markdown(promoted)
        self.assertTrue(valid, error)

    def test_markdown_mode_promotes_plain_title_without_hash(self) -> None:
        body = "强化学习\n\n课程概述\n知其然，知其所以然。——《朱子语类》卷九《论知行》。\n" + (
            "这是正文段落，用来保证超过八十个字的校验下限。" * 3
        )

        class FakeLlm:
            def chat(self, messages, **kwargs):
                return body

        llm = FakeLlm()
        with patch("ai_engine.syllabus.optimizer.settings") as mock_settings:
            mock_settings.section.return_value = {
                "max_input_chars": 80000,
                "prompt_template": "syllabus_optimize.j2",
                "markdown_max_length_ratio": 2.0,
            }
            with patch("ai_engine.syllabus.optimizer.get_llm", return_value=llm):
                result = optimize_text("原始大纲内容足够长用于测试", prompt_mode="markdown")

        self.assertTrue(result["valid"], result["validation_error"])
        self.assertTrue(result["xml"].lstrip().startswith("# 强化学习"))
        self.assertEqual(result["course_name"], "强化学习")

    def test_strip_markdown_wrapper(self) -> None:
        wrapped = "说明文字\n```markdown\n# 课程\n\n正文\n```"
        self.assertTrue(_strip_markdown_wrapper(wrapped).startswith("# 课程"))
        # 正文已以一级标题开头时，后面的 ## 是结构，不能把 H1 切掉
        stripped = _strip_markdown_wrapper(self.VALID_MD)
        self.assertTrue(stripped.startswith("# 测试课程"), stripped[:40])

    def test_detect_output_format(self) -> None:
        self.assertEqual(detect_output_format("<?xml version='1.0'?><syllabus/>"), "xml")
        self.assertEqual(detect_output_format("# 课程\n正文"), "markdown")

    def test_extract_course_name_from_markdown(self) -> None:
        self.assertEqual(extract_course_name_from_markdown(self.VALID_MD), "测试课程")

    def test_export_markdown_source_as_markdown(self) -> None:
        content, media_type, suffix = export_syllabus(self.VALID_MD, "markdown")
        self.assertEqual(suffix, ".md")
        self.assertIn("text/markdown", media_type)
        self.assertIn("测试课程", content.decode("utf-8"))

    def test_validate_markdown_length_hint(self) -> None:
        valid, error = validate_markdown(self.VALID_MD, max_chars=50)
        self.assertTrue(valid)
        self.assertIn("超过建议上限", error)

    def test_markdown_mode_passes_length_limits_to_prompt(self) -> None:
        # 原文需超过 400 字，否则 max_output_chars 会落到 800 字下限，测不到「2 倍」这条路径
        original = "原始大纲内容足够长用于测试" * 40
        expected_max = len(original) * 2
        self.assertGreater(expected_max, 800)

        class FakeLlm:
            prompts: list[str] = []

            def chat(self, messages, **kwargs):
                FakeLlm.prompts.append(messages[-1].content)
                return MarkdownModeTests.VALID_MD

        llm = FakeLlm()
        with patch("ai_engine.syllabus.optimizer.settings") as mock_settings:
            mock_settings.section.return_value = {
                "max_input_chars": 80000,
                "prompt_template": "syllabus_optimize.j2",
                "markdown_max_length_ratio": 2.0,
            }
            with patch("ai_engine.syllabus.optimizer.get_llm", return_value=llm):
                result = optimize_text(original, prompt_mode="markdown_schema")

        self.assertEqual(result["output_format"], "markdown")
        self.assertTrue(result["valid"], result["validation_error"])
        self.assertEqual(result["prompt_mode"], "syllabus_optimize_markdown_schema.j2")
        self.assertEqual(result["original_char_count"], len(original))
        self.assertEqual(result["max_output_chars"], expected_max)
        self.assertIn(str(len(original)), llm.prompts[0])
        self.assertIn(str(expected_max), llm.prompts[0])
        self.assertIn("大纲级别", llm.prompts[0])
        self.assertIn("必须融合 AI 辅助教学", llm.prompts[0])
        self.assertNotIn("或整节省略", llm.prompts[0])

    def test_markdown_mode_uses_markdown_prompt(self) -> None:
        class FakeLlm:
            prompts: list[str] = []

            def chat(self, messages, **kwargs):
                FakeLlm.prompts.append(messages[-1].content)
                return MarkdownModeTests.VALID_MD

        llm = FakeLlm()
        with patch("ai_engine.syllabus.optimizer.settings") as mock_settings:
            mock_settings.section.return_value = {
                "max_input_chars": 80000,
                "prompt_template": "syllabus_optimize.j2",
                "markdown_max_length_ratio": 2.0,
            }
            with patch("ai_engine.syllabus.optimizer.get_llm", return_value=llm):
                result = optimize_text("原始大纲内容足够长用于测试", prompt_mode="markdown")

        self.assertEqual(result["output_format"], "markdown")
        self.assertTrue(result["valid"], result["validation_error"])
        self.assertEqual(result["prompt_mode"], "syllabus_optimize_markdown.j2")
        self.assertEqual(result["course_name"], "测试课程")
        prompt = llm.prompts[0]
        self.assertIn("灵活结构", prompt)
        self.assertIn("只在原来的基础上增补或删减", prompt)
        self.assertIn("禁止一律列表化", prompt)
        self.assertIn("必须融合 AI 辅助教学", prompt)
        self.assertIn("ATX", prompt)
        self.assertNotIn("否则省略", prompt)


if __name__ == "__main__":
    unittest.main()
