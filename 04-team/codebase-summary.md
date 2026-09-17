# Codebase Tour — Streakly (stand-in: Habitica)

*Streakly itself has no real, clonable codebase — the rest of this repo (`project.md`, `strategy.md`, the prototype in `03-build/`) is course/discovery work, not a running app. Per Eric, this tour uses [github.com/HabitRPG/habitica](https://github.com/HabitRPG/habitica) as a real, public stand-in — a similar habit-tracking app with an actual streak mechanic in its code. Everything below describes Habitica's real codebase, used as a reference point for what a Streakly codebase would look like, not Streakly's actual code.*

A few terms, since this is written for a first read of any codebase:
- **Repo (repository):** the whole folder of code and files for one product.
- **Frontend / client:** the part that runs in the user's browser or app — what they see and click.
- **Backend / server:** the part that runs on the company's computers — handles logins, saves data, runs business logic.
- **API:** the specific set of "requests" the frontend sends to the backend, like "save this task" or "log this user in."
- **Database / model / schema:** where user data actually lives, and the blueprint that defines what fields each piece of data has (e.g., every user has an email, a password, a list of tasks).

## 1. What it does, in one sentence

Habitica is a habit-tracking app that turns your real-life to-do list into a role-playing game — you gain experience and gold for completing tasks and lose health for missing them, with a visible "streak" counter that tracks daily tasks completed in a row.

## 2. How the codebase is organized

Three top-level pieces do almost all the work:

- **`website/client`** — the frontend. Built with Vue (a framework for building what users see). `client/src/pages` holds full screens, `client/src/components` holds reusable pieces (task cards, stat displays, spell menus), `client/src/store` holds the app's in-memory copy of your data while you're using it.
- **`website/server`** — the backend. `server/controllers` defines every API endpoint (every "request" the frontend can make). `server/models` defines the database blueprints (see Q4). `server/libs` holds business logic that's too complex to put directly in a controller — this is where the nightly job that resets streaks lives (`server/libs/cron.js`).
- **`website/common`** — logic shared between frontend and backend, so both sides agree on the rules without duplicating code. This is where the actual "what happens when you check off a task" logic lives (`common/script/ops/scoreTask.js`).

Everything else supports those three: `migrations/` (one-time scripts for changing old data to a new format), `database_reports/` (one-off scripts to answer questions about the data), `test/` (automated checks that the code still works), `kubernetes/` and `Dockerfile*` (how the app gets deployed to run in production).

## 3. Where the main user-facing features are implemented

Take "complete a daily task and watch your streak go up" as the example, since it's the closest thing to Streakly's own streak feature:

1. **Frontend:** `client/src/components/tasks/task.vue` renders the task card the user taps to check something off.
2. **API call:** that tap sends a request to `POST /api/v3/tasks/:taskId/score/:direction` — defined in `server/controllers/api-v3/tasks.js`.
3. **Shared logic:** the controller calls into `common/script/ops/scoreTask.js`, which is the actual rulebook — it increments `task.streak` by 1 on completion, decrements it if you uncheck a task, and grants a small in-game bonus that scales with streak length.
4. **The nightly reset:** `server/libs/cron.js` runs once a day for each user and is what actually resets a missed daily's streak to 0 — this is the backend equivalent of Streakly's "streak reset."
5. **A real streak-freeze precedent:** Habitica has a Wizard-class spell called "Chilling Frost" (`common/script/content/spells.js`), which sets a flag (`user.stats.buffs.streaks = true`) that tells the nightly reset job to skip resetting streaks for that user — but only for one day, and it costs in-game currency (mana) to cast, gated behind character level. **This is directly relevant to the open freeze-rule question in `pm-brief.md` and `docs/decision-brief.md`** — it's a real example of a team deciding to make streak protection a limited, earned resource rather than an unlimited free pass, worth raising at the triad session.

## 4. What the database models tell us about the data model

Habitica uses MongoDB — a "document" database, meaning each user or task is stored as one flexible bundle of fields, not spread across many rigid tables like a spreadsheet. The blueprints for those bundles live in `server/models/`:

- **`User`** is one large document per person — everything about them lives in one place: login info (`auth`), game stats and buffs (`stats`, including the streak-freeze flag above), achievements, party/guild membership, preferences, and a list of references to their own tasks (`tasksOrder`). This tells us the app is built around "everything about one user in one record" rather than joining many separate tables together.
- **`Task`** is a single collection that holds four different task types — habit, daily, todo, reward — using a pattern called a "discriminator" (one shared shape, with type-specific extra fields bolted on). **The streak count itself lives on the Daily task type specifically** (`streak`, defaulting to 0), not on the User — meaning in this app, streaks are tracked per-task, not as one single number per person. That's a meaningful modeling choice: a user can have several independent streaks running (one per daily habit) rather than one account-wide streak.
- **`Group` / `Challenge` / `Tag` / `Message`** round out the model — groups are how "parties" and "guilds" work (shared quests, shared task lists), challenges are shareable task templates, tags are just labels, and messages are chat/inbox content.

**Takeaway for Streakly:** if Streakly's real data model looks like this, the open question flagged back in `pm-brief.md` — "does the pass connect the *pre-break streak* or just the *best-streak stat*, and are those even the same number?" — has a concrete answer to check for: it depends on whether Streakly tracks streak per-lesson-track (like Habitica's per-Daily streak) or as one account-wide number. That's a question for Raj, not something this tour can answer, but it's now a sharper question to bring to him.
