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
    grep -q "Python" dist/index.html
    grep -q "FastAPI" dist/index.html
    grep -q "Docker" dist/index.html
    grep -q "Latest posts" dist/index.html
    grep -q "/blog/data-science-in-esports/" dist/index.html
    grep -q "/blog/lp-vs-ilp/" dist/index.html
    test -f dist/blog/lp-vs-ilp/index.html
    test -f dist/blog/data-science-in-esports/index.html
    test -f dist/assets/styles.css

check: format-check lint test build smoke

serve:
    uv run python -m http.server 8000 -d dist
