#!/usr/bin/env python3
"""Build a resumable MIT OpenCourseWare catalog under knowledge/corpora/teaching_cases/MIT.

The course list comes from MIT's public search API (platform=ocw). Each course
homepage is fetched and its real navigation is recorded. Full text is extracted
only for pages this run explicitly selects. Binary files are indexed, not saved.

Resume: a course with discovery_status=complete in crawl_status.jsonl is skipped.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "knowledge" / "corpora" / "teaching_cases" / "MIT"
COURSES = OUT / "courses"
CACHE = OUT / "_crawl"
API_URL = "https://open.mit.edu/api/v0/search/"
SITE = "https://ocw.mit.edu"
UA = "PKU-Wenjiao-KnowledgeBase/1.0 (educational catalog; MIT OCW course pages)"
CAPTURE_DATE = "2026-10-03"

BINARY_EXT = {
    ".pdf", ".zip", ".gz", ".tgz", ".tar", ".7z", ".rar",
    ".mp4", ".m4v", ".mov", ".avi", ".webm", ".mp3", ".wav", ".m4a",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    ".ppt", ".pptx", ".doc", ".docx", ".xls", ".xlsx",
    ".ipynb", ".py", ".r", ".m", ".csv", ".tsv", ".json", ".mat", ".h5", ".npz",
    ".sas", ".dta", ".sav", ".psd", ".ai",
}
FULL_TEXT_FILES = {
    "course_home": "course-description.md",
    "syllabus": "syllabus.md",
    "calendar": "calendar.md",
    "readings": "readings.md",
    "lecture_notes": "lecture-notes.md",
    "assignments": "assignments.md",
    "projects": "projects.md",
    "exams": "exams.md",
    "quizzes": "quizzes.md",
    "instructor_insights": "instructor-insights.md",
    "related_resources": "related-resources.md",
    "teaching_notes": "teaching-notes.md",
}
RESOURCE_FLAGS = (
    "syllabus", "calendar", "readings", "lecture_notes", "assignments",
    "projects", "exams", "videos", "instructor_insights", "related_resources",
)
TERM_RE = re.compile(
    r"(January IAP|Spring|Fall|Summer|IAP)\s+(\d{4})", re.IGNORECASE
)
LEVELS = ("undergraduate", "graduate", "non-credit", "high school")
CC_NAMES = {
    "by-nc-sa": "CC BY-NC-SA",
    "by-nc-nd": "CC BY-NC-ND",
    "by-nc": "CC BY-NC",
    "by-sa": "CC BY-SA",
    "by-nd": "CC BY-ND",
    "by": "CC BY",
}


class Node:
    def __init__(self, tag: str, attrs):
        self.tag = tag
        self.attrs = {k: v for k, v in attrs}
        self.children: list = []

    def classes(self) -> set[str]:
        return set((self.attrs.get("class") or "").split())

    def has_class(self, name: str) -> bool:
        return name in self.classes()


class TreeBuilder(HTMLParser):
    VOID = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("document", {})
        self.stack = [self.root]
        self.parents: dict[Node, Node | None] = {self.root: None}

    def handle_starttag(self, tag, attrs):
        node = Node(tag.lower(), attrs)
        parent = self.stack[-1]
        parent.children.append(node)
        self.parents[node] = parent
        if tag.lower() not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        tag = tag.lower()
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if data:
            self.stack[-1].children.append(data)


def repair_html(html: str) -> str:
    """Drop stray paragraph tags that OCW leaves inside tables.

    Those tags make a strict parser close the table after the header row.
    """
    html = re.sub(r"<p>\s*(<table\b)", r"\1", html, flags=re.I)
    def _strip_paragraphs(match: re.Match) -> str:
        block = re.sub(r"<p\b[^>]*>", "", match.group(0), flags=re.I)
        return re.sub(r"</p>", "<br>", block, flags=re.I)
    return re.sub(r"<table\b.*?</table>", _strip_paragraphs, html, flags=re.I | re.S)


def parse_html(html: str) -> TreeBuilder:
    builder = TreeBuilder()
    builder.feed(repair_html(html))
    builder.close()
    return builder


def walk(node: Node):
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from walk(child)


def find_all(node: Node, tag: str | None = None, class_name: str | None = None, elem_id: str | None = None):
    found = []
    for item in walk(node):
        if tag and item.tag != tag:
            continue
        if class_name and not item.has_class(class_name):
            continue
        if elem_id and item.attrs.get("id") != elem_id:
            continue
        found.append(item)
    return found


def find_id(node: Node, elem_id: str) -> Node | None:
    for item in walk(node):
        if item.attrs.get("id") == elem_id:
            return item
    return None


def clean_text(node: Node | str) -> str:
    if isinstance(node, str):
        return re.sub(r"\s+", " ", node).strip()
    parts = []
    for child in node.children:
        if isinstance(child, str):
            parts.append(child)
        elif isinstance(child, Node) and child.tag not in {"script", "style", "noscript"}:
            parts.append(clean_text(child))
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def ancestor_has(node: Node, parents: dict, class_name: str) -> bool:
    cur = node
    while cur is not None:
        if cur.has_class(class_name):
            return True
        cur = parents.get(cur)
    return False


def section_container(root: Node, heading: str) -> Node | None:
    for h in find_all(root, "h3"):
        if clean_text(h).lower() == heading.lower():
            parent = h
            # The heading's parent block also holds the following content div.
            return parent.attrs and None or _parent_of(root, h)
    return None


def _parent_of(root: Node, target: Node) -> Node | None:
    for item in walk(root):
        for child in item.children:
            if child is target:
                return item
    return None


def following_content(root: Node, heading: str) -> Node | None:
    parent = _parent_of(root, _first_heading(root, heading)) if _first_heading(root, heading) else None
    heading_node = _first_heading(root, heading)
    if parent is None or heading_node is None:
        return None
    seen = False
    for child in parent.children:
        if child is heading_node:
            seen = True
            continue
        if seen and isinstance(child, Node):
            return child
    return None


def _first_heading(root: Node, heading: str) -> Node | None:
    for h in find_all(root, "h3"):
        if clean_text(h).lower() == heading.lower():
            return h
    return None


def absolute_url(base: str, href: str | None) -> str | None:
    if not href:
        return None
    href = href.strip()
    if not href or href.startswith(("#", "javascript:", "mailto:")):
        return None
    url = urljoin(base, href)
    parts = urlparse(url)
    if parts.scheme not in {"http", "https"}:
        return None
    # Drop fragments; keep query because a few OCW links use it.
    return urlunparse(parts._replace(fragment=""))


def extension_of(url: str) -> str:
    path = urlparse(url).path.lower()
    return Path(path).suffix


def is_binary_url(url: str) -> bool:
    return extension_of(url) in BINARY_EXT


def slugify_code(code: str) -> str:
    text = code.strip().lower().replace(".", "-").replace("_", "-")
    text = re.sub(r"[^a-z0-9-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "course"


def term_slug(term: str | None) -> str:
    if not term:
        return "undated"
    return re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-") or "undated"


class Limiter:
    def __init__(self, per_second: float):
        self.interval = 1.0 / per_second if per_second > 0 else 0
        self.lock = threading.Lock()
        self.next_at = 0.0

    def wait(self):
        if self.interval <= 0:
            return
        with self.lock:
            now = time.monotonic()
            slot = max(now, self.next_at)
            self.next_at = slot + self.interval
            delay = slot - now
        if delay > 0:
            time.sleep(delay)


LIMITER = Limiter(4)


def fetch(url: str, accept: str = "text/html,application/xhtml+xml") -> tuple[int, str, str, bytes]:
    last_error = None
    for attempt in range(4):
        LIMITER.wait()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.status, resp.geturl(), resp.headers.get("Content-Type", ""), resp.read()
        except urllib.error.HTTPError as exc:
            body = exc.read() if exc.fp else b""
            if exc.code in {429, 500, 502, 503, 504} and attempt < 3:
                time.sleep(2 ** attempt)
                last_error = exc
                continue
            return exc.code, url, exc.headers.get("Content-Type", "") if exc.headers else "", body
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"fetch failed for {url}: {last_error}")


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    last_error = None
    for attempt in range(4):
        LIMITER.wait()
        req = urllib.request.Request(
            url,
            data=data,
            headers={"User-Agent": UA, "Accept": "application/json", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001 - retry network/API failures
            last_error = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"API request failed: {last_error}")


def load_api_courses(refresh: bool = False) -> list[dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE / "api_courses.jsonl"
    if cache_path.exists() and not refresh:
        rows = []
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        if rows:
            return rows
    rows = []
    start = 0
    size = 100
    total = None
    while total is None or start < total:
        payload = {
            "from": start,
            "size": size,
            "track_total_hits": True,
            "_source": {"exclude": ["content", "transcript"]},
            "query": {"bool": {"filter": [
                {"term": {"object_type.keyword": "course"}},
                {"term": {"platform": "ocw"}},
            ]}},
            "sort": [{"id": "asc"}],
        }
        data = post_json(API_URL, payload)
        raw_total = data["hits"]["total"]
        total = raw_total["value"] if isinstance(raw_total, dict) else raw_total
        hits = data["hits"]["hits"]
        if not hits:
            break
        for hit in hits:
            rows.append(hit["_source"])
        start += len(hits)
        print(f"api {min(start, total)}/{total}", flush=True)
    seen = set()
    unique = []
    for row in rows:
        runs = row.get("runs") or [{}]
        slug = (runs[0].get("slug") or "").strip("/")
        if not slug or slug in seen:
            continue
        seen.add(slug)
        unique.append(row)
    with cache_path.open("w", encoding="utf-8") as fh:
        for row in unique:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"api unique courses {len(unique)}", flush=True)
    return unique


def course_slug_of(api_row: dict) -> str:
    runs = api_row.get("runs") or [{}]
    slug = (runs[0].get("slug") or "").strip("/")
    if slug.startswith("courses/"):
        slug = slug[len("courses/"):]
    return slug.strip("/")


def course_url_of(slug: str) -> str:
    return f"{SITE}/courses/{slug}/"


def license_from_html(html: str) -> tuple[str | None, str | None]:
    match = re.search(r'"license"\s*:\s*"(https://creativecommons\.org/[^"]+)"', html)
    url = match.group(1) if match else None
    if not url:
        match = re.search(r'href="(https://creativecommons\.org/licenses/[^"]+)"', html)
        url = match.group(1) if match else None
    if not url:
        return None, None
    path = urlparse(url).path.strip("/")
    parts = path.split("/")
    # licenses/by-nc-sa/4.0
    name = None
    version = None
    if len(parts) >= 2 and parts[0] == "licenses":
        key = parts[1]
        version = parts[2] if len(parts) > 2 else None
        base = CC_NAMES.get(key)
        if base and version:
            name = f"{base} {version}"
        elif base:
            name = base
    return name, url


def parse_banner(text: str) -> tuple[list[str], list[str]]:
    codes: list[str] = []
    levels: list[str] = []
    for part in [p.strip() for p in text.split("|") if p.strip()]:
        if TERM_RE.search(part):
            continue
        bits = [b.strip() for b in re.split(r"\s*/\s*|\s*,\s*|,", part) if b.strip()]
        if bits and all(b.lower() in LEVELS for b in bits):
            levels.extend(_canonical_level(b) for b in bits)
            continue
        for bit in bits:
            if bit.lower() in LEVELS:
                levels.append(_canonical_level(bit))
            elif re.search(r"\d", bit):
                codes.append(bit)
    return _dedupe(codes), _dedupe(levels)


def _canonical_level(value: str) -> str:
    key = value.strip().lower()
    mapping = {
        "undergraduate": "Undergraduate",
        "graduate": "Graduate",
        "non-credit": "Non-Credit",
        "high school": "High School",
    }
    return mapping.get(key, value.strip())


def explode_codes(codes: list[str]) -> list[str]:
    parts: list[str] = []
    for code in codes:
        parts.extend(piece.strip() for piece in re.split(r"\s*,\s*|/", code or "") if piece.strip())
    return _dedupe(parts)


def _dedupe(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def parse_term(text: str) -> tuple[str | None, int | None]:
    match = TERM_RE.search(text or "")
    if not match:
        return None, None
    raw = match.group(1).lower()
    names = {
        "spring": "Spring",
        "fall": "Fall",
        "summer": "Summer",
        "january iap": "January IAP",
        "iap": "IAP",
    }
    return names.get(raw, match.group(1)), int(match.group(2))


def parse_topic_tree(root: Node) -> list[dict]:
    heading = _first_heading(root, "Topics")
    if heading is None:
        return []
    parent = _parent_of(root, heading)
    if parent is None:
        return []
    tree = []
    # Topics markup is: h3, then a ul of top-level topics. Use the first ul
    # among the heading's siblings. Mobile and desktop each have their own h3,
    # and _first_heading keeps only one copy.
    ul = None
    seen = False
    for child in parent.children:
        if child is heading:
            seen = True
            continue
        if seen and isinstance(child, Node) and child.tag == "ul":
            ul = child
            break
    if ul is None:
        return []
    for li in [c for c in ul.children if isinstance(c, Node) and c.tag == "li"]:
        link = next((a for a in find_all(li, "a", "course-info-topic") if _parent_of(li, a) is not None), None)
        # The first topic link in this li is the top-level topic. Nested uls hold the rest.
        links = find_all(li, "a", "course-info-topic")
        if not links:
            continue
        top_name = clean_text(links[0])
        subtopics = []
        nested_uls = [c for c in li.children if isinstance(c, Node) and c.tag == "ul"]
        # Subtopics are nested further down; collect ul elements below the first link's container.
        sub_uls = []
        for item in walk(li):
            if item.tag == "ul" and item is not ul and "subtopic-container" in " ".join(item.classes()):
                sub_uls.append(item)
        if not sub_uls:
            for item in li.children:
                if isinstance(item, Node) and item.tag == "ul":
                    sub_uls.append(item)
        for sub_ul in sub_uls[:1]:
            for sub_li in [c for c in sub_ul.children if isinstance(c, Node) and c.tag == "li"]:
                sub_links = find_all(sub_li, "a", "course-info-topic")
                if not sub_links:
                    continue
                specialties = [clean_text(a) for a in sub_links[1:]]
                # Specialty links live in a nested ul and are also found by find_all,
                # so sub_links[0] is the subtopic and the rest include specialties.
                spec_ul_links = []
                for spec_ul in [c for c in walk(sub_li) if isinstance(c, Node) and c.tag == "ul"]:
                    spec_ul_links.extend(clean_text(a) for a in find_all(spec_ul, "a", "course-info-topic"))
                subtopics.append({
                    "name": clean_text(sub_links[0]),
                    "specialties": _dedupe(spec_ul_links or specialties),
                })
        tree.append({"name": top_name, "subtopics": subtopics})
    return tree


def subject_fields(tree: list[dict]) -> tuple[str | None, list[str]]:
    """Map OCW's own topic / subtopic / specialty labels.

    subject_primary is the first subtopic when MIT provided one, otherwise the
    first top-level topic. Remaining MIT labels go to subject_secondary.
    Nothing is inferred from the course title.
    """
    if not tree:
        return None, []
    primary = None
    secondary: list[str] = []
    for branch in tree:
        if branch["subtopics"]:
            if primary is None:
                primary = branch["subtopics"][0]["name"]
                secondary.extend(branch["subtopics"][0]["specialties"])
                for extra in branch["subtopics"][1:]:
                    secondary.append(extra["name"])
                    secondary.extend(extra["specialties"])
            else:
                secondary.append(branch["name"])
                for extra in branch["subtopics"]:
                    secondary.append(extra["name"])
                    secondary.extend(extra["specialties"])
        elif primary is None:
            primary = branch["name"]
        else:
            secondary.append(branch["name"])
    return primary, _dedupe([s for s in secondary if s and s != primary])


def feature_tags(root: Node) -> list[str]:
    tags = []
    for div in find_all(root, "div", "d-flex"):
        icon = next((c for c in div.children if isinstance(c, Node) and c.tag == "i"), None)
        label = next((c for c in div.children if isinstance(c, Node) and c.tag == "span"), None)
        if icon and label and icon.has_class("material-icons"):
            text = clean_text(label)
            if text:
                tags.append(text)
    return _dedupe(tags)


def desktop_nav(root: Node, parents: dict) -> Node | None:
    navs = find_all(root, "nav", "course-nav")
    for nav in navs:
        if ancestor_has(nav, parents, "large-and-above-only"):
            return nav
    return navs[-1] if navs else None


def classify_resource(title: str, url: str) -> str:
    path = urlparse(url).path.lower().strip("/")
    title_l = title.lower().strip()
    rules = [
        ("syllabus", ("/pages/syllabus",), ("syllabus",)),
        ("calendar", ("/pages/calendar", "/pages/schedule"), ("calendar", "schedule")),
        ("readings", ("/pages/readings", "/pages/reading", "/pages/textbooks"), ("readings", "reading list", "textbooks")),
        ("lecture_notes", ("/pages/lecture-notes", "/pages/lecture-slides", "/pages/notes"), ("lecture notes", "lecture slides", "class notes")),
        ("assignments", ("/pages/assignments", "/pages/homework", "/pages/problem-sets", "/pages/problemsets"), ("assignments", "problem sets", "homework")),
        ("projects", ("/pages/projects", "/pages/project", "/pages/final-project"), ("projects", "final project")),
        ("exams", ("/pages/exams", "/pages/exam", "/pages/midterm", "/pages/final-exam"), ("exams", "exam", "midterm", "final exam")),
        ("quizzes", ("/pages/quizzes", "/pages/quiz"), ("quizzes", "quiz")),
        ("instructor_insights", ("/pages/instructor-insights", "/pages/this-course-at-mit"), ("instructor insights", "this course at mit")),
        ("teaching_notes", ("/pages/teaching-notes",), ("teaching notes",)),
        ("related_resources", ("/pages/related-resources", "/pages/related-resources-and-tools"), ("related resources",)),
        ("videos", ("/video_galleries/", "/pages/video", "/pages/lecture-videos"), ("lecture videos", "videos", "video lectures")),
        ("course_package", ("/download",), ("download course",)),
    ]
    for name, paths, titles in rules:
        if any(piece in f"/{path}" or path.endswith(piece.strip("/")) for piece in paths):
            return name
        if title_l in titles or any(title_l == t for t in titles):
            return name
    if path.endswith("/download"):
        return "course_package"
    if is_binary_url(url):
        ext = extension_of(url)
        if ext == ".pdf":
            return "pdf"
        if ext in {".mp4", ".m4v", ".mov", ".webm"}:
            return "video"
        if ext in {".mp3", ".wav", ".m4a"}:
            return "audio"
        if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
            return "image"
        if ext in {".zip", ".gz", ".tgz", ".tar", ".7z", ".rar"}:
            return "archive"
        return "file"
    slug = re.sub(r"[^a-z0-9]+", "_", title_l).strip("_")
    return slug or "page"


def allocate_local_path(resource_type: str, url: str, local_path: str | None, used: dict[str, str]) -> str | None:
    """Keep one Markdown file per source page when a course has several of one type."""
    if not local_path:
        local_path = FULL_TEXT_FILES.get(resource_type)
    if not local_path:
        return None
    if used.get(local_path) in {None, url}:
        used[local_path] = url
        return local_path
    slug = Path(urlparse(url).path.rstrip("/")).name or "page"
    slug = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-") or "page"
    stem = Path(local_path).stem
    candidate = f"{stem}-{slug}.md"
    number = 2
    while used.get(candidate) not in {None, url}:
        candidate = f"{stem}-{slug}-{number}.md"
        number += 1
    used[candidate] = url
    return candidate


def extraction_plan(resource_type: str, url: str) -> tuple[str, str, str | None]:
    if resource_type == "course_package" or is_binary_url(url) or resource_type in {
        "pdf", "video", "audio", "image", "archive", "file", "videos",
    }:
        policy = "skip_binary" if resource_type in {"course_package", "video", "audio", "image", "archive", "file", "videos"} or is_binary_url(url) else "index_only"
        if resource_type == "videos":
            policy = "index_only"
        if is_binary_url(url) or resource_type in {"pdf", "video", "audio", "image", "archive", "file", "course_package"}:
            policy = "skip_binary"
        return policy, "skipped", None
    if resource_type in FULL_TEXT_FILES:
        # A syllabus that is itself a PDF is still full text, extracted from the PDF.
        if is_binary_url(url) and extension_of(url) == ".pdf" and resource_type in FULL_TEXT_FILES:
            return "full_text", "pending", FULL_TEXT_FILES[resource_type]
        return "full_text", "pending", FULL_TEXT_FILES[resource_type]
    return "index_only", "skipped", None


def nav_resources(root: Node, parents: dict, course_url: str) -> list[dict]:
    nav = desktop_nav(root, parents)
    items = []
    if nav is not None:
        for anchor in find_all(nav, "a"):
            url = absolute_url(course_url, anchor.attrs.get("href"))
            title = clean_text(anchor)
            if not url or not title:
                continue
            if url.rstrip("/") == course_url.rstrip("/"):
                continue
            items.append({"source_title": title, "source_url": url})
    for anchor in find_all(root, "a", "download-course-link-button"):
        url = absolute_url(course_url, anchor.attrs.get("href"))
        title = clean_text(anchor) or "Download Course"
        if url:
            items.append({"source_title": title, "source_url": url})
    deduped = []
    seen = set()
    for item in items:
        if item["source_url"] in seen:
            continue
        seen.add(item["source_url"])
        deduped.append(item)
    return deduped


def link_texts(node: Node | None, class_name: str) -> list[str]:
    if node is None:
        return []
    return _dedupe(clean_text(a) for a in find_all(node, "a", class_name) if clean_text(a))


def build_course_record(html: str, api_row: dict) -> tuple[dict, list[dict]]:
    tree = parse_html(html)
    slug = course_slug_of(api_row)
    course_url = course_url_of(slug)
    banner_node = find_id(tree.root, "course-banner")
    banner = ""
    title = None
    if banner_node is not None:
        number = next((n for n in walk(banner_node) if n.has_class("course-number-term-detail")), None)
        banner = clean_text(number) if number else ""
        h1 = next((n for n in walk(banner_node) if n.tag == "h1"), None)
        title = clean_text(h1) if h1 else None
    title = title or api_row.get("title")
    banner_codes, banner_levels = parse_banner(banner)
    taught_node = following_content(tree.root, "As Taught In")
    as_taught_in = clean_text(taught_node) if taught_node else ""
    term, year = parse_term(as_taught_in or banner)
    if term is None or year is None:
        slug_term, slug_year = parse_term(slug.replace("-", " "))
        # Slug uses january-iap-2010. parse_term on hyphenated text may fail.
        slug_match = re.search(r"(spring|fall|summer|january-iap|iap)-(\d{4})", slug)
        if slug_match and (term is None or year is None):
            term = term or {
                "spring": "Spring", "fall": "Fall", "summer": "Summer",
                "january-iap": "January IAP", "iap": "IAP",
            }[slug_match.group(1)]
            year = year or int(slug_match.group(2))
        elif slug_term and term is None:
            term, year = slug_term, slug_year
    level_node = following_content(tree.root, "Level")
    levels = link_texts(level_node, "") if level_node else []
    levels = [_canonical_level(x) for x in levels] or banner_levels
    runs = (api_row.get("runs") or [{}])[0]
    if not levels:
        levels = [_canonical_level(x) for x in (runs.get("level") or [])]
    dept_node = following_content(tree.root, "Departments")
    departments = link_texts(dept_node, "course-info-department")
    if not departments:
        departments = list(api_row.get("department_name") or [])
    inst_node = following_content(tree.root, "Instructors")
    instructors = link_texts(inst_node, "course-info-instructor")
    if not instructors:
        instructors = list(runs.get("instructors") or [])
    api_numbers = api_row.get("department_course_numbers") or []
    primary_api = [n.get("coursenum") for n in api_numbers if n.get("primary") and n.get("coursenum")]
    other_api = [n.get("coursenum") for n in api_numbers if n.get("coursenum") and not n.get("primary")]
    raw_codes = banner_codes or primary_api or ([api_row.get("coursenum")] if api_row.get("coursenum") else [])
    all_codes = explode_codes(list(raw_codes) + list(other_api) + list(banner_codes))
    primary = all_codes[0] if all_codes else None
    codes = [primary] if primary else []
    cross = [code for code in all_codes if code != primary]
    expanded = find_id(tree.root, "expanded-description")
    description = clean_text(expanded) if expanded else ""
    description = re.sub(r"\s*Show less\s*$", "", description).strip()
    if not description:
        description = (api_row.get("short_description") or "").strip()
        description = re.sub(r"\{\{%\s*resource_link.*?%\}\}", "", description).strip()
    tree_topics = parse_topic_tree(tree.root)
    subject_primary, subject_secondary = subject_fields(tree_topics)
    image = None
    image_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if image_match:
        image = absolute_url(course_url, image_match.group(1))
    elif api_row.get("image_src"):
        image = absolute_url(SITE, api_row.get("image_src"))
    license_name, license_url = license_from_html(html)
    code_for_id = slugify_code(primary or slug.split("-")[0])
    course_id = claim_course_id(
        f"mitocw-{code_for_id}-{term_slug(term)}-{year or 'undated'}",
        slug,
    )
    tags = feature_tags(tree.root)
    resources_found = nav_resources(tree.root, tree.parents, course_url)
    resource_rows = []
    type_seen = Counter()
    used_paths: dict[str, str] = {}
    flags = {key: False for key in RESOURCE_FLAGS}
    # Homepage description is a real section, even though it is not a nav item.
    if description:
        resources_found.insert(0, {
            "source_title": "Course Description",
            "source_url": course_url,
            "resource_type": "course_home",
        })
    for item in resources_found:
        rtype = item.get("resource_type") or classify_resource(item["source_title"], item["source_url"])
        policy, status, local_path = extraction_plan(rtype, item["source_url"])
        if rtype == "course_home":
            policy, status, local_path = "full_text", "pending", FULL_TEXT_FILES["course_home"]
        if is_binary_url(item["source_url"]) and extension_of(item["source_url"]) == ".pdf" and rtype in FULL_TEXT_FILES:
            policy, status, local_path = "full_text", "pending", FULL_TEXT_FILES[rtype]
        if policy == "full_text":
            local_path = allocate_local_path(rtype, item["source_url"], local_path, used_paths)
        type_seen[rtype] += 1
        suffix = "" if type_seen[rtype] == 1 else f"-{type_seen[rtype]}"
        if rtype in flags:
            flags[rtype] = True
        if rtype == "quizzes":
            flags["exams"] = True
        if rtype == "lecture_notes":
            flags["lecture_notes"] = True
        resource_rows.append({
            "resource_id": f"{course_id}-{rtype.replace('_', '-')}{suffix}",
            "course_id": course_id,
            "resource_type": rtype,
            "source_title": item["source_title"],
            "source_url": item["source_url"],
            "source_format": "pdf" if extension_of(item["source_url"]) == ".pdf" else "html",
            "availability": "available",
            "extraction_policy": policy,
            "extraction_status": status,
            "local_path": local_path,
            "capture_date": CAPTURE_DATE,
            "content_sha256": None,
            "error": None,
        })
    origin = {}
    if subject_primary:
        origin["subject_primary"] = "source"
    if subject_secondary:
        origin["subject_secondary"] = "source"
    if levels:
        origin["academic_levels"] = "source"
    if tags:
        origin["course_feature_tags"] = "source"
    record = {
        "schema_version": "1.0",
        "course_id": course_id,
        "institution": "Massachusetts Institute of Technology",
        "platform": "MIT OpenCourseWare",
        "course_codes": codes,
        "cross_listed_codes": cross,
        "course_title": title,
        "course_slug": slug,
        "term": term,
        "year": year,
        "as_taught_in": as_taught_in or None,
        "language": "en",
        "departments": departments,
        "academic_levels": _dedupe(levels),
        "instructors": instructors,
        "subject_primary": subject_primary,
        "subject_secondary": subject_secondary,
        "topic_tree": tree_topics,
        "topic_keywords": [],
        "pedagogy_tags": [],
        "assessment_types": [],
        "course_feature_tags": tags,
        "description": description or None,
        "course_url": course_url,
        "image_url": image,
        "license_name": license_name,
        "license_url": license_url,
        "resources": flags,
        "metadata_origin": origin,
        "capture_date": CAPTURE_DATE,
        "last_verified_date": CAPTURE_DATE,
        "extraction_status": "pending",
    }
    return record, resource_rows


def yaml_scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def _yaml_lines(value, level: int) -> list[str]:
    indent = "  " * level
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, dict):
                if not item:
                    lines.append(f"{indent}{key}: {{}}")
                else:
                    lines.append(f"{indent}{key}:")
                    lines.extend(_yaml_lines(item, level + 1))
            elif isinstance(item, list):
                if not item:
                    lines.append(f"{indent}{key}: []")
                else:
                    lines.append(f"{indent}{key}:")
                    lines.extend(_yaml_lines(item, level + 1))
            elif isinstance(item, str) and ("\n" in item or len(item) > 140):
                lines.append(f"{indent}{key}: |")
                for line in item.replace("\r\n", "\n").strip("\n").split("\n"):
                    lines.append(f"{indent}  {line}")
            else:
                lines.append(f"{indent}{key}: {yaml_scalar(item)}")
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, dict):
                item_lines = _yaml_lines(item, 0)
                lines.append(f"{indent}- {item_lines[0]}")
                for extra in item_lines[1:]:
                    lines.append(f"{indent}  {extra}")
            else:
                lines.append(f"{indent}- {yaml_scalar(item)}")
        return lines
    return [f"{indent}{yaml_scalar(value)}"]


def to_yaml(value, level: int = 0) -> str:
    return "\n".join(_yaml_lines(value, level))


USED_COURSE_IDS: set[str] = set()
COURSE_ID_LOCK = threading.Lock()


def claim_course_id(base: str, slug: str) -> str:
    existing = CACHE / "records" / f"{slug}.json"
    if existing.exists():
        return json.loads(existing.read_text(encoding="utf-8"))["course"]["course_id"]
    with COURSE_ID_LOCK:
        if base not in USED_COURSE_IDS:
            USED_COURSE_IDS.add(base)
            return base
        candidate = base
        number = 2
        while candidate in USED_COURSE_IDS:
            candidate = f"{base}-{number}"
            number += 1
        USED_COURSE_IDS.add(candidate)
        return candidate


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def write_course_files(record: dict, resources: list[dict]):
    slug = record["course_slug"]
    folder = COURSES / slug
    folder.mkdir(parents=True, exist_ok=True)
    write_text(folder / "course.yaml", to_yaml(record) + "\n")
    lines = [json.dumps(row, ensure_ascii=False) for row in resources]
    write_text(folder / "resources.jsonl", ("\n".join(lines) + "\n") if lines else "")
    write_text(CACHE / "records" / f"{slug}.json", json.dumps({"course": record, "resources": resources}, ensure_ascii=False))


def load_status() -> dict[str, dict]:
    path = OUT / "crawl_status.jsonl"
    found = {}
    if not path.exists():
        return found
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        found[row["course_slug"]] = row
    return found


def append_status(row: dict, lock: threading.Lock):
    OUT.mkdir(parents=True, exist_ok=True)
    with lock:
        with (OUT / "crawl_status.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def discover_one(api_row: dict) -> dict:
    slug = course_slug_of(api_row)
    url = course_url_of(slug)
    status, final_url, ctype, body = fetch(url)
    if status != 200:
        return {
            "course_slug": slug,
            "course_url": url,
            "discovery_status": "failed",
            "extraction_status": "failed",
            "http_status": status,
            "resource_count": 0,
            "error": f"HTTP {status}",
            "capture_date": CAPTURE_DATE,
        }
    html = body.decode("utf-8", errors="replace")
    record, resources = build_course_record(html, api_row)
    if final_url and urlparse(final_url).path.rstrip("/") != urlparse(url).path.rstrip("/"):
        record["course_url"] = final_url if final_url.startswith(SITE) else url
    write_course_files(record, resources)
    return {
        "course_id": record["course_id"],
        "course_slug": slug,
        "course_url": record["course_url"],
        "discovery_status": "complete",
        "extraction_status": "pending",
        "http_status": status,
        "resource_count": len(resources),
        "error": None,
        "capture_date": CAPTURE_DATE,
    }


def reserve_existing_ids():
    with COURSE_ID_LOCK:
        for saved in iter_saved_records():
            USED_COURSE_IDS.add(saved["course"]["course_id"])


def repair_saved_codes():
    """Split course numbers that were stored as one comma-joined string."""
    changed = 0
    for saved in list(iter_saved_records()):
        course = saved["course"]
        original = (course.get("course_codes") or []) + (course.get("cross_listed_codes") or [])
        if not any("," in code for code in original):
            continue
        all_codes = explode_codes((course.get("course_codes") or []) + (course.get("cross_listed_codes") or []))
        primary = all_codes[0] if all_codes else None
        course["course_codes"] = [primary] if primary else []
        course["cross_listed_codes"] = [code for code in all_codes if code != primary]
        write_course_files(course, saved["resources"])
        changed += 1
    if changed:
        print(f"split comma-joined course codes in {changed} records", flush=True)


def repair_local_paths():
    changed_courses = 0
    for saved in list(iter_saved_records()):
        used: dict[str, str] = {}
        changed = False
        for row in saved["resources"]:
            if row.get("extraction_policy") != "full_text":
                continue
            new_path = allocate_local_path(
                row["resource_type"], row["source_url"], row.get("local_path"), used,
            )
            if new_path != row.get("local_path"):
                row["local_path"] = new_path
                changed = True
        if changed:
            write_course_files(saved["course"], saved["resources"])
            changed_courses += 1
    print(f"gave distinct files to {changed_courses} courses with repeated sections", flush=True)


def discover(args):
    reserve_existing_ids()
    repair_saved_codes()
    rows = load_api_courses(refresh=args.refresh_api)
    if args.slug:
        rows = [row for row in rows if course_slug_of(row) == args.slug]
        if not rows:
            raise SystemExit(f"slug not in OCW course list: {args.slug}")
    if args.limit:
        rows = rows[: args.limit]
    pending = []
    for row in rows:
        slug = course_slug_of(row)
        folder = COURSES / slug
        # Existing course.yaml is the resume point. Refetching would replace
        # an already extracted resources.jsonl with a pending catalog row.
        if (folder / "course.yaml").exists() and (folder / "resources.jsonl").exists():
            continue
        pending.append(row)
    print(f"discover {len(pending)} courses ({len(rows) - len(pending)} already complete)", flush=True)
    lock = threading.Lock()
    failures = 0
    if args.workers <= 1:
        for index, row in enumerate(pending, 1):
            result = _safe_discover(row)
            append_status(result, lock)
            failures += _note_progress(index, len(pending), result)
    else:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(_safe_discover, row): row for row in pending}
            for index, future in enumerate(as_completed(futures), 1):
                result = future.result()
                append_status(result, lock)
                failures += _note_progress(index, len(pending), result)
    rebuild_indexes()
    print(f"discover finished, new failures in this run: {failures}", flush=True)


def _safe_discover(row: dict) -> dict:
    slug = course_slug_of(row)
    try:
        return discover_one(row)
    except Exception as exc:  # noqa: BLE001 - one course must not stop the catalog
        return {
            "course_slug": slug,
            "course_url": course_url_of(slug),
            "discovery_status": "failed",
            "extraction_status": "failed",
            "http_status": None,
            "resource_count": 0,
            "error": str(exc),
            "capture_date": CAPTURE_DATE,
        }


def _note_progress(index: int, total: int, result: dict) -> int:
    if index % 25 == 0 or result.get("discovery_status") != "complete":
        print(f"{index}/{total} {result.get('course_slug')} {result.get('discovery_status')} {result.get('error') or ''}", flush=True)
    return 0 if result.get("discovery_status") == "complete" else 1


def latest_status_rows() -> list[dict]:
    found = load_status()
    return list(found.values())


def iter_saved_records():
    folder = CACHE / "records"
    if not folder.exists():
        return
    for path in sorted(folder.glob("*.json")):
        yield json.loads(path.read_text(encoding="utf-8"))


def rebuild_indexes():
    OUT.mkdir(parents=True, exist_ok=True)
    catalog_lines = []
    dept = Counter()
    levels = Counter()
    terms = Counter()
    subjects = Counter()
    years = Counter()
    count = 0
    for saved in iter_saved_records():
        course = saved["course"]
        count += 1
        catalog_lines.append(json.dumps(catalog_row(course), ensure_ascii=False))
        for name in course.get("departments") or []:
            dept[name] += 1
        for name in course.get("academic_levels") or []:
            levels[name] += 1
        if course.get("term"):
            terms[course["term"]] += 1
        if course.get("subject_primary"):
            subjects[course["subject_primary"]] += 1
        if course.get("year"):
            years[str(course["year"])] += 1
    write_text(OUT / "catalog.jsonl", ("\n".join(catalog_lines) + "\n") if catalog_lines else "")
    taxonomy = {
        "schema_version": "1.0",
        "source": "MIT OpenCourseWare course homepages",
        "capture_date": CAPTURE_DATE,
        "course_count": count,
        "note": "Counts are labels printed on OCW course pages. subject_primary uses MIT's first subtopic when the page provides one.",
        "departments": [{"name": name, "course_count": n} for name, n in dept.most_common()],
        "academic_levels": [{"name": name, "course_count": n} for name, n in levels.most_common()],
        "terms": [{"name": name, "course_count": n} for name, n in terms.most_common()],
        "subject_primary": [{"name": name, "course_count": n} for name, n in subjects.most_common()],
        "years": [{"year": int(name), "course_count": n} for name, n in sorted(years.items())],
    }
    write_text(OUT / "taxonomy.yaml", to_yaml(taxonomy) + "\n")
    print(f"indexes rebuilt for {count} courses", flush=True)


def catalog_row(course: dict) -> dict:
    return {
        "course_id": course["course_id"],
        "course_codes": course["course_codes"],
        "cross_listed_codes": course["cross_listed_codes"],
        "course_title": course["course_title"],
        "course_slug": course["course_slug"],
        "term": course["term"],
        "year": course["year"],
        "departments": course["departments"],
        "academic_levels": course["academic_levels"],
        "instructors": course["instructors"],
        "subject_primary": course["subject_primary"],
        "subject_secondary": course["subject_secondary"],
        "course_url": course["course_url"],
        "image_url": course["image_url"],
        "license_name": course["license_name"],
        "license_url": course["license_url"],
        "resources": course["resources"],
        "extraction_status": course["extraction_status"],
        "capture_date": course["capture_date"],
    }


# --- HTML to Markdown -------------------------------------------------------

SKIP_TAGS = {"script", "style", "noscript", "svg", "button", "form", "iframe", "nav"}


def render_markdown(node: Node, base_url: str) -> str:
    text = _render_block(node, base_url).replace("\xa0", " ")
    lines = []
    for line in text.splitlines():
        if re.match(r"\s*(?:[-*]|\d+\.)\s", line) or line.lstrip().startswith(("|", "<", ">")):
            lines.append(line.rstrip())
        else:
            lines.append(line.strip())
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def _render_block(node: Node | str, base_url: str) -> str:
    if isinstance(node, str):
        return re.sub(r"\s+", " ", node)
    if node.tag in SKIP_TAGS or node.attrs.get("id") == "collapsed-description":
        return ""
    if node.tag == "br":
        return "\n"
    if node.tag == "img":
        return _image(node, base_url)
    if node.tag == "a":
        return _link(node, base_url)
    if node.has_class("resource-list-page"):
        body = re.sub(r"\s+", " ", _inline(node, base_url)).strip()
        return f"\n\n- {body}\n" if body else ""
    if node.tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = int(node.tag[1])
        title = _inline(node, base_url).strip()
        if not title:
            return ""
        return f"\n\n{'#' * level} {title}\n\n"
    if node.tag == "p":
        body = _inline(node, base_url).strip()
        return f"\n\n{body}\n\n" if body else ""
    if node.tag in {"ul", "ol"}:
        return "\n\n" + _list(node, base_url, ordered=node.tag == "ol", depth=0) + "\n\n"
    if node.tag == "blockquote":
        holder = Node("div", {})
        holder.children = list(node.children)
        inner = render_markdown(holder, base_url).strip()
        quoted = "\n".join("> " + line if line else ">" for line in inner.splitlines())
        return f"\n\n{quoted}\n\n"
    if node.tag == "pre":
        code = clean_text(node)
        return f"\n\n```\n{code}\n```\n\n"
    if node.tag == "table":
        return "\n\n" + _table(node, base_url) + "\n\n"
    if node.tag == "hr":
        return "\n\n---\n\n"
    if node.tag == "li":
        return _inline(node, base_url)
    parts = []
    for child in node.children:
        if isinstance(child, Node):
            parts.append(_render_block(child, base_url))
        else:
            parts.append(_text_piece(child))
    return "".join(parts)


def _text_piece(data: str) -> str:
    if not data:
        return ""
    if not data.strip():
        return " "
    left = " " if data[:1].isspace() else ""
    right = " " if data[-1:].isspace() else ""
    return left + re.sub(r"\s+", " ", data.strip()) + right


def _inline(node: Node, base_url: str) -> str:
    parts = []
    for child in node.children:
        if isinstance(child, str):
            parts.append(_text_piece(child))
            continue
        if child.tag in SKIP_TAGS or child.attrs.get("id") == "collapsed-description":
            continue
        if child.tag == "br":
            parts.append("\n")
        elif child.tag == "img":
            parts.append(_image(child, base_url))
        elif child.tag == "a":
            parts.append(_link(child, base_url))
        elif child.tag in {"strong", "b"}:
            inner = _inline(child, base_url).strip()
            parts.append(f"**{inner}**" if inner else "")
        elif child.tag in {"em", "i"}:
            if child.has_class("material-icons"):
                continue
            inner = _inline(child, base_url).strip()
            parts.append(f"*{inner}*" if inner else "")
        elif child.tag == "code":
            inner = clean_text(child)
            parts.append(f"`{inner}`" if inner else "")
        elif child.tag == "sub":
            inner = _inline(child, base_url).strip()
            parts.append(f"<sub>{inner}</sub>" if inner else "")
        elif child.tag == "sup":
            inner = _inline(child, base_url).strip()
            parts.append(f"<sup>{inner}</sup>" if inner else "")
        elif child.tag in {"ul", "ol", "table", "p", "div", "section", "blockquote", "pre"} or child.tag.startswith("h"):
            parts.append(_render_block(child, base_url))
        else:
            parts.append(_inline(child, base_url))
    return "".join(parts)


def _link(node: Node, base_url: str) -> str:
    href = absolute_url(base_url, node.attrs.get("href"))
    text = _inline(node, base_url).strip() or (href or "")
    if not href:
        return text
    return f"[{text}]({href})"


def _image(node: Node, base_url: str) -> str:
    src = absolute_url(base_url, node.attrs.get("src"))
    if not src or "/static_shared/" in src:
        return ""
    alt = (node.attrs.get("alt") or "").strip()
    if not alt and not node.attrs.get("title"):
        # Decorative or unlabeled images are not given invented descriptions.
        return f"![image]({src})"
    return f"![{alt}]({src})"


def _list(node: Node, base_url: str, ordered: bool, depth: int) -> str:
    lines = []
    index = 1
    for child in node.children:
        if not isinstance(child, Node) or child.tag != "li":
            continue
        content, nested = _li_parts(child, base_url, depth)
        marker = f"{index}." if ordered else "-"
        indent = "  " * depth
        lines.append(f"{indent}{marker} {content}".rstrip())
        if nested:
            lines.append(nested)
        index += 1
    return "\n".join(lines)


def _li_parts(node: Node, base_url: str, depth: int) -> tuple[str, str]:
    inline_nodes = []
    nested = []
    for child in node.children:
        if isinstance(child, Node) and child.tag in {"ul", "ol"}:
            nested.append(_list(child, base_url, ordered=child.tag == "ol", depth=depth + 1))
        else:
            inline_nodes.append(child)
    holder = Node("span", {})
    holder.children = inline_nodes
    text = re.sub(r"\s+", " ", _inline(holder, base_url)).strip()
    return text, "\n".join(nested)


def _cell_chunks(node: Node | str, base_url: str) -> list[str]:
    if isinstance(node, str):
        text = _text_piece(node).strip()
        return [text] if text else []
    if node.tag in {"br", "script", "style", "button"}:
        return []
    if node.tag == "a":
        text = _link(node, base_url).strip()
        return [text] if text else []
    if node.tag == "img":
        text = _image(node, base_url).strip()
        return [text] if text else []
    if node.tag in {"p", "li", "blockquote"} or node.tag.startswith("h"):
        parts = []
        for child in node.children:
            parts.extend(_cell_chunks(child, base_url))
        text = re.sub(r"\s+", " ", " ".join(parts)).strip()
        return [text] if text else []
    chunks = []
    for child in node.children:
        chunks.extend(_cell_chunks(child, base_url))
    return chunks


def _cell_text(cell: Node, base_url: str) -> str:
    return " <br> ".join(chunk.replace("|", "\\|") for chunk in _cell_chunks(cell, base_url))


def _table(node: Node, base_url: str) -> str:
    rows = []
    has_header = False
    complex_table = False
    for tr in find_all(node, "tr"):
        cells = []
        for cell in tr.children:
            if not isinstance(cell, Node) or cell.tag not in {"td", "th"}:
                continue
            if cell.attrs.get("colspan") or cell.attrs.get("rowspan"):
                complex_table = True
            if cell.tag == "th":
                has_header = True
            cells.append(_cell_text(cell, base_url))
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    if complex_table:
        return _html_table(node, base_url)
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    header = rows[0] if has_header else [""] * width
    body = rows[1:] if has_header else rows
    line = "| " + " | ".join(header) + " |"
    sep = "| " + " | ".join("---" for _ in header) + " |"
    lines = [line, sep]
    for row in body:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _html_table(node: Node, base_url: str) -> str:
    # Colspan/rowspan cannot be represented in a pipe table without changing the grid.
    parts = ["<table>"]
    for tr in find_all(node, "tr"):
        cells = []
        for cell in tr.children:
            if isinstance(cell, Node) and cell.tag in {"td", "th"}:
                attrs = ""
                for key in ("colspan", "rowspan"):
                    if cell.attrs.get(key):
                        attrs += f' {key}="{cell.attrs[key]}"'
                inner = _cell_text(cell, base_url)
                cells.append(f"<{cell.tag}{attrs}>{inner}</{cell.tag}>")
        if cells:
            parts.append("<tr>" + "".join(cells) + "</tr>")
    parts.append("</table>")
    return "".join(parts)


def page_article(html: str) -> Node | None:
    tree = parse_html(html)
    main = find_id(tree.root, "course-content-section")
    items = find_all(tree.root, "div", "resource-list-page")
    if items and (main is None or len(clean_text(main)) < 40):
        # Newer OCW list pages leave the article empty and render files after it.
        holder = Node("div", {})
        descriptions = find_all(tree.root, "div", "collection-description")
        if descriptions and clean_text(descriptions[0]):
            holder.children.append(descriptions[0])
        seen = set()
        for item in items:
            hrefs = [a.attrs.get("href") for a in find_all(item, "a") if a.attrs.get("href")]
            key = hrefs[0] if hrefs else str(id(item))
            if key in seen:
                continue
            seen.add(key)
            holder.children.append(item)
        return holder
    if main is not None:
        return main
    articles = find_all(tree.root, "article", "content")
    return articles[0] if articles else None


def headings_of(markdown: str) -> list[str]:
    heads = []
    for line in markdown.splitlines():
        match = re.match(r"#{1,6}\s+(.+)", line.strip())
        if match:
            heads.append(re.sub(r"\[(.*?)\]\(.*?\)", r"\1", match.group(1)).strip())
    return heads


def retrieval_header(course: dict, page_title: str, markdown: str, source_url: str, source_format: str) -> str:
    codes = ", ".join(course.get("course_codes") or []) or course["course_slug"]
    term = course.get("term") or "学期未在页面标明"
    year = course.get("year") or ""
    levels = "、".join(course.get("academic_levels") or []) or "层次未在页面标明"
    heads = headings_of(markdown)
    head_text = f"页内标题：{'；'.join(heads[:12])}。" if heads else ""
    summary = (
        f"检索摘要：{codes} {course.get('course_title')}（{term} {year}，{levels}）的「{page_title}」。"
        f"{head_text}分隔线后是该页英文原文，未翻译、未改写。"
    )
    license_url = course.get("license_url") or ""
    header = [
        f"> {summary}",
        "",
        f"- Source: {source_url}",
        f"- source_format: {source_format}",
        f"- capture_date: {CAPTURE_DATE}",
    ]
    if license_url:
        header.append(f"- license: {license_url}")
    header.extend(["", "---", ""])
    return "\n".join(header)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def pdf_to_text(data: bytes) -> tuple[str, str | None]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "source.pdf"
        path.write_bytes(data)
        try:
            proc = subprocess.run(
                ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
                check=False,
                capture_output=True,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return "", str(exc)
        if proc.returncode != 0:
            return "", proc.stderr.decode("utf-8", errors="replace")[:500]
        return proc.stdout.decode("utf-8", errors="replace"), None


def meaningful_text(text: str) -> bool:
    letters = re.findall(r"[A-Za-z]", text)
    return len(letters) >= 40


def course_prefix(course_url: str) -> str:
    return course_url.rstrip("/") + "/"


def harvested_type(title: str, url: str, parent_type: str) -> str:
    label = title.lower()
    if parent_type == "videos" or any(host in url for host in ("youtube.com", "youtu.be", "vimeo.com")):
        return "video"
    if "(zip)" in label or extension_of(url) in {".zip", ".gz", ".tgz", ".tar", ".7z", ".rar"}:
        kind = "archive"
    elif "(pdf)" in label or extension_of(url) == ".pdf":
        kind = "pdf"
    elif extension_of(url) in {".mp4", ".m4v", ".mov", ".webm"}:
        return "video"
    elif extension_of(url) in {".mp3", ".wav", ".m4a"}:
        return "audio"
    else:
        kind = "file"
    stem = {
        "lecture_notes": "lecture_note",
        "assignments": "assignment",
        "exams": "exam",
        "quizzes": "exam",
        "projects": "project",
        "readings": "reading",
    }.get(parent_type, "file")
    if stem == "file":
        return kind
    if "solution" in label:
        return f"{stem}_solution"
    return f"{stem}_{kind}"


def harvest_links(article: Node, page_url: str, course_url: str, parent_type: str) -> list[dict]:
    prefix = course_prefix(course_url)
    found = []
    seen = set()
    for anchor in find_all(article, "a"):
        url = absolute_url(page_url, anchor.attrs.get("href"))
        if not url or url in seen:
            continue
        title = clean_text(anchor) or Path(urlparse(url).path).name
        same_course = url.startswith(prefix)
        path = urlparse(url).path
        resource_page = same_course and "/resources/" in path
        binary = is_binary_url(url)
        video = any(host in url for host in ("youtube.com", "youtu.be", "vimeo.com"))
        if not ((same_course and binary) or resource_page or video):
            continue
        seen.add(url)
        found.append({
            "source_title": title,
            "source_url": url,
            "resource_type": harvested_type(title, url, parent_type),
        })
    return found


def extract_resource(course: dict, resource: dict) -> tuple[str | None, list[dict], dict]:
    url = resource["source_url"]
    status, final_url, ctype, body = fetch(url)
    if status != 200:
        resource = dict(resource)
        resource["availability"] = "missing" if status == 404 else "unknown"
        resource["extraction_status"] = "failed"
        resource["error"] = f"HTTP {status}"
        return None, [], resource
    is_pdf = "pdf" in ctype.lower() or extension_of(final_url or url) == ".pdf" or body[:5] == b"%PDF-"
    page_title = resource["source_title"]
    harvested = []
    if is_pdf:
        text, error = pdf_to_text(body)
        if error or not meaningful_text(text):
            resource = dict(resource)
            resource["source_format"] = "pdf"
            resource["extraction_status"] = "failed" if not text.strip() else "partial"
            resource["error"] = error or "PDF text was too short to treat as a reliable extraction"
            resource["local_path"] = None
            return None, [], resource
        verbatim = text.replace("\r\n", "\n").strip() + "\n"
        source_format = "pdf"
        source_url = final_url or url
    else:
        html = body.decode("utf-8", errors="replace")
        if resource["resource_type"] == "course_home":
            verbatim = homepage_markdown(html, course["course_url"])
            harvested = []
        elif resource["resource_type"] == "videos":
            article = page_article(html)
            harvested = harvest_links(article, final_url or url, course["course_url"], "videos") if article else []
            resource = dict(resource)
            resource["extraction_policy"] = "index_only"
            resource["extraction_status"] = "complete"
            resource["local_path"] = None
            resource["source_url"] = final_url or url
            return None, harvested, resource
        else:
            article = page_article(html)
            if article is None:
                resource = dict(resource)
                resource["extraction_status"] = "failed"
                resource["error"] = "content container not found"
                return None, [], resource
            title_node = find_id(parse_html(html).root, "course-title")
            if title_node is not None and clean_text(title_node):
                page_title = clean_text(title_node)
                verbatim = f"## {page_title}\n\n{render_markdown(article, final_url or url)}"
            else:
                verbatim = render_markdown(article, final_url or url)
            harvested = harvest_links(article, final_url or url, course["course_url"], resource["resource_type"])
        source_format = "html"
        source_url = final_url or url
    if not meaningful_text(verbatim):
        resource = dict(resource)
        resource["source_format"] = source_format
        resource["extraction_status"] = "partial"
        resource["error"] = "extracted text was too short"
        resource["local_path"] = None
        return None, harvested, resource
    document = retrieval_header(course, page_title, verbatim, source_url, source_format) + verbatim
    resource = dict(resource)
    resource["source_title"] = page_title
    resource["source_url"] = source_url
    resource["source_format"] = source_format
    resource["extraction_status"] = "complete"
    resource["content_sha256"] = sha256_text(verbatim)
    resource["error"] = None
    return document, harvested, resource


def homepage_markdown(html: str, course_url: str) -> str:
    tree = parse_html(html)
    description = find_id(tree.root, "expanded-description")
    parts = ["## Course Description\n\n"]
    if description is not None:
        parts.append(render_markdown(description, course_url))
    blocks = find_all(tree.root, "div", "course-info")
    if blocks:
        parts.append("\n\n")
        parts.append(render_markdown(blocks[0], course_url))
    return "".join(parts)


def load_saved(slug: str) -> dict:
    path = CACHE / "records" / f"{slug}.json"
    if not path.exists():
        raise SystemExit(f"missing discovery record for {slug}")
    return json.loads(path.read_text(encoding="utf-8"))


def extract_slug(slug: str):
    saved = load_saved(slug)
    course = saved["course"]
    resources = saved["resources"]
    folder = COURSES / slug
    used_paths: dict[str, str] = {}
    for resource in resources:
        if resource.get("extraction_policy") == "full_text":
            resource["local_path"] = allocate_local_path(
                resource["resource_type"], resource["source_url"], resource.get("local_path"), used_paths,
            )
    new_children = []
    updated = []
    for resource in resources:
        if resource["resource_type"] == "videos":
            _document, children, new_resource = extract_resource(course, resource)
            updated.append(new_resource)
            new_children.extend(children)
            continue
        if resource["extraction_policy"] != "full_text":
            updated.append(resource)
            continue
        document, children, new_resource = extract_resource(course, resource)
        if document and new_resource.get("local_path"):
            write_text(folder / new_resource["local_path"], document)
        updated.append(new_resource)
        new_children.extend(children)
    known = {row["source_url"] for row in updated}
    type_seen = Counter(row["resource_type"] for row in updated)
    for child in new_children:
        if child["source_url"] in known:
            continue
        known.add(child["source_url"])
        rtype = child["resource_type"]
        type_seen[rtype] += 1
        policy, status, local_path = extraction_plan(rtype, child["source_url"])
        updated.append({
            "resource_id": f"{course['course_id']}-{rtype.replace('_', '-')}-{type_seen[rtype]}",
            "course_id": course["course_id"],
            "resource_type": rtype,
            "source_title": child["source_title"],
            "source_url": child["source_url"],
            "source_format": "pdf" if extension_of(child["source_url"]) == ".pdf" else extension_of(child["source_url"]).lstrip(".") or "html",
            "availability": "available",
            "extraction_policy": policy,
            "extraction_status": status,
            "local_path": None,
            "capture_date": CAPTURE_DATE,
            "content_sha256": None,
            "error": None,
        })
    statuses = [row["extraction_status"] for row in updated if row["extraction_policy"] == "full_text"]
    if statuses and all(item == "complete" for item in statuses):
        course["extraction_status"] = "complete"
    elif any(item == "complete" for item in statuses):
        course["extraction_status"] = "partial"
    elif statuses:
        course["extraction_status"] = "failed"
    course["last_verified_date"] = CAPTURE_DATE
    write_course_files(course, updated)
    print(f"extracted {slug} {course['extraction_status']} full_text={statuses.count('complete')}/{len(statuses)}", flush=True)


def select_sample(limit: int) -> list[str]:
    """Pick review courses by the department printed first on the OCW page.

    Cross-listed courses are not used to represent a department that is only
    their second affiliation. Within a department, prefer pages that actually
    publish a syllabus, calendar, and assignments.
    """
    records = list(iter_saved_records())
    if not records:
        raise SystemExit("no discovered courses")
    chosen: list[str] = []
    chosen_slugs: set[str] = set()

    def richness(saved: dict) -> tuple:
        resources = saved["course"]["resources"]
        return (
            int(bool(resources.get("syllabus"))),
            int(bool(resources.get("calendar"))),
            int(bool(resources.get("assignments"))),
            int(bool(resources.get("exams"))),
            int(bool(resources.get("readings"))),
            saved["course"].get("year") or 0,
        )

    def take(predicate, label: str):
        if len(chosen) >= limit:
            return
        pool = [
            saved for saved in records
            if saved["course"]["course_slug"] not in chosen_slugs and predicate(saved)
        ]
        if not pool:
            print(f"sample missing: {label}", flush=True)
            return
        saved = max(pool, key=richness)
        chosen.append(saved["course"]["course_slug"])
        chosen_slugs.add(saved["course"]["course_slug"])
        print(f"sample {label}: {saved['course']['course_slug']}", flush=True)

    def first_dept(saved: dict) -> str:
        departments = saved["course"].get("departments") or []
        return departments[0] if departments else ""

    def has(saved: dict, key: str) -> bool:
        return bool(saved["course"]["resources"].get(key))

    take(lambda s: s["course"]["course_slug"] == "6-006-introduction-to-algorithms-spring-2020", "EECS anchor")
    for dept in [
        "Mathematics", "Physics", "Biology", "Chemistry", "Economics",
        "Sloan School of Management", "Architecture", "Political Science",
        "Mechanical Engineering", "History", "Literature",
        "Brain and Cognitive Sciences", "Materials Science and Engineering",
        "Aeronautics and Astronautics", "Urban Studies and Planning",
        "Linguistics and Philosophy",
    ]:
        take(lambda s, dept=dept: first_dept(s) == dept and has(s, "syllabus"), dept)
    take(lambda s: has(s, "instructor_insights") and has(s, "syllabus"), "instructor insights")
    take(
        lambda s: has(s, "projects") and has(s, "syllabus") and first_dept(s) not in {
            "Electrical Engineering and Computer Science",
        },
        "projects",
    )
    take(lambda s: s["course"]["course_slug"] == "res-tll-005-how-to-speak-january-iap-2018", "non-credit")
    if not any(slug.startswith("res-tll-005-") for slug in chosen):
        take(lambda s: "Non-Credit" in (s["course"].get("academic_levels") or []) and has(s, "syllabus"), "non-credit fallback")
    chosen = chosen[:limit]
    write_text(CACHE / "sample_slugs.txt", "\n".join(chosen) + "\n")
    return chosen


def extract_many(slugs: list[str]):
    for slug in slugs:
        try:
            extract_slug(slug)
        except Exception as exc:  # noqa: BLE001
            print(f"extract failed {slug}: {exc}", flush=True)
    rebuild_indexes()


def self_test():
    reserve_existing_ids()
    rows = load_api_courses(refresh=False)
    target = next(row for row in rows if course_slug_of(row) == "6-006-introduction-to-algorithms-spring-2020")
    status = discover_one(target)
    print(json.dumps(status, ensure_ascii=False, indent=2))
    saved = load_saved(status["course_slug"])
    course = saved["course"]
    assert course["course_codes"][0] == "6.006", course["course_codes"]
    assert course["term"] == "Spring" and course["year"] == 2020
    assert course["academic_levels"] == ["Undergraduate"]
    assert "Electrical Engineering and Computer Science" in course["departments"]
    assert course["subject_primary"] == "Computer Science", course["subject_primary"]
    assert "Algorithms and Data Structures" in course["subject_secondary"]
    assert course["resources"]["syllabus"] and course["resources"]["calendar"]
    assert any(r["resource_type"] == "syllabus" for r in saved["resources"])
    extract_slug(course["course_slug"])
    syllabus = (COURSES / course["course_slug"] / "syllabus.md").read_text(encoding="utf-8")
    assert "Source: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/syllabus/" in syllabus
    assert "Prerequisites" in syllabus
    assert "http://" in syllabus or "https://ocw.mit.edu/courses/" in syllabus
    assert "Give Now" not in syllabus
    body = syllabus.split("\n---\n", 1)[-1]
    assert "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016" in body
    assert "](/courses/" not in body
    print("self-test ok", flush=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Crawl MIT OCW into the teaching_cases/MIT catalog")
    parser.add_argument("--rate", type=float, default=4, help="maximum HTTP requests per second")
    sub = parser.add_subparsers(dest="command", required=True)
    discover_parser = sub.add_parser("discover")
    discover_parser.add_argument("--limit", type=int, default=0)
    discover_parser.add_argument("--slug", default="")
    discover_parser.add_argument("--workers", type=int, default=4)
    discover_parser.add_argument("--refresh-api", action="store_true")
    sub.add_parser("rebuild")
    sub.add_parser("self-test")
    extract_parser = sub.add_parser("extract")
    extract_parser.add_argument("--slug", action="append", default=[])
    extract_parser.add_argument("--sample", type=int, default=0)
    extract_parser.add_argument("--all", action="store_true", help="extract every course that is not already complete")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    global LIMITER
    LIMITER = Limiter(args.rate)
    OUT.mkdir(parents=True, exist_ok=True)
    if args.command == "discover":
        discover(args)
    elif args.command == "rebuild":
        rebuild_indexes()
    elif args.command == "self-test":
        self_test()
    elif args.command == "extract":
        slugs = list(args.slug)
        if args.sample:
            slugs.extend(select_sample(args.sample))
        if args.all:
            slugs.extend(
                saved["course"]["course_slug"]
                for saved in iter_saved_records()
                if saved["course"].get("extraction_status") != "complete"
            )
        slugs = list(dict.fromkeys(slugs))
        if not slugs:
            raise SystemExit("extract needs --slug or --sample")
        extract_many(slugs)


if __name__ == "__main__":
    main()
