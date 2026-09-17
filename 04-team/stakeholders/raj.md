# Raj — Engineering Lead

*Compiled 2026-09-16. Sources checked: `project.md`, `strategy.md`, `change_log.md`, `research/nps-analysis.md`, `docs/decision-brief.md`, `03-build/pm-brief.md`, `03-build/hypothesis.md`, `03-build/prototype/README.md`, `03-build/triad-session.md`. Two requested paths don't exist in this repo and were not read: `02-research/decision-brief.md` (the real file is at `docs/decision-brief.md`) and `02-research/interview-synthesis.md` (no file by that name exists anywhere in the repo). Flag if these live somewhere I haven't checked.*

## From the workspace (sourced, with citation)

- Engineering Lead on the Streakly squad, alongside Marcus, Lena, and Eric (`project.md`).
- Provided the key data insight driving this whole project: users who miss two days in a row churn at nearly double the rate — the sharpest-drop segment (`project.md`, `strategy.md`).
- Confirmed the proposed Comeback screen is **"technically doable" with existing systems and data — no new infrastructure needed** (`project.md`, restated in `strategy.md` and `docs/decision-brief.md`'s Key Findings).
- Per `project.md`: still needs to define **targeting logic** (who sees the Comeback screen, when) and **specific freeze rules** — flagged as his open items, not yet resolved.
- `docs/decision-brief.md`'s Next Steps — Discovery lists as open: **"Size engineering lift and timeline for the Comeback screen (Raj confirmed it's 'technically doable,' not yet estimated)"** — feasibility confirmed, but no size/timeline given yet.
- `strategy.md` flags an open question that needs Raj (and Lena) to resolve: whether "continuing where you left off" means resuming at the user's prior lesson/track position, versus Lena's fresh 60-second comeback lesson concept — these pull different data.
- `03-build/pm-brief.md` flags a question for Raj (and Marcus) before this becomes a real spec: what number should a "connected" streak actually resume at — the user's best-streak stat, or their actual pre-break streak length? The prototype currently assumes these are the same number; nothing in the workspace confirms that.
- `03-build/triad-session.md` — the working-session agenda built specifically to get from Raj: (1) whether "continue where left off" is feasible with what's actually tracked today, (2) a rough (even directional) size/timeline, (3) any data/infra gaps for targeting logic.

## From this conversation (said, not yet saved to a workspace file)

- In drafting the triad-session invite, Eric planned to ask Raj to come with a rough gut-check on eng sizing and the freeze rule beforehand, rather than deriving both live in the 30-minute session — this framing exists only in the chat draft, not in `triad-session.md` itself.

## From the default profile (unconfirmed — correct anything inaccurate)

- **Role:** Owns technical architecture, sprint scope, and feasibility decisions for the Streakly squad.
- **Pushes back on:** Underspecified requirements, scope that grows mid-sprint, anything touching the streak/notification pipeline without a clear rollback plan.
- **Needs before saying yes:** Clear acceptance criteria, edge cases called out upfront, an answer to "what does done look like."
- **Has asked before that was hard to answer:** "How will we know if this is working after it ships?" and "What happens if the user has never set a streak, or breaks it twice in a week?"
- **Communication preference:** Async first, short messages, bullet points over paragraphs, dislikes being surprised in standups.
- **Open items (per default profile):** Still waiting on data model clarification for the streak-freeze field.

## Where the default lines up with what's already documented

The default profile's open item — "waiting on data model clarification for the streak-freeze field" — matches exactly what's already flagged from real sources: `pm-brief.md`'s "best streak vs. actual pre-break streak length" question and `project.md`'s "specific freeze rules" gap. That's the same open item showing up in three places, which makes it the single most load-bearing thing to resolve with Raj — not a coincidence to treat lightly.

The default's edge-case question ("what if the user has never set a streak, or breaks it twice in a week") isn't addressed anywhere in the sourced files — the prototype and brief only cover the single-break case. Worth raising explicitly, since it's an unhandled case in the current design, not just a hypothetical Raj might ask about.
