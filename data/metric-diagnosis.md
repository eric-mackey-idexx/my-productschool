# Streakly Comeback Screen — Metric Diagnosis

*2026-09-17. All numbers below are real SQLite query results against `data/*.csv`, not estimates. Builds on `data/metric-findings.md`.*

## 1. Metric Tree — What Actually Moves Day-7 Retention

```
Day-7 Retention
├── Streak-start rate         → 100% (500/500 users have a goal_set_date)
│                               NOT a differentiating lever in this data — every user in
│                               this dataset already set a goal. The pre-goal funnel
│                               (installs who never set one) isn't captured here at all.
│
├── Streak-break rate (wk1)   → 38% (190/500) — real, measurable, the dominant lever.
│                               Breaking drops Day-7 retention from 45.8% → 26.8%.
│
├── Comeback rate             → Only measurable for the subset who got a comeback-type
│   (re-engagement after       outreach, not company-wide:
│    a break)                  • Old-style "streak_lost" nudge: 0% acted-on (0/141)
│                               • New "comeback_screen" nudge: 50% acted-on (10/20)
│                               This is the sharpest lever found in the whole analysis —
│                               see Hypothesis 1 below.
│
└── Notification opt-in       → NOT PRESENT in this dataset. No field tracks push
                                permission state anywhere in users.csv, retention.csv,
                                or nudges.csv. This is a real instrumentation gap, not a
                                zero — flagging it rather than guessing a number.
```

**What this means:** two of the four requested levers are real and measurable (streak-break rate, comeback/act-on rate); one is currently saturated and not a bottleneck (streak-start, 100%); one can't be measured at all with current instrumentation (notification opt-in). Before scaling, the notification opt-in gap should be closed — if a meaningful share of users have push disabled, the comeback *nudge* can't reach them no matter how good the *screen* is once they open the app.

## 2. What Caused the Decline in Weeks 1–4 (Specific, Not Generic)

Two distinct, separately-measurable things are happening — not one vague "engagement dropped":

**A. The streak-break rate rose and stayed elevated.**

| Cohort week | Broke streak wk1 |
|---|---|
| 1 | 26.0% |
| 2 | 39.0% |
| 3 | 45.0% |
| 4 | 35.0% |

Week 1's 26% break rate jumped to 39–45% in weeks 2–4 and never returned to the week-1 level. Since breakers retain at a flat ~23% regardless of cohort week (23.1%, 23.1%, 24.4%, 22.9% — remarkably stable), more people landing in that low-retention bucket mechanically drags the cohort average down.

**B. Independently, non-breakers' own retention also eroded.**

| Cohort week | Day-7 retention, users who did NOT break |
|---|---|
| 1 | 41.9% |
| 2 | 45.9% |
| 3 | 36.4% |
| 4 | 29.2% |

Even people who kept their streak intact retained worse by week 4 than week 1 — a 12.7-point drop among *successful* streak-keepers. This is not explained by:
- **Acquisition channel mix** — identical every week (34 organic / 34 paid / 32 referral, all four weeks) — ruled out.
- **Session engagement** — average sessions/user (4.0, flat) and average session duration (~230 sec, flat) across all four weeks — ruled out.

This dataset does not contain a field that explains *why* non-breaker retention fell (no app-version flag, no notification-tone flag, nothing that changed week over week). Stated plainly: **the data confirms two real, distinct effects — more people breaking their streak, and even non-breakers retaining worse — but only explains the mechanism for the first one.** The second is consistent with `project.md`'s premise that a redesign shipped and hurt retention broadly, but this dataset alone can't prove that specific causal link — it can only rule out channel mix and session volume as the explanation.

## 3. What the Week-5 Split Tells Us About What the Comeback Screen Actually Fixed

Breaking week 5 down by whether the user actually broke their streak (the population the screen is meant for) changes the story:

| Variant | Broke streak wk1 | n | Day-7 retention |
|---|---|---|---|
| Comeback | No | 30 | 93.3% |
| Comeback | Yes | 20 | 50.0% |
| Control | No | 25 | 64.0% |
| Control | Yes | 25 | 28.0% |

**Among people who actually broke their streak — the screen's intended target — comeback lifts retention from 28.0% to 50.0%, a 22-point gap.** That's the mechanism-consistent result: the feature helped the people it was built for.

**But there's a real problem with the topline number:** among people who *never broke their streak* — who shouldn't even be eligible to see this screen under the gating rule in `04-team/spec-readiness.md` (`preBreakStreak > 0`) — comeback-variant users still retained far better than control (93.3% vs. 64.0%, a 29.3-point gap). The screen mechanically can't explain that gap, since these users never triggered it. Two explanations, both worth investigating before trusting the topline 76%-vs-46% number as "the comeback screen's effect":
1. The week-5 `variant` field may represent a broader experience change (e.g., overall tone/notification changes), not just this one screen — the data alone can't distinguish "comeback screen" from "everything else that shipped alongside it in the treatment arm."
2. At n=50/arm, random imbalance is plausible — the two arms' breaker rates aren't even identical (comeback: 40% broke, control: 50% broke), which is itself a small randomization-balance flag.

