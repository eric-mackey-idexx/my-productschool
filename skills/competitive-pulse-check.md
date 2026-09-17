---
name: competitive-pulse-check
description: One-paste weekly check for new public moves from Streakly's competitors — searches the web for each competitor already in research/competitive-matrix.md, compares against what's already documented, and reports only what's actually new.
---

# Competitive Pulse Check

## Trigger prompt (paste this, nothing else needed)

> Run this week's competitive pulse check for Streakly.

## What Claude does, step by step

1. **Read the baseline.** Pull the competitor list and each one's "Notable recent changes" from `research/competitive-matrix.md` — this is what's already known and dated; the point of this run is to find what isn't in there yet.
2. **Search the web for each competitor** (Duolingo, Babbel, Elevate, Memrise, Headspace, or whatever list is current in the matrix) for news/updates from roughly the last 7-14 days — product announcements, pricing changes, new features, especially anything touching streaks, retention mechanics, or re-engagement, since that's what this project is actually watching for.
3. **Filter against the baseline.** Anything a search turns up that's already reflected in the matrix isn't "news" — only report what's genuinely new since that document was last touched.
4. **If a competitor has no new public moves, say that plainly** — "No new public moves found for [competitor]" — rather than restating their existing feature set to look like an update.
5. **Flag direct relevance to Streakly's own work.** If anything found touches streak-freeze, comeback/re-entry flows, or retention mechanics specifically — the same territory as the Comeback screen — call that out explicitly, since it's the one thing that would actually change this project's competitive framing.
6. Cite sources (links) for every claim, the same discipline `research/competitive-matrix.md` already follows — no uncited claims about a competitor.

## Output format

```markdown
## Competitive Pulse Check — [date]

- **Duolingo:** [new finding + source, or "No new public moves found"]
- **Babbel:** [...]
- **Elevate:** [...]
- **Memrise:** [...]
- **Headspace:** [...]

**Relevant to our work:** [anything touching streak-freeze/comeback/retention specifically, or "nothing this week"]
```

## Where it's saved

Appended to `research/competitive-pulse.md` (created on first run) — a running dated log. If a finding is significant enough to change the white-space argument in `research/competitive-matrix.md` (e.g. a competitor ships a free, built-in comeback mechanic), that's flagged clearly in the pulse-check output as worth a deliberate update to the matrix itself — not folded in silently.
