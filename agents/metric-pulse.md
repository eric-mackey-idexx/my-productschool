# Metric Pulse Agent — Streakly

*2026-09-17. Monitors Day-7 retention and streak-break rate against a fixed baseline and an adaptive, sample-size-aware alert threshold, broken down by acquisition channel, delivered as a Monday-morning Slack digest.*

## Spec, as given (and one change made after the first test run)

| | |
|---|---|
| Metrics monitored | Day-7 retention rate, streak-break rate |
| Baseline | 39% Day-7 retention |
| Alert threshold | Originally specified as a fixed ±2 percentage points, week over week |
| Breakdown | By acquisition channel — organic, paid, referral |
| Output | Slack digest, plain-English |
| Schedule | Runs nightly; delivers Monday 8am |

**The fixed ±2pt threshold was rebuilt as an adaptive one after the first test run.** At this project's actual weekly volume (n≈100 overall, n≈33 per channel), ordinary sampling noise on a ~35% rate is already ±5-8 points — well past a fixed 2pt bar. The first test run below (pre-rebuild) fired 8 alerts, most of them noise. The threshold is now computed from the standard error of the week-over-week difference at whatever sample size that metric actually has that week (`adaptive_threshold_pts()` in the script — roughly a 95%-confidence cutoff, via `z=2.0`), so a small cohort needs a bigger move to alert, and the same script would tighten its own bar automatically once real weekly volume is in the thousands.

## 1. The Agent Script

`agents/metric_pulse.py` — three subcommands, matching the nightly-vs-Monday split in the spec:

- **`snapshot`** (the nightly job) — reads `data/users.csv` and `data/retention.csv`, computes Day-7 retention and streak-break rate overall and per channel for the current period, and writes/updates one entry in a small JSON history file (`agents/state/metric-pulse-history.json`). Re-running it the same night just overwrites that period's entry — safe to run every night without double-counting.
- **`digest`** (the Monday 8am job) — reads the history file, takes the two most recently recorded periods, computes week-over-week deltas for every metric (overall and per channel), checks each against its own adaptive threshold for that metric's sample size, and prints (or posts) the Slack message.
- **`test-run`** — bootstraps the history file from whatever's currently in `data/` (all 5 cohort weeks at once) and immediately runs the digest — this is the one to use for manual verification (Section 3), since it doesn't require actually waiting for multiple real nights to accumulate history.

As with `agents/monday_retention_check.py`, "this week"/"last week" are the two most recent `cohort_week` values in the data — a stand-in for real calendar weeks, since this dataset is a fixed sample, not a live feed. Swap `compute_metrics()`'s two `load_csv()` calls for a real warehouse query and nothing else in the file needs to change.

## 2. The Slack Message Template

```
:pushpin: *Streakly Metric Pulse — Week [this] vs. Week [last]*

*Day-7 retention:* [X]% ([+/-]Y pts WoW, [+/-]Z pts vs. 39.0% baseline)
*Streak-break rate:* [X]% ([+/-]Y pts WoW)

*By acquisition channel:*
  • *organic:* Day-7 [X]% ([+/-]Y pts) · break rate [X]% ([+/-]Y pts)
  • *paid:* Day-7 [X]% ([+/-]Y pts) · break rate [X]% ([+/-]Y pts)
  • *referral:* Day-7 [X]% ([+/-]Y pts) · break rate [X]% ([+/-]Y pts)

:rotating_light: *ALERT — N metric(s) moved more than their sample size can explain as noise:*
  • [metric] moved [+/-]Y pts week over week (adaptive threshold at n=[N]: ±T pts).
  ...
```
(If nothing crosses the threshold that week, the alert block is replaced by a single `:white_check_mark: No metric moved more than this week's sample size would explain as ordinary noise.` line — the digest never fires a false alarm just to have something to say, and it shows the threshold it actually used so the number is never a mystery.)

## 3. Run It Manually to Verify

```bash
cd agents
python3 metric_pulse.py test-run
```

Real output from this repo's actual data, captured 2026-09-17, after the adaptive-threshold rebuild:

