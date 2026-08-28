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
| `affective-ceo.md` | The writing style Adam's own chats run on | every agent, at the start of a session |
| `worktree-reminder.py` | A hook, not a rule — see below | it runs; nobody reads it |
| `worktree-reminder.test.sh` | Checks that hook still speaks and stays quiet in the right places | run it after changing the hook |

## The one file here that is not words

`worktree-reminder.py` is a **hook**: a small program Claude Code runs by itself before every edit.
It speaks up when an edit is about to land in a shared project folder instead of in that chat's own
copy — rule 12 — and it stays quiet everywhere else.

It lives here for the same reason the rules do: **one copy, edited in one place.**

- **On Adam's Mac**, `~/.claude/hooks/worktree-reminder.py` is a symlink pointing at this file, and
  `~/.claude/settings.json` runs it before every Write and Edit.
- **In the cloud**, a run has none of his Mac, so it downloads this file at the start of every
  session and runs the copy it just fetched.

So editing it here changes both. Do not copy it into another repo — that is the thing this
arrangement exists to prevent.

**After changing it, run `./worktree-reminder.test.sh`.** A hook that is too noisy gets switched
off, and a hook that is too quiet is not there at all — and both look like success from the
outside. The first version watched only the Write and Edit tools, so a file changed with `sed`,
a heredoc or `>` sailed straight past it.

## The addresses to read them at

```
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/kiss.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/CLAUDE.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/filing-suggestions.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/routine-reports.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/writing-runbooks.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/affective-ceo.md
https://raw.githubusercontent.com/YesThats3DPrinted/claude-rules/main/worktree-reminder.py
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
