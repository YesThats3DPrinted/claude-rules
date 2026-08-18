# How every routine reports back

**This file is the single set of rules. Every routine reads it before writing its report or its
summary email.** Change it here and every routine changes with it. Never copy these rules into a
runbook.

## Short. Exceptions only.

Adam's rule: *"stop writing so much shit in the end of routine summaries. only tell me anything
important, any anomalies, could not verify, that type of stuff. telling me the results of each
shipment and stock check, how many links you checked etc. doesn't help at all. those things live in
their respective sheets."*

## Checking and reporting are two different jobs

You still check everything. You still account for every step. What changes is that **a step that
worked gets no line at all.**

This is the part that gets confused. Cutting the report does not mean cutting the work, and a
routine that stops checking because it stopped reporting has broken itself.

## Write only these

Skip any that is empty:

- **Anything that failed, was skipped, or came back empty.** Name it and say why. A duty that
  returned nothing has **failed** — say so plainly, never write it up as clean.
- **Anything you could not verify**, with enough for Adam to look himself: the full address, the
  order number, whatever he would need.
- **Anomalies.** Something structurally wrong, a changed heading, a check that disagrees with
  itself. Say what you would do about it.
- **Anything needing Adam to act**, and exactly what the action is.
- **Every question you need him to answer**, and what it is about.

**If everything worked and nothing needs him, say so in one line and stop.** For example *"All six
duties clean, nothing to action."* That is a complete and correct report.

## Never write

- a list of every item you handled
- counts of how many things you read, checked or skipped
- "✅ done" ticks for steps that simply worked
- a restatement of what the routine does
- the same thing twice, in different words

## Say a thing once

Several items hit by one problem get **one** heading and the items listed under it. Not one
paragraph each.

*"No tracking number: A, B, C."* Then *"Couldn't update the delivery window: B, D, F."* Never six
near-identical paragraphs saying the same sentence over and over. Reading the same line six times
is the thing that makes a report feel like work.

The same goes for an email the routine sends: group by the problem, not by the item.

## Never guess how to reach him

A report is not a substitute for an escalation the runbook asks for, and an escalation is not a
substitute for the report. Do both, as written. Never reach for a phone notification or a question
prompt in place of the harder thing the runbook told you to do.
