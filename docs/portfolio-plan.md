# Portfolio Website Plan

## Purpose

Build a personal portfolio website that is professional enough for technical hiring readers while still leaving room for personal expression through writing, formal papers, books, and visual design.

The site should not duplicate a CV or LinkedIn profile. LinkedIn remains the contact/professional-history source, while the portfolio focuses on selected writing, formal papers, intellectual interests, technical taste, and personality.

## Primary Audience

Optimize first for the technical hiring reader: someone evaluating whether the owner is thoughtful, technical, and worth contacting for professional opportunities.

## Hosting Decision

Use GitHub Pages as a static host.

Target hosting mode:

- GitHub Pages user site
- Repository name: `<github-username>.github.io`
- URL: `https://<github-username>.github.io/`

V1 does not implement custom-domain support, but internal links should be root-relative so a future custom domain is not painful.

## Technology Stack

See [Tech Stack Rationale](./tech-stack-rationale.md) for the personal-skill-fit arguments and alternatives considered.

- Python site compiler
- Markdown for blog posts
- YAML for structured content
- Jinja2 for templates
- Tailwind CSS for styling
- Tailwind Typography for Markdown prose
- Pygments for code highlighting
- Small custom JavaScript for hero text carousel/typewriter behavior
- CSS animations for technology marquee and hero technology logo motion
- GitHub Actions for CI/deployment
- uv for Python dependency management
- npm/Node only for Tailwind CSS compilation; use npm rather than pnpm in v1 to keep tooling minimal
- just for local project commands
- Ruff for formatting/linting
- pytest for compiler/content behavior tests
- Pydantic for strict content schema validation

## Personal Skill Fit

The stack is intentionally Python-centered. The portfolio should showcase Python/backend/data engineering strengths through content modeling, strict validation, compiler architecture, tests, CI, and static deployment. Frontend work should provide polished presentation without becoming the main technical risk.

The v1 balance is roughly 70% shipping and 30% stretch: use familiar Python tools for the core, then stretch through disciplined build architecture, Tailwind styling, and deployment automation rather than through a larger frontend framework.

## Frontend Interactivity Decision

Use small custom JavaScript plus CSS animations in v1 rather than Alpine.js, Alpine AJAX, HTMX, or a larger frontend framework.

Reasoning:

- The planned moving parts are presentational: hero typewriter/carousel text, a continuous technology marquee, and subtle pulsing/floating hero technology logos.
- The marquee and hero logo motion are better expressed as CSS animations than framework state.
- The hero typewriter has timing/state, but it is isolated enough for a tiny local script that progressively enhances pre-rendered HTML.
- Alpine.js is a reasonable later option if the site grows richer user-driven interactions such as filters, tabs, modals, or a navigation drawer.
- Alpine AJAX and HTMX are not useful in v1 because the site is statically hosted on GitHub Pages and has no backend endpoints for server-rendered fragments.
- Avoiding a frontend framework keeps the technical story centered on the Python compiler, strict content validation, and static deployment pipeline.

## Static Site Compiler

Use a custom Python site compiler rather than MkDocs, Pelican, a collection of loose scripts, or a full frontend framework. The compiler is part of the portfolio's technical signal for readers who inspect the repository, not merely hidden build plumbing.

The compiler should:

1. load Markdown/YAML source content,
2. validate schemas, slugs, URLs, links, and declared assets,
3. prepare render output,
4. remove existing `dist/` only after validation succeeds,
5. write the complete static artifact,
6. copy the full `assets/` tree.

Reasoning:

- The site is a custom portfolio, not documentation-first.
- The homepage layout and content model should match the portfolio domain directly.
- Strict validation prevents broken content from silently deploying.
- A compiler-style build avoids stale pages and partial conceptual output better than loose scripts.

## Architecture Quality Principles

