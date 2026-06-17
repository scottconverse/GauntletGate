---
name: walkthrough
description: Perform a comprehensive Playwright-driven walkthrough and interface wiring audit after UI/UX implementation is complete. Use when Codex is asked to do a complete UI walkthrough, product walkthrough, post-design audit, interface wiring audit, Playwright exploration, readiness review, or cross-check of a frontend against docs, specs, code, tests, routes, APIs, backend behavior, and persistence.
---

# Walkthrough

## Purpose

Audit a finished or nearly finished product UI as a real interface, not as a shallow smoke test. Determine whether the product works as promised, whether the UI is fully wired to the underlying system, and where the implementation diverges from docs, design, code, tests, or user expectations.

Use Playwright for runtime exploration and evidence capture. Use repository reading for source-of-truth comparison.

## Operating Mode

Default to audit mode.

- Do not modify product source code.
- Do not fix bugs unless the user explicitly switches from audit mode to repair mode.
- Create temporary audit artifacts only when useful for investigation, and keep them clearly separated from product code.
- Prefer read-only inspection, local app execution, Playwright traces/screenshots/logs, accessibility snapshots, network inspection, and code references.
- If the app cannot run, document the blocker and continue with static analysis of code, docs, routes, and tests.

## First-run reality — the non-negotiable rule

A walkthrough that only observes whatever state the machine happens to be in is not a walkthrough — it is a tour of the developer's already-working setup. **The worst defects for real users live in states a dev box never shows: the first run, with external dependencies absent, with empty data.** Catching those is the whole point.

This rule exists because of a real miss: a product was reported "near-clean (1 Minor)" while a brand-new user hit an immediate dead-end — the core feature was disabled and the setup step told the user to go install a dependency themselves. The walkthrough missed it for two reasons: (1) it ran on an already-provisioned dev box (the AI dependency installed, running, models pulled, settings configured), so the dependency-absent onboarding flow was never on screen; and (2) the "clean profile" isolation silently failed and nobody verified it — the supposedly clean run secretly read the real provisioned profile.

Two hard rules follow:

1. **Construct and VERIFY the true first-run / zero / dependency-absent state — never settle for the convenient one.** Deliberately build the new-user reality and prove you are in it. Observing a working dev environment tells you nothing about first-run UX.
2. **An already-provisioned environment is DISQUALIFYING for first-run findings.** A dev machine — dependencies installed, models pulled, settings configured, data seeded, first-run flags long cleared — is the WORST place to judge first-run UX. If you cannot construct and verify a clean state, you **may not** report the product as first-run-clean: say so explicitly and mark first-run coverage **INVALID**.

If isolation cannot be verified — you cannot prove the app actually used the clean profile and that the dependency was truly absent — the run is **INVALID for first-run findings**. Report that plainly; do not let a convenient state masquerade as the first-run state.

## Workflow

### 1. Build The Product Model

Read enough of the repository to understand what the product is supposed to be before launching the app.

Review relevant README files, specs, PRDs, design notes, tickets, architecture docs, route definitions, navigation structure, frontend components, state management, API routes, backend services, schemas, models, persistence code, mock data, fixtures, seed scripts, environment setup, existing tests, and design references.

Establish:

- Product purpose
- User roles
- Primary and secondary workflows
- Expected screens, routes, modals, drawers, and states
- Backend or system capabilities
- What the UI appears to promise
- What the docs/spec/design explicitly promise or imply
- **Every external dependency and first-run gate** — model/inference server (e.g. Ollama), database, license/activation, cloud account, API key, network connectivity, hardware. For each, answer up front: *what does the product do when it is ABSENT or unconfigured, what does the in-product onboarding path tell the user to do, and can a new user actually reach the core feature by following it?* These are the states you will be required to construct and walk in step 3.

### 2. Bring Up The App

Derive setup from the repo itself. Identify dependency install, build, lint, typecheck, test, and dev-server commands from package files, scripts, docs, lockfiles, config, or existing CI.

Launch the app locally and run relevant existing tests where feasible. Capture setup issues, failed scripts, type errors, lint failures, build failures, flaky tests, missing environment variables, missing services, failed requests, or incomplete instructions.

**Verify the environment is what you think it is — before trusting any first-run observation.** This is not optional; a past run was invalidated precisely because it skipped this.

