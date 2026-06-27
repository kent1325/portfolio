from pathlib import Path
from textwrap import dedent

from pytest import raises

from portfolio.content import load_technologies


def test_load_technologies_has_valid_casing(tmp_path: Path) -> None:
    content_dir: Path = tmp_path / "content"
    content_dir.mkdir(parents=True)
    icon_dir: Path = tmp_path / "assets" / "icons"
    icon_dir.mkdir(parents=True)
    (icon_dir / "python.svg").write_text("<svg></svg>", encoding="utf-8")

    (content_dir / "technologies.yaml").write_text(
        dedent(
            """\
            technologies:
                - tag: python
                  label: Python
                  icon: /assets/icons/python.svg
            """,
        ),
        encoding="utf-8",
    )

    technologies = load_technologies(tmp_path)
    technology = technologies[0]
    assert technology.tag == "python"
    assert technology.label == "Python"
    assert technology.icon == "/assets/icons/python.svg"


def test_load_technologies_requires_file(tmp_path: Path) -> None:
    content_dir: Path = tmp_path / "content"
    content_dir.mkdir(parents=True)

    with raises(FileNotFoundError):
        load_technologies(tmp_path)


def test_load_technologies_has_technologies(tmp_path: Path) -> None:
    content_dir: Path = tmp_path / "content"
    content_dir.mkdir(parents=True)

    (content_dir / "technologies.yaml").write_text(
        dedent(
            """\
            technologies: []
            """,
        ),
        encoding="utf-8",
    )

    with raises(ValueError, match="at least one"):
        load_technologies(tmp_path)


def test_load_technologies_rejects_bad_tag_casing(tmp_path: Path) -> None:
    content_dir: Path = tmp_path / "content"
    content_dir.mkdir(parents=True)

    (content_dir / "technologies.yaml").write_text(
        dedent(
            """\
            technologies:
                - tag: Data Science
                  label: Data Science
            """,
        ),
        encoding="utf-8",
    )

    with raises(ValueError, match="tag"):
        load_technologies(tmp_path)


def test_load_technologies_must_have_label_or_icon(tmp_path: Path) -> None:
    content_dir: Path = tmp_path / "content"
    content_dir.mkdir(parents=True)
    icon_dir: Path = tmp_path / "assets" / "icons"
    icon_dir.mkdir(parents=True)
    (icon_dir / "python.svg").write_text("<svg></svg>", encoding="utf-8")

    (content_dir / "technologies.yaml").write_text(
        dedent(
            """\
            technologies:
                - tag: python
                  icon: /assets/icons/python.svg
            """,
        ),
        encoding="utf-8",
    )

    technologies = load_technologies(tmp_path)
    technology = technologies[0]
    assert technology.label is None
    assert technology.icon == "/assets/icons/python.svg"


def test_load_technologies_reject_if_no_label_or_icon(tmp_path: Path) -> None:
    content_dir: Path = tmp_path / "content"
    content_dir.mkdir(parents=True)

    (content_dir / "technologies.yaml").write_text(
        dedent(
            """\
            technologies:
                - tag: python
            """,
        ),
        encoding="utf-8",
    )

    with raises(ValueError, match="label or icon"):
        load_technologies(tmp_path)
