# claude-rules

The rules every Claude agent of Adam's reads — chats on his Mac, routines on his Mac, and routines
running in the cloud.

**This repo is public on purpose.** A cloud routine runs on a fresh machine that can see nothing of
Adam's Mac and holds no login for a private repo. Public means one plain web address it can always
read. **Nothing secret goes in here. Ever.** No passwords, no keys, no customer details.

## What is in it

| File | What it is | Who reads it |
| --- | --- | --- |
| `kiss.md` | How to write to Adam: short, plain words, no filler | every agent, on every message |
| `CLAUDE.md` | Adam's rules for how to work with him | every agent, at the start of a session |
| `filing-suggestions.md` | How a routine files an improvement suggestion | the routines, before filing one |
| `routine-reports.md` | How a routine writes its report and its summary emails | the routines, before reporting back |
| `writing-runbooks.md` | How to write anything somebody reads later: a runbook, a recipe, a how-to page | any agent about to write one |

## The addresses to read them at

```
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/kiss.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/CLAUDE.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/filing-suggestions.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/routine-reports.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/writing-runbooks.md
```

## Do not keep a second copy

The whole point is that there is **one** of each. A runbook points at the address above; it never
repeats what the file says. Copy a rule into a runbook and the two drift apart, which is the
problem this repo exists to kill.

## On Adam's Mac

`~/.claude/CLAUDE.md`, `~/.claude/hooks/kiss.md` and
`~/.claude/skills/writing-runbooks/SKILL.md` are **links** to the files in this folder, not
copies. So editing one here is the same as editing it there — nothing to keep in step.

After changing anything, push it, or the cloud routines carry on reading the old version:

```bash
git -C "$HOME/Adam work/Claude Code/claude-rules" add -A && git -C "$HOME/Adam work/Claude Code/claude-rules" commit -m "what changed" && git -C "$HOME/Adam work/Claude Code/claude-rules" push
```
