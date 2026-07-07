#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

WHITESPACE_RE = re.compile(r"\s+")


@dataclass(slots=True)
class InteractiveElement:
    tag: str
    attrs: dict[str, str]
    line: int
    text_parts: list[str] = field(default_factory=list)

    @property
    def accessible_name(self) -> str:
        explicit_name = self.attrs.get("aria-label") or self.attrs.get("title")
        text = " ".join([explicit_name or "", *self.text_parts])
        return WHITESPACE_RE.sub(" ", text).strip()


@dataclass(slots=True)
class PageAudit:
    file: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)


class AccessibilityParser(HTMLParser):
    def __init__(self, file_path: Path, dist_path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.audit = PageAudit(file=file_path.relative_to(dist_path).as_posix())
        self.dist_path = dist_path
        self.html_lang: str | None = None
        self.main_count = 0
        self.main_content_id_seen = False
        self.skip_link_seen = False
        self.meta_description_seen = False
        self.h1_count = 0
        self.title_depth = 0
        self.title_text: list[str] = []
        self.ids: dict[str, int] = {}
        self.interactive_stack: list[InteractiveElement] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized_attrs = {name.lower(): value or "" for name, value in attrs}
        line, _ = self.getpos()

        element_id = normalized_attrs.get("id")
        if element_id:
            if element_id in self.ids:
                self.audit.error(
                    f"Duplicate id '{element_id}' at line {line}; first seen at line "
                    f"{self.ids[element_id]}."
                )
            else:
                self.ids[element_id] = line

        if tag == "html":
            self.html_lang = normalized_attrs.get("lang", "").strip()
        elif tag == "main":
            self.main_count += 1
            if normalized_attrs.get("id") == "main-content":
                self.main_content_id_seen = True
        elif tag == "title":
            self.title_depth += 1
        elif tag == "meta":
            name = normalized_attrs.get("name", "").lower()
            content = normalized_attrs.get("content", "").strip()
            if name == "description" and content:
                self.meta_description_seen = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "img":
            self._check_image(normalized_attrs, line)
        elif tag in {"a", "button"}:
            self._start_interactive(tag, normalized_attrs, line)

        if tag == "a":
            self._check_link(normalized_attrs, line)

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)
        for element in self.interactive_stack:
            element.text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1
        if tag not in {"a", "button"}:
            return

        for index in range(len(self.interactive_stack) - 1, -1, -1):
            element = self.interactive_stack[index]
            if element.tag != tag:
                continue
            self.interactive_stack.pop(index)
            if not element.accessible_name:
                self.audit.error(f"<{tag}> at line {element.line} has no accessible name.")
            return

    def close(self) -> None:
        super().close()
        self._check_document_landmarks()

    def _start_interactive(self, tag: str, attrs: dict[str, str], line: int) -> None:
        element = InteractiveElement(tag=tag, attrs=attrs, line=line)
        if tag == "a" and "skip-link" in attrs.get("class", "").split():
            self.skip_link_seen = attrs.get("href") == "#main-content"
        self.interactive_stack.append(element)

    def _check_image(self, attrs: dict[str, str], line: int) -> None:
        if "alt" not in attrs:
            self.audit.error(f"<img> at line {line} is missing an alt attribute.")
            return

        alt_text = attrs.get("alt", "")
        for element in self.interactive_stack:
            element.text_parts.append(alt_text)

    def _check_link(self, attrs: dict[str, str], line: int) -> None:
        if attrs.get("target") != "_blank":
            return
        rel_values = set(attrs.get("rel", "").lower().split())
        if "noopener" not in rel_values:
            self.audit.warning(f"External-tab link at line {line} should include rel='noopener'.")

    def _check_document_landmarks(self) -> None:
        title = WHITESPACE_RE.sub(" ", " ".join(self.title_text)).strip()

        if not self.html_lang:
            self.audit.error("<html> is missing a non-empty lang attribute.")
        if not title:
            self.audit.error("Document is missing a non-empty <title>.")
        if not self.meta_description_seen:
            self.audit.error("Document is missing a non-empty meta description.")
        if self.main_count != 1:
            self.audit.error(f"Document must have exactly one <main>; found {self.main_count}.")
        if not self.main_content_id_seen:
            self.audit.error("Document <main> must use id='main-content'.")
        if not self.skip_link_seen:
            self.audit.error("Document is missing a skip link to #main-content.")
        if self.h1_count != 1:
            self.audit.error(f"Document must have exactly one <h1>; found {self.h1_count}.")


def audit_file(html_file: Path, dist_path: Path) -> PageAudit:
    parser = AccessibilityParser(html_file, dist_path)
    parser.feed(html_file.read_text(encoding="utf-8"))
    parser.close()
    return parser.audit


def build_report(audits: list[PageAudit]) -> dict[str, Any]:
    return {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "summary": {
            "pages": len(audits),
            "errors": sum(len(audit.errors) for audit in audits),
            "warnings": sum(len(audit.warnings) for audit in audits),
        },
        "pages": [
            {"file": audit.file, "errors": audit.errors, "warnings": audit.warnings}
            for audit in audits
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run static accessibility checks against generated HTML."
    )
    parser.add_argument("--dist", type=Path, default=Path("dist"), help="Generated site directory")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("audit-reports/accessibility/accessibility.json"),
        help="JSON report path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dist_path = args.dist.resolve()
    if not dist_path.exists():
        print(f"Generated site directory does not exist: {dist_path}", file=sys.stderr)
        return 2

    audits = [audit_file(path, dist_path) for path in sorted(dist_path.rglob("*.html"))]
    report = build_report(audits)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for audit in audits:
        for warning in audit.warnings:
            print(f"[warning] {audit.file}: {warning}")
        for error in audit.errors:
            print(f"[error] {audit.file}: {error}")

    summary = report["summary"]
    print(
        "Accessibility check complete: "
        f"{summary['pages']} pages, {summary['errors']} errors, "
        f"{summary['warnings']} warnings."
    )
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
