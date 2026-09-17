# Weekly Insight Report Agent — Streakly

*2026-09-17. Pulls retention metrics, sprint completions, and NPS themes into a 3-2-1 report — Done this week, Changed this week, Watch next week — saved to `reports/` and posted to Slack.*

## Spec, as given

| | |
|---|---|
| Sources | Retention metrics (`data/`), sprint completions (`change_log.md`), top NPS themes (`research/nps-analysis.md`) |
| Output | Done this week (3 bullets) · Changed this week (2 bullets) · Watch next week (1 bullet) |
| Delivery | `reports/YYYY-MM-DD.md` + Slack 3-2-1 summary |
| Schedule | Every Friday at 4pm, in the real world |

## 1. The Agent Script

`agents/weekly_insight.py` — pulls each source with a distinct, honest method rather than treating all three the same way:

- **Done this week** — parses `change_log.md`'s own markdown table (no new dependency; it's already the project's real chronological log) and takes the 3 most recent entries, condensed to their first clause. If the most recent date has fewer than 3 entries, it backfills from the next most recent date rather than padding with something unrelated.
- **Changed this week** — **reuses `agents/metric_pulse.py`'s own `load_data()`/`compute_metrics()`**, not a separate computation. The two bullets are always Day-7 retention and streak-break rate, week over week — the same two metrics `metric_pulse.py` already watches.
- **Watch next week** — the one bullet that required real design work; see below.

## How "Watch Next Week" Is Actually Chosen

This is not a free-form judgment call each time — it's a fixed decision procedure that **reuses `agents/anomaly_diagnosis.py`'s own step functions directly** (`step1_threshold_check`, `step2_decompose`, `generate_hypotheses` — not `run_diagnosis()`, which prints/posts rather than returning a value):

1. Check both overall metrics (Day-7 retention, streak-break rate) against their own adaptive alert threshold, exactly as `metric_pulse.py` would.
2. If one alerted, run it through the same Step 2 (driver decomposition) and Step 3 (hypothesis generation) the anomaly-diagnosis agent uses:
   - If Step 2 finds fewer than 2 meaningful drivers: the watch item is an honest "alert fired, cause unclear" — not a forced explanation.
   - If Step 3's top hypothesis clears the confidence bar: the watch item is that hypothesis, by name.
   - If Step 3's top hypothesis doesn't clear the bar: the watch item says so plainly, pointing at `agents/outcome-log.md`.
3. **Only if neither metric alerted** does this fall back to the #1 NPS theme by frequency in `research/nps-analysis.md`. This is the standing signal, not manufactured news — worth knowing which case produced the watch item, since the report doesn't distinguish them by wording alone if you're skimming.

This means the weekly insight report and the anomaly diagnosis agent can never quietly disagree with each other — there's one source of truth for "did something alert," reused, not reimplemented.

## 2. Run It Manually to Verify

```bash
cd agents
python3 weekly_insight.py --dry-run
```

Real output from this repo's actual data, captured 2026-09-17:

```
Report saved to reports/2026-09-17.md

:clipboard: *Streakly Weekly Insight — 2026-09-17*

*Done (3):*
  • Built `agents/anomaly_diagnosis.py` + spec: a 5-step diagnostic loop (threshold check → metric-tree...
  • Built `agents/metric_pulse.py` + spec (nightly `snapshot` / Monday `digest` split, channel...
  • Built `agents/monday_retention_check.py` + spec

*Changed (2):*
  • Day-7 retention: 27.0% → 61.0% (+34.0 pts WoW)
  • Streak-break rate: 35.0% → 45.0% (+10.0 pts WoW)

*Watch (1):* Day-7 retention moved +34.0 pts but no hypothesis cleared the confidence bar — flagged for manual review in agents/outcome-log.md.
```

The full report (with sources footer) is written to `reports/2026-09-17.md`.

**Read before scheduling this for real:**
- **The "Done" bullets are only as current as `change_log.md`.** Before this test run, `change_log.md` hadn't been updated since 2026-09-16 despite a full day of work on 2026-09-17 — I backfilled 14 missing entries before running this agent, or its first real report would have said almost nothing happened this week. This agent doesn't fix a stale log; it just faithfully reports what's in it, gaps included.
- **The condense() truncation is a simple heuristic** (break at the first " — ", "; ", or ". ", else hard-truncate at ~140 chars) — long `change_log.md` entries without an early natural break point (like the anomaly-diagnosis one above) truncate mid-clause rather than at a clean boundary. Cosmetic, not wrong, but worth knowing before it shows up in a real Friday report.
- **This week's "Watch" item is a real, honest non-answer**, not a demo failure: the +34pt retention move is genuinely a low-confidence case (see `agents/anomaly-diagnosis.md`) because real sessions moved *up* that week, which doesn't fit the rule table's "notification issue" pattern. A future week with a cleaner signal (or no alert at all, falling back to the NPS theme) would look different — worth re-running this once such a week exists in the data, the same caveat `agents/metric-pulse.md` already carries.

## 3. Wiring This Up for Real

Same three options as the other agents in this folder, at the same effort levels:

- **Python + cron** — `0 16 * * 5 cd /path/to/repo/agents && python3 weekly_insight.py` (Friday, 4pm). Swap `metric_pulse.load_data()`'s CSV reads for a real warehouse query; point `change_log_path`/`nps_path` at wherever those actually live in production (a real changelog system, a real NPS export) instead of local markdown files.
- **n8n** — a Friday 4pm Cron trigger calling the same three data pulls (a database node for retention, a changelog/Jira API node for completions, an NPS-export node for themes) into a Function node running the same "Watch" decision procedure, then a Slack node.
- **A developer ticket** — hand `agents/weekly_insight.py` and this doc to whoever owns the reporting pipeline as the reference implementation; the real integration points (a real changelog API, a real NPS pipeline, a real Slack app) are outside what a local script can stand in for.
