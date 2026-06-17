# Changelog

All notable changes to GauntletGate are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is
[SemVer](https://semver.org/).

## [0.1.0] — 2026-06-17

Initial public release. GauntletGate began as **FirstRunWalkthrough** and absorbed a
lite single-pass lane and a five-role adversarial audit lane into one stage-gate.

### Added
- **The `gauntletgate` skill** (`skill/gauntletgate/SKILL.md`) — one command,
  argument-dispatched to three lanes: `lite`, `walkthrough`, `full`, `all`, or any
  combination. Bare `/gauntletgate` = `all`.
- **Three lanes** (`skill/gauntletgate/lanes/`):
  - **Lite** — fast single-pass on a change/slice, first-run-aware.
  - **Walkthrough** — first-run-truth + interface-wiring runtime audit; verifies the
    real first-run / dependency-absent state.
  - **Full** — 5-role adversarial deep audit that **consumes the Walkthrough report**
    instead of re-walking the UI.
- **Shared backbone** (`references/shared-backbone.md`) — one source of truth for the
  first-run rule, the environment-provisioning attestation, and the severity
  framework, obeyed by all lanes so they can't drift.
- **Gate verdict** (`references/gate-verdict.md`) — CLEAR TO ADVANCE only from a full
  run at 0 Blocker / 0 Critical with first-run valid + reachable; partial runs are
  labeled PARTIAL CHECK and can never greenlight advancement; any Blocker/Critical or
  invalid first-run → DO NOT ADVANCE.
- **Gate report template**, **installer** (`install.py`), and full docs — README,
  manual (with architecture section), architecture diagram (`docs/architecture.svg`),
  honest landing page, discussion seeds.

### Notes
- It's a **skill** (instructions an agent follows), not a binary or CI job. Written
  for and verified against Claude Code and Codex.
- It is strong guidance with verdict-gating, not a mechanical lock. A future release
  may add a hard "no CLEAR TO ADVANCE without a verified attestation" enforcement and
  CI integration.
