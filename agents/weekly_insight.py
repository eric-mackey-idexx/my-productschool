#!/usr/bin/env python3
"""
Weekly Insight Report Agent — Streakly

Pulls three sources into a 3-2-1 report:
  1. Retention metrics (data/*.csv, via metric_pulse.py's own computation)
  2. Sprint completions this week (change_log.md)
  3. Top NPS themes (research/nps-analysis.md)

Output:
  - Done this week      (3 bullets, from change_log.md's most recent entries)
  - Changed this week    (2 bullets, retention/break-rate deltas from data/)
  - Watch next week      (1 bullet — see pick_watch_item() below)

"Watch next week" isn't a free-form guess: it reuses agents/metric_pulse.py's
own alert check and agents/anomaly_diagnosis.py's own hypothesis rules. If
either overall metric alerted this week, the watch item is that diagnosis's
top hypothesis (or an honest "cause unclear" if the diagnosis loop itself
stopped early). Only if NEITHER metric alerted does this fall back to the
#1 NPS theme by frequency — the standing signal, not a new one.

Usage:
    python3 weekly_insight.py [--data-dir PATH] [--repo-root PATH] [--dry-run]
"""

import argparse
import datetime
import os
import re
import sys

import anomaly_diagnosis
import metric_pulse


def parse_change_log(path):
    """Very small markdown-table parser: date-prefixed rows only, matching
    change_log.md's actual format (| YYYY-MM-DD | change | why |)."""
    rows = []
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) < 2:
                continue
            if not date_re.match(parts[0]):
                continue  # skips the header row and the --- separator row
            rows.append({"date": parts[0], "change": parts[1], "why": parts[2] if len(parts) > 2 else ""})
    return rows


def condense(text, max_len=140):
    """First clause of a change_log entry, not the whole paragraph."""
    for sep in [" — ", "; ", ". "]:
        if sep in text:
            head = text.split(sep)[0]
            if len(head) <= max_len:
                return head
    return text if len(text) <= max_len else text[:max_len].rsplit(" ", 1)[0] + "..."


def done_this_week(change_log_path, n=3):
    rows = parse_change_log(change_log_path)
    if not rows:
        return []
    dates_present = sorted({r["date"] for r in rows}, reverse=True)
    picked = []
    for d in dates_present:
        for r in reversed([r for r in rows if r["date"] == d]):
            picked.append(r)
            if len(picked) >= n:
                return picked[:n]
    return picked[:n]


