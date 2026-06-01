#!/usr/bin/env python3
"""Claude Code Stop hook for advisory knowledge-base maintenance checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def read_hook_payload() -> dict:
    try:
        if sys.stdin.isatty():
            return {}
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def main() -> int:
    payload = read_hook_payload()
    root = Path(payload.get("cwd") or ".").resolve()
    kb_script = root / "scripts" / "kb.py"
    if not kb_script.exists():
        return 0

    result = subprocess.run(
        [
            sys.executable,
            str(kb_script),
            "stale-check",
            "--vault",
            str(root),
            "--max-age-days",
            "7",
            "--inbox-threshold",
            "10",
            "--fail-on-findings",
        ],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return 0

    report = (result.stdout or result.stderr).strip()
    reason = (
        "Before ending this session, review stale knowledge-base items. "
        "Write a handoff or update the project bridge card if project state changed.\n\n"
        + report[-3000:]
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
