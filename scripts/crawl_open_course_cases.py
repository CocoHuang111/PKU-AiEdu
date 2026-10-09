#!/usr/bin/env python3
"""Build source-faithful MIT innovation and current course-case corpora.

The crawler stores rendered Markdown, never raw HTML. Text below each document's
separator is copied from the public source page without translation or
paraphrase. Chinese retrieval summaries are generated separately and can be
refreshed without touching the English source text.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

import crawl_mit_ocw as mit


ROOT = Path(__file__).resolve().parents[1]
CORPORA = ROOT / "knowledge" / "corpora"
CAPTURE_DATE = "2026-10-09"
UA = "PKU-Wenjiao-KnowledgeBase/1.0 (public educational resources)"

MIT_INDEX = "https://openlearning.mit.edu/mit-faculty/residential-digital-innovations"
MIT_OUT = CORPORA / "teaching_cases" / "MIT-Open-Learning"
COURSE_OUT = CORPORA / "course_cases"

HARVARD = {
    "cs50x": "https://cs50.harvard.edu/x/",
    "games": "https://cs50.harvard.edu/games/",
    "ai": "https://cs50.harvard.edu/ai/",
    "business": "https://cs50.harvard.edu/business/",
    "cybersecurity": "https://cs50.harvard.edu/cybersecurity/",
    "law": "https://cs50.harvard.edu/law/",
    "python": "https://cs50.harvard.edu/python/",
    "r": "https://cs50.harvard.edu/r/",
    "scratch": "https://cs50.harvard.edu/scratch/",
    "sql": "https://cs50.harvard.edu/sql/",
    "web": "https://cs50.harvard.edu/web/",
}

COURSES = {
    **{
        f"harvard-{slug}": {
            "institution": "Harvard University",
            "platform": "CS50 OpenCourseWare",
            "url": url,
            "term": "Continuously updated",
            "status": "active",
        }
        for slug, url in HARVARD.items()
    },
    "stanford-cs106a-autumn-2026": {
        "institution": "Stanford University",
        "platform": "Stanford CS106A",
        "url": "https://web.stanford.edu/class/cs106a/",
        "term": "Autumn 2026",
        "status": "in_progress",
    },
    "cmu-15-122-fall-2026": {
        "institution": "Carnegie Mellon University",
        "platform": "CMU 15-122",
        "url": "https://www.cs.cmu.edu/~15122/",
        "term": "Fall 2026",
        "status": "in_progress",
    },
}

TOOL_ZH = {
    "Active Learning": "主动学习",
    "Blended Learning & Flipped Classroom": "混合式学习与翻转课堂",
    "Remote Teaching": "远程教学",
    "Flexible Course Delivery": "灵活课程实施",
    "Simulations & Visualizations": "模拟与可视化",
    "Online Assessments & Rapid Feedback": "在线评价与快速反馈",
    "Lightboard": "光板教学",
    "Perusall": "Perusall社会化批注",
    "Piazza": "Piazza课程讨论",
    "Adaptive Hinting": "自适应提示",
    "Slack": "Slack协作",
    "Dropbox": "Dropbox资源协作",
}


class Rate:
    def __init__(self, per_second: float = 3.0):
        self.delay = 1.0 / per_second
        self.last = 0.0

    def wait(self):
        delta = time.monotonic() - self.last
        if delta < self.delay:
            time.sleep(self.delay - delta)
        self.last = time.monotonic()


RATE = Rate()


def fetch(url: str) -> tuple[int, str, str]:
    error = None
    for attempt in range(4):
        RATE.wait()
        req = urllib.request.Request(
            url,
            headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                charset = "utf-8"
                match = re.search(r"charset=([\w-]+)", resp.headers.get("Content-Type", ""), re.I)
                if match:
                    charset = match.group(1)
                return resp.status, resp.geturl(), data.decode(charset, "replace")
        except urllib.error.HTTPError as exc:
            if exc.code in {429, 500, 502, 503, 504} and attempt < 3:
                time.sleep(2**attempt)
                error = exc
                continue
            return exc.code, url, exc.read().decode("utf-8", "replace") if exc.fp else ""
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            error = exc
            time.sleep(2**attempt)
    raise RuntimeError(f"fetch failed for {url}: {error}")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:140] or "page"


def node_by_class(root, class_name: str):
    found = mit.find_all(root, class_name=class_name)
    return found[0] if found else None


def field_items(root, field_name: str) -> list[str]:
    node = node_by_class(root, field_name)
    if not node:
        return []
    items = mit.find_all(node, class_name="field__item")
    values = [mit.clean_text(item) for item in items]
    return [value for value in values if value]


def title_of(page: str, fallback: str) -> str:
    tree = mit.parse_html(page)
    for klass in ("faux-full-title", "page-title"):
        node = node_by_class(tree.root, klass)
        if node and mit.clean_text(node):
            return mit.clean_text(node)
    heads = mit.find_all(tree.root, "h1")
    if heads and mit.clean_text(heads[0]):
        return mit.clean_text(heads[0])
    titles = mit.find_all(tree.root, "title")
    return mit.clean_text(titles[0]) if titles else fallback


def best_content(page: str, site: str):
    tree = mit.parse_html(page)
    if site == "mit-open-learning":
        return node_by_class(tree.root, "news-event-wrap")
    candidates = []
    for tag in ("main", "article"):
        candidates.extend(mit.find_all(tree.root, tag))
    for ident in ("main-content", "content", "page-content"):
        node = mit.find_id(tree.root, ident)
        if node:
            candidates.append(node)
    for klass in (
        "container-xl",
        "container-lg",
        "container",
        "content",
        "main",
        "page-content",
    ):
        candidates.extend(mit.find_all(tree.root, class_name=klass))
    if not candidates:
        bodies = mit.find_all(tree.root, "body")
        candidates = bodies or [tree.root]
    return max(candidates, key=lambda n: len(mit.clean_text(n)))


def clean_markdown(body: str) -> str:
    body = body.replace("(opens in a new window)", "")
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip() + "\n"


def page_header(summary: str, source_url: str) -> str:
    return (
        f"> {summary}\n\n"
        f"- Source: {source_url}\n"
        f"- source_format: html\n"
        f"- capture_date: {CAPTURE_DATE}\n\n"
        "---\n\n"
    )


def source_header(source_url: str) -> str:
    return (
        f"- Source: {source_url}\n"
        f"- source_format: html\n"
        f"- capture_date: {CAPTURE_DATE}\n\n"
        "---\n\n"
    )


def write_jsonl(path: Path, rows: list[dict]):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def source_links(node, base_url: str) -> list[dict]:
    rows = []
    seen = set()
    for anchor in mit.find_all(node, "a"):
        href = mit.absolute_url(base_url, anchor.attrs.get("href"))
        if not href or href in seen:
            continue
        seen.add(href)
        rows.append({"title": mit.clean_text(anchor), "url": href})
    return rows


def fallback_innovation_summary(title: str, subjects: list[str], instructors: list[str], tools: list[str]) -> str:
    parts = [f"MIT Open Learning 教学创新资料《{title}》"]
    if subjects:
        parts.append(f"涉及课程 {', '.join(subjects)}")
    if instructors:
        parts.append(f"教师/作者为 {', '.join(instructors)}")
    if tools:
        translated = [TOOL_ZH.get(t, t) for t in tools]
        parts.append(f"重点呈现{'、'.join(translated)}的教学应用")
    return "，".join(parts) + "。用于检索具体教学问题、实施策略、数字工具和课程情境；英文原文位于分隔线后。"


def mit_innovations():
    status, final, index = fetch(MIT_INDEX)
    if status != 200:
        raise RuntimeError(f"MIT innovation index HTTP {status}")
    tree = mit.parse_html(index)
    urls = []
    seen = set()
    prefix = "/mit-faculty/residential-digital-innovations/"
    for anchor in mit.find_all(tree.root, "a"):
        href = anchor.attrs.get("href") or ""
        if not href.startswith(prefix):
            continue
        url = urljoin(final, href)
        if url not in seen:
            seen.add(url)
            urls.append(url)
    if len(urls) != 146:
        raise RuntimeError(f"expected 146 MIT innovation URLs, found {len(urls)}")

    cases = MIT_OUT / "cases"
    cases.mkdir(parents=True, exist_ok=True)
    catalog = []
    for number, url in enumerate(urls, 1):
        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        directory = cases / slug
        status, final_url, page = fetch(url)
        if status != 200:
            catalog.append({"case_id": f"mit-open-learning-{slug}", "source_url": url, "extraction_status": "failed"})
            print(f"MIT {number:03}/146 failed HTTP {status}: {slug}", flush=True)
            continue
        parsed = mit.parse_html(page)
        title = title_of(page, slug)
        subjects = field_items(parsed.root, "field--name-field-mitx-course-id")
        departments = field_items(parsed.root, "field--name-field-mitx-course-department")
        instructors = field_items(parsed.root, "field--name-field-mitx-instructors")
        tools = field_items(parsed.root, "field--name-field-digital-innovations-tools")
        node = best_content(page, "mit-open-learning")
        body = clean_markdown(mit.render_markdown(node, final_url))
        summary = fallback_innovation_summary(title, subjects, instructors, tools)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "case.md").write_text(page_header(summary, final_url) + body, encoding="utf-8")
        (directory / "检索摘要.md").write_text(summary + "\n", encoding="utf-8")
        record = {
            "schema_version": "1.0",
            "case_id": f"mit-open-learning-{slug}",
            "institution": "Massachusetts Institute of Technology",
            "platform": "MIT Open Learning",
            "collection": "Residential Digital Innovations",
            "title": title,
            "slug": slug,
            "course_codes": subjects,
            "departments": departments,
            "instructors": instructors,
            "digital_innovations_tools": tools,
            "source_url": final_url,
            "language": "en",
            "capture_date": CAPTURE_DATE,
            "extraction_status": "complete",
            "content_sha256": sha(body),
        }
        (directory / "case.yaml").write_text(mit.to_yaml(record) + "\n", encoding="utf-8")
        resources = [{
            "resource_type": "case_page",
            "title": title,
            "source_url": final_url,
            "source_format": "html",
            "extraction_policy": "full_text",
            "extraction_status": "complete",
            "local_path": "case.md",
            "content_sha256": sha(body),
        }]
        resources.extend({"resource_type": "linked_resource", **link} for link in source_links(node, final_url))
        write_jsonl(directory / "resources.jsonl", resources)
        catalog.append({
            "case_id": record["case_id"],
            "title": title,
            "source_url": final_url,
            "course_codes": subjects,
            "digital_innovations_tools": tools,
            "extraction_status": "complete",
            "local_path": str(directory.relative_to(MIT_OUT) / "case.md"),
        })
        print(f"MIT {number:03}/146 complete: {slug}", flush=True)
    write_jsonl(MIT_OUT / "catalog.jsonl", catalog)
    readme = f"""# MIT Open Learning 教学创新资料库

