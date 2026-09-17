# Agent Registry — Comeback Coach

*2026-09-17. The three agents below, chained together, are what's being called "Comeback Coach" — a monitoring stack for the Streakly Comeback screen. None are deployed on a real schedule yet; all three are built, real, and manually verified against actual `data/` output (see each one's own spec doc).*

**One correction before the table:** the original ask describes the anomaly agent as triggering "on a 2pt move." What's actually built (`agents/metric_pulse.py`) triggers on a **sample-size-adaptive statistical threshold**, not a fixed 2pt cutoff — that fixed threshold was tried first and rebuilt after it fired 8 alerts, most of them noise, on this project's actual data volume (see `agents/metric-pulse.md`). The table below describes what's really running, not the original spec, so this registry doesn't quietly become wrong the moment someone reads the code.

## 1. Registry

| | Metric Pulse Agent | Anomaly-to-Hypothesis Agent | Weekly Insight Report |
|---|---|---|---|
| **Name** | `agents/metric_pulse.py` | `agents/anomaly_diagnosis.py` | `agents/weekly_insight.py` |
| **Trigger** | Scheduled (nightly snapshot + Monday digest) | Chained — called by the Pulse Agent's digest step for each overall metric; re-checks its own threshold, so it's a no-op unless that metric actually alerted | Scheduled (Friday) |
| **Trigger detail** | Adaptive threshold: ~2x the standard error of the week-over-week difference at that week's actual sample size — not a fixed point value | Same adaptive threshold, re-verified independently inside the agent (Step 1) so it's self-contained and testable on its own | Its "Watch" item reuses the Pulse/Anomaly agents' own check — see Connection Plan below |
| **Data sources** | `data/users.csv`, `data/retention.csv`, `data/sessions.csv`, `data/nudges.csv`; `agents/state/metric-pulse-history.json` (its own snapshot history) | Metric values and driver data handed to it by the Pulse Agent's `cmd_digest()` — see Connection Plan; no independent data pull | `data/*.csv` (via the Pulse Agent's own `load_data()`/`compute_metrics()`), `change_log.md`, `research/nps-analysis.md` |
| **Output format** | Slack digest: headline Day-7 retention + break rate, per-channel breakdown, list of metrics that crossed their adaptive threshold | Full diagnostic (trigger, metric-tree decomposition, top 3 ranked hypotheses, SQL to confirm) — or a "low confidence" variant if no hypothesis clears the bar, or a silent log if Step 1/2 didn't pass | 3-2-1 report: Done this week (3) / Changed this week (2) / Watch next week (1) |
| **Delivery channel** | Slack (stubbed — needs `SLACK_WEBHOOK_URL`) | Slack (same stub) + `agents/outcome-log.md` | `reports/YYYY-MM-DD.md` (versioned file) + Slack summary |
| **Schedule (intended real-world)** | Nightly snapshot (e.g. 2am); Monday 8am digest | Runs inside the Monday 8am digest, same moment as the Pulse Agent | Friday 4pm |
| **Owner** | Eric (PM) — day-to-day use and interpretation. Raj (Eng) for real data-pipeline wiring once this moves off local CSVs. | Eric (PM) for triage; Raj (Eng) explicitly in the loop for Step 4 — the agent writes the SQL, a human runs it and confirms | Eric (PM) |

## 2. Connection Plan

**Pulse → Anomaly: a direct function call, not a message queue or file handoff.** `metric_pulse.py`'s `cmd_digest()` computes this-week/last-week metrics once, builds its own alert list from them, and then — for each of the two overall metrics (Day-7 retention, streak-break rate) — calls `anomaly_diagnosis.run_diagnosis()` directly, passing:

```
metric_label, tw_pct, tw_n, lw_pct, lw_n,          # the metric itself
break_tw, break_lw,                                 # driver 1: streak-break rate
sessions_tw, sessions_lw,                           # driver 2: avg sessions/user
pushopt_tw, pushopt_lw                              # driver 3: push open rate
```

`run_diagnosis()` re-checks Step 1 (its own adaptive threshold) on arrival — so this call happens unconditionally for both metrics every run, and the "only triggers on alert" behavior is enforced by the callee re-verifying, not by the caller deciding in advance. That's a deliberate choice: it means the anomaly agent is independently testable and correct even if called wrong, rather than trusting the caller to gate it properly.

**Anomaly → Weekly Insight: reused logic, not a read of the anomaly agent's saved output — and that's worth flagging as a real gap, not glossing over.** `weekly_insight.py`'s `pick_watch_item()` does **not** read `agents/outcome-log.md` (the anomaly agent's actual persisted conclusion). Instead, it independently calls the same three step-functions (`step1_threshold_check`, `step2_decompose`, `generate_hypotheses`) itself, on the same week's data, and gets the same answer *because it's running identical logic*, not because it consulted the anomaly agent's actual output.

Right now these two paths can't diverge, because they're the same code called twice. But that's fragile: if `anomaly_diagnosis.py`'s rules change independently (e.g. via the Learning Loop's proposed heuristic updates), or if `outcome-log.md` ever needs to reflect a manually-corrected diagnosis, `weekly_insight.py` would silently keep computing its own version instead of reflecting the real record. **Recommended hardening, not yet done:** have `pick_watch_item()` read the most recent matching entry in `outcome-log.md` directly, falling back to a live recomputation only if no logged entry exists for that period.

## 3. What's Genuinely Not Built Yet

- None of the three agents are wired into a real scheduler (cron, n8n, or otherwise) — every run so far has been manual, for verification.
- No real Slack webhook is configured — every "delivery" so far has printed to the terminal.
- The Pulse Agent doesn't detect an active A/B-test week (unlike its sibling script `monday_retention_check.py`, which does) — see `agents/metric-pulse.md`'s own flagged caveat.
- The anomaly agent's hypothesis rules are unvalidated against real outcomes — see `agents/learning-loop.md`: 0 of 2 logged diagnoses are scoreable as of this writing.
