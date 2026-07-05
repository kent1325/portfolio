import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .content import (
    BlogPost,
    Book,
    EventParticipation,
    Technology,
    get_hero_logo_technologies,
    load_blog_posts,
    load_books,
    load_events,
    load_profile,
    load_technologies,
)
from .markdown import render_markdown


def _get_project_root() -> Path:
    # Normalize and get the absolute path of the current script
    current_file: Path = Path(__file__).resolve()

    # Iterate through parent directories
    for parent in current_file.parents:
        # Check for a common root marker (e.g., .git, pyproject.toml, setup.py)
        if (parent / ".git").exists() or (parent / "pyproject.toml").exists():
            return parent.resolve()

    raise FileNotFoundError("Project root not found.")


ROOT_PATH = _get_project_root()
SITE_URL = "https://kvugs.github.io"
SOCIAL_IMAGE_PATH = "/assets/images/social-preview.png"


def _page_url(path: str) -> str:
    return f"{SITE_URL}{path}"


def _drop_dist_dir() -> None:
    dist_path: Path = (ROOT_PATH / "dist").resolve()
    if dist_path.parent != ROOT_PATH:
        raise RuntimeError(
            f"Expected parent of path to be at the root of the project, but got {dist_path}"
        )
    if dist_path.is_dir():
        shutil.rmtree(dist_path)
    elif dist_path.exists():
        raise RuntimeError(f"Expected path to be a folder, but got {dist_path}")


def _copy_assets() -> None:
    assets_path: Path = (ROOT_PATH / "assets").resolve()
    dist_assets_path: Path = (ROOT_PATH / "dist" / "assets").resolve()
    if dist_assets_path.parent != (ROOT_PATH / "dist").resolve():
        raise RuntimeError(f"Expected path to be root of project, but got {dist_assets_path}")

    if not assets_path.is_dir():
        raise FileNotFoundError(f"Assets directory not found: {assets_path}")

    if dist_assets_path.is_dir():
        shutil.rmtree(dist_assets_path)
    elif dist_assets_path.exists():
        raise RuntimeError(
            f"Expected dist/assets to be a directory, but found a non-directory: {dist_assets_path}"
        )

    shutil.copytree(assets_path, dist_assets_path)


def build_site() -> None:
    profile = load_profile(ROOT_PATH)

    template_dir = ROOT_PATH / "templates"
    environment = Environment(
        loader=FileSystemLoader(template_dir), autoescape=select_autoescape(["html", "xml"])
    )
    index_template = environment.get_template("index.html")
    blog_index_template = environment.get_template("blog_index.html")
    blog_post_template = environment.get_template("blog_post.html")

    blog_posts: list[BlogPost] = load_blog_posts(ROOT_PATH)
    technologies: list[Technology] = load_technologies(ROOT_PATH)
    latest_posts: list[BlogPost] = blog_posts[:4]
    hero_logo_technologies: list[Technology] = get_hero_logo_technologies(profile, technologies)
    books: list[Book] = load_books(ROOT_PATH)
    events: list[EventParticipation] = load_events(ROOT_PATH)
    site_name = profile.name
    home_description = (
        f"{site_name}'s portfolio with writing and projects focused on data science, "
        "machine learning, and engineering."
    )
    blog_index_description = (
        "Short notes, thoughts, and project posts focusing on data science and machine learning."
    )
    social_image_url = _page_url(SOCIAL_IMAGE_PATH)
    social_image_alt = f"{site_name} portfolio preview"

    index_html = index_template.render(
        profile=profile,
        technologies=technologies,
        latest_posts=latest_posts,
        hero_logo_technologies=hero_logo_technologies,
        books=books,
        events=events,
        site_name=site_name,
        page_title=site_name,
        page_description=home_description,
        page_url=_page_url("/"),
        page_type="website",
        page_image_url=social_image_url,
        page_image_alt=social_image_alt,
        include_hero_script=True,
    )
    blog_index_html = blog_index_template.render(
        posts=blog_posts,
        site_name=site_name,
        page_title=f"Posts | {site_name}",
        page_description=blog_index_description,
        page_url=_page_url("/blog/"),
        page_type="website",
        page_image_url=social_image_url,
        page_image_alt=social_image_alt,
    )

    _drop_dist_dir()

    index_html_out_path = ROOT_PATH / "dist" / "index.html"
    blog_index_html_out_path = ROOT_PATH / "dist" / "blog" / "index.html"
    for blog_post in blog_posts:
        blog_post_html = blog_post_template.render(
            post=blog_post,
            body_html=render_markdown(blog_post.body),
            site_name=site_name,
            page_title=f"{blog_post.title} | {site_name}",
            page_description=blog_post.summary,
            page_url=_page_url(f"/blog/{blog_post.slug}/"),
            page_type="article",
            page_image_url=social_image_url,
            page_image_alt=social_image_alt,
        )
        blog_post_html_out_path = ROOT_PATH / "dist" / "blog" / blog_post.slug / "index.html"
        blog_post_html_out_path.parent.mkdir(parents=True, exist_ok=True)
        blog_post_html_out_path.write_text(blog_post_html, encoding="utf-8")

    for path, html in [
        (index_html_out_path, index_html),
        (blog_index_html_out_path, blog_index_html),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")

    _copy_assets()


def main() -> None:
    build_site()


if __name__ == "__main__":
    main()
