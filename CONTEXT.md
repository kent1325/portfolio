# Portfolio Website

This context describes the public-facing portfolio website: the audience it serves, the content it presents, and the boundaries that keep it distinct from a CV or LinkedIn profile.

## Language

**Content Tag**:
A lowercase kebab-case label that describes the topic of a blog post, paper, or book entry.
_Avoid_: Category, free-text label, mixed-case tag

**Technology Tag**:
A technology, tool, or domain the portfolio owner wants associated with their technical interests or experience, without implying proficiency level.
_Avoid_: Skill rating, proficiency claim, expertise badge

**Technical Hiring Reader**:
A visitor evaluating whether the portfolio owner is thoughtful, technical, and worth contacting for professional opportunities.
_Avoid_: Recruiter-only audience, generic company audience, personal audience

**Profile Link**:
A public external link in the hero that points only to the owner's GitHub or LinkedIn profile.
_Avoid_: Contact link, social link, email link, CV link

**Project Writeup**:
A blog post that explains an informal experiment, technical project, or implementation and may link to code or a demo.
_Avoid_: Project page, research paper, portfolio project card

**Local Asset Reference**:
A public URL path beginning with `/assets/` that points to a file bundled into the portfolio website.
_Avoid_: Filesystem path, source-relative path, implicit asset name

**Paper**:
A formal academic or research document, usually from a university or research context, that may be summarized on the portfolio website.
_Avoid_: Research note, experiment, notebook, project writeup

**Paper Artifact**:
A public PDF or formal external page that lets readers verify or access a paper.
_Avoid_: Code-only link, informal project page, private document

**Portfolio Website**:
A public personal website that presents selected writing, research, interests, and technical taste without duplicating the owner's CV or LinkedIn profile.
_Avoid_: Online CV, resume site, LinkedIn clone

**Source Content**:
The Markdown, YAML, and declared assets that author the portfolio before compilation.
_Avoid_: Data files, CMS content, configuration

**Site Compiler**:
The build process that validates source content and assets, then produces the complete static website output.
_Avoid_: Script collection, page generator, loose build scripts

**Draft Post**:
A blog post that is intentionally private, may be incomplete, and is excluded from website output.
_Avoid_: Unpublished post, hidden post, invalid post

**Published Post**:
A blog post whose status marks it as public and eligible to appear on the website.
_Avoid_: Live post, non-draft post, dated post

**Bookshelf Entry**:
A book the portfolio owner has read or is currently reading and wants to present as part of their intellectual interests without commentary.
_Avoid_: Want-to-read item, reading queue item, book note, book reflection

**Certificate**:
A completed credential the portfolio owner wants to present with a downloadable PDF artifact.
_Avoid_: Course, badge, CV credential, unverifiable claim

**Event Participation**:
A conference, meetup, community event, or technical gathering the portfolio owner attended, spoke at, organized, or otherwise participated in.
_Avoid_: Calendar event, future plan, generic activity log

**Event Homepage**:
A public external page representing the event itself.
_Avoid_: Registration link, arbitrary event-related URL, social media mention

**Event Participation Artifact**:
A bundled local PDF document that verifies or commemorates participation in an event.
_Avoid_: Certificate, paper artifact, remote file link

**Book Reflection**:
A written personal response to a book, published as a blog post rather than stored in the bookshelf.
_Avoid_: Bookshelf summary, book card reflection, reading note

**Blog Source**:
The flat collection of Markdown files that provide blog post content.
_Avoid_: Blog tree, nested posts, content hierarchy

**Hero Line**:
A short identity phrase displayed under the portfolio owner's name in the hero.
_Avoid_: Role title, tagline, JavaScript-only text

**Hero Technology Logo**:
A decorative logo near the avatar that represents one curated core technical association of the portfolio owner.
_Avoid_: Skill badge, proficiency rating, arbitrary decoration

**Internal URL**:
A root-relative public URL path for a page or bundled asset within the portfolio website.
_Avoid_: Absolute site URL, page-relative URL, GitHub project-site URL

**Post Slug**:
The lowercase kebab-case URL-safe identifier for a blog post, derived from the post's source filename.
_Avoid_: Frontmatter slug, post ID, title slug, case-sensitive slug

**Published Date**:
The date a **Published Post** first became public.
_Avoid_: Date, post date, created date

**Updated Date**:
The date a **Published Post** was meaningfully revised after first publication.
_Avoid_: Modified date, edited date, last touched date

