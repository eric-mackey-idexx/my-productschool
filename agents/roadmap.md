# Comeback Coach — 6-Month Roadmap

*2026-09-17. One agent added per month, each building on a real gap the existing stack already surfaced — not a wishlist independent of what's actually been built. See `agents/registry.md` for what exists today (Month 0).*

## Month 0 (done) — Monitor + Diagnose + Report
Metric Pulse, Anomaly-to-Hypothesis, Weekly Insight — built, chained, manually verified. Not yet scheduled anywhere real.

## Month 1 — Deployment Agent
**Gap it closes:** all three Month-0 agents are real scripts that only run when a human remembers to type the command. Nothing here changes the *logic*; it wires the existing three into an actual cron/n8n schedule and sets up the real Slack webhook.

*Note: this month's plan originally included adding A/B-test detection to `metric_pulse.py` — that got pulled forward and done on 2026-09-17, the same day the Learning Loop's first real review found a diagnosis had missed exactly because of it (see `agents/outcome-log.md`). Left here as a record that the roadmap isn't fixed in stone — a real finding jumped the queue.*

## Month 2 — Outcome Confirmation Agent
**Gap it closes:** `agents/outcome-log.md` has a "what actually happened" column that's a placeholder by design — nobody is filling it in. This agent's one job: every time a diagnosis is logged, follow up N days later (Slack DM or scheduled check-in) asking "did hypothesis 1 turn out to be right?" and write the answer back into `outcome-log.md`. Without this, the Learning Loop (already built, Month 0) has nothing to score, forever.

## Month 3 — Learning Loop Automation
**Gap it closes:** the Learning Loop prompt exists (`agents/learning-loop.md`) but runs manually, and only produces a real result once Month 2 has fed it real outcomes. This turns it into a scheduled weekly job, and — once there's enough scored history — lets it actually *edit* `anomaly_diagnosis.py`'s confidence numbers automatically for high-confidence pattern changes, rather than just proposing them for manual approval.

## Month 4 — Segment Drill-Down Agent
**Gap it closes:** every alert and diagnosis so far treats "users" as one population, with acquisition-channel breakdown as the only cut `metric_pulse.py` does. Real diagnoses (like the paid-channel quality-shift hypothesis) need to check other cuts too — platform (iOS/Android), cohort tenure, whether the user has ever used the freeze/pass. This agent extends Step 2's metric-tree decomposition with a second dimension: not just *which driver* moved, but *which segment of users* is actually driving it.

## Month 5 — Experiment Watcher
**Gap it closes:** `data/experiment-design.md` already worked out what a properly powered follow-up test needs (~1,565 users/arm, 2-5 week duration). Nobody's watching for when that test is actually live, or checking its interim results against that pre-registered plan. This agent's job: once a real A/B test starts, track enrollment against the target sample size, flag if it's running long or short, and — the important discipline part — refuse to declare a result "significant" before the pre-committed sample size and duration are actually reached, so nobody peeks early and calls it.

## Month 6 — Cross-Feature Portfolio Agent
**Gap it closes:** everything built so far is scoped to one feature (the Comeback screen). By month 6, Streakly will presumably have shipped or tested other retention ideas too. This agent rolls Comeback Coach up a level: instead of one feature's Day-7 retention, it tracks a portfolio of active experiments/features against the same rigor (adaptive thresholds, hypothesis logging, outcome confirmation) this stack already applies to one — so "which of our 4 retention bets actually worked this quarter" has a real, evidence-backed answer instead of a gut-feel roundup.

## The Throughline

Each month fixes a specific, already-identified weakness in what came before it, in this order: **make it run automatically → give it real feedback → let it learn from that feedback → make its diagnoses sharper → make sure the tests behind it are run honestly → generalize past one feature.** None of these are invented needs — every one of them is a gap this session's own agents already flagged about themselves.
