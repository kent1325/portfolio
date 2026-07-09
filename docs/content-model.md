# Content Model

## Overview

Use Markdown for long-form writing and YAML for structured homepage content.

```text
content/
  blog/          Flat Markdown blog source; no nested folders in v1
  profile.yaml   Basic identity and hero links
  skills.yaml    Technology marquee source content
  papers.yaml    Formal paper summaries
  books.yaml     Bookshelf entries
  certificates.yaml
  events.yaml
```

Schemas are strict: unknown YAML/frontmatter fields fail validation. Content tags are optional lowercase kebab-case strings such as `machine-learning` or `data-systems`.

## Paths and URLs

Internal URLs are root-relative and use pretty directory-style page paths:

```text
/                         → dist/index.html
/blog/                    → dist/blog/index.html
/blog/my-post/            → dist/blog/my-post/index.html
/assets/images/profile.jpg
```

Local asset references must:

- start with `/assets/`
- not contain `..`
- resolve inside the local `assets/` directory

The full `assets/` tree is copied into the generated site, including unreferenced files. Declared local asset references must exist.

Markdown images must use local asset references. Markdown links that start with `/` must resolve to a generated page or bundled asset. External links are allowed, but v1 does not check reachability.

## Profile

`content/profile.yaml` contains only minimal website-specific identity data.

```yaml
name: "Your Name"
avatar: "/assets/images/profile.jpg"

hero_lines:
  - "I do data science."
  - "I do machine learning."
  - "I do AI."

hero_logos:
  - Python
  - PyTorch
  - SQL
  - Hugging Face

links:
  github: "https://github.com/username"
  linkedin: "https://www.linkedin.com/in/username"
```

Required fields:

- `name`
- `avatar`
- `hero_lines` with at least one line
- `links.github`
- `links.linkedin`

Rules:

- All hero lines must render into HTML source; the first hero line must be visible without JavaScript.
- Carousel/typewriter behavior is progressive enhancement over the rendered hero lines.
- Optional hero logos are selected by Technology Tag name from the technology marquee source.
- Hero logo selections must reference known Technology Tags with local SVG icons.
- Hero logos are decorative but curated core technical associations, not proficiency ratings.
- Hero logo motion is CSS-only with explicit designed positions.
- Hero profile links are limited to GitHub and LinkedIn in v1.
- GitHub and LinkedIn links must match their expected public profile URL shape.
- No public email, CV link, contact CTA, or extra social/profile links in v1.

## Blog Posts

Blog posts live directly in `content/blog/*.md`. Nested folders are invalid in v1.

Each post URL is derived from the filename stem:

```text
content/blog/my-post.md → /blog/my-post/
```

Post slugs must be lowercase kebab-case. There is no frontmatter `slug` field in v1.

Recommended published post frontmatter:

```md
---
title: "My Blog Post"
published_date: "2026-05-03"
updated_date: "2026-05-10"
summary: "Short preview shown on cards."
tags: ["python", "machine-learning"]
status: "published"
links:
  github: "https://github.com/username/project"
  demo: "https://example.com"
---

Body content starts here.
```

Required for every blog file:

- `title`
- `status`: `published` or `draft`

Required for `status: published`:

- `published_date`
- `summary`

Optional for published posts:

- `updated_date` — must not be earlier than `published_date`
- `tags` — lowercase kebab-case
- `links.github`
- `links.demo`

Draft behavior:

- Draft posts are excluded from generated output.
- Draft posts may omit `summary`, `published_date`, and `updated_date`.
- Draft post filenames must still produce valid slugs.

Publication behavior:

- `status: published` controls whether a post appears.
- Future `published_date` values do not schedule or hide posts in v1.
- Blog index at `/blog/` is always generated, even with zero published posts.
- Homepage shows the five latest published posts when any exist.
- Homepage blog cards link to `/blog/<slug>/` using a stretched title link, making the full card target clickable without changing the canonical post route.
- Duplicate titles are allowed; slugs are the unique post identity.
- No series metadata or tag filtering/pages in v1.

