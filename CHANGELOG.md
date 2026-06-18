# Changelog

All notable changes to GauntletGate are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is
[SemVer](https://semver.org/).

## [0.2.0] — 2026-06-17

Audit-response sprint (team technical review of v0.1.0). The exit gate for this
release was the new golden eval passing.

### Added
- **Golden eval that gates the repo** (`eval/`) — a sample app with a *genuine*
  dependency-absent first-run dead-end, a harness that constructs the **real** absent
  state (no mocking) and asserts a new user is dead-ended → the condition a correct
  Walkthrough lane reports as DO NOT ADVANCE, with a theater-guard so it can't pass
  vacuously. Writes evidence artifacts. GauntletGate now dogfoods itself.
- **CI** (`.github/workflows/eval.yml`) — runs the skill-structure lint, the golden
  eval, and an installer smoke test on every push/PR; uploads eval artifacts.
- **Per-stack isolation recipes** (`references/isolation-recipes.md`) — web/SaaS, Node,
  Python, Electron, Docker, headless API.
- **Sample reports** (`docs/examples/`) — a real DO NOT ADVANCE (from the eval) and an
  illustrative CLEAR TO ADVANCE.
- **Roadmap** in the README — mechanical enforcement of the attestation + CI.

### Changed
- **Attestation must now link to on-disk evidence artifacts.** An attestation with no
  artifact is treated as UNVERIFIED → first-run coverage INVALID → cannot be CLEAR TO
  ADVANCE. (shared-backbone, gate-verdict, report-template.)
- **`full.md`:** defined the degraded (sequential, no fan-out) fallback — never silently
  changes the verdict — and a deep-dive content schema (empty/generic = coverage gap).
- **Verdict-consistency fix:** reconciled "only `all`" vs "walkthrough + full" across
  README/SKILL/MANUAL to match the governing `gate-verdict.md`.
- **No-UI products:** documented the `first-run N/A` case (library/API/CLI) in the
  shared backbone and the manual.
- **`install.py`:** added `--backup`; dropped the inaccurate "idempotent" wording
  ("replaces, does not merge").
- **MANUAL:** surfaced the honest-limits caveat up front (§1 callout).
- Added a **provenance/credibility note** (Full lane distilled from a battle-used
  multi-role audit method; Walkthrough from a real production miss).

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
