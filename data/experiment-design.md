# Streakly Comeback Screen — Full Experiment Design

*2026-09-17. Pressure-tests the week-5 pilot (`data/metric-findings.md`, `data/metric-diagnosis.md`) and designs the properly-powered follow-up test before any scale decision. Written for a PM audience — statistics explained in plain English before each calculation.*

## 1. Is the Pilot Statistically Significant?

**What significance means for a go/no-go call:** it tells you whether a result is unlikely to be random chance — it answers "is this real?", not "is this big enough to act on?" (that's the MDE question, Section 2).

**Pilot data:** comeback 38/50 (76%) vs. control 23/50 (46%), n=50 per arm.

- Two-proportion z-test: pooled p = 0.61, SE = 0.0976, **z = 3.08, p ≈ 0.002**
- **Significant at 95% confidence** — a gap this size would occur by chance only ~2 times in 1,000.
- **95% confidence interval on the effect size: 11.8 to 48.2 percentage points.**

**What this means:** the pilot result is real, not noise. But at n=50/arm, the estimate of *how big* the effect is stays wide open — anywhere from a modest 12-point lift to a huge 48-point one. Significance answers "is something happening"; it does not answer "how much," and the memo to Marcus should not present 76%-vs-46% as a precise, load-bearing number.

## 2. Minimum Detectable Effect (MDE)

**What it means, and why set it in advance:** MDE is the smallest effect size worth acting on, fixed *before* the test runs — so the bar for success is decided before anyone has seen a result they might be tempted to rationalize toward.

**MDE for this test: 5 percentage points**, set going in.

## 3. Statistical Power & Required Sample Size

**What power means, and the risk if it's too low:** power is the probability the test actually detects a real effect of the MDE size if one exists. Too-low power risks a false "no effect" verdict — killing a genuinely good feature for a statistical reason, not a product one.

**Inputs:** 80% power, 95% significance, MDE = 5pts, baseline = 46%.

```
n per variant = (z_α/2 + z_β)² × [p1(1-p1) + p2(1-p2)] / (p1-p2)²
             = (1.96 + 0.84)² × (0.46×0.54 + 0.51×0.49) / (0.05)²
             = 7.85 × 0.4983 / 0.0025
             ≈ 1,565 per variant (≈ 3,130 total)
```

**Result: ~1,565 users per variant (~3,130 total)** — roughly 31x the pilot's sample size.

*Note on the baseline used: 46% is the pilot's blended control rate across all week-5 users (breakers and non-breakers together), per the parameters given for this calculation. `metric-diagnosis.md` found the mechanism-consistent effect specifically among streak-breakers uses a different baseline (28%) — worth deciding explicitly whether the full test's eligibility and baseline should be breaker-specific before it launches, since that changes both the required n and who gets enrolled.*

## 4. Test Duration

**Eligible population:** users who break their streak, not the full 85,000 WAU. Using the dataset's overall observed break rate (~38%, `data/users.csv`) as a working assumption — flagged as an assumption, since weekly rates in the pilot period ranged 26–45%:

```
Eligible per week ≈ 85,000 × 0.38 ≈ 32,300/week → ~16,150 per arm/week
Time to reach 1,565/arm ≈ 1,565 / 16,150 ≈ 0.7 days
```

**Finding: sample size is not the constraint.** The eligible population is large enough that the required n arrives in under a day. The real constraint is the outcome-measurement lag — waiting out Day-7 (and Day-30) for the *last* enrolled user.

**Recommended design:**
- **1 week of enrollment** (avoids day-of-week bias; banks a ~10x safety margin over the statistical minimum)
- **+ 7 days** to observe Day-7 for the last-enrolled cohort → **~2 weeks total for the primary Day-7 read**
- **+ 30 days** (instead of 7) if also confirming Day-30 durability as the pilot did → **~5 weeks total**

**Fits the 8-week constraint?** Yes, comfortably — with 3 to 6 weeks of unused margin, because enrollment speed was never the bottleneck.

## 5. The Decision

**Recommendation: run the full test before scaling.** Don't scale on the pilot alone (n=50/arm, CI of 12–48pts is too wide to commit a rollout to), and don't sit on the pilot indefinitely either (the full test is cheap — 2 to 5 weeks against an 8-week budget).

| Path | Risk, in one sentence |
|---|---|
| **Scale now, on the pilot alone** | Commits engineering and organizational credibility to a lift that could be closer to 12 points than 30, and that gap surfaces only after full rollout, when it's expensive to reverse. |
| **Run the full test first** | A few more weeks of continued churn at the current retention rate before any rollout decision — bounded and short, not open-ended. |

## 6. Leading Indicators to Watch Weekly

| Metric | Nervous if... | Why it matters |
|---|---|---|
| Comeback message open rate (treatment) | Falls below ~15–20% in week 1 of the real test | Pilot's lowest single send still hit 28% — roughly half that signals the message isn't resonating at scale the way it did in a 50-person pilot. |
| Act-on rate among those who open | Drops well below the pilot's ~50% (among streak-breakers) | `metric-diagnosis.md` found action — not exposure — predicts retention (10/10 actors retained vs. 0/10 non-actors). A falling act-on rate is the earliest sign the actual mechanism is breaking down, regardless of open rate. |
| Day-1 / Day-3 retention gap (treatment vs. control) | No meaningful separation (<3–5pts) in the first few days | No need to wait the full 7 days — if the groups aren't diverging within days, the eventual Day-7 gap is unlikely to resemble the pilot's. |

## Summary for the Go/No-Go Call

The pilot is real (p≈0.002) but imprecise (12–48pt CI). A properly powered follow-up test needs ~1,565 users/arm, which the eligible population supplies in under a day — meaning the *actual* time cost is the 2–5 week outcome-measurement window, not enrollment. That comfortably fits the 8-week ceiling. Recommend running that test, with the three leading indicators above tracked weekly, before any commitment to scale.
