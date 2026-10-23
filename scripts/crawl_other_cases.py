#!/usr/bin/env python3
"""Save source-faithful text for the teaching-case sites behind teaching_cases/other.

Cornell, Columbia, Open Yale Courses, and Poorvu Center pages are fetched
directly. Michigan CRLT returns HTTP 403 to this client, so those articles
come from a browser capture of the Teaching Innovation Prize pages that
responded. Binary files are indexed, not downloaded. Raw HTML is not kept.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

import crawl_mit_ocw as mit

ROOT = Path(__file__).resolve().parents[1]
OTHER = ROOT / "knowledge" / "corpora" / "teaching_cases" / "other"
UA = "PKU-Wenjiao-KnowledgeBase/1.0 (educational catalog; university teaching cases)"
CAPTURE_DATE = "2026-10-08"
MICHIGAN_CAPTURE = Path(
    "/Users/huangkefan/.cursor/browser-logs/"
    "cdp-response-Runtime.evaluate-2026-10-08T05-40-19-550Z.json"
)

# Award year is printed on the winners index, not always on the article.
MICHIGAN_YEARS = {
    "https://crlt.umich.edu/modelling-art-tolerance-and-reason-world-seemingly-intractably-divided-pagan-christian-podcasts": "2025",
    "https://crlt.umich.edu/modules-introduce-social-issues-foundational-engineering-courses": "2025",
    "https://crlt.umich.edu/participatory-action-research-class-improve-teaching-across-campus": "2025",
    "https://crlt.umich.edu/pluralism-workbook-building-skills-talk-across-differences-hard-topics": "2025",
    "https://crlt.umich.edu/teaching-humanities-designing-generative-ai-chatbots": "2025",
    "https://crlt.umich.edu/closing-loop-positioning-formerly-incarcerated-students-co-instructors-equity-focused-community": "2024",
    "https://crlt.umich.edu/digital-sandbox-experiential-model-based-engineering-education": "2024",
    "https://crlt.umich.edu/equity-analytics-new-course-addressing-societal-inequality": "2024",
    "https://crlt.umich.edu/stacked-mentorship-model-new-model-mentorship-equity-architectural-education": "2024",
    "https://crlt.umich.edu/supporting-anti-racist-teaching-through-health-equity-anti-racist-teaching-heart-free-online": "2024",
    "https://crlt.umich.edu/abrahamic-sensorium": "2023",
    "https://crlt.umich.edu/architecture-and-artificial-intelligence": "2023",
    "https://crlt.umich.edu/humanize-numbers-using-photographic-collaboration-expose-humanity-incarcerated-individuals": "2023",
    "https://crlt.umich.edu/lettersmith-writing-support-tool-provides-structured-guidance-and-encourages-metacognition": "2023",
    "https://crlt.umich.edu/repoliticizing-engineering-knowledge-through-racism-conscious-engineering-instruction": "2023",
    "https://crlt.umich.edu/community-engaged-research-schools-support-newcomer-students": "2022",
    "https://crlt.umich.edu/life-longitudinal-interprofessional-family-based-experience": "2022",
    "https://crlt.umich.edu/shifting-eurocentrism-and-enhancing-dei-voice-classes": "2022",
    "https://crlt.umich.edu/simulating-interactions-between-science-and-policymaking": "2022",
    "https://crlt.umich.edu/slack-bots-remote-asynchronous-education": "2022",
    "https://crlt.umich.edu/african-centered-practices-community-and-classroom": "2021",
    "https://crlt.umich.edu/breaking-ap-calculus-hold-stem": "2021",
    "https://crlt.umich.edu/creative-contracts-incentivizing-engagement-writerly-behaviors": "2021",
    "https://crlt.umich.edu/improving-our-city-ann-arbor-human-rights-commission-project": "2021",
    "https://crlt.umich.edu/mixed-reality-medical-education-and-practice": "2021",
    "https://crlt.umich.edu/umturk-and-inclusive-teaching-u-m-methods-courses": "2021",
    "https://crlt.umich.edu/building-high-stakes-skills-outside-operating-room-realistic-3d-models": "2020",
    "https://crlt.umich.edu/gender-neutral-fibers-initiative-leveraging-creative-process-inclusive-learning": "2020",
    "https://crlt.umich.edu/good-words-transforming-teaching-public-speaking": "2020",
    "https://crlt.umich.edu/tandem-automating-tailored-guidance-students-working-teams": "2020",
    "https://crlt.umich.edu/trust-your-gut-retaining-stem-students-through-authentic-research": "2020",
    "https://crlt.umich.edu/advancing-diversity-equity-and-inclusion-advanced-quantitative-courses": "2019",
    "https://crlt.umich.edu/design-charrette-hacking-health-through-community-engagement-innovation-and-entrepreneurship": "2019",
    "https://crlt.umich.edu/m-write-making-writing-learn-pedagogies-practical-and-sustainable": "2019",
    "https://crlt.umich.edu/problem-roulette-stress-free-practice-zone-supports-student-success": "2019",
}

# Poorvu /posts/ is a news stream. These slugs are the posts about a course,
# a classroom activity, or a teaching partnership. The rest are center news.
POORVU_KEEP = (
    "faculty-student-partnership",
    "spanish-learning",
    "canvas-lightning",
    "bulldog-days",
    "mastering-the-craft",
    "online-course-helps-parents",
    "writing-beyond-yale",
    "comedy-chops",
    "safer-chemical",
    "language-tastings",
    "writing-partner",
    "writing-expertise",
    "yielding-results",
)

EXTRA_COLUMBIA = [
    "https://ctl.columbia.edu/spotlight/rachel-cummings/",
    "https://ctl.columbia.edu/spotlight/sewell-chan-tollman/",
    "https://ctl.columbia.edu/announcements/faculty-spotlight-mary-ann-price/",
    "https://ctl.columbia.edu/announcements/techniques-for-just-in-time-teaching-in-a-medical-school-course/",
]

LIMITER = mit.Limiter(4)


def break_info_rows(page: str) -> str:
    """Cornell case pages store the fact table as nested divs, not a <table>."""
    return re.sub(
        r'<div class="info-row"><div class="info-cell info-label">(.*?)</div>'
        r'<div class="info-cell info-value">(.*?)</div></div>',
        r"<p><strong>\1:</strong> \2</p>",
        page,
        flags=re.S,
    )


def fetch_text(url: str) -> tuple[int, str, str]:
    last_error = None
    for attempt in range(4):
        LIMITER.wait()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/json"})
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
                charset = "utf-8"
                match = re.search(r"charset=([\w-]+)", resp.headers.get("Content-Type", ""), re.I)
                if match:
                    charset = match.group(1)
                return resp.status, resp.geturl(), data.decode(charset, "replace")
        except urllib.error.HTTPError as exc:
            if exc.code in {429, 500, 502, 503, 504} and attempt < 3:
                time.sleep(2 ** attempt)
                last_error = exc
                continue
            body = exc.read().decode("utf-8", "replace") if exc.fp else ""
            return exc.code, url, body
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"fetch failed for {url}: {last_error}")


def plain(value: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    return re.sub(r"\s+", " ", text).strip()


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    slug = path.split("/")[-1] if path else "index"
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    return slug[:120] or "index"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def license_url(page_html: str) -> str:
    match = re.search(r"https://creativecommons\.org/licenses/[^\"'\s<]+", page_html or "")
    return match.group(0).rstrip(").,") if match else ""


def content_node(page_html: str, class_names: tuple[str, ...]):
    tree = mit.parse_html(page_html)
    for name in class_names:
        nodes = mit.find_all(tree.root, class_name=name)
        for node in nodes:
            parent = tree.parents.get(node)
            footer = False
            while parent is not None:
                if parent.tag == "footer" or parent.has_class("footer") or "footer" in (parent.attrs.get("id") or ""):
                    footer = True
                    break
                parent = tree.parents.get(parent)
            if not footer and len(mit.clean_text(node)) > 40:
                return node
    main = mit.find_id(tree.root, "main-content") or mit.find_id(tree.root, "content")
    return main


def render_node(node, base_url: str) -> str:
    if node is None:
        return ""
    return mit.render_markdown(node, base_url)


def headings_of(markdown: str) -> list[str]:
    return mit.headings_of(markdown)


def header(summary: str, source_url: str, source_format: str, license_href: str) -> str:
    lines = [
        f"> {summary}",
        "",
        f"- Source: {source_url}",
        f"- source_format: {source_format}",
        f"- capture_date: {CAPTURE_DATE}",
    ]
    if license_href:
        lines.append(f"- license: {license_href}")
    lines.extend(["", "---", ""])
    return "\n".join(lines)


def course_source_header(source_url: str, source_format: str, license_href: str) -> str:
    lines = [
        f"- Source: {source_url}",
        f"- source_format: {source_format}",
        f"- capture_date: {CAPTURE_DATE}",
    ]
    if license_href:
        lines.append(f"- license: {license_href}")
    lines.extend(["", "---", ""])
    return "\n".join(lines)


def binary_rows(node, page_url: str, parent_title: str) -> list[dict]:
    if node is None:
        return []
    rows = []
    seen = set()
    for anchor in mit.find_all(node, "a"):
        href = mit.absolute_url(page_url, anchor.attrs.get("href"))
        if not href or href in seen or not mit.is_binary_url(href):
            continue
        seen.add(href)
        title = mit.clean_text(anchor) or parent_title
        rows.append({
            "resource_type": "binary",
            "title": title,
            "source_url": href,
            "source_format": mit.extension_of(href).lstrip(".") or "binary",
            "extraction_policy": "skip_binary",
            "extraction_status": "skipped",
            "local_path": None,
            "content_sha256": None,
        })
    return rows


def write_case(directory: Path, record: dict, resources: list[dict], body: str, summary: str):
    directory.mkdir(parents=True, exist_ok=True)
    source_url = record["source_url"]
    license_href = record.get("license_url") or ""
    verbatim = body.strip() + "\n"
    document = header(summary, source_url, "html", license_href) + verbatim
    case_path = directory / "case.md"
    case_path.write_text(document, encoding="utf-8")
    digest = sha256_text(verbatim)
    page_row = {
        "resource_type": "case_page",
        "title": record["title"],
        "source_url": source_url,
        "source_format": "html",
        "extraction_policy": "full_text",
        "extraction_status": "complete",
        "local_path": "case.md",
        "content_sha256": digest,
    }
    lines = [json.dumps(page_row, ensure_ascii=False)]
    for row in resources:
        lines.append(json.dumps(row, ensure_ascii=False))
    (directory / "resources.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    record["extraction_status"] = "complete"
    record["content_sha256"] = digest
    (directory / "case.yaml").write_text(mit.to_yaml(record) + "\n", encoding="utf-8")


def case_record(**fields) -> dict:
    record = {
        "schema_version": "1.0",
        "case_id": fields["case_id"],
        "institution": fields["institution"],
        "platform": fields["platform"],
        "collection": fields["collection"],
        "title": fields["title"],
        "slug": fields["slug"],
        "source_url": fields["source_url"],
        "language": "en",
        "published": fields.get("published") or None,
        "awarded_year": fields.get("awarded_year") or None,
        "license_url": fields.get("license_url") or "",
        "topic_keywords": [],
        "pedagogy_tags": [],
        "assessment_types": [],
        "capture_date": CAPTURE_DATE,
        "metadata_origin": {},
    }
    if record["published"]:
        record["metadata_origin"]["published"] = "source"
    if record["awarded_year"]:
        record["metadata_origin"]["awarded_year"] = "source"
    if record["license_url"]:
        record["metadata_origin"]["license_url"] = "source"
    return record


def gist_from_file(path: Path) -> str:
    if not path.exists():
        return ""
    first = path.read_text(encoding="utf-8").split("\n", 1)[0]
    match = re.search(r"主要内容：(.+?)。(?:页内标题：|分隔线后)", first)
    return match.group(1) if match else ""


def summary_for(title: str, institution: str, markdown: str, gist: str = "") -> str:
    heads = headings_of(markdown)
    head_text = f"页内标题：{'；'.join(heads[:12])}。" if heads else ""
    gist_text = f"主要内容：{gist}。" if gist else ""
    return (
        f"检索摘要：{institution}「{title}」。{gist_text}{head_text}"
        "分隔线后是英文原文，未翻译、未改写。"
    )


def yaml_is_complete(yaml_path: Path) -> bool:
    if not yaml_path.exists():
        return False
    return bool(
        re.search(
            r'(?m)^extraction_status:\s*"?complete"?\s*$',
            yaml_path.read_text(encoding="utf-8"),
        )
    )


def already(directory: Path) -> bool:
    if not (directory / "case.md").exists():
        return False
    return yaml_is_complete(directory / "case.yaml")


def save_article(directory: Path, record: dict, page_html: str, class_names: tuple[str, ...]):
    if already(directory):
        return "skip"
    node = content_node(page_html, class_names)
    body = render_node(node, record["source_url"])
    if len(re.sub(r"\s+", "", body)) < 80:
        record["extraction_status"] = "partial"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "case.yaml").write_text(mit.to_yaml(record) + "\n", encoding="utf-8")
        return "partial"
    write_case(
        directory,
        record,
        binary_rows(node, record["source_url"], record["title"]),
        body,
        summary_for(
            record["title"],
            record["institution"],
            body,
            gist_from_file(directory / "case.md"),
        ),
    )
    return "complete"


def write_catalog(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")


def catalog_case(record: dict) -> dict:
    return {
        "case_id": record["case_id"],
        "title": record["title"],
        "slug": record["slug"],
        "source_url": record["source_url"],
        "collection": record["collection"],
        "extraction_status": record.get("extraction_status"),
    }


def remove_old_rewrites(school: Path):
    for path in school.glob("[0-9]*.md"):
        path.unlink()
    source = school / "source"
    if source.exists():
        shutil.rmtree(source)


def cornell() -> list[dict]:
    school = OTHER / "Cornell"
    cases = school / "cases"
    status, _, raw = fetch_text("https://blogs.cornell.edu/teachingcasestudies/wp-json/wp/v2/posts?per_page=100")
    if status != 200:
        raise RuntimeError(f"Cornell API HTTP {status}")
    posts = json.loads(raw)
    rows = []
    seen_urls = set()
    for post in posts:
        url = post["link"]
        seen_urls.add(url.rstrip("/"))
        slug = slug_from_url(url)
        directory = cases / slug
        title = plain(post["title"]["rendered"])
        published = (post.get("date") or "")[:10] or None
        record = case_record(
            case_id=f"cornell-{slug}",
            institution="Cornell University",
            platform="Cornell Teaching Case Studies",
            collection="Teaching Innovation Case Study Library",
            title=title,
            slug=slug,
            source_url=url,
            published=published,
            license_url=license_url(post["content"]["rendered"]),
        )
        fragment = "<div class='field-name-body'>" + break_info_rows(post["content"]["rendered"]) + "</div>"
        state = save_article(directory, record, fragment, ("field-name-body",))
        record["extraction_status"] = "complete" if state != "partial" else "partial"
        rows.append(catalog_case(record))
        print(f"cornell {state} {slug}")

    status, final, page = fetch_text(
        "https://teaching.cornell.edu/teaching-spotlight/teaching-innovation-case-study-library"
    )
    if status != 200:
        raise RuntimeError(f"Cornell library HTTP {status}")
    tree = mit.parse_html(page)
    extra = []
    for anchor in mit.find_all(tree.root, "a"):
        href = mit.absolute_url(final, anchor.attrs.get("href"))
        if not href:
            continue
        host = urlparse(href).netloc
        path = urlparse(href).path.strip("/")
        if host == "blogs.cornell.edu" and "/teachingcasestudies/" in href:
            if any(part in path.split("/") for part in ("category", "author", "feed", "wp-json", "comments")):
                continue
            if path.count("/") < 2:
                continue
        elif host == "teaching.cornell.edu":
            parts = path.split("/")
            title = mit.clean_text(anchor)
            provost_case = (
                parts[:2] == ["teaching-spotlight", "provosts-working-group-innovation-assessment"]
                and len(parts) == 3
            )
            # Case titles on the library page are long. Site navigation is not.
            standalone_case = len(parts) == 1 and len(title) >= 40
            if not (provost_case or standalone_case):
                continue
        else:
            continue
        if href.rstrip("/") in seen_urls:
            continue
        title = mit.clean_text(anchor)
        if len(title) < 12:
            continue
        seen_urls.add(href.rstrip("/"))
        extra.append((href, title))

    for url, title in extra:
        status, final_url, page = fetch_text(url)
        slug = slug_from_url(final_url)
        directory = cases / slug
        record = case_record(
            case_id=f"cornell-{slug}",
            institution="Cornell University",
            platform="Cornell Center for Teaching Innovation",
            collection="Teaching Innovation Case Study Library",
            title=title,
            slug=slug,
            source_url=final_url,
            license_url=license_url(page) if status == 200 else "",
        )
        if status != 200:
            record["extraction_status"] = "failed"
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "case.yaml").write_text(mit.to_yaml(record) + "\n", encoding="utf-8")
            rows.append(catalog_case(record))
            print(f"cornell failed {status} {slug}")
            continue
        h1 = mit.find_all(mit.parse_html(page).root, "h1")
        if h1:
            record["title"] = mit.clean_text(h1[0]) or title
        state = save_article(directory, record, break_info_rows(page), ("field-name-body", "entry-content"))
        record["extraction_status"] = "complete" if state != "partial" else "partial"
        rows.append(catalog_case(record))
        print(f"cornell {state} {slug}")
    write_catalog(school / "catalog.jsonl", rows)
    remove_old_rewrites(school)
    return rows


def columbia() -> list[dict]:
    school = OTHER / "Columbia"
    cases = school / "cases"
    status, final, page = fetch_text("https://ctl.columbia.edu/transformations/faculty/")
    if status != 200:
        raise RuntimeError(f"Columbia faculty index HTTP {status}")
    urls = []
    seen = set()
    tree = mit.parse_html(page)
    for anchor in mit.find_all(tree.root, "a"):
        href = mit.absolute_url(final, anchor.attrs.get("href"))
        if not href:
            continue
        path = urlparse(href).path.strip("/")
        parts = path.split("/")
        if len(parts) == 3 and parts[0] == "transformations" and parts[1] == "faculty" and "{" not in parts[2]:
            url = "https://ctl.columbia.edu/" + path + "/"
            if url not in seen:
                seen.add(url)
                urls.append(url)
    for url in EXTRA_COLUMBIA:
        if url not in seen:
            seen.add(url)
            urls.append(url)
    rows = []
    for url in urls:
        status, final_url, page = fetch_text(url)
        slug = slug_from_url(final_url)
        directory = cases / slug
        title = slug
        if status == 200:
            tree = mit.parse_html(page)
            for node in mit.find_all(tree.root, "h1"):
                text = mit.clean_text(node)
                if text:
                    title = text
                    break
            if title == slug:
                body = content_node(page, ("entry-content", "post-content"))
                if body is not None:
                    for tag in ("h2", "h3"):
                        heads = mit.find_all(body, tag)
                        if not heads:
                            continue
                        text = mit.clean_text(heads[0])
                        if text:
                            title = text
                            break
        collection = "Teaching Transformations" if "/transformations/faculty/" in final_url else "CTL spotlight or announcement"
        record = case_record(
            case_id=f"columbia-{slug}",
            institution="Columbia University",
            platform="Columbia Center for Teaching and Learning",
            collection=collection,
            title=title,
            slug=slug,
            source_url=final_url,
            license_url=license_url(page) if status == 200 else "",
        )
        if status != 200:
            record["extraction_status"] = "failed"
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "case.yaml").write_text(mit.to_yaml(record) + "\n", encoding="utf-8")
            state = "failed"
        else:
            state = save_article(directory, record, page, ("entry-content", "post-content"))
            record["extraction_status"] = "complete" if state != "partial" else "partial"
        rows.append(catalog_case(record))
        print(f"columbia {state} {slug}")
    write_catalog(school / "catalog.jsonl", rows)
    remove_old_rewrites(school)
    return rows


def michigan() -> list[dict]:
    school = OTHER / "Michigan"
    cases = school / "cases"
    if not MICHIGAN_CAPTURE.exists():
        catalog = school / "catalog.jsonl"
        if catalog.exists():
            print("michigan skip: browser capture file is missing; kept saved cases")
            return [
                json.loads(line)
                for line in catalog.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        raise RuntimeError(
            "Michigan CRLT blocks scripted downloads, and the browser capture file is missing: "
            + str(MICHIGAN_CAPTURE)
        )
    payload = json.loads(MICHIGAN_CAPTURE.read_text(encoding="utf-8"))
    items = payload["result"]["value"]["items"]
    rows = []
    for item in items:
        url = item["url"]
        slug = slug_from_url(url)
        year = MICHIGAN_YEARS.get(url)
        record = case_record(
            case_id=f"michigan-{slug}",
            institution="University of Michigan",
            platform="CRLT Provost's Teaching Innovation Prize",
            collection="Provost's Teaching Innovation Prize winners",
            title=item["title"],
            slug=slug,
            source_url=url,
            awarded_year=year,
            license_url=license_url(item.get("html") or ""),
        )
        fragment = "<div class='field--name-body'>" + (item.get("html") or "") + "</div>"
        state = save_article(cases / slug, record, fragment, ("field--name-body",))
        record["extraction_status"] = "complete" if state != "partial" else "partial"
        rows.append(catalog_case(record))
        print(f"michigan {state} {slug}")
    write_catalog(school / "catalog.jsonl", rows)
    remove_old_rewrites(school)
    return rows


def oyc_home_markup(page: str) -> str:
    page = re.sub(r"<a[^>]+quicktabs/nojs[^>]*>.*?</a>", "", page, flags=re.S)
    return re.sub(
        r'<span class="views-label[^"]*">([^<]+)</span>\s*<div class="field-content">',
        r"<h2>\1</h2><div class=\"field-content\">",
        page,
    )


def labeled_values(page_html: str) -> dict[str, str]:
    tree = mit.parse_html(page_html)
    values = {}
    for node in mit.find_all(tree.root, class_name="views-field"):
        label = mit.find_all(node, class_name="views-label")
        content = mit.find_all(node, class_name="field-content")
        if label and content:
            key = mit.clean_text(label[0]).rstrip(":")
            values[key] = mit.clean_text(content[0])
    return values


def oyc_sessions(page_html: str, course_url: str) -> list[tuple[str, str]]:
    """Read the Sessions table. Some rows use another department path or /node/."""
    tree = mit.parse_html(page_html)
    found = []
    seen = set()
    for node in mit.find_all(tree.root, class_name="views-field-field-session-display-title"):
        for anchor in mit.find_all(node, "a"):
            href = mit.absolute_url(course_url, anchor.attrs.get("href"))
            if not href or href in seen or urlparse(href).netloc != "oyc.yale.edu":
                continue
            if mit.is_binary_url(href):
                continue
            title = mit.clean_text(anchor) or slug_from_url(href)
            seen.add(href)
            found.append((href, title))
    if found:
        return found
    code = slug_from_url(course_url)
    for anchor in mit.find_all(tree.root, "a"):
        href = mit.absolute_url(course_url, anchor.attrs.get("href"))
        if not href or href in seen or urlparse(href).netloc != "oyc.yale.edu":
            continue
        if mit.is_binary_url(href):
            continue
        parts = [part for part in urlparse(href).path.split("/") if part]
        if len(parts) < 2:
            continue
        parent, last = parts[-2], parts[-1]
        if parent != code and not parent.startswith(code + "-"):
            continue
        if not re.search(r"(lecture|exam|session|chapter|update|paper)", last):
            continue
        title = mit.clean_text(anchor) or last
        seen.add(href)
        found.append((href, title))
    return found


def tidy_verbatim(body: str) -> str:
    text = body.strip().replace(" <br> ", "\n")
    text = re.sub(r"(?m)^-\s*$\n", "", text)
    return text.strip() + "\n"


def write_course_page(directory: Path, filename: str, summary: str, source_url: str, body: str, license_href: str) -> str:
    verbatim = tidy_verbatim(body)
    document = course_source_header(source_url, "html", license_href) + verbatim
    (directory / filename).write_text(document, encoding="utf-8")
    return sha256_text(verbatim)


def yale_oyc() -> list[dict]:
    school = ROOT / "knowledge" / "corpora" / "course_cases" / "Yale-OYC"
    courses = school / "courses"
    status, final, page = fetch_text("https://oyc.yale.edu/courses")
    if status != 200:
        raise RuntimeError(f"OYC catalog HTTP {status}")
    course_urls = []
    seen = set()
    for match in re.findall(r'href="(/[a-z0-9-]+/[a-z0-9-]+)"', page):
        if match.count("/") != 2:
            continue
        url = urljoin("https://oyc.yale.edu", match)
        if url not in seen and not match.startswith("/courses"):
            seen.add(url)
            course_urls.append(url)
    rows = []
    for course_url in course_urls:
        slug = slug_from_url(course_url)
        directory = courses / slug
        yaml_path = directory / "course.yaml"
        if yaml_is_complete(yaml_path):
            saved = yaml_path.read_text(encoding="utf-8")
            title_match = re.search(r"^course_title:\s*(.+)$", saved, re.M)
            count_match = re.search(r"^session_count:\s*(\d+)\s*$", saved, re.M)
            url_match = re.search(r"^course_url:\s*(.+)$", saved, re.M)
            title = json.loads(title_match.group(1)) if title_match else slug
            rows.append({
                "course_id": f"oyc-{slug}",
                "course_title": title,
                "course_slug": slug,
                "course_url": json.loads(url_match.group(1)) if url_match else course_url,
                "session_count": int(count_match.group(1)) if count_match else None,
                "extraction_status": "complete",
            })
            print(f"oyc skip {slug}", flush=True)
            continue
        status, final_url, page = fetch_text(course_url)
        slug = slug_from_url(final_url)
        directory = courses / slug
        if status != 200:
            print(f"oyc failed {status} {slug}")
            rows.append({"course_id": f"oyc-{slug}", "course_slug": slug, "course_url": course_url, "extraction_status": "failed"})
            continue
        fields = labeled_values(page)
        h1 = mit.find_all(mit.parse_html(page).root, "h1")
        title = mit.clean_text(h1[0]) if h1 else fields.get("Course Title") or slug
        code = fields.get("Course Number") or slug
        department = urlparse(final_url).path.strip("/").split("/")[0].replace("-", " ")
        license_href = license_url(page)
        home = content_node(oyc_home_markup(page), ("region-content",))
        home_body = render_node(home, final_url)
        sessions = oyc_sessions(page, final_url)
        resources = []
        directory.mkdir(parents=True, exist_ok=True)
        if len(re.sub(r"\s+", "", home_body)) >= 80:
            digest = write_course_page(
                directory,
                "course-description.md",
                summary_for(
                    f"{code} {title}",
                    "Open Yale Courses",
                    home_body,
                    gist_from_file(directory / "course-description.md"),
                ),
                final_url,
                home_body,
                license_href,
            )
            resources.append({
                "resource_type": "course_home",
                "title": title,
                "source_url": final_url,
                "source_format": "html",
                "extraction_policy": "full_text",
                "extraction_status": "complete",
                "local_path": "course-description.md",
                "content_sha256": digest,
            })
            resources.extend(binary_rows(home, final_url, title))
        session_ok = 0
        session_partial = 0
        for session_url, session_title in sessions:
            s_status, s_final, s_page = fetch_text(session_url)
            filename = slug_from_url(s_final) + ".md"
            if s_status != 200:
                resources.append({
                    "resource_type": "session",
                    "title": session_title,
                    "source_url": session_url,
                    "source_format": "html",
                    "extraction_policy": "full_text",
                    "extraction_status": "failed",
                    "local_path": None,
                    "content_sha256": None,
                    "error": f"HTTP {s_status}",
                })
                session_partial += 1
                continue
            node = content_node(s_page, ("region-content",))
            body = render_node(node, s_final)
            if len(re.sub(r"\s+", "", body)) < 80:
                resources.append({
                    "resource_type": "session",
                    "title": session_title,
                    "source_url": s_final,
                    "source_format": "html",
                    "extraction_policy": "full_text",
                    "extraction_status": "partial",
                    "local_path": None,
                    "content_sha256": None,
                    "error": "extracted text was too short",
                })
                session_partial += 1
                continue
            digest = write_course_page(
                directory,
                filename,
                summary_for(
                    f"{code} {session_title}",
                    "Open Yale Courses",
                    body,
                    gist_from_file(directory / filename),
                ),
                s_final,
                body,
                license_url(s_page) or license_href,
            )
            resources.append({
                "resource_type": "session",
                "title": session_title,
                "source_url": s_final,
                "source_format": "html",
                "extraction_policy": "full_text",
                "extraction_status": "complete",
                "local_path": filename,
                "content_sha256": digest,
            })
            resources.extend(binary_rows(node, s_final, session_title))
            session_ok += 1
        status_name = "complete" if session_partial == 0 and resources else "partial"
        record = {
            "schema_version": "1.0",
            "course_id": f"oyc-{slug}",
            "institution": "Yale University",
            "platform": "Open Yale Courses",
            "course_codes": [code] if code else [],
            "course_title": title,
            "course_slug": slug,
            "department_path": department,
            "professors": [fields["Professor"]] if fields.get("Professor") else [],
            "course_url": final_url,
            "language": "en",
            "description": fields.get("About the Course") or "",
            "license_url": license_href,
            "session_count": len(sessions),
            "topic_keywords": [],
            "pedagogy_tags": [],
            "assessment_types": [],
            "capture_date": CAPTURE_DATE,
            "extraction_status": status_name,
            "metadata_origin": {},
        }
        if code:
            record["metadata_origin"]["course_codes"] = "source"
        if fields.get("Professor"):
            record["metadata_origin"]["professors"] = "source"
        if fields.get("About the Course"):
            record["metadata_origin"]["description"] = "source"
        record["metadata_origin"]["department_path"] = "source"
        (directory / "course.yaml").write_text(mit.to_yaml(record) + "\n", encoding="utf-8")
        (directory / "resources.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in resources),
            encoding="utf-8",
        )
        rows.append({
            "course_id": record["course_id"],
            "course_title": title,
            "course_slug": slug,
            "course_url": final_url,
            "session_count": len(sessions),
            "sessions_saved": session_ok,
            "extraction_status": status_name,
        })
        print(f"oyc {status_name} {slug} sessions {session_ok}/{len(sessions)}")
    write_catalog(school / "catalog.jsonl", rows)
    return rows


def yale_poorvu() -> tuple[list[dict], list[str]]:
    school = OTHER / "Yale" / "poorvu"
    cases = school / "cases"
    status, _, page = fetch_text("https://poorvucenter.yale.edu/sitemap.xml")
    if status != 200:
        raise RuntimeError(f"Poorvu sitemap HTTP {status}")
    posts = sorted(set(re.findall(r"https?://poorvucenter\.yale\.edu/posts/[^<\s]+", page)))
    rows = []
    skipped = []
    for url in posts:
        url = url.replace("http://", "https://")
        slug = slug_from_url(url)
        if not any(token in slug for token in POORVU_KEEP):
            skipped.append(url)
            continue
        status, final_url, page = fetch_text(url)
        record = case_record(
            case_id=f"poorvu-{slug}",
            institution="Yale University",
            platform="Poorvu Center for Teaching and Learning",
            collection="Poorvu Center teaching stories",
            title=slug,
            slug=slug,
            source_url=final_url,
            license_url=license_url(page) if status == 200 else "",
        )
        if status == 200:
            h1 = mit.find_all(mit.parse_html(page).root, "h1")
            if h1:
                record["title"] = mit.clean_text(h1[0]) or slug
            state = save_article(cases / slug, record, page, ("field--name-body", "entry-content", "region-content"))
            record["extraction_status"] = "complete" if state != "partial" else "partial"
        else:
            state = "failed"
            record["extraction_status"] = "failed"
            (cases / slug).mkdir(parents=True, exist_ok=True)
            ((cases / slug) / "case.yaml").write_text(mit.to_yaml(record) + "\n", encoding="utf-8")
        rows.append(catalog_case(record))
        print(f"poorvu {state} {slug}")
    write_catalog(school / "catalog.jsonl", rows)
    (school / "skipped_news.txt").write_text("\n".join(skipped) + "\n", encoding="utf-8")
    return rows, skipped


def main():
    parser = argparse.ArgumentParser(description="Save source text for teaching_cases/other")
    parser.add_argument("--only", choices=["cornell", "columbia", "michigan", "oyc", "poorvu"])
    parser.add_argument("--rate", type=float, default=4)
    args = parser.parse_args()
    global LIMITER
    LIMITER = mit.Limiter(args.rate)
    selected = {args.only} if args.only else {"cornell", "columbia", "michigan", "oyc", "poorvu"}
    if "cornell" in selected:
        cornell()
    if "columbia" in selected:
        columbia()
    if "michigan" in selected:
        michigan()
    if "poorvu" in selected:
        yale_poorvu()
        remove_old_rewrites(OTHER / "Yale")
    if "oyc" in selected:
        yale_oyc()
        remove_old_rewrites(OTHER / "Yale")


if __name__ == "__main__":
    main()
