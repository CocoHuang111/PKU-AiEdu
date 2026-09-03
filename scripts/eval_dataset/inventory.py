"""扫描教师文件夹、按姓名匹配打分表、判定视频/大纲/课件。"""

from __future__ import annotations

import csv
import re
import statistics
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]

from .xlsx import read_sheet_rows  # noqa: E402

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm", ".wmv"}
PPT_EXT = {".ppt", ".pptx"}
DOC_EXT = {".doc", ".docx"}
SYLLABUS_PDF_MARKERS = ("大纲", "教案", "备课")
IGNORE_NAME_MARKERS = ("考核证明", "证明")
HANDOUT_MARKERS = ("讲义", "handout", "讲稿")
FINDER_COPY_SUFFIX = " (2)"

# 文件夹名里的噪音，抽取中文姓名时去掉这些词
NOISE_PHRASES = (
    "大赛视频",
    "微格评审未通过",
    "提交评审未通过",
    "微格评审",
    "未通过",
    "视频很小",
    "后交",
    "可以",
    "前沿交叉",
    "青教视频",
    "403微格",
    "评审后重新录制通过",
    "评审后重新录制",
    "评审后重新提交",
    "提交了青教比赛的视频",
    "自己拍摄的",
)

CJK = re.compile(r"[\u4e00-\u9fff]{2,4}")
# 2022：01-楚健春-数学科学学院.mp4 / 54-青教赛-李阿明-工学院.pptx
FLAT_STEM = re.compile(
    r"^(?P<seq>\d+)-(?:青教赛-)?(?P<name>[\u4e00-\u9fff]{2,4})-(?P<dept>.+)$"
)
FLAT_DIR_MIN_FILES = 8
SCORE_COL_ALIASES = ("平均分", "平均分数")
COMMENT_COL_ALIASES = ("评语", "汇总评语-ZX")
DEPT_MARKERS = ("学院", "学系", "研究院", "中心", "教研部", "研究所", "系")
LATIN_NAME = re.compile(r"[A-Za-z][A-Za-z .'-]+")


def iter_teacher_dirs(root: Path) -> list[Path]:
    """叶子教师文件夹：自己有文件，或没有子目录（空文件夹也算）。"""
    root = root.resolve()
    found: list[Path] = []
    for dirpath, dirnames, filenames in os_walk_sorted(root):
        p = Path(dirpath)
        if p == root:
            continue
        real_files = [
            f
            for f in filenames
            if not f.startswith(".") and not f.startswith("~$")
        ]
        if real_files or not dirnames:
            found.append(p)
    return found


def os_walk_sorted(root: Path):
    import os

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        filenames.sort()
        yield dirpath, dirnames, filenames


def chinese_runs(folder_name: str) -> list[str]:
    cleaned = folder_name
    for phrase in NOISE_PHRASES:
        cleaned = cleaned.replace(phrase, " ")
    cleaned = re.sub(r"\d+", " ", cleaned)
    return CJK.findall(cleaned)


def match_score_row(
    folder_name: str, score_rows: list[dict[str, str]], name_col: str, dept_col: str
) -> tuple[dict[str, str] | None, str]:
    """文件夹名包含打分表姓名。重名再比院系关键字。"""
    hits = [r for r in score_rows if r.get(name_col) and r[name_col] in folder_name]
    if not hits:
        return None, "no_score"
    if len(hits) == 1:
        return hits[0], ""
    dept_hits = []
    for r in hits:
        dept = r.get(dept_col, "")
        keys = [k for k in re.findall(r"[\u4e00-\u9fff]{2,}", dept) if k not in ("学院", "大学")]
        if any(k and k in folder_name for k in keys):
            dept_hits.append(r)
    if len(dept_hits) == 1:
        return dept_hits[0], ""
    return hits[0], "name_ambiguous"


