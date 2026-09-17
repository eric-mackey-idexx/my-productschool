# Monday Retention Check — Agent Spec

*2026-09-17. Checks Streakly Day-7 retention and streak-break rate against last week's baseline, compares session counts and push notification open rates, and posts a plain-English digest to Slack — meant to run every Monday morning before standup.*

## Today vs. the real world

This spec and script are real and runnable against the data that actually exists in this repo (`data/*.csv`). Two things are stubbed rather than faked:

- **The schedule.** Nothing in this repo runs on a timer. In production this would be a cron job, an n8n workflow, or a scheduled Python job (e.g. `0 8 * * 1` — 8am every Monday). For now, you run it by hand (Step 2 below).
- **The Slack post.** No Slack webhook is configured in this environment, so `post_to_slack()` in the script is a real function with real POST logic, but it no-ops and prints the message instead of sending it, unless a `SLACK_WEBHOOK_URL` environment variable is actually set.

One more thing worth knowing before you rely on this: "this week" and "last week" are defined as the two most recent `cohort_week` values in `data/retention.csv` (5 and 4 right now), not real calendar weeks — this dataset is a fixed course sample, not a live feed with today's date in it. The comparison logic itself doesn't change when you point this at a real production data source; only `load_data()`'s two `load_csv()` calls need to become real queries filtered by actual date.

## 1. The Agent Script

`agents/monday_retention_check.py` — reads `data/users.csv`, `data/retention.csv`, `data/sessions.csv`, and `data/nudges.csv`, computes the four requested comparisons for the two most recent weeks, and builds the digest. Full source is in that file; the logic in brief:

- **Day-7 retention** and **streak-break rate** — straight from `retention.csv`, grouped by week.
- **Session counts** — average sessions per user that week (`sessions.csv` joined to that week's user cohort), including users with zero sessions in the denominator — a silent churner should pull the average down, not get excluded from it.
- **Push notification open rate** — `nudges.csv` joined to the same week's users.
- **A/B-test detection** — checks whether `users.csv`'s `variant` column has more than one non-empty value in the current week. If so, the script overrides the default "signal to watch" and "suggested action" to flag that the retention headline is blended across experiment arms, rather than reporting a misleadingly clean week-over-week number. This isn't a hardcoded special case for week 5 — it checks the live data every run, so it'll trigger correctly whenever a future week also happens to contain an active experiment.

## 2. Run It Manually to Verify

```bash
cd agents
python3 monday_retention_check.py --dry-run
```

`--dry-run` prints the digest and skips the Slack-posting step entirely (skip the flag once a real `SLACK_WEBHOOK_URL` is set, and it'll actually post). Real output from this repo's actual data, captured 2026-09-17:

```
:bar_chart: *Streakly Retention Digest — Week 5 vs. Week 4*

*Headline:* Day-7 retention: 61.0% (+34.0 pts vs. week 4's 27.0%)

*Signal to watch:* Week 5 includes an active A/B test (comeback, control) — the retention headline is blended across arms, not organic movement.

*Suggested action this week:* Before reporting the +34.0-pt retention move, split it by variant to confirm how much is the treatment working vs. sample composition — don't take the blended number to standup at face value.

_Details: break rate 45.0% (was 35.0%) · avg sessions/user 4.5 (was 3.2) · push open rate 22.2% (was 20.7%)_
```

That +34pt headline is real, but exactly the number `data/metric-diagnosis.md` already warned about — a meaningful share of it isn't attributable to the Comeback screen itself. This is the script catching that automatically, not a special case written in for this demo. Worth checking: run it again once a future week has no active experiment, to confirm the plain week-over-week path (no A/B caveat) also produces a sensible, non-generic "biggest mover" signal — this repo's data doesn't currently have two clean, back-to-back non-experiment weeks to demonstrate that branch.

## 3. Slack Message Template

The script's `format_slack_message()` produces exactly this shape every run — the four bracketed values are the only things that change week to week:

```
:bar_chart: *Streakly Retention Digest — Week [this_week] vs. Week [last_week]*

*Headline:* Day-7 retention: [X]% ([+/-]Y pts vs. week [last_week]'s [Z]%)

*Signal to watch:* [Biggest mover among break rate / sessions / push open rate — or the A/B-test caveat if one is active this week.]

*Suggested action this week:* [What to look into, tied directly to the signal above — not a generic "monitor closely."]

_Details: break rate [X]% (was [Y]%) · avg sessions/user [X] (was [Y]) · push open rate [X]% (was [Y]%)_
```

## Wiring This Up for Real (Not Done Here)

- **Schedule:** a cron entry (`0 8 * * 1 cd /path/to/repo/agents && python3 monday_retention_check.py`) or an n8n workflow with a Cron trigger node calling the same script.
- **Slack:** create an Incoming Webhook in the target Slack workspace, set `SLACK_WEBHOOK_URL` in the job's environment, drop the `--dry-run` flag.
- **Real data:** swap `load_data()`'s CSV reads for whatever the real Streakly analytics warehouse actually is (a SQL query filtered by real calendar-week dates instead of `cohort_week`) — `metrics_for_week()` and everything downstream doesn't need to change.