## Relationships

- A **Technology Tag** has a name and may have a local SVG icon.
- A **Technology Tag** may appear in an unlabeled marquee row.
- A technology marquee row uses CSS-first continuous animation with duplicated rendered items, with JavaScript allowed later only if the CSS loop quality is insufficient.
- A **Hero Technology Logo** represents a curated **Technology Tag** and may use subtle CSS motion.
- **Hero Technology Logos** are selected in profile source content but must reference known **Technology Tags**.
- **Hero Technology Logos** use CSS-only subtle motion with explicit designed positions rather than randomized JavaScript layout.
- The **Portfolio Website** uses CSS animation for decorative motion and small custom JavaScript for isolated timed behavior, without a frontend framework in version 1.
- Technology marquee row labels may organize **Source Content** but are not visible page headings.
- A **Bookshelf Entry** has a title, author, reading state, and optional **Content Tags**.
- A **Certificate** has a title, issuer, issued date, optional **Content Tags**, and downloadable PDF artifact.
- Certificate PDF artifacts are preferably organized under `/assets/certificates/`, though any local PDF under `/assets/` is valid in v1.
- A **Certificate** issued date may use year, month, or day precision.
- All **Certificates** are presented on the homepage, newest-first by issued date, treating partial dates as the last possible date at that precision.
- Missing or empty **Certificate** content hides the certificate section.
- A **Certificate** does not include a summary in version 1.
- An **Event Participation** describes one past or confirmed event participation by the portfolio owner.
- An **Event Participation** may have zero or more **Content Tags**.
- An **Event Participation** has exactly one lowercase machine role of attendee, speaker, organizer, or volunteer, rendered as human-friendly display text.
- An **Event Participation** may have one free-text location.
- An **Event Participation** date may use year, month, or day precision.
- An **Event Participation** date is the start date for multi-day events.
- All **Event Participations** are presented on the homepage, newest-first by date, treating partial dates as the last possible date at that precision.
- An **Event Participation** may have one **Event Homepage**.
- An **Event Participation** may have one **Event Participation Artifact** as a **Local Asset Reference**.
- Event participation PDF artifacts are preferably organized under `/assets/events/`, though any local PDF under `/assets/` is valid in v1.
- Missing or empty **Event Participation** content hides the events section.
- A **Bookshelf Entry** has a reading state of either read or currently reading.
- A **Bookshelf Entry** does not include a **Book Reflection** or read date.
- A **Book Reflection** belongs in a **Published Post**.
- A blog post, paper, or book entry may have zero or more **Content Tags**.
- An **Internal URL** starts at the site root, uses pretty directory-style page paths, and must resolve within the generated website when used in Markdown links.
- A **Local Asset Reference** is an **Internal URL** under `/assets/`.
- At least one **Hero Line** is visible without JavaScript.
- All **Hero Lines** are rendered into HTML source content, and JavaScript only progressively enhances their display behavior.
- A **Local Asset Reference** must resolve to a file inside the source `assets/` directory.
- Markdown images must use **Local Asset References**.
- The full source `assets/` directory is bundled into the **Portfolio Website**, including unreferenced files.
- A **Project Writeup** is a kind of **Published Post**.
- A **Project Writeup** may have typed GitHub and demo links.
- Informal experiments belong in **Project Writeups**, not in **Papers**.
- A **Profile Link** is limited to GitHub or LinkedIn in version 1.
- A **Profile Link** must use the expected public profile URL shape for its provider.
- A **Paper** may appear on the **Portfolio Website** with a public-facing summary.
- A **Paper** must have at least one **Paper Artifact**.
- Code links may support a **Paper**, but do not replace a **Paper Artifact**.
- The **Portfolio Website** is optimized first for the **Technical Hiring Reader**.
- The **Site Compiler** validates **Source Content** before producing the deployable form of the **Portfolio Website**.
- The **Site Compiler** is part of the portfolio's technical signal for readers who inspect the repository, not merely hidden build plumbing.
- Deployment of the **Portfolio Website** is gated on the full strict validation/build check passing, including smoke checks for required generated HTML and CSS files.
- CI uses pinned Python `3.14` and Node `v26.0.0` runtime versions to reduce workflow drift.
- CI uses committed Python and npm lockfiles for reproducible dependency installation.
- npm is used rather than pnpm in v1 because Node tooling is limited to Tailwind CSS compilation and minimal local setup is preferred.
- Local development uses `just` as the canonical command interface over raw `uv` and npm commands.
- pytest verifies compiler and content behavior using fixture-style tests.
- Static type checking is deferred in version 1 because Pydantic, pytest, and Ruff cover the initial risk profile.
- The **Site Compiler** removes existing output only after validation succeeds.
- The **Site Compiler** writes fresh output directly to `dist/` after removing existing output, rather than swapping from a temporary output directory.
- The **Site Compiler** writes a complete deployable artifact after removing existing output.
- The **Site Compiler** uses full clean builds, not incremental rendering or cached Markdown output.
- **Source Content** must use known fields only.
- A **Blog Source** contains blog posts directly, without nested topic folders.
- A blog post has exactly one **Post Slug**.
- A **Post Slug** comes from the source filename, not frontmatter.
- A **Post Slug** must be lowercase kebab-case.
- Every blog post, including a **Draft Post**, must have a valid **Post Slug**.
- A **Draft Post** and a **Published Post** are mutually exclusive blog post states.
- A **Draft Post** may be incomplete and is excluded from website output.
- A **Published Post** has exactly one **Published Date** and may have one **Updated Date**.
- An **Updated Date** must not be earlier than the **Published Date** for the same **Published Post**.