def relpath(path: Path | str | None) -> str:
    if not path:
        return ""
    p = Path(path).resolve()
    try:
        return str(p.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(p)


def should_ignore(path: Path) -> bool:
    stem = path.stem
    if path.name.startswith(".") or path.name.startswith("~$"):
        return True
    return any(m in stem for m in IGNORE_NAME_MARKERS)


def parse_flat_stem(stem: str) -> tuple[str, str, str] | None:
    """编号-姓名-院系；青教赛前缀可有可无。院系段须带学院/系等，避免 403-光华-肖潇。"""
    m = FLAT_STEM.match(stem.strip())
    if not m:
        return None
    dept = m.group("dept")
    if not any(k in dept for k in DEPT_MARKERS):
        return None
    return m.group("seq"), m.group("name"), dept


def parse_name_id_stem(stem: str) -> str | None:
    """2024：张亿.mp4 / 刘允-2140.pdf / ALAA ELDIN …-3787.pdf。不抢 2022 编号-姓名-院系。"""
    if parse_flat_stem(stem):
        return None
    s = stem.strip()
    m = re.match(r"^(.+)-(\d{3,})$", s)
    if m:
        return m.group(1).strip()
    if CJK.fullmatch(s):
        return s
    if LATIN_NAME.fullmatch(s) and " " in s:
        return s
    return None


def person_name_from_file(stem: str) -> str | None:
    parsed = parse_flat_stem(stem)
    if parsed:
        return parsed[1]
    return parse_name_id_stem(stem)


def match_file_name_to_score(file_name: str, score_names: list[str]) -> str | None:
    """文件名是打分表姓名，或英文名少了末尾姓氏（AKEF）。"""
    if file_name in score_names:
        return file_name
    fn = file_name.casefold()
    hits = [
        n
        for n in score_names
        if n.casefold().startswith(fn) or fn.startswith(n.casefold())
    ]
    if len(hits) == 1:
        return hits[0]
    return None


def find_flat_containers(root: Path) -> list[Path]:
    """备课/试讲这类目录：自己堆着一堆编号文件，不是一人一夹。"""
    found: list[Path] = []
    for dirpath, _dirnames, filenames in os_walk_sorted(root):
        n = sum(1 for f in filenames if person_name_from_file(Path(f).stem))
        if n >= FLAT_DIR_MIN_FILES:
            found.append(Path(dirpath))
    return found


def classify_files(folder: Path) -> dict[str, Any]:
    files = [
        p
        for p in sorted(folder.iterdir())
        if p.is_file() and not should_ignore(p)
    ]
    return classify_file_list(files)


def classify_file_list(files: list[Path]) -> dict[str, Any]:
    videos: list[Path] = []
    ppts: list[Path] = []
    docs: list[Path] = []
    pdfs: list[Path] = []
    others: list[str] = []
    review_needed: list[str] = []

    for p in sorted(files, key=lambda x: x.name):
        if not p.is_file() or should_ignore(p):
            continue
        ext = p.suffix.lower()
        if ext in VIDEO_EXT:
            videos.append(p)
        elif ext in PPT_EXT:
            ppts.append(p)
        elif ext in DOC_EXT:
            docs.append(p)
        elif ext == ".pdf":
            pdfs.append(p)
        elif ext in {".xlsx", ".xls"}:
            continue
        else:
            others.append(p.name)

    video, alt_videos, video_note = pick_video(videos)
    if len(videos) > 1:
        review_needed.append("multi_video")

    courseware, cw_note = pick_courseware(ppts, pdfs)
    if cw_note:
        review_needed.append(cw_note)

    syllabus = pick_syllabus(docs, pdfs, has_ppt=bool(ppts))
    if not syllabus and pdfs and not ppts:
        # 仅 PDF：无大纲关键词时默认当课件（已在 pick_courseware）
        pass

    skip = ""
    if video is None:
        skip = "no_video"

    return {
        "video_path": relpath(video) if video else "",
        "alt_videos": ";".join(relpath(p) for p in alt_videos),
        "syllabus_path": relpath(syllabus) if syllabus else "",
        "courseware_path": relpath(courseware) if courseware else "",
        "review_needed": ",".join(review_needed),
        "other_files": ";".join(others),
        "skip_media": skip,
        "video_pick_note": video_note,
    }


def pick_video(videos: list[Path]) -> tuple[Path | None, list[Path], str]:
    if not videos:
        return None, [], ""
    if len(videos) == 1:
        return videos[0], [], ""

    def rank(p: Path) -> tuple[int, int, int]:
        name = p.stem
        prefer = 1 if any(
            k in name for k in ("合成", "调整", "微格教学", "教学视频", "试讲")
        ) else 0
        penalize = 1 if any(k in name for k in ("小", "Compress", "compress")) else 0
        try:
            size = p.stat().st_size
        except OSError:
            size = 0
        return (prefer, -penalize, size)

    ordered = sorted(videos, key=rank, reverse=True)
    chosen = ordered[0]
    alts = [p for p in ordered if p != chosen]
    return chosen, alts, "heuristic_multi_video"


def is_valid_pptx(path: Path) -> bool:
    """能当 Office Open XML 打开。截断 zip / 旧版 OLE 改后缀的会失败。"""
    if path.suffix.lower() != ".pptx" or not path.is_file():
        return False
    try:
        import zipfile

        with zipfile.ZipFile(path) as z:
            names = z.namelist()
        return "[Content_Types].xml" in names or any(n.startswith("ppt/") for n in names)
    except Exception:
        return False


def pick_courseware(ppts: list[Path], pdfs: list[Path]) -> tuple[Path | None, str]:
    if ppts:
        notes: list[str] = []
        if len(ppts) > 1:
            notes.append("multi_ppt")
        pptx_ok = [p for p in ppts if p.suffix.lower() == ".pptx" and is_valid_pptx(p)]
        ppt = [p for p in ppts if p.suffix.lower() == ".ppt"]
        pptx_bad = [p for p in ppts if p.suffix.lower() == ".pptx" and not is_valid_pptx(p)]
        if pptx_ok:
            chosen = pptx_ok[0]
        elif ppt:
            chosen = ppt[0]
            if pptx_bad:
                notes.append("pptx_invalid_use_ppt")
        elif pptx_bad:
            chosen = pptx_bad[0]
            notes.append("pptx_invalid")
        else:
            chosen = ppts[0]
        return chosen, ",".join(notes)
    syllabusish = [p for p in pdfs if any(m in p.stem for m in SYLLABUS_PDF_MARKERS)]
    leftover = [p for p in pdfs if p not in syllabusish]
    if leftover:
        handout = [p for p in leftover if any(m.lower() in p.stem.lower() for m in HANDOUT_MARKERS)]
        chosen = leftover[0]
        note = "pdf_as_courseware"
        if handout:
            note = "pdf_handout_as_courseware"
        return chosen, note
    return None, ""


def comment_from_row(row: dict[str, str], comment_col: str) -> str:
    """2018「评语」；2019「整体优点 / 需要改进」；2022「突出优点 / 需要改进」；
    2024「汇总评语-ZX」，另把「备注」接上。"""
    if (row.get("_merged_comment") or "").strip():
        body = row["_merged_comment"].strip()
    else:
        text = (row.get(comment_col) or "").strip()
        if text:
            body = text
        else:
            parts: list[str] = []
            plus = (row.get("整体优点") or row.get("突出优点") or "").strip()
            minus = (row.get("需要改进") or "").strip()
            if plus:
                parts.append(f"优点：{plus}")
            if minus:
                parts.append(f"改进：{minus}")
            body = "\n".join(parts)
    remark = (row.get("备注") or "").strip()
    if remark:
        return f"{body}\n备注：{remark}" if body else f"备注：{remark}"
    return body


def resolve_score_col(headers: list[str], score_col: str) -> str:
    if score_col in headers:
        return score_col
    for alt in SCORE_COL_ALIASES:
        if alt in headers:
            return alt
    return score_col


def resolve_comment_col(headers: list[str], comment_col: str) -> str:
    if comment_col in headers:
        return comment_col
    for alt in COMMENT_COL_ALIASES:
        if alt in headers:
            return alt
    return comment_col


def expert_score_cols(headers: list[str]) -> list[str]:
    """专家1 / 专家2 是分数；「专家」是人名，「专家账号」不是分。"""
    cols = [c for c in headers if re.fullmatch(r"专家\d+", c)]

    def sort_key(c: str) -> tuple[int, int | str]:
        rest = c[2:]
        return (0, int(rest)) if rest.isdigit() else (1, c)

    return sorted(cols, key=sort_key)


def collect_expert_cols(rows: list[dict[str, str]]) -> list[str]:
    seen: list[str] = []
    for r in rows:
        for c in expert_score_cols(list(r.keys())):
            if c not in seen:
                seen.append(c)
    cols = expert_score_cols(seen)
    if cols:
        return cols
    keys = list(rows[0].keys()) if rows else []
    # 2024：一人一行，「分数」是某一位专家分，「平均分」才是标签
    if "分数" in keys and any(k in keys for k in SCORE_COL_ALIASES):
        return ["分数"]
    return cols


def merge_expert_comments(rows: list[dict[str, str]]) -> str:
    parts: list[str] = []
    for r in rows:
        expert = (r.get("专家") or "").strip()
        plus = (r.get("突出优点") or r.get("整体优点") or "").strip()
        minus = (r.get("需要改进") or "").strip()
        chunks: list[str] = []
        if plus:
            chunks.append(f"优点：{plus}")
        if minus:
            chunks.append(f"改进：{minus}")
        if not chunks:
            continue
        body = "；".join(chunks)
        parts.append(f"[{expert}] {body}" if expert else body)
    return "\n".join(parts)


def collapse_long_score_table(
    score_rows: list[dict[str, str]], name_col: str, score_col: str
) -> tuple[list[dict[str, str]], str]:
    """同一姓名多行（每位专家一行）合成一人一行。均分用「平均分数」，评语全保留。"""
    from collections import OrderedDict

    groups: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    for r in score_rows:
        name = (r.get(name_col) or "").strip()
        if name:
            groups.setdefault(name, []).append(r)
    multi = sum(1 for rows in groups.values() if len(rows) > 1)
    keys = list(score_rows[0].keys()) if score_rows else []
    long_form = "专家" in keys and any("总体评价" in c for c in keys)
    if not groups or multi == 0 or not (long_form or multi >= max(3, len(groups) // 4)):
        return score_rows, score_col

    resolved = resolve_score_col(keys, score_col)
    per_score = next((c for c in keys if "总体评价" in c), "")
    max_n = max(len(rows) for rows in groups.values())

    collapsed: list[dict[str, str]] = []
    for _name, rows in groups.items():
        merged = dict(rows[0])
        avg = None
        for r in rows:
            avg = _to_float(r.get(resolved, ""))
            if avg is not None:
                break
        # 有均分列就用均分；缺了才退回各位专家「总体评价」的算术平均
        if avg is None and per_score:
            vals = [_to_float(r.get(per_score, "")) for r in rows]
            vals = [v for v in vals if v is not None]
            if vals:
                avg = round(sum(vals) / len(vals), 4)
        merged[resolved] = str(avg) if avg is not None else ""
        if resolved != score_col:
            merged[score_col] = merged[resolved]
        if per_score:
            for i in range(1, max_n + 1):
                merged[f"专家{i}"] = rows[i - 1].get(per_score, "") if i <= len(rows) else ""
        merged["_merged_comment"] = merge_expert_comments(rows)
        if per_score and len(rows) < max_n:
            merged["_incomplete_experts"] = "1"
        collapsed.append(merged)
    return collapsed, resolved


def pick_syllabus(docs: list[Path], pdfs: list[Path], has_ppt: bool) -> Path | None:
    if docs:
        return docs[0]
    marked = [p for p in pdfs if any(m in p.stem for m in SYLLABUS_PDF_MARKERS)]
    if marked:
        return marked[0]
    return None


def _to_float(raw: str) -> float | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def expert_total_100(avg: float, score_min: float, score_max: float) -> float:
    """把专家原始分按满分直接换算为百分制。

    评分表中的 ``score_min=2`` 是及格线，不是量表零点；因此 2/4 应为
    50 分，不能用 min-max 拉伸成 0 分。保留 score_min 参数是为了兼容
    inventory 的命令行接口。
    """
    if score_max <= 0:
        return avg
    return round(avg / score_max * 100.0, 2)


def _score_fields(
    row: dict[str, str] | None,
    *,
    name_col: str,
    dept_col: str,
    score_col: str,
    comment_col: str,
    expert_cols: list[str],
    fallback_dept: str = "",
) -> tuple[str, str, str, float | None, dict[str, float | None], str]:
    name = ""
    dept = fallback_dept
    comment = ""
    avg = None
    experts: dict[str, float | None] = {}
    extra_skip = ""
    if row is None:
        return name, dept, comment, avg, experts, "no_score"
    name = row.get(name_col, "")
    dept = row.get(dept_col, "") or fallback_dept
    comment = comment_from_row(row, comment_col)
    avg = _to_float(row.get(score_col, ""))
    for c in expert_cols:
        experts[c] = _to_float(row.get(c, ""))
    if avg is None:
        extra_skip = "no_score"
    return name, dept, comment, avg, experts, extra_skip


def _finish_record(
    *,
    folder_name: str,
    folder_rel: str,
    files: dict[str, Any],
    name: str,
    dept: str,
    comment: str,
    avg: float | None,
    experts: dict[str, float | None],
    expert_cols: list[str],
    match_note: str,
    extra_skip: str,
    score_min: float,
    score_max: float,
    incomplete_experts: bool = False,
) -> dict[str, Any]:
    skip = files["skip_media"] or extra_skip
    std = None
    vals = [v for v in experts.values() if v is not None]
    if len(vals) >= 2:
        std = round(statistics.pstdev(vals), 4)
    notes = [n for n in (files["review_needed"], match_note) if n]
    if incomplete_experts:
        notes.append("incomplete_experts")
    rec: dict[str, Any] = {
        "video_id": name or folder_name,
        "folder_name": folder_name,
        "folder_rel": folder_rel,
        "name": name,
        "dept": dept,
        "video_path": files["video_path"],
        "syllabus_path": files["syllabus_path"],
        "courseware_path": files["courseware_path"],
        "alt_videos": files["alt_videos"],
        "review_needed": ",".join(notes),
        "skip": skip,
        "expert_avg": avg if avg is not None else "",
        "score_std": std if std is not None else "",
        "comment": comment,
        "expert_total_100": (
            expert_total_100(avg, score_min, score_max) if avg is not None else ""
        ),
    }
    for i, c in enumerate(expert_cols, start=1):
        rec[f"expert{i}"] = experts.get(c) if experts.get(c) is not None else ""
    rec["n_experts"] = len(vals)
    return rec


def build_flat_inventory(
    root: Path,
    score_rows: list[dict[str, str]],
    *,
    name_col: str,
    dept_col: str,
    score_col: str,
    comment_col: str,
    expert_cols: list[str],
    score_min: float,
    score_max: float,
) -> list[dict[str, Any]]:
    """按文件名把备课/试讲拼成一人一条。支持 2022「编号-姓名-院系」和 2024「姓名-学号」。"""
    by_file_name: dict[str, list[Path]] = {}
    file_dept: dict[str, str] = {}
    file_seq: dict[str, str] = {}
    for dirpath, _dirnames, filenames in os_walk_sorted(root):
        for fn in filenames:
            p = Path(dirpath) / fn
            if should_ignore(p):
                continue
            parsed = parse_flat_stem(p.stem)
            if parsed:
                seq, name, dept = parsed
                by_file_name.setdefault(name, []).append(p)
                file_dept.setdefault(name, dept)
                file_seq.setdefault(name, seq)
                continue
            name = parse_name_id_stem(p.stem)
            if name:
                by_file_name.setdefault(name, []).append(p)

    score_by_name: dict[str, dict[str, str]] = {}
    for r in score_rows:
        name = (r.get(name_col) or "").strip()
        if name and name not in score_by_name:
            score_by_name[name] = r
    score_names = list(score_by_name)

    bound: dict[str, list[Path]] = {n: [] for n in score_names}
    leftover: dict[str, list[Path]] = {}
    for fname, paths in by_file_name.items():
        hit = match_file_name_to_score(fname, score_names)
        if hit:
            bound[hit].extend(paths)
            if fname in file_dept and hit not in file_dept:
                file_dept[hit] = file_dept[fname]
                file_seq[hit] = file_seq.get(fname, "")
        else:
            leftover[fname] = paths

    names = sorted(set(bound) | set(leftover))
    inventory: list[dict[str, Any]] = []
    for name in names:
        paths = bound.get(name) or leftover.get(name) or []
        files = classify_file_list(paths)
        seq = file_seq.get(name, "")
        dept_from_file = file_dept.get(name, "")
        folder_name = f"{seq}-{name}-{dept_from_file}" if seq else name
        folder_rel = "flat"
        if paths:
            try:
                parents = sorted({str(p.parent.relative_to(root)) for p in paths})
            except ValueError:
                parents = sorted({str(p.parent) for p in paths})
            folder_rel = "flat:" + "+".join(parents)
        row = score_by_name.get(name)
        match_note = "" if row or not paths else "no_score"
        sname, dept, comment, avg, experts, extra_skip = _score_fields(
            row,
            name_col=name_col,
            dept_col=dept_col,
            score_col=score_col,
            comment_col=comment_col,
            expert_cols=expert_cols,
            fallback_dept=dept_from_file,
        )
        inventory.append(
            _finish_record(
                folder_name=folder_name,
                folder_rel=folder_rel,
                files=files,
                name=sname or name,
                dept=dept,
                comment=comment,
                avg=avg,
                experts=experts,
                expert_cols=expert_cols,
                match_note=match_note,
                extra_skip=extra_skip,
                score_min=score_min,
                score_max=score_max,
                incomplete_experts=bool(row and row.get("_incomplete_experts")),
            )
        )
    return inventory


def build_inventory(
    root: Path,
    xlsx: Path,
    *,
    name_col: str = "姓名",
    dept_col: str = "院系",
    score_col: str = "平均分",
    comment_col: str = "评语",
    score_min: float = 2.0,
    score_max: float = 4.0,
    skip_dir_prefix: str = "",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    score_rows = read_sheet_rows(xlsx)
    if not score_rows:
        raise RuntimeError(f"打分表为空：{xlsx}")
    if name_col not in score_rows[0]:
        raise RuntimeError(f"打分表没有「{name_col}」列，实际列：{list(score_rows[0])}")

    score_col = resolve_score_col(list(score_rows[0].keys()), score_col)
    comment_col = resolve_comment_col(list(score_rows[0].keys()), comment_col)
    score_rows, score_col = collapse_long_score_table(score_rows, name_col, score_col)
    expert_cols = collect_expert_cols(score_rows)

    if find_flat_containers(root):
        inventory = build_flat_inventory(
            root,
            score_rows,
            name_col=name_col,
            dept_col=dept_col,
            score_col=score_col,
            comment_col=comment_col,
            expert_cols=expert_cols,
            score_min=score_min,
            score_max=score_max,
        )
    else:
        inventory = []
        for folder in iter_teacher_dirs(root):
            if folder.name.endswith(FINDER_COPY_SUFFIX):
                continue
            rel = str(folder.relative_to(root))
            if skip_dir_prefix and rel.startswith(skip_dir_prefix):
                continue
            files = classify_files(folder)
            row, match_note = match_score_row(folder.name, score_rows, name_col, dept_col)
            sname, dept, comment, avg, experts, extra_skip = _score_fields(
                row,
                name_col=name_col,
                dept_col=dept_col,
                score_col=score_col,
                comment_col=comment_col,
                expert_cols=expert_cols,
            )
            inventory.append(
                _finish_record(
                    folder_name=folder.name,
                    folder_rel=rel,
                    files=files,
                    name=sname,
                    dept=dept,
                    comment=comment,
                    avg=avg,
                    experts=experts,
                    expert_cols=expert_cols,
                    match_note=match_note,
                    extra_skip=extra_skip,
                    score_min=score_min,
                    score_max=score_max,
                    incomplete_experts=bool(row and row.get("_incomplete_experts")),
                )
            )

    inventory.sort(key=lambda r: (r["skip"] or "", r["name"] or r["folder_name"]))
    manifest = [r for r in inventory if not r["skip"]]
    return inventory, manifest


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for r in rows:
        for k in r:
            if k not in fieldnames:
                fieldnames.append(k)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n"
        )
        w.writeheader()
        w.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))
