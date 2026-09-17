# Lena — Design Lead

*Compiled 2026-09-16. Sources checked: `project.md`, `strategy.md`, `change_log.md`, `research/nps-analysis.md`, `docs/decision-brief.md`, `03-build/pm-brief.md`, `03-build/hypothesis.md`, `03-build/prototype/README.md`, `03-build/triad-session.md`. Two requested paths don't exist in this repo and were not read: `02-research/decision-brief.md` (the real file is at `docs/decision-brief.md`) and `02-research/interview-synthesis.md` (no file by that name exists anywhere in the repo). Flag if these live somewhere I haven't checked.*

## From the workspace (sourced, with citation)

- Design Lead on the Streakly squad, alongside Marcus, Raj, and Eric (`project.md`).
- Originated the core design concept this whole build is based on — the **Comeback screen**: best-streak stat, one 60-second comeback lesson, and a one-tap streak-freeze, shown instead of a cold reset to a default home screen (`project.md`, restated in `strategy.md` and `docs/decision-brief.md`'s Options Considered).
- The prototype's personalization elements (best-streak stat, "where your streak stopped" reminder) are sourced directly from her original concept (`03-build/pm-brief.md`).
- Two pieces of her original concept are explicitly **not** in the current prototype yet — the 60-second comeback lesson and the one-tap streak-freeze (implemented only as placeholder copy, not the real mechanic) — both remain open items in `strategy.md` and `03-build/pm-brief.md`.
- `strategy.md` flags an open question that needs her (and Raj) to resolve: whether "continuing where you left off" should mean resuming at the user's prior lesson/track position, or should instead route to her fresh 60-second comeback lesson — these are two different mechanics pulling different data.
- `03-build/triad-session.md` — the working-session agenda built specifically to get from her: (1) whether the current visual direction (icons, cards, tone) holds up against Streakly's real design system, since nothing in the prototype was pulled from an actual style guide, (2) whether the reassurance copy and "pass" framing read as warm or as gamified/guilt-adjacent, (3) minimum visual fidelity needed before this goes near real users. The session is meant to land a named owner and rough timing for a brand-alignment pass.

## From this conversation (said, not yet saved to a workspace file)

- None found beyond what's already reflected in `03-build/triad-session.md` and `03-build/pm-brief.md`.

## From the default profile (unconfirmed — correct anything inaccurate)

- **Role:** Owns the end-to-end user experience, interaction design, and design system consistency for Streakly.
- **Pushes back on:** Feature requests that skip the problem definition, copy that reads like it was written by a product manager, anything that adds cognitive load without a clear user benefit.
- **Needs before saying yes:** Evidence from real users (not assumptions), a clear definition of the primary user and their context, understanding of what the empty state looks like.
- **Has asked before that was hard to answer:** "What does the user do after they see the Comeback screen?" and "How do we make a broken streak feel forgiving instead of like a guilt trip?"
- **Communication preference:** Prefers to see things rather than read about them; responds well to "here is what users told us" framing.
- **Open items (per default profile):** Wants to revisit the streak-freeze UI after seeing Amara's feedback.

## Where the default lines up with what's already documented

The default's open item — wanting to revisit the streak-freeze UI after Amara's feedback — matches real, already-logged testing: Round 1 and Round 2 persona testing in `change_log.md` (2026-09-16 entries) is exactly where Amara's reaction was captured, including her Round 1 complaint that the stats felt generic/impersonal and her Round 2 reaction once they were made persona-relevant. This gives a concrete artifact to bring into the triad session rather than a vague callback — the actual before/after screenshots and copy exist in `03-build/prototype/index.html` and the change log.

Her default's guilt-trip question ("how do we make a broken streak feel forgiving instead of like a guilt trip") is the closest match in the sourced material to Tom's Round 1 and Round 2 objections (the "no reset needed" contradiction, and later "is this a one-time trick") — worth connecting explicitly when you talk to her, since it's the same underlying tension she's already named, now with persona evidence behind it.
