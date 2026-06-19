# GauntletGate

**An adversarial stage-gate your product must survive to advance.**

Version 0.2.0 · MIT licensed · a skill for Codex Desktop and CoWork/Claude-style agents

> **What it is, honestly.** GauntletGate is a *skill* — a Markdown instruction set
> an AI coding agent loads and follows. It is not a binary, a CI job, or a service.
> One command, three lanes; the argument picks which run. It reads your repo as the
> source of truth and drives your running app with Playwright. It works with any
> agent that can run Playwright and read your code; it's written for Codex Desktop
> and CoWork/Claude-style agents.

---

## The idea

At the end of a stage, sprint, or before a release, you run the gauntlet. The
product doesn't advance until it passes. The gate is **adversarial by default** — its
job is to *block* advancement until the product is genuinely ready, not to wave it
through.

It folds three escalating checks into one gate, with a single shared standard for
the first-run discipline, the environment attestation, and severity.

## One gate, three lanes

Ask your agent to run `gauntletgate <args>`; `args` is any subset of:

| arg | lane | what it does | weight |
|-----|------|--------------|--------|
| `lite` | **Lite** | fast single-pass review of a change/slice (first-run-aware) | light, inline |
| `walkthrough` | **Walkthrough** | first-run-truth + interface-wiring runtime audit | light–medium, inline |
| `full` | **Full** | 5-role adversarial deep audit (eng / security / perf / tests / docs / QA) | **heavy, multi-agent, billed** |
| `all` | all three | Lite → Walkthrough → Full, then one gate verdict | **heavy** |

- **Bare `gauntletgate` = `all`** — the product is the full gauntlet.
- **Any combination:** `gauntletgate lite walkthrough`, `gauntletgate walkthrough full`, etc.
- The lanes compose: **Full consumes the Walkthrough report** instead of re-walking the UI, so they compound rather than overlap.

## The verdict

- **CLEAR TO ADVANCE** — only when the **walkthrough and full lanes both ran** (i.e.
  `all`, or explicitly `walkthrough full`), at **0 Blocker / 0 Critical**, with
  **first-run coverage VALID and a new user able to reach the core feature.**
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
python install.py                # auto-detect Codex or CoWork/Claude
python install.py --app codex    # install to ~/.codex/skills/gauntletgate/
python install.py --app cowork   # install to ~/.claude/skills/gauntletgate/
python install.py --project PATH # project-local install using the selected app format
```

If auto-detection is ambiguous in an interactive terminal, the installer asks you to
choose **Codex** or **CoWork**. In noninteractive contexts it preserves the historical
CoWork/Claude-style default unless `--app` or `--dest` is supplied.

After installing, start a fresh agent session. In Codex Desktop, ask Codex to use
GauntletGate by name or by saying which lane to run. In CoWork/Claude-style agents,
use the slash-command form shown in the installed skill.

## Requirements

- An agent that loads skills and can run **Playwright** and read your repo (Codex Desktop or CoWork/Claude-style agents).
- A locally runnable app (or the gate falls back to static analysis and says so).
- For `full`/`all`: a **multi-agent budget** — Full fans out 5 role subagents (billed).

## Docs

- **[Manual](docs/MANUAL.md)** — lanes, the first-run discipline, the architecture, the verdict, honest limits.
- **[Architecture diagram](docs/architecture.svg)** — the gate, the three lanes, and the verdict logic.
- **[Landing page](https://scottconverse.github.io/GauntletGate/)**
- **[CHANGELOG](CHANGELOG.md)**

## Roadmap

GauntletGate is honest that it's currently **strong guidance, not a mechanical lock**
(see the manual's limits). The named next steps:

- **Mechanical enforcement of the attestation.** A companion check that **refuses to
  emit CLEAR TO ADVANCE unless the verified evidence artifacts exist on disk** — the
  same way a hard gate refuses an action without proof. This turns the first-run
  guarantee from a convention into something checkable by someone other than the agent
  that wrote it.
- **CI integration.** Run `lite` on every PR and `all` at stage boundaries, surfacing
  the verdict as a status check. (This repo already dogfoods: see `eval/` and
  `.github/workflows/eval.yml` — GauntletGate gates itself.)

## Provenance

The **Full** lane's five-role adversarial method isn't invented here — it's distilled
from a multi-role audit methodology (Principal Engineer · UI/UX · Technical Writer ·
Test · QA) that has been run as a stage-close audit on real projects. The
**Walkthrough** lane's first-run discipline likewise comes from a real production miss
(see *Why it exists*). GauntletGate's contribution is folding these, plus a fast Lite
pass, into one argument-dispatched gate with a single shared standard and an honest
verdict. Mentioned here as a maturity signal, not a footnote: the methods are battle-
used, not theoretical.

## License

MIT — see [LICENSE](LICENSE).
