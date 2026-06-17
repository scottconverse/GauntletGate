#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Install the GauntletGate skill into an agent's skills directory.

Usage:
  python install.py                      # -> ~/.claude/skills/gauntletgate/   (user-level)
  python install.py --project PATH       # -> PATH/.claude/skills/gauntletgate/  (one project)
  python install.py --dest PATH          # -> PATH/gauntletgate/  (any skills dir)

Idempotent: re-running overwrites the installed copy with this repo's version.
To uninstall, delete the installed `gauntletgate/` folder.

After installing, start a fresh session and run:
  /gauntletgate all          (the full stage-gate; also the bare-command default)
  /gauntletgate lite | walkthrough | full | <any combination>
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

SRC = pathlib.Path(__file__).resolve().parent / "skill" / "gauntletgate"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Install the GauntletGate skill.")
    ap.add_argument("--project", help="install into <PROJECT>/.claude/skills/gauntletgate/")
    ap.add_argument("--dest", help="install into <DEST>/gauntletgate/ (any skills dir)")
    args = ap.parse_args(argv[1:])

    if not (SRC / "SKILL.md").is_file():
        print(f"error: skill source not found at {SRC}", file=sys.stderr)
        return 2

    if args.dest:
        dest = pathlib.Path(args.dest).expanduser().resolve() / "gauntletgate"
    elif args.project:
        proj = pathlib.Path(args.project).expanduser().resolve()
        if not proj.is_dir():
            print(f"error: project dir does not exist: {proj}", file=sys.stderr)
            return 2
        dest = proj / ".claude" / "skills" / "gauntletgate"
    else:
        dest = pathlib.Path.home() / ".claude" / "skills" / "gauntletgate"

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SRC, dest)

    print(f"installed GauntletGate skill -> {dest}")
    print("start a fresh session, then run:  /gauntletgate all")
    print("(or: /gauntletgate lite | walkthrough | full | any combination)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
