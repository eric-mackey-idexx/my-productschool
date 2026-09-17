#!/usr/bin/env python3
"""
Anomaly Diagnosis Agent — Streakly

Chained to agents/metric_pulse.py: whenever the pulse agent's *overall*
Day-7 retention or streak-break rate alert fires (adaptive threshold
crossed), this runs a 5-step diagnostic loop and either posts a full
diagnosis to Slack or stops early and says why.

Step 1  Threshold check       — did the pulse agent actually alert on this metric?
Step 2  Metric tree decomposition — pull the 3 driver metrics; need >=2 to show
                                    "meaningful movement" or the loop stops as inconclusive.
Step 3  Hypothesis generation — 3 ranked, rule-based hypotheses with confidence
                                    scores; need top confidence > 6/10 or the loop
                                    stops with a "low confidence" Slack alert.
Step 4  SQL + Slack           — write the SQL to confirm the top hypothesis,
                                    post the full diagnostic to Slack.
Step 5  Log the call          — append hypotheses + confidence + an outcome
                                    placeholder to outcome-log.md.

Hypothesis generation here is a small, explicit, inspectable rule table (see
generate_hypotheses()) — not a model call. That's a deliberate v1 scope: it
covers the 3 driver-movement patterns this project has actually seen discussed
(notification/session drop, paid-channel quality shift, unexplained break-rate
move), and is easy to extend with more rules as new patterns show up. A real
production version might swap this step for an LLM call or a human-in-the-loop
review — the rest of the loop (thresholds, driver pull, SQL, Slack, logging)
doesn't need to change either way.

Usage:
    python3 anomaly_diagnosis.py diagnose --metric day7_retention \\
        --tw-pct 35 --tw-n 100 --lw-pct 39 --lw-n 100 \\
        --break-tw 29 --break-lw 22 --sessions-tw 3.2 --sessions-lw 4.1 \\
        --pushopt-tw 51 --pushopt-lw 54 [--dry-run]

    python3 anomaly_diagnosis.py simulate-drop     # the 4-point-drop scenario, end to end
"""

import argparse
import datetime
import math
import os
import sys

ALERT_Z = 2.0  # must match agents/metric_pulse.py's adaptive threshold
MEANINGFUL_RATE_PTS = 3.0       # driver screening bar for rate-type drivers (break rate, push opt-in)
MEANINGFUL_RELATIVE_PCT = 10.0  # driver screening bar for continuous drivers (sessions/user)
MIN_TOP_CONFIDENCE = 6  # per spec: must be > 6/10 to proceed to Step 4

OUTCOME_LOG = os.path.join(os.path.dirname(__file__), "outcome-log.md")


def adaptive_threshold_pts(p1_pct, n1, p2_pct, n2, z=ALERT_Z):
    """Same formula as metric_pulse.py — duplicated intentionally so this module
    can be tested standalone without importing pulse-agent internals."""
    if not n1 or not n2:
        return float("inf")
    p1, p2 = p1_pct / 100.0, p2_pct / 100.0
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return round(z * se * 100.0, 1)


# ---------------------------------------------------------------------------
# Step 1 — Threshold check
# ---------------------------------------------------------------------------

def step1_threshold_check(metric_label, tw_pct, tw_n, lw_pct, lw_n):
    """Returns (passed, delta, threshold). This mirrors the exact check
    agents/metric_pulse.py already does — the anomaly loop is only ever
    invoked when that check has already passed, but it's re-verified here
    so this module is self-contained and testable on its own."""
    delta = round(tw_pct - lw_pct, 1)
    threshold = adaptive_threshold_pts(tw_pct, tw_n, lw_pct, lw_n)
    passed = abs(delta) >= threshold
    return passed, delta, threshold


# ---------------------------------------------------------------------------
# Step 2 — Metric tree decomposition
# ---------------------------------------------------------------------------

def _rate_driver(name, tw, lw):
    d = round(tw - lw, 1)
    return {"name": name, "tw": tw, "lw": lw, "delta": d, "unit": "pts",
             "meaningful": abs(d) >= MEANINGFUL_RATE_PTS}


def _relative_driver(name, tw, lw):
    rel = round(100.0 * (tw - lw) / lw, 1) if lw else 0.0
    return {"name": name, "tw": tw, "lw": lw, "delta": rel, "unit": "% relative",
             "meaningful": abs(rel) >= MEANINGFUL_RELATIVE_PCT}