Project writeups are normal blog posts with optional `links.github` and/or `links.demo`. Unusual links belong in the Markdown body.

Markdown should support:

- headings
- links
- local images
- fenced code blocks with language names
- tables
- blockquotes
- footnotes
- task lists

Markdown should not allow raw HTML in v1. Raw HTML should be disabled or escaped so posts use supported Markdown features and local assets instead of arbitrary embeds/scripts.

## Technology Marquee

The former “skills” content is treated as technology tags: technologies, tools, or domains associated with the owner’s interests or experience without implying proficiency level.

`content/skills.yaml` may keep row labels for source organization, but labels are not visible page headings in v1.

```yaml
rows:
  - label: "Languages & backend"
    items:
      - name: Python
        icon: "/assets/icons/python.svg"
      - name: SQL
      - name: FastAPI
        icon: "/assets/icons/fastapi.svg"

  - label: "Data science & ML"
    items:
      - name: PyTorch
        icon: "/assets/icons/pytorch.svg"
      - name: pandas
```

Rules:

- `rows` required
- row `label` required for source organization
- item `name` required
- item `icon` optional
- if present, `icon` must be a local SVG asset reference
- no remote icon CDNs
- no proficiency levels in v1

## Papers

`content/papers.yaml` contains formal academic or research papers only. Informal experiments, notebooks, and project explanations belong in blog posts/project writeups instead.

```yaml
- title: "Forecasting Electricity Demand with Machine Learning"
  year: 2025
  type: "University paper"
  institution: "Your University"
  summary: "Short public-facing explanation of the problem, method, and result."
  tags:
    - machine-learning
    - forecasting
  links:
    pdf: "/assets/papers/electricity-demand.pdf"
    external: "https://university.example/papers/electricity-demand"
    github: "https://github.com/username/repo"
```

Required fields:

- `title`
- `year`
- `summary`
- at least one paper artifact link: `links.pdf` or `links.external`

Optional fields:

- `type`
- `institution`
- `tags`
- `links.github`

Rules:

- `links.pdf` must be a local asset reference.
- `links.external` must be an `http://` or `https://` URL and should point to a formal paper page.
- `links.github` must start with `https://github.com/`, may support the paper, and does not satisfy the artifact requirement.
- Papers are shown on the homepage in v1.
- Paper cards choose a primary stretched-card link in this priority order: `links.pdf`, then `links.external`, then `links.github`.
- Paper cards may also show explicit secondary links for PDF, paper page, and code; those links remain independently clickable.
- Papers are sorted by `year` descending, preserving source order for papers with the same year.
- No separate `/papers/` archive page in v1.

## Bookshelf

`content/books.yaml` contains books the owner has read or is currently reading. It is not a reading queue and does not contain reflections.

```yaml
- title: "Designing Data-Intensive Applications"
  author: "Martin Kleppmann"
  status: "read"
  tags:
    - systems
    - databases

- title: "Hands-On Machine Learning"
  author: "Aurélien Géron"
  status: "reading"
  tags:
    - machine-learning
```

Required fields:

- `title`
- `author`
- `status`: `read` or `reading`

Optional fields:

- `tags`

Rules:

- `want_to_read` is not supported in v1.
- `summary`, `reflection`, and `year_read` are not supported in v1.
- If the owner wants to share thoughts about a book, publish a blog post.
- Books are shown on the homepage in v1 as compact, non-clickable bookshelf cards.
- Book cards do not link out to stores, Goodreads, summaries, or reflections in v1.
- No separate `/books/` archive page in v1.

## Certificates

`content/certificates.yaml` contains completed certificates with downloadable PDF artifacts.

