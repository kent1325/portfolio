# PRD: Static Portfolio Website

## Problem Statement

The user wants a personal portfolio website hosted on GitHub Pages while keeping a Python-centered development workflow. The portfolio should signal competence and taste to technical hiring readers without becoming a duplicate CV or LinkedIn profile.

The site should provide lightweight publishing for Markdown blog posts, a polished hero, an unlabeled technology marquee, formal papers, a compact bookshelf, certificates with downloadable PDFs, and event participation cards. It should remain static, maintainable, deployable through GitHub Actions, and strict enough to catch broken content before publication.

The repository now contains the Python site compiler, source content, templates, styling, tests, and GitHub Pages deployment workflow.

## Primary Audience

Optimize first for the **technical hiring reader**: engineers, technical managers, and serious recruiters evaluating whether the owner is thoughtful, technical, and worth contacting.

## Solution

Build a custom Python site compiler that converts Markdown and YAML source content into static HTML/CSS/JS output. Style the site with Tailwind CSS, using npm only for Tailwind compilation. Use npm rather than pnpm in v1 to keep the required tooling minimal. Deploy the generated `dist/` artifact to a GitHub Pages user site through GitHub Actions. See [Tech Stack Rationale](./tech-stack-rationale.md) for the personal-skill-fit arguments and alternatives considered.

The site has no backend, database, CMS, server-side rendering runtime, FastAPI app, HTMX/Alpine AJAX-style fragment interaction layer, or frontend framework.

## Core Product Decisions

- Use a custom Python **site compiler**, not loose scripts or a framework site generator.
- Treat the **site compiler** as part of the portfolio's inspectable technical signal.
- Validate source content strictly before writing output.
- Use root-relative internal URLs and pretty directory-style page URLs.
- Generate deployment artifacts in CI; do not commit `dist/`.
- Pin GitHub Actions runtime versions, using Python `3.14` and Node `v26.0.0`.
- Commit `uv.lock` and `package-lock.json`; CI uses locked dependency installation and fails on missing or stale lockfiles.
- Use GitHub Pages user-site hosting at domain root in v1.
- Do not implement custom-domain/CNAME behavior in v1.
- Use system-preference dark mode in v1 with a lightweight manual theme override.
- Support reduced-motion preferences by disabling decorative animation and minimizing transition movement.
- Use CSS animations for decorative motion and small custom JavaScript for isolated behavior such as the hero carousel/typewriter.
- Do not use Alpine.js in v1; reconsider it later only if user-driven interactions grow beyond presentational animation.
- Do not use HTMX or Alpine AJAX in v1 because GitHub Pages has no backend fragment endpoints.
- Include pytest in v1 for fixture-based compiler/content behavior tests.
- Do not include mypy or pyright in v1; reconsider static type checking after the compiler shape stabilizes.

## Architecture Quality Principles

- **Maintainability**: model papers, books, certificates, and events as first-class content types because their domain rules differ; use Pydantic for centralized strict validation; keep compiler orchestration separate from content schemas, route inventory, asset validation, Markdown rendering, and templates.
- **Reliability**: validate before writing output; perform full clean builds; disable or escape raw Markdown HTML; gate deployment on the complete check/build; use committed lockfiles, pinned Python and Node runtimes, and smoke checks for generated HTML/CSS.
- **Scalability**: avoid v1 search, pagination, tag pages, caching, and incremental builds; the expected static output is small enough for full regeneration, while route/content boundaries remain ready for later pagination or archive pages.
- **Adaptability**: use root-relative URLs, pretty paths, source-based Tailwind scanning, shared base card styles, section partial templates, and scroll-based homepage composition so later navigation, archive pages, custom domains, or UX changes remain localized.

## Site Structure

### Pages

- Homepage `/`
- Blog index `/blog/`, always generated
- Blog post pages `/blog/<slug>/`

### Homepage order

