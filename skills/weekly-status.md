---
name: weekly-status
description: Turn raw bullet-point notes into a formatted leadership update with Shipped, In Progress, Blockers, and Next Week sections.
---

# Weekly Status Skill

## When to use it

Use when you have raw, unordered bullet notes about the week's work and need a clean, leadership-ready status update.

## Input

Raw bullet-point notes — unstructured, any order, mixing completed work, ongoing work, issues, and future plans.

## Output

A formatted update with exactly these four sections, in this order:

1. **Shipped**
2. **In Progress**
3. **Blockers**
4. **Next Week**

## Rules

- Maximum 3 bullets per section
- Plain, declarative language — no jargon, no buzzwords
- One sentence per bullet, stating what happened or is happening
- If a section has no relevant notes, write "None" rather than omitting it
- If more than 3 items qualify for a section, keep the 3 most significant and drop the rest — don't compress multiple items into one bullet

## Example

**Input notes:**
- Fixed the login bug that was blocking QA
- Started the Comeback screen wireframes
- Waiting on data team for churn segment definitions
- Need legal review before ship
- Planning to finalize freeze rules next week
- Onboarding new engineer starts Monday

**Output:**

**Shipped**
- Fixed the login bug that was blocking QA

**In Progress**
- Comeback screen wireframes underway
- Legal review pending before ship

**Blockers**
- Waiting on data team for churn segment definitions

**Next Week**
- Finalize streak-freeze rules
- Onboard new engineer
