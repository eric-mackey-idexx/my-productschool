# Triad Working Session — Streakly Comeback Screen

*Eric + Raj (Eng) + Lena (Design), 30 min. Prep: `03-build/prototype/index.html`, `03-build/pm-brief.md`, `docs/decision-brief.md`, `change_log.md` (Round 1 & 2 testing entries).*

## 1. Agenda

| Time | Segment |
|------|---------|
| 0:00–0:03 | Why we're here — Day-7 retention drop, where the Comeback screen concept came from, what's been tested so far |
| 0:03–0:12 | Live walkthrough of the prototype — 3 screens, persona switcher (Priya/Tom/Amara), what Round 1 and Round 2 testing found and fixed |
| 0:12–0:24 | Discussion — open questions for Raj and Lena (below) |
| 0:24–0:29 | Lock decisions and owners (below) |
| 0:29–0:30 | Confirm who fills out the alignment doc and by when |

### What to show

- The comeback flow end to end (broken streak → welcome-back screen → confirmation), using the persona switcher to show it's not one generic message.
- Round 1 finding: the original "no reset needed" promise directly contradicted a "Day 1" confirmation — fixed by making the day count actually continue.
- Round 2 finding: making stats persona-relevant (417 days / 12 days / 3 days instead of one generic "14 days") resolved Amara's and Priya's objections, but only partially addressed Tom's — his concern shifted to whether the freeze/"pass" mechanic is a real, repeatable rule or a one-time trick.
- The specific things still marked "not sourced/undefined" in `pm-brief.md`: no real Streakly brand/style guide behind the visuals, and no defined freeze rules (duration, frequency, one-time vs. repeatable).

### Questions to ask

**For Raj (Eng):**
- Is "continue where you left off" (resuming the day count instead of resetting) feasible with what we actually track today — do we have the user's pre-break streak length, or only their best-streak stat? (The prototype currently reuses best-streak as a stand-in; that may not be the same number in real data.)
- Rough t-shirt size and timeline for the Comeback screen as scoped — even directional, to get into planning.
- Any data/infra gaps for targeting logic — knowing which users should see this screen, and when.

**For Lena (Design):**
- Does the visual direction (icons, cards, tone) hold up against the real Streakly design system? Nothing here was pulled from an actual style guide — what has to change before this goes near real users?
- Does the reassurance copy ("it's okay, everyone gets busy") and the "pass" framing read as warm, or as gamified/guilt-adjacent in Streakly's actual voice?
- What's the minimum visual fidelity needed before this can go in front of real users vs. staying an internal test?

**For both:**
- First-pass definition of the freeze/"pass" rule — duration, how often a user can use it, one-time or repeatable. This is the single thing Round 2 testing flagged as the deepest remaining trust issue (Tom's persona) and it's currently undefined anywhere.
- What's missing from this prototype that would block moving to real user testing next?

### Decisions we need to walk out with

1. **Freeze/pass rule — first pass.** Doesn't need to be final, but needs a directional answer (duration + frequency) so copy and testing can stop working around an undefined mechanic.
2. **Feasibility read on "continue where left off."** Confirm whether real data supports resuming an actual pre-break streak count, or whether the honest version of this screen has to use a different (and possibly less satisfying) mechanic.
3. **Eng sizing (directional).** Rough size/timeline to carry into `decision-brief.md`'s "Next Steps — Discovery."
4. **Design next step.** Named owner and rough timing for checking this against Streakly's real brand system before broader testing.

*Not a decision for this session: free vs. paywalled freeze, and the streak-intensity trade-off (softening the reset vs. what motivates high-stakes streak owners) — both are flagged in `docs/decision-brief.md` as calls for Marcus, not this triad.*

---

## 2. Post-Session Alignment Doc (template — fill out after the session)

# Streakly Comeback Screen — Triad Alignment

*Date: [___] · Attendees: Eric, Raj, Lena*

## Decisions Made

| Decision | Answer | Owner | Notes |
|----------|--------|-------|-------|
| Freeze/pass rule (duration, frequency) | [___] | [___] | [___] |
| "Continue where left off" feasibility | [___] | [___] | [___] |
| Eng sizing / timeline (directional) | [___] | [___] | [___] |
| Design next step (brand alignment) | [___] | [___] | [___] |

## Open Items Deferred (not decided today)

- [___]

## Changes to Make Before Next Round

- Prototype (`03-build/prototype/index.html`): [___]
- Brief (`03-build/pm-brief.md`): [___]

## Next Round of Testing

- Personas / real users: [___]
- Target date: [___]

## Escalate to Marcus

- [___]