def step2_decompose(break_tw, break_lw, sessions_tw, sessions_lw, pushopt_tw, pushopt_lw):
    drivers = [
        _rate_driver("Streak-break rate", break_tw, break_lw),
        _relative_driver("Sessions in week 1", sessions_tw, sessions_lw),
        _rate_driver("Push opt-in rate", pushopt_tw, pushopt_lw),
    ]
    n_meaningful = sum(1 for d in drivers if d["meaningful"])
    passed = n_meaningful >= 2
    return passed, drivers, n_meaningful


# ---------------------------------------------------------------------------
# Step 3 — Hypothesis generation (explicit rule table, not a model call)
# ---------------------------------------------------------------------------

def generate_hypotheses(drivers):
    by_name = {d["name"]: d for d in drivers}
    sessions = by_name["Sessions in week 1"]
    pushopt = by_name["Push opt-in rate"]
    breakrate = by_name["Streak-break rate"]

    hyps = []

    # H1: notification/engagement issue — sessions and push opt-in both fell meaningfully.
    if sessions["meaningful"] and sessions["delta"] < 0 and pushopt["meaningful"] and pushopt["delta"] < 0:
        hyps.append({
            "text": "Push notification delivery/engagement issue — correlates with the session drop.",
            "confidence": 8,
            "why": "Both sessions and push opt-in moved meaningfully in the same direction — a plausible causal chain (fewer notifications landing -> fewer sessions -> worse retention).",
        })
    elif sessions["meaningful"] and sessions["delta"] < 0:
        hyps.append({
            "text": "Push notification delivery/engagement issue — sessions dropped, but push opt-in move alone doesn't confirm it.",
            "confidence": 5,
            "why": "Only one of the two corroborating drivers (sessions) moved meaningfully.",
        })

    # H2: cohort/channel quality shift — break rate worsened; flagged whenever break rate
    # is a meaningful driver, since channel-mix data isn't available inside this loop
    # (it lives in data/users.csv, joined separately — see agents/metric-pulse.md).
    if breakrate["meaningful"] and breakrate["delta"] > 0:
        hyps.append({
            "text": "New-user cohort quality shift (e.g. a lower-intent acquisition channel) driving more early streak breaks.",
            "confidence": 6,
            "why": "Streak-break rate rose meaningfully; channel-level attribution needs a follow-up query, not assumed here.",
        })

    # H3: catch-all — always offered, always low confidence, explicitly needs confirmation.
    hyps.append({
        "text": "Product/copy regression (e.g. a recent deploy touching the streak-reset or comeback flow) not explained by the instrumented drivers above.",
        "confidence": 3,
        "why": "Fallback hypothesis when the move isn't fully explained by session/notification/channel signals; requires manual confirmation (release log, QA) rather than a query.",
    })

    hyps.sort(key=lambda h: h["confidence"], reverse=True)
    return hyps[:3]


# ---------------------------------------------------------------------------
# Step 4 — SQL + Slack
# ---------------------------------------------------------------------------

def sql_for_hypothesis(top_hyp):
    text = top_hyp["text"]
    if "notification" in text.lower():
        return (
            "SELECT date, COUNT(*) AS push_sent, SUM(delivered) AS push_delivered,\n"
            "       AVG(opened) AS open_rate\n"
            "FROM streakly_notifications\n"
            "WHERE sent_date >= CURRENT_DATE - 7\n"
            "GROUP BY date\n"
            "ORDER BY date;"
        )
    if "cohort quality" in text.lower() or "channel" in text.lower():
        return (
            "SELECT acquisition_channel, COUNT(*) AS users, AVG(broke_streak_week1::int) AS break_rate\n"
            "FROM streakly_users\n"
            "WHERE signup_date >= CURRENT_DATE - 7\n"
            "GROUP BY acquisition_channel\n"
            "ORDER BY break_rate DESC;"
        )
    return (
        "SELECT deploy_id, deployed_at, description\n"
        "FROM release_log\n"
        "WHERE deployed_at >= CURRENT_DATE - 10\n"
        "ORDER BY deployed_at DESC;"
    )


