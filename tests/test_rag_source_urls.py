from pathlib import Path

from ai_engine.rag.loaders import iter_documents, source_url_for_document


def test_html_prefers_canonical_url(tmp_path: Path):
    page = tmp_path / "course.html"
    page.write_text(
        '<html><head><link rel="canonical" href="https://example.edu/course" /></head>'
        "<body><main>Course content</main></body></html>",
        encoding="utf-8",
    )

    assert source_url_for_document(page, tmp_path) == "https://example.edu/course"


def test_marked_source_url_is_extracted(tmp_path: Path):
    page = tmp_path / "case.md"
    text = "# Case\n\n原始URL：https://example.edu/case\n"
    page.write_text(text, encoding="utf-8")

    assert source_url_for_document(page, tmp_path, text) == "https://example.edu/case"


def test_markdown_bold_source_url_is_extracted(tmp_path: Path):
    page = tmp_path / "case.md"
    text = "# Case\n\n**来源**：https://example.edu/case（访问 2026-10-02）\n"
    page.write_text(text, encoding="utf-8")

    assert source_url_for_document(page, tmp_path, text) == "https://example.edu/case"


def test_readme_manifest_maps_local_file(tmp_path: Path):
    page = tmp_path / "University" / "course.html"
    page.parent.mkdir()
    page.write_text("<html><body>Course content</body></html>", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "| **本地文件** | `University/course.html` |\n"
        "| **原始 URL** | https://example.edu/syllabus/ |\n",
        encoding="utf-8",
    )

    assert source_url_for_document(page, tmp_path) == "https://example.edu/syllabus/"


def test_archive_source_directory_is_not_ingested(tmp_path: Path):
    archive = tmp_path / "source"
    archive.mkdir()
    (archive / "snapshot.html").write_text(
        "<html><body>Archived duplicate</body></html>", encoding="utf-8"
    )
    article = tmp_path / "article.md"
    article.write_text("Searchable article", encoding="utf-8")

    paths = [path.relative_to(tmp_path).as_posix() for path, _ in iter_documents(tmp_path)]
    assert paths == ["article.md"]
