# Workspace Audit — Streakly Comeback Project

*2026-09-17. Based on the full repo tree, `git status`, and the actual content of every file, not just filenames.*

## 1. What's Missing (for Claude to be more useful next session)

**No file map anywhere.** This is the single biggest recurring friction point in this whole project — by count, at least 6 separate requests this session referenced a path that didn't exist: `docs/hypothesis.md` (real: `03-build/hypothesis.md`), `stakeholders/*.md` (real: `04-team/stakeholders/*.md`, wrong twice on two different days), `research/interview-synthesis.md` and `research/competitive-reddit.md` (neither exists — `research/nps-analysis.md` is the real quotes/themes file), and `02-research/decision-brief.md` (real: `docs/decision-brief.md`). Every one of these cost a round-trip to verify and correct. `CLAUDE.md` had nowhere to look this up.

**The numbered module files (`01-orient/` through `06-systems/`) are still blank templates, even though the work they're asking for already exists elsewhere.** Concretely:
- `03-build/build.md`'s "Prototype + Iteration Log" table (Round | What changed | What we learned) is still `___ | ___` — but Round 1 and Round 2 are fully logged in `change_log.md`.
- `03-build/build.md`'s "Hypothesis Worth Shipping" template is unfilled — but the real hypothesis is written out in `03-build/hypothesis.md`.
- `03-build/build.md`'s "Triad Session Plan" section is empty — but `03-build/triad-session.md` is a complete agenda.
- `04-team/collaboration.md`'s "Codebase Tour + Spec Readiness" section is empty — but `04-team/codebase-summary.md` and `04-team/spec-readiness.md` both exist.
- `04-team/collaboration.md`'s "Design Review + QA" edge-case table is still `___ | ___ | ☐` — but `04-team/design-review.md` and `04-team/qa-checklist.md` cover this in full.
- `01-orient/orientation.md`, `02-research/research.md`, and `05-decide/decide.md` are all still template placeholders too.

None of the real work is missing — it all exists. What's missing is the two-line pointer in each module file saying "see X" so a new session (or a teammate) starting from the numbered folders — the workspace's own stated structure — doesn't conclude nothing has been done.

**8 files exist locally but were never committed.** `git status` shows: `data/experiment-design.md`, `data/metric-diagnosis.md`, `data/metric-findings.md`, `docs/prd.md`, `docs/presentation.md`, `docs/presentation-notes.md`, `docs/recommendation-memo.md`, `docs/streakly-comeback-quarterly-review.pptx`, plus a modified `skills/weekly-status.md`. None of this is on GitHub. If a next session (or anyone else) checks the remote, or if this machine's local state is ever lost, this work doesn't exist anywhere else.

**A skill was built but never delivered.** Earlier this session, a `prd-writer` skill was drafted, tested against 3 eval cases (with results reviewed), but it still lives only in a temporary scratch directory outside this project — it was never packaged into a `.skill` file or saved anywhere durable. If it's worth keeping, it needs to be finished; if not, that's fine, but it shouldn't just be forgotten in temp space.

**`CLAUDE.md`'s own Glossary table is still empty** (`| ___ | ___ |`), despite the project having accumulated real, specific vocabulary (pre-break streak, best streak, the "pass," persona testing rounds) that a fresh session would benefit from on day one.

**No target metric values exist anywhere.** `docs/decision-brief.md`, `03-build/hypothesis.md`, and `docs/prd.md` all independently flag this as open — it's the same unresolved thread surfacing three times, never closed.

## 2. Reorganization to Reduce Friction

1. **Add a "Where Things Live" map to `CLAUDE.md`.** This alone would have prevented most of the wrong-path incidents above. See the updated `CLAUDE.md`.
2. **Cross-link the numbered module files to the real artifacts** rather than leaving them blank or deleting them — they're cheap to fix (one line each) and preserve the course structure's intent while fixing the "where's my Round 1 log" discoverability problem.
3. **State the three-way split explicitly**, since it already exists in practice but was never written down: `docs/` = external-facing deliverables (decision brief, PRD, recommendation memo, presentation), `03-build/` = prototype and build-phase working docs, `04-team/` = stakeholder-facing and collaboration artifacts (profiles, spec readiness, design review, QA, codebase tour), `data/` = quantitative pilot data and analysis, `research/` = qualitative/competitive research.
4. **Commit and push the 8 pending files** — recommended as a next action, not done automatically here since this task didn't ask for it.
5. **Decide the fate of the `prd-writer` skill** — finish and package it, or explicitly drop it, rather than leaving it half-built in scratch space where it'll be forgotten.
6. **Fill in the Glossary table** — done in the updated `CLAUDE.md`.

## 3. One Caveat Worth Repeating Here

A large share of this project's "stakeholder input" — Raj's and Lena's questions in the triad-session and PRD work, Marcus's pushback in the recommendation-memo review — was Claude role-playing against their documented profiles, not the real people. `04-team/spec-readiness.md`, `04-team/design-review.md`, and `docs/recommendation-memo.md` all say this explicitly, but it's easy for a fresh session to lose that distinction if it isn't restated. Carried into the updated `CLAUDE.md`.
