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
    grep -q "/assets/icons/python.svg" dist/index.html
    grep -q "/assets/icons/fastapi.svg" dist/index.html
    grep -q "/assets/icons/docker.svg" dist/index.html
    grep -q "latest-posts-heading" dist/index.html
    grep -q "latest-posts" dist/index.html
    grep -q "latest-post-card" dist/index.html
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
    grep -q "technology-marquee-scroll" dist/assets/styles.css
    test -f dist/assets/icons/python.svg
    test -f dist/assets/icons/fastapi.svg
    test -f dist/assets/icons/docker.svg
    grep -q "/assets/scripts/hero-lines.js" dist/index.html
    test -f dist/assets/scripts/hero-lines.js
    grep -q "/assets/icons/linkedin.svg" dist/index.html
    grep -q "/assets/icons/github.svg" dist/index.html
    test -f dist/assets/icons/linkedin.svg
    test -f dist/assets/icons/github.svg

check: format-check lint test build smoke

serve:
    uv run python -m http.server 8000 -d dist
