"""Regression test for direct systemd gateway stops."""

from __future__ import annotations

from hermes_cli import gateway as gateway_cli


def test_units_mark_direct_systemd_stop_as_planned(monkeypatch):
    """ExecStop must mark the PID before systemd delivers SIGTERM."""
    python_path = "/opt/hermes/venv/bin/python"
    monkeypatch.setattr(gateway_cli, "get_python_path", lambda: python_path)
    monkeypatch.setattr(
        gateway_cli,
        "_system_service_identity",
        lambda run_as_user=None: ("alice", "alice", "/home/alice"),
    )

    user_unit = gateway_cli.generate_systemd_unit(system=False)
    system_unit = gateway_cli.generate_systemd_unit(
        system=True,
        run_as_user="alice",
    )

    expected = f"ExecStop=-{python_path} -m gateway.planned_stop $MAINPID"
    assert expected in user_unit
    assert expected in system_unit
