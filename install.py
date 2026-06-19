#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Install the GauntletGate skill into an agent's skills directory.

Usage:
  python install.py                      # auto-detect Codex or CoWork/Claude
  python install.py --app codex          # -> ~/.codex/skills/gauntletgate/
  python install.py --app cowork         # -> ~/.claude/skills/gauntletgate/
  python install.py --project PATH       # -> PATH/.<app>/skills/gauntletgate/
  python install.py --dest PATH          # -> PATH/gauntletgate/  (any skills dir)
  python install.py --backup             # save the prior install to <dest>.bak-<ts> first

Re-running REPLACES the installed copy with this repo's version (it does not merge).
If you've customized the installed files, pass --backup to preserve the prior copy
next to the new one. To uninstall, delete the installed `gauntletgate/` folder.

After installing, start a fresh agent session. In Codex, ask for GauntletGate by
name or natural language. In CoWork/Claude-style agents, use the slash command
shown in the skill docs.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import sys
import time

SRC = pathlib.Path(__file__).resolve().parent / "skill" / "gauntletgate"
APP_CHOICES = ("auto", "codex", "cowork", "claude")


def app_config(app: str) -> tuple[str, str, str]:
    """Return display name, home env var, and dotdir for an app format."""
    if app == "codex":
        return ("Codex", "CODEX_HOME", ".codex")
    if app in {"cowork", "claude"}:
        return ("CoWork/Claude", "COWORK_HOME", ".claude")
    raise ValueError(f"unknown app: {app}")


def existing_app_home(app: str) -> pathlib.Path:
    _, env_var, dotdir = app_config(app)
    if app in {"cowork", "claude"}:
        for var in (env_var, "CLAUDE_CONFIG_DIR"):
            value = os_environ_get(var)
            if value:
                return pathlib.Path(value).expanduser()
    value = os_environ_get(env_var)
    if value:
        return pathlib.Path(value).expanduser()
    return pathlib.Path.home() / dotdir


def os_environ_get(name: str) -> str | None:
    return os.environ.get(name)


def detect_app() -> str | None:
    """Detect a single installed app format, or return None if ambiguous."""
    codex_home = existing_app_home("codex")
    cowork_home = existing_app_home("cowork")

    codex_signal = bool(os_environ_get("CODEX_HOME")) or codex_home.exists()
    cowork_signal = (
        bool(os_environ_get("COWORK_HOME"))
        or bool(os_environ_get("CLAUDE_CONFIG_DIR"))
        or cowork_home.exists()
    )

    if codex_signal and not cowork_signal:
        return "codex"
    if cowork_signal and not codex_signal:
        return "cowork"
    return None


def prompt_for_app() -> str | None:
    print("Choose where to install GauntletGate:")
    print("  1. Codex   (~/.codex/skills/gauntletgate/)")
    print("  2. CoWork  (~/.claude/skills/gauntletgate/)")
    choice = input("Install for Codex or CoWork? [1/2]: ").strip().lower()
    if choice in {"1", "codex", "c"}:
        return "codex"
    if choice in {"2", "cowork", "co", "claude"}:
        return "cowork"
    return None


def resolve_app(requested: str) -> str:
    if requested != "auto":
        return "cowork" if requested == "claude" else requested

    detected = detect_app()
    if detected:
        return detected

    if sys.stdin.isatty():
        selected = prompt_for_app()
        if selected:
            return selected
        raise SystemExit("error: expected Codex or CoWork")

    # Non-interactive fallback preserves the historical installer behavior.
    return "cowork"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Install the GauntletGate skill.")
    ap.add_argument(
        "--app",
        choices=APP_CHOICES,
        default="auto",
        help="agent format to install for (default: auto-detect; claude is an alias for cowork)",
    )
    ap.add_argument("--project", help="install into <PROJECT>/.<app>/skills/gauntletgate/")
    ap.add_argument("--dest", help="install into <DEST>/gauntletgate/ (any skills dir)")
    ap.add_argument(
        "--backup",
        action="store_true",
        help="if a prior install exists, move it to <dest>.bak-<timestamp> instead of deleting it",
    )
    args = ap.parse_args(argv[1:])

    if not (SRC / "SKILL.md").is_file():
        print(f"error: skill source not found at {SRC}", file=sys.stderr)
        return 2

    if args.dest:
        app = "custom"
        app_name = "custom destination"
        app_dotdir = ""
        dest = pathlib.Path(args.dest).expanduser().resolve() / "gauntletgate"
    else:
        app = resolve_app(args.app)
        app_name, _, app_dotdir = app_config(app)

    if args.project and not args.dest:
        proj = pathlib.Path(args.project).expanduser().resolve()
        if not proj.is_dir():
            print(f"error: project dir does not exist: {proj}", file=sys.stderr)
            return 2
        dest = proj / app_dotdir / "skills" / "gauntletgate"
    elif not args.dest:
        dest = existing_app_home(app) / "skills" / "gauntletgate"

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        if args.backup:
            backup = dest.with_name(f"{dest.name}.bak-{int(time.time())}")
            shutil.move(str(dest), str(backup))
            print(f"backed up prior install -> {backup}")
        else:
            shutil.rmtree(dest)
    shutil.copytree(SRC, dest)

    print(f"installed GauntletGate skill for {app_name} -> {dest}")
    if app == "codex":
        print("start a fresh Codex session, then ask Codex to use GauntletGate.")
    elif app == "cowork":
        print("start a fresh CoWork/Claude-style session, then use the gauntletgate command.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
