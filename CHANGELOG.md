# Changelog

All notable changes to FirstRunWalkthrough are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is
[SemVer](https://semver.org/).

## [0.1.0] — 2026-06-17

Initial public release.

### Added
- **The walkthrough skill** (`skill/walkthrough/SKILL.md`) — a Playwright-driven
  interface-wiring audit for an AI coding agent, with a **mandatory, verified
  first-run / zero-state discipline**: construct and prove a clean
  dependency-absent state, walk the product with dependencies absent, treat an
  already-provisioned environment as disqualifying for first-run findings, and
  file a first-run dead-end on the core feature as a Blocker.
- **Report template** (`skill/walkthrough/references/report-template.md`) — with a
  required "Environment provisioning — verified" attestation and a "Zero-state /
  first-run" section, plus a sign-off checklist that gates the verdict.
- **Installer** (`install.py`) — copies the skill into `~/.claude/skills/` (or a
  project's `.claude/skills/`).
- **Docs** — README, full manual (incl. an architecture section), an architecture
  diagram (`docs/architecture.svg`), an honest landing page (`docs/index.html`),
  and discussion-board seed posts.

### Notes
- This is a **skill** (instructions an agent follows), not a binary or CI job. It
  is written for and verified against Claude Code and Codex.
- It is strong guidance with verdict-gating, not a mechanical lock. A future
  release may add a hard "no pass without a verified attestation" enforcement.
