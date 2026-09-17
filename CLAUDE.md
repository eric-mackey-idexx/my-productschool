# CLAUDE.md — Persistent Memory

> The file Claude Code reads at the start of every session. Short, true, current — the difference between Claude building blind and building with context.

## The Product

Working scenario: the **Streakly Comeback experience** — recovering Day-7 retention for Streakly, a consumer habit + micro-learning app whose Day-7 retention slipped from 48% to 39% after a v2 redesign.

**Status as of 2026-09-17:** past discovery. A prototype exists and has been through two rounds of persona testing, a real quantitative pilot (week-5 A/B test) has run and shown a Day-7 lift, and that result has been pressure-tested (sample size, confidence interval, a full-test design) rather than taken at face value. A recommendation memo and a 6-slide quarterly-review deck exist. What's still open: eng sizing for a larger validation test, the freeze-rule and monetization decisions, and target metric values — see "Open Threads" below.

## Where Things Live

The numbered module folders (`01-orient/` … `06-systems/`) are the original course scaffold; the real work outgrew them and lives in these places instead — check here before guessing a path:

| Folder / File | What's actually in it |
|---|---|
| `project.md`, `strategy.md` | Original discovery notes, hypothesis, open questions from the Slack thread |
| `research/nps-analysis.md` | Real user quotes and themes (this is the "interview synthesis" — no file by that literal name exists) |
| `research/competitive-matrix.md` | Structured competitor research (no `competitive-reddit.md` exists — Reddit access failed and was never substituted) |
| `docs/decision-brief.md` | What was recommended to Marcus, pre-pilot |
| `docs/prd.md` | The PRD for Raj + Lena |
| `docs/recommendation-memo.md` | The pilot results memo, with Marcus's pressure-test questions |
| `docs/presentation.md` / `presentation-notes.md` / `*.pptx` | The 6-slide quarterly-review deck and its narrative/speaker notes |
| `03-build/pm-brief.md`, `hypothesis.md`, `triad-session.md` | Build-phase docs: the prototype's brief, the draft hypothesis, the Raj/Lena working-session agenda |
| `03-build/prototype/` | The actual click-through HTML prototype |
| `04-team/stakeholders/*.md` | Raj, Lena, Marcus profiles — sourced facts vs. default-profile fill are marked separately in each file |
| `04-team/spec-readiness.md`, `design-review.md`, `qa-checklist.md`, `codebase-summary.md` | Spec pressure-testing, design review, QA pass, and a codebase tour (using Habitica as a real-code stand-in, since Streakly has no actual codebase) |
| `data/*.csv`, `metric-findings.md`, `metric-diagnosis.md`, `experiment-design.md` | The real quantitative pilot data and every analysis run against it |
| `change_log.md` | Chronological log of everything built and why — check here for history before re-deriving something |
| `skills/weekly-status.md` | Reusable skill: raw notes → calibrated status updates for the team vs. leadership |

## How I Want Claude to Work With Me

- **Interview first:** ask clarifying questions before building.
- **Tone:** Direct and concise.
- **Defaults:**
  - Save new artifacts into the folder that matches its audience per the map above — `docs/` for external-facing deliverables, `03-build/` for prototype/build work, `04-team/` for stakeholder-facing collaboration docs, `data/` for anything touching the CSVs — not everything into `project.md`.
  - Before reading a file someone names, verify it exists. Wrong paths have been the single most common error in this project — check, and if it's missing or moved, say so plainly and use the real file instead of guessing at its contents.
  - Treat source material (threads, docs, data) as the single source of truth.
  - Flag open/unresolved items rather than filling gaps with assumptions.
  - Skeleton/draft-level output, not polished, unless asked for a finished deliverable.
  - Proactively prompt to save conversation content into the right file — don't wait to be asked.
- **Never:**
  - Invent details, data, or decisions not sourced from real threads/docs.
  - Skip the interview-first step before creating files or writing code.
  - Present proposed/unconfirmed items (goals, metrics, targets) as agreed decisions.
  - Overwrite or rewrite existing content without confirming first.
  - Present a role-played stakeholder response (Raj/Lena/Marcus persona simulations against their profile docs) as if it were the real person's actual sign-off — several documents in this project are Claude-role-played pressure tests, not real approvals. Say so.

## Open Threads (don't re-derive these — they're genuinely still open)

- Freeze/pass frequency and cooldown rule — undefined anywhere.
- Free vs. paywalled streak-freeze, and the streak-intensity trade-off — Marcus's calls, not yet made.
- Target metric values and dates — flagged as missing in three separate docs, never set.
- Eng sizing for the larger validation test — Raj's estimate doesn't exist yet.
- 8 files (see `workspace-audit.md`) exist locally but aren't committed to git as of 2026-09-17.

## Glossary (my product's words)

| Term | Meaning |
|------|---------|
| Comeback screen | The welcome-back screen shown after a streak breaks — best-streak stat, personalized re-entry, streak-connect pass — replacing the old cold reset |
| Best streak | A user's all-time longest streak — historical, doesn't change on a break |
| Pre-break streak | The streak length at the moment it broke — this, not best streak, is what the "continue where you left off" counter resumes from |
| The "pass" | Shorthand for the streak-connect/freeze mechanic on the Comeback screen; its actual duration/frequency rule is still undefined |
| Persona testing (Round 1 / Round 2) | Simulated user-reaction testing against Priya, Tom, and Amara — personas, not real interview subjects |
| Triad session | The working session format bringing Eric + Raj (eng) + Lena (design) together on the prototype |
