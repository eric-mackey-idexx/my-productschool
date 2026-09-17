---
name: weekly-status
description: Turn raw bullet-point week notes (Shipped/In Progress/Blockers) into TWO calibrated status updates — a team update for the people building the thing, and a leadership update for the person deciding on it — using each stakeholder's documented profile to set tone, format, and level of detail.
---

# Weekly Status Skill

## When to use it

Use when you have raw, unordered week notes and need to report the same underlying status to two different audiences who need it presented differently: engineering/design peers building the feature, and a leader who needs to feel informed without reading a full replay of the week.

## Inputs

- Raw bullet-point notes — unstructured, any order, mixing shipped work, in-progress work, blockers, and (optionally) next-week plans.
- Stakeholder profile files for everyone receiving an update (e.g. `04-team/stakeholders/*.md`) — read these for calibration signal, not just names: how they prefer to receive information, what they need to feel confident/informed, and anything they've flagged themselves that should come back to them plainly, not as a surprise.

## Output 1: Team Update (engineering + design peers)

Same four sections as a standard status update — **Shipped / In Progress / Blockers / Next Week** — written to match how builders actually want status:

- Short bullets, one sentence each, no fluff — matches a preference for async, bullet-first communication over prose.
- Research or user-testing items get a "here's what we learned" framing, not just "here's what we did" — a design-oriented reader responds to real evidence, not a bare activity log.
- Any blocker a specific person already raised gets stated back to them plainly and attributed to them (e.g. "Raj: ..."). Confirming a blocker someone flagged is tracked is good news to them; a surprised reaction in standup is not — that's the thing this format exists to prevent.

## Output 2: Leadership Update (single decision-maker)

Not the same four-header structure — a leader who wants the headline first and the whole thing on one page is better served by a short narrative, not a bulleted replay of the team's week:

- **Lead with the one-line status/recommendation, first sentence, not buried at the end.**
- Connect shipped and in-progress work to the business outcome it serves (e.g. the retention number this is meant to move), not just a list of activities.
- Surface only what actually needs their attention or a decision from them — omit anything that's just informational noise at their altitude.
- If they're unavailable for part of the week, state plainly whether anything is actually blocked on them, or whether it can wait — don't make them infer it.

## Rules

- Maximum 3-4 bullets per section in the team update; if more items qualify, keep the most significant and drop the rest rather than compressing several into one bullet.
- Plain, declarative language — no jargon, no buzzwords.
- If a section has no relevant notes, write "None" rather than omitting it.
- Only include information the notes actually support — a status update is not the place to guess at unstated progress. Deriving a "Next Week" item directly from an "In Progress" item (e.g. "PRD 70% done" → "finish PRD") is a reasonable continuation, not a guess; inventing a new, unmentioned initiative is not.

## Worked Example — Streakly Comeback Screen, 2026-09-17

**Input notes:**
- Shipped: interview synthesis complete (Priya, Tom, Amara); competitive matrix done (Duolingo, Babbel, Elevate; 2 white-space gaps); Reddit sentiment analysis complete (gaps confirmed by real user friction); prototype v1 live and tested across three personas.
- In progress: PRD first draft, 70% done; usability session scheduling, 3 of 5 confirmed.
- Blockers: Raj flagged the streak-freeze logic needs a data model change, estimate TBD; Marcus out Thu–Fri, async review only.

**Team Update (for Raj and Lena):**

> **Shipped**
> - Interview synthesis complete — direct input from Priya, Tom, and Amara now folded into the research base.
> - Competitive matrix done (Duolingo, Babbel, Elevate) — 2 white-space gaps confirmed.
> - Reddit sentiment analysis complete — real users' own words independently confirm the same gaps our interviews found.
> - Prototype v1 live and tested across all three personas — first real reactions in hand.
>
> **In Progress**
> - PRD first draft — 70% done.
> - Usability session scheduling — 3 of 5 confirmed.
>
> **Blockers**
> - Raj: streak-freeze logic needs a data model change — estimate still TBD. Flagging this back to you as tracked, not new.
>
> **Next Week**
> - Finish the PRD draft.
> - Confirm the remaining 2 usability sessions.

**Leadership Update (for Marcus):**

> **Status: on track, no decision needed from you this week.**
>
> Research and prototype testing are both complete — three-persona testing, competitive white-space, and independent Reddit sentiment all point the same direction the retention data already showed. The PRD is 70% drafted and usability testing is scheduling (3 of 5 sessions confirmed). One open engineering question — the streak-freeze data model — is with Raj; no estimate yet.
>
> Nothing here needs your input before Monday. Flagging your Thu–Fri async-only window in case that changes once Raj's estimate lands.
