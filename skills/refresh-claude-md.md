---
name: refresh-claude-md
description: One-paste refresh of CLAUDE.md so it reflects where the Streakly project actually stands — re-scans the workspace, updates only what's changed, and never silently drops something still true.
---

# Refresh CLAUDE.md

## Trigger prompt (paste this, nothing else needed)

> Update CLAUDE.md to reflect where the Streakly project actually stands.

## What Claude does, step by step

1. **Re-scan the workspace.** Read `change_log.md` for everything shipped since `CLAUDE.md`'s current "Status as of" date, run `git log`/`git status` for anything committed or still pending, and check whether any of the numbered module files (`01-orient/` … `06-systems/`) got filled in since the last refresh.
2. **Check "Open Threads" against reality.** For each item currently listed as open, check whether it's actually been resolved since (a decision made, an estimate given, a file committed). Remove or mark resolved anything that's no longer true; add anything genuinely new and still unresolved.
3. **Check the "Where Things Live" table against the real tree.** Add any new top-level file or folder that's appeared since the last refresh; don't remove an entry just because it wasn't touched recently — only remove one if the file is actually gone.
4. **Check the Glossary.** If new project-specific vocabulary has accumulated (a new named mechanic, a new recurring shorthand) that a fresh session would need defined, add it. Don't invent definitions for terms that only appeared once in passing.
5. **Update the "Status as of" line and date** to reflect the real current phase, not just a timestamp bump.
6. **Only change what's actually changed.** This file gets fully rewritten by this workflow, but that doesn't mean every section gets touched — if the product description, defaults, or "Never" list are still accurate, leave them as-is rather than rephrasing for the sake of it.
7. If something surfaced during the scan that looks like a genuinely new *pattern* of friction (not just one new fact) — e.g. a new recurring wrong-path issue, a new file-location convention that's drifted — flag it to the user rather than folding a structural change in silently.

## Output format

The updated `CLAUDE.md` itself, plus a short chat summary of what actually changed section by section (what was added, what was removed as resolved, what was left alone) — not a full re-read of the file, just the diff that matters.

## Where it's saved

`CLAUDE.md`, in place, at the project root. Unlike the other three workflows (which append to a running log), this one overwrites — `CLAUDE.md` is meant to describe the current state, not accumulate history, so an old "Status as of" line has no value once it's stale.
