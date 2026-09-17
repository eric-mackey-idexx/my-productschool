# Streakly Comeback Prototype

A click-through HTML prototype of the "comeback" moment after a user breaks their streak. Built from [pm-brief.md](../pm-brief.md).

## How to open

Double-click `index.html`, or open it directly in any browser (Chrome, Safari, etc.) — no server or install needed. Works on desktop or mobile; the layout is a fixed phone-frame mockup.

## What it shows (4 screens, tap through)

1. **Streak reset** — soft acknowledgment that the streak broke, no harsh "you lost your streak" language.
2. **Comeback screen** — the core of this brief: reassurance ("it's okay, everyone gets busy"), the user's best-streak stat for encouragement, a reminder of where the streak stopped (last lesson), and two CTAs: continue, or maybe later.
3. **Confirmation** (via "Continue where I left off") — the streak continues from the selected persona's pre-break streak (a separate value from their best-streak stat), not a reset to Day 1 — this keeps the payoff consistent with the "pass to connect your streak" promise on screen 2.
4. **Deferred** (via "Maybe later") — a distinct screen ("No worries. Come back when you are ready...") that does not start a new streak day, unlike screen 3.

Tap "Restart demo" (screen 3) or "Got it" (screen 4) to loop back and show someone else.

## What this is / isn't

- Static prototype for gut-check reactions from users or the team today. No login, no backend, no real streak data — every persona's best-streak stat, last-lesson reminder, and pre-break-streak continuation are hardcoded placeholders. Per `04-team/spec-readiness.md`, the continuation counter is meant to resume from `preBreakStreak`, a value distinct from `bestStreak` — the prototype now tracks both separately (they happen to be equal for these three personas, but the fields are no longer conflated in code).
- Not wired to Lena's full Comeback screen concept from `project.md` (60-second comeback lesson, one-tap streak-freeze) — this brief scoped only to the welcome-back/encouragement moment. Those remain open items in `strategy.md`.
- Visual style is a generic warm/rounded mobile aesthetic, **not** sourced from an actual Streakly brand or style guide (none exists in this repo) — treat colors/type/layout as placeholder, not final design.

## Suggested use with users today

Show screens 1→2→3 in order, then ask: does screen 2's message feel reassuring or dismissive? Does "continue where I left off" read as clear next step? Capture reactions in `03-build/build.md`'s iteration log.
