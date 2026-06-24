from datetime import date
from pathlib import Path
from textwrap import dedent

from pytest import raises

from portfolio.content import BlogPost, load_blog_posts


def test_load_blog_posts_returns_only_published_posts(tmp_path: Path) -> None:
    blog_dir: Path = tmp_path / "content" / "blog"
    blog_dir.mkdir(parents=True)

    (blog_dir / "hello-world.md").write_text(
        dedent(
            """\
            ---
            title: Hello World
            status: published
            summary: First post.
            published_date: 2026-06-10
            updated_date: 2026-06-11
            ---

            # Hello World

            Published body.
            """,
        ),
        encoding="utf-8",
    )

    (blog_dir / "draft-idea.md").write_text(
        dedent(
            """\
            ---
            title: Draft Idea
            status: draft
            ---

            # Draft Idea

            Draft body.
            """,
        ),
        encoding="utf-8",
    )

    posts: list[BlogPost] = load_blog_posts(tmp_path)

    assert len(posts) == 1

    post = posts[0]
    assert post.slug == "hello-world"
    assert post.title == "Hello World"
    assert post.status == "published"
    assert post.summary == "First post."
    assert post.published_date == date(2026, 6, 10)
    assert post.updated_date == date(2026, 6, 11)
    assert post.body.strip() == "# Hello World\n\nPublished body."


def test_load_blog_bad_naming_convention(tmp_path: Path) -> None:
    blog_dir: Path = tmp_path / "content" / "blog"
    blog_dir.mkdir(parents=True)

    (blog_dir / "Bad_Name.md").write_text(
        dedent(
            """\
            ---
            title: Bad Name
            status: published
            summary: First bad post.
            published_date: 2026-06-10
            ---

            # Bad Name

            Published body.
            """,
        ),
        encoding="utf-8",
    )

    with raises(ValueError):
        load_blog_posts(tmp_path)


def test_load_blog_incorrect_updated_date(tmp_path: Path) -> None:
    blog_dir: Path = tmp_path / "content" / "blog"
    blog_dir.mkdir(parents=True)

    (blog_dir / "hello-world.md").write_text(
        dedent(
            """\
            ---
            title: Hello World
            status: published
            summary: First post.
            published_date: 2026-06-10
            updated_date: 2026-06-09
            ---

            # Hello World

            Published body.
            """,
        ),
        encoding="utf-8",
    )

    with raises(ValueError):
        load_blog_posts(tmp_path)
