# Interface Wiring & Walkthrough Audit — <product / area>

**Date:** <YYYY-MM-DD>
**Auditor:** <name / agent>
**Build / commit:** <sha or version>
**App URL / how run:** <local dev server, port, command>
**Environment:** <first-run-clean vs already-provisioned; was a verified clean state used? — full attestation in §2>
**Scope:** <which routes/workflows/roles were walked; what was out of scope>

---

## 1. Verdict (read this first)

2–5 sentences, honest. Is the product as-promised, partly wired, or mostly cosmetic? What's the single most important thing the reader should know? **State first-run reachability explicitly: can a brand-new user with nothing set up reach the core feature?** If first-run was not verified on a true clean state, say so here and mark first-run coverage **INVALID** — do not imply "clean."

**First-run verdict:** <Reaches core feature ✅ / Dead-ends a new user ❌ / NOT VERIFIED — see §2>

**Readiness by area:**

| Area / screen | Finished | Partially wired | Cosmetic only | Broken |
|---|---|---|---|---|
| <e.g. Login> | ✅ |  |  |  |
| <e.g. Dashboard> |  | ⚠️ |  |  |
| ... |  |  |  | ❌ |

**Severity roll-up:** Blocker N · Critical N · Major N · Minor N · Nit N

---

## 2. Environment provisioning — verified (attestation)

> This section **gates the first-run verdict.** If you cannot fill it with *verified* facts (not assumptions), first-run coverage is **INVALID** and §1 must say so. An already-provisioned environment is disqualifying for first-run findings.

| What | State used | How it was VERIFIED — not assumed |
|---|---|---|
| Profile / `HOME` / `USERPROFILE` / app-data isolation | <clean temp dir / fresh container / real profile> | <e.g. confirmed the app wrote its config + first-run marker into the isolated path; quote the path it actually used> |
| First-run flags | <unset / already cleared> | <how confirmed> |
| External dependency: <name, e.g. Ollama> | <ABSENT / present vX, running / stopped> | <how probed — API call, process check, file check> |
| External dependency: <name> | <...> | <...> |
| Data store | <empty / populated> | <how confirmed> |
| Network | <online / offline / throttled> | <how set> |

**Isolation verified?** <YES — the app provably used the clean state / NO — could not confirm>
**→ First-run coverage:** <VALID / **INVALID** (and why)>

If isolation could not be verified, treat **no** first-run observation as trustworthy — the run may have silently read a provisioned environment. Say so in §1.

---

## 3. Zero-state / first-run

The new-user experience, walked **deliberately** — not whatever state the dev box happened to be in.

- **Onboarding / setup flow:** <what a brand-new user sees and is told to do; does it carry them to a working state end to end?>
- **Empty / landing states:** <what renders with no data>
- **Core feature attempted with nothing set up:** <result — reaches a working state, OR **DEAD-END**: disabled primary action / "go install X yourself" with no in-product help / blank screen / silent failure>. **A first-run dead-end on the core feature is a Blocker** — cross-reference its finding id.

**Provisioning matrix walked** (`{first-run vs returning} × {dependency present vs ABSENT} × {data empty vs populated} × {offline vs online}` — the dependency-ABSENT row is mandatory):

| first-run / returning | dependency | data | network | Result (guided / degraded / dead-end / silent error) |
|---|---|---|---|---|
| first-run | **ABSENT** | empty | online | <...> |
| first-run | present | empty | online | <...> |
| returning | ABSENT | populated | online | <...> |
| <other cells walked> | | | | |

**Cells deliberately not covered (and why):** <be explicit — silence is not coverage>

---

## 4. Product model (what it's supposed to be)

- **Purpose:** <one line>
- **User roles:** <list>
- **Primary workflows:** <list>
- **Secondary workflows:** <list>
- **Expected screens/routes/states:** <list>
- **What the UI promises vs. what docs/spec/design promise:** <note any gap in promises before even running>

---

## 5. Bring-up notes

How the app was set up and run, derived from the repo. List every blocker, failed script, missing env var, missing service, type/lint/build failure, and any place the documented setup was wrong or incomplete.

- Install/build/run commands used: <...>
- Existing tests run + result: <...>
- Blockers / friction: <...>

---

## 6. Findings

Number every finding. One block each. Be specific and evidence-backed — never "some buttons don't work."

### F-001 — <severity> — <one-line title>
- **Route / screen:** <path>
- **Element / workflow:** <what was exercised>
- **Expected:** <what the UI/docs imply should happen>
- **Actual:** <what happened>
- **Evidence:** <screenshot/trace/console/network/a11y-snapshot path or quote; file:line for code>
- **Likely cause:** <component / handler / API / state / schema>
- **Suggested fix:** <concrete next step>
- **Suggested test:** <the test that would catch this>

### F-002 — ...

(Repeat. Group by screen/workflow if that reads better.)

---

## 7. Docs & design cross-check

Classify each promised or implied feature.

| Feature / promise | Status | Evidence / note |
|---|---|---|
| <feature> | Implemented & working | <...> |
| <feature> | Implemented but partially wired | <...> |
| <feature> | Implemented but broken | <...> |
| <feature> | In code, missing from UI | <...> |
| <feature> | In UI, unsupported by system | <...> |
| <feature> | Documented, not implemented | <...> |
| <feature> | Ambiguous / underspecified | <...> |

Also note mismatches in labels, flows, information architecture, visual states, and overall product purpose.

---

## 8. Test assessment

- **What the existing tests actually prove:** <...>
- **Render-only / pass-despite-broken-wiring tests:** <...>
- **Coverage gaps:** workflows with no coverage, missing Playwright/API/persistence/validation, missing error/empty/loading/permission-state tests.

**Highest-value tests to add (ranked):**
1. <test> — catches <which finding>
2. ...

---

## 9. Wiring map (optional)

For the most important workflows, the chain that was traced: UI element → route/component → state → API call → service → schema → persistence → test. Note where the chain breaks.

| Workflow | UI → Route → API → Service → Persistence | Breaks at |
|---|---|---|---|
| <...> | <...> | <...> |

---

## Sign-off checklist

- [ ] **Environment provisioning (§2) is attested with *verified* facts** — isolation proven to have taken; every external dependency probed (not assumed). If not verifiable, first-run coverage is marked INVALID.
- [ ] **A true first-run / zero / dependency-ABSENT state was constructed and walked (§3)** — not the convenient already-provisioned dev-box state.
- [ ] **The core feature was attempted as a brand-new user with nothing set up**, and the result (reaches working state vs. dead-end) is reported. A first-run dead-end on the core feature is filed as a **Blocker**.
- [ ] The product was walked with each external dependency **ABSENT**, not only present.
- [ ] Every primary route and documented workflow was walked (or the blocker is documented).
- [ ] Each finding has route, element, expected, actual, evidence, cause, fix, and test.
- [ ] Cosmetic-vs-finished-vs-broken is explicit per area.
- [ ] Docs/design divergences are classified.
- [ ] Test gaps and the highest-value additions are listed.
- [ ] The verdict gives a clear, concrete readiness picture.
