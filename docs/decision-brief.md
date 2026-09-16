# Decision Brief: Streakly Day-7 Retention

*For: Marcus (Head of Product) — Prepared by Eric Mackey, Product Lead*
*Sources: `project.md` (team discussion), `research/nps-analysis.md`, `research/competitive-matrix.md`. `competitive-reddit.md` was not available (Reddit access failed and was not substituted) and is excluded from this brief.*

## Situation

Day-7 retention dropped from 48% to 39% after the streak redesign, concentrated among users who break their streak in week 1 — missing two days in a row nearly doubles churn. The team's working hypothesis is that a punishing, non-personalized comeback experience is driving this, and that hypothesis now has independent support from user feedback and competitive research.

## Problem to Be Solved

The streak itself isn't the problem — it's what hooks people in the first place. The problem is that there's no graceful way back in after a break: the app resets to zero with no acknowledgment, pairs it with a harsh-toned "you lost your streak" push, and offers no path forward. Users experience this as failure rather than a nudge to continue, so a temporary lapse turns into permanent churn.

## Key Findings

- **Team hypothesis (project.md):** the post-break experience is a cold reset with no acknowledgment and a harsh-toned notification; Eric's read is that the friction is mainly functional (hard to resume), with some emotional component.
- **NPS data confirms it independently:** 7 of 10 verbatim comments cite the punishing streak reset as the reason they disengaged or uninstalled — strong triangulation between the internal hypothesis and real user voice, not just an assumption.
- **Competitive research confirms the fix is genuinely differentiated:** none of 5 competitors reviewed (Duolingo, Babbel, Elevate, Memrise, Headspace) offer a free, built-in recovery moment. Duolingo's Streak Freeze is the only protection mechanic found, and it's paywalled.
- **Two independent sources point to the same specific gap:** no competitor personalizes the return experience based on how long a user was away — the identical gap NPS feedback raised directly ("home screen looks the same whether I'm on a 2-day streak or coming back after two weeks").
- **Unresolved risk (from NPS analysis):** the streak is both the top engagement driver and the top churn trigger for the same users. Softening the reset (freeze, partial credit) could reduce the intensity that currently motivates high-stakes streak owners — this trade-off isn't resolved by current research and needs a decision, not just a design.

## Options Considered

1. **Ship the proposed Comeback screen** (best-streak stat, 60-second comeback lesson, one-tap streak-freeze) as sketched in `project.md` — directly addresses the dominant NPS theme (7/10) and both competitive white-space gaps.
2. **Fix notification tone/cadence only**, leaving the reset mechanic unchanged — lower risk and effort, but doesn't touch the dominant theme or the core hypothesis.
3. **Hold any build until Thursday's alignment meeting** resolves root cause and target metrics — lowest risk, but the retention drop compounds every week it's unaddressed.

## Recommended Action

Move forward with scoping and designing the Comeback screen as the primary Day-7 retention fix — it's now backed by three independent sources (team hypothesis, NPS themes, competitive white space) — while resolving the still-open targeting logic, freeze rules, and the streak-intensity trade-off at Thursday's meeting.

## Why Now

Three independent signals — the team's own hypothesis, 7 of 10 NPS comments, and a confirmed competitive gap — are pointing at the same root cause and the same fix simultaneously; every additional week at 39% Day-7 retention compounds churn before the team even agrees to act.

## Next Steps — Discovery

- Size engineering lift and timeline for the Comeback screen (Raj confirmed it's "technically doable," not yet estimated)
- Define target metric values and a date to hit them by (current metrics in `project.md` have no targets set)
- Define targeting logic — which users see the Comeback screen, and when
- Define freeze rules — duration, frequency limits
- Confirm whether the notification tone/cadence fix is in scope now or a separate follow-on workstream

## Decisions Needed (Not Discovery)

- **Free vs. paywalled streak-freeze** — a monetization call, not something to research. Duolingo gates this; our proposal doesn't.
- **Accepting the streak-intensity trade-off** — softening the reset may reduce what motivates high-stakes streak owners. This is a judgment call for the team to make at Thursday's meeting, not an open research question.
