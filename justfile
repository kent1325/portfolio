format:
    uv run ruff check --fix src tests
    uv run ruff format src tests

format-check:
    uv run ruff format --check src tests

lint:
    uv run ruff check src tests

test:
    PYTHONPATH=src uv run pytest

build:
    PYTHONPATH=src uv run python -m portfolio.build && npm run css

smoke:
    test -f dist/index.html
    test -f dist/blog/index.html
    grep -q '<title>Kent Vugs Nielsen</title>' dist/index.html
    grep -q '<meta name="color-scheme" content="light dark">' dist/index.html
    grep -q '<meta name="theme-color" content="#f8fafc" data-theme-color>' dist/index.html
    grep -q 'class="skip-link"' dist/index.html
    grep -q '<main id="main-content" tabindex="-1">' dist/index.html
    grep -q '/assets/scripts/theme-toggle.js' dist/index.html
    grep -q 'data-theme-toggle' dist/index.html
    grep -q '<meta name="description" content=' dist/index.html
    grep -q '<link rel="canonical" href="https://kvugs.github.io/">' dist/index.html
    grep -q '<meta property="og:type" content="website">' dist/index.html
    grep -q '<meta property="og:image" content="https://kvugs.github.io/assets/images/social-preview.png">' dist/index.html
    grep -q '<meta property="og:image:width" content="1200">' dist/index.html
    grep -q '<meta property="og:image:height" content="630">' dist/index.html
    grep -q '<meta name="twitter:card" content="summary_large_image">' dist/index.html
    grep -q '<link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml">' dist/index.html
    grep -q '<title>Posts | Kent Vugs Nielsen</title>' dist/blog/index.html
    grep -q '<meta name="description" content=' dist/blog/index.html
    grep -q '<link rel="canonical" href="https://kvugs.github.io/blog/">' dist/blog/index.html
    grep -q '<title>Linear Programming vs. Integer Linear Programming | Kent Vugs Nielsen</title>' dist/blog/lp-vs-ilp/index.html
    grep -q '<meta name="description" content="Mathematical Optimization.">' dist/blog/lp-vs-ilp/index.html
    grep -q '<link rel="canonical" href="https://kvugs.github.io/blog/lp-vs-ilp/">' dist/blog/lp-vs-ilp/index.html
    grep -q '<meta property="og:type" content="article">' dist/blog/lp-vs-ilp/index.html
    grep -q '<meta name="twitter:image" content="https://kvugs.github.io/assets/images/social-preview.png">' dist/blog/lp-vs-ilp/index.html
    grep -q "/assets/icons/python.svg" dist/index.html
    grep -q "/assets/icons/fastapi.svg" dist/index.html
    grep -q "/assets/icons/docker.svg" dist/index.html
    grep -q "latest-posts-heading" dist/index.html
    grep -q "latest-posts" dist/index.html
    grep -q "latest-post-card" dist/index.html
    grep -q "papers" dist/index.html
    grep -q "Condition Monitoring with Machine Learning" dist/index.html
    grep -q "/assets/papers/condition-monitoring-with-machine-learning.pdf" dist/index.html
    test -f dist/assets/papers/condition-monitoring-with-machine-learning.pdf
    grep -q "bookshelf" dist/index.html
    grep -q "/assets/books/designing-machine-learning-systems.jpg" dist/index.html
    grep -q "events" dist/index.html
    grep -q "/assets/events/pyday.pdf" dist/index.html
    test -f dist/assets/events/pyday.pdf
    grep -q "site-footer" dist/index.html
    grep -q "Built with Python" dist/index.html
    grep -q "/blog/data-science-in-esports/" dist/index.html
    grep -q "/blog/lp-vs-ilp/" dist/index.html
    test -f dist/blog/lp-vs-ilp/index.html
    test -f dist/blog/data-science-in-esports/index.html
    grep -q "blog-index" dist/blog/index.html
    grep -q "blog-post" dist/blog/lp-vs-ilp/index.html
    grep -q "blog-post__body" dist/blog/lp-vs-ilp/index.html
    test -f dist/assets/styles.css
    test -f dist/assets/images/social-preview.png
    test -f dist/assets/images/favicon.svg
    test -f dist/assets/books/designing-machine-learning-systems.jpg
    grep -q "prefers-color-scheme: dark" dist/assets/styles.css
    grep -q "prefers-reduced-motion: reduce" dist/assets/styles.css
    grep -q "focus-visible" dist/assets/styles.css
    grep -q "data-theme=\\\"dark\\\"" dist/assets/styles.css
    grep -q "technology-marquee-scroll" dist/assets/styles.css
    test -f dist/assets/icons/python.svg
    test -f dist/assets/icons/fastapi.svg
    test -f dist/assets/icons/docker.svg
    grep -q "/assets/scripts/hero-lines.js" dist/index.html
    test -f dist/assets/scripts/hero-lines.js
    test -f dist/assets/scripts/theme-toggle.js
    grep -q "/assets/icons/linkedin.svg" dist/index.html
    grep -q "/assets/icons/github.svg" dist/index.html
    test -f dist/assets/icons/linkedin.svg
    test -f dist/assets/icons/github.svg

check: format-check lint test build smoke

hooks-install:
    uv run pre-commit install

hooks-run:
    uv run pre-commit run --all-files

serve:
    uv run python -m http.server 8000 -d dist
