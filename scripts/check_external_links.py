#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import html
import json
import socket
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

DEFAULT_SKIP_HOSTS = frozenset(
    {
        "127.0.0.1",
        "0.0.0.0",
        "localhost",
        "kvugs.github.io",
    }
)
IGNORED_SCHEMES = frozenset({"", "data", "javascript", "mailto", "tel"})
WARNING_STATUSES = frozenset({401, 403, 408, 425, 429, 999})
RETRYABLE_HEAD_STATUSES = frozenset({403, 405, 408, 425, 429, 500, 501, 502, 503, 504, 999})
URL_ATTRIBUTES = {
    "a": ("href",),
    "area": ("href",),
    "audio": ("src",),
    "iframe": ("src",),
    "img": ("src", "srcset"),
    "link": ("href",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "track": ("src",),
    "video": ("src", "poster"),
}


@dataclass(slots=True)
class LinkSource:
    file: str
    tag: str
    attribute: str
    value: str


@dataclass(slots=True)
class CollectedLink:
    url: str
    sources: list[LinkSource] = field(default_factory=list)


class ExternalLinkParser(HTMLParser):
    def __init__(self, file_path: Path, dist_path: Path, skip_hosts: set[str]) -> None:
        super().__init__(convert_charrefs=True)
        self.file_path = file_path
        self.dist_path = dist_path
        self.skip_hosts = skip_hosts
        self.links: dict[str, CollectedLink] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name.lower(): value for name, value in attrs if value is not None}

        for attribute in URL_ATTRIBUTES.get(tag, ()):
            value = attributes.get(attribute)
            if not value:
                continue
            if attribute == "srcset":
                for srcset_url in parse_srcset(value):
                    self._add_url(srcset_url, tag, attribute, value)
            else:
                self._add_url(value, tag, attribute, value)

        # Open Graph/Twitter image URLs and other URL-like metadata are held in content="...".
        if tag == "meta":
            content = attributes.get("content")
            if content:
                self._add_url(content, tag, "content", content)

    def _add_url(self, raw_url: str, tag: str, attribute: str, raw_value: str) -> None:
        normalized = normalize_external_url(raw_url, self.skip_hosts)
        if normalized is None:
            return

        source = LinkSource(
            file=self.file_path.relative_to(self.dist_path).as_posix(),
            tag=tag,
            attribute=attribute,
            value=raw_value,
        )
        self.links.setdefault(normalized, CollectedLink(url=normalized)).sources.append(source)


def parse_srcset(value: str) -> list[str]:
    urls: list[str] = []
    for candidate in value.split(","):
        candidate = candidate.strip()
        if not candidate:
            continue
        urls.append(candidate.split()[0])
    return urls


def normalize_external_url(raw_url: str, skip_hosts: set[str]) -> str | None:
    value = html.unescape(raw_url).strip()
    if not value or value.startswith("#"):
        return None

    parsed = urllib.parse.urlparse(value)
    scheme = parsed.scheme.lower()
    if scheme in IGNORED_SCHEMES or scheme not in {"http", "https"}:
        return None

    host = (parsed.hostname or "").lower()
    if host in skip_hosts or host.endswith(".localhost"):
        return None

    return urllib.parse.urlunparse(parsed._replace(fragment=""))


def collect_external_links(dist_path: Path, skip_hosts: set[str]) -> dict[str, CollectedLink]:
    links: dict[str, CollectedLink] = {}

    for html_file in sorted(dist_path.rglob("*.html")):
        parser = ExternalLinkParser(html_file, dist_path, skip_hosts)
        parser.feed(html_file.read_text(encoding="utf-8"))
        for url, collected in parser.links.items():
            links.setdefault(url, CollectedLink(url=url)).sources.extend(collected.sources)

    return links


def classify_http_status(status: int) -> str:
    if 200 <= status < 400:
        return "ok"
    if status in WARNING_STATUSES:
        return "warning"
    return "failed"


