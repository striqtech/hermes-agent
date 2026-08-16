"""Mark a systemd gateway stop as intentional before SIGTERM is sent.

The gateway deliberately exits with status 1 after an unexpected SIGTERM so
``Restart=on-failure`` supervisors can revive it.  systemd runs ``ExecStop``
before it sends the service's ``KillSignal``, which gives us the same marker
handshake used by ``hermes gateway stop`` even when an operator invokes
``systemctl stop`` directly.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence

from gateway.status import write_planned_stop_marker


def main(argv: Sequence[str] | None = None) -> int:
    """Write the planned-stop marker for the single PID in *argv*."""
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: python -m gateway.planned_stop PID", file=sys.stderr)
        return 2

    try:
        target_pid = int(args[0])
    except (TypeError, ValueError):
        print(f"invalid gateway PID: {args[0]!r}", file=sys.stderr)
        return 2
    if target_pid <= 0:
        print(f"invalid gateway PID: {target_pid}", file=sys.stderr)
        return 2

    if not write_planned_stop_marker(target_pid):
        print(
            f"could not write planned-stop marker for gateway PID {target_pid}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
