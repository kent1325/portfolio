#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def print_group_start(name: str) -> None:
    if os.environ.get("GITHUB_ACTIONS"):
        print(f"::group::{name}")
    else:
        print(f"\n==> {name}")


def print_group_end() -> None:
    if os.environ.get("GITHUB_ACTIONS"):
        print("::endgroup::")


def run_logged(name: str, command: list[str], log_path: Path, env: dict[str, str]) -> int:
    print_group_start(name)
    print("$ " + " ".join(command))
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    output = result.stdout + result.stderr
    log_path.write_text(output, encoding="utf-8")
    if output:
        print(output, end="" if output.endswith("\n") else "\n")
    print(f"{name} exited with {result.returncode}")
    print_group_end()
    return result.returncode


def run_accessibility(dist_path: Path, reports_path: Path, env: dict[str, str]) -> bool:
    (reports_path / "accessibility").mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "scripts/check_accessibility.py",
        "--dist",
        str(dist_path),
        "--output",
        str(reports_path / "accessibility" / "accessibility.json"),
    ]
    return_code = run_logged(
        "Static accessibility audit",
        command,
        reports_path / "logs" / "accessibility.log",
        env,
    )
    return return_code == 0


def run_external_links(dist_path: Path, reports_path: Path, env: dict[str, str]) -> bool:
    (reports_path / "links").mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "scripts/check_external_links.py",
        "--dist",
        str(dist_path),
        "--output",
        str(reports_path / "links" / "external-links.json"),
    ]
    return_code = run_logged(
        "External link audit",
        command,
        reports_path / "logs" / "external-links.log",
        env,
    )
    return return_code == 0


def discover_pages(dist_path: Path) -> list[str]:
    return [path.relative_to(dist_path).as_posix() for path in sorted(dist_path.rglob("*.html"))]


