from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_audits.py"
SPEC = importlib.util.spec_from_file_location("run_audits", SCRIPT_PATH)
assert SPEC is not None
run_audits = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = run_audits
assert SPEC.loader is not None
SPEC.loader.exec_module(run_audits)


def test_build_markdown_summary_includes_counts_and_attention_items(tmp_path: Path) -> None:
    reports = tmp_path / "audit-reports"
    accessibility = reports / "accessibility"
    links = reports / "links"
    accessibility.mkdir(parents=True)
    links.mkdir(parents=True)

    (accessibility / "accessibility.json").write_text(
        json.dumps(
            {
                "summary": {"pages": 2, "errors": 1, "warnings": 0},
                "pages": [
                    {
                        "file": "index.html",
                        "errors": ["Example accessibility error."],
                        "warnings": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (links / "external-links.json").write_text(
        json.dumps(
            {
                "summary": {"ok": 3, "warnings": 1, "failed": 0},
                "results": [
                    {
                        "url": "https://example.com/blocked",
                        "status": "warning",
                        "http_status": 403,
                        "message": "Forbidden",
                        "sources": [{"file": "index.html"}],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    summary = run_audits.build_markdown_summary(
        reports,
        ["index.html", "blog/index.html"],
        {"accessibility": False, "external_links": True},
    )

    assert "## Audit summary" in summary
    assert "| Static accessibility | ❌ Failed | 2 pages, 1 errors, 0 warnings" in summary
    assert "| External links | ✅ Passed | 3 ok, 1 warnings, 0 failed" in summary
    assert "Example accessibility error." in summary
    assert "external link warning: https://example.com/blocked (403)" in summary
    assert "`blog/index.html`" in summary