## Example dialogue

> **Dev:** "Can a **Technology Tag** appear without an icon?"
> **Domain expert:** "Yes — icons are optional; if present, they must be valid local SVG **Local Asset References**."
>
> **Dev:** "Should marquee row labels like `Languages & backend` appear on the page?"
> **Domain expert:** "No — row labels may organize **Source Content**, but the public marquee stays unlabeled."
>
> **Dev:** "Does a marquee item mean the owner is an expert in that technology?"
> **Domain expert:** "No — a **Technology Tag** signals association or experience without claiming a proficiency level."
>
> **Dev:** "Should the bookshelf show books the owner wants to read someday?"
> **Domain expert:** "No — a **Bookshelf Entry** should reflect actual engagement: read or currently reading."
>
> **Dev:** "Should each book card include a short personal reflection?"
> **Domain expert:** "No — keep the bookshelf as a clean list; publish a **Book Reflection** as a blog post when there is something to say."
>
> **Dev:** "Can one post use `Machine Learning` and another use `machine-learning`?"
> **Domain expert:** "No — use a normalized **Content Tag** like `machine-learning` so related content stays consistent."
>
> **Dev:** "Should unused files in `assets/` fail the build?"
> **Domain expert:** "No — declared **Local Asset References** must be valid, but the full assets directory is bundled for predictability."
>
> **Dev:** "Can a blog post embed an image from another website?"
> **Domain expert:** "No — rendered media should be bundled, so Markdown images must use **Local Asset References**."
>
> **Dev:** "If JavaScript fails, should the hero lose its identity text?"
> **Domain expert:** "No — the first **Hero Line** must render as normal content, with carousel behavior as enhancement."
>
> **Dev:** "Should post URLs end in `.html`?"
> **Domain expert:** "No — page **Internal URLs** use pretty directory-style paths such as `/blog/my-post/`."
>
> **Dev:** "Can a blog post link to `/blog/old-post/` after that post is removed?"
> **Domain expert:** "No — Markdown **Internal URLs** must resolve to generated pages or bundled assets."
>
> **Dev:** "Should internal links include `https://username.github.io`?"
> **Domain expert:** "No — use an **Internal URL** like `/blog/my-post/` so the site is not tied to one hostname."
>
> **Dev:** "Should `avatar` be `profile.jpg`, `assets/images/profile.jpg`, or `/assets/images/profile.jpg`?"
> **Domain expert:** "Use a **Local Asset Reference** like `/assets/images/profile.jpg` so content matches the final public URL."
>
> **Dev:** "Can the GitHub **Profile Link** point to a GitLab or personal website URL?"
> **Domain expert:** "No — a **Profile Link** must use the expected URL shape for GitHub or LinkedIn."
>
> **Dev:** "Can the hero include email, CV, Scholar, or social media links?"
> **Domain expert:** "No — a version 1 **Profile Link** is limited to GitHub or LinkedIn."
>
> **Dev:** "Can a **Paper** card link only to a GitHub repository?"
> **Domain expert:** "No — a **Paper** needs a **Paper Artifact** such as a public PDF or formal external page; code can be supporting material."
>
> **Dev:** "Can a **Project Writeup** define arbitrary card links like `dataset`, `slides`, or `notebook`?"
> **Domain expert:** "No — version 1 card links are typed as GitHub or demo; unusual links belong in the post body."
>
> **Dev:** "Can a quick experiment or notebook go in the papers section?"
> **Domain expert:** "No — the papers section is for a formal **Paper**; use a **Project Writeup** for informal experiments."
>
> **Dev:** "Should the homepage lead with a complete professional timeline?"
> **Domain expert:** "No — the **Portfolio Website** is for a **Technical Hiring Reader**, so it should signal competence and taste without becoming an online CV."
>
> **Dev:** "Should the **Site Compiler** delete `dist/` before checking whether content is valid?"
> **Domain expert:** "No — it validates first, then removes existing output and writes the new artifact."
>
> **Dev:** "Can old files stay in `dist/` if no current page writes them?"
> **Domain expert:** "No — the **Site Compiler** performs a clean build so removed content cannot leave stale pages."
>
> **Dev:** "Can we add temporary YAML fields that templates do not use yet?"
> **Domain expert:** "No — **Source Content** must use known fields only so typos and schema drift fail early."
>
> **Dev:** "Can we copy assets even if one blog post has invalid metadata?"
> **Domain expert:** "No — the **Site Compiler** should fail before producing deployable output when source content is invalid."
>
> **Dev:** "Should a future **Published Date** hide a post until that date?"
> **Domain expert:** "No — publication is controlled by whether the post is a **Published Post**; dates communicate publication and freshness to readers."
>
> **Dev:** "Does a **Draft Post** need a summary and **Published Date**?"
> **Domain expert:** "No — a **Draft Post** may be incomplete because it is private and excluded from website output."
>
> **Dev:** "Can we organize posts under topic folders inside the **Blog Source**?"
> **Domain expert:** "No — the **Blog Source** is flat in version 1; topical grouping can come from tags later."
>
> **Dev:** "Can a post filename be `My_Post.md` if the compiler normalizes it?"
> **Domain expert:** "No — the filename stem must already be a lowercase kebab-case **Post Slug**."
>
> **Dev:** "Can the URL differ from the blog post filename?"
> **Domain expert:** "No — the **Post Slug** comes from the source filename so post identity has one source of truth."
>
> **Dev:** "Can a **Draft Post** have a messy temporary filename?"
> **Domain expert:** "No — a **Draft Post** may have incomplete metadata, but its **Post Slug** must still be valid."

