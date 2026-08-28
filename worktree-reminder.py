#!/usr/bin/env python3
"""Runs before every Write, Edit and Bash command.

Speaks up when an edit is about to land in a shared project folder on `main`, instead of
in the session's own copy of it. CLAUDE.md rule 12: always a work tree.

Why it is a hook and not just the rule: the rule was already there and was broken anyway,
for a whole session, because every edit one at a time looked small enough to be the
exception. Meanwhile another chat was editing the same folder that morning. Noticing is
the part that fails, so this does not rely on noticing.

**Bash counts.** The first version watched only the Write and Edit tools, so a file changed
with `sed -i`, a heredoc, or `>` went straight past it — which is exactly how the shared
folder got edited again an hour after this hook was written. A command is read for the
paths it would WRITE to; reading, searching and git commands are ignored.

Speaks once per repository per session — the copy it asks for is per session too, not per
job — and only when it would change something:

- silent inside a work tree, which is the thing it is asking for;
- silent on a branch, since a branch means somebody already thought about it;
- silent for a folder that is not in git;
- silent for a routine, whose runs are told to push straight to `main`.

This file is the ONE copy. Adam's Mac reaches it through a symlink at
`~/.claude/hooks/worktree-reminder.py`; a cloud run downloads it from this repo at the start of
every session. Edit it here and both change together.

Plain python3 and nothing else — no `jq`, which is missing on the Mac, and no package anybody has
to install. A hook that cannot run fails silently and does nothing, which looks exactly like a
hook that is working.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

MESSAGE = (
    "Before editing {repo}: you are in the shared folder, on main. Another chat may be in "
    "the same one right now, and neither of you would be told. CLAUDE.md rule 12 — take "
    "this session's own copy first, and merge it back when the work is done and tested. "
    "There is no small-edit exception. ONE copy per chat, not per job — if you already made "
    "one here, use that. If this IS one of Adam's routines, carry on: a routine reads main "
    "and must never be given a branch."
)


def git(repo: str, *args: str) -> str:
    """One git command in that folder, or "" if git has anything to say about it."""
    try:
        out = subprocess.run(("git", "-C", repo) + args, capture_output=True,
                             text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


# Ways a bash command puts something ON DISK. Reading, searching and git are not here on
# purpose: `grep`, `cat`, `git log` and friends must never make this speak.
# A path as it can appear in a command: quoted, or a run of non-space characters. The quoted
# forms come FIRST and matter — Adam's folders have spaces in them ("Adam work"), so a pattern
# that stops at whitespace silently reads half a path and finds nothing.
_PATH = r"""(?:'([^']+)'|"([^"]+)"|([^\s;|&)]+))"""

# Ways a bash command puts something ON DISK. Reading, searching and git are not here on
# purpose: `grep`, `cat`, `git log` and friends must never make this speak.
WRITES = (
    re.compile(r"(?<![0-9&])>>?\s*" + _PATH),                       # > file and >> file
    # sed -i writes the file it is given. On this Mac it takes an empty backup suffix first
    # (`sed -i '' …`), so the path is simply the LAST thing on the line, not the second.
    re.compile(r"\bsed\s+[^;|&]*?-i[^;|&]*?" + _PATH + r"\s*(?:$|[;|&])"),
    # these take a source and then a destination
    re.compile(r"\b(?:cp|mv|install)\s+(?:-[^\s]+\s+)*(?:'[^']+'|\"[^\"]+\"|[^\s]+)\s+" + _PATH),
    # these take only a destination
    re.compile(r"\b(?:tee|truncate|touch|mkdir)\s+(?:-[^\s]+\s+)*" + _PATH),
    re.compile(r"\bopen\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"][wa]"),   # python open(path,'w')
)

# `cd <somewhere> && …` — the folder the rest of the command runs in.
CD = re.compile(r"\bcd\s+" + _PATH)


def _first(match) -> str:
    """The one group that actually matched, whichever quoting was used."""
    return next((g for g in match.groups() if g), "")


def targets(command: str) -> list:
    """Every path this command might write to, plus any folder it cds into."""
    out = [_first(m) for pattern in WRITES for m in pattern.finditer(command)]
    # Throw away the throwaways BEFORE deciding whether this command writes anything at all —
    # otherwise `ls > /dev/null` counts as a write and drags the folder it ran in in with it.
    out = [p for p in out if p and not p.startswith("/dev/")]
    if out:                       # only care where it runs if it writes something real
        out += [_first(m) for m in CD.finditer(command)]
    return [p for p in out if p]


def shared_repo(path: str) -> str:
    """The repo this path sits in, but only if it is the SHARED checkout on main.

    Empty for a work tree, a branch, or anything not in git — all three mean somebody has
    already thought about it, or there is nothing to think about.
    """
    path = os.path.expanduser(path.strip().strip("'\""))
    if not os.path.isabs(path):
        return ""                 # relative to a cwd we cannot know from here
    # A path inside a work tree is the thing being asked for, whether or not it exists yet.
    if "/.claude/worktrees/" in path:
        return ""
    folder = path if os.path.isdir(path) else os.path.dirname(path)
    while folder and not os.path.isdir(folder):
        folder = os.path.dirname(folder)
    if not folder:
        return ""
    top = git(folder, "rev-parse", "--show-toplevel")
    if not top:
        return ""
    # A work tree's .git is a FILE pointing elsewhere; a normal checkout has a directory.
    if os.path.isfile(os.path.join(top, ".git")):
        return ""
    if git(folder, "rev-parse", "--abbrev-ref", "HEAD") not in ("main", "master"):
        return ""
    return top


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = payload.get("tool_input") or {}

    if payload.get("tool_name") == "Bash":
        candidates = targets(tool_input.get("command") or "")
    else:
        candidates = [tool_input.get("file_path") or ""]

    top = next((r for r in (shared_repo(c) for c in candidates if c) if r), "")
    if not top:
        return 0

    key = hashlib.sha256(f"{payload.get('session_id', '')}|{top}".encode()).hexdigest()[:20]
    stamp = os.path.join(tempfile.gettempdir(), f"claude-worktree-reminder-{key}")
    if os.path.exists(stamp):
        return 0
    try:
        open(stamp, "w").close()
    except OSError:
        pass

    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": MESSAGE.format(repo=os.path.basename(top)),
    }}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
