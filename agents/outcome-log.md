# Anomaly Diagnosis Outcome Log

*Every anomaly-diagnosis run logs its hypotheses here. The "what actually happened" column starts as a placeholder — fill it in once the real cause is confirmed, so this log becomes a track record of how good the hypothesis-generation rules actually are.*

## 2026-09-17 — Day-7 retention moved +34.0 pts

**Loop stopped at:** Step 3 — low confidence (6/10)

| Rank | Hypothesis | Confidence | What actually happened |
|---|---|---|---|
| 1 | New-user cohort quality shift (e.g. a lower-intent acquisition channel) driving more early streak breaks. | 6/10 | **Miss.** Confirmed cause was the week-5 Comeback screen A/B test (comeback vs. control), not a cohort/channel shift — see `data/metric-diagnosis.md` and `data/metric-findings.md`, which established this independently before the anomaly agent existed. The agent had no way to know: `agents/metric_pulse.py` doesn't check the `variant` column for an active experiment (a gap already flagged in `agents/metric-pulse.md` and `agents/registry.md`). |
| 2 | Product/copy regression (e.g. a recent deploy touching the streak-reset or comeback flow) not explained by the instrumented drivers above. | 3/10 | **Miss**, same real cause as above (the A/B test) — no deploy/copy regression occurred. |

## 2026-09-17 — Streak-break rate moved +10.0 pts

**Loop stopped at:** Step 1 — below threshold

| Rank | Hypothesis | Confidence | What actually happened |
|---|---|---|---|

## Weekly Learning Loop Review — 2026-09-17

**Scoreable this week:** 1 of 2 logged diagnosis checks (the streak-break-rate check stopped at Step 1 with no hypothesis generated — nothing to score there by design).

| Date | Hypothesis | Confidence | Outcome | Score | Reasoning |
|---|---|---|---|---|---|
| 2026-09-17 | New-user cohort quality shift | 6/10 | A/B test, not a cohort shift | **Miss** | Confident-sounding guess named a real mechanism (channel quality) but not the one that actually happened. |
| 2026-09-17 | Product/copy regression | 3/10 | A/B test, not a regression | **Miss** | Correctly low-confidence, and still wrong — but appropriately hedged, unlike hypothesis 1. |

**Pattern:** n=1 scored diagnosis is nowhere near enough to say either the "cohort quality shift" or "product regression" *templates* are unreliable in general — one miss each isn't a rate, it's an anecdote. What the miss *does* show clearly: both wrong hypotheses failed for the identical, single reason — the rule table has no check for an active A/B test before generating cohort/product hypotheses, and `agents/metric_pulse.py` doesn't look at the `variant` column at all. That's a structural gap, not a confidence-calibration one, and this is direct, confirmed evidence of its cost (not just a flagged risk anymore).

**Proposed heuristic update:** Add a Step 2.5 check to `agents/anomaly_diagnosis.py`'s `generate_hypotheses()`: if the current period has more than one non-empty `variant` value in `data/users.csv` (the same check `monday_retention_check.py` already does), generate a 4th, top-ranked hypothesis — "Active A/B test (variant: [x]) — check treatment vs. control split before trusting the blended number" — ahead of the other three, since an active experiment should always outrank a guess when one is detectable. **Not proposing a confidence-number change to the existing 3 templates** — that would be overfitting a rate from a single miss each.

*Applied 2026-09-17, per Eric. Re-ran `metric_pulse.py test-run` afterward: this same Day-7 retention move now correctly ranks the A/B test 9/10 and proceeds through Step 4, instead of stopping at low confidence on two wrong guesses. See the new entry below.*

## 2026-09-17 — Day-7 retention moved +34.0 pts

**Loop completed through Step 4 (SQL + Slack posted).**

| Rank | Hypothesis | Confidence | What actually happened |
|---|---|---|---|
| 1 | Active A/B test detected this period (variant: comeback, control) — check the treatment vs. control split before trusting the blended number. | 9/10 | _placeholder — fill in after investigating_ |
| 2 | New-user cohort quality shift (e.g. a lower-intent acquisition channel) driving more early streak breaks. | 6/10 | _placeholder — fill in after investigating_ |
| 3 | Product/copy regression (e.g. a recent deploy touching the streak-reset or comeback flow) not explained by the instrumented drivers above. | 3/10 | _placeholder — fill in after investigating_ |

## 2026-09-17 — Streak-break rate moved +10.0 pts

**Loop stopped at:** Step 1 — below threshold

| Rank | Hypothesis | Confidence | What actually happened |
|---|---|---|---|
