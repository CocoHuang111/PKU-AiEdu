"""Shared evaluation export formatting for downloads and notification attachments."""
from datetime import datetime
from pathlib import Path
from ai_engine.evaluation.pipeline import strip_report_digest
from ai_engine.syllabus import export_syllabus
from ai_engine.syllabus.export import export_filename


def report_title(task):
    return f"{Path(task.get('filename') or '课堂').stem} · 教学评估报告"


def build_export_markdown(task, report):
    result = task.get('result') or {}
    overall = result.get('overall') or {}
    lines = [f'# {report_title(task)}', '']
    ts = task.get('created_at') or task.get('updated_at')
    if ts:
        try:
            generated = datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M')
            lines.append(f'- **生成日期**：{generated}')
        except (TypeError, ValueError, OSError):
            pass
    score = overall.get('score')
    if score is not None:
        grade, label = overall.get('grade') or '', overall.get('grade_label') or ''
        extra = f'（{grade} 级' + (f' · {label}' if label else '') + '）' if grade else ''
        lines.append(f'- **综合得分**：{score} / 100{extra}')
    minutes = overall.get('duration_minutes')
    if minutes not in (None, ''):
        lines.append(f'- **课堂时长**：{minutes} 分钟')
    source = '讲稿评估' if result.get('source') == 'transcript' else '视频评估'
    lines.append(f'- **评估方式**：{source}')
    labels = {'audio': '音频', 'text': '文本', 'vision': '图像'}
    mods = [labels.get(m, m) for m in (overall.get('modalities') or []) if m]
    if mods:
        lines.append(f"- **可用模态**：{'、'.join(mods)}")
    used = []
    if result.get('transcript_source') == 'script' or task.get('has_script'):
        used.append('讲稿')
    if result.get('has_syllabus') or task.get('has_syllabus'):
        used.append('课程大纲')
    if result.get('has_courseware') or task.get('has_courseware'):
        used.append('上传课件')
    if used:
        lines.append(f"- **对照材料**：{'、'.join(used)}")
    lines.extend(['', '---', '', strip_report_digest(report).strip(), ''])
    return '\n'.join(lines)


def render_report_pdf(task):
    report = ((task.get('result') or {}).get('report') or '').strip()
    if not report:
        raise ValueError('没有可导出的诊断报告')
    content, _, suffix = export_syllabus(build_export_markdown(task, report), 'pdf')
    return content, export_filename(report_title(task), suffix)
