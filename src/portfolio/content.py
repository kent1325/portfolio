from datetime import date
from pathlib import Path
from re import compile
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

SLUG_PATTERN = compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ProfileLinks(BaseModel):
    model_config = ConfigDict(extra="forbid")

    linkedin: str
    github: str

    @field_validator("github")
    @classmethod
    def github_must_be_valid(cls, value: str) -> str:
        value = value.strip()
        rule: str = "https://github.com/"
        if not value.startswith(rule):
            raise ValueError(f"The 'github' profile field must start with {rule} but was '{value}'")
        return value

    @field_validator("linkedin")
    @classmethod
    def linkedin_must_be_valid(cls, value: str) -> str:
        value = value.strip()
        rule: str = "https://www.linkedin.com/in/"
        if not value.startswith(rule):
            raise ValueError(
                f"The 'linkedin' profile field must start with {rule} but was '{value}'"
            )
        return value


class Profile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    avatar: str
    hero_lines: list[str]
    links: ProfileLinks

    @field_validator("name")
    @classmethod
    def name_must_exist(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("The 'name' profile field must not be empty")
        return value

    @field_validator("avatar")
    @classmethod
    def avatar_must_be_asset_path(cls, value: str) -> str:
        value = value.strip()
        rule: str = "/assets/"
        if not value.startswith(rule):
            raise ValueError(f"The 'avatar' profile field must start with {rule} but was '{value}'")
        if ".." in value:
            raise ValueError("avatar must not contain '..'")
        return value

    @field_validator("hero_lines")
    @classmethod
    def hero_lines_must_be_valid(cls, value: list[str]) -> list[str]:
        value_cleaned = [line.strip() for line in value]
        if not value_cleaned:
            raise ValueError("The 'hero_lines' profile field must contain at least one item")
        for index, line in enumerate(value_cleaned):
            if not line:
                raise ValueError(f"The 'hero_lines[{index}]' must not be empty")
        return value_cleaned


class BlogPost(BaseModel):
    model_config = ConfigDict(extra="forbid")

    slug: str
    title: str
    status: Literal["published", "draft"]
    summary: str | None = None
    published_date: date | None = None
    updated_date: date | None = None
    body: str

    @field_validator("status")
    @classmethod
    def status_must_be_valid(cls, value: str) -> str:
        if value not in {"published", "draft"}:
            raise ValueError(f"Blog post status must be 'published' or 'draft', but got '{value}'")
        return value

    @model_validator(mode="after")
    def published_posts_must_have_required_fields(self) -> BlogPost:
        if self.status == "published":
            if self.summary is None:
                raise ValueError("Published blog posts must have a summary")
            if self.published_date is None:
                raise ValueError("Published blog posts must have a published_date")
        return self

    @field_validator("slug")
    @classmethod
    def slug_must_be_lowercase_kebab_case(cls, value: str) -> str:
        if not SLUG_PATTERN.fullmatch(value):
            raise ValueError(f"Blog post slug must be lowercase kebab-case, but got '{value}'")
        return value

    @model_validator(mode="after")
    def updated_date_must_be_at_or_later_than_published_date(self) -> BlogPost:
        if self.published_date is not None and self.updated_date is not None:
            if self.updated_date < self.published_date:
                raise ValueError("Updated date cannot be earlier than the published date")
        return self


def load_profile(root_path: Path) -> Profile:
    yaml_file_path: Path = root_path / "content" / "profile.yaml"
    raw_profile: dict[str, Any]
    if not yaml_file_path.is_file():
        raise FileNotFoundError(f"YAML file not found: {yaml_file_path}")

    with yaml_file_path.open("r", encoding="utf-8") as f:
        raw_profile = yaml.safe_load(f)

    if raw_profile is None:
        raise ValueError(f"YAML file is empty: {yaml_file_path}")

    if not isinstance(raw_profile, dict):
        raise ValueError(f"YAML root must be a mapping/object: {yaml_file_path}")

    profile: Profile = Profile.model_validate(raw_profile)
    _validate_avatar_exists(root_path, profile.avatar)
    return profile


def load_blog_posts(root_path: Path) -> list[BlogPost]:
    blog_dir: Path = root_path / "content" / "blog"
    if not blog_dir.exists():
        return []

    posts: list[BlogPost] = []
    for blog_file_path in sorted(blog_dir.glob("*.md")):
        raw_text = blog_file_path.read_text(encoding="utf-8")
        frontmatter, body = _split_markdown_frontmatter(raw_text, blog_file_path)
        post = BlogPost.model_validate(
            {**frontmatter, "slug": blog_file_path.stem, "body": body.strip()}
        )
        if post.status == "published":
            posts.append(post)

    return posts


def _split_markdown_frontmatter(raw_text: str, file_path: Path) -> tuple[dict[str, Any], str]:
    if not raw_text.startswith("---"):
        raise ValueError(f"Blog post is missing YAML frontmatter: {file_path}")

    parts: list = raw_text.split("---", maxsplit=2)
    if len(parts) != 3:
        raise ValueError(f"Blog post has invalid YAML frontmatter: {file_path}")

    raw_frontmatter: dict = yaml.safe_load(parts[1])
    if not isinstance(raw_frontmatter, dict):
        raise ValueError(f"Blog post frontmatter must be a mapping/object: {file_path}")

    return raw_frontmatter, parts[2]


def _validate_avatar_exists(root_path: Path, avatar_path: str) -> None:
    path: Path = root_path / avatar_path.removeprefix("/")
    if not path.is_file():
        raise FileNotFoundError(
            f"Avatar file not found: {path} from profile avatar path: {avatar_path}"
        )
