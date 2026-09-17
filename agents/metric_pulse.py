#!/usr/bin/env python3
"""
Metric Pulse Agent — Streakly

Monitors Day-7 retention rate and streak-break rate, broken down by
acquisition channel (organic, paid, referral), against a fixed baseline
and a week-over-week alert threshold. Designed to run in two modes:

  snapshot  - (nightly) compute the current period's metrics and record
              them to a local history file. Idempotent: re-running the
              same night/period just overwrites that period's entry.
  digest    - (Monday 8am) read the last two recorded periods, compute
              week-over-week deltas, check the alert threshold, and
              print (or post) the Slack digest.

"This week" / "last week" are the two most recent `cohort_week` values in
data/retention.csv — a stand-in for calendar weeks, since this is a fixed
course dataset, not a live feed. See agents/metric-pulse.md for how this
maps onto a real nightly-cron + Monday-delivery schedule.

Usage:
    python3 metric_pulse.py snapshot [--data-dir PATH] [--history PATH]
    python3 metric_pulse.py digest   [--history PATH] [--dry-run]
    python3 metric_pulse.py test-run [--data-dir PATH]   # bootstrap + digest in one shot
"""

import argparse
import csv
import json
import math
import os
import sys

import anomaly_diagnosis

BASELINE_DAY7_PCT = 39.0
ALERT_Z = 2.0  # ~95% confidence the move isn't just sampling noise, at whatever N this week has
CHANNELS = ["organic", "paid", "referral"]


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_data(data_dir):
    return {
        "users": load_csv(os.path.join(data_dir, "users.csv")),
        "retention": load_csv(os.path.join(data_dir, "retention.csv")),
        "sessions": load_csv(os.path.join(data_dir, "sessions.csv")),
        "nudges": load_csv(os.path.join(data_dir, "nudges.csv")),
    }


def pct(numerator, denominator):
    return round(100.0 * numerator / denominator, 1) if denominator else 0.0


def channel_for_user(users, user_id):
    for u in users:
        if u["user_id"] == user_id:
            return u["acquisition_channel"]
    return None


def compute_metrics(data, week):
    """Overall + per-channel Day-7 retention and streak-break rate for one cohort_week."""
    week = str(week)
    user_channel = {u["user_id"]: u["acquisition_channel"] for u in data["users"] if u["cohort_week"] == week}
    rows = [r for r in data["retention"] if r["cohort_week"] == week]

    def rate(subset, field):
        n = len(subset)
        return pct(sum(1 for r in subset if r[field] == "true"), n)

    user_ids = set(user_channel.keys())
    week_sessions = [s for s in data["sessions"] if s["user_id"] in user_ids]
    week_nudges = [n for n in data["nudges"] if n["user_id"] in user_ids]

    overall = {
        "n_users": len(rows),
        "day7_retention_pct": rate(rows, "day_7"),
        "break_rate_pct": rate(rows, "broke_streak_week1"),
        # Driver metrics for the chained anomaly-diagnosis agent (agents/anomaly_diagnosis.py).
        "avg_sessions_per_user": round(len(week_sessions) / len(rows), 2) if rows else 0.0,
        "push_open_rate_pct": pct(sum(1 for n in week_nudges if n["opened"] == "true"), len(week_nudges)),
    }

    by_channel = {}
    for ch in CHANNELS:
        ch_rows = [r for r in rows if user_channel.get(r["user_id"]) == ch]
        by_channel[ch] = {
            "n_users": len(ch_rows),
            "day7_retention_pct": rate(ch_rows, "day_7"),
            "break_rate_pct": rate(ch_rows, "broke_streak_week1"),
        }

    return {"overall": overall, "by_channel": by_channel}


def load_history(history_path):
    if os.path.exists(history_path):
        with open(history_path) as f:
            return json.load(f)
    return {}


def save_history(history_path, history):
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2, sort_keys=True)


def cmd_snapshot(args):
    data = load_data(args.data_dir)
    weeks = sorted({int(r["cohort_week"]) for r in data["retention"]})
    history = load_history(args.history)
    for week in weeks:
        history[str(week)] = compute_metrics(data, week)
    save_history(args.history, history)
    print(f"Snapshot recorded for period(s): {weeks}. History file: {args.history}")


