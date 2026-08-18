---
name: writing-runbooks
description: Use when writing or editing anything somebody reads LATER, with none of today's context. Two kinds. (1) Instructions an agent follows — a skill, a recipe, a routine or scheduled-task prompt, a runbook, an agent prompt, or a rule added to one. (2) Documentation — a how-to page, a write-up of how something works, a page under docs/, a README, a plan or project doc, notes explaining a feature to whoever comes next. Read it BEFORE writing, including when the page is a side-job of a coding task, and especially when you are about to record something you just learned, add a warning, or explain why a rule exists.
---

# Writing skills, recipes, routines and how-to pages

Somebody reads this **later**, with none of today's context. Write for that person.

That covers instructions an agent follows **and** documentation a person reads — a how-to page, a
write-up of how something works, a page under `docs/`, a README. Same job, same rules. A page
written as the tail end of a coding task is the one that slips through, because it feels like part
of the code rather than a thing anyone will read cold.

## The one rule: generic, not "what I was doing today"

State **what to do, and what goes wrong if you don't.** Stop there.

Cut the date, the order number, the customer name, the run it happened on, how many seconds it
took, the version it was fixed in. None of it helps anyone follow the rule, and a page of it buries
the rule itself.

- ❌ "On the 6th, order #2605 was flagged as marketing and the fix would have wiped its real
  delivery cost, so a minus line always means a refund."
- ✅ "A minus line is always a refund, never a marketing shipment. Zeroing its costs would delete a
  delivery charge that really was paid."

Both say the same thing. Only one still makes sense in a year.

**Keep a number only when the number IS the rule** — a limit, a rate, a threshold, a figure
something gets checked against. Drop measurements that were only ever proof it worked once.

**Keep a name only when the thing is called that.** A person's name in a rule is almost always
decoration.

**Write the shape of the problem, not the one time you hit it.** If your example only makes sense
to someone who was there, it isn't an example yet.

## Where the background goes

The runbook says **what to do**. Anything that is really the story of how something was worked out
belongs in a separate notes file, and the runbook links to it in one line.

If you cannot bring yourself to delete the story, that is the test that it belongs elsewhere.

## What you never trim

Cutting words is not cutting information. Keep, exactly as they are:

- every command, address, filename and setting;
- every message the thing prints, word for word, because that is what the reader matches against;
- every safety line: what must never happen, and what to do instead;
- what to do for each outcome, including the boring ones.

If a shorter version would leave someone guessing, it isn't shorter, it's broken.

## Keep the front page short

An entry file loads every time the skill fires. Put the facts that apply to everything there, then
point at the detailed page. See CLAUDE.md §10 for how the folder is laid out.

## Writing a routine's report or summary email

Don't. Those rules are shared by every routine and live in one file:

```
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/routine-reports.md
```

A runbook **points** at that address; it never repeats what the page says. Copy the rules into a
runbook and the two drift, and every routine ends up sounding different.

## Plain words

Same as everything else here: short sentences, easy words, no jargon, no filler. If a ten-year-old
couldn't follow it, rewrite it.
