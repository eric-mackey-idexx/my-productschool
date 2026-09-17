---
name: friday-status-update
description: One-paste Friday status update for Streakly — compiles what shipped, what's in progress, and what's blocked by reading the workspace itself, not by asking the user for notes.
---

# Friday Status Update

## Trigger prompt (paste this, nothing else needed)

> Run my Friday status update for Streakly.

## What Claude does, step by step

1. **Find the last status update.** Look at the bottom of `status-updates/log.md` for the most recent entry's date (or, if the file doesn't exist yet, use `git log` for the date of the earliest commit this week as the window start).
2. **Compile Shipped.** Read `change_log.md` for every entry since that date — each row is something that actually happened, in Eric's own words, so this section is close to a direct pull, not a re-summary.
3. **Compile In Progress.** Cross-check two things: (a) `git status` for anything modified/untracked but not yet committed, and (b) any doc created this week whose own content flags it as a draft or partial (e.g. "70% done," "not yet reviewed," "draft — proposed by Eric"). List what's actively being worked, not finished.
4. **Compile Blocked.** Pull from `CLAUDE.md`'s "Open Threads" section and any stakeholder profile's "open items" that are explicitly waiting on someone else's action (Raj's sizing estimate, Marcus's pending decisions, etc.) — only include things genuinely stuck on another person or decision, not just unfinished work (that belongs in In Progress).
5. If a section has nothing that qualifies, write "None this week" rather than omitting the section or padding it with unrelated items.

## Output format

```markdown
## Friday Status — [date]

**Shipped**
- [one line each, max 5]

**In Progress**
- [one line each, max 5]

**Blocked**
- [one line each — who/what it's waiting on]
```

## Where it's saved

Appended to `status-updates/log.md` (created on first run) — a running weekly log, newest entry at the bottom, same convention as `change_log.md`. Not overwritten week to week, so the history of status over time stays intact.