def delta(a, b):
    return round(a - b, 1)


def adaptive_threshold_pts(p1_pct, n1, p2_pct, n2, z=ALERT_Z):
    """
    Statistically-scaled alert threshold, in percentage points, for comparing two
    week-over-week proportions. Rather than a fixed cutoff (e.g. always 2pts,
    which fires on pure sampling noise whenever N is small), this computes the
    standard error of the difference between the two proportions and scales the
    threshold to it — so a small cohort needs a bigger move to alert, and a large
    one can alert on a genuinely small move, matching how confident we can
    actually be that the change is real rather than noise.

        SE = sqrt( p1(1-p1)/n1 + p2(1-p2)/n2 )   (proportions, not percentages)
        threshold = z * SE, converted back to percentage points

    z=2.0 is roughly a 95% confidence cutoff that the observed move isn't
    just sampling variation, at whatever N this week and last week happened
    to have.
    """
    if not n1 or not n2:
        return float("inf")  # can't assess confidence with no data — never alert on a metric with n=0
    p1, p2 = p1_pct / 100.0, p2_pct / 100.0
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return round(z * se * 100.0, 1)


def check_metric(alerts, label, tw_pct, tw_n, lw_pct, lw_n):
    d = delta(tw_pct, lw_pct)
    threshold = adaptive_threshold_pts(tw_pct, tw_n, lw_pct, lw_n)
    if abs(d) >= threshold:
        alerts.append(
            f"{label} moved {d:+.1f} pts week over week "
            f"(adaptive threshold at n={min(tw_n, lw_n)}: ±{threshold} pts)."
        )


def build_alerts(tw, lw):
    alerts = []
    ov_tw, ov_lw = tw["overall"], lw["overall"]
    check_metric(alerts, "Day-7 retention", ov_tw["day7_retention_pct"], ov_tw["n_users"],
                 ov_lw["day7_retention_pct"], ov_lw["n_users"])
    check_metric(alerts, "Streak-break rate", ov_tw["break_rate_pct"], ov_tw["n_users"],
                 ov_lw["break_rate_pct"], ov_lw["n_users"])
    for ch in CHANNELS:
        ch_tw, ch_lw = tw["by_channel"][ch], lw["by_channel"][ch]
        check_metric(alerts, f"[{ch}] Day-7 retention", ch_tw["day7_retention_pct"], ch_tw["n_users"],
                     ch_lw["day7_retention_pct"], ch_lw["n_users"])
        check_metric(alerts, f"[{ch}] Streak-break rate", ch_tw["break_rate_pct"], ch_tw["n_users"],
                     ch_lw["break_rate_pct"], ch_lw["n_users"])
    return alerts


def format_slack_message(this_period, last_period, tw, lw, alerts):
    vs_baseline = delta(tw["overall"]["day7_retention_pct"], BASELINE_DAY7_PCT)
    wow = delta(tw["overall"]["day7_retention_pct"], lw["overall"]["day7_retention_pct"])
    break_wow = delta(tw["overall"]["break_rate_pct"], lw["overall"]["break_rate_pct"])

    lines = []
    lines.append(f":pushpin: *Streakly Metric Pulse — Week {this_period} vs. Week {last_period}*")
    lines.append("")
    lines.append(
        f"*Day-7 retention:* {tw['overall']['day7_retention_pct']}% "
        f"({wow:+.1f} pts WoW, {vs_baseline:+.1f} pts vs. {BASELINE_DAY7_PCT}% baseline)"
    )
    lines.append(f"*Streak-break rate:* {tw['overall']['break_rate_pct']}% ({break_wow:+.1f} pts WoW)")
    lines.append("")
    lines.append("*By acquisition channel:*")
    for ch in CHANNELS:
        t = tw["by_channel"][ch]
        l = lw["by_channel"][ch]
        d7 = delta(t["day7_retention_pct"], l["day7_retention_pct"])
        db = delta(t["break_rate_pct"], l["break_rate_pct"])
        lines.append(
            f"  • *{ch}:* Day-7 {t['day7_retention_pct']}% ({d7:+.1f} pts) "
            f"· break rate {t['break_rate_pct']}% ({db:+.1f} pts)"
        )
    lines.append("")
    if alerts:
        lines.append(f":rotating_light: *ALERT — {len(alerts)} metric(s) moved more than their sample size can explain as noise:*")
        for a in alerts:
            lines.append(f"  • {a}")
    else:
        lines.append(":white_check_mark: No metric moved more than this week's sample size would explain as ordinary noise.")
    return "\n".join(lines)