1. Hero
2. Unlabeled technology marquee
3. Latest five published blog posts, if any
4. Formal papers, if any
5. Bookshelf, if any
6. Certificates, if any
7. Events, if any
8. Minimal footer

Empty homepage sections are hidden. Remaining sections keep the same relative order.

## Content Model

### Profile

Profile content includes only:

- name
- avatar local asset reference
- hero lines
- optional hero technology logo selections
- GitHub profile link
- LinkedIn profile link

Hero lines are required; all hero lines render into HTML source, the first line must be visible without JavaScript, and carousel/typewriter behavior is progressive enhancement. Optional hero technology logos are decorative but curated core technical associations selected from known technology tags with local SVG icons.

No public email, CV link, contact CTA, role/title line, or extra profile/social links in v1.

### Blog

Blog posts are flat Markdown files in `content/blog/*.md`; nested folders are invalid in v1.

Post identity:

- slug comes from the filename stem
- slug must be lowercase kebab-case
- no frontmatter slug in v1
- duplicate titles are allowed; duplicate slugs fail

Post states:

- `status: published` appears on the site
- `status: draft` is excluded from output
- publication is controlled by status, not date scheduling

Published posts require:

- `title`
- `status`
- `summary`
- `published_date`

Published posts may include:

- `updated_date`, not earlier than `published_date`
- lowercase kebab-case content tags
- typed links: `github`, `demo`

Draft posts require `title` and `status`, may omit publication fields, and must still have valid filename-derived slugs.

Project writeups are normal blog posts that explain informal experiments, technical projects, or implementations. They may use `github` and `demo` links. There is no separate project content type in v1.

No featured posts, series metadata, search, pagination, tag filtering, or tag pages in v1. The architecture should keep routing and content boundaries clear enough to add pagination later if content volume requires it.

### Technology marquee

The marquee shows **technology tags**, not proficiency claims. Items may represent expertise, experience, or current learning.

- No visible “Skills” section label in v1.
- No visible row labels in v1.
- Row labels may exist in YAML for source organization/accessibility.
- Technology icons are optional.
- If an icon is present, it must be a local SVG asset reference.
- No remote icon CDNs.
- No proficiency levels.
- Marquee animation is CSS-first using duplicated rendered items; JavaScript is reserved for fixing poor loop quality if real content requires it.

### Papers

The papers section contains formal academic or research documents only.

Each paper requires:

- title
- year
- public-facing summary
- at least one paper artifact: local PDF or formal external paper page

Optional supporting code links are allowed but do not satisfy the artifact requirement.

Informal research experiments, notebooks, and implementation reports belong in blog posts/project writeups.

All papers are shown on the homepage and sorted by year descending, preserving source order for papers with the same year.

No dedicated papers archive page in v1.

### Bookshelf

The bookshelf contains books the owner has read or is currently reading.

Each bookshelf entry requires:

- title
- author
- status: `read` or `reading`

Optional:

- lowercase kebab-case content tags

Unsupported in v1:

- `want_to_read`
- summaries
- reflections
- read dates

Book reflections should be blog posts, not bookshelf fields.

No dedicated books archive page in v1.

### Certificates

The certificates section contains completed credentials the owner wants to display with a downloadable certificate PDF.

Each certificate requires:

- title
- issuer
- issued date, using `YYYY`, `YYYY-MM`, or `YYYY-MM-DD` precision
- local PDF artifact under `/assets/`

Optional:

- lowercase kebab-case content tags

Certificate summaries are not supported in v1.

All certificates are shown on the homepage and sorted by issued date descending. For sorting, partial certificate dates use the last possible missing value: `YYYY` behaves like `YYYY-12-31`, and `YYYY-MM` behaves like the last day of that month.

Missing or empty certificate content hides the section.

No dedicated certificates archive page in v1.

### Events

The events section contains events the owner has participated in, such as AI conferences, Python conferences, and Pi Day.

Each event requires:

- name
- exactly one lowercase machine role: `attendee`, `speaker`, `organizer`, or `volunteer`, rendered as human-friendly display text
- date, using `YYYY`, `YYYY-MM`, or `YYYY-MM-DD` precision; for multi-day events, this is the start date

Optional:

- location as free display text
- lowercase kebab-case content tags
- event homepage link
- local PDF artifact under `/assets/` for event participation proof, such as an attendance diploma

All events are shown on the homepage and sorted by date descending. For sorting, partial event dates use the last possible missing value: `YYYY` behaves like `YYYY-12-31`, and `YYYY-MM` behaves like the last day of that month.

Events represent participation, not a future event calendar.

Missing or empty event content hides the section.

No dedicated events archive page in v1.

### Assets and Links

- Local asset references are public URL paths under `/assets/`.
- Declared local asset references must resolve inside the source `assets/` directory.
- The full `assets/` directory is copied to the generated site, including unreferenced files.
- Markdown images must be local asset references.
- Markdown links starting with `/` must resolve to generated pages or bundled assets.
- External links must be `http://` or `https://`; reachability is not checked in v1.
- GitHub and LinkedIn profile links must match expected provider URL shapes.

## User Stories

1. As the portfolio owner, I want to host the site on GitHub Pages, so that publishing is cheap and reliable.
2. As the portfolio owner, I want a Python site compiler, so that the implementation matches my preferred stack.
3. As the portfolio owner, I want strict content validation, so that broken source content does not deploy.
4. As the portfolio owner, I want Markdown blog posts, so that publishing writing is simple.
5. As the portfolio owner, I want draft posts, so that unfinished writing can live in the repository without appearing publicly.
6. As the portfolio owner, I want published and updated dates, so that readers can understand publication and freshness.
7. As the portfolio owner, I want filename-derived post slugs, so that URLs have one source of truth.
8. As the portfolio owner, I want a blog index and individual blog pages, so that writing is browsable.
9. As the portfolio owner, I want project writeups to be normal blog posts, so that v1 avoids a separate projects section.
10. As the portfolio owner, I want a polished hero with avatar, name, hero lines, GitHub, and LinkedIn, so that the first impression is personal and professional.
11. As a visitor without JavaScript, I want the first hero line to remain visible, so that the hero still communicates identity.
12. As the portfolio owner, I want an unlabeled technology marquee, so that I can show technical associations without implying proficiency levels.
13. As the portfolio owner, I want optional local SVG technology icons, so that recognizable technologies can have visual impact without requiring icons for all items.
14. As the portfolio owner, I want formal papers on the homepage, so that academic/research work is visible.
15. As a visitor, I want each paper to link to a public artifact, so that I can verify or access the paper.
16. As the portfolio owner, I want informal experiments to be blog posts, so that papers remain formal and the content model stays simple.
17. As the portfolio owner, I want a compact bookshelf without reflections, so that it signals interests without becoming a note-taking system.
18. As the portfolio owner, I want book reflections to be blog posts, so that substantial thoughts have proper space.
19. As a visitor, I want empty homepage sections hidden, so that the site does not feel unfinished.
20. As the portfolio owner, I want certificates with downloadable PDF links, so that visitors can verify completed credentials.
21. As the portfolio owner, I want an events section, so that visitors can see technical communities and events I participate in.
22. As the portfolio owner, I want root-relative internal URLs, so that the site is not tied to a specific hostname.
23. As the portfolio owner, I want GitHub Actions checks and deployment, so that pushes can be validated and published automatically.
24. As the portfolio owner, I want deployment gated on the full strict validation/build check, so that failed content or broken links never publish partially.
25. As the portfolio owner, I want uv, npm/Tailwind, just, Ruff, and pytest, so that local and CI workflows are reproducible, simple, and covered by behavior tests.

## Major Modules to Build