```
:pushpin: *Streakly Metric Pulse — Week 5 vs. Week 4*

*Day-7 retention:* 61.0% (+34.0 pts WoW, +22.0 pts vs. 39.0% baseline)
*Streak-break rate:* 45.0% (+10.0 pts WoW)

*By acquisition channel:*
  • *organic:* Day-7 82.4% (+53.0 pts) · break rate 38.2% (-3.0 pts)
  • *paid:* Day-7 57.6% (+42.9 pts) · break rate 57.6% (+22.3 pts)
  • *referral:* Day-7 42.4% (+4.9 pts) · break rate 39.4% (+11.3 pts)

:rotating_light: *ALERT — 3 metric(s) moved more than their sample size can explain as noise:*
  • Day-7 retention moved +34.0 pts week over week (adaptive threshold at n=100: ±13.2 pts).
  • [organic] Day-7 retention moved +53.0 pts week over week (adaptive threshold at n=34: ±20.4 pts).
  • [paid] Day-7 retention moved +42.9 pts week over week (adaptive threshold at n=33: ±21.1 pts).
```

Before the rebuild, the fixed ±2pt threshold fired on all 8 metrics, including a -3.0pt organic break-rate move and a +22.3pt paid break-rate move that turned out to be just under its own adaptive bar (±23.8pts at that n) — noise by this sample size's own standard, not a real signal. The adaptive version cut that down to the 3 moves that are actually implausible as chance: +34 to +53 points is many multiples of what sampling noise could produce even at n≈33-100.

I also ran `snapshot` and `digest` as two separate calls (not just `test-run`) to confirm the state file genuinely persists between the nightly and Monday jobs rather than only working in the bootstrapped single-shot path — same output both ways, both before and after the rebuild.

**Update, 2026-09-17, later the same day:** the gap described in the paragraph below was real — and then it actually caused a confirmed wrong diagnosis (see `agents/outcome-log.md`'s Weekly Learning Loop Review). It's now fixed: `compute_metrics()` checks the `variant` column the same way `monday_retention_check.py` always did, and `agents/anomaly_diagnosis.py`'s hypothesis generation now ranks an active-experiment hypothesis above guesses whenever one is detected. Leaving the original paragraph below for the record, since it's what led to finding and fixing this the hard way — through a real miss, not a code review.

The 3 alerts from this test run are still real week-over-week moves, but they're still happening because week 5 is the Comeback screen A/B test cohort, not because of organic, unexplained retention change — `data/metric-diagnosis.md` already found part of that lift isn't attributable to the screen itself. ~~The adaptive threshold solves the noise problem (most of the 8 original alerts), not the "is this actually an experiment week" problem — this script still doesn't know a variant column exists, unlike `agents/monday_retention_check.py`'s explicit A/B-detection check.~~ (See update above — this is now fixed downstream, in the anomaly-diagnosis agent's hypothesis ranking, not by changing what metric_pulse itself alerts on.)

## 4. Wiring This Up for Real

Three ways this actually gets scheduled and shipped, roughly in order of effort:

- **Python + cron** — lowest effort, matches the script as written. Two crontab entries: `0 2 * * * cd /path/to/repo/agents && python3 metric_pulse.py snapshot` (nightly, 2am) and `0 8 * * 1 cd /path/to/repo/agents && python3 metric_pulse.py digest` (Monday 8am). Swap the CSV reads in `compute_metrics()` for a real warehouse query; set `SLACK_WEBHOOK_URL` in the cron environment.
- **n8n** — a Cron trigger node (nightly) calling a database/HTTP node feeding the same computation into a Function node, plus a second Cron trigger (Monday 8am) reading stored state and posting to a Slack node. Better fit if this needs to live alongside other no-code workflows a team can see and edit without touching Python.
- **A developer ticket** — if this needs to be a real production job (proper monitoring, retries, on-call visibility), this spec and script are the acceptance criteria for that ticket, not the deployment itself: hand `agents/metric_pulse.py` and this doc to whoever owns the analytics pipeline as the reference implementation and expected output, and let them wire it into the real scheduler/data warehouse/Slack app properly.