def read_json_report(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as error:
        return {"error": f"Invalid JSON report: {error}"}


def display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return str(path)


def result_label(passed: bool) -> str:
    return "✅ Passed" if passed else "❌ Failed"


def format_accessibility_details(report: dict[str, Any] | None) -> str:
    if report is None:
        return "report missing"
    if "error" in report:
        return str(report["error"])

    summary = report.get("summary", {})
    pages = summary.get("pages", 0)
    errors = summary.get("errors", 0)
    warnings = summary.get("warnings", 0)
    return f"{pages} pages, {errors} errors, {warnings} warnings"


def format_external_link_details(report: dict[str, Any] | None) -> str:
    if report is None:
        return "report missing"
    if "error" in report:
        return str(report["error"])

    summary = report.get("summary", {})
    ok = summary.get("ok", 0)
    warnings = summary.get("warnings", 0)
    failed = summary.get("failed", 0)
    return f"{ok} ok, {warnings} warnings, {failed} failed"


def limit_notes(notes: list[str], limit: int) -> list[str]:
    if len(notes) <= limit:
        return notes
    remaining = len(notes) - limit
    return [*notes[:limit], f"- …and {remaining} more. See the JSON reports for details."]


def collect_accessibility_notes(report: dict[str, Any] | None, limit: int = 10) -> list[str]:
    if not report:
        return []

    notes: list[str] = []
    for page in report.get("pages", []):
        file_name = page.get("file", "unknown page")
        for error in page.get("errors", []):
            notes.append(f"- accessibility error in `{file_name}`: {error}")
        for warning in page.get("warnings", []):
            notes.append(f"- accessibility warning in `{file_name}`: {warning}")
    return limit_notes(notes, limit)


def collect_external_link_notes(report: dict[str, Any] | None, limit: int = 10) -> list[str]:
    if not report:
        return []

    notes: list[str] = []
    for result in report.get("results", []):
        status = result.get("status")
        if status not in {"failed", "warning"}:
            continue
        reason = result.get("http_status") or result.get("message") or "unknown"
        source = (result.get("sources") or [{"file": "unknown page"}])[0]
        source_file = source.get("file", "unknown page")
        notes.append(
            f"- external link {status}: {result.get('url')} ({reason}) from `{source_file}`"
        )
    return limit_notes(notes, limit)


def build_markdown_summary(
    reports_path: Path,
    pages: list[str],
    results: dict[str, bool],
) -> str:
    accessibility_path = reports_path / "accessibility" / "accessibility.json"
    external_links_path = reports_path / "links" / "external-links.json"
    accessibility_report = read_json_report(accessibility_path)
    external_links_report = read_json_report(external_links_path)

    lines = [
        "## Audit summary",
        "",
        f"Pages audited: {len(pages)}",
        "",
        "| Audit | Result | Details | Report |",
        "| --- | --- | --- | --- |",
        (
            "| Static accessibility | "
            f"{result_label(results.get('accessibility', False))} | "
            f"{format_accessibility_details(accessibility_report)} | "
            f"`{display_path(accessibility_path)}` |"
        ),
        (
            "| External links | "
            f"{result_label(results.get('external_links', False))} | "
            f"{format_external_link_details(external_links_report)} | "
            f"`{display_path(external_links_path)}` |"
        ),
    ]

    notes = [
        *collect_accessibility_notes(accessibility_report),
        *collect_external_link_notes(external_links_report),
    ]
    if notes:
        lines.extend(["", "### Attention needed", "", *notes])
    else:
        lines.extend(["", "No audit warnings or failures were reported."])

    if pages:
        lines.extend(["", "<details>", "<summary>Pages checked</summary>", ""])
        lines.extend(f"- `{page}`" for page in pages)
        lines.extend(["", "</details>"])

    return "\n".join(lines)


def write_markdown_summary(
    reports_path: Path,
    pages: list[str],
    results: dict[str, bool],
) -> None:
    markdown = build_markdown_summary(reports_path, pages, results)
    summary_path = reports_path / "summary.md"
    summary_path.write_text(markdown + "\n", encoding="utf-8")
    print("\n" + markdown)

    github_step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_step_summary:
        with Path(github_step_summary).open("a", encoding="utf-8") as summary_file:
            summary_file.write(markdown + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run generated-site accessibility and external link audits."
    )
    parser.add_argument("--dist", type=Path, default=Path("dist"), help="Generated site directory")
    parser.add_argument(
        "--reports",
        type=Path,
        default=Path("audit-reports"),
        help="Directory where audit reports are written",
    )
    return parser.parse_args()


def build_summary(reports_path: Path, pages: list[str], results: dict[str, bool]) -> dict[str, Any]:
    return {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "pages": pages,
        "reports": {
            "accessibility": str(reports_path / "accessibility" / "accessibility.json"),
            "external_links": str(reports_path / "links" / "external-links.json"),
            "markdown_summary": str(reports_path / "summary.md"),
        },
        "results": results,
    }


def main() -> int:
    args = parse_args()
    dist_path = args.dist.resolve()
    reports_path = args.reports.resolve()

    if not (dist_path / "index.html").exists():
        print(f"Build output is missing: {dist_path / 'index.html'}", file=sys.stderr)
        return 2

    if reports_path.exists():
        shutil.rmtree(reports_path)
    (reports_path / "logs").mkdir(parents=True, exist_ok=True)

    pages = discover_pages(dist_path)
    print(f"Discovered {len(pages)} generated HTML pages to audit:")
    for page in pages:
        print(f"- {page}")

    env = os.environ.copy()
    env["AUDIT_REPORT_DIR"] = str(reports_path)

    results = {
        "accessibility": run_accessibility(dist_path, reports_path, env),
        "external_links": run_external_links(dist_path, reports_path, env),
    }

    summary = build_summary(reports_path, pages, results)
    (reports_path / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_markdown_summary(reports_path, pages, results)

    failed = [name for name, passed in results.items() if not passed]
    if failed:
        print(f"Audit failed: {', '.join(failed)}")
        return 1

    print("All audits passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
