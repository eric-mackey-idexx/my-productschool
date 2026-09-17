# PM Brief — Streakly Comeback Screen

*Source: Eric (Product Lead), given directly for the Module 3 build, 2026-09-16.*

**User:** A person who has a multi-day streak but broke it.

**Job to be done:** Make it easy and welcoming for the user to start a streak again.

**Flow:** Personalized screen that welcomes the user back and encourages them to get started again.

**Success condition:** User isn't discouraged from starting again.

**Constraints:** Keep within the design pattern of Streakly.

---

## Notes / open items carried from project.md and strategy.md

- No Streakly brand/style guide exists in this repo. The prototype uses a generic warm, encouraging mobile-app aesthetic (rounded cards, puppy-greeting motif, soft coral/orange palette) as a stand-in — **flag for design review against actual Streakly UI before user testing.**
- Personalization includes the best-streak stat and a "where your streak stopped" (last lesson) reminder (sourced from project.md's Comeback screen concept — Lena, plus strategy.md's open question about last-lesson vs. best-streak data). No user name/avatar is used since no real user data source is wired up in this prototype.
- Screen now also surfaces a "pass to connect your streak" perk (Eric, added 2026-09-16) — this is functionally the one-tap streak-freeze from project.md's Comeback screen concept, reintroduced here as copy only. **Still open:** freeze/pass frequency and cooldown rule (how often it can be used) is not yet defined — tracked for the `03-build/triad-session.md` working session, not blocking the build below.
- Round 1 persona testing (2026-09-16) surfaced a contradiction: the perk-card promised "no reset needed" while the confirmation screen showed a literal Day 1 reset. Fixed two ways: (1) softened the perk-card sub-label to stop over-promising, and (2) per Eric, changed the confirmation screen to actually continue the day count instead of resetting to 1.
- **Resolved 2026-09-16, via a Raj role-play spec review (`04-team/spec-readiness.md`):** what number the "connected" streak resumes at was the prototype's biggest open question — now answered. Two separate values are tracked: `bestStreak` (all-time, unchanged, still shown as the "you can beat it" stat) and `preBreakStreak` (the streak length at the moment it broke — this is what the continuation counter actually resumes from, not `bestStreak`). `preBreakStreak` is written by modifying the existing nightly reset job, behind a feature flag so it can be disabled without a deploy. The screen only renders when `preBreakStreak > 0` — a user with no prior streak never sees it, by design, not by omission. This is Eric's role-play-tested answer, not yet confirmed by the real Raj — see the async confirmation message in `04-team/spec-readiness.md`.
- Scope: comeback lesson selection logic (Lena's 60-second lesson) is still not included in this prototype — remains an open item in strategy.md.
- Round 2 persona testing (2026-09-16) found Tom's remaining objection was about durability, not accuracy: "is this pass a one-time trick, or a real ongoing rule." Eric reviewed 3 wording options for the perk-card and **prefers Option C: "Pause protection, built in" / "Every streak includes up to 3 pause days — not just a one-time thing."** Held, not yet applied to the prototype — the "3 pause days" figure is illustrative only; the actual freeze duration/frequency rule is a decision item for the `03-build/triad-session.md` working session with Raj and Lena. Apply this copy only after that rule is confirmed.
- This is a static, no-login, click-through prototype for early user reactions — not wired to real streak data or backend logic.
