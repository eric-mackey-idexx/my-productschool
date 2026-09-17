# Streakly Comeback Screen — Design Review (Lena Role-Play Session)

*2026-09-16. Sources reviewed: `03-build/prototype/index.html`, `04-team/spec-readiness.md`, `04-team/stakeholders/lena.md`. Note: `02-research/interview-synthesis.md` does not exist in this repo. All Priya/Tom/Amara material below is simulated persona testing (`change_log.md`, `03-build/pm-brief.md` — Round 1 & 2), not real user interviews. That distinction is itself one of this review's findings, not a footnote to skip.*

## 1. Prototype vs. Persona Evidence

**Addressed well:**
- Relevant, non-generic stats per user — Priya (417 days/Lesson 301), Tom (12 days/Lesson 12), Amara (3 days/Lesson 3) each see numbers matching their own profile, resolving Amara's Round 1 complaint that the screen "doesn't even know me."
- Reassuring, non-punishing tone — addressed for Amara specifically, whose profile is most sensitive to punishing/nagging tone.
- Promise-behavior consistency — Tom's Round 1 objection (the app "lying" by promising no reset, then showing Day 1) was fixed by making the day count actually continue.

**Not yet addressed:**
- **No real next action after the confirmation screen.** Stops at "Day 15" + a prototype-only "Restart demo" button. None of the three personas have reacted to an actual re-engagement step, because none exists yet.
- **Freeze/pass durability.** Tom's Round 2 objection — one-time trick vs. real ongoing rule — is still open.
- **Whether personalization is real.** Priya's Round 2 question (demo toggle vs. live data) isn't answered anywhere the user can see, even though `spec-readiness.md` now answers it at the data-model level.
- **Repeated/nagging exposure.** Amara's core sensitivity (streak pressure generally, not just one screen) has never been tested against recurrence.

## 2. Design Review — Questions and Resolutions

| Lena's question | Resolution reached |
|---|---|
| What does the user do after this screen? | Build Lena's original 60-second comeback lesson into the **next round of testing** (not committed to build yet) — test with Tom specifically, since reassurance alone didn't satisfy him. If it resonates, add to the next iteration. |
| Is any of this from real users? | No — confirmed personas, not real interviews. Next step: survey **users who have actually broken a streak in week 1** (not clients generally), incentivized by influence over the roadmap. Real-user validation still needs to happen before this is called "validated," not just built. |
| How do we make a broken streak feel forgiving instead of a guilt trip, for real? | Commit to including some freeze/pass mechanic — competitive research (Duolingo's paywalled Streak Freeze) and NPS demand (2 of 10 users asked for it) support inclusion. The specific rule (duration, frequency, free vs. paywalled) is explicitly Marcus's decision (`docs/decision-brief.md`), not resolved here. |

## 3. Single Highest-Impact Change for Week-1 Retention

**Build the 60-second comeback lesson as the destination after the confirmation screen.**

Why this over the freeze-rule question: the freeze mechanic mainly affects whether a user *trusts* the app across a *future* break — a repeat-engagement, longer-horizon concern. The comeback lesson is what converts this week's break into this week's actual re-engaged action. The job to be done (`pm-brief.md`) is "make it easy... to start a streak again" — starting requires a completed action, not a feeling. Right now every fix so far (accurate stats, honest copy, continued day count) makes the screen feel better, but the flow still dead-ends at a confetti screen with nothing to actually do. Without a real next step, none of the reassurance work converts into the thing Day-7 retention actually measures: continued use.

## 4. Product Decision vs. What Lena Should Own

**Product decisions (Marcus / Eric, not Lena's call):**
- Free vs. paywalled freeze, and the specific freeze duration/frequency rule (`docs/decision-brief.md`, `04-team/spec-readiness.md`).
- The streak-intensity trade-off (softening the reset vs. what motivates high-stakes streak owners).
- Whether/when the comeback lesson graduates from "next test" to "next sprint," based on results.
- Budget/expectation-setting for the client research incentive (roadmap influence is a commitment, not just a survey perk).

**Lena's to own:**
- The actual UX/interaction design of the comeback lesson (content shape, length, feel) once testing confirms it's worth building.
- Translating whatever freeze rule Marcus sets into copy/UI that reads as forgiving, not transactional or guilt-inducing — her job starts only after his decision lands.
- Design-system alignment for the whole screen (already flagged in `03-build/pm-brief.md` and `03-build/triad-session.md` as unresolved against real Streakly UI).
- The research script/prompts for the next round of real-user testing — what to ask, not who to recruit or how to incentivize them.
