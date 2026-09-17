# Learning Loop — Weekly Self-Review

*2026-09-17. Reads `agents/outcome-log.md`, scores each past diagnosis against what actually happened (hit / miss / partial), and proposes one heuristic update to `CLAUDE.md`. Part of the Comeback Coach agent stack — see `agents/registry.md`.*

## Why this is a prompt, not a script

Scoring "did hypothesis text X match outcome text Y" is a semantic judgment, not a string comparison — the same reason `anomaly_diagnosis.py`'s hypothesis generation is an explicit rule table rather than a model call, just in reverse: generation was kept deterministic because it's checkable; scoring can't be, because "what actually happened" is free text written by a person, not a fixed vocabulary. So this is split in two:

- **`agents/learning_loop.py`** (real, runnable) — the *mechanical* half. Parses `outcome-log.md` and splits logged diagnoses into scoreable (top hypothesis has a real, filled-in outcome) vs. pending (still the placeholder) vs. no-hypothesis (the loop stopped at Step 1 or 2 before generating one). It does not judge anything.
- **This prompt** — the *judgment* half, run by whoever/whatever triggers the weekly review.

## Trigger Prompt (paste this, nothing else needed)

> Run the weekly learning-loop review on agents/outcome-log.md.

## What Claude Does, Step by Step

1. Run `python3 agents/learning_loop.py` to get the mechanical split — how many entries are scoreable, pending, or never reached a hypothesis.
2. **If nothing is scoreable, stop here and say so.** Do not propose a heuristic change from zero evidence — that's exactly the failure mode this whole project has tried to avoid elsewhere (inventing a signal because a slot exists for one).
3. For each scoreable entry, compare the top-ranked hypothesis against the real "what actually happened" text and assign **hit** (the hypothesis correctly identified the cause), **miss** (it didn't), or **partial** (right category, wrong specifics — e.g. correctly identified a channel-quality issue but named the wrong channel). Give one sentence of reasoning per score, not just the label.
4. Aggregate hit/miss/partial by which of the 3 fixed hypothesis templates in `anomaly_diagnosis.py`'s `generate_hypotheses()` it was (notification issue / cohort quality shift / product regression) — the point is to find out which *template* is reliable, not just which single instance was right.
5. **Propose exactly one heuristic update**, grounded in that aggregate pattern — e.g. "the cohort-quality-shift hypothesis has missed 2 of 2 times; lower its base confidence from 6 to 4" or "add a 4th template for [newly observed pattern], since neither of the 3 current ones explained the last miss." If the sample is too small to support a confident proposal (e.g. only 1 scoreable entry), say that explicitly and propose nothing rather than force a change.

## Output Format

Appended to `agents/outcome-log.md` as a dated section:

```markdown
## Weekly Learning Loop Review — [date]

**Scoreable this week:** [N] of [total logged]

| Date | Hypothesis | Confidence | Outcome | Score | Reasoning |
|---|---|---|---|---|---|
| ... | ... | ... | ... | hit/miss/partial | ... |

**Pattern:** [what the aggregate hit/miss/partial rate by template shows, or "not enough data yet"]

**Proposed heuristic update:** [the one change, with why — or "none this week; insufficient scored data"]
```

If a change is proposed and accepted, it gets applied directly to `CLAUDE.md` (or `anomaly_diagnosis.py`'s confidence rules, whichever the pattern actually points to) — this prompt proposes, it doesn't auto-apply.

## Run It Manually to Verify

```bash
cd agents
python3 learning_loop.py
```

Real output from this repo's actual `outcome-log.md`, captured 2026-09-17:

```
Total logged diagnosis checks: 2
  Scoreable (outcome filled in):     0
  Pending (still placeholder):       1
  No hypothesis generated (Step 1/2 stop): 1

Nothing scoreable yet — every logged diagnosis still has a placeholder outcome, or stopped before
generating a hypothesis. No heuristic update can be responsibly proposed from zero confirmed outcomes.
```

**This is the honest result, not a placeholder demo.** Both real entries in `outcome-log.md` right now are: one that stopped at Step 1 (no hypothesis at all — the streak-break-rate check from `metric_pulse.py`'s real test run), and one that reached Step 3 but is still an unfilled placeholder (the Day-7 retention low-confidence case from the same run). The learning loop can't score either, so it shouldn't — and doesn't. The first real proposal will only happen once someone actually fills in a "what actually happened" row.
