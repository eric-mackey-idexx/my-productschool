# Streakly Comeback Screen — Metric Findings

*2026-09-17. Queries run against `data/users.csv`, `data/retention.csv`, and `data/comeback_sends.csv`, loaded into a local SQLite database for this analysis (not committed — the CSVs are the source of truth). All numbers below are actual query results, not estimates.*

## 1. Day-7 retention by cohort week — what does the decline look like?

```sql
SELECT
  u.cohort_week,
  COUNT(*) AS users,
  SUM(CASE WHEN r.day_7 = 'true' THEN 1 ELSE 0 END) AS retained_day7,
  ROUND(100.0 * SUM(CASE WHEN r.day_7 = 'true' THEN 1 ELSE 0 END) / COUNT(*), 1) AS day7_retention_pct
FROM users u
JOIN retention r ON r.user_id = u.user_id
GROUP BY u.cohort_week
ORDER BY u.cohort_week;
```

**Plain English:** For each cohort week, count how many of that week's 100 users were still active on Day 7, and turn that into a percentage.

**Result:**

| Cohort week | Users | Retained Day-7 | Day-7 retention |
|---|---|---|---|
| 1 | 100 | 37 | 37.0% |
| 2 | 100 | 37 | 37.0% |
| 3 | 100 | 31 | 31.0% |
| 4 | 100 | 27 | 27.0% |
| 5 | 100 | 61 | 61.0% |

**What this means for the decision:** Weeks 1–4 show a real, steady decline (37% → 37% → 31% → 27%) — this is the retention erosion `project.md` and `docs/decision-brief.md` describe, playing out week over week, not a one-time dip. Week 5's jump to 61% is **not** a natural recovery — it's an average of two very different groups (see Q3): the comeback variant and control were both first introduced in week 5. Don't read week 5 as "the decline reversed itself" — read it as "the decline continued for the control half, and the treatment half is what pulled the average up." This is exactly why Q3 needs to be looked at split by variant, not blended.

## 2. Do users who break their streak in week 1 retain worse than those who don't?

```sql
SELECT
  broke_streak_week1,
  COUNT(*) AS users,
  ROUND(100.0 * SUM(CASE WHEN day_7 = 'true' THEN 1 ELSE 0 END) / COUNT(*), 1) AS day7_retention_pct,
  ROUND(100.0 * SUM(CASE WHEN day_30 = 'true' THEN 1 ELSE 0 END) / COUNT(*), 1) AS day30_retention_pct,
  ROUND(100.0 * SUM(CASE WHEN churned = 'true' THEN 1 ELSE 0 END) / COUNT(*), 1) AS churn_pct
FROM retention
GROUP BY broke_streak_week1;
```

**Plain English:** Split all 500 users into two groups — broke their streak in week 1, or didn't — and compare Day-7 retention, Day-30 retention, and overall churn between them.

**Result:**

| Broke streak week 1? | Users | Day-7 retention | Day-30 retention | Churn |
|---|---|---|---|---|
| No | 310 | 45.8% | 12.6% | 54.5% |
| Yes | 190 | 26.8% | 12.6% | 73.2% |

**What this means for the decision:** Yes — clearly, at Day 7. Breaking a streak in week 1 drops retention from 45.8% to 26.8% and pushes churn from 54.5% to 73.2%. This directly confirms the core problem statement the whole Comeback screen project is built on. One honest caveat worth flagging, not smoothing over: **Day-30 retention is identical for both groups (12.6% vs 12.6%)** — whatever damage the week-1 break does, it shows up clearly at Day 7 but the gap is gone by Day 30 in this dataset. That's either a real finding (survivors of either path look similar a month out) or an artifact of how this sample was generated — worth a second look before leaning on Day-30 numbers in any pitch to Marcus.

## 3. Week 5 only — Day-7 and Day-30 retention, treatment vs. control

```sql
SELECT
  u.variant,
  COUNT(*) AS users,
  ROUND(100.0 * SUM(CASE WHEN r.day_7 = 'true' THEN 1 ELSE 0 END) / COUNT(*), 1) AS day7_retention_pct,
  ROUND(100.0 * SUM(CASE WHEN r.day_30 = 'true' THEN 1 ELSE 0 END) / COUNT(*), 1) AS day30_retention_pct
FROM users u
JOIN retention r ON r.user_id = u.user_id
WHERE u.cohort_week = '5'
GROUP BY u.variant;
```

**Plain English:** Restrict to only the 100 week-5 users (the only cohort that actually got the A/B test), split by which version they saw, and compare Day-7 and Day-30 retention.

**Result:**

| Variant | Users | Day-7 retention | Day-30 retention |
|---|---|---|---|
| Comeback | 50 | 76.0% | 36.0% |
| Control | 50 | 46.0% | 22.0% |

**What this means for the decision:** This is the strongest single result in the dataset. The comeback variant beats control by 30 points at Day 7 (76% vs. 46%) **and** the lift holds at Day 30 (36% vs. 22%, still a 14-point gap) — so this isn't just a short-term novelty bump that fades. Unlike Q2's Day-30 flatline, the treatment effect here persists a month out. This is the number that answers `hypothesis.md`'s test: "we believe the Comeback screen will deliver reduced churn... recovering Day-7 retention toward the 48% baseline" — 76% clears that bar. One caveat for whoever takes this to Marcus: n=50 per group is a small sample for a launch decision: worth stating the sample size alongside the percentage, not just the headline lift.

## 4. Did the Comeback screen's open rate improve across the 4 sends vs. control?

```sql
SELECT
  send_number,
  variant,
  COUNT(*) AS sends,
  ROUND(100.0 * SUM(CASE WHEN opened = 'true' THEN 1 ELSE 0 END) / COUNT(*), 1) AS open_rate_pct
FROM comeback_sends
GROUP BY send_number, variant
ORDER BY send_number, variant;
```

**Plain English:** For each of the 4 comeback-related messages sent to week-5 users, and for each variant, work out what percentage of the 50 recipients opened it.

**Result:**

| Send # | Comeback open rate | Control open rate |
|---|---|---|
| 1 | 28.0% | 4.0% |
| 2 | 38.0% | 4.0% |
| 3 | 46.0% | 4.0% |
| 4 | 56.0% | 4.0% |

**What this means for the decision:** Yes, decisively. The comeback variant's open rate climbs every single send (28% → 38% → 46% → 56%) while control stays flat at 4.0% for all four — not just higher, but *increasingly* higher relative to a control that never moves. That pattern (rising engagement, not a one-time spike) is evidence the message itself is doing something right, not just novelty. Combined with Q3, this suggests the comeback screen's effect compounds with repeated exposure rather than wearing off — a point worth using directly in the recommendation to scale.

## Bottom line for the scale decision

All four queries point the same direction: the comeback variant outperforms control at Day 7, the lift persists at Day 30, and engagement with the comeback messaging itself climbs rather than fades across sends. The two things worth flagging before this goes to Marcus as a scale recommendation, not glossing over: the week-5 sample is small (n=50/arm), and the week-1-break Day-30 flatline (Q2) is worth understanding before extrapolating too far on long-term impact.
