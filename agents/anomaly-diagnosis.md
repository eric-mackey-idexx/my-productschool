# Anomaly Diagnosis Agent — Streakly

*2026-09-17. Chained to `agents/metric_pulse.py`: whenever the pulse agent's overall Day-7 retention or streak-break rate alert fires, this runs a 5-step diagnostic loop and either posts a full diagnosis to Slack or stops early and says why.*

## 1. The Updated Agent

**`agents/anomaly_diagnosis.py`** (new) — implements the 5-step loop as `run_diagnosis()`, plus a `diagnose` CLI for testing one scenario by hand and a `simulate-drop` CLI for the fixed 4-point-drop scenario end to end.

**`agents/metric_pulse.py`** (updated) — two changes:
- `load_data()` and `compute_metrics()` now also pull `sessions.csv` and `nudges.csv` and compute two new overall-level driver metrics: average sessions per user, and push open rate. These feed the diagnosis loop's Step 2 decomposition.
- `cmd_digest()` now calls `anomaly_diagnosis.run_diagnosis()` for both overall metrics (Day-7 retention, streak-break rate) after posting the pulse digest. **This is the actual chain, not a description of one** — `run_diagnosis()` re-checks Step 1 internally, so calling it unconditionally for both metrics is safe: it silently logs-and-stops for whichever one didn't actually cross its own adaptive threshold that week. "Only triggers on alert" is enforced by that internal check, not by metric_pulse deciding in advance which metric to diagnose.

Hypothesis generation (Step 3) is an explicit, inspectable rule table (`generate_hypotheses()`), not a model call — see the "How hypotheses are generated" section below. That's a deliberate v1 scope, documented so it's not mistaken for something smarter than it is.

## 2. The Conditions at Each Step

| Step | Check | Passes when | Stops when |
|---|---|---|---|
| 1. Threshold check | Is the move above the adaptive threshold for this metric's sample size? (Same formula as `metric_pulse.py`.) | `\|delta\| >= threshold` | Move is under threshold — **logged, loop stops.** No Slack post; this is expected to happen often and isn't itself news. |
| 2. Metric tree decomposition | Decompose into 3 drivers — streak-break rate, sessions in week 1, push opt-in rate — each screened for "meaningful movement" (±3pts for rate drivers, ±10% relative for sessions). | At least 2 of 3 drivers meaningful | Only 0-1 driver meaningful — **flagged inconclusive, loop stops.** The move is confirmed real (Step 1 passed) but not explained by any instrumented driver; that itself is worth knowing, logged as such. |
| 3. Hypothesis generation | Generate up to 3 ranked, rule-based hypotheses from which drivers moved and how. | Top hypothesis confidence **> 6/10** | Top hypothesis confidence **<= 6/10** — **posts a "low confidence" Slack alert, loop stops.** Does not guess further or force a top pick past what the rules actually support. |
| 4. SQL + Slack | Write the SQL to confirm the top hypothesis; post the full diagnostic to Slack. | Always, once Step 3 passes | — |
| 5. Log the call | Append the ranked hypotheses, confidence, and a placeholder for "what actually happened" to `outcome-log.md`. | Always — even on an early stop, so every check leaves a trace | — |

## How Hypotheses Are Generated (Step 3 Detail)

Three fixed templates, each with an explicit confidence rule:

1. **Push notification delivery/engagement issue** — confidence 8/10 if *both* sessions and push opt-in dropped meaningfully in the same direction (the corroborating pattern in the spec's own worked example); 5/10 if only sessions dropped meaningfully without push corroborating it; not generated at all if sessions didn't drop.
2. **New-user cohort quality shift** — confidence 6/10 whenever streak-break rate rose meaningfully. Channel-level attribution isn't computed inside this loop (that lives in `metric_pulse.py`'s per-channel breakdown) — this hypothesis flags the pattern, the SQL in Step 4 is what actually checks it.
3. **Product/copy regression** — confidence 3/10, always offered as a catch-all. This is the "we don't have an instrumented driver for this" bucket — explicitly low, and explicitly requires manual confirmation (release log, QA), not a query.

This is a small, extensible table, not a claim that every possible cause is covered — new patterns should get added as explicit rules, the same way these three were.

## 3. Slack Diagnostic Format

**Full diagnostic (Steps 1-4 all passed):**

```
:mag: *Streakly Anomaly Detected, [timestamp]*

*Trigger:* [metric] moved [delta]pts ([last]% → [this]%) week over week

*Metric tree decomposition:*
  • Streak-break rate: [last]% → [this]% ([↑/↓] [delta]pts) [(meaningful)]
  • Sessions in week 1: [last] → [this] ([↑/↓] [delta]%) [(meaningful)]
  • Push opt-in rate: [last]% → [this]% ([↑/↓] [delta]pts) [(meaningful)]

*Top 3 hypotheses:*
  1. [text] ([likelihood], confidence [N]/10)
  2. [text] ([likelihood], confidence [N]/10)
  3. [text] ([likelihood], confidence [N]/10)

*SQL to confirm hypothesis 1:*
```[sql]```

Logged to outcome-log.md. Run this query and reply with the output — I'll interpret.
```

