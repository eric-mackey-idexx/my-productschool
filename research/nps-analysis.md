# NPS Feedback Analysis — Streakly

*Source: 10 raw NPS comments (verbatim, unattributed). Sample size is small — treat as directional signal, not statistically robust.*

## 1–2. Themes Mentioned More Than Once, Ranked by Frequency

| Rank | Theme | Frequency | Quotes |
|------|-------|-----------|--------|
| 1 | Streak reset after a break feels punishing, with no graceful way back — drives disengagement and uninstalls | 7 of 10 | "reset to zero... felt pointless to start over"; "scorekeeper that punishes me"; "no way to recover it... other apps let you freeze a streak"; "home screen looks the same whether I'm on a 2-day streak or coming back after two weeks"; "make coming back easier instead of making me feel like I failed"; "the moment I lost my streak the whole thing lost its meaning"; "the second I lost it, I was done" |
| 2 | Notifications feel like nagging or arrive randomly, leading users to disable them | 2 of 10 | "daily reminder just started to feel like nagging"; "got three in one afternoon and just turned them all off" |

## 3. Praise vs. Complaints

**Praise**
- Onboarding/first week experience was "genuinely fun"
- Lesson content itself is well liked ("Love the lessons")

**Complaints**
- Streak reset to zero after a break feels punishing, not motivating
- No mechanism to protect or recover a streak (users explicitly compare to competitors' streak-freeze)
- Home screen gives no acknowledgment of where a user actually is (2-day streak vs. returning after weeks away)
- Losing a streak effectively ends engagement — several users stopped opening the app or deleted it entirely after a break
- Notifications are frequent/random enough that users disable them, even though (per one user) a well-timed, useful nudge would bring them back
- The streak is described as the *only* thing keeping some users engaged — a single point of failure

## 4. Top 3 Actionable Issues

1. **No streak-recovery mechanism.** Users explicitly want a way to protect a streak after a miss (streak-freeze), and cite competitors who already offer this.
2. **No acknowledgment of the user's actual state on return.** The home screen treats a 2-day streak and a 2-week absence identically — there's no personalized re-entry point.
3. **Notification cadence/logic is off.** Frequency and randomness are causing opt-outs, which removes the one channel that could otherwise pull lapsed users back.

## Tensions / Contradictions

- **Notification frequency: "less" vs. "more, but better."** Some users say notifications feel like nagging or arrive randomly and got turned off. Another says they forget the app exists and would return if pulled back "with something useful." This isn't simply "reduce notifications" — current ones are frequent/random but not relevant, while what's missing is a well-targeted one. Cutting volume could fix the nagging complaint and worsen the re-engagement complaint.
- **The streak is both the hook and the cliff.** One user says the streak is "the only thing keeping me engaged," then finishes: "the second I lost it, I was done." Combined with users who abandoned the app specifically because of the streak reset, the same mechanic drives engagement for some and churn for others — often the same person, at different points. Softening the reset (freeze, partial credit) risks diluting the thing that makes the streak motivating in the first place; this feedback alone doesn't resolve that trade-off.
- **Fun at first, punishing later.** One user's own arc goes from "genuinely fun" in week one to feeling nagged by reminders — suggesting the issue may be escalation/timing over the lifecycle rather than the mechanic existing at all, which points to a different fix than simply removing reminders.

## Possible Customer Segments

*Based only on stated behavior/motivation in these 10 comments — no demographic or usage data exists to validate this, so treat as a directional typology, not a confirmed segmentation.*

- **High-stakes streak owners** — built a meaningful streak and its loss caused total disengagement or deletion ("20-day streak... haven't opened the app since"; "deleted after 3 weeks... lost its meaning"; "the only thing keeping me engaged... the second I lost it, I was done"). Extrinsic, streak-centric motivation — highest risk of total loss on a single miss. Likely the segment behind the Day-7 drop.
- **Content-driven lapsers** — like the product for its own sake but disengage through forgetting, not punishment ("Love the lessons. I just forget it exists... If it pulled me back with something useful I'd come back"). Needs a different fix than Segment 1: relevance of re-engagement, not a comeback/freeze mechanism.
- **Notification-fatigued but still present** — annoyed by current notification cadence and opted out, but didn't report leaving the app itself ("nagging"; "turned them all off"). Risk is losing the re-engagement channel, not necessarily the user yet.
- **Resilient returners** — actually came back after a lapse (implied by "coming back after two weeks away") and engaged enough to give detailed feedback. May be won over by smaller UX fixes (acknowledgment/personalization) rather than a hard recovery mechanism like streak-freeze.

## Summary for Marcus

This feedback independently confirms the retention hypothesis already in `strategy.md`: the streak reset is the biggest driver of disengagement, showing up in 7 of 10 comments, and it's costing us users outright (multiple mentions of stopped use or deletion tied directly to losing a streak). Two users specifically asked for a streak-freeze feature we don't have. This is real user-voice support for the proposed Comeback screen direction (best-streak stat, comeback lesson, streak-freeze) — worth bringing into Thursday's discussion as corroborating evidence, not just an internal hypothesis.
