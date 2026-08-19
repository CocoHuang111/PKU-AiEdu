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
)

CJK = re.compile(r"[\u4e00-\u9fff]{2,4}")


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


def classify_files(folder: Path) -> dict[str, Any]:
    videos: list[Path] = []
    ppts: list[Path] = []
    docs: list[Path] = []
    pdfs: list[Path] = []
    others: list[str] = []
    review_needed: list[str] = []

    for p in sorted(folder.iterdir()):
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
        prefer = 1 if any(k in name for k in ("合成", "调整")) else 0
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


def pick_courseware(ppts: list[Path], pdfs: list[Path]) -> tuple[Path | None, str]:
    if ppts:
        pptx = [p for p in ppts if p.suffix.lower() == ".pptx"]
        chosen = pptx[0] if pptx else ppts[0]
        note = "multi_ppt" if len(ppts) > 1 else ""
        return chosen, note
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
    span = score_max - score_min
    if span <= 0:
        return avg
    return round((avg - score_min) / span * 100.0, 2)


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

    expert_cols = [c for c in score_rows[0] if c.startswith("专家")]
    inventory: list[dict[str, Any]] = []

    for folder in iter_teacher_dirs(root):
        rel = str(folder.relative_to(root))
        if skip_dir_prefix and rel.startswith(skip_dir_prefix):
            continue
        files = classify_files(folder)
        row, match_note = match_score_row(folder.name, score_rows, name_col, dept_col)
        skip = files["skip_media"]
        name = ""
        dept = ""
        comment = ""
        avg = None
        experts: dict[str, float | None] = {}
        if row is None:
            skip = skip or "no_score"
        else:
            name = row.get(name_col, "")
            dept = row.get(dept_col, "")
            comment = row.get(comment_col, "")
            avg = _to_float(row.get(score_col, ""))
            for c in expert_cols:
                experts[c] = _to_float(row.get(c, ""))
            if avg is None:
                skip = skip or "no_score"

        std = None
        vals = [v for v in experts.values() if v is not None]
        if len(vals) >= 2:
            std = round(statistics.pstdev(vals), 4)

        rec = {
            "video_id": name or folder.name,
            "folder_name": folder.name,
            "folder_rel": rel,
            "name": name,
            "dept": dept,
            "video_path": files["video_path"],
            "syllabus_path": files["syllabus_path"],
            "courseware_path": files["courseware_path"],
            "alt_videos": files["alt_videos"],
            "review_needed": files["review_needed"]
            + (("," + match_note) if match_note else ""),
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
        rec["n_experts"] = len(expert_cols)
        inventory.append(rec)

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
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))