**Low-confidence variant (stopped at Step 3):**

```
:grey_question: *Streakly Anomaly Detected — Low Confidence, [timestamp]*

*Trigger:* [metric] moved [delta]pts ([last]% → [this]%) week over week

*Metric tree decomposition:*
  • [driver]: [delta] [unit] [(meaningful)]
  ...

*No hypothesis cleared the confidence bar.* Best guess: "[top hypothesis text]" at [N]/10 — below the 6/10 threshold needed to auto-generate SQL and page the team.

Flagging for manual review rather than guessing further. Logged to outcome-log.md.
```

## 4. Simulated Test — 4-Point Retention Drop, End to End

```bash
cd agents
python3 anomaly_diagnosis.py simulate-drop
```

Uses n=5000 (approximating real weekly active volume per `data/experiment-design.md`'s 85,000-WAU context) rather than the 100-user pilot cohort in `data/` — at that pilot scale, this same 4-point move would not clear the adaptive threshold and would stop at Step 1 instead (verified separately below). Real output, captured 2026-09-17:

```
[Step 1] PASS — Day-7 retention moved -4.0pts, over the 1.9pt threshold. Continuing.
[Step 2] PASS — 3 drivers showed meaningful movement. Continuing.
[Step 3] PASS — top hypothesis confidence 8/10 > 6. Continuing.

:mag: *Streakly Anomaly Detected, Tue May 13, 8:47am*

*Trigger:* Day-7 retention moved -4pts (39% → 35%) week over week

*Metric tree decomposition:*
  • Streak-break rate: 22% → 29% (↑ 7pts) (meaningful)
  • Sessions in week 1: 4.1 → 3.2 (↓ 22.0%) (meaningful)
  • Push opt-in rate: 54% → 51% (↓ 3pts) (meaningful)

*Top 3 hypotheses:*
  1. Push notification delivery/engagement issue — correlates with the session drop. (high likelihood, confidence 8/10)
  2. New-user cohort quality shift (e.g. a lower-intent acquisition channel) driving more early streak breaks. (medium likelihood, confidence 6/10)
  3. Product/copy regression (e.g. a recent deploy touching the streak-reset or comeback flow) not explained by the instrumented drivers above. (low likelihood, confidence 3/10)

*SQL to confirm hypothesis 1:*
SELECT date, COUNT(*) AS push_sent, SUM(delivered) AS push_delivered,
       AVG(opened) AS open_rate
FROM streakly_notifications
WHERE sent_date >= CURRENT_DATE - 7
GROUP BY date
ORDER BY date;

Logged to outcome-log.md. Run this query and reply with the output — I'll interpret.

[Step 5] Logged to agents/outcome-log.md.
```

This matches the spec's worked example almost exactly (it was built to). I also verified the other two stop paths by hand, since "runs correctly end to end" should mean all three exits, not just the happy path:

- **Step 2 stop (inconclusive):** same threshold-clearing move, but only streak-break rate moved meaningfully (sessions and push opt-in held flat) → `[Step 2] Only 1 driver(s) showed meaningful movement (need >=2). Flagging inconclusive, stopping.`
- **Step 3 stop (low confidence):** streak-break rate and sessions moved meaningfully, but push opt-in didn't (only -1pt) → hypothesis 1 downgrades to 5/10 (no push corroboration), hypothesis 2 lands at exactly 6/10 — not `> 6` — so it correctly stops with the low-confidence Slack variant instead of forcing a top pick.

**I also ran the real chain**, via `python3 metric_pulse.py test-run` against this repo's actual data (week 5 vs. week 4) — not just the simulated scenario. Day-7 retention's real +34pt move passed Steps 1-2, but correctly stopped at Step 3 with low confidence: real sessions moved *up* 40.6% that week (not down), so the notification-issue hypothesis wasn't even generated — the rules didn't force a plausible-sounding but wrong answer just because a hypothesis slot needed filling. Streak-break rate's real +10pt move stopped at Step 1 (under its own 13.8pt threshold). Both runs are in `agents/outcome-log.md` alongside the simulated ones, with today's date.

## 5. Where This Still Needs a Human

`outcome-log.md`'s "what actually happened" column is a placeholder by design — this loop generates and ranks hypotheses, it doesn't confirm them. Step 4's SQL is written for a real production schema (`streakly_notifications`, `streakly_users`) that doesn't exist in this repo's local CSVs; running it and interpreting the result is still on you, exactly as the spec's own worked example ends: "Run this query and reply with the output. I'll interpret."
