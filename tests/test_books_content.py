from pathlib import Path
from textwrap import dedent

from pytest import raises

from portfolio.content import Book, load_books


def _write_book_cover(root_path: Path, cover_path: str) -> None:
    path = root_path / cover_path.removeprefix("/")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"placeholder image bytes")


def _write_books_yaml(root_path: Path, content: str) -> None:
    content_dir = root_path / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    (content_dir / "books.yaml").write_text(dedent(content), encoding="utf-8")


def test_load_books_loads_valid_books_in_source_order(tmp_path: Path) -> None:
    _write_book_cover(tmp_path, "/assets/books/first-book.jpg")
    _write_book_cover(tmp_path, "/assets/books/second-book.webp")
    _write_books_yaml(
        tmp_path,
        """\
        - title: " First Book "
          author: "First Author"
          status: "reading"
          cover: "/assets/books/first-book.jpg"
          tags:
            - machine-learning
            - python

        - title: "Second Book"
          author: "Second Author"
          status: "read"
          cover: "/assets/books/second-book.webp"
        """,
    )

    books: list[Book] = load_books(tmp_path)

    assert [book.title for book in books] == ["First Book", "Second Book"]
    assert books[0].author == "First Author"
    assert books[0].status == "reading"
    assert books[0].cover == "/assets/books/first-book.jpg"
    assert books[0].tags == ["machine-learning", "python"]
    assert books[1].tags is None


def test_load_books_returns_empty_list_when_file_is_missing(tmp_path: Path) -> None:
    assert load_books(tmp_path) == []


def test_load_books_returns_empty_list_when_file_is_empty(tmp_path: Path) -> None:
    _write_books_yaml(tmp_path, "")

    assert load_books(tmp_path) == []


def test_load_books_rejects_non_list_yaml_root(tmp_path: Path) -> None:
    _write_books_yaml(
        tmp_path,
        """\
        title: "Not a list"
        author: "No One"
        status: "reading"
        cover: "/assets/books/not-a-list.jpg"
        """,
    )

    with raises(ValueError, match="YAML root must be a list"):
        load_books(tmp_path)


def test_load_books_rejects_bad_status(tmp_path: Path) -> None:
    _write_book_cover(tmp_path, "/assets/books/bad-status.jpg")
    _write_books_yaml(
        tmp_path,
        """\
        - title: "Bad Status"
          author: "Author"
          status: "want-to-read"
          cover: "/assets/books/bad-status.jpg"
        """,
    )

    with raises(ValueError, match="read|reading"):
        load_books(tmp_path)


def test_load_books_rejects_bad_tag(tmp_path: Path) -> None:
    _write_book_cover(tmp_path, "/assets/books/bad-tag.jpg")
    _write_books_yaml(
        tmp_path,
        """\
        - title: "Bad Tag"
          author: "Author"
          status: "reading"
          cover: "/assets/books/bad-tag.jpg"
          tags:
            - Machine Learning
        """,
    )

    with raises(ValueError, match="tag must be lowercase kebab-case"):
        load_books(tmp_path)


def test_load_books_rejects_non_asset_cover_path(tmp_path: Path) -> None:
    _write_books_yaml(
        tmp_path,
        """\
        - title: "Remote Cover"
          author: "Author"
          status: "reading"
          cover: "https://example.com/cover.jpg"
        """,
    )

    with raises(ValueError, match="cover must start with /assets/"):
        load_books(tmp_path)


def test_load_books_rejects_non_image_cover_path(tmp_path: Path) -> None:
    _write_books_yaml(
        tmp_path,
        """\
        - title: "PDF Cover"
          author: "Author"
          status: "reading"
          cover: "/assets/books/not-an-image.pdf"
        """,
    )

    with raises(ValueError, match="cover must be an image"):
        load_books(tmp_path)


def test_load_books_rejects_missing_cover_file(tmp_path: Path) -> None:
    _write_books_yaml(
        tmp_path,
        """\
        - title: "Missing Cover"
          author: "Author"
          status: "reading"
          cover: "/assets/books/missing-cover.jpg"
        """,
    )

    with raises(FileNotFoundError, match="Book cover file not found"):
        load_books(tmp_path)
