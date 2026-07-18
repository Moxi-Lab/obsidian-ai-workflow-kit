#!/usr/bin/env python3
"""CLI entry point for Obsidian AI Workflow Kit helpers."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from kb.cli import build_parser, main
from kb.config import *
from kb.health import *
from kb.install import *
from kb.intake import *
from kb.migrate import *
from kb.project import *
from kb.release import *
from kb.utils import *


if __name__ == "__main__":
    sys.exit(main())
