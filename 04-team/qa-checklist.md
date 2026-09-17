# Streakly Comeback Screen — QA Checklist

*2026-09-16. Sources reviewed: `04-team/spec-readiness.md`, `03-build/prototype/README.md`, `03-build/prototype/index.html`. The prototype is a static, no-backend HTML file — many real-product questions below genuinely cannot be answered from it, and that's flagged explicitly rather than guessed at.*

## 1. Edge Case List

### Empty states
- User has never held a streak (`preBreakStreak` is 0/null) — per `spec-readiness.md`, the screen shouldn't render at all. No copy exists anywhere for "what if it renders anyway."
- No best-streak stat exists yet (`bestStreak` is 0/undefined, e.g. a genuinely new user) — the trophy card ("your best streak so far — you can beat it") has no defined fallback copy for this case.
- No lessons available in the user's track (`lastLesson` is null — track finished, or track has no more content) — the "📍" reminder card has no empty-state copy; the prototype only ever shows 3 hardcoded, always-populated values.
- The referenced last lesson no longer exists (renamed/removed content since the user's last visit) — a dangling-reference case not addressed anywhere.

### Edge data conditions
- Streak of exactly 1 (broken on day 2) — gating rule says `preBreakStreak > 0` still shows the screen; worth confirming a 1-day comeback message doesn't feel disproportionate.
- User breaks their streak twice in the same week — does `preBreakStreak` simply get overwritten, and does the "pass" get reissued each time? This is Tom's exact unresolved objection from persona testing, and the frequency/cooldown rule is still open per `spec-readiness.md`.
- Streak-freeze/pass already used once — nothing distinguishes a first-time view of this screen from an nth-time view; the perk-card copy ("we'll give you a pass") is static regardless of prior use.
- `bestStreak` and `preBreakStreak` are equal (the streak that just broke *was* their best) — "you can beat it" doesn't quite make sense if there's nothing to beat yet.
- `preBreakStreak > bestStreak` (a data-integrity case that shouldn't be possible if `bestStreak` is a proper running max, but worth a defensive check).

### Timing scenarios
- Missed 1 day vs. missed many (7, 30+) — the same copy and mechanic apply regardless of gap length; no lapse-length threshold is defined anywhere.
- Time zone boundaries — `spec-readiness.md` resolves that `preBreakStreak` is written by the nightly reset job; a user near local midnight could have their streak evaluated against a different "day" than they perceive. Not addressed anywhere.
- Comeback screen shown "too late" (user returns 3 weeks after breaking, not the next day) — no staleness/expiry rule for the pass or the screen itself.
- User re-breaks their streak before ever opening/dismissing the Comeback screen from the first break — unclear if the screen re-triggers or shows stale data.
- Daylight saving transitions affecting the nightly cron run (an hour skipped or repeated) — a technical edge case tied directly to modifying the reset job.

### Permission states
- Notifications off — does the in-app Comeback screen still appear next time the user opens the app regardless of push permission? Implied but never stated as a requirement.
- Background app refresh off — could delay when the client learns about `preBreakStreak`, risking stale data shown on first open after being backgrounded.
- User revokes notification permission mid-streak — unclear if this affects Comeback screen eligibility/timing at all, or is purely unrelated.
- Device offline when "Continue where I left off" (the pass action) is tapped — does it require a live network call, and what happens if that call fails silently? (No network calls exist anywhere in this prototype, so this is entirely untested.)

## 2. PM QA Pass Against the Prototype

| # | What's being verified | Screen | Result | Blocking or known issue |
|---|---|---|---|---|
| 1 | Persona switch correctly updates best-streak stat, last-lesson text, and continuation day for all 3 personas | 1→2→3 | **Pass** — verified in browser: Priya (417/Lesson 301), Tom (12/Lesson 12), Amara (3/Lesson 3) all render correctly. | — |
| 2 | Comeback screen only shows when `preBreakStreak > 0` (the gating rule agreed in `spec-readiness.md`) | 1→2 | **Cannot be determined** — this is a static file with no real streak state; there's no gating logic to test, only 3 always-eligible hardcoded personas. | **Blocking** for real sign-off — this acceptance criterion has never actually been exercised, only agreed to on paper. |
| 3 | Continuation counter uses `preBreakStreak`, not `bestStreak`, per the resolved spec decision | 3 | **Fixed (2026-09-16)** — `PERSONAS` now has a separate `preBreakStreak` field per persona, and `renderPersona()` computes `continueDay = p.preBreakStreak + 1`. Verified in-browser: Priya's counter still shows Day 418. Note this only fixes the *prototype* — whether Raj's real implementation was ever wired to the wrong field is still the open question in the PR comment below. | No longer blocking in the prototype; the underlying question for the real codebase remains open. |
| 4 | "Maybe later" produces different behavior from "Continue where I left off" | 2 | **Fixed (2026-09-16)** — "Maybe later" now routes to a new Screen 4 ("No worries. Come back when you are ready...") instead of Screen 3, and does not start a new streak day. Verified in-browser, including the loop back via "Got it." | No longer blocking. |
| 5 | Empty-state copy exists for no-best-streak or no-lesson-available cases | 2 | **Fail** — no such copy exists; all 3 personas always have populated values by construction. | Known issue — acceptable for a click-through prototype, but must be resolved before real build, not just before this ships. |
| 6 | Screen 1's persona picker is clearly a prototype-only affordance, not a real product element | 1 | **Cannot be determined** — no in-file disclaimer on screen 1 itself (unlike screen 3's explicit note); relies on `README.md` context outside the file. | Known issue — low risk, but worth an explicit comment before this gets mistaken for a real feature idea (e.g., "let users pick a demo persona"). |
| 7 | Screen 3's "Day 15" continuation and disclaimer note are internally consistent with each other | 3 | **Pass** — the note text ("day count continues from the best-streak stat...") accurately describes what the code does, even though what the code does contradicts the *spec* (see #3). The prototype is internally honest about itself. | — |
| 8 | Accessibility — tap target size, color contrast | 2, 3 | **Cannot be determined** from a static code read — buttons have adequate padding (16px, ~48px+ height), but contrast ratios for coral-on-cream text weren't computed. | Needs a real accessibility pass; not gradable from this file alone. |
| 9 | Behavior when the "pass"/continue action is triggered while offline | 2 | **Cannot be determined** — the prototype makes zero network calls; it's pure client-side HTML/JS. Nothing here indicates what a real implementation does offline. | **This is the open question raised in the PR comment below.** |
| 10 | Visual design matches actual Streakly brand/style system | 1, 2, 3 | **Fail** — already known and documented; `pm-brief.md` and this `README.md` both state the visual style is a generic stand-in, not sourced from a real brand guide. | Known issue — already tracked for the Lena design review (`04-team/design-review.md`), not a new finding. |

## 3. Draft PR Comment for Raj

> Not blocking merge on this necessarily, but wanted to flag before we sign off: `renderPersona()` computes the Day N continuation counter as `bestStreak + 1`. Didn't we land on `preBreakStreak` as the field that should drive this in `spec-readiness.md`? Want to make sure I'm not misreading which field this build is actually wired to — if it's intentionally still using `bestStreak` for now, can you help me understand why, so I can update the spec doc instead of leaving it out of sync?
