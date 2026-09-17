#!/usr/bin/env python3
"""
Monday Retention Check — Streakly

Compares this week vs. last week on Day-7 retention, streak-break rate,
session volume, and push-notification open rate, then prints a plain-English
digest formatted for Slack.

Data source (today): the local CSVs in data/. "This week" / "last week" are
defined as the two most recent `cohort_week` values present in the data —
a stand-in for calendar weeks, since this dataset is a fixed course sample,
not a live production feed. In a real deployment, swap `load_week_data()`
for a query against a real warehouse/API filtered by actual calendar date,
and everything downstream is unchanged.

Usage:
    python3 monday_retention_check.py [--data-dir PATH] [--dry-run]

--dry-run prints the digest without attempting to post to Slack (the Slack
post itself is stubbed — see post_to_slack() — since no Slack webhook is
configured in this environment).
"""

import argparse
import csv
import os
import sys
from collections import defaultdict


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


def two_most_recent_weeks(retention_rows):
    weeks = sorted({int(r["cohort_week"]) for r in retention_rows})
    if len(weeks) < 2:
        raise ValueError("Need at least 2 cohort weeks of data to compare.")
    return weeks[-1], weeks[-2]  # this_week, last_week


def pct(numerator, denominator):
    return round(100.0 * numerator / denominator, 1) if denominator else 0.0


def metrics_for_week(data, week):
    week = str(week)
    retention_rows = [r for r in data["retention"] if r["cohort_week"] == week]
    user_ids_in_week = {r["user_id"] for r in retention_rows}
    n = len(retention_rows)

    day7 = pct(sum(1 for r in retention_rows if r["day_7"] == "true"), n)
    broke = pct(sum(1 for r in retention_rows if r["broke_streak_week1"] == "true"), n)

    sessions_this_week = [s for s in data["sessions"] if s["user_id"] in user_ids_in_week]
    avg_sessions = round(len(sessions_this_week) / n, 2) if n else 0.0

    nudges_this_week = [ng for ng in data["nudges"] if ng["user_id"] in user_ids_in_week]
    n_nudges = len(nudges_this_week)
    open_rate = pct(sum(1 for ng in nudges_this_week if ng["opened"] == "true"), n_nudges)

    variants = {u["variant"] for u in data["users"] if u["cohort_week"] == week and u["variant"]}

    return {
        "n_users": n,
        "day7_retention_pct": day7,
        "break_rate_pct": broke,
        "avg_sessions_per_user": avg_sessions,
        "total_sessions": len(sessions_this_week),
        "nudge_open_rate_pct": open_rate,
        "n_nudges": n_nudges,
        "has_ab_test": len(variants) > 1,
        "variants": sorted(variants),
    }


def build_digest(this_week, last_week, tw, lw):
    deltas = {
        "day7_retention": round(tw["day7_retention_pct"] - lw["day7_retention_pct"], 1),
        "break_rate": round(tw["break_rate_pct"] - lw["break_rate_pct"], 1),
        "avg_sessions": round(tw["avg_sessions_per_user"] - lw["avg_sessions_per_user"], 2),
        "nudge_open_rate": round(tw["nudge_open_rate_pct"] - lw["nudge_open_rate_pct"], 1),
    }

    # Headline is always Day-7 retention vs. last week, per the requested format.
    headline = (
        f"Day-7 retention: {tw['day7_retention_pct']}% "
        f"({'+' if deltas['day7_retention'] >= 0 else ''}{deltas['day7_retention']} pts vs. week {last_week}'s {lw['day7_retention_pct']}%)"
    )

    # Signal to watch = whichever OTHER metric moved the most, in relative terms.
    other_moves = {
        "streak-break rate": (deltas["break_rate"], f"{lw['break_rate_pct']}% -> {tw['break_rate_pct']}%"),
        "avg sessions/user": (deltas["avg_sessions"] * 10, f"{lw['avg_sessions_per_user']} -> {tw['avg_sessions_per_user']}"),  # scaled for comparability
        "push open rate": (deltas["nudge_open_rate"], f"{lw['nudge_open_rate_pct']}% -> {tw['nudge_open_rate_pct']}%"),
    }
    biggest = max(other_moves.items(), key=lambda kv: abs(kv[1][0]))
    signal_name, (signal_delta_scaled, signal_readable) = biggest

    if tw["has_ab_test"]:
        signal = f"Week {this_week} includes an active A/B test ({', '.join(tw['variants'])}) — the retention headline is blended across arms, not organic movement."
        action = (
            f"Before reporting the {deltas['day7_retention']:+.1f}-pt retention move, split it by variant "
            f"to confirm how much is the treatment working vs. sample composition — don't take the blended number to standup at face value."
        )
    else:
        signal = f"Biggest mover besides retention: {signal_name} ({signal_readable})."
        action = f"Look into what's driving the {signal_name} change this week before next Monday's check."

    return {
        "headline": headline,
        "signal": signal,
        "action": action,
        "this_week": this_week,
        "last_week": last_week,
        "tw": tw,
        "lw": lw,
        "deltas": deltas,
    }


def format_slack_message(digest):
    tw, lw = digest["this_week"], digest["last_week"]
    return (
        f":bar_chart: *Streakly Retention Digest — Week {tw} vs. Week {lw}*\n\n"
        f"*Headline:* {digest['headline']}\n\n"
        f"*Signal to watch:* {digest['signal']}\n\n"
        f"*Suggested action this week:* {digest['action']}\n\n"
        f"_Details: break rate {digest['tw']['break_rate_pct']}% (was {digest['lw']['break_rate_pct']}%) · "
        f"avg sessions/user {digest['tw']['avg_sessions_per_user']} (was {digest['lw']['avg_sessions_per_user']}) · "
        f"push open rate {digest['tw']['nudge_open_rate_pct']}% (was {digest['lw']['nudge_open_rate_pct']}%)_"
    )


def post_to_slack(message, webhook_url=None):
    """
    Stub. No Slack webhook is configured in this environment.
    In a real deployment: POST {"text": message} to a Slack Incoming Webhook URL,
    or use slack_sdk's WebClient.chat_postMessage with a bot token.
    """
    if not webhook_url:
        print("\n[post_to_slack] No SLACK_WEBHOOK_URL configured — not posting. "
              "Message that would have been sent is printed above.")
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


def main():
    parser = argparse.ArgumentParser(description="Monday retention check for Streakly.")
    parser.add_argument("--data-dir", default=os.path.join(os.path.dirname(__file__), "..", "data"))
    parser.add_argument("--dry-run", action="store_true", help="Print the digest, don't attempt to post to Slack.")
    args = parser.parse_args()

    data = load_data(args.data_dir)
    this_week, last_week = two_most_recent_weeks(data["retention"])
    tw = metrics_for_week(data, this_week)
    lw = metrics_for_week(data, last_week)
    digest = build_digest(this_week, last_week, tw, lw)
    message = format_slack_message(digest)

    print(message)

    if not args.dry_run:
        webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
        post_to_slack(message, webhook_url)


if __name__ == "__main__":
    sys.exit(main())