def parse_nps_top_theme(nps_path):
    """Pull the #1 row of the 'Themes Mentioned More Than Once, Ranked by
    Frequency' table — the theme + how many of the 10 comments raised it."""
    with open(nps_path) as f:
        text = f.read()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("| 1 |"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 3:
                return cells[1], cells[2]  # theme, frequency
    return None, None


def changed_this_week(tw, lw):
    d7 = round(tw["overall"]["day7_retention_pct"] - lw["overall"]["day7_retention_pct"], 1)
    br = round(tw["overall"]["break_rate_pct"] - lw["overall"]["break_rate_pct"], 1)
    return [
        f"Day-7 retention: {lw['overall']['day7_retention_pct']}% → {tw['overall']['day7_retention_pct']}% ({d7:+.1f} pts WoW)",
        f"Streak-break rate: {lw['overall']['break_rate_pct']}% → {tw['overall']['break_rate_pct']}% ({br:+.1f} pts WoW)",
    ]


def pick_watch_item(tw, lw, nps_path):
    """Reuses metric_pulse's alert check and anomaly_diagnosis's own step
    functions directly (not run_diagnosis, which prints/posts) so this can
    compose a single clean sentence."""
    for label, key in [("Day-7 retention", "day7_retention_pct"), ("Streak-break rate", "break_rate_pct")]:
        ov_tw, ov_lw = tw["overall"], lw["overall"]
        passed1, delta, threshold = anomaly_diagnosis.step1_threshold_check(
            label, ov_tw[key], ov_tw["n_users"], ov_lw[key], ov_lw["n_users"]
        )
        if not passed1:
            continue

        passed2, drivers, n_meaningful = anomaly_diagnosis.step2_decompose(
            ov_tw["break_rate_pct"], ov_lw["break_rate_pct"],
            ov_tw["avg_sessions_per_user"], ov_lw["avg_sessions_per_user"],
            ov_tw["push_open_rate_pct"], ov_lw["push_open_rate_pct"],
        )
        if not passed2:
            return (f"{label} moved {delta:+.1f} pts (past its own alert threshold) but no driver combination "
                    f"explains why yet — inconclusive, see agents/outcome-log.md before it happens again.")

        hyps = anomaly_diagnosis.generate_hypotheses(drivers)
        top = hyps[0]
        if top["confidence"] > anomaly_diagnosis.MIN_TOP_CONFIDENCE:
            return (f"{label} moved {delta:+.1f} pts — leading hypothesis: \"{top['text']}\" "
                    f"(confidence {top['confidence']}/10). Full diagnostic in agents/outcome-log.md.")
        else:
            return (f"{label} moved {delta:+.1f} pts but no hypothesis cleared the confidence bar — "
                    f"flagged for manual review in agents/outcome-log.md.")

    theme, freq = parse_nps_top_theme(nps_path)
    if theme:
        return f"No retention or break-rate alert this week — the standing signal is still the NPS theme: {theme} ({freq})."
    return "No retention or break-rate alert this week, and no NPS theme file to fall back on."


def format_report_md(date_str, done, changed, watch):
    lines = [f"# Weekly Insight Report — {date_str}", ""]
    lines.append("## Done This Week")
    for d in done:
        lines.append(f"- {condense(d['change'])} (`{d['date']}`)")
    lines.append("")
    lines.append("## Changed This Week")
    for c in changed:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("## Watch Next Week")
    lines.append(f"- {watch}")
    lines.append("")
    lines.append("---")
    lines.append("*Sources: `data/*.csv` (via `agents/metric_pulse.py`), `change_log.md`, `research/nps-analysis.md`. "
                 "Watch item reuses `agents/anomaly_diagnosis.py`'s own alert/hypothesis logic — not a fresh guess.*")
    return "\n".join(lines)


def format_slack_321(date_str, done, changed, watch):
    lines = [f":clipboard: *Streakly Weekly Insight — {date_str}*", ""]
    lines.append("*Done (3):*")
    for d in done:
        lines.append(f"  • {condense(d['change'], 100)}")
    lines.append("")
    lines.append("*Changed (2):*")
    for c in changed:
        lines.append(f"  • {c}")
    lines.append("")
    lines.append(f"*Watch (1):* {watch}")
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


def main():
    parser = argparse.ArgumentParser(description="Streakly weekly insight report agent.")
    default_data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    default_repo_root = os.path.join(os.path.dirname(__file__), "..")
    parser.add_argument("--data-dir", default=default_data_dir)
    parser.add_argument("--repo-root", default=default_repo_root)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    change_log_path = os.path.join(args.repo_root, "change_log.md")
    nps_path = os.path.join(args.repo_root, "research", "nps-analysis.md")
    reports_dir = os.path.join(args.repo_root, "reports")

    data = metric_pulse.load_data(args.data_dir)
    weeks = sorted({int(r["cohort_week"]) for r in data["retention"]})
    this_period, last_period = weeks[-1], weeks[-2]
    tw = metric_pulse.compute_metrics(data, this_period)
    lw = metric_pulse.compute_metrics(data, last_period)

    done = done_this_week(change_log_path, n=3)
    changed = changed_this_week(tw, lw)
    watch = pick_watch_item(tw, lw, nps_path)

    date_str = datetime.date.today().isoformat()
    report_md = format_report_md(date_str, done, changed, watch)
    slack_msg = format_slack_321(date_str, done, changed, watch)

    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, f"{date_str}.md")
    with open(report_path, "w") as f:
        f.write(report_md)

    print(f"Report saved to {report_path}\n")
    print(slack_msg)

    if not args.dry_run:
        post_to_slack(slack_msg, os.environ.get("SLACK_WEBHOOK_URL"))


if __name__ == "__main__":
    sys.exit(main())
