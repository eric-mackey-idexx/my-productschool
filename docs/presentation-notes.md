# Streakly Comeback Screen — Speaker Notes

*Companion to `docs/presentation.md`. Full sentences, written to be said out loud.*

## Slide 1 — The Problem

This slide shows the number driving everything else in this deck: Day-7 retention dropped from 48% to 39% after the streak redesign shipped. That's not a broad, diffuse decline — it concentrates specifically in users who break their streak in week 1, and missing two days in a row nearly doubles their churn. We're not guessing at why, either: seven of the ten NPS comments we reviewed independently named the punishing streak reset as the reason they disengaged or uninstalled. Before we move on, I want you to leave this slide with one thing — this is a specific, identifiable segment causing a specific, measurable drop, not a vague engagement problem.

## Slide 2 — Why Now

Here's what's changed since we last talked about this: we didn't just plan the Comeback screen, we built a working version of it and ran a controlled test against a live cohort. In that week-five test, the comeback variant hit 76% Day-7 retention against 46% for control, and that gap held at Day-30 too — 36% versus 22%. That's the shift I want you to take away: we've moved from a hypothesis you approved in principle to a real, measured signal. The question in front of you today isn't whether to believe in this anymore, it's what to do with evidence that's real but still based on a small sample.

## Slide 3 — The Proposal

This slide draws a hard line around what we're actually proposing, because I don't want you to leave here thinking the ask is bigger than it is. The proposal is to fund a larger-sample validation test of the Comeback screen next sprint, targeted specifically at the users who break their streak — the same segment from slide one. What it isn't: it's not a full rollout, and it's also not asking you to shelve the idea and wait indefinitely. The one thing I want you to take away from this slide is that distinction — we're asking for a bigger test, not a bet-the-quarter rollout decision.

## Slide 4 — Evidence

This is where I want to ground everything I've said in something you can actually see and hear, not just numbers I'm asserting. On the qualitative side, real users told us this directly — one wrote that "the moment I lost my streak the whole thing lost its meaning," and others explicitly asked for exactly the kind of streak-recovery mechanic we've now built. On the quantitative side, the four numbers that matter are the weeks 1-through-4 retention decline, the nearly doubled churn for users who break their streak, the week-5 variant lift, and the comeback message's open rate climbing from 28% to 56% while control stayed flat at 4%. What I want you to take away here is that this isn't one number I'm leaning on — it's the same story showing up in what people said and in what they actually did.

## Slide 5 — The Plan

This slide is about sequencing, not certainty, because I don't have a finished timeline to hand you yet. The first milestone is Raj sizing the engineering lift for a larger test, and that estimate doesn't exist yet — I'm not going to pretend it does. The two risks here are real in both directions: scaling now risks committing to a lift number that could be much smaller than today's 30-point headline once we test at scale, while waiting means we keep bleeding retention at 39% in the meantime. I want you to leave this slide understanding that the plan is deliberately staged — size, then test, then decide — not because we're being slow, but because a 50-person pilot isn't a rollout decision.

## Slide 6 — The Ask

This is the actual ask, and I want to be plain about it. First, approve sizing this into next sprint so we can run the bigger test — that's a go-ahead to size and test, not a rollout approval. Second, I need two decisions that are yours specifically, not something the team can research its way to: whether the streak-freeze is free or paywalled, and whether we accept the trade-off that softening the reset might reduce what currently motivates our highest-stakes streak owners. One thing I can't give you today is a rollout timeline — that depends on Raj's estimate, which depends on you saying yes to the first ask. What I want you to leave with is a yes on sizing the test and a decision on those two open calls, not a signature on a launch date that doesn't exist yet.
