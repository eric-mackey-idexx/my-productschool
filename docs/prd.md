# PRD: Streakly Comeback Screen

*Audience: Raj (Eng), Lena (Design). Sources: `research/nps-analysis.md`, `research/competitive-matrix.md`, `docs/decision-brief.md`, `03-build/hypothesis.md`, `04-team/stakeholders/raj.md`, `04-team/stakeholders/lena.md`. `research/interview-synthesis.md` and `research/competitive-reddit.md` do not exist in this repo and are not used as sources.*

## Problem Statement

Day-7 retention dropped from 48% to 39% after the streak redesign shipped, concentrated in users who break their streak in week 1 (`docs/decision-brief.md`). Today, a break resets the streak to zero with no acknowledgment (`docs/decision-brief.md`). 7 of 10 NPS comments name this reset as their reason for disengaging or uninstalling (`research/nps-analysis.md`). No competitor reviewed — Duolingo, Babbel, Elevate, Memrise, Headspace — offers a free, built-in recovery moment; Duolingo's Streak Freeze is the only protection mechanic found, and it's paywalled (`research/competitive-matrix.md`). No competitor personalizes the return experience by time away — the same gap NPS feedback raised independently (`research/competitive-matrix.md`, `research/nps-analysis.md`).

## User

**Who:** A Streakly user who has built a multi-day streak and breaks it in week 1 — NPS calls this the "high-stakes streak owner" segment, whose loss of a streak caused total disengagement or deletion (`research/nps-analysis.md`).
**Job to be done:** Give the user a reason and a concrete way to resume, so a break doesn't become a permanent stop (`research/nps-analysis.md`'s "no personalized re-entry point" finding).

## Goals and Non-Goals

**Goals** (`docs/decision-brief.md`, Recommended Action):
- Ship the Comeback screen (best-streak stat, personalized re-entry, one-tap streak-freeze) in place of the cold reset.
- Address the dominant NPS theme (7/10 comments) and both competitive white-space gaps: free recovery, personalized re-entry (`research/competitive-matrix.md`).

**Non-Goals** (`docs/decision-brief.md`, Next Steps / Decisions Needed):
- Notification tone/cadence redesign — separate workstream, scope not yet confirmed.
- Free vs. paywalled streak-freeze — Marcus's monetization call, not a design/eng decision.
- Resolving the streak-intensity trade-off (softening the reset vs. what motivates high-stakes streak owners) — a team judgment call, unresolved by current research (`research/nps-analysis.md`).

## Success Metrics

*Draft, not yet team-agreed (`03-build/hypothesis.md`).*
- Day-7 retention among the week-1-break segment, trending toward the pre-redesign 48% baseline.
- No corresponding drop in engagement among high-stakes streak owners — required companion metric per the unresolved streak-intensity trade-off; no target value defined yet (`research/nps-analysis.md`, `docs/decision-brief.md`).

## User Stories

1. As a user who broke my streak, I see my best-streak stat instead of a blank reset, so I know my past effort wasn't erased. (`research/nps-analysis.md`: "home screen looks the same whether I'm on a 2-day streak or coming back after two weeks away.")
2. As a returning user, I get a one-tap way to protect/continue my streak, so recovery doesn't require starting over. (`research/nps-analysis.md`: "no way to recover it... other apps let you freeze a streak.")
3. As a high-stakes streak owner, the comeback offer doesn't feel like a gimmick, so I don't lose trust in the mechanic that otherwise keeps me engaged. (`research/nps-analysis.md`'s hook-vs-cliff tension: the same mechanic drives engagement and churn for the same users.)
4. As Raj, I need the data model question — does "resume" pull from best-streak or actual pre-break streak length — answered before I can size this. (`04-team/stakeholders/raj.md`.)
5. As Lena, I need this checked against Streakly's real design system and grounded in real user evidence, not PM-assumed copy, before I sign off. (`04-team/stakeholders/lena.md`.)

## Open Questions

- **Targeting logic:** which users see this screen, and when (`docs/decision-brief.md`).
- **Freeze rules:** duration, frequency limits — undefined (`docs/decision-brief.md`).
- **Data model:** best-streak vs. actual pre-break streak length — not the same number, not yet resolved (`04-team/stakeholders/raj.md`).
- **Eng sizing/timeline:** feasibility confirmed, not yet estimated (`docs/decision-brief.md`).
- **Edge cases:** a user who has never held a streak, or breaks twice in a week — not addressed in any source (`04-team/stakeholders/raj.md`).
- **Mechanic scope:** does "continue where left off" resume the user's prior lesson/track position, or route to a separate short comeback lesson — these pull different data (`04-team/stakeholders/lena.md`).
- **Visual/tone fidelity:** current design direction isn't checked against Streakly's real design system; minimum fidelity needed before user testing is undefined (`04-team/stakeholders/lena.md`).
