# Streakly Comeback Screen — Results & Recommendation

*For: Marcus. From: Eric. 2026-09-17. Full data behind this memo: `data/metric-findings.md`, `data/metric-diagnosis.md`.*

**Recommendation: fund a larger-sample validation test of the Comeback screen next sprint, targeted specifically at users who break their streak — not a full rollout yet, and not a pass.**

## Situation

We shipped a prototype of the Comeback screen — a welcome-back message, personalized stats, and a "pass" to reconnect a broken streak instead of a cold reset — and ran it as a controlled test against the current experience for one week-5 cohort, to see whether it moves Day-7 retention for users who break their streak in week 1.

## Evidence

- **Day-7 retention: 76% (comeback) vs. 46% (control), and the lift holds at Day-30** (36% vs. 22%) — not a short-term bump that fades.
- **Among the actual target segment — users who broke their streak — retention went from 28% to 50%.** Comeback-message open rates climbed 28%→56% across 4 sends while control stayed flat at 4% every time.
- **The single clearest driver: users who acted on the offer retained at 100% (10/10); those who saw it but didn't act churned at 100% (0/10).** Retention depends on action, not just exposure — a fixable UX lever, not a fixed trait of the users.

## Ask

Two things, both needed before eng can scope the real build, not just the test: (1) sign off on Raj sizing this into next sprint so we can run a larger-sample test before any rollout decision, and (2) decide the two calls that are yours, not the team's — free vs. paywalled streak-freeze, and whether we accept the streak-intensity trade-off — both already flagged in `docs/decision-brief.md`.

## Risk if We Wait

Every week we stay at 39% Day-7 retention compounds churn, and we're now sitting on the strongest signal this project has produced without a plan to validate it past a 50-person sample.

---

*Caveat stated plainly, not buried: this is a single cohort at n=50 per arm, and `data/metric-diagnosis.md` found part of the topline lift shows up even among users who never broke their streak at all — meaning the number attributable to the screen itself is smaller than the headline 76%-vs-46%. That's exactly why the ask is a bigger test, not a rollout.*