- **Site compiler entrypoint**: coordinates validation, rendering, asset copying, and output generation without owning content schemas, route inventory, or template internals.
- **Content loading and validation**: reads YAML/frontmatter, uses Pydantic models for strict schemas, validates post states, dates, tags, profile links, paper artifacts, certificate artifacts, event links/artifacts, and bookshelf entries.
- **Markdown rendering**: converts Markdown to HTML with technical-writing extensions and Pygments code highlighting, while disabling or escaping raw HTML.
- **Link and asset validation**: validates local asset references, Markdown images, and internal Markdown links.
- **Template rendering**: renders homepage, blog index, and blog post pages; homepage sections use separate partial templates composed by `index.html`.
- **Routing/output**: owns slug rules, pretty URLs, output paths, and generated page inventory as the source of truth for internal link validation.
- **Asset pipeline**: copies the full assets tree and ensures declared local assets exist.
- **Frontend behavior**: provides minimal hero carousel behavior.
- **Styling system**: Tailwind configuration, typography, dark mode, marquee styles, reusable component classes, a shared base card style with small content-specific variations, and source-based Tailwind content scanning that avoids relying on `dist/`.
- **CI/deployment**: check workflow and GitHub Pages deployment workflow, with deployment gated on the full strict validation/build check.
- **Local workflow commands**: install, build, serve, dev, check, and format via `just`.

## Testing Decisions

Tests should verify external behavior rather than implementation details. Prefer small fixture site directories over mocked filesystem/content loaders so tests exercise real YAML, Markdown, assets, route generation, and output paths.

Focus areas:

- strict schema validation and unknown-field rejection
- blog status rules and draft filtering
- published/updated date validation
- lowercase kebab-case slug validation
- flat blog source enforcement
- homepage empty-section behavior
- `/blog/` generation with zero posts
- Markdown rendering for technical-writing features
- raw HTML in Markdown is disabled or escaped
- Markdown local image validation
- Markdown internal link validation
- profile link provider-shape validation
- technology icon validation
- paper artifact requirement
- bookshelf status/field validation
- certificate PDF artifact validation by `/assets/` path, existence, and `.pdf` suffix
- event field validation
- event PDF artifact validation by `/assets/` path, existence, and `.pdf` suffix
- route/output generation for pretty URLs
- clean build behavior
- full fixture build generating homepage, blog index, post pages, and CSS output
- deployable artifact smoke checks for `dist/index.html`, `dist/blog/index.html`, and `dist/assets/styles.css`
- Pydantic schema validation behavior
- pytest fixture-based behavior tests in automated checks
- Ruff formatting/linting in automated checks

Avoid tests that assert private helper calls, parser internals, or exact template internals unless the behavior is user-visible.

## Out of Scope

- Backend runtime, server-side rendering at request time, database, or CMS.
- FastAPI app.
- Scraping LinkedIn or parsing CV PDFs.
- Public email, contact form, CV link/download, or contact CTA.
- Extra profile/social links beyond GitHub and LinkedIn.
- Global navigation bar or homepage anchor navigation.
- Separate projects section or project content type.
- Dedicated certificates archive page.
- Dedicated events archive page.
- Featured posts.
- Blog series support.
- Search, blog pagination, tag filtering, or tag pages.
- Dedicated books or papers archive pages.
- Book summaries/reflections in bookshelf data.
- Want-to-read bookshelf items.
- Alpine.js for v1 presentational animation.
- HTMX, Alpine AJAX, or server/fragment-driven interaction libraries.
- Heavy JS framework, canvas, WebGL, or 3D animation system.
- Raw HTML embeds in Markdown.
- Incremental builds or render caching.
- File-watching development server.
- Custom-domain/CNAME handling.
- External link reachability checking.
- Dependabot, pre-commit, accessibility checks, and Lighthouse in v1.

## Further Notes

Version 1 should prioritize a working deployed site with strict content validation and a clean content workflow. Visual polish can iterate after the generator, content model, and deployment pipeline are functional.

Recommended first implementation slice: deployment-first + generator tracer bullet. Build a minimal profile-driven homepage, compile Tailwind, and deploy through GitHub Actions before expanding the remaining content types.
