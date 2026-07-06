from pathlib import Path
from textwrap import dedent

from pytest import raises

from portfolio.content import Paper, load_papers


def _write_paper_pdf(root_path: Path, pdf_path: str) -> None:
    path = root_path / pdf_path.removeprefix("/")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"placeholder pdf bytes")


def _write_papers_yaml(root_path: Path, content: str) -> None:
    content_dir = root_path / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    (content_dir / "papers.yaml").write_text(dedent(content), encoding="utf-8")


def test_load_papers_loads_valid_papers_newest_first(tmp_path: Path) -> None:
    _write_paper_pdf(tmp_path, "/assets/papers/older-paper.pdf")
    _write_paper_pdf(tmp_path, "/assets/papers/newer-paper.pdf")
    _write_papers_yaml(
        tmp_path,
        """\
        - title: " Older Paper "
          year: 2024
          summary: "An older paper."
          tags:
            - machine-learning
          links:
            pdf: "/assets/papers/older-paper.pdf"

        - title: "Newer Paper"
          year: "2025"
          summary: " A newer paper. "
          type: "University paper"
          institution: "Example University"
          links:
            pdf: "/assets/papers/newer-paper.pdf"
            external: "https://example.com/newer-paper"
            github: "https://github.com/example/newer-paper"
        """,
    )

    papers: list[Paper] = load_papers(tmp_path)

    assert [paper.title for paper in papers] == ["Newer Paper", "Older Paper"]
    assert papers[0].year == 2025
    assert papers[0].summary == "A newer paper."
    assert papers[0].type == "University paper"
    assert papers[0].institution == "Example University"
    assert papers[0].links.pdf == "/assets/papers/newer-paper.pdf"
    assert papers[0].links.external == "https://example.com/newer-paper"
    assert papers[0].links.github == "https://github.com/example/newer-paper"
    assert papers[1].tags == ["machine-learning"]


def test_load_papers_returns_empty_list_when_file_is_missing(tmp_path: Path) -> None:
    assert load_papers(tmp_path) == []


def test_load_papers_returns_empty_list_when_file_is_empty(tmp_path: Path) -> None:
    _write_papers_yaml(tmp_path, "")

    assert load_papers(tmp_path) == []


def test_load_papers_rejects_non_list_yaml_root(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        title: "Not a list"
        year: 2025
        summary: "Nope."
        links:
          external: "https://example.com/paper"
        """,
    )

    with raises(ValueError, match="YAML root must be a list"):
        load_papers(tmp_path)


def test_load_papers_rejects_non_object_entries(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        - "not an object"
        """,
    )

    with raises(ValueError, match="Every paper entry must be a mapping/object"):
        load_papers(tmp_path)


def test_load_papers_rejects_bad_year(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        - title: "Bad Year"
          year: "twenty twenty-five"
          summary: "Nope."
          links:
            external: "https://example.com/paper"
        """,
    )

    with raises(ValueError, match="year must be a four-digit year"):
        load_papers(tmp_path)


def test_load_papers_rejects_bad_tag(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        - title: "Bad Tag"
          year: 2025
          summary: "Nope."
          tags:
            - Machine Learning
          links:
            external: "https://example.com/paper"
        """,
    )

    with raises(ValueError, match="tag must be lowercase kebab-case"):
        load_papers(tmp_path)


def test_load_papers_rejects_bad_pdf_path(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        - title: "Bad PDF"
          year: 2025
          summary: "Nope."
          links:
            pdf: "https://example.com/paper.pdf"
        """,
    )

    with raises(ValueError, match="pdf must start with /assets/"):
        load_papers(tmp_path)


def test_load_papers_rejects_non_pdf_artifact_path(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        - title: "Image Artifact"
          year: 2025
          summary: "Nope."
          links:
            pdf: "/assets/papers/paper.jpg"
        """,
    )

    with raises(ValueError, match="pdf must be a PDF asset"):
        load_papers(tmp_path)


def test_load_papers_rejects_missing_pdf_file(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        - title: "Missing PDF"
          year: 2025
          summary: "Nope."
          links:
            pdf: "/assets/papers/missing.pdf"
        """,
    )

    with raises(FileNotFoundError, match="Paper PDF file not found"):
        load_papers(tmp_path)


def test_load_papers_rejects_bad_external_url(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        - title: "Bad External"
          year: 2025
          summary: "Nope."
          links:
            external: "example.com/paper"
        """,
    )

    with raises(ValueError, match="external must start with http:// or https://"):
        load_papers(tmp_path)


def test_load_papers_rejects_bad_github_url(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        - title: "Bad GitHub"
          year: 2025
          summary: "Nope."
          links:
            external: "https://example.com/paper"
            github: "https://example.com/code"
        """,
    )

    with raises(ValueError, match="github must start with https://github.com/"):
        load_papers(tmp_path)


def test_load_papers_rejects_missing_artifact_link(tmp_path: Path) -> None:
    _write_papers_yaml(
        tmp_path,
        """\
        - title: "Code Only"
          year: 2025
          summary: "Nope."
          links:
            github: "https://github.com/example/code-only"
        """,
    )

    with raises(ValueError, match="at least one artifact link"):
        load_papers(tmp_path)
