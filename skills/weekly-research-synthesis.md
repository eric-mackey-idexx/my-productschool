---
name: weekly-research-synthesis
description: One-paste weekly synthesis of new user feedback, support tickets, or NPS comments for Streakly — finds what's actually new since the last synthesis and says plainly when nothing is.
---

# Weekly Research Synthesis

## Trigger prompt (paste this, nothing else needed)

> Run this week's research synthesis for Streakly.

## What Claude does, step by step

1. **Establish the baseline.** Read `research/nps-analysis.md` (the existing themes/quotes/segments) and the most recent entry in `research/weekly-synthesis.md` if one exists — this is "what we already know," not the target of this run.
2. **Find anything new.** Check for feedback added since the last run: new or modified files under `research/`, any raw feedback dropped into a `research/inbox/` folder (create it if it doesn't exist — that's where new NPS exports, support-ticket dumps, or feedback pastes should go before running this), and anything referenced in `change_log.md` since the last synthesis date that looks like new user-facing feedback.
3. **If nothing new is found, say so plainly** — "No new feedback since [date]; themes unchanged" — rather than re-summarizing the existing NPS analysis as if it were a fresh finding. Stale-data-presented-as-new is worse than no update at all.
4. **If new material exists, analyze it the same way `research/nps-analysis.md` was built:** themes ranked by frequency, notable quotes, praise vs. complaints, and — critically — whether each new theme **confirms** an existing one (cite which) or is genuinely **new**. Flag sample size every time (this workspace treats 10 unattributed comments as directional, not statistical — carry that same caution forward).
5. Note any tension the new feedback creates with an existing finding (e.g. if new comments contradict the "streak reset is the top complaint" theme) rather than quietly averaging it away.

## Output format

```markdown
## Weekly Research Synthesis — [date]

**New since last synthesis:** [what was reviewed, or "nothing new — see below"]

**Confirms existing themes:**
- [theme] — [new quote/evidence], consistent with `research/nps-analysis.md`

**New themes (not previously seen):**
- [theme] — [quote/evidence] — flagged for the team, not yet corroborated elsewhere

**Sample size / caution:** [state it every time, don't let it go stale]
```

## Where it's saved

Appended to `research/weekly-synthesis.md` (created on first run) — a running log, one dated section per run. `research/nps-analysis.md` itself stays as the stable, canonical baseline document; it only gets edited if a synthesis run finds something significant enough to warrant updating the source analysis, and that's a separate, deliberate action, not automatic.