```yaml
- title: "Machine Learning Specialization"
  issuer: "DeepLearning.AI"
  issued_date: "2025-04-18"
  tags:
    - machine-learning
  links:
    pdf: "/assets/certificates/machine-learning-specialization.pdf"
```

Required fields:

- `title`
- `issuer`
- `issued_date`
- `links.pdf`

`issued_date` may use `YYYY`, `YYYY-MM`, or `YYYY-MM-DD` precision.

Optional fields:

- `tags`

Rules:

- `tags` use the same lowercase kebab-case content tag format as other site content.
- `links.pdf` must be a local PDF asset reference.
- PDF validation requires a `/assets/` path, no `..`, an existing file, and a `.pdf` suffix; v1 does not inspect file headers.
- Recommended certificate PDF location is `/assets/certificates/`, but v1 only requires a local PDF under `/assets/`.
- All certificates are shown on the homepage in v1.
- Certificates are sorted by `issued_date` descending.
- For sorting, partial certificate dates use the last possible missing value: `YYYY` behaves like `YYYY-12-31`, and `YYYY-MM` behaves like the last day of that month.
- Missing or empty certificate content hides the section.
- No separate `/certificates/` archive page in v1.

## Events

`content/events.yaml` contains events the owner has participated in, such as AI conferences, Python conferences, and Pi Day.

```yaml
- name: "PyCon Denmark"
  role: "attendee"
  date: "2025-04"
  location: "Copenhagen, Denmark"
  tags:
    - python
  links:
    homepage: "https://example.com/pycon-denmark"
    pdf: "/assets/events/pycon-denmark-attendance.pdf"
```

Required fields:

- `name`
- `role`: exactly one lowercase machine value: `attendee`, `speaker`, `organizer`, or `volunteer`
- `date`

Optional fields:

- `location` — free display text such as `Copenhagen, Denmark` or `Online`
- `tags`
- `links.homepage`
- `links.pdf`

Rules:

- `tags` use the same lowercase kebab-case content tag format as other site content.
- `date` may use `YYYY`, `YYYY-MM`, or `YYYY-MM-DD` precision.
- `date` represents the event start date for multi-day events.
- If multiple roles apply to one event, choose one primary role for v1.
- Render role labels in human-friendly text such as `Attendee`, `Speaker`, `Organizer`, or `Volunteer`.
- `links.homepage` must be an `http://` or `https://` URL for the event homepage.
- `links.pdf` must be a local PDF asset reference for an event participation artifact, such as an attendance diploma.
- PDF validation requires a `/assets/` path, no `..`, an existing file, and a `.pdf` suffix; v1 does not inspect file headers.
- Recommended event PDF location is `/assets/events/`, but v1 only requires a local PDF under `/assets/`.
- All events are shown on the homepage in v1.
- If `links.pdf` exists, the whole event card links to the local participation artifact.
- If `links.pdf` is absent and `links.homepage` exists, only the event action link points to the homepage.
- Events are sorted by `date` descending.
- For sorting, partial event dates use the last possible missing value: `YYYY` behaves like `YYYY-12-31`, and `YYYY-MM` behaves like the last day of that month.
- Events represent participation, not a future event calendar.
- Missing or empty event content hides the section.
- No separate `/events/` archive page in v1.

## Homepage composition and routes

Generated routes in v1 are intentionally limited to:

```text
/              → dist/index.html
/blog/         → dist/blog/index.html
/blog/<slug>/  → dist/blog/<slug>/index.html
```

Papers, books, and events are homepage-only content sections in v1. Missing or empty optional homepage sections are hidden instead of showing placeholders.

The homepage template keeps Papers, Bookshelf, and Events in section partials:

```text
templates/_papers.html
templates/_bookshelf.html
templates/_events.html
```

These sections share the neutral homepage card base and section rhythm styles, with content-specific behavior layered on top: papers use stretched title links plus secondary links, bookshelf cards are non-clickable, and PDF-backed event cards are whole-card links.
