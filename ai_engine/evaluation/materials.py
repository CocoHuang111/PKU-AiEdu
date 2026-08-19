"""评估辅助材料：课程大纲文本抽取、课件翻成页面图像。

教师选填。有大纲就对照大纲安排评本节课完整性；有课件就以课件文件评版式，
不再拿教室录像截帧当课件设计的权威证据。
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from ..config import settings
from ..rag.loaders import SUPPORTED as DOC_SUPPORTED
from ..rag.loaders import UnsupportedDocument, load_document

SYLLABUS_EXT = set(DOC_SUPPORTED)
COURSEWARE_EXT = {".pdf", ".pptx", ".ppt"}

MAX_SYLLABUS_CHARS = 12000
MAX_COURSEWARE_TEXT_CHARS = 8000

SOFFICE_CANDIDATES = (
    "soffice",
    "libreoffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/usr/bin/soffice",
    "/usr/local/bin/soffice",
)


class MaterialError(RuntimeError):
    pass


def load_syllabus_text(path: str | Path, max_chars: int = MAX_SYLLABUS_CHARS) -> str:
    """把大纲文档抽成纯文本。解析失败直接抛错，避免静默丢掉教师上传的参照。"""
    path = Path(path)
    try:
        text = load_document(path)
    except UnsupportedDocument as e:
        raise MaterialError(str(e)) from e
    except FileNotFoundError as e:
        raise MaterialError(f"课程大纲文件不存在：{path.name}") from e
    text = text.strip()
    if not text:
        raise MaterialError(f"{path.name} 解析结果为空。扫描版 PDF 请先做 OCR，或改传 Word。")
    if len(text) > max_chars:
        text = text[:max_chars] + "\n……（大纲已截断）"
    return text


def _find_soffice() -> str | None:
    for cand in SOFFICE_CANDIDATES:
        p = Path(cand)
        if p.is_file():
            return str(p)
        found = shutil.which(cand)
        if found:
            return found
    return None


def _pick_indices(n: int, k: int) -> list[int]:
    if n <= 0:
        return []
    if n <= k:
        return list(range(n))
    if k == 1:
        return [n // 2]
    return [int(i * (n - 1) / (k - 1) + 0.5) for i in range(k)]


def _office_to_pdf(src: Path, dest_dir: Path) -> Path:
    soffice = _find_soffice()
    if not soffice:
        raise MaterialError(
            f"无法将 {src.suffix} 转成页面图像：本机未安装 LibreOffice。"
            "请另存为 PDF 后上传，或安装 LibreOffice（brew install --cask libreoffice）。"
        )
    dest_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            soffice,
            "--headless",
            "--norestore",
            "--convert-to",
            "pdf",
            "--outdir",
            str(dest_dir),
            str(src),
        ],
        capture_output=True,
        text=True,
        timeout=180,
    )
    pdf = dest_dir / f"{src.stem}.pdf"
    if result.returncode != 0 or not pdf.is_file():
        err = (result.stderr or result.stdout or "").strip()[-400:]
        raise MaterialError(f"{src.name} 转为 PDF 失败。{err}")
    return pdf


def _pptx_text(path: Path) -> str:
    from pptx import Presentation

    prs = Presentation(str(path))
    parts: list[str] = []
    for i, slide in enumerate(prs.slides, 1):
        texts: list[str] = []
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False):
                t = (shape.text_frame.text or "").strip()
                if t:
                    texts.append(t)
        if texts:
            parts.append(f"【第 {i} 页】\n" + "\n".join(texts))
    return "\n\n".join(parts).strip()


def _render_pdf_pages(
    pdf_path: Path, out_dir: Path, max_pages: int, prefix: str = "cw"
) -> tuple[list[dict], str]:
    import fitz

    doc = fitz.open(str(pdf_path))
    try:
        n = doc.page_count
        if n <= 0:
            raise MaterialError(f"{pdf_path.name} 没有可渲染的页面")
        indices = _pick_indices(n, max_pages)
        out_dir.mkdir(parents=True, exist_ok=True)
        pages: list[dict] = []
        text_parts: list[str] = []
        for order, page_i in enumerate(indices):
            page = doc[page_i]
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
            out_path = out_dir / f"{prefix}_{order:03d}.jpg"
            pix.save(str(out_path))
            pages.append(
                {
                    "index": order,
                    "page": page_i + 1,
                    "page_count": n,
                    "path": str(out_path),
                }
            )
            page_text = (page.get_text("text") or "").strip()
            if page_text:
                text_parts.append(f"【第 {page_i + 1} 页】\n{page_text}")
        full_text = "\n\n".join(text_parts).strip()
        return pages, full_text
    finally:
        doc.close()


def prepare_courseware(
    path: str | Path,
    out_dir: str | Path,
    max_pages: int | None = None,
) -> dict:
    """把课件变成「页面图像 + 抽取文本」。

    PDF 直接渲染。PPT/PPTX 优先用 LibreOffice 转 PDF 再渲染；转不成时
    PPTX 退回纯文本（版式无法观测），PPT 则报错请教师另存。
    """
    path = Path(path)
    out_dir = Path(out_dir)
    suffix = path.suffix.lower()
    if suffix not in COURSEWARE_EXT:
        raise MaterialError(
            f"不支持的课件格式 {suffix}，目前支持：{', '.join(sorted(COURSEWARE_EXT))}"
        )
    if not path.is_file():
        raise MaterialError(f"课件文件不存在：{path.name}")

    eval_conf = settings.section("evaluation")
    max_pages = max_pages or int(eval_conf.get("courseware_max_pages", 16))
    warning = ""
    visual = True
    pdf_path = path

    if suffix in {".pptx", ".ppt"}:
        try:
            pdf_path = _office_to_pdf(path, out_dir / "_convert")
        except MaterialError as e:
            if suffix == ".pptx":
                try:
                    text = _pptx_text(path)
                except Exception as inner:
                    raise MaterialError(
                        f"{path.name} 无法转成页面图像，文本抽取也失败：{inner}"
                    ) from inner
                if not text:
                    raise MaterialError(
                        f"{path.name} 无法转成页面图像，且抽不到幻灯片文字。"
                        "请另存为 PDF 后上传。"
                    ) from e
                if len(text) > MAX_COURSEWARE_TEXT_CHARS:
                    text = text[:MAX_COURSEWARE_TEXT_CHARS] + "\n……（课件文本已截断）"
                return {
                    "pages": [],
                    "text": text,
                    "visual": False,
                    "page_count": 0,
                    "source": path.name,
                    "warning": str(e),
                }
            raise

    try:
        pages, text = _render_pdf_pages(pdf_path, out_dir, max_pages)
    except MaterialError:
        raise
    except Exception as e:
        raise MaterialError(f"渲染课件页面失败：{e}") from e

    if not text and suffix == ".pptx":
        try:
            text = _pptx_text(path)
        except Exception:
            pass

    if len(text) > MAX_COURSEWARE_TEXT_CHARS:
        text = text[:MAX_COURSEWARE_TEXT_CHARS] + "\n……（课件文本已截断）"

    if not pages:
        visual = False
        warning = "课件没有可渲染的页面，仅保留抽取文本"

    return {
        "pages": pages,
        "text": text,
        "visual": visual,
        "page_count": pages[0]["page_count"] if pages else 0,
        "source": path.name,
        "warning": warning,
    }