- **Maintainability**: keep first-class content types for domain-specific rules, use Pydantic for centralized validation, split compiler responsibilities by content, routes, rendering, assets, and orchestration, and compose homepage sections from partial templates.
- **Reliability**: validate all source content, links, assets, and key generated artifacts before deployment; gate deployment on the full check; use lockfiles and pinned Python and Node runtimes in CI; perform full clean builds without caches.
- **Scalability**: generate static pages with simple routing; defer search, pagination, and tag pages until real content volume requires them.
- **Adaptability**: use root-relative internal URLs, source-based Tailwind scanning, shared card styles with small content-specific variations, and clear module boundaries so later archive pages, pagination, navigation, or custom domains can be added without reshaping v1.

## Project Layout

Planned structure:

```text
content/
  blog/
  profile.yaml
  skills.yaml
  papers.yaml
  books.yaml
  certificates.yaml
  events.yaml

templates/
  base.html
  index.html
  blog_index.html
  blog_post.html
  partials/
    hero.html
    technology_marquee.html
    latest_posts.html
    papers.html
    bookshelf.html
    certificates.html
    events.html

src/
  portfolio_site/
    __init__.py
    build.py
    markdown.py
    content.py
    routes.py
    assets.py

assets/
  images/
    profile.jpg
  icons/
  papers/
  certificates/
  events/
  js/
    hero-carousel.js

styles/
  input.css

dist/

.github/
  workflows/
    check.yml
    deploy.yml

.python-version
.node-version
pyproject.toml
uv.lock
package.json
package-lock.json
tailwind.config.js
justfile
```

`dist/` is generated and should not be committed.

## Homepage Sections

Version 1 homepage order:

1. Hero
2. Unlabeled technology marquee
3. Latest blog posts, if any
4. Formal papers, if any
5. Bookshelf, if any
6. Certificates, if any
7. Events, if any
8. Minimal footer

Empty homepage sections are hidden. Remaining sections keep the same relative order.

No separate projects section in v1. Informal experiments and project explanations should be blog posts/project writeups that link to code/demo where relevant.

No global navigation bar in v1, even after adding certificates and events. The homepage is scroll-based with section headings. Blog pages should include simple local navigation links such as `← Home` or `← Blog`. If homepage content grows enough to need anchors or navigation, handle that as a later UX iteration.

## Hero Section

The hero should include:

- Centered circular profile picture
- Rounded profile image
- Subtle glass/water-drop overlay effect on the image
- Name directly below the image
- Hero text carousel below the name
- GitHub and LinkedIn links only
- Decorative circular/ring/orb graphics around the hero
- Optional subtle pulsing hero technology logos selected from known technology tags

The hero should not include:

- Role/title line
- Public email address
- CV link
- Contact CTA
- Extra social/profile links

Implementation:

- Store hero lines in `content/profile.yaml`.
- Require at least one hero line.
- Render all hero lines into HTML source, with the first hero line visible without JavaScript.
- Use a tiny local JavaScript file to progressively enhance the rendered lines into a carousel/typewriter effect.
- Use CSS-based shapes/rings/orbs for decorative graphics.
- Use CSS animation for hero technology logo motion; do not require a frontend framework for decorative movement.
- Avoid canvas, WebGL, or heavy animation libraries in v1.

## Technology Marquee

The marquee shows technology tags rather than proficiency claims. Items may represent expertise, experience, or current learning, so the public UI should not label them as “skills” or show proficiency levels.

Rules:

- Use unlabeled marquee rows in the UI.
- Keep row labels in YAML for source organization/accessibility only.
- `name` required for each item.
- `icon` optional.
- Icons must be local SVG asset references when present.
- Text fallback is acceptable.
- Render duplicated marquee row items in templates and use CSS-first continuous animation.
- Add JavaScript for marquee behavior only if real content shows the CSS loop quality is insufficient.

## Blog

