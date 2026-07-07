from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_external_links.py"
SPEC = importlib.util.spec_from_file_location("check_external_links", SCRIPT_PATH)
assert SPEC is not None
check_external_links = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_external_links
assert SPEC.loader is not None
SPEC.loader.exec_module(check_external_links)


def test_collect_external_links_skips_local_and_same_site_urls(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text(
        """
        <a href="/blog/">Blog</a>
        <a href="#main-content">Skip</a>
        <a href="mailto:kent@example.com">Email</a>
        <a href="https://kvugs.github.io/blog/">Canonical self link</a>
        <a href="https://github.com/kvugs#profile">GitHub</a>
        <meta property="og:image" content="https://kvugs.github.io/assets/images/social.png">
        <img srcset="https://cdn.example.com/small.png 1x, https://cdn.example.com/large.png 2x">
        """,
        encoding="utf-8",
    )

    links = check_external_links.collect_external_links(
        dist,
        {"kvugs.github.io", "localhost", "127.0.0.1"},
    )

    assert sorted(links) == [
        "https://cdn.example.com/large.png",
        "https://cdn.example.com/small.png",
        "https://github.com/kvugs",
    ]
    assert links["https://github.com/kvugs"].sources[0].file == "index.html"


def test_classify_http_status_distinguishes_failures_from_inconclusive_blocks() -> None:
    assert check_external_links.classify_http_status(200) == "ok"
    assert check_external_links.classify_http_status(301) == "ok"
    assert check_external_links.classify_http_status(403) == "warning"
    assert check_external_links.classify_http_status(429) == "warning"
    assert check_external_links.classify_http_status(404) == "failed"
    assert check_external_links.classify_http_status(500) == "failed"