## Flagged ambiguities

- "companies" was used broadly; resolved: optimize for the **Technical Hiring Reader** rather than a generic company audience.
- "custom generator" could mean either a compiler-style build or loose scripts; resolved: use **Site Compiler**.
- The compiler could have been treated as disposable behind-the-scenes tooling; resolved: the **Site Compiler** should be clean enough to serve as a technical signal when the repository is inspected.
- The stack could have optimized for frontend framework familiarity; resolved: optimize first for Python/backend/data strengths and use frontend tooling only where it supports visual polish.
- The v1 effort could have maximized learning stretch; resolved: use an approximate 70% shipping and 30% stretch balance.
- Unknown YAML/frontmatter fields could have been ignored; resolved: **Source Content** uses strict known-field schemas.
- Strict schema validation could have used scattered manual checks; resolved: use Pydantic models for centralized content validation.
- Compiler behavior could have relied only on build smoke checks; resolved: include pytest fixture-based behavior tests in version 1.
- Static type checking could have been added immediately with mypy or pyright; resolved: defer it until after version 1 unless the Python codebase grows enough to justify it.
- Tailwind could have scanned generated output; resolved: scan source templates/content and avoid dynamic Python-constructed Tailwind classes.
- Node package management could have used pnpm; resolved: use npm in v1 because it is already available and Tailwind is the only Node-based build tool.
- Local commands could have used Make or raw package-manager commands; resolved: use `just` as the canonical local workflow.
- Asset paths could have used filesystem-relative paths or implicit names; resolved: use **Local Asset Reference** public paths under `/assets/`.
- Markdown images could have embedded external media; resolved: rendered images must be bundled as **Local Asset References**.
- Markdown could have allowed raw HTML; resolved: raw HTML is disabled or escaped in v1.
- Hero carousel text could have depended on JavaScript; resolved: all **Hero Lines** are rendered into HTML and at least one **Hero Line** must be visible without JavaScript.
- Internal links could have used absolute or page-relative paths; resolved: use root-relative **Internal URLs**.
- Page URLs could have exposed `.html` filenames; resolved: use pretty directory-style **Internal URLs**.
- Markdown internal links could have been left to a later link checker; resolved: validate Markdown **Internal URLs** during compilation.
- "date" was ambiguous between creation, publication, scheduling, and freshness; resolved: use **Published Date** and optional **Updated Date**.
- "slug" could have been frontmatter or filename-derived; resolved: use filename-derived **Post Slug** only.
- Blog organization could have used nested folders; resolved: use a flat **Blog Source** in version 1.
- Blog browsing could have included search, pagination, or tag pages in v1; resolved: generate all post pages and a simple blog index, keeping routing boundaries clean for later pagination.
- "research/papers" could have meant broad research artifacts; resolved: a **Paper** is a formal academic or research document.
- Hero links could have expanded into general social/contact links; resolved: **Profile Links** are GitHub and LinkedIn only in version 1.
- Adding more homepage sections could have triggered global navigation or anchor navigation; resolved: v1 remains scroll-based with section headings.
- Paper links could have been optional or code-only; resolved: every **Paper** needs at least one **Paper Artifact**.
- Informal experiments could have become a separate content type; resolved: publish them as **Project Writeups**.
- "skills" could imply proficiency claims; resolved: use unlabeled marquee rows of **Technology Tags** without proficiency levels.
- Marquee animation could have been JavaScript-driven from the start; resolved: use CSS-first duplicated markup, with JavaScript reserved for fixing poor loop quality if needed.
- Alpine.js could have handled small browser interactions; resolved: skip it in version 1 because the current interactions remain small enough for plain JavaScript, while keeping Alpine.js as a possible later option for richer user-driven interactions.
- HTMX or Alpine AJAX could have been used for frontend dynamism; resolved: exclude them in version 1 because static GitHub Pages has no backend fragment endpoints.
- Reduced-motion behavior could have been deferred because the animations are decorative; resolved: support reduced-motion in version 1 with CSS-first safeguards that stop decorative animation and minimize hover movement.
- Hero logos could have been arbitrary decoration or proficiency badges; resolved: use **Hero Technology Logos** as decorative but curated core technical associations without ratings.
- Hero logo source could have been duplicated from the marquee or fully separate; resolved: select **Hero Technology Logos** in profile content while validating them against known **Technology Tags**.
- Hero logo movement could have used JavaScript positioning/randomization; resolved: use CSS-only subtle motion with explicit designed positions.
- "tags" could have been uncontrolled labels or a central taxonomy; resolved: use normalized **Content Tags** without a central registry in version 1.
- The bookshelf could have included aspirational reading; resolved: a **Bookshelf Entry** must be read or currently reading.
- Book thoughts could have been stored as bookshelf summaries; resolved: a **Book Reflection** belongs in a blog post, not a **Bookshelf Entry**.
- Bookshelf entries could have tracked read dates; resolved: use title, author, reading state, and optional **Content Tags** only.
- Certificates and events could have been post-v1 backlog items; resolved: include **Certificate** and **Event Participation** sections in the v1 homepage scope, after **Bookshelf** and before the footer.
- Certificate content could have included summaries or credential verification links; resolved: v1 **Certificate** entries use title, issuer, issued date, optional **Content Tags**, and PDF artifact only.
- Event participation roles could have been free-text; resolved: v1 **Event Participation** roles are attendee, speaker, organizer, or volunteer.
- Event attendance diplomas could have been modeled as **Certificates**; resolved: PDFs tied to event attendance are **Event Participation Artifacts**, while **Certificates** are standalone completed credentials.
- Tags for certificates and events could have introduced separate taxonomies; resolved: use the existing lowercase kebab-case **Content Tags** consistently across site content.
- Structured homepage content could have used one generic collection/card model; resolved: keep first-class content types because **Papers**, **Bookshelf Entries**, **Certificates**, and **Event Participations** have different domain rules.
- The compiler could have been implemented as one large build script; resolved: separate content validation, route inventory, rendering, and build orchestration boundaries.
- Clean builds could have used a temporary directory and atomic swap; resolved: v1 validates first, then deletes and writes `dist/` directly because generated output is disposable and simplicity is preferred.
- Build performance could have been optimized with incremental rendering or caches; resolved: v1 always performs full clean builds because the site is small and cache invalidation would reduce reliability.
