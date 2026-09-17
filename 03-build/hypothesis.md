# Hypothesis — Streakly Comeback Screen

*Source: synthesized from `change_log.md` and `docs/decision-brief.md`, 2026-09-16.*

## Learning Synthesis

### What We Know

- Day-7 retention dropped from 48% to 39% after the streak redesign, concentrated among users who break their streak in week 1 — missing two days in a row nearly doubles churn (`decision-brief.md`, Situation).
- The current post-break experience is a cold reset to zero with no acknowledgment, paired with a harsh-toned "you lost your streak" push notification, and no offered path forward (`decision-brief.md`, Problem to Be Solved).
- Three independent sources converge on the same root cause and the same fix direction: the team's own hypothesis (`project.md`), NPS data (7 of 10 verbatim comments cite the punishing streak reset as their reason for disengaging/uninstalling), and competitive research (none of 5 reviewed competitors offer a free, built-in recovery moment — Duolingo's is the only protection mechanic found, and it's paywalled) (`decision-brief.md`, Key Findings).
- No competitor personalizes the return experience based on how long a user was away — this white-space gap was independently raised by both NPS feedback and competitive research (`decision-brief.md`).
- Raj (Eng) confirmed the proposed Comeback screen is "technically doable" with existing systems and data — no new infrastructure needed (`project.md`, carried into `decision-brief.md`).
- Round 1 prototype testing found that an unkept promise in the comeback copy ("no reset needed" contradicted by a literal "Day 1" reset) reads as the app lying, not just as a design nitpick — and this risks reinforcing the exact punishing-reset perception already found in the NPS data, rather than fixing it (`change_log.md`, 2026-09-16 entries).

### What We Assume

- Eric's working read that the friction is *mainly functional* (hard to resume) with *some emotional component* (cold reset feels like failure) — this is a stated hypothesis, not yet validated with users (`project.md`).
- That fixing the comeback moment specifically (vs. notification tone alone, or the broader streak/notification system) is the right scope to move Day-7 retention — Option 2 (notification-only) and Option 3 (hold for Thursday) were both considered and set aside in favor of Option 1, but this is a recommendation, not a tested result (`decision-brief.md`, Options Considered).
- That a free streak-freeze/"pass" mechanic is viable and won't need to be paywalled — flagged explicitly as a monetization call for the team, not a research finding (`decision-brief.md`, Decisions Needed).

### What We Still Do Not Know

- **Targeting logic** — which users see the Comeback screen, and when (still open per both `project.md` and `decision-brief.md`'s Next Steps).
- **Freeze rules** — duration, frequency limits, and whether the "pass" is a one-time hook or a repeatable mechanic (open in `decision-brief.md`; also the specific question Tom's persona raised in Round 2 prototype testing, not yet logged to `change_log.md`).
- **Target metric values and a date to hit them by** — current metrics in `project.md` have no targets set (`decision-brief.md`, Next Steps).
- **Engineering size/timeline** — Raj confirmed feasibility but hasn't sized the lift (`decision-brief.md`, Next Steps).
- **The streak-intensity trade-off** — softening the reset may reduce what currently motivates high-stakes streak owners; this is an explicit judgment call for the team, not resolved by any research to date (`decision-brief.md`, Decisions Needed).
- **Notification tone/cadence scope** — unclear if it's in scope now or a separate follow-on workstream (`decision-brief.md`, Next Steps).
- Whether the root driver is the streak reset itself, notification tone/timing, or re-entry friction — the original open question from `project.md`/`strategy.md` that Thursday's meeting was meant to resolve; not confirmed as answered in either source file reviewed here.

---

## Hypothesis Statement

*Draft — proposed by Eric, not yet reviewed or agreed by the team (Marcus, Raj, Lena). Presented here as a hypothesis to test, not a committed target.*

> We believe that **the Comeback screen (personalized best-streak stat, last-lesson reminder, and a one-tap streak-connect pass that continues the streak count instead of resetting it)** will deliver **reduced churn among users who break their streak in week 1, recovering Day-7 retention toward the pre-redesign 48% baseline** for Streakly users in their first 7 days, as measured by Day-7 retention rate.

**Signal we'd need to confirm or reject this:** Day-7 retention trending back toward 48% specifically among the week-1-break segment, without a corresponding drop in engagement among high-stakes streak owners (the unresolved streak-intensity trade-off flagged above) — neither of which can be measured until targeting logic, freeze rules, and target metric values are decided.
