# strategy.md

*Streakly — Day-7 Retention Recovery*

## Hypothesis

The 9-point Day-7 retention drop (48% → 39%) is concentrated in users who break their streak in week 1 — missing two days in a row nearly doubles churn (Raj).

Working hypothesis: users go passive after a streak break mainly due to **functional friction** — it isn't easy to jump back in, no clear path to resume — with **some emotional friction** mixed in (the cold reset feels like failure; the current "you lost your streak" push has a harsh tone) (Eric's read).

Proposed direction, not yet committed: a "Comeback screen" for users who break a streak — best-streak stat, one 60-second comeback lesson, one-tap streak-freeze — instead of a cold reset to zero (Lena's concept). Technically buildable on existing systems; no new data sources needed (Raj).

## Still Open

- Which is the primary driver — streak reset, notification tone/timing, or re-entry friction — to be aligned on Thursday before designing solutions
- Targeting logic (who sees the Comeback screen, when)
- Freeze rules (duration, frequency limits)
- Copy/tone for the screen and any revised notification
  - *Draft option (Eric, proposed, not team-agreed):* reassurance message on streak break — "it's ok, everyone gets busy — let's help you start a new streak by continuing where you left off." Addresses both emotional friction (reassurance, avoids "failure" tone) and functional friction (offers a concrete next step). Open question: "continuing where you left off" implies resuming at prior lesson/track position — need to confirm with Raj/Lena whether that's the intended mechanic vs. Lena's fresh 60-second comeback lesson concept, since they'd pull different data (last lesson vs. best-streak stat).

## Not Yet Validated

No user testing or quantitative data yet confirms this hypothesis — it's based on the Slack thread discussion, not research.
