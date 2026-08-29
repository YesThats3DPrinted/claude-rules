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
| `writing-runbooks-reminder.py` | A hook, not a rule — see below | it runs; nobody reads it |
| `writing-runbooks-reminder.test.sh` | Checks that hook still speaks and stays quiet in the right places | run it after changing the hook |

## The files here that are not words

Two of these are **hooks**: small programs Claude Code runs by itself before every edit.

- `worktree-reminder.py` speaks up when an edit is about to land in a shared project folder
  instead of in that chat's own copy — rule 12.
- `writing-runbooks-reminder.py` speaks up when what is being written is a page somebody reads
  later, and says to load the `writing-runbooks` skill first.

Both stay quiet everywhere else.

They live here for the same reason the rules do: **one copy, edited in one place.**

- **On Adam's Mac**, each one has a symlink in `~/.claude/hooks/` pointing at this file, and
  `~/.claude/settings.json` runs it before every Write, Edit and Bash.
- **In the cloud**, a run has none of his Mac, so it downloads these files at the start of every
  session and runs the copies it just fetched.

So editing one here changes both places. Do not copy either into another repo — that is the thing
this arrangement exists to prevent.

**After changing a hook, run its test script.** A hook that is too noisy gets switched off, and a
hook that is too quiet is not there at all — and both look like success from the outside.

Two things both hooks had to learn the hard way, so do not undo either:

- **A file is often changed with Bash**, not with the Write or Edit tool. Watching only those two
  tools lets `sed`, a heredoc and `>` sail straight past.
- **A path after `cd` has no folder in it.** `cd <folder> && sed -i '' page.md` names the page
  alone, so the folder has to be put back on before you can tell where it lands.

`writing-runbooks-reminder.py` also reads **what is being written**, not only the file's name. A
page inside a skill folder can be called anything, so a name-only check misses most of them.

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