- **Prove your isolation actually took.** If you isolate state (a throwaway/clean profile, a temp `HOME`/`USERPROFILE`/`XDG_*`/app-data dir, a fresh container, a separate DB) — after launch, **assert the app actually wrote its config, data, and first-run markers into the isolated location, not the real one.** An env override that "looks set" but is silently ignored by the app (the exact trap that defeated a past run) must be caught here. If you can't confirm the app used the clean location, your "clean" state is fiction.
- **Probe the real dependency state — never assume it.** Actively query each external dependency (hit the model/inference server's API, connect to the DB, check for the license/credential file, test connectivity). Record present/absent, version, running/stopped — measured, not guessed.
- **Write it down as an attestation.** Record the verified environment in the report's "Environment provisioning — verified" section. **No attestation → no first-run verdict.**

### 3. Construct and walk the first-run / zero state and the provisioning matrix (MANDATORY)

Do this **before** the general exploration, and never skip it for a product that has any external dependency, onboarding flow, or empty-data state. Deliberately produce the states a real new user hits — do not wait to stumble onto them.

**Zero-state / first-run pass — drive the product as if freshly installed:**

- Fresh, **verified-isolated** profile; first-run flags unset; empty data store; **every external dependency ABSENT or unconfigured** (per step 1's list).
- Walk the onboarding/setup flow end to end, the empty/landing states, and — critically — **an attempt to use the core feature with nothing set up.**
- Judge the result as a new user would: does the product carry the user to a working state, or **dead-end** them? A disabled primary action, a "go install X yourself" instruction with no in-product help, a blank screen, or a silent failure on the core feature is a **first-run dead-end**. A core feature a new user cannot reach by following the in-product path is a **Blocker — not a Minor**.

**Provisioning matrix — walk the combinations, not just the convenient cell:**

Walk `{first-run vs returning}` × `{dependency present vs ABSENT}` × `{data empty vs populated}` × `{offline vs online}`. You need not cross every cell exhaustively, but **a product with an external dependency MUST be walked with that dependency ABSENT** (both first-run and returning) — that is the new-user reality where dead-ends live. State exactly which cells you covered and which you did not.

**Construct each state deliberately — don't hope to see it:**

Force loading, empty, error, and not-configured states rather than waiting for them: stop or kill the dependency (dead backend, killed model server), clear the data store or point the app at an empty one, remove the license/credential, throttle or disconnect the network, reset the first-run flags. For each constructed state, record what the UI actually did (guided / degraded gracefully / dead-ended / errored silently).

### 4. Explore With Playwright

Walk the running app as both a real user and adversarial QA reviewer.

Cover:

- All primary routes
- All documented workflows
- All visible navigation paths
- All state-changing actions
- Forms and validation paths
- Modals, drawers, menus, tabs, accordions, and wizards
- Settings, save/cancel, import/export, upload/download, create/update/delete flows
- Empty, loading, error, success, and disabled states where reachable
- Back/forward navigation
- Refresh/reload behavior
- Desktop and mobile-sized viewport behavior

Click every meaningful visible interactive element on each audited screen. For repeated UI patterns, audit representative examples and note the pattern scope.

Do not only test happy paths. Try realistic alternate paths, invalid inputs, empty inputs, interrupted flows, repeated submissions, stale navigation, and edge cases.

### 5. Cross-Check Wiring

For each screen and workflow, compare what the UI suggests against what the system actually does.

Look for:

- Buttons or controls that do nothing
- Clickable-looking elements that are inert
- Controls wired to the wrong behavior
- Broken links or dead routes
- Placeholder pages presented as finished features
- Cosmetic UI disconnected from real data or behavior
- Mocked, hardcoded, or stubbed flows presented as real
- Forms that accept invalid data or reject valid data
- Missing validation or persistence
- State-changing actions that do not affect expected system state
- Frontend/backend mismatches
- Backend capabilities not surfaced in the UI
- UI features unsupported by backend/system behavior
- Broken route guards, auth assumptions, or permission flows
- Console errors, failed requests, hydration errors, and broken assets

For important workflows, inspect the relevant route, component, state, API call, service function, schema, persistence layer, and tests.

### 6. Cross-Check Docs And Design

Compare implementation against docs, specs, product intent, and design references.

Classify each promised or implied feature as:

- Implemented and working
- Implemented but partially wired
- Implemented but broken
- Present in code but missing from the UI
- Present in UI but unsupported by the system
- Documented but not implemented
- Ambiguous or underspecified

Call out mismatches in labels, flows, information architecture, visual states, and product purpose.

### 7. Assess Tests

Review existing tests and identify what they prove.

Call out workflows with no coverage, render-only tests, tests that pass despite broken wiring, missing Playwright coverage, missing API/backend coverage for UI-critical flows, missing persistence tests, missing validation tests, and missing error/empty/loading/permission-state tests.

Recommend high-value tests that would catch the most serious issues found.

## Evidence Standards

Findings must be specific and evidence-backed. Avoid vague statements such as "some buttons do not work."

For each finding, identify the route/screen, element/workflow, expected behavior, actual behavior, evidence, likely cause, suggested fix, and suggested test coverage.

Use screenshots, traces, console logs, network logs, accessibility snapshots, DOM inspection, docs/spec references, code references, and test references where helpful.

## Report

Create the audit report at the path requested by the user. If no path is provided, use `AUDIT_PLAYWRIGHT_INTERFACE_WIRING.md` in the target repo.

Use `references/report-template.md` as the report structure. Adapt headings only when the project context makes a different structure clearer. The template's **"Environment provisioning — verified"** attestation and **"Zero-state / first-run"** sections are **required, not optional** — a report missing either is incomplete.

The audit is complete only when the report gives a clear, concrete picture of where the UI is finished, where it is cosmetic, where it is broken, and where it diverges from the product's docs, design, code, tests, or system capabilities.

**Before you call it done, this gate must pass — answer each explicitly in the report:**

1. Did I construct and **verify** a true first-run / zero / dependency-absent state (isolation proven to have taken; dependency state probed, not assumed)? If not, first-run coverage is **INVALID** and the verdict must say so — never report "clean" off an unverified or already-provisioned environment.
2. Did I attempt the **core feature as a brand-new user with nothing set up**, and report whether they reach a working state or hit a dead-end? A first-run dead-end on the core feature is a **Blocker**.
3. Did I walk the product with each external dependency **ABSENT**, not just present?
4. Is the environment I judged actually the new-user environment — or just the convenient dev-box state? If the latter, the run does not support a first-run verdict.

If any answer is "no" or "couldn't verify," say so loudly in the verdict and mark the affected coverage INVALID. A product that dead-ends a new user must never be reportable as near-clean.