**Straight answer to the question: the screen has a real, plausible, mechanism-consistent effect specifically on streak-breakers (28% → 50%). A meaningful share of the topline 76%-vs-46% lift is currently unexplained by the screen itself** and needs to be isolated before it's used to justify scaling on its full magnitude.

## 4. Four Ranked Hypotheses for Why Some Treatment Users Still Churned

*Population: the 12 comeback-variant, week-5 users who did not retain at Day 7 (out of 50).*

### Hypothesis 1 — Action, not exposure, is what protects retention
**Prediction:** Among streak-breakers who see the comeback screen, users who act on it (tap through) will retain at a dramatically higher rate than users who merely see it without acting — action on the offer, not delivery of the offer, is the actual protective mechanism.

- **Rank: 1 (highest)**
- **Confidence: 9/10** — Among the 20 comeback-variant users who broke their streak, the `comeback_screen` nudge's `acted_on` field predicts Day-7 retention *perfectly*: all 10 who acted_on=true retained; all 10 who acted_on=false churned. That's a 100%-vs-0% split, not a trend. Not a 10 because a split this clean is unusually tidy for real user behavior — worth confirming it's not an artifact of how this sample dataset was constructed before treating it as a proven causal mechanism.
- **Confirms it:** A future test where the CTA is made lower-friction (e.g., one-tap, no navigation) shows a higher act-on rate *and* a correspondingly higher retention rate for the newly-converted actors.
- **Rules it out:** A future cohort where users who acted_on the nudge still churn at a meaningfully high rate (e.g., >20%), or where non-actors retain at rates close to actors.

### Hypothesis 2 — The screen narrows the breaker gap but doesn't close it
**Prediction:** Even at full rollout, users who break their streak will retain at a meaningfully lower rate than users who never broke it, regardless of comeback screen exposure — the feature is a mitigation, not a cure.

- **Rank: 2**
- **Confidence: 6/10** — Directionally certain (50.0% vs. 93.3% within the same variant, a 43-point gap that treatment didn't close), but this is the more expected/generic-adjacent finding of the four — breaking a streak being worse than not breaking one isn't surprising on its own.
- **Confirms it:** Scaling to 100% adoption still leaves a >30-point gap between ever-broke and never-broke users at Day 7.
- **Rules it out:** A future iteration of the screen closes that gap to under ~10 points, showing the feature *can* fully compensate for a break.

### Hypothesis 3 — Paid-acquired users are less responsive to the comeback intervention
**Prediction:** The comeback screen's treatment-vs-control lift will be consistently smaller for paid-acquired users than for organic or referral users across future cohorts.

- **Rank: 3**
- **Confidence: 5/10** — Consistent with two independent signals: paid has the lowest baseline Day-7 retention across weeks 1–4 (27.9% vs. 34.6% organic, 36.7% referral) *and* the smallest treatment lift in week 5 (comeback-vs-control gap: paid +14.7pts, organic +23.5pts, referral +51.2pts). But each week-5 channel cell is only 16–17 users — too small to rule out noise on its own.
- **Confirms it:** A larger-sample repeat shows the same ordering (referral > organic > paid lift) holding up.
- **Rules it out:** A larger sample shows the lift is statistically indistinguishable across channels.

### Hypothesis 4 — Some treatment-arm churn is unrelated to the comeback screen entirely
**Prediction:** A baseline churn rate exists among users who never break their streak (and thus never see the screen) that's roughly equal between variants — not all churn inside the "treatment" label is a signal about the feature.

- **Rank: 4 (lowest)**
- **Confidence: 3/10** — Real but tiny evidence: 2 of the 12 churned comeback-variant users never broke their streak at all, so the screen mechanically couldn't have reached them. n=2 is an existence proof, not a rate.
- **Confirms it:** At scale, a stable, roughly-equal background churn rate persists among never-broke users in both arms.
- **Rules it out:** Those 2 users turn out to have had an undocumented break/exposure not captured by the `broke_streak_week1` flag — i.e., this would become a data-quality finding, not a churn-mechanism finding.

## 5. Which Hypothesis to Test First Next Sprint

**Hypothesis 1** — action-on-offer, not exposure, drives retention.

Three reasons it beats the other three for a next-sprint test: it has the highest confidence (9/10, backed by a perfect 10/10-vs-0/10 split, not just a directional lean); it's the most **actionable** — the product lever is a UX change the squad directly controls (reduce friction to acting, e.g., a one-tap "connect my streak" action instead of navigation), unlike Hypothesis 3's channel-mix lever, which belongs to marketing/acquisition, not this squad; and it's the most **consequential** — if true, it means the current rollout is leaving retention on the table for every user who *sees* the screen but doesn't act, which is a fixable UX problem, not a fixed population characteristic like Hypotheses 2 and 4.
