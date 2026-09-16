# project.md

*Source: Slack thread (Marcus, Raj, Lena, you) re: Streakly Day-7 retention drop*

## What Streakly Is

Consumer habit + micro-learning app. Users pick a track and complete a 5-minute daily lesson; the streak they build is the core habit loop. Launched 4 years ago, Series B funded ($42M). 2.1M registered users, 340K monthly active users, growing 28% YoY on MAU.

## Current Phase

Discovery — diagnosing the cause of the Day-7 retention drop (48% → 39%) before committing to a solution. Team alignment meeting scheduled for Thursday.

## Squad & Key Stakeholders

- Marcus — Head of Product
- Raj — Engineering Lead
- Lena — Design Lead
- Eric Mackey (you) — Product Lead

## Problem Statement

Day-7 retention has dropped from 48% to 39% since the streak redesign shipped. The drop is sharpest among users who break their streak in week 1: once a user misses two days in a row, churn is almost double.

Current experience after a streak break: the app resets the streak to zero with no acknowledgment, and the "you lost your streak" push notification has a harsh tone. Users who tap through are dropped back at day zero with nothing offered.

Working hypothesis: users go passive after breaking a streak because it feels like failure and there's no graceful way back in — not a generic "keep going!" but something specific to their own progress.

Open question raised in thread, not yet resolved: is the core problem the streak reset itself, the notification tone/timing, or both?

Eric's take (Product Lead): the friction is mainly functional — it isn't easy for users to jump back in after a break — with some emotional component mixed in as well.

## Goals

*Proposed — not yet agreed by the team (pending Thursday alignment):*

- Reduce churn among users who break their streak in week 1 (sharpest-drop segment per Raj's data — missing two days nearly doubles churn)
- Recover Day-7 retention toward the pre-redesign baseline (48%)
- Give users a specific, personalized path back after a streak break, instead of a generic "keep going" message
- Reduce the harshness of the post-break experience (tone of the "you lost your streak" push, the jarring reset)

## Non-Goals

*Proposed — not yet agreed by the team (pending Thursday alignment):*

- Not a full redesign of the streak/notification system — scoped to the comeback moment after a break
- Not introducing new data sources or infrastructure (Raj confirmed current systems are sufficient)
- Not addressing retention drivers unrelated to streak breaks (e.g., users who never engage past onboarding)

## Success Metrics

*Proposed — not yet agreed by the team (pending Thursday alignment); no target values established:*

- Day-7 retention overall (baseline 48%, currently 39%)
- Churn rate among users who miss 2+ days in a row (the segment Raj identified)
- Comeback screen engagement — % of eligible users who complete the 60-second comeback lesson
- Streak-freeze usage — % of users who use the one-tap freeze, and retention comparison vs. non-freeze users
- Push-to-open rate on the "lost streak" notification, to check effect of any tone/content change

## Design: Comeback Screen

Concept proposed by Lena in thread, for users who break a streak. Instead of a cold reset to a default home screen, the user sees:

- **Best-streak stat** — their previous best streak, shown to acknowledge progress already made rather than just resetting to zero.
- **One 60-second comeback lesson** — a short lesson intended to rebuild momentum (specific lesson content/selection logic not discussed).
- **One-tap streak-freeze** — a single tap to protect the streak they've rebuilt (freeze rules not yet defined).

Per Raj: technically doable with existing systems and data sources. Still needed: the logic for who sees this screen, and the specific freeze rules.

Open/TBD (not discussed in thread):
- Targeting logic — which users see the Comeback screen and when
- Freeze rule details — how long a freeze lasts, how often it can be used, limits
- Copy/tone for the screen and any accompanying notification (thread only establishes that the *current* "you lost your streak" push has a harsh tone, not what the new copy should say)
- Visual layout/UI (this section is a written description only, not a mockup)

---
*This is a skeleton, not a finished PRD. To fill in before/at Thursday's meeting: agreed goals, non-goals, target metrics, and the open Design items above.*