本目录保存 MIT Open Learning “Residential Digital Innovations” 的 **146 项**公开资料。每项英文正文不翻译、不改写；中文内容仅用于检索。

- 入口：<{MIT_INDEX}>
- 采集日期：{CAPTURE_DATE}
- 数量：{len(catalog)}
- 正文：`cases/<slug>/case.md`（分隔线后为英文原文）
- 中文检索摘要：`cases/<slug>/检索摘要.md`
- 元数据：`case.yaml`
- 来源与链接：`resources.jsonl`

图片、视频和二进制附件不下载，只保留原网页地址。`catalog.jsonl` 为全量清单。本次只整理知识库，没有执行 RAG 入库。
"""
    (MIT_OUT / "README.md").write_text(readme, encoding="utf-8")


def allowed_course_link(home_url: str, candidate: str, key: str) -> bool:
    parsed_home, parsed = urlparse(home_url), urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or parsed.netloc != parsed_home.netloc:
        return False
    if re.search(r"\.(?:pdf|zip|png|jpe?g|gif|svg|mp4|mov|mp3|csv|docx?|pptx?|xlsx?)(?:$|\?)", parsed.path, re.I):
        return False
    path = parsed.path.rstrip("/") + "/"
    if key.startswith("harvard-"):
        return path.startswith(parsed_home.path.rstrip("/") + "/") and not any(x in path for x in ("/courses/", "/communities/"))
    if key.startswith("stanford-"):
        return path.startswith("/class/cs106a/") and not any(x in path for x in ("/ide/", "/img/", "/static/"))
    if key.startswith("cmu-"):
        return path.startswith("/~15122/") and not any(x in path for x in ("/activities", "/autolab", "/gradescope"))
    return False


def linked_pages(home_url: str, page: str, key: str) -> list[tuple[str, str]]:
    # Course navigation often sits outside the central article. Read links from
    # the whole document, then constrain them to the course URL prefix.
    root = mit.parse_html(page).root
    links = [(home_url, "Course Home")]
    seen = {home_url.rstrip("/")}
    for anchor in mit.find_all(root, "a"):
        href = mit.absolute_url(home_url, anchor.attrs.get("href"))
        if not href:
            continue
        href = href.split("#", 1)[0]
        normalized = href.rstrip("/")
        if normalized in seen or not allowed_course_link(home_url, href, key):
            continue
        seen.add(normalized)
        links.append((href, mit.clean_text(anchor) or normalized.rsplit("/", 1)[-1]))
    return links


def filename_for(url: str, home_url: str, used: set[str]) -> str:
    if url.rstrip("/") == home_url.rstrip("/"):
        name = "course-description.md"
    else:
        path = urlparse(url).path.rstrip("/").split("/")[-1]
        path = re.sub(r"\.(?:s?html?)$", "", path, flags=re.I)
        name = slugify(path) + ".md"
    base = name[:-3]
    counter = 2
    while name in used:
        name = f"{base}-{counter}.md"
        counter += 1
    used.add(name)
    return name


def fallback_course_summary(title: str, institution: str, term: str, headings: list[str]) -> str:
    topics = "、".join(headings[:10])
    result = f"{institution}《{title}》，版本为 {term}。用于按课程主题、教学安排、作业评价、学习支持与课程政策检索相似课程"
    if topics:
        result += f"；已公开页面涉及：{topics}"
    return result + "。各文档分隔线后保留英文原文。"


def crawl_course(key: str, conf: dict):
    school = "Harvard-CS50" if key.startswith("harvard-") else "Stanford" if key.startswith("stanford-") else "CMU"
    directory = COURSE_OUT / school / key
    directory.mkdir(parents=True, exist_ok=True)
    status, final_home, home_page = fetch(conf["url"])
    if status != 200:
        raise RuntimeError(f"{key} home HTTP {status}")
    title = title_of(home_page, key)
    if key == "stanford-cs106a-autumn-2026":
        title = "CS106A: Programming Methodology"
    elif key == "cmu-15-122-fall-2026":
        title = "CS 15-122: Principles of Imperative Computation"
    pages = linked_pages(final_home, home_page, key)
    resources = []
    headings = []
    used = set()
    for number, (url, link_title) in enumerate(pages, 1):
        p_status, final_url, page = (status, final_home, home_page) if number == 1 else fetch(url)
        if p_status != 200:
            resources.append({"resource_type": "course_page", "title": link_title, "source_url": url, "extraction_status": "failed", "error": f"HTTP {p_status}"})
            continue
        node = best_content(page, "course")
        body = clean_markdown(mit.render_markdown(node, final_url))
        if len(re.sub(r"\s+", "", body)) < 60:
            resources.append({
                "resource_type": "linked_page",
                "title": link_title,
                "source_url": final_url,
                "source_format": "html",
                "extraction_policy": "link_only",
                "extraction_status": "skipped",
                "reason": "page has no server-rendered text",
            })
            continue
        page_title = title_of(page, link_title)
        page_heads = mit.headings_of(body)
        headings.extend(page_heads)
        filename = filename_for(final_url, final_home, used)
        (directory / filename).write_text(source_header(final_url) + body, encoding="utf-8")
        resources.append({
            "resource_type": "course_page",
            "title": page_title,
            "source_url": final_url,
            "source_format": "html",
            "extraction_policy": "full_text",
            "extraction_status": "complete",
            "local_path": filename,
            "content_sha256": sha(body),
        })
        print(f"{key} {number:02}/{len(pages):02} complete: {filename}", flush=True)
    summary = fallback_course_summary(title, conf["institution"], conf["term"], list(dict.fromkeys(headings)))
    (directory / "检索摘要.md").write_text(summary + "\n", encoding="utf-8")
    record = {
        "schema_version": "1.0",
        "course_id": key,
        "institution": conf["institution"],
        "platform": conf["platform"],
        "course_title": title,
        "course_slug": key,
        "version": conf["term"],
        "offering_status": conf["status"],
        "course_url": final_home,
        "language": "en",
        "capture_date": CAPTURE_DATE,
        "last_verified_date": CAPTURE_DATE,
        "extraction_status": "complete" if resources and all(r["extraction_status"] in {"complete", "skipped"} for r in resources) else "partial",
        "page_count": sum(r.get("extraction_status") == "complete" for r in resources),
    }
    (directory / "course.yaml").write_text(mit.to_yaml(record) + "\n", encoding="utf-8")
    write_jsonl(directory / "resources.jsonl", resources)
    return record


def course_cases():
    COURSE_OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for key, conf in COURSES.items():
        rows.append(crawl_course(key, conf))
    write_jsonl(COURSE_OUT / "catalog-current.jsonl", rows)
    readme = f"""# 国外公开课程案例库

