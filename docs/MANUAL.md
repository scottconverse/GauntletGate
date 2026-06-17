# FirstRunWalkthrough — Manual

Version 0.1.0

This manual covers what the skill is, how to install and run it, the first-run
discipline that is its whole reason to exist, the architecture of the audit
pipeline, the report it produces, and its honest limits.

---

## 1. What it is (and isn't)

FirstRunWalkthrough is a **skill** — a Markdown instruction set that an AI coding
agent (Claude Code, or a Codex-style agent) loads and follows. When you run it, the
agent:

1. reads your repository as the source of truth,
2. brings your app up locally,
3. drives it with Playwright like a real (and adversarial) user, and
4. writes an evidence-backed audit report.

It is **not** a binary, a CI job, or a test framework. It produces no code changes
in audit mode — it observes, verifies, and reports.

**Use it** when a UI is finished or nearly finished and you want an honest answer
to: *does this actually work for a real user — including a brand-new one — or does
it just work on the machine it was built on?*

---

## 2. Install

The skill is a folder you place in your agent's skills directory.

**Claude Code, user-level (every project sees it):**

```bash
python install.py
# copies skill/walkthrough/ → ~/.claude/skills/walkthrough/
```

**Project-level (one repo only):**

```bash
python install.py --project /path/to/project
# → <project>/.claude/skills/walkthrough/
```

**By hand** (any agent that reads a skills folder):

```bash
cp -r skill/walkthrough <your-skills-dir>/walkthrough
```

Start a fresh session, then invoke it with `/walkthrough`, or simply ask for "a
full UI walkthrough and interface-wiring audit."

---

## 3. The first-run discipline (why this exists)

The most expensive UX defect is the one a developer never sees, because the
developer's machine is already set up. Databases are seeded, the model server is
running, the license is activated, settings are filled in, first-run flags were
cleared months ago. A walkthrough run there audits a product that is *already
working* — and the first-run experience, where new users actually live, is never
on screen.

This skill was built after exactly that failure: a product was reported
**"near-clean (1 Minor)"** while a brand-new user with no model server installed
hit an immediate dead-end (the core action was disabled; the setup step told them
to go install the dependency themselves). Two things let it slip:

1. the audit ran on a fully-provisioned dev box, so the dependency-absent
   onboarding flow was never exercised; and
2. the "clean profile" isolation silently failed, and nobody verified it — so the
   supposedly clean run secretly read the real, working profile.

The skill closes both holes with rules that are **not optional**:

- **Construct and *verify* the true first-run state.** Fresh, isolated profile;
  first-run flags unset; empty data; **every external dependency ABSENT**. And
  *prove* the app actually used the clean state — assert it wrote its config and
  first-run markers to the isolated location, not the real one. An override that
  "looks set" but is silently ignored must be caught here.
- **Probe dependencies, don't assume them.** Actively query the model server / DB
  / license / network and record present-or-absent, measured.
- **Walk the product with each dependency ABSENT** — first-run *and* returning —
  because that is the new-user reality where dead-ends live.
- **An already-provisioned environment is disqualifying** for first-run findings.
  If a clean state can't be verified, the run is marked **INVALID** for first-run
  and may *never* report the product as "clean."
- **A first-run dead-end on the core feature is a Blocker** — a disabled primary
  action, a "go install X yourself" with no in-product help, a blank screen, or a
  silent failure — not a footnote.

---

## 4. Architecture

The audit is a pipeline with two gates. The amber stages are the first-run
discipline ordinary walkthroughs skip; the red branch is where a run disqualifies
itself from reporting "clean."

![Audit pipeline](architecture.svg)

**The flow:**

1. **Build the product model** — purpose, roles, workflows, promises, and *every
   external dependency and first-run gate*.
2. **Bring up the app and verify the environment** — prove the clean profile was
   actually used; probe each dependency's real state. → **Gate 1: was a clean
   first-run state verified?** If no, first-run coverage is **INVALID** and the
   verdict must say so.
3. **Zero-state / first-run pass + provisioning matrix** (mandatory) — walk
   onboarding and try the core feature with nothing set up, across
   `first-run × dependency-absent × empty-data × offline`.