def format_slack_diagnostic(metric_label, tw_pct, lw_pct, delta, drivers, hypotheses, sql, timestamp=None):
    timestamp = timestamp or datetime.datetime.now().strftime("%a %b %-d, %-I:%M%p").replace("AM", "am").replace("PM", "pm")
    lines = []
    lines.append(f":mag: *Streakly Anomaly Detected, {timestamp}*")
    lines.append("")
    lines.append(f"*Trigger:* {metric_label} moved {delta:+.0f}pts ({lw_pct:.0f}% → {tw_pct:.0f}%) week over week")
    lines.append("")
    lines.append("*Metric tree decomposition:*")
    for d in drivers:
        arrow = "↑" if d["delta"] > 0 else "↓"
        flag = " (meaningful)" if d["meaningful"] else ""
        if d["unit"] == "pts":
            lines.append(f"  • {d['name']}: {d['lw']}% → {d['tw']}% ({arrow} {abs(d['delta'])}pts){flag}")
        else:
            lines.append(f"  • {d['name']}: {d['lw']} → {d['tw']} ({arrow} {abs(d['delta'])}%){flag}")
    lines.append("")
    lines.append("*Top 3 hypotheses:*")
    for i, h in enumerate(hypotheses, 1):
        likelihood = "high" if h["confidence"] >= 7 else ("medium" if h["confidence"] >= 5 else "low")
        lines.append(f"  {i}. {h['text']} ({likelihood} likelihood, confidence {h['confidence']}/10)")
    lines.append("")
    lines.append(f"*SQL to confirm hypothesis 1:*\n```{sql}```")
    lines.append("")
    lines.append("Logged to outcome-log.md. Run this query and reply with the output — I'll interpret.")
    return "\n".join(lines)


def format_low_confidence_slack(metric_label, tw_pct, lw_pct, delta, drivers, top_hyp, timestamp=None):
    timestamp = timestamp or datetime.datetime.now().strftime("%a %b %-d, %-I:%M%p").replace("AM", "am").replace("PM", "pm")
    lines = []
    lines.append(f":grey_question: *Streakly Anomaly Detected — Low Confidence, {timestamp}*")
    lines.append("")
    lines.append(f"*Trigger:* {metric_label} moved {delta:+.0f}pts ({lw_pct:.0f}% → {tw_pct:.0f}%) week over week")
    lines.append("")
    lines.append("*Metric tree decomposition:*")
    for d in drivers:
        flag = " (meaningful)" if d["meaningful"] else ""
        lines.append(f"  • {d['name']}: {d['delta']:+} {d['unit']}{flag}")
    lines.append("")
    lines.append(
        f"*No hypothesis cleared the confidence bar.* Best guess: \"{top_hyp['text']}\" "
        f"at {top_hyp['confidence']}/10 — below the {MIN_TOP_CONFIDENCE}/10 threshold needed to auto-generate SQL and page the team."
    )
    lines.append("")
    lines.append("Flagging for manual review rather than guessing further. Logged to outcome-log.md.")
    return "\n".join(lines)


