# Streakly Comeback Screen — Spec Readiness (Raj Role-Play Session)

*2026-09-16. Sources reviewed: `project.md`, `strategy.md`, `docs/decision-brief.md`, `03-build/pm-brief.md`, `03-build/prototype/`, `04-team/stakeholders/raj.md`. Conducted as a role-play with Claude playing Raj against Raj's documented profile, to pressure-test the spec before it goes to the real Raj. Decisions below were made live in that conversation — they are Eric's calls, not yet confirmed by the real Raj.*

## 1. Spec Readiness Summary

### What was already solid going in

- The problem framing and data: the churn-doubling stat for users who miss 2 days, and Raj's own prior confirmation that the Comeback screen concept is "technically doable" with existing systems (`project.md`, `docs/decision-brief.md`).
- The prototype had already been through two rounds of persona testing (`change_log.md`) and had already caught and fixed a real defect (the "no reset needed" claim contradicting a "Day 1" reset) before this conversation started.
- The core UX intent (reassurance + a concrete next step, not a generic "keep going") was clear and consistent across every document.

### What needed work before this conversation

- **Which scope, exactly.** `project.md` and `docs/decision-brief.md` describe a three-part Comeback screen (best-streak stat, 60-second comeback lesson, one-tap streak-freeze). `03-build/pm-brief.md` and the actual prototype only build the welcome-message-plus-pass piece. Nothing stated which one was the sprint target.
- **Which number drives "continue where you left off."** The prototype reused the best-streak stat as a stand-in; `pm-brief.md` explicitly flagged that this might not match the actual pre-break streak length, and no doc resolved it.
- **How the continuation would actually be built.** No document said whether this reads from a separately tracked value or requires changing the nightly streak-reset job — a meaningful difference for risk and rollback.
- **Edge cases.** Nothing addressed what a user with no prior streak sees, or whether the screen even applies to them.
- **Rollback/safety plan** for touching the reset job — not mentioned anywhere.

### What got resolved in this conversation

| Item | Resolution |
|------|-----------|
| Scope | Welcome-message + pass version only. No 60-second comeback lesson in this build. |
| Data model | Track both `pre-break streak` and `best streak` as separate values. The continuation counter uses **pre-break streak**; best streak stays a separate "you can beat it" stat. |
| Implementation approach | Modify the existing nightly reset job to capture pre-break streak, rather than building a separate tracking pipeline. |
| Edge case: never-streaked user | Not applicable — screen requires pre-break streak > 0 to show at all. |
| Rollback / safety | A feature flag on the modified reset-job logic, so it can be disabled in production without a deploy. Confirmed as "on the table." |

### What's still open (explicitly deferred, not blocking sizing)

- Freeze/pass frequency and cooldown rule (how often it can be used) — still needs a first-pass answer at the `03-build/triad-session.md` working session.
- Free vs. paywalled freeze, and the streak-intensity trade-off — both already correctly parked as Marcus-level decisions in `docs/decision-brief.md`.
- Targeting logic beyond the "pre-break streak > 0" gate (e.g., timing/frequency of when the screen surfaces).
- The actual eng size/timeline number itself — this conversation cleared the blockers *to* sizing; it didn't produce the size.

## 2. Rewrite — Unclear Sections, Now Specified

*Replaces the relevant bullets in `03-build/pm-brief.md`'s "Notes / open items" section (lines 21–22).*

> **Data model.** The Comeback screen requires two separately tracked values per user: `bestStreak` (all-time longest streak, already used for the "you can beat it" stat) and `preBreakStreak` (the streak length at the moment it broke). These are not the same number and must not be conflated — `bestStreak` is historical and does not change on a break; `preBreakStreak` is what the "continue where you left off" counter resumes from.
>
> **Where `preBreakStreak` is written.** Captured by modifying the existing nightly streak-reset job at the moment a streak would otherwise reset to zero, rather than a separate tracking system. This change ships behind a feature flag so it can be disabled in production without a deploy if the write logic misbehaves.
>
> **Display gating.** The Comeback screen only renders when `preBreakStreak > 0`. Users with no prior streak do not see this screen — this is an explicit acceptance criterion, not an assumed default.
>
> **Still open, not blocking this build:** freeze/pass frequency and duration rules; whether/how often a user can trigger this screen more than once; free vs. paywalled framing. These are tracked separately in `strategy.md` and `docs/decision-brief.md`'s Decisions Needed and are not required to size or start this sprint.

## 3. Async Message to Send Raj (Before Sprint Kickoff)

> Hey Raj — before kickoff, confirming scope on the Comeback screen so we're sizing the same thing:
>
> - **Scope:** welcome-message + pass version only. No 60-second comeback lesson in this pass.
> - **Data:** two separate fields — `bestStreak` (unchanged, all-time) and `preBreakStreak` (new). The "continue where you left off" counter resumes from `preBreakStreak`, not `bestStreak`.
> - **Implementation:** `preBreakStreak` gets written by modifying the nightly reset job, behind a feature flag so we can kill it without a deploy.
> - **Gating:** screen only shows if `preBreakStreak > 0` — no prior streak means no screen, no special-cased empty state needed.
> - **Explicitly not in this sprint:** freeze/pass frequency rule, monetization call — both still open, tracked separately, not blocking your estimate.
>
> Reply here if anything above doesn't match what you'd actually build — otherwise I'll take this as confirmed scope for sizing.
