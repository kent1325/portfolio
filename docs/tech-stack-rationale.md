# Tech Stack Rationale

This document records why the v1 stack is shaped around the portfolio owner's strengths and why nearby alternatives were rejected or deferred.

## Guiding principle

Version 1 should showcase Python/backend/data engineering strengths first, with enough frontend polish to feel professional. The main technical signal is the custom Python site compiler, strict content validation, fixture-based tests, clean build pipeline, and reproducible deployment. Frontend tooling should support the visual design without becoming the center of gravity.

The intended balance is roughly 70% shipping and 30% stretch: use familiar Python-centered tools for the core and stretch through disciplined compiler architecture, validation, Tailwind styling, and CI/CD rather than by adopting a larger frontend stack.

## Accepted v1 stack

- Python site compiler
- Markdown for blog posts
- YAML for structured content
- Pydantic for strict schemas
- Jinja2 for templates
- Tailwind CSS and Tailwind Typography for styling/prose
- Pygments for code highlighting
- Small custom JavaScript for isolated timed behavior such as the hero carousel/typewriter
- CSS animations for decorative movement such as marquee rows and hero technology logos
- pytest for fixture-based behavior tests
- Ruff for formatting/linting
- uv for Python dependency management
- npm only for Tailwind compilation
- just as the canonical local command interface
- GitHub Actions and GitHub Pages for checked deployment

## Python compiler over site generator or frontend framework

Use a custom Python **Site Compiler** rather than MkDocs, Pelican, Astro, Next.js, SvelteKit, or loose scripts.

Reasons:

- The site is a custom portfolio, not a documentation site or frontend application.
- The owner is strongest in Python modeling/validation and content/writing, so the core implementation should live there.
- Strict content validation, route inventory, asset checks, link checks, clean builds, and fixture tests become part of the technical signal for readers who inspect the repository.
- A compiler-style build gives clearer boundaries than loose scripts and avoids stale generated output.

Trade-off: this takes more implementation work than using an off-the-shelf generator, but it better matches the desired portfolio signal and personal skill profile.

## Jinja2 over Python HTML builders

Keep Jinja2 templates.

Reasons:

- Jinja2 is boring, readable, and familiar to many Python/web readers.
- It separates rendering from compiler orchestration.
- Future readers can inspect page structure faster than with a custom Python HTML DSL.

## Tailwind over plain CSS

Keep Tailwind CSS.

Reasons:

- Tailwind helps achieve responsive layout, dark mode, cards, typography, and restrained visual polish without designing a full CSS architecture from scratch.
- Node/npm remains a small build-time dependency used only for Tailwind compilation.
- Tailwind supports the visual goal without turning the site into a frontend-heavy project.

Trade-off: Tailwind adds npm/Node, but the dependency surface is intentionally small and reproducible with `package-lock.json` and `npm ci`.

## Pydantic over manual validation

Keep Pydantic.

Reasons:

- The content model has many strict rules: unknown-field rejection, dates, local asset references, profile URL shapes, controlled statuses/roles, and artifact requirements.
- Centralized model validation is more maintainable than scattered manual checks.
- It aligns with Python strengths and makes compiler correctness more visible.

## pytest in v1

Add pytest from the start.

Reasons:

- The compiler's value depends on behavior that should be proven: schema validation, draft filtering, route generation, asset/link validation, clean builds, and smoke outputs.
- Fixture-based tests exercise real YAML, Markdown, assets, routes, and generated output paths.
- This reinforces the repository as a technical artifact rather than only a generated website.

## Static type checking deferred

Do not add mypy or pyright in v1.

Reasons:

- Pydantic, pytest, and Ruff cover the main risks for the first implementation.
- A type checker adds configuration and annotation overhead before the compiler shape is stable.
- It can be reconsidered after v1 if the Python code grows.

## uv, npm, and just

Use uv for Python dependency management because it gives a modern, reproducible Python workflow with a committed lockfile.

Use npm rather than pnpm because Node is only present to compile Tailwind. `npm ci` with a committed `package-lock.json` is enough for the small JavaScript dependency surface.

Use `just` as the canonical local workflow:

- `just install`
- `just check`
- `just build`
- `just serve`
- `just dev`
- `just format`

Underlying `uv` and `npm` commands may appear in CI and troubleshooting docs, but day-to-day development should not present competing workflows.

## GitHub Pages and Actions

Use GitHub Pages with GitHub Actions deployment.

Reasons:

- The site is static and does not need a server platform.
- It keeps hosting simple, free, and repository-centered.
- Automatic deployment on pushes to `main` is acceptable because strict checks, tests, build validation, and smoke checks gate publication.

## Frontend interactivity

Use small custom JavaScript plus CSS animations in v1. Do not use Alpine.js, Alpine AJAX, HTMX, React, Svelte, Astro, or another frontend framework in v1.

Reasons:

- The planned moving parts are presentational: a hero typewriter/carousel, continuous technology marquee rows, and subtle pulsing/floating hero technology logos.
- CSS is the right tool for continuous/decorative motion such as marquee loops and logo pulse/float.
- The typewriter/carousel has timing state, but it is isolated enough for a tiny local script that progressively enhances pre-rendered hero lines.
- Alpine.js is useful for richer user-driven UI state such as tabs, filters, modals, and navigation drawers; the v1 theme toggle is small enough for plain JavaScript.
- Alpine AJAX and HTMX are designed around server-rendered fragments or dynamic fetch/replace flows. GitHub Pages has no backend fragment endpoints, so they would not earn their complexity in v1.
- Avoiding a frontend framework keeps the technical story centered on the Python compiler and static deployment pipeline.

Future posture:

- Alpine.js may be reconsidered after v1 if the site grows richer user-driven interactions.
- HTMX or Alpine AJAX should only be reconsidered if the project gains a backend or a deliberate static-fragment loading architecture.

## Animation boundaries

V1 animation is intentionally restrained:

- Hero typewriter/carousel: small custom JavaScript over pre-rendered HTML lines.
- Technology marquee: CSS-first continuous animation using duplicated rendered items; JavaScript may be added later only if real content shows the CSS loop quality is insufficient.
- Hero technology logos: CSS-only subtle motion with explicit designed positions.

Support reduced-motion preferences in v1 with CSS-first safeguards: stop decorative animations, hide duplicated marquee content, and avoid animated hover movement where possible without adding framework complexity.

## Hero technology logos

Hero logos are both decorative atmosphere and curated technical associations. They should represent a small set of core technologies associated with the owner, such as Python, PyTorch, SQL, or Hugging Face.

Rules:

- Select hero logos in `content/profile.yaml`.
- Validate selections against known Technology Tags from the technology marquee source.
- Require selected hero logos to have local SVG icons.
- Treat them as association/decorative signals, not proficiency ratings.
- Use explicit positions and subtle CSS motion rather than JavaScript randomization.
