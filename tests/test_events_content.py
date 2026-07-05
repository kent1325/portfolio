from pathlib import Path
from textwrap import dedent

from pytest import raises

from portfolio.content import EventParticipation, load_events


def _write_event_pdf(root_path: Path, pdf_path: str) -> None:
    path = root_path / pdf_path.removeprefix("/")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"placeholder pdf bytes")


def _write_events_yaml(root_path: Path, content: str) -> None:
    content_dir = root_path / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    (content_dir / "events.yaml").write_text(dedent(content), encoding="utf-8")


def test_load_events_loads_valid_events_newest_first(tmp_path: Path) -> None:
    _write_event_pdf(tmp_path, "/assets/events/pyday.pdf")
    _write_events_yaml(
        tmp_path,
        """\
        - name: "Older Event"
          role: "speaker"
          date: "2024-04"
          location: "Online"
          tags:
            - python
          links:
            homepage: "https://example.com/older-event"

        - name: " PyDay 2025 "
          role: "attendee"
          date: "2025-11-29"
          tags:
            - python
            - workshops
          links:
            pdf: "/assets/events/pyday.pdf"
        """,
    )

    events: list[EventParticipation] = load_events(tmp_path)

    assert [event.name for event in events] == ["PyDay 2025", "Older Event"]
    assert events[0].role == "attendee"
    assert events[0].role_label == "Attendee"
    assert events[0].date == "2025-11-29"
    assert events[0].tags == ["python", "workshops"]
    assert events[0].links is not None
    assert events[0].links.pdf == "/assets/events/pyday.pdf"
    assert events[1].links is not None
    assert events[1].links.homepage == "https://example.com/older-event"


def test_load_events_returns_empty_list_when_file_is_missing(tmp_path: Path) -> None:
    assert load_events(tmp_path) == []


def test_load_events_returns_empty_list_when_file_is_empty(tmp_path: Path) -> None:
    _write_events_yaml(tmp_path, "")

    assert load_events(tmp_path) == []


def test_load_events_rejects_non_list_yaml_root(tmp_path: Path) -> None:
    _write_events_yaml(
        tmp_path,
        """\
        name: "Not a list"
        role: "attendee"
        date: "2025-11-29"
        """,
    )

    with raises(ValueError, match="YAML root must be a list"):
        load_events(tmp_path)


def test_load_events_rejects_bad_role(tmp_path: Path) -> None:
    _write_events_yaml(
        tmp_path,
        """\
        - name: "Bad Role"
          role: "watcher"
          date: "2025-11-29"
        """,
    )

    with raises(ValueError, match="attendee|speaker|organizer|volunteer"):
        load_events(tmp_path)


def test_load_events_rejects_bad_tag(tmp_path: Path) -> None:
    _write_events_yaml(
        tmp_path,
        """\
        - name: "Bad Tag"
          role: "attendee"
          date: "2025-11-29"
          tags:
            - Python
        """,
    )

    with raises(ValueError, match="tag must be lowercase kebab-case"):
        load_events(tmp_path)


def test_load_events_rejects_bad_homepage_url(tmp_path: Path) -> None:
    _write_events_yaml(
        tmp_path,
        """\
        - name: "Bad Homepage"
          role: "attendee"
          date: "2025-11-29"
          links:
            homepage: "example.com/event"
        """,
    )

    with raises(ValueError, match="homepage must start with http:// or https://"):
        load_events(tmp_path)


def test_load_events_rejects_bad_pdf_path(tmp_path: Path) -> None:
    _write_events_yaml(
        tmp_path,
        """\
        - name: "Bad PDF"
          role: "attendee"
          date: "2025-11-29"
          links:
            pdf: "https://example.com/certificate.pdf"
        """,
    )

    with raises(ValueError, match="pdf must start with /assets/"):
        load_events(tmp_path)


def test_load_events_rejects_non_pdf_artifact_path(tmp_path: Path) -> None:
    _write_events_yaml(
        tmp_path,
        """\
        - name: "Image Artifact"
          role: "attendee"
          date: "2025-11-29"
          links:
            pdf: "/assets/events/certificate.jpg"
        """,
    )

    with raises(ValueError, match="pdf must be a PDF asset"):
        load_events(tmp_path)


def test_load_events_rejects_missing_pdf_file(tmp_path: Path) -> None:
    _write_events_yaml(
        tmp_path,
        """\
        - name: "Missing PDF"
          role: "attendee"
          date: "2025-11-29"
          links:
            pdf: "/assets/events/missing.pdf"
        """,
    )

    with raises(FileNotFoundError, match="Event PDF file not found"):
        load_events(tmp_path)


def test_load_events_rejects_bad_partial_date(tmp_path: Path) -> None:
    _write_events_yaml(
        tmp_path,
        """\
        - name: "Bad Date"
          role: "attendee"
          date: "2025-13"
        """,
    )

    with raises(ValueError, match="date must be YYYY, YYYY-MM, or YYYY-MM-DD"):
        load_events(tmp_path)


def test_load_events_sorts_partial_dates_by_last_possible_date(tmp_path: Path) -> None:
    _write_events_yaml(
        tmp_path,
        """\
        - name: "Full Date"
          role: "attendee"
          date: "2025-11-01"

        - name: "Year Only"
          role: "attendee"
          date: "2025"

        - name: "Month Only"
          role: "attendee"
          date: "2025-11"
        """,
    )

    events = load_events(tmp_path)

    assert [event.name for event in events] == ["Year Only", "Month Only", "Full Date"]
