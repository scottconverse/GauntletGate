# FirstRunWalkthrough

**A walkthrough-audit skill that refuses to call a product "clean" when it's broken for new users.**

Version 0.1.0 · MIT licensed · a skill for [Claude Code](https://claude.com/claude-code) (and Codex-style agents)

> **What it is, honestly.** This is a *skill* — a Markdown instruction set an AI
> coding agent loads and follows. It is not a binary, a test runner, or a service.
> It drives your running app with Playwright, reads your repo as the source of
> truth, and produces an evidence-backed audit report. It works with any agent
> that can run Playwright and read your code; it's written and verified against
> Claude Code and Codex.

---

## The problem it solves

A normal "walkthrough" or smoke test is run on the **developer's machine** — where
the database is seeded, the model server is running, the license is activated, the
config is filled in, and the app has been opened a hundred times. So it audits a
product that is *already working*, and reports it clean.

Then a real new user installs it, opens it, and hits a wall on the first screen:
a disabled primary button, a "go install X yourself" instruction, a blank page, a
silent failure. The single most important defect — *can a brand-new user actually
get started?* — is the one a dev-box walkthrough is structurally blind to.

This skill exists because that happened: a product was audited and reported
**"near-clean (1 Minor)"** while a new user with no model server hit an immediate
dead-end. The audit ran on a fully-provisioned dev box, and its "clean profile"
isolation had silently failed — so it secretly read the real, working profile.

## What it does differently

FirstRunWalkthrough is a full interface-wiring audit — routes, forms, state,
backend wiring, docs/design cross-check, test reality — **plus** a non-negotiable
discipline that ordinary walkthroughs skip:

- **Constructs and *verifies* the true first-run state.** Fresh profile,
  dependencies **absent**, empty data, first-run flags unset — and it *proves* the
  app actually used the clean state instead of trusting an override that may have
  silently failed.
- **Walks the product with each external dependency ABSENT** — the new-user
  reality where dead-ends live — not just with everything conveniently installed.
- **Treats an already-provisioned dev box as disqualifying** for first-run
  findings. If a clean state can't be verified, the run is marked **INVALID** for
  first-run — it is *never* allowed to report "clean."
- **Files a first-run dead-end on the core feature as a Blocker**, not a footnote.

The result: the exact miss above cannot happen again. A product that strands a new
user can no longer pass as near-clean.

## What you get

An evidence-backed report (template included) covering:

- A **verdict** that states, up front, whether a brand-new user can reach the core feature.
- A verified **environment-provisioning attestation** (what was clean/absent, and *how that was confirmed*).
- A **zero-state / first-run** section and a **provisioning matrix** (first-run × dependency-absent × empty-data × offline).
- Numbered, evidence-backed findings (route, expected, actual, evidence, cause, fix, test).
- Docs/design cross-check, test-coverage reality, and an optional wiring map.

## Install

The skill is a folder you drop into your agent's skills directory.

**Claude Code (user-level, available in every project):**
```bash
python install.py            # copies skill/walkthrough/ into ~/.claude/skills/
```
Or do it by hand:
```bash
cp -r skill/walkthrough ~/.claude/skills/walkthrough
```

**Project-level (just this repo):**
```bash
python install.py --project /path/to/your/project   # → <project>/.claude/skills/walkthrough/
```

Then start a session and run `/walkthrough` (or ask the agent for "a full UI
walkthrough / interface-wiring audit"). See the [manual](docs/MANUAL.md) for the
full operating protocol.

## Requirements

- An AI coding agent that loads skills and can run **Playwright** and read your repo (Claude Code or Codex).
- Your app must be runnable locally (the skill derives setup from your repo; if it can't run, it falls back to static analysis and says so).

## Docs

- **[User manual](docs/MANUAL.md)** — operating protocol, the first-run discipline, the architecture, and the report sections.
- **[Architecture diagram](docs/architecture.svg)** — the audit pipeline and its gates.
- **[Landing page](https://scottconverse.github.io/FirstRunWalkthrough/)** — the short version.
- **[CHANGELOG](CHANGELOG.md)**

## License

MIT — see [LICENSE](LICENSE).
