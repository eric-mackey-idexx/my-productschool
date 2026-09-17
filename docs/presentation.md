# Streakly Comeback Screen — Quarterly Review Deck (Narrative Structure)

*2026-09-17. Audience: Marcus. Sources: `CLAUDE.md`, `docs/decision-brief.md`, `docs/recommendation-memo.md`, `data/metric-findings.md`, `research/nps-analysis.md`, `04-team/stakeholders/marcus.md`. `research/interview-synthesis.md` does not exist in this repo — `research/nps-analysis.md` is the file that actually contains user quotes and themes, used in its place.*

## Slide 1 — The Problem

- **The number:** Day-7 retention dropped from **48% to 39%** after the streak redesign shipped (`CLAUDE.md`, `docs/decision-brief.md`).
- **The insight:** The drop concentrates in users who break their streak in week 1 — missing two days in a row nearly doubles churn — and this isn't just an internal read of the data: 7 of 10 NPS comments independently name the punishing streak reset as their reason for disengaging or uninstalling (`docs/decision-brief.md`, `research/nps-analysis.md`).

## Slide 2 — Why Now

- **What changed:** since the original recommendation, we shipped a working prototype and ran it as a controlled test against a live cohort, rather than staying at the hypothesis stage (`docs/recommendation-memo.md`, Situation).
- **What we learned:** the comeback variant hit 76% Day-7 retention vs. 46% for control, and the lift held at Day-30 too (36% vs. 22%) (`data/metric-findings.md`, `docs/recommendation-memo.md`).
- **Framing:** we've moved from "we believe this will work" to "we have a real, measured signal."

## Slide 3 — The Proposal

- **What it is:** fund a larger-sample validation test of the Comeback screen next sprint, targeted specifically at the users who break their streak (`docs/recommendation-memo.md`, Recommendation).
- **What it isn't:** not a full rollout yet — and not shelving the idea either (`docs/recommendation-memo.md`).
- **For context, the underlying feature:** a welcome-back message, personalized stats, and a streak-connect pass, replacing the current cold reset (`docs/decision-brief.md`, Options Considered).

## Slide 4 — Evidence

- **Prototype:** tested as a controlled experience, not just described (`docs/recommendation-memo.md`).
- **User quotes:** "the moment I lost my streak the whole thing lost its meaning"; users explicitly asked for a streak-recovery mechanic we didn't have (`research/nps-analysis.md`).
- **Data, the four numbers that matter:** the weeks 1–4 retention decline; the retention gap between users who break their streak and those who don't; the week-5 variant lift (Day-7 and Day-30); the comeback message's open rate climbing 28%→56% while control stayed flat at 4% (`data/metric-findings.md`).

## Slide 5 — The Plan

- **Milestone 1:** Raj sizes the engineering lift for a larger test — not yet estimated (`docs/decision-brief.md`, Next Steps).
- **Milestone 2:** run the larger-sample test next sprint (`docs/recommendation-memo.md`, Ask).
- **Risk of scaling now:** committing to a lift that could be far smaller than today's 30-point headline once tested at scale (`docs/recommendation-memo.md`, Risk).
- **Risk of waiting:** continued churn at 39% Day-7 retention while we validate (`docs/recommendation-memo.md`; `docs/decision-brief.md`, Why Now).
- **Caveat carried forward, not smoothed over:** n=50 per arm, and part of the topline lift isn't yet isolated as attributable to the screen itself (`docs/recommendation-memo.md`).

## Slide 6 — The Ask

1. Approve sizing this into next sprint — a go-ahead to size and test, not a rollout decision (`docs/recommendation-memo.md`, Ask).
2. Decide the two calls that are Marcus's specifically, not the team's to research: free vs. paywalled streak-freeze, and whether to accept the streak-intensity trade-off (`docs/decision-brief.md`, Decisions Needed).
3. **Not answered today:** a rollout timeline — it depends on Raj's sizing, which depends on ask #1 (`04-team/stakeholders/marcus.md`; `docs/decision-brief.md`).