本目录保存完整课程层面的公开资料，服务于相似课程匹配、大纲设计和教学设计。英文正文不翻译、不改写，中文检索摘要单独保存。

本次更新（{CAPTURE_DATE}）：

- Harvard CS50：11 门当前活跃课程（旗舰 CS50x + 官方列表中的 10 门课程）；页面持续更新，以抓取日期标识版本。
- Stanford CS106A：Autumn 2026，学期进行中，保存截至抓取日公开的页面。
- CMU 15-122：Fall 2026，学期进行中，保存截至抓取日公开的页面。

每门课程包含 `course.yaml`、`resources.jsonl`、`检索摘要.md` 和实际公开且成功提取的英文页面 Markdown。视频、图片与二进制附件不下载，只保留网页链接。本次未执行 RAG 入库。
"""
    (COURSE_OUT / "README.md").write_text(readme, encoding="utf-8")


def load_env(path: Path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def llm_json(prompt: str) -> dict[str, str]:
    load_env(ROOT / ".env")
    api_key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY is not configured")
    payload = json.dumps({
        "model": "qwen-plus",
        "messages": [
            {"role": "system", "content": "你负责生成教育知识库的中文检索摘要。只依据输入材料，不增加外部事实。严格输出JSON对象。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 4000,
        "response_format": {"type": "json_object"},
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        response = json.loads(resp.read().decode("utf-8"))
    content = response["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content)
    return json.loads(content)


def improve_summaries(root: Path, kind: str):
    yaml_name = "case.yaml" if kind == "case" else "course.yaml"
    dirs = sorted(path.parent for path in root.rglob(yaml_name))
    batch_size = 8 if kind == "case" else 4
    for start in range(0, len(dirs), batch_size):
        batch = dirs[start : start + batch_size]
        inputs = []
        for directory in batch:
            meta = (directory / yaml_name).read_text(encoding="utf-8")
            if kind == "case":
                source_files = [directory / "case.md"]
            else:
                preferred = (
                    "course-description.md", "syllabus.md", "syllabus-cs106a.md",
                    "about.md", "schedule.md", "weeks.md", "assignments.md",
                    "projects.md", "psets.md", "handouts.md", "grade-meaning.md",
                    "honesty.md",
                )
                source_files = [directory / name for name in preferred if (directory / name).exists()]
                source_files.extend(
                    path for path in sorted(directory.glob("*.md"))
                    if path.name not in {"检索摘要.md", *preferred} and path not in source_files
                )
            excerpts = []
            remaining = 12000 if kind == "course" else 7000
            for source_file in source_files:
                if remaining <= 0 or not source_file.exists():
                    break
                text = source_file.read_text(encoding="utf-8")
                original = text.split("\n---\n", 1)[-1]
                excerpt = original[: min(3000, remaining)]
                excerpts.append(f"[{source_file.name}]\n{excerpt}")
                remaining -= len(excerpt)
            inputs.append({"id": directory.name, "metadata": meta[:4000], "source_excerpts": excerpts})
        instruction = (
            "为下列材料分别写一段180至300字的中文RAG检索摘要。重点写可匹配的课程主题或教学问题、对象/情境、实施策略、工具、评价方式和已陈述的效果；"
            "保留重要英文专名和课程号；不得推测材料未写的信息，不要评价，不要翻译全文。返回JSON对象，键必须是输入id，值只能是一段摘要文本。\n\n"
            + json.dumps(inputs, ensure_ascii=False)
        )
        result = llm_json(instruction)
        for directory in batch:
            summary = re.sub(r"\s+", " ", result.get(directory.name, "")).strip()
            if len(summary) < 40:
                continue
            summary_path = directory / "检索摘要.md"
            summary_path.write_text(summary + "\n", encoding="utf-8")
            source_file = directory / "case.md"
            if kind == "case" and source_file.exists():
                text = source_file.read_text(encoding="utf-8")
                marker = text.find("\n\n- Source:")
                if text.startswith("> ") and marker > 0:
                    text = "> 检索摘要：" + summary + text[marker:]
                    source_file.write_text(text, encoding="utf-8")
        print(f"summaries {start + 1}-{start + len(batch)} / {len(dirs)}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        choices=("mit", "courses", "mit-summaries", "course-summaries", "summaries", "all"),
    )
    args = parser.parse_args()
    if args.target in {"mit", "all"}:
        mit_innovations()
    if args.target in {"courses", "all"}:
        course_cases()
    if args.target in {"mit-summaries", "summaries", "all"}:
        improve_summaries(MIT_OUT, "case")
    if args.target in {"course-summaries", "summaries", "all"}:
        improve_summaries(COURSE_OUT / "Harvard-CS50", "course")
        improve_summaries(COURSE_OUT / "Stanford", "course")
        improve_summaries(COURSE_OUT / "CMU", "course")


if __name__ == "__main__":
    main()