def post_to_slack(message, webhook_url=None):
    """Stub — no Slack webhook is configured in this environment. See agents/monday-retention.md
    for the same pattern; real deployment just needs SLACK_WEBHOOK_URL set."""
    if not webhook_url:
        print("\n[post_to_slack] No SLACK_WEBHOOK_URL configured — not posting. Message printed above.")
        return False
    import json as _json
    import urllib.request

    req = urllib.request.Request(
        webhook_url,
        data=_json.dumps({"text": message}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status == 200


def cmd_digest(args):
    history = load_history(args.history)
    periods = sorted(int(p) for p in history.keys())
    if len(periods) < 2:
        print(f"Need at least 2 recorded periods to build a digest; have {periods}.", file=sys.stderr)
        return 1
    this_period, last_period = periods[-1], periods[-2]
    tw, lw = history[str(this_period)], history[str(last_period)]
    alerts = build_alerts(tw, lw)
    message = format_slack_message(this_period, last_period, tw, lw, alerts)
    print(message)
    if not args.dry_run:
        post_to_slack(message, os.environ.get("SLACK_WEBHOOK_URL"))

    # Chain to the anomaly-diagnosis agent — it only actually does anything if the
    # metric in question crosses ITS OWN adaptive threshold (re-checked inside
    # run_diagnosis's Step 1), so calling it for both overall metrics unconditionally
    # is safe: it's a no-op log-and-stop for whichever one didn't alert.
    for label, tw_key, lw_key in [("Day-7 retention", "day7_retention_pct", "day7_retention_pct"),
                                    ("Streak-break rate", "break_rate_pct", "break_rate_pct")]:
        print(f"\n--- Anomaly diagnosis check: {label} ---")
        anomaly_diagnosis.run_diagnosis(
            metric_label=label,
            tw_pct=tw["overall"][tw_key], tw_n=tw["overall"]["n_users"],
            lw_pct=lw["overall"][lw_key], lw_n=lw["overall"]["n_users"],
            break_tw=tw["overall"]["break_rate_pct"], break_lw=lw["overall"]["break_rate_pct"],
            sessions_tw=tw["overall"]["avg_sessions_per_user"], sessions_lw=lw["overall"]["avg_sessions_per_user"],
            pushopt_tw=tw["overall"]["push_open_rate_pct"], pushopt_lw=lw["overall"]["push_open_rate_pct"],
            dry_run=args.dry_run,
        )
    return 0


def cmd_test_run(args):
    """Bootstrap: snapshot every period currently in the data, then run the digest
    on the latest two — for manual verification before this is ever scheduled."""
    class NS:
        pass

    snap_args = NS()
    snap_args.data_dir = args.data_dir
    snap_args.history = args.history
    cmd_snapshot(snap_args)

    digest_args = NS()
    digest_args.history = args.history
    digest_args.dry_run = True
    return cmd_digest(digest_args)


def main():
    parser = argparse.ArgumentParser(description="Streakly metric pulse agent.")
    default_data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    default_history = os.path.join(os.path.dirname(__file__), "state", "metric-pulse-history.json")

    sub = parser.add_subparsers(dest="command", required=True)

    p_snap = sub.add_parser("snapshot", help="Nightly: record current period metrics.")
    p_snap.add_argument("--data-dir", default=default_data_dir)
    p_snap.add_argument("--history", default=default_history)
    p_snap.set_defaults(func=cmd_snapshot)

    p_dig = sub.add_parser("digest", help="Monday 8am: build and post the Slack digest.")
    p_dig.add_argument("--history", default=default_history)
    p_dig.add_argument("--dry-run", action="store_true")
    p_dig.set_defaults(func=cmd_digest)

    p_test = sub.add_parser("test-run", help="Bootstrap history from data/ and print a digest, for manual verification.")
    p_test.add_argument("--data-dir", default=default_data_dir)
    p_test.add_argument("--history", default=default_history)
    p_test.set_defaults(func=cmd_test_run)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
