#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Install the FirstRunWalkthrough skill into an agent's skills directory.

Usage:
  python install.py                      # → ~/.claude/skills/walkthrough/  (user-level)
  python install.py --project PATH       # → PATH/.claude/skills/walkthrough/  (one project)
  python install.py --dest PATH          # → PATH/walkthrough/  (any skills dir)

Idempotent: re-running overwrites the installed copy with this repo's version.
The skill is just files — to uninstall, delete the installed `walkthrough/` folder.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

SRC = pathlib.Path(__file__).resolve().parent / "skill" / "walkthrough"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Install the FirstRunWalkthrough skill.")
    ap.add_argument("--project", help="install into <PROJECT>/.claude/skills/walkthrough/")
    ap.add_argument("--dest", help="install into <DEST>/walkthrough/ (any skills dir)")
    args = ap.parse_args(argv[1:])

    if not (SRC / "SKILL.md").is_file():
        print(f"error: skill source not found at {SRC}", file=sys.stderr)
        return 2

    if args.dest:
        dest = pathlib.Path(args.dest).expanduser().resolve() / "walkthrough"
    elif args.project:
        proj = pathlib.Path(args.project).expanduser().resolve()
        if not proj.is_dir():
            print(f"error: project dir does not exist: {proj}", file=sys.stderr)
            return 2
        dest = proj / ".claude" / "skills" / "walkthrough"
    else:
        dest = pathlib.Path.home() / ".claude" / "skills" / "walkthrough"

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SRC, dest)

    print(f"installed FirstRunWalkthrough skill -> {dest}")
    print("start a fresh session, then run:  /walkthrough")
    print('(or ask the agent: "do a full UI walkthrough + interface-wiring audit")')
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
