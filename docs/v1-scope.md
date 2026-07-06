# Version 1 Scope

## Included in v1

### Site architecture

- Static GitHub Pages user site at domain root
- Custom Python site compiler
- Markdown blog posts
- Strict YAML structured content with Pydantic validation
- Jinja2 templates
- Tailwind CSS styling
- Tailwind Typography for blog prose
- Pygments for code highlighting
- Small custom JavaScript hero carousel/typewriter behavior
- CSS animations for decorative motion
- System-preference dark mode with a manual theme override
- Reduced-motion handling for decorative animation
- Root-relative internal URLs
- Pretty directory-style generated page URLs

### Pages

- Homepage `/`
- Blog index `/blog/` generated even if there are no published posts
- Individual blog posts `/blog/<slug>/`

### Homepage sections

Fixed relative order, with empty content sections hidden:

1. Hero
2. Unlabeled technology marquee
3. Latest 5 published blog posts, if any
4. Formal papers, if any
5. Bookshelf, if any
6. Certificates, if any
7. Events, if any
8. Minimal footer

### Hero

- Centered circular profile picture
- Glass/water-drop style visual treatment
- Name below picture
- All hero lines rendered into HTML source
- At least one hero line visible without JavaScript
- Carousel/typewriter enhancement for hero lines
- GitHub and LinkedIn profile links only
- CSS-based circular/ring/orb decorations
- Optional CSS-animated hero technology logos selected from known technology tags

### Blog content

- Flat `content/blog/*.md` source only
- Lowercase kebab-case filename-derived slugs
- `status: published` / `status: draft`
- `published_date` required for published posts
- optional `updated_date`
- draft posts may have incomplete metadata but must have valid slugs
- optional lowercase kebab-case content tags
- optional typed project writeup links: `github`, `demo`
- Markdown internal link validation for root-relative links
- Markdown images restricted to local asset references

### Technology marquee

- Source file may remain `content/skills.yaml`
- Public UI has no visible “Skills” label and no visible row labels
- Items are technology tags, not proficiency claims
- Optional local SVG icons
- Text fallback when no icon exists
- CSS-first continuous marquee animation with duplicated rendered items
- JavaScript only if real content shows the CSS loop quality is insufficient

### Papers

- Formal academic/research papers only
- Each paper requires at least one paper artifact: local PDF or formal external page
- Code links are optional supporting links only
- All papers shown on homepage, sorted by year descending
- Homepage-only section; no `/papers/` page

### Bookshelf

- Read or currently-reading books only
- No want-to-read entries
- No bookshelf reflections, summaries, or read dates
- Optional content tags
- Homepage-only section; no `/books/` page

### Certificates

- Completed certificates only
- Title, issuer, issued date, optional content tags, and downloadable local PDF artifact
- Issued date supports `YYYY`, `YYYY-MM`, or `YYYY-MM-DD`
- All certificates shown on homepage, sorted newest-first
- Homepage-only section; no `/certificates/` page

### Events

- Events the portfolio owner has participated in, such as AI conferences, Python conferences, and Pi Day
- Exactly one lowercase role: `attendee`, `speaker`, `organizer`, or `volunteer`
- Date supports `YYYY`, `YYYY-MM`, or `YYYY-MM-DD`; for multi-day events it represents the start date
- Optional free-text location, event homepage link, content tags, and local PDF participation artifact
- All events shown on homepage, sorted newest-first
- Homepage-only section; no `/events/` page

### Quality/deployment

- `uv` dependency management with committed `uv.lock`
- npm/Tailwind CSS build with committed `package-lock.json`
- `justfile` commands
- Ruff formatting/linting
- pytest fixture-based compiler/content behavior tests
- No mypy/pyright static type checker in v1
- GitHub Actions check workflow with pinned Python `3.14` and Node `v26.0.0` versions
- GitHub Actions deploy workflow gated on the full strict validation/build check
- Strict build/content validation, including raw Markdown HTML disabled or escaped
- Clean build behavior: validate first, then remove/write `dist/`
- Copy full `assets/` tree
- Generated `dist/` excluded from source control
- Deployable artifact smoke checks for homepage, blog index, and CSS output

## Excluded from v1

- Global navigation bar
- Contact form
- Public email
- CV link/download
- Additional hero/profile links beyond GitHub and LinkedIn
- Separate projects section
- Dedicated project content type
- Featured posts
- Blog series metadata/navigation
- Search
- Blog pagination
- Tag filtering or tag pages
- Separate `/books/` page
- Separate `/papers/` page
- Separate `/certificates/` page
- Separate `/events/` page
- Book reflections inside bookshelf data
- Want-to-read bookshelf status
- Alpine.js, unless later user-driven interactions justify it after v1
- Alpine AJAX, HTMX, or other server/fragment-driven interaction libraries
- Heavy frontend framework
- Server/backend runtime
- Database/CMS
- Canvas/WebGL/3D animations
- File watching dev server
- Incremental builds or render caching
- Custom-domain/CNAME handling
- External link reachability checks

## Post-v1 Backlog

Potential improvements after the first working deployment:

- Dependabot
- external link checker
- accessibility checker
- Lighthouse/performance checks
- Alpine.js for richer user-driven interactions if the site grows beyond presentational animation
- `/books/` archive page
- `/papers/` archive page
- Featured blog posts
- Blog series support
- Tag filtering or static tag pages
- More advanced local dev watching
- More advanced hero graphics
- Optional custom-domain/CNAME support
- Optional project-specific blog templates

## Open Design Areas for Later Iteration

- Exact hero image glass/water effect
- Exact circular graphics around hero
- Typography choices
- Color palette
- Blog card design
- Small content-specific card variations on top of the shared base card style
- Mobile layout details
- Footer copy