def check_url(url: str, timeout: float, retries: int) -> dict[str, Any]:
    last_error: BaseException | None = None

    for attempt in range(retries + 1):
        for method in ("HEAD", "GET"):
            result = request_url(url, method, timeout)
            if result["status"] != "retry":
                result["attempts"] = attempt + 1
                return result
            last_error = result.get("error")

    return classify_error(url, last_error, retries + 1)


def request_url(url: str, method: str, timeout: float) -> dict[str, Any]:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "kvugs-link-checker/1.0 (+https://kvugs.github.io/)",
    }
    if method == "GET":
        headers["Range"] = "bytes=0-0"

    request = urllib.request.Request(url, method=method, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            http_status = response.status
            return {
                "url": url,
                "status": classify_http_status(http_status),
                "http_status": http_status,
                "final_url": response.url,
                "message": response.reason,
            }
    except urllib.error.HTTPError as error:
        if method == "HEAD" and error.code in RETRYABLE_HEAD_STATUSES:
            return {"status": "retry", "error": error}
        return {
            "url": url,
            "status": classify_http_status(error.code),
            "http_status": error.code,
            "final_url": error.url,
            "message": str(error.reason),
        }
    except TimeoutError as error:
        return {"status": "retry", "error": error}
    except urllib.error.URLError as error:
        return {"status": "retry", "error": error}


def classify_error(url: str, error: BaseException | None, attempts: int) -> dict[str, Any]:
    reason = getattr(error, "reason", error)
    message = str(reason) if reason else "unknown error"
    status = "failed"

    if isinstance(reason, TimeoutError | socket.timeout):
        status = "warning"
    elif isinstance(reason, ssl.SSLError):
        status = "failed"
    elif isinstance(reason, socket.gaierror):
        status = "failed"
    elif isinstance(error, urllib.error.HTTPError):
        status = classify_http_status(error.code)

    return {
        "url": url,
        "status": status,
        "http_status": getattr(error, "code", None),
        "final_url": getattr(error, "url", None),
        "message": message,
        "attempts": attempts,
    }


def source_to_dict(source: LinkSource) -> dict[str, str]:
    return {
        "file": source.file,
        "tag": source.tag,
        "attribute": source.attribute,
        "value": source.value,
    }


def build_report(results: list[dict[str, Any]]) -> dict[str, Any]:
    grouped = {
        "ok": [result for result in results if result["status"] == "ok"],
        "warnings": [result for result in results if result["status"] == "warning"],
        "failed": [result for result in results if result["status"] == "failed"],
    }
    return {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "summary": {key: len(value) for key, value in grouped.items()},
        "results": results,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check generated HTML for broken external links.")
    parser.add_argument("--dist", type=Path, default=Path("dist"), help="Generated site directory")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("audit-reports/links/external-links.json"),
        help="JSON report path",
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    parser.add_argument(
        "--retries",
        type=int,
        default=1,
        help="Retries after the first failed attempt",
    )
    parser.add_argument("--concurrency", type=int, default=6, help="Concurrent link checks")
    parser.add_argument(
        "--skip-host",
        action="append",
        default=[],
        help="Host to skip; may be repeated. Defaults include kvugs.github.io and localhost.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dist_path = args.dist.resolve()
    if not dist_path.exists():
        print(f"Generated site directory does not exist: {dist_path}", file=sys.stderr)
        return 2

    skip_hosts = set(DEFAULT_SKIP_HOSTS) | {host.lower() for host in args.skip_host}
    collected_links = collect_external_links(dist_path, skip_hosts)
    print(f"Found {len(collected_links)} unique external links to check.")

    results_by_url: dict[str, dict[str, Any]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        future_to_url = {
            executor.submit(check_url, url, args.timeout, args.retries): url
            for url in sorted(collected_links)
        }
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            result = future.result()
            result["sources"] = [source_to_dict(source) for source in collected_links[url].sources]
            results_by_url[url] = result
            print(f"[{result['status']}] {url} ({result.get('http_status') or result['message']})")

    report = build_report([results_by_url[url] for url in sorted(results_by_url)])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary = report["summary"]
    print(
        "External link check complete: "
        f"{summary['ok']} ok, {summary['warnings']} warnings, {summary['failed']} failed."
    )
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
