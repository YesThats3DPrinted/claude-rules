#!/usr/bin/env python3
"""Runs before every Write and Edit.

Speaks up when an edit is about to land in a shared project folder on `main`, instead of
in the session's own copy of it. CLAUDE.md rule 12: always a work tree.

Why it is a hook and not just the rule: the rule was already there and was broken anyway,
for a whole session, because every edit one at a time looked small enough to be the
exception. Meanwhile another chat was editing the same folder that morning. Noticing is
the part that fails, so this does not rely on noticing.

Speaks once per repository per session, and only when it would change something:

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
import subprocess
import sys
import tempfile

MESSAGE = (
    "Before editing {repo}: you are in the shared folder, on main. Another chat may be in "
    "the same one right now, and neither of you would be told. CLAUDE.md rule 12 — take "
    "this session's own copy first, and merge it back when the work is done and tested. "
    "There is no small-edit exception. If this IS one of Adam's routines, carry on: a "
    "routine reads main and must never be given a branch."
)


def git(repo: str, *args: str) -> str:
    """One git command in that folder, or "" if git has anything to say about it."""
    try:
        out = subprocess.run(("git", "-C", repo) + args, capture_output=True,
                             text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path:
        return 0

    folder = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(folder):
        return 0

    top = git(folder, "rev-parse", "--show-toplevel")
    if not top:
        return 0                                   # not in git — rule 12 says say so, not this

    # Already in a work tree? That is the whole ask. Its .git is a FILE pointing elsewhere,
    # where a normal checkout has a directory.
    if os.path.isfile(os.path.join(top, ".git")):
        return 0

    branch = git(folder, "rev-parse", "--abbrev-ref", "HEAD")
    if branch not in ("main", "master"):
        return 0                                   # on a branch — somebody has thought about it

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
