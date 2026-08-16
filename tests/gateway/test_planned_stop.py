"""Tests for the systemd ExecStop planned-shutdown marker helper."""

from __future__ import annotations

from gateway import planned_stop


def test_main_writes_marker_for_valid_pid(monkeypatch):
    calls: list[int] = []
    monkeypatch.setattr(
        planned_stop,
        "write_planned_stop_marker",
        lambda pid: calls.append(pid) or True,
    )

    assert planned_stop.main(["4242"]) == 0
    assert calls == [4242]


def test_main_rejects_invalid_pid_without_writing(monkeypatch):
    calls: list[int] = []
    monkeypatch.setattr(
        planned_stop,
        "write_planned_stop_marker",
        lambda pid: calls.append(pid) or True,
    )

    assert planned_stop.main(["not-a-pid"]) == 2
    assert planned_stop.main(["0"]) == 2
    assert calls == []


def test_main_reports_marker_write_failure(monkeypatch):
    monkeypatch.setattr(
        planned_stop,
        "write_planned_stop_marker",
        lambda _pid: False,
    )

    assert planned_stop.main(["4242"]) == 1
