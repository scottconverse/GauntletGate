# GauntletGate

**An adversarial stage-gate your product must survive to advance.**

Version 0.1.0 · MIT licensed · a skill for [Claude Code](https://claude.com/claude-code) (and Codex-style agents)

> **What it is, honestly.** GauntletGate is a *skill* — a Markdown instruction set
> an AI coding agent loads and follows. It is not a binary, a CI job, or a service.
> One command, three lanes; the argument picks which run. It reads your repo as the
> source of truth and drives your running app with Playwright. It works with any
> agent that can run Playwright and read your code; it's written for Claude Code and
> Codex.

---

## The idea

At the end of a stage, sprint, or before a release, you run the gauntlet. The
product doesn't advance until it passes. The gate is **adversarial by default** — its
job is to *block* advancement until the product is genuinely ready, not to wave it
through.

It folds three escalating checks into one command, with a single shared standard for
the first-run discipline, the environment attestation, and severity.

## One command, three lanes

`/gauntletgate <args>` — `args` is any subset of:

| arg | lane | what it does | weight |
|-----|------|--------------|--------|
| `lite` | **Lite** | fast single-pass review of a change/slice (first-run-aware) | light, inline |
| `walkthrough` | **Walkthrough** | first-run-truth + interface-wiring runtime audit | light–medium, inline |
| `full` | **Full** | 5-role adversarial deep audit (eng / security / perf / tests / docs / QA) | **heavy, multi-agent, billed** |
| `all` | all three | Lite → Walkthrough → Full, then one gate verdict | **heavy** |

- **Bare `/gauntletgate` = `all`** — the product is the full gauntlet.
- **Any combination:** `/gauntletgate lite walkthrough`, `/gauntletgate walkthrough full`, etc.
- The lanes compose: **Full consumes the Walkthrough report** instead of re-walking the UI, so they compound rather than overlap.

## The verdict

- **CLEAR TO ADVANCE** — only when `all` ran (walkthrough **and** full), at **0 Blocker
  / 0 Critical**, with **first-run coverage VALID and a new user able to reach the core
  feature.**
- **PARTIAL CHECK** — any run missing a required lane (e.g. `lite`, or `walkthrough`
  alone). Explicitly *not* an advancement gate — a cheap run can't masquerade as the
  full gate.
- **DO NOT ADVANCE** — any Blocker/Critical, or invalid first-run coverage on a product
  with a first-run surface, plus the blocking punch list to clear before a re-run.

## Why it exists — the first-run spine

The most expensive defect is the one a developer never sees, because the dev box is
already set up. GauntletGate was built after a real miss: a product was reported
**"near-clean (1 Minor)"** while a brand-new user with no model server hit an immediate
dead-end — and the check had run on a provisioned dev box whose "clean profile"
isolation had silently failed. So every lane that touches a first-run / onboarding /
dependency / empty-data surface must **construct and verify the true first-run state**,
walk the product with dependencies **absent**, treat a provisioned dev box as
**disqualifying**, and file a first-run dead-end on the core feature as a **Blocker**.
That standard lives once, in `skill/gauntletgate/references/shared-backbone.md`, and
all three lanes obey it.

## Install

```bash
python install.py            # -> ~/.claude/skills/gauntletgate/  (Claude Code, every project)
# or project-only:
python install.py --project /path/to/your/project

# then, in a fresh session:
/gauntletgate all            # full stage-gate
/gauntletgate lite | walkthrough | full | <any combination>
```

## Requirements

- An agent that loads skills and can run **Playwright** and read your repo (Claude Code or Codex).
- A locally runnable app (or the gate falls back to static analysis and says so).
- For `full`/`all`: a **multi-agent budget** — Full fans out 5 role subagents (billed).

## Docs

- **[Manual](docs/MANUAL.md)** — lanes, the first-run discipline, the architecture, the verdict, honest limits.
- **[Architecture diagram](docs/architecture.svg)** — the gate, the three lanes, and the verdict logic.
- **[Landing page](https://scottconverse.github.io/GauntletGate/)**
- **[CHANGELOG](CHANGELOG.md)**

## License

MIT — see [LICENSE](LICENSE).
