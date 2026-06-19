# GitHub Discussions — seed posts

Ready-to-post seed threads for the repo's Discussions tab. Create the categories
(Announcements, Q&A, Show and tell, Ideas) under *Settings → Features →
Discussions*, then paste each post into its category.

---

## 📣 Announcements — "GauntletGate 0.1.0: an adversarial stage-gate your product must survive to advance"

Most quality checks run on the machine the product was built on — database seeded,
dependencies running, settings filled in. So they audit a product that already
works, and wave it through. GauntletGate is built to *block* advancement until the
product is genuinely ready — including for a brand-new user.

**GauntletGate 0.1.0** is one gate with three lanes (a skill for Codex Desktop and
CoWork/Claude-style agents):

- `gauntletgate lite` — a fast single-pass on a change/slice (first-run-aware).
- `gauntletgate walkthrough` — a first-run-truth + interface-wiring runtime audit
  that *verifies* the real first-run state and walks the product with dependencies
  absent.
- `gauntletgate full` — a 5-role adversarial deep audit that consumes the
  walkthrough report instead of re-walking the UI.
- `gauntletgate all` (the default) — all three, then one verdict.

**Only the full run can say CLEAR TO ADVANCE** (0 Blocker / 0 Critical, first-run
valid and reachable). Any partial run is labeled a PARTIAL CHECK — a cheap run can't
masquerade as the gate. It was born from a real miss: a product reported "near-clean"
while a new user hit an instant dead-end, because the check ran on a provisioned dev
box whose isolation had silently failed.

- Install + docs: see the README and the [manual](MANUAL.md).
- It's a skill, not a binary — honest about that in the README.

---

## 🙋 Q&A — "Can a `lite` run clear a stage? / no external dependency?"

- **Can `lite` greenlight a stage?** No. Only `all` can be CLEAR TO ADVANCE;
  everything else is a PARTIAL CHECK by design — so a quick check can't be mistaken
  for the full gate.
- **My product has no external dependency.** The dependency-absent axis just doesn't
  apply; first-run, empty-data, and onboarding states still do.
- **Will it change my code?** No, not in audit mode. Repair mode is opt-in.
- **What does `full` cost?** It fans out 5 role subagents (billed, multi-agent
  opt-in). `lite` and `walkthrough` are light and run inline.
- **Which agents?** Written for and verified against Codex Desktop and
  CoWork/Claude-style agents; assumes Playwright + repo access.

---

## 🙌 Show and tell — "What did the gate block?"

Post the thing that *almost* advanced. The interesting ones:

- A first-run dead-end a dev box was hiding (disabled core action, "go install X
  yourself," blank screen).
- A "clean" run that turned out to be reading a provisioned profile — and how the
  attestation caught it.
- A cross-role finding the full lane surfaced (a security bug with no test and no
  doc).

Screenshots of a `⛔ DO NOT ADVANCE` verdict especially welcome.

---

## 💡 Ideas — "What would make the gate stronger?"

On the table:

- A **mechanical gate**: make it impossible to emit CLEAR TO ADVANCE without a
  verified environment attestation file present (today it's strong guidance, not a
  hard lock).
- **CI integration**: run `lite` on every PR, `all` at stage boundaries, and post the
  verdict as a status check.
- **Per-stack isolation + dependency-absent recipes** contributed by the community.
- **A persisted gate ledger** (which stages a build cleared, when, with what verdict).

File an Idea with what you'd want.
