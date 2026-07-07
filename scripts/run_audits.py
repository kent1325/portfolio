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

    failed = [name for name, passed in results.items() if not passed]
    if failed:
        print(f"Audit failed: {', '.join(failed)}")
        return 1

    print("All audits passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
