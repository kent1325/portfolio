from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_accessibility.py"
SPEC = importlib.util.spec_from_file_location("check_accessibility", SCRIPT_PATH)
assert SPEC is not None
check_accessibility = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_accessibility
assert SPEC.loader is not None
SPEC.loader.exec_module(check_accessibility)


def test_accessibility_checker_accepts_basic_accessible_document(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    html_file = dist / "index.html"
    html_file.write_text(
        """
        <!doctype html>
        <html lang="en">
          <head>
            <title>Example</title>
            <meta name="description" content="Example page">
          </head>
          <body>
            <a class="skip-link" href="#main-content">Skip to content</a>
            <main id="main-content">
              <h1>Example</h1>
              <a href="/about/">About</a>
              <button type="button" aria-label="Toggle theme"></button>
              <img src="/assets/example.png" alt="Example diagram">
            </main>
          </body>
        </html>
        """,
        encoding="utf-8",
    )

    audit = check_accessibility.audit_file(html_file, dist)

    assert audit.errors == []


def test_accessibility_checker_reports_missing_names_and_landmarks(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    html_file = dist / "index.html"
    html_file.write_text(
        """
        <!doctype html>
        <html>
          <head><title></title></head>
          <body>
            <main>
              <a href="/empty/"></a>
              <img src="/assets/example.png">
            </main>
          </body>
        </html>
        """,
        encoding="utf-8",
    )

    audit = check_accessibility.audit_file(html_file, dist)

    assert "<html> is missing a non-empty lang attribute." in audit.errors
    assert "Document <main> must use id='main-content'." in audit.errors
    assert any("<a>" in error and "accessible name" in error for error in audit.errors)
    assert any("<img>" in error and "alt" in error for error in audit.errors)
