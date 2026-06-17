# GitHub Discussions — seed posts

Ready-to-post seed threads for the repo's Discussions tab. Create the categories
(Announcements, Q&A, Show and tell, Ideas) under *Settings → Features →
Discussions*, then paste each post into its category. (The maintainer can also
post these via `gh api graphql`.)

---

## 📣 Announcements — "FirstRunWalkthrough 0.1.0: a walkthrough audit that can't be fooled by a dev box"

Most "walkthroughs" run on the machine the product was built on — database seeded,
model server running, license activated, settings filled in, first-run flags long
cleared. So they audit a product that *already works*, and report it clean. The
single most important question — *can a brand-new user actually get started?* — is
the one a dev-box walkthrough is structurally blind to.

**FirstRunWalkthrough 0.1.0** is a skill (for Claude Code / Codex) that drives your
app with Playwright and reads your repo as the source of truth — and then does the
part everyone skips: it **constructs and verifies the real first-run state** (fresh
profile, empty data, dependencies *absent*), proves the app actually used that
clean state rather than a silently-ignored override, and walks the product with its
dependencies removed. A first-run dead-end on the core feature is a **Blocker**, and
an already-provisioned environment is **disqualified** from reporting "clean."

It was extracted from a real miss: a product reported "near-clean (1 Minor)" while a
new user hit an immediate dead-end, because the audit ran on a provisioned dev box
and its isolation had silently failed.

- Install + docs: see the README and the [manual](MANUAL.md).
- It's a skill, not a binary — honest about that in the README.

---

## 🙋 Q&A — "Does it work for products without an external dependency?"

Yes. The dependency-absent part of the matrix simply doesn't apply — but the
first-run, empty-data, and onboarding states still do, and those exist in almost
every product. The verdict still answers "can a brand-new user reach the core
feature?"

Other common questions worth seeding:

- **Will it change my code?** No, not in audit mode. It creates only temporary audit
  artifacts and keeps them away from your source. Repair mode is opt-in.
- **Which agents does it work with?** Written for and verified against Claude Code
  and Codex. The method is agent-agnostic but assumes Playwright + repo access.
- **What if my app can't run locally?** It documents the blocker and continues as
  static analysis — and says so, rather than pretending it walked the UI.

---

## 🙌 Show and tell — "What did your first-run pass catch?"

Post the dead-end your dev box was hiding. The interesting ones:

- A core action disabled with no in-product path to enable it.
- A "go install X yourself" step with no help, no link, no fallback.
- An onboarding flow that assumes a dependency is already running.
- A "clean" run that turned out to be reading a provisioned profile (and how you
  caught the isolation failure).

Screenshots of the verdict line *"Dead-ends a new user ❌"* especially welcome.

---

## 💡 Ideas — "What would make first-run auditing stronger?"

Some directions on the table:

- A **mechanical gate**: make it impossible to emit a "pass" without a verified
  environment-provisioning attestation file present (today the skill is strong
  guidance, but not a hard lock).
- **Recorded first-run traces** as shareable artifacts (the new-user journey as a
  replayable Playwright trace).
- **Per-platform isolation recipes** (clean profile / temp HOME / container / fresh
  DB) contributed for common stacks.
- A small **library of dependency-absent probes** (model server, DB, license,
  network) the skill can reuse.

What would you want? File an Idea.