- Blog source is flat: `content/blog/*.md` only.
- Post URLs come from lowercase kebab-case filenames.
- No frontmatter `slug` field in v1.
- Published posts require `title`, `status`, `summary`, and `published_date`.
- `updated_date` is optional and must not precede `published_date`.
- Draft posts may be incomplete but must have valid filenames/slugs.
- Publication is controlled by `status: published`; dates do not schedule posts.
- `/blog/` is always generated.
- Homepage shows the five latest published posts when any exist.
- Project writeups are normal blog posts with optional typed `github` and `demo` links.
- No series, featured posts, tag filtering, or tag pages in v1.

## Papers

The papers section is for formal academic or research documents only.

- Every paper requires title, year, summary, and at least one paper artifact.
- A paper artifact is either a public local PDF or a formal external paper page.
- GitHub/code links may support a paper but do not replace the paper artifact.
- Informal experiments, notebooks, and implementation reports belong in blog posts/project writeups.
- Papers are sorted by year descending, preserving source order for papers with the same year.
- No dedicated papers archive page in v1.

## Bookshelf

The bookshelf shows books the owner has read or is currently reading.

- Supported statuses: `read`, `reading`.
- `want_to_read` is not supported in v1.
- No reflections, summaries, or read dates in bookshelf data.
- If the owner wants to share thoughts on a book, publish a blog post.
- No dedicated books archive page in v1.

## Certificates

The certificates section shows completed certificates with downloadable PDF artifacts.

- Each certificate includes title, issuer, issued date, and a local PDF file under `/assets/`; `/assets/certificates/` is the recommended organization.
- Certificate issued dates may use `YYYY`, `YYYY-MM`, or `YYYY-MM-DD` precision.
- Certificate summaries are not supported in v1.
- All certificates are shown on the homepage.
- Certificates are sorted by issued date descending.
- For sorting, partial certificate dates use the last possible missing value: `YYYY` behaves like `YYYY-12-31`, and `YYYY-MM` behaves like the last day of that month.
- Missing or empty certificates content hides the section.
- No dedicated certificates archive page in v1.

## Events

The events section shows events the owner has participated in, such as AI conferences, Python conferences, and Pi Day.

- Each event includes name, role, and date.
- Event roles are limited to attendee, speaker, organizer, or volunteer.
- Event location is optional free display text, not structured city/country data.
- Event dates may use `YYYY`, `YYYY-MM`, or `YYYY-MM-DD` precision.
- Event dates represent the start date for multi-day events.
- Events may link to the event homepage.
- Events may link to a local bundled PDF participation artifact under `/assets/`, such as an attendance diploma; `/assets/events/` is the recommended organization.
- All events are shown on the homepage.
- Events are sorted by date descending.
- For sorting, partial event dates use the last possible missing value: `YYYY` behaves like `YYYY-12-31`, and `YYYY-MM` behaves like the last day of that month.
- Events should represent actual participation rather than an aspirational event calendar.
- Missing or empty events content hides the section.
- No dedicated events archive page in v1.

## Visual Direction

V1 should be minimal professional with restrained animations.

Use:

- Clean typography
- Strong centered hero
- Subtle image treatment
- Hero text carousel
- Technology marquee
- Shared base card style with small content-specific variations for papers, books, certificates, and events
- Card hover effects
- System-preference dark mode

Avoid in v1:

- Heavy animation frameworks
- Complex 3D effects
- Canvas/WebGL backgrounds
- Overly experimental interactions

Reduced-motion behavior is supported in v1 for decorative animation: stop the hero/typewriter motion, stop the marquee loop, hide duplicated marquee content, and minimize animated hover movement.

## Dark Mode

Support dark mode from v1 using system preference plus a small manual theme override.

Implementation:

- Use CSS custom properties and explicit dark selectors for source-controlled styling
- Apply system preference by default
- Use a tiny local script and `localStorage` only for the manual override

## Footer

Use an extremely minimal footer.

Possible content:

```text
© 2026 Your Name · GitHub · LinkedIn
```

or:

```text
Built with Python, Markdown, and Tailwind.
```

No contact form, email, or contact CTA.