def post_to_slack(message, webhook_url=None):
    if not webhook_url:
        print("\n[post_to_slack] No SLACK_WEBHOOK_URL configured — not posting. Message printed above.")
        return False
    import json
    import urllib.request

    req = urllib.request.Request(
        webhook_url,
        data=json.dumps({"text": message}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status == 200


# ---------------------------------------------------------------------------
# Step 5 — Log the call
# ---------------------------------------------------------------------------

def log_outcome(metric_label, delta, hypotheses, stopped_at=None, log_path=OUTCOME_LOG):
    date_str = datetime.date.today().isoformat()
    lines = [f"\n## {date_str} — {metric_label} moved {delta:+.1f} pts\n"]
    if stopped_at:
        lines.append(f"**Loop stopped at:** {stopped_at}\n")
    else:
        lines.append("**Loop completed through Step 4 (SQL + Slack posted).**\n")
    lines.append("| Rank | Hypothesis | Confidence | What actually happened |")
    lines.append("|---|---|---|---|")
    for i, h in enumerate(hypotheses, 1):
        lines.append(f"| {i} | {h['text']} | {h['confidence']}/10 | _placeholder — fill in after investigating_ |")
    lines.append("")
    entry = "\n".join(lines)

    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write("# Anomaly Diagnosis Outcome Log\n\n"
                    "*Every anomaly-diagnosis run logs its hypotheses here. The \"what actually happened\" "
                    "column starts as a placeholder — fill it in once the real cause is confirmed, so this "
                    "log becomes a track record of how good the hypothesis-generation rules actually are.*\n")
    with open(log_path, "a") as f:
        f.write(entry)
    return log_path


# ---------------------------------------------------------------------------
# The full chained loop
# ---------------------------------------------------------------------------

def run_diagnosis(metric_label, tw_pct, tw_n, lw_pct, lw_n,
                   break_tw, break_lw, sessions_tw, sessions_lw, pushopt_tw, pushopt_lw,
                   dry_run=True, timestamp=None):
    # Step 1
    passed1, delta, threshold = step1_threshold_check(metric_label, tw_pct, tw_n, lw_pct, lw_n)
    if not passed1:
        print(f"[Step 1] {metric_label} moved {delta:+.1f}pts, under the {threshold}pt adaptive threshold. Logged, stopping.")
        log_outcome(metric_label, delta, [], stopped_at="Step 1 — below threshold")
        return

    print(f"[Step 1] PASS — {metric_label} moved {delta:+.1f}pts, over the {threshold}pt threshold. Continuing.")

    # Step 2
    passed2, drivers, n_meaningful = step2_decompose(break_tw, break_lw, sessions_tw, sessions_lw, pushopt_tw, pushopt_lw)
    if not passed2:
        print(f"[Step 2] Only {n_meaningful} driver(s) showed meaningful movement (need >=2). Flagging inconclusive, stopping.")
        log_outcome(metric_label, delta, [], stopped_at=f"Step 2 — inconclusive ({n_meaningful} driver moved)")
        return

    print(f"[Step 2] PASS — {n_meaningful} drivers showed meaningful movement. Continuing.")

    # Step 3
    hypotheses = generate_hypotheses(drivers)
    top = hypotheses[0]
    if top["confidence"] <= MIN_TOP_CONFIDENCE:
        print(f"[Step 3] Top hypothesis confidence {top['confidence']}/10 <= {MIN_TOP_CONFIDENCE}. Posting low-confidence alert, stopping.")
        message = format_low_confidence_slack(metric_label, tw_pct, lw_pct, delta, drivers, top, timestamp)
        print("\n" + message)
        if not dry_run:
            post_to_slack(message, os.environ.get("SLACK_WEBHOOK_URL"))
        log_outcome(metric_label, delta, hypotheses, stopped_at=f"Step 3 — low confidence ({top['confidence']}/10)")
        return

    print(f"[Step 3] PASS — top hypothesis confidence {top['confidence']}/10 > {MIN_TOP_CONFIDENCE}. Continuing.")

    # Step 4
    sql = sql_for_hypothesis(top)
    message = format_slack_diagnostic(metric_label, tw_pct, lw_pct, delta, drivers, hypotheses, sql, timestamp)
    print("\n[Step 4] Full diagnostic:\n")
    print(message)
    if not dry_run:
        post_to_slack(message, os.environ.get("SLACK_WEBHOOK_URL"))

    # Step 5
    log_path = log_outcome(metric_label, delta, hypotheses)
    print(f"\n[Step 5] Logged to {log_path}.")


def cmd_diagnose(args):
    run_diagnosis(
        args.metric, args.tw_pct, args.tw_n, args.lw_pct, args.lw_n,
        args.break_tw, args.break_lw, args.sessions_tw, args.sessions_lw,
        args.pushopt_tw, args.pushopt_lw, dry_run=args.dry_run,
    )


def cmd_simulate_drop(args):
    """The 4-point-drop scenario from the spec, run end to end with a fixed timestamp
    for reproducible output."""
    print("=== SIMULATED SCENARIO: Day-7 retention drop, 39% -> 35%, n=5000 both weeks ===")
    print("(n=5000 approximates real weekly active volume, per data/experiment-design.md's\n"
          " 85,000 WAU context — not the 100-user pilot cohort in data/. At that pilot scale,\n"
          " this exact same 4-point move would NOT clear the adaptive threshold; try\n"
          " --tw-n 1000 --lw-n 1000 via `diagnose` to see that stop at Step 1.)\n")
    run_diagnosis(
        metric_label="Day-7 retention",
        tw_pct=35, tw_n=5000, lw_pct=39, lw_n=5000,
        break_tw=29, break_lw=22,
        sessions_tw=3.2, sessions_lw=4.1,
        pushopt_tw=51, pushopt_lw=54,
        dry_run=True,
        timestamp="Tue May 13, 8:47am",
    )


def main():
    parser = argparse.ArgumentParser(description="Streakly anomaly diagnosis agent.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("diagnose", help="Run the diagnosis loop on a specific metric move.")
    p.add_argument("--metric", required=True)
    p.add_argument("--tw-pct", type=float, required=True)
    p.add_argument("--tw-n", type=int, required=True)
    p.add_argument("--lw-pct", type=float, required=True)
    p.add_argument("--lw-n", type=int, required=True)
    p.add_argument("--break-tw", type=float, required=True)
    p.add_argument("--break-lw", type=float, required=True)
    p.add_argument("--sessions-tw", type=float, required=True)
    p.add_argument("--sessions-lw", type=float, required=True)
    p.add_argument("--pushopt-tw", type=float, required=True)
    p.add_argument("--pushopt-lw", type=float, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_diagnose)

    p2 = sub.add_parser("simulate-drop", help="Run the fixed 4-point-drop scenario end to end.")
    p2.set_defaults(func=cmd_simulate_drop)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