4. **Explore with Playwright** — all routes, forms, and states; adversarial paths.
5. **Cross-check wiring** — UI → route → API → service → schema → persistence.
6. **Cross-check docs & design** — promised vs. implemented vs. wired vs. broken.
7. **Assess tests** — what they actually prove; the highest-value gaps.

**Output → Gate 2 (the verdict):** the report must answer, up front, *can a
brand-new user reach the core feature?*, and it must carry a verified
environment-provisioning attestation. No attestation → no first-run verdict.

**Design stance:** audit-only by default (no source changes); evidence-backed
findings only (no "some buttons don't work"); the agent reads code as the source
of truth and drives the running app as the behavior of record.

---

## 5. Operating protocol (what the agent does, step by step)

The skill instructs the agent through the seven phases above. A few rules govern
*how*, not just *what*:

- **Construct states deliberately — don't wait to stumble on them.** Force
  loading / empty / error / not-configured states by stopping the dependency,
  clearing the data store, removing the license, or disconnecting the network.
- **Evidence per finding.** Route/screen, element, expected, actual, evidence
  (screenshot/trace/console/network/a11y/code ref), likely cause, suggested fix,
  suggested test.
- **Classify, don't hand-wave.** Each promised feature is implemented-and-working,
  partially wired, broken, in-code-but-missing-from-UI, in-UI-but-unsupported,
  documented-but-not-implemented, or ambiguous.
- **A blocker that can't run the app** is documented, and the audit continues as
  static analysis — and says so plainly.

---

## 6. The report

The skill ships a report template (`skill/walkthrough/references/report-template.md`).
Its sections:

1. **Verdict** — honest, up front, including the first-run verdict.
2. **Environment provisioning — verified** — the attestation table: what was
   clean/absent and *how it was confirmed*; isolation verified yes/no; first-run
   coverage VALID/INVALID. **This gates the first-run verdict.**
3. **Zero-state / first-run** — the new-user experience and the provisioning
   matrix actually walked.
4. **Product model** — what it's supposed to be.
5. **Bring-up notes** — how it was run; every blocker and friction.
6. **Findings** — numbered, evidence-backed.
7. **Docs & design cross-check.**
8. **Test assessment** — and the highest-value tests to add.
9. **Wiring map** (optional).

A sign-off checklist at the end enforces the first-run gates before the audit can
be called done.

---

## 7. Requirements, runtime support, and honest limits

**Requirements**

- An agent that loads skills and can run **Playwright** and read your repo.
- A locally runnable app (or the skill falls back to static analysis and labels it
  as such).

**Runtime support — read this honestly.** The skill is written for and verified
against **Claude Code** and **Codex**. The *methodology* is agent-agnostic, but the
phrasing assumes an agent with Playwright + filesystem access; another runtime may
need light adaptation. Don't assume drop-in portability to a runtime that can't
drive a browser or read the repo.

**Limits**

- It is **guidance the agent follows**, not a mechanical gate. It is written to make
  the first-run pass mandatory, to require a *verified* attestation, and to
  disqualify a provisioned environment — the strongest a skill can be — but it
  ultimately relies on the agent executing it faithfully. (A mechanical "no pass
  without an attestation file" enforcement would be a separate harness.)
- It audits; it does not fix. Switch it to repair mode explicitly if you want
  changes.
- It is only as good as the states it can construct. A dependency it cannot remove,
  or an app it cannot run, is reported as a coverage gap rather than silently
  skipped.

---

## 8. FAQ

**Does it work for projects with no external dependency?** Yes. The
dependency-absent axis simply doesn't apply, but the first-run, empty-data, and
onboarding states still do — and those exist in almost every product.

**Will it change my code?** No, not in audit mode. It creates only temporary audit
artifacts, kept separate from your source.

**Why "first run" if it's a full audit?** Because the first-run guarantee is the
part everyone else skips and the reason this exists. The rest — wiring, docs, tests
— is the thorough audit you'd expect; the first-run discipline is what makes it
trustworthy for *new users*, not just the dev who built it.
